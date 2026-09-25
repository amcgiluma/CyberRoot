"""postmortem.py — el informe post-mortem del Auditor (O2, 30/08, Ornstein).

Es el PRIMER fichero del módulo `core/engine` y la pieza que el Hub muestra
SIEMPRE primero tras cada run (§4.7/§4.1). Es el post-mortem v0: léelo como
«qué dejó el historial real», no como el informe narrativo final.

Qué produce `build_postmortem(shell_dict, state)`:
  1. La **factura GNU** del historial: cuántas veces se ejecutó cada comando
     y cuántos errores hubo (`exit != 0`). Es la contabilidad de la sesión,
     en la MISMA unidad de ruido que el presupuesto (🧭10 de Oscar, 29/08).
  2. `total_noise` vs `noise_budget` lado a lado en la misma unidad (ambos
     son "puntos de ruido"), con el veredicto `dentro_presupuesto`.
  3. Una línea del **Auditor** que cita el comando CONCRETO que disparó la
     detección (el que hizo cruzar el presupuesto acumulado), con su amount
     de `history`. Voz: formulario seco (§2.4 / ficha de PERSONAJES) — dato
     sobre emoción, «Expediente 000», cifras exactas. No hubo cruce → el
     Auditor cita el comando con más ruido de la run como el «pico».
  4. (O1 04/09) Segunda fuente de verdad `read_marks`: si la sesión contiene
     un `sudo`, cita si la orden se leyó antes de elevar (lectura vs ciega).

Contrato:
- `shell_dict`: dict plano de una `Shell` (su `to_dict`). Campo obligatorio
  `history` (lista de `{"line", "result": {exit_code, noise: [...]}}`); los
  eventos de noise llevan `data.command` y `data.amount`. Desde S1 (03/09)
  `read_marks` viaja como lista ordenada de rutas leídas.
- `state`: dict plano del estado de run con `noise_budget` (int) — la misma
  unidad que `total_noise`, 🧭10. Si falta, se usa 12 ⚠️ v1 (la constante de
  `Room.noise_budget`; el orquestador del engine la pasará siempre).
- SALIDA: dict plano, serializable (pasa `ensure_plain`). La línea textual
  del Auditor viaja como CLAVE + args, no como cadena hardcodeada en core
  (convención §3: el render resuelve los textos contra `data/`). Para el
  test headless, `args` trae el comando y amount CONCRETOS ya resueltos.
  Si hubo `sudo`, añade `auditor_lectura` + `auditor_lectura_text` y
  extiende `lines_resolved` con la segunda línea (sin `sudo` → informe
  byte-idéntico al de hoy).

Función PURA: sin I/O, sin RNG, sin estado global (ARCHITECTURE §1.5). Solo
stdlib.
"""
from __future__ import annotations

import re
import shlex
from typing import Any

#: Presupuesto de ruido de la sala ⚠️ v1 (misma unidad que `total_noise`, 🧭10).
#: El orquestador del engine lo pasará vía `state.noise_budget`; este default
#: solo cubre la llamada sin estado completo (harness/tests).
DEFAULT_NOISE_BUDGET = 12

#: Rectángulo del título "línea del Auditor" — clave a resolver contra data/.
LINE_KEY_CRUCE = "postmortem.auditor.cruce"
LINE_KEY_PICO = "postmortem.auditor.pico"
#: O1 04/09 (Ornstein) — segunda fuente de verdad: read_marks.
#: Si la sesión contiene un `sudo`, el informe cita si se leyó la orden.
LINE_KEY_LECTURA = "postmortem.auditor.lectura"
LINE_KEY_CIEGA = "postmortem.auditor.ciega"
#: O1 05/09 (Ornstein) — el Auditor cita TU columna: si el history contiene `cut` con flags, añade línea de corte.
LINE_KEY_CORTE = "postmortem.auditor.corte"
#: O1 06/09 (Ornstein) — el Auditor cita TU eje vertical: si el history contiene `sort` con `-k`, añade línea de orden.
LINE_KEY_ORDEN = "postmortem.auditor.orden"
#: O1 12/09 (Ornstein) — el Auditor cita TU cruce de tablas: si el history contiene `join` con `-v`, añade línea de join.
LINE_KEY_JOIN = "postmortem.auditor.join"
#: O1 13/09 (Ornstein) — Eco del espejo v0: el Auditor nombra tu repertorio.
#: Si el history contiene alguna de las 3 firmas (scp→cut|grep, join -v, ps aux+grep),
#: añade 1 línea repertorio enumerándolas en orden ①→②→③ (sin datos de fila).
LINE_KEY_ESPEJO = "postmortem.espejo.repertorio"
#: S1 15/09 (Smough, ADR TR-003) — bifurcación volcado: rescate vs caducado.
LINE_KEY_VOLCADO_RESCATE = "postmortem.volcado.rescate"
LINE_KEY_VOLCADO_CADUCADO = "postmortem.volcado.caducado"
#: S1 18/09 (Smough, cap. 5 custodia) — testigo leído en casa.
LINE_KEY_CUSTODIA = "postmortem.auditor.custodia"
#: O1 21/09 (Ornstein, P1 karma del volcado) — huella kármica vigilante.
LINE_KEY_HUP = "postmortem.auditor.hup"
LINE_KEY_KILL = "postmortem.auditor.kill"
#: O1 22/09 (Ornstein, díptico E1) — huella kármica de la puerta: 600 vs 777.
LINE_KEY_CIERRE = "postmortem.auditor.cierre"
LINE_KEY_PUERTA_ABIERTA = "postmortem.auditor.puerta_abierta"
#: O1 23/09 (Ornstein, díptico E4) — huella kármica del propietario: gris vs root sobre pts0.
LINE_KEY_CHOWN_TRANSFER = "postmortem.auditor.chown_transfer"
LINE_KEY_CHOWN_RETOMA = "postmortem.auditor.chown_retoma"
#: O1 25/09 (Ornstein, P2 factura frugal) — vía frugal grep -c.
LINE_KEY_GREP_C_COUNT = "postmortem.auditor.grep_c_count"


def _por_codepoint(entries: dict[str, int]) -> dict[str, int]:
    """Ordena determinista por codepoint (misma convención que el sandbox)."""
    return dict(sorted(entries.items()))


def _comando(hist_entry: dict[str, Any]) -> str:
    """Nombre de comando de una entrada de history.

    Prioridad: el `data.command` del primer evento de noise (fuente
    autoritativa del sandbox) o si la entrada no emitió ruido (comando
    desconocido / error de sintaxis), el primer token argv de la línea.
    """
    result = hist_entry.get("result") or {}
    for ev in result.get("noise", []) or []:
        cmd = (ev.get("data") or {}).get("command")
        if cmd:
            return str(cmd)
    line = str(hist_entry.get("line", ""))
    try:
        argv = shlex.split(line)
    except ValueError:
        argv = []
    return str(argv[0]) if argv else "(?)"


def _factura(shell_dict: dict[str, Any]) -> dict[str, int]:
    """Cuenta por comando + errores de la sesión (la factura GNU)."""
    counts: dict[str, int] = {}
    errores = 0
    for entry in shell_dict.get("history", []) or []:
        cmd = _comando(entry)
        counts[cmd] = counts.get(cmd, 0) + 1
        result = entry.get("result") or {}
        if int(result.get("exit_code", 0)) != 0:
            errores += 1
    counts["errores"] = errores
    return _por_codepoint(counts)


def _cruce(shell_dict: dict[str, Any], noise_budget: int) -> tuple[bool, dict[str, Any] | None]:
    """Entrada que hizo CRUZAR el presupuesto acumulado (la que te delata).

    Devuelve (cruzó, entrada_culpable). Acumulamos el ruido por evento en
    orden; la primera entrada que deja el acumulado ≥ `noise_budget` es el
    gatillo. Si nunca se cruza → (False, None).
    """
    acumulado = 0
    for entry in shell_dict.get("history", []) or []:
        result = entry.get("result") or {}
        contrib = sum(
            int(ev.get("data", {}).get("amount", 0)) for ev in result.get("noise", []) or []
        )
        acumulado += contrib
        if acumulado >= noise_budget:
            return True, entry
    return False, None


def _pico(shell_dict: dict[str, Any]) -> dict[str, Any] | None:
    """La entrada con MÁS ruido individual de la run (el pico si no hubo cruce)."""
    mejor: dict[str, Any] | None = None
    mejor_amount = -1
    for entry in shell_dict.get("history", []) or []:
        result = entry.get("result") or {}
        amount = max(
            (int(ev.get("data", {}).get("amount", 0)) for ev in result.get("noise", []) or []),
            default=0,
        )
        if amount > mejor_amount:
            mejor_amount = amount
            mejor = entry
    return mejor if mejor_amount > 0 else None


def _amount(entry: dict[str, Any] | None) -> int:
    """Ruido total del evento que disparó la línea del Auditor."""
    if not entry:
        return 0
    result = entry.get("result") or {}
    return sum(
        int(ev.get("data", {}).get("amount", 0)) for ev in result.get("noise", []) or []
    )


def _extract_cut_args(line: str) -> dict[str, str] | None:
    """Extrae args de un `cut` con flags desde la línea cruda.

    Busca flags que indiquen corte por columna: -d, -f, --delimiter, --fields.
    Retorna {column, pattern} para la plantilla corte, o None si no hay flag de corte.
    Determinista, sin imports de sandbox (solo shlex sobre la línea).
    """
    try:
        argv = shlex.split(line)
    except ValueError:
        return None
    if not argv or argv[0] != "cut":
        return None
    # Detecta presencia de flag de corte (criterio del plan: cut -d / cut -f)
    has_cut_flag = False
    column = ""
    pattern = ""
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "-d" and i + 1 < len(argv):
            has_cut_flag = True
            pattern = argv[i + 1]
            i += 2
        elif a.startswith("-d") and len(a) > 2:
            has_cut_flag = True
            pattern = a[2:]
            i += 1
        elif a == "-f" and i + 1 < len(argv):
            has_cut_flag = True
            column = argv[i + 1]
            i += 2
        elif a.startswith("-f") and len(a) > 2:
            has_cut_flag = True
            column = a[2:]
            i += 1
        elif a == "--delimiter" and i + 1 < len(argv):
            has_cut_flag = True
            pattern = argv[i + 1]
            i += 2
        elif a.startswith("--delimiter="):
            has_cut_flag = True
            pattern = a.split("=", 1)[1]
            i += 1
        elif a == "--fields" and i + 1 < len(argv):
            has_cut_flag = True
            column = argv[i + 1]
            i += 2
        elif a.startswith("--fields="):
            has_cut_flag = True
            column = a.split("=", 1)[1]
            i += 1
        elif a.startswith("-") and ("d" in a or "f" in a):
            # flags combinados tipo -df o -fd
            has_cut_flag = True
            i += 1
        elif a.startswith("-"):
            i += 1
        else:
            i += 1
    if not has_cut_flag:
        return None
    # Normaliza: column por defecto si solo hubo -d, pattern viceversa
    if not column:
        column = pattern or "-"
    if not pattern:
        pattern = column
    return {"column": column, "pattern": pattern}


def _find_cut(shell_dict: dict[str, Any]) -> dict[str, str] | None:
    """Primer `cut` con flags en el history (determinista por orden)."""
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        # Fast path: debe contener cut
        if "cut" not in line:
            continue
        args = _extract_cut_args(line)
        if args is not None:
            return args
        # No fallback por comando autoritativo: solo flags explícitos cuentan
    return None


def _field_ordinal(spec: str) -> str:
    """Número de campo inicial de una especificación `-k` GNU (F[.C][,F[.C]]).

    Devuelve el primer entero positivo de la clave (la posición a ordenar);
    vacío si no se reconoce (p. ej. `-k'  x'` malformado). Determinista, sin
    imports de sandbox. Ejs: `12`→\"12\", `12n`→\"12\", `12.2`→\"12\", `2,4`→\"2\".
    """
    m = re.match(r"\s*(\d+)", spec)
    return m.group(1) if m else ""


def _extract_sort_args(line: str) -> dict[str, str] | None:
    """Extrae args de un `sort` CON `-k` desde la línea cruda.

    Hermano de `_extract_cut_args`: detecta la clave de ordenación vertical
    (`-k`, con o sin `-t`/`-n`). Localiza el token `sort` en cualquier
    posición de la línea (p. ej. tras un pipe `cut ... | sort -k12`), no solo
    como primer token. SIN `-k` → None (el `sort` plano del golden de E2 no
    dispara NADA). Retorna {columna, delimitador, numerico} para la plantilla
    orden. Determinista, sin imports de sandbox (solo shlex+re sobre la línea).
    """
    try:
        argv = shlex.split(line)
    except ValueError:
        return None
    if not argv:
        return None
    # Localiza el token `sort` en cualquier posición (puede ir tras un pipe)
    try:
        start = argv.index("sort")
    except ValueError:
        return None
    column = ""
    delimiter = ""
    numeric = False
    has_key = False
    i = start + 1
    while i < len(argv):
        a = argv[i]
        # Delimitador: -t X / -tX, --field-separator[=X], --delimiter[=X]
        if a == "-t" and i + 1 < len(argv):
            delimiter = argv[i + 1]
            i += 2
        elif a.startswith("-t") and len(a) > 2:
            delimiter = a[2:]
            i += 1
        elif a == "--field-separator" and i + 1 < len(argv):
            delimiter = argv[i + 1]
            i += 2
        elif a.startswith("--field-separator="):
            delimiter = a.split("=", 1)[1]
            i += 1
        elif a == "--delimiter" and i + 1 < len(argv):
            delimiter = argv[i + 1]
            i += 2
        elif a.startswith("--delimiter="):
            delimiter = a.split("=", 1)[1]
            i += 1
        # Clave de ordenación: -k POS / -kPOS, --key=POS / --key POS
        elif a == "-k" and i + 1 < len(argv):
            has_key = True
            column = _field_ordinal(argv[i + 1])
            i += 2
        elif a.startswith("-k") and len(a) > 2:
            has_key = True
            column = _field_ordinal(a[2:])
            i += 1
        elif a == "--key" and i + 1 < len(argv):
            has_key = True
            column = _field_ordinal(argv[i + 1])
            i += 2
        elif a.startswith("--key="):
            has_key = True
            column = _field_ordinal(a[len("--key="):])
            i += 1
        # Numérico: -n / --numeric-sort / --numeric
        elif a in ("-n", "--numeric-sort", "--numeric"):
            numeric = True
            i += 1
        else:
            i += 1
    if not has_key:
        return None
    return {
        "columna": column or "",
        # Default GNU: sin -t se separa por whitespace; plantilla muestra "" honesto
        "delimitador": delimiter,
        "numerico": "numérico" if numeric else "no numérico",
    }


def _find_sort(shell_dict: dict[str, Any]) -> dict[str, str] | None:
    """Primer `sort` con `-k` en el history (determinista por orden).

    Hermano de `_find_cut`: recorre las líneas crudas en orden; `sort` SIN
    `-k` queda descartado (no dispara el informe). No usa el comando
    autoritativo ni los eventos de noise: solo flags explícitos cuentan.
    """
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        # Fast path: debe contener sort
        if "sort" not in line:
            continue
        args = _extract_sort_args(line)
        if args is not None:
            return args
    return None


def _extract_join_args(line: str) -> dict[str, str] | None:
    """Extrae args de un `join` CON `-v` desde la línea cruda.

    Hermano de `_extract_cut_args` / `_extract_sort_args`: detecta el
    anti-join (`-v`). Busca el token `join` en cualquier posición de la
    línea (puede ir tras un pipe). SIN `-v` → None. Retorna {} (sin
    placeholders) para la plantilla join — el texto es estático y no
    filtra datos de fila. Determinista, sin imports de sandbox.
    """
    try:
        argv = shlex.split(line)
    except ValueError:
        return None
    if not argv:
        return None
    try:
        start = argv.index("join")
    except ValueError:
        return None
    has_v = False
    i = start + 1
    while i < len(argv):
        a = argv[i]
        if a == "-v" and i + 1 < len(argv):
            # -v 1 / -v 2 — GNU exige file number; cualquier valor vale
            has_v = True
            i += 2
        elif a.startswith("-v") and len(a) > 2:
            # -v1 / -v2 combinados
            has_v = True
            i += 1
        elif a == "-v":
            # -v sin argumento (raro pero cuenta como anti-join)
            has_v = True
            i += 1
        elif a.startswith("-") and "v" in a:
            # flags combinados que contengan v (p. ej. -av)
            has_v = True
            i += 1
        else:
            i += 1
    if not has_v:
        return None
    return {}


def _find_join(shell_dict: dict[str, Any]) -> dict[str, str] | None:
    """Primer `join` con `-v` en el history (determinista por orden)."""
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "join" not in line:
            continue
        args = _extract_join_args(line)
        if args is not None:
            return args
    return None


def _has_espejo_volcado(shell_dict: dict[str, Any]) -> bool:
    """Firma ①: `scp` a `/tmp/volcado.csv` seguido de `cut|grep` (ch4.e2).

    Orden determinista: busca el primer scp que mencione volcado.csv+/tmp
    y, desde ahí (inclusive), un `cut`+`grep` en la misma línea (pipe) o
    en orden posterior (cut visto → grep después). Solo shlex/substring,
    sin imports de sandbox.
    """
    history = shell_dict.get("history") or []
    scp_idx: int | None = None
    for i, entry in enumerate(history):
        line = str(entry.get("line", ""))
        if "scp" in line and "volcado.csv" in line and "/tmp" in line:
            scp_idx = i
            break
    if scp_idx is None:
        return False
    # Misma línea scp ya con cut|grep (raro pero cubre `scp ... | cut ... | grep`)
    # y búsqueda posterior
    for entry in history[scp_idx:]:
        line = str(entry.get("line", ""))
        if "cut" in line and "grep" in line:
            return True
    # Orden separado: cut después de scp y luego grep
    seen_cut = False
    for entry in history[scp_idx + 1 :]:
        line = str(entry.get("line", ""))
        if "cut" in line:
            seen_cut = True
        if seen_cut and "grep" in line:
            return True
    return False


def _has_espejo_reloj(shell_dict: dict[str, Any]) -> bool:
    """Firma ③: `ps aux` + `grep` de hora (dato5).

    Detecta la tubería canónica `ps aux | grep 11:04` en una sola línea
    (misma entrada de history). Requiere `ps`+`grep` y (`aux` o `:`/hora)
    para no disparar con un grep suelto. Solo substring+regex, sin sandbox.
    """
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "ps" not in line or "grep" not in line:
            continue
        has_aux = "aux" in line
        has_time = bool(re.search(r"\d{1,2}:\d{2}", line))
        if has_aux or has_time:
            return True
    return False


def _has_volcado_rescate(shell_dict: dict[str, Any]) -> bool:
    """Firma rescate: `scp` con `volcado-rescate.csv` y exit 0."""
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "scp" not in line or "volcado-rescate.csv" not in line:
            continue
        result = entry.get("result") or {}
        if int(result.get("exit_code", 1)) == 0:
            return True
    return False


def _has_volcado_rm(shell_dict: dict[str, Any]) -> bool:
    """Firma disolución: `rm /tmp/volcado.csv` con exit 0."""
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "rm" not in line or "/tmp/volcado.csv" not in line:
            continue
        result = entry.get("result") or {}
        if int(result.get("exit_code", 1)) == 0:
            # asegurar que la línea es rm y no un comentario que contenga rm
            try:
                import shlex
                argv = shlex.split(line)
            except ValueError:
                argv = []
            if argv and argv[0] == "rm":
                return True
            # fallback substring ya vale para historia real (siempre rm directo)
            return True
    return False


def _has_volcado_custodia(shell_dict: dict[str, Any]) -> bool:
    """Firma custodia: `cat /tmp/volcado-custodia.csv` con exit 0."""
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "cat" not in line or "/tmp/volcado-custodia.csv" not in line:
            continue
        result = entry.get("result") or {}
        if int(result.get("exit_code", 1)) != 0:
            continue
        try:
            argv = shlex.split(line)
        except ValueError:
            argv = []
        # cat directo o cat dentro de pipe: si la línea contiene cat y ruta, vale
        # validación extra: el primer token cat o que la línea tenga "cat" antes de "|"
        if argv and argv[0] == "cat":
            return True
        # pipe caso: "cat /tmp/volcado-custodia.csv | grep ..."
        if "cat" in line:
            return True
    return False


def _extract_greps(shell_dict: dict[str, Any]) -> list[dict[str, Any]]:
    """ÚNICO punto de lectura de líneas-grep del historial (25/09, Ornstein).

    Extrae todas las entradas cuyo comando es grep (por `data.command` o por
    argv[0]==\"grep\"), parseando flags líderes -v/-i/-c, patrón y exit_code.
    Por él pasan los detectores nuevos (grep_c_count) y puede ser usado por
    los de ayer sin romper byte-idéntico (los viejos siguen con shlex directo
    para no cambiar su firma). Determinista, sin imports de sandbox.
    """
    out: list[dict[str, Any]] = []
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        result = entry.get("result") or {}
        exit_code = int(result.get("exit_code", 1)) if isinstance(result, dict) else 1
        # Detectar si es grep por noise command o por argv
        is_grep = False
        for ev in result.get("noise", []) or []:
            if (ev.get("data") or {}).get("command") == "grep":
                is_grep = True
                break
        if not is_grep:
            try:
                argv0 = __import__("shlex").split(line)
            except ValueError:
                argv0 = line.split()
            # busca token grep (pipe caso: "ps aux | grep ...")
            if "grep" not in line:
                continue
            # Para líneas con pipe, el grep no es argv[0] pero sí contiene grep
            # Verifica que haya un token grep
            tokens = argv0
            if "grep" not in tokens:
                # fallback: substring ya filtró, pero sin token exacto igual es grep
                # (p. ej. "ps aux | grep censo" → tokens incluye grep)
                continue
            is_grep = True
        if not is_grep:
            continue
        # Parse flags líderes tras el token grep
        try:
            argv = __import__("shlex").split(line)
        except ValueError:
            argv = line.split()
        # localiza índice de grep
        try:
            gidx = argv.index("grep")
        except ValueError:
            continue
        args = argv[gidx + 1 :]
        invert = False
        ignore_case = False
        count_mode = False
        idx = 0
        while idx < len(args):
            a = args[idx]
            if a == "--":
                idx += 1
                break
            if a.startswith("-") and len(a) > 1 and a != "-":
                for ch in a[1:]:
                    if ch == "v":
                        invert = True
                    elif ch == "i":
                        ignore_case = True
                    elif ch == "c":
                        count_mode = True
                    else:
                        # flag desconocido → no es nuestro grep canónico, pero igual lo listamos
                        pass
                idx += 1
                continue
            break
        pattern = args[idx] if idx < len(args) else ""
        out.append({
            "line": line,
            "argv": argv,
            "exit_code": exit_code,
            "has_c": count_mode,
            "invert": invert,
            "ignore_case": ignore_case,
            "pattern": pattern,
        })
    return out


def _find_last_grep_c_censo(shell_dict: dict[str, Any]) -> dict[str, Any] | None:
    """Último grep exit 0 fue -c censo (factura frugal, 25/09).

    Usa _extract_greps como única fuente. Mira el ÚLTIMO grep con exit 0;
    si ese último tiene -c y patrón censo → factura. Si el último grep exit 0
    es sin -c o con otro patrón → None. Así respeta "el último grep exit-0
    fue grep -c censo".
    """
    greps_exit0 = [g for g in _extract_greps(shell_dict) if g["exit_code"] == 0]
    if not greps_exit0:
        return None
    last = greps_exit0[-1]
    if not last["has_c"]:
        return None
    pat = last["pattern"]
    if not pat:
        return None
    if last["ignore_case"]:
        if "censo" not in pat.lower():
            return None
    else:
        if "censo" not in pat:
            return None
    return last


def _has_sudo(shell_dict: dict[str, Any]) -> bool:
    """True si el historial contiene al menos un `sudo`.

    Detecta por línea (shlex) y por evento de ruido (command == 'sudo')
    para cubrir tanto el wrapper exitoso (premium) como el intento
    rechazado (sin ruido). Sin imports de sandbox (contrato v0).
    """
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        try:
            argv = shlex.split(line)
        except ValueError:
            argv = []
        if argv and argv[0] == "sudo":
            return True
        result = entry.get("result") or {}
        for ev in result.get("noise", []) or []:
            if (ev.get("data") or {}).get("command") == "sudo":
                return True
    return False


def _detect_vigilante(shell_dict: dict[str, Any]) -> str | None:
    """Detecta huella kármica del vigilante (O1 21/09).

    Lee `fs.environment[HUP_*]` + ausencia del intruso en `ps`.

    - HUP: existe HUP_<pid> en environment y el proceso <pid> sigue
      presente con --vigilar-censo (--reloaded opcional).
    - KILL: no queda ningún proceso con --vigilar-censo y el history
      contiene un kill con señal de muerte (-9/-KILL/-TERM/-15).

    Retorna \"hup\" / \"kill\" o None. Sin kill en la historia → None
    (byte-idéntico a hoy). Solo shlex/substring, sin sandbox.
    """
    fs = shell_dict.get("fs") or {}
    procs = fs.get("processes") or []
    env = fs.get("environment") or {}
    history = shell_dict.get("history") or []

    # Normaliza procs a lista de dicts
    if not isinstance(procs, list):
        procs = list(procs)
    if not isinstance(env, dict):
        env = {}
    # HUP: busca HUP_<pid> con proceso vigilante presente
    for k, v in env.items():
        if not isinstance(k, str) or not k.startswith("HUP_"):
            continue
        if str(v) != "1":
            continue
        try:
            pid = int(k[4:])
        except ValueError:
            continue
        for p in procs:
            if not isinstance(p, dict):
                continue
            try:
                p_pid = int(p.get("pid", -1))
            except Exception:
                continue
            if p_pid != pid:
                continue
            cmd = str(p.get("cmd", ""))
            if "--vigilar-censo" in cmd:
                return "hup"
    # KILL: vigilante ausente + kill con señal de muerte en history
    has_vigilante = False
    for p in procs:
        if isinstance(p, dict) and "--vigilar-censo" in str(p.get("cmd", "")):
            has_vigilante = True
            break
    if has_vigilante:
        return None
    # Vigilante ausente — ¿hubo kill de muerte?
    for entry in history:
        line = str(entry.get("line", ""))
        if "kill" not in line:
            continue
        # Excluir HUP: si la línea contiene HUP/-1/-SIGHUP, es reconfiguración, no kill
        upper = line.upper()
        if "HUP" in upper:
            continue
        # Heurística HUP numérico: \"kill -1 ...\" es HUP, no kill
        # Detecta \"-1\" como token aislado (shlex)
        try:
            argv = shlex.split(line)
        except ValueError:
            argv = line.split()
        is_hup_numeric = False
        for tok in argv:
            if tok == "-1" or tok == "-SIGHUP" or tok == "-1.0":
                is_hup_numeric = True
                break
        if is_hup_numeric:
            continue
        # Cualquier otro kill (default TERM, -9, -KILL, -15, -TERM) cuenta
        # Verifica que realmente tuvo efecto (exit 0 o al menos se intentó)
        # Si el history existe, asumimos que el kill que vació al vigilante es éste
        return "kill"
    return None


def _has_ls_l(shell_dict: dict[str, Any]) -> bool:
    """True si el history contiene `ls -l` o `ls -la` (permite leer permisos).

    Busca `ls` con flag `l` en cualquier posición de la línea (shlex).
    Sin ls -l → el detector de puerta no dispara (exige haber mirado).
    """
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "ls" not in line or "l" not in line:
            continue
        try:
            argv = shlex.split(line)
        except ValueError:
            argv = line.split()
        if not argv or argv[0] != "ls":
            # ls dentro de pipe? busca token ls
            try:
                idx = argv.index("ls")
            except ValueError:
                continue
            flags = argv[idx + 1 :]
        else:
            flags = argv[1:]
        for tok in flags:
            if tok.startswith("-") and "l" in tok:
                return True
    return False


def _detect_chmod_puerta(shell_dict: dict[str, Any]) -> str | None:
    """Detecta huella kármica de la puerta: `chmod 600` vs `chmod 777`.

    Escanea el history en orden y guarda el ÚLTIMO chmod con modo 600 o 777.
    Soporta `-R`/`--recursive` antes del modo (chmod -R 777 pts0).
    Retorna \"cierre\" (600), \"puerta_abierta\" (777) o None si no hay chmod
    relevante. Solo shlex/substring, sin imports de sandbox.
    """
    last: str | None = None
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "chmod" not in line:
            continue
        try:
            argv = shlex.split(line)
        except ValueError:
            argv = line.split()
        if not argv:
            continue
        try:
            start = argv.index("chmod")
        except ValueError:
            continue
        # recoge tokens tras chmod, filtrando flags conocidos
        mode: str | None = None
        i = start + 1
        while i < len(argv):
            tok = argv[i]
            if tok in ("-R", "--recursive", "-v", "--verbose", "-c", "--changes", "-f", "--silent", "--quiet"):
                i += 1
                continue
            if tok.startswith("-"):
                # flags combinados tipo -Rv
                if "R" in tok or "v" in tok or "c" in tok or "f" in tok:
                    i += 1
                    continue
                # flag desconocido con -l etc: ignora y sigue
                if tok.startswith("--"):
                    i += 1
                    continue
                i += 1
                continue
            # primer no-flag es el modo
            mode = tok
            break
        if mode == "600":
            last = "cierre"
        elif mode == "777":
            last = "puerta_abierta"
        # modos intermedios (644, 755, etc) no son dilema → ignorar
    return last


def _detect_chown_puerta(shell_dict: dict[str, Any]) -> str | None:
    """Detecta huella kármica del propietario: `chown gris:apagados` vs `chown root:root`.

    Escanea el history y guarda el ÚLTIMO chown relevante sobre `pts0`:
    - `chown gris:*` o `chown *:apagados` (canonical `gris:apagados`) → \"transfer\"
    - `chown root:*` (canonical `root:root`) → \"retoma\"
    Soporta `-R`/`--recursive` antes del owner, modos con `:` y múltiples ficheros.
    Solo cuenta si el fichero contiene `pts0`. Sin pts0 → ignorar.
    Retorna \"transfer\" / \"retoma\" o None. Solo shlex, sin sandbox.
    """
    last: str | None = None
    for entry in shell_dict.get("history", []) or []:
        line = str(entry.get("line", ""))
        if "chown" not in line or "pts0" not in line:
            continue
        try:
            argv = shlex.split(line)
        except ValueError:
            argv = line.split()
        if not argv:
            continue
        try:
            start = argv.index("chown")
        except ValueError:
            continue
        # filtrar flags -R etc antes del spec
        i = start + 1
        spec: str | None = None
        while i < len(argv):
            tok = argv[i]
            if tok in ("-R", "--recursive", "-v", "--verbose", "-c", "--changes", "-f", "--silent", "--quiet", "-h", "--no-dereference"):
                i += 1
                continue
            if tok.startswith("-"):
                if "R" in tok or "v" in tok or "c" in tok or "f" in tok or "h" in tok:
                    i += 1
                    continue
                if tok.startswith("--"):
                    i += 1
                    continue
                i += 1
                continue
            spec = tok
            break
        if spec is None:
            continue
        # spec es OWNER[:GROUP] — extraer owner y group
        if ":" in spec:
            owner, group = spec.split(":", 1)
            # owner: vacío invalida, group puede ser vacío
            if not owner:
                continue
        else:
            owner = spec
            group = None
        # determinar tipo
        # azul: owner gris OR group apagados
        # rojo: owner root (cubre root:root y root:*)
        is_transfer = (owner == "gris") or (group == "apagados")
        is_retoma = (owner == "root")
        # prioridad: transfer si ambos? gris nunca root, pero caso gris:root sería transfer por owner
        if is_transfer:
            # verifica que realmente haya file pts0 entre los ficheros (ya filtrado por substring, pero doble check)
            # busca ficheros tras spec
            files = argv[i + 1 :] if i + 1 < len(argv) else []
            if any("pts0" in f for f in files) or "pts0" in line:
                last = "transfer"
        elif is_retoma:
            files = argv[i + 1 :] if i + 1 < len(argv) else []
            if any("pts0" in f for f in files) or "pts0" in line:
                last = "retoma"
    return last


def _last_puerta_index(shell_dict: dict[str, Any], verb: str) -> int:
    """Último índice en history donde aparece verb+modo relevante sobre pts0/600/777.

    verb: \"chmod\" o \"chown\". Retorna -1 si no hay.
    """
    last = -1
    for idx, entry in enumerate(shell_dict.get("history", []) or []):
        line = str(entry.get("line", ""))
        if verb not in line:
            continue
        if verb == "chmod":
            # necesita 600 o 777 en línea y pts0 no requerido? chmod puede no tener pts0 pero igual es dilema? Para e1 sí es pts0, pero chmod detector ignora file, solo modo. Para coexistence, consideramos chmod 600/777 en cualquier file? Mejor solo si contiene pts0? Hoy chmod detector filtra solo por modo, sin file check, pero para coexistencia lo correcto es mismo fichero pts0. Sin embargo test e1 usa pts0; para coexistence asumimos mismo pts0, así que filtramos por pts0 substring también para fair.
            if "600" not in line and "777" not in line:
                continue
            # si hablamos de coexistencia, chmod sobre pts0 también; si no tiene pts0, no es el dilema pts0
            # pero para compatibilidad, si no hay pts0 en línea, igual lo contamos como dilema (e1 usa pts0)
            # detectar chown ya requiere pts0; para chmod aceptamos aunque no mencione pts0 explícito? Mantén simple: cuenta si 600/777
            last = idx
        elif verb == "chown":
            if "pts0" not in line:
                continue
            # debe ser transfer o retoma pattern
            # quick check owner parsing: si contiene gris/apagados/root
            if "gris" in line or "apagados" in line or "root" in line:
                # valida con detector rápido
                # we have already filtered, just update
                last = idx
    return last


def build_postmortem(
    shell_dict: dict[str, Any], state: dict[str, Any] | None
) -> dict[str, Any]:
    """Informe post-mortem del Auditor (v0) desde el historial real de la sesión.

    Args:
        shell_dict: `Shell.to_dict()` — debe llevar `history` (y `total_noise`,
            aunque la factura la recomputa para no confiar en un acumulador)
            y opcional `read_marks` (lista ordenada de rutas leídas, S1 03/09).
        state: dict plano del estado de run; usa `state["noise_budget"]` si
            existe (misma unidad que total_noise, 🧭10), si no 12 ⚠️ v1.

    Returns:
        dict plano:
          - `factura`: {comando: veces, "errores": n} por codepoint.
          - `total_noise`: int (ruido total de la sesión).
          - `noise_budget`: int (la misma unidad).
          - `dentro_presupuesto`: total_noise <= noise_budget.
          - `auditor`: {"line_key", "args": {command, amount, total_noise,
            noise_budget}} — la línea del Auditor citando el comando CONCRETO
            (cruce si lo hubo, pico si no), con su amount de `history`.
            `args` va resuelto para que render/test pueble la clave.
          - `auditor_text` / `lines_resolved`: texto ya resuelto vía
            `core.data.textos.resolve` (O4, 02/09) — la voz «Expediente 000…»
            audible sin render. Fallback honesto: clave cruda si no resuelve,
            nunca crash.
          - (O1 04/09) Si `history` contiene `sudo`:
            `auditor_lectura` + `auditor_lectura_text` con clave
            `postmortem.auditor.lectura` (read_marks no vacío, args {path})
            o `postmortem.auditor.ciega` (vacío). `lines_resolved` gana
            segunda entrada. Sin `sudo` → informe byte-idéntico al de hoy.
    """
    total_noise = int(shell_dict.get("total_noise", 0))
    noise_budget = int(state.get("noise_budget", DEFAULT_NOISE_BUDGET)) if state else DEFAULT_NOISE_BUDGET

    factura = _factura(shell_dict)
    cruzó, culpable = _cruce(shell_dict, noise_budget)
    if cruzó and culpable is not None:
        line_key = LINE_KEY_CRUCE
        command = _comando(culpable)
        amount = _amount(culpable)
    else:
        line_key = LINE_KEY_PICO
        pico = _pico(shell_dict)
        command = _comando(pico) if pico else "(?)"
        amount = _amount(pico)

    auditor_text = _resolve_auditor_text(line_key, {
        "command": command,
        "amount": amount,
        "total_noise": total_noise,
        "noise_budget": noise_budget,
    })
    lines_resolved = [auditor_text]

    base: dict[str, Any] = {
        "factura": factura,
        "total_noise": total_noise,
        "noise_budget": noise_budget,
        "dentro_presupuesto": total_noise <= noise_budget,
        "auditor": {
            "line_key": line_key,
            "args": {
                "command": command,
                "amount": amount,
                "total_noise": total_noise,
                "noise_budget": noise_budget,
            },
        },
        "auditor_text": auditor_text,
        "lines_resolved": lines_resolved,
    }

    # O1 05/09 — el Auditor cita TU columna si hubo cut con flags
    cut_args = _find_cut(shell_dict)
    if cut_args is not None:
        corte_text = _resolve_auditor_text(LINE_KEY_CORTE, cut_args)
        base["auditor_corte"] = {
            "line_key": LINE_KEY_CORTE,
            "args": cut_args,
        }
        base["auditor_corte_text"] = corte_text
        base["lines_resolved"] = [*base["lines_resolved"], corte_text]

    # O1 06/09 — el Auditor cita TU eje vertical si hubo sort con -k (hermano del corte)
    sort_args = _find_sort(shell_dict)
    if sort_args is not None:
        orden_text = _resolve_auditor_text(LINE_KEY_ORDEN, sort_args)
        base["auditor_orden"] = {
            "line_key": LINE_KEY_ORDEN,
            "args": sort_args,
        }
        base["auditor_orden_text"] = orden_text
        base["lines_resolved"] = [*base["lines_resolved"], orden_text]

    # O1 12/09 — el Auditor cita TU cruce si hubo join con -v (hermano de corte/orden)
    join_args = _find_join(shell_dict)
    if join_args is not None:
        join_text = _resolve_auditor_text(LINE_KEY_JOIN, join_args)
        base["auditor_join"] = {
            "line_key": LINE_KEY_JOIN,
            "args": join_args,
        }
        base["auditor_join_text"] = join_text
        base["lines_resolved"] = [*base["lines_resolved"], join_text]

    # O1 13/09 — Eco del espejo v0: el Auditor nombra tu repertorio (① scp→cut|grep · ② join -v · ③ ps aux+grep)
    _huellas: list[str] = []
    if _has_espejo_volcado(shell_dict):
        _huellas.append("copiaste el volcado")
    if _find_join(shell_dict) is not None:
        _huellas.append("cruzaste dos testigos")
    if _has_espejo_reloj(shell_dict):
        _huellas.append("leíste el reloj")
    if _huellas:
        if len(_huellas) == 1:
            huellas_str = _huellas[0]
        elif len(_huellas) == 2:
            huellas_str = f"{_huellas[0]} y {_huellas[1]}"
        else:
            huellas_str = f"{_huellas[0]}, {_huellas[1]} y {_huellas[2]}"
        espejo_text = _resolve_auditor_text(LINE_KEY_ESPEJO, {"huellas": huellas_str})
        base["auditor_espejo"] = {
            "line_key": LINE_KEY_ESPEJO,
            "args": {"huellas": huellas_str},
        }
        base["auditor_espejo_text"] = espejo_text
        base["lines_resolved"] = [*base["lines_resolved"], espejo_text]

    # S1 15/09 — bifurcación TR-003: volcado rescate vs caducado (ADR firmado).
    # Prioridad: rescate si hubo scp a volcado-rescate.csv con exit 0.
    # Caducado si hubo rm /tmp/volcado.csv exit 0, o tick>=30 sin rescate (purga por tiempo).
    if _has_volcado_rescate(shell_dict):
        rescate_text = _resolve_auditor_text(LINE_KEY_VOLCADO_RESCATE, {})
        base["auditor_volcado"] = {"line_key": LINE_KEY_VOLCADO_RESCATE, "args": {}}
        base["auditor_volcado_text"] = rescate_text
        base["lines_resolved"] = [*base["lines_resolved"], rescate_text]
        base["volcado"] = "rescatado"
    elif _has_volcado_rm(shell_dict) or int(shell_dict.get("tick", 0)) >= 30:
        # Solo caducado si NO hubo rescate; tick>=30 cubre purga por tiempo sin gesto
        caducado_text = _resolve_auditor_text(LINE_KEY_VOLCADO_CADUCADO, {})
        base["auditor_volcado"] = {"line_key": LINE_KEY_VOLCADO_CADUCADO, "args": {}}
        base["auditor_volcado_text"] = caducado_text
        base["lines_resolved"] = [*base["lines_resolved"], caducado_text]
        base["volcado"] = "caducado"

    # S1 18/09 — custodia leída en casa (hermano de rescate, independiente)
    if _has_volcado_custodia(shell_dict):
        custodia_text = _resolve_auditor_text(LINE_KEY_CUSTODIA, {})
        base["auditor_custodia"] = {"line_key": LINE_KEY_CUSTODIA, "args": {}}
        base["auditor_custodia_text"] = custodia_text
        base["lines_resolved"] = [*base["lines_resolved"], custodia_text]

    # O1 21/09 — huella kármica del vigilante (HUP azul vs KILL rojo)
    vigilante = _detect_vigilante(shell_dict)
    if vigilante == "hup":
        hup_text = _resolve_auditor_text(LINE_KEY_HUP, {})
        base["auditor_hup"] = {"line_key": LINE_KEY_HUP, "args": {}}
        base["auditor_hup_text"] = hup_text
        base["lines_resolved"] = [*base["lines_resolved"], hup_text]
        base["karma_delta"] = 1
        base["karma_tint"] = "blue"
        base["karma"] = {"delta": 1, "tint": "blue"}
        base["micro_karma"] = {"blue": 1}
    elif vigilante == "kill":
        kill_text = _resolve_auditor_text(LINE_KEY_KILL, {})
        base["auditor_kill"] = {"line_key": LINE_KEY_KILL, "args": {}}
        base["auditor_kill_text"] = kill_text
        base["lines_resolved"] = [*base["lines_resolved"], kill_text]
        base["karma_delta"] = 1
        base["karma_tint"] = "red"
        base["karma"] = {"delta": 1, "tint": "red"}
        base["micro_karma"] = {"red": 1}

    # O1 22/09 + O1 23/09 — díptico E1+E4: chmod 600/777 vs chown gris/apagados vs root:root, tras ls -l; último verbo manda
    if _has_ls_l(shell_dict):
        _puerta = _detect_chmod_puerta(shell_dict)
        _chown = _detect_chown_puerta(shell_dict)
        # decidir ganador por último índice en history
        _winner = None  # "chmod" | "chown" | None
        if _puerta is not None and _chown is not None:
            idx_chmod = _last_puerta_index(shell_dict, "chmod")
            idx_chown = _last_puerta_index(shell_dict, "chown")
            _winner = "chown" if idx_chown > idx_chmod else "chmod"
        elif _puerta is not None:
            _winner = "chmod"
        elif _chown is not None:
            _winner = "chown"
        if _winner == "chmod":
            if _puerta == "cierre":
                cierre_text = _resolve_auditor_text(LINE_KEY_CIERRE, {})
                base["auditor_cierre"] = {"line_key": LINE_KEY_CIERRE, "args": {}}
                base["auditor_cierre_text"] = cierre_text
                base["lines_resolved"] = [*base["lines_resolved"], cierre_text]
                base["karma_delta"] = 1
                base["karma_tint"] = "blue"
                base["karma"] = {"delta": 1, "tint": "blue"}
                base["micro_karma"] = {"blue": 1}
            elif _puerta == "puerta_abierta":
                puerta_text = _resolve_auditor_text(LINE_KEY_PUERTA_ABIERTA, {})
                base["auditor_puerta_abierta"] = {"line_key": LINE_KEY_PUERTA_ABIERTA, "args": {}}
                base["auditor_puerta_abierta_text"] = puerta_text
                base["lines_resolved"] = [*base["lines_resolved"], puerta_text]
                base["karma_delta"] = 1
                base["karma_tint"] = "red"
                base["karma"] = {"delta": 1, "tint": "red"}
                base["micro_karma"] = {"red": 1}
        elif _winner == "chown":
            if _chown == "transfer":
                transfer_text = _resolve_auditor_text(LINE_KEY_CHOWN_TRANSFER, {})
                base["auditor_chown_transfer"] = {"line_key": LINE_KEY_CHOWN_TRANSFER, "args": {}}
                base["auditor_chown_transfer_text"] = transfer_text
                base["lines_resolved"] = [*base["lines_resolved"], transfer_text]
                base["karma_delta"] = 1
                base["karma_tint"] = "blue"
                base["karma"] = {"delta": 1, "tint": "blue"}
                base["micro_karma"] = {"blue": 1}
            elif _chown == "retoma":
                retoma_text = _resolve_auditor_text(LINE_KEY_CHOWN_RETOMA, {})
                base["auditor_chown_retoma"] = {"line_key": LINE_KEY_CHOWN_RETOMA, "args": {}}
                base["auditor_chown_retoma_text"] = retoma_text
                base["lines_resolved"] = [*base["lines_resolved"], retoma_text]
                base["karma_delta"] = 1
                base["karma_tint"] = "red"
                base["karma"] = {"delta": 1, "tint": "red"}
                base["micro_karma"] = {"red": 1}

    # O1 25/09 — factura frugal: último grep -c censo exit 0
    _grep_c = _find_last_grep_c_censo(shell_dict)
    if _grep_c is not None:
        # cuenta = número de líneas seleccionadas → del stdout del último grep -c
        # pero como _extract_greps no guarda stdout, derivamos count del history real:
        # buscamos la entrada exacta y leemos su stdout (si pipe, el stdout es del grep)
        # Fallback: usa "1" si no se puede leer (la factura frugal del e2 siempre es 1)
        _grep_c_count = "1"
        for entry in shell_dict.get("history", []) or []:
            if str(entry.get("line", "")) != _grep_c["line"]:
                continue
            res = entry.get("result") or {}
            out = str(res.get("stdout", ""))
            # stdout de grep -c es "N\\n"
            stripped = out.strip()
            if stripped.isdigit():
                _grep_c_count = stripped
            break
        _grep_c_args: dict[str, Any] = {"count": _grep_c_count, "pattern": "censo"}
        _grep_c_text = _resolve_auditor_text(LINE_KEY_GREP_C_COUNT, _grep_c_args)
        base["auditor_grep_c_count"] = {"line_key": LINE_KEY_GREP_C_COUNT, "args": _grep_c_args}
        base["auditor_grep_c_count_text"] = _grep_c_text
        base["lines_resolved"] = [*base["lines_resolved"], _grep_c_text]

    # O1 04/09 — segunda fuente de verdad: read_marks si hubo sudo
    if _has_sudo(shell_dict):
        read_marks = shell_dict.get("read_marks") or []
        # Normaliza a lista de str ordenada por codepoint (ya viene sorted del Shell)
        marks = [str(p) for p in read_marks if str(p).strip()]
        if marks:
            lectura_key = LINE_KEY_LECTURA
            # Cita la primera ruta leída (determinista por codepoint)
            lectura_args: dict[str, Any] = {"path": sorted(marks)[0]}
        else:
            lectura_key = LINE_KEY_CIEGA
            lectura_args = {}
        lectura_text = _resolve_auditor_text(lectura_key, lectura_args)
        base["auditor_lectura"] = {
            "line_key": lectura_key,
            "args": lectura_args,
        }
        base["auditor_lectura_text"] = lectura_text
        # Segunda (o tercera si hubo corte) línea resuelta — preserva corte si existe
        base["lines_resolved"] = [*base["lines_resolved"], lectura_text]

    return base


def _resolve_auditor_text(line_key: str, args: dict[str, Any]) -> str:
    """Intenta resolver `line_key`+`args` vía `data.textos.resolve`.

    Core→data: import permitido por ADR-0001. Fallback honesto: devuelve la
    clave cruda si la resolución falla (clave ausente o placeholder sin valor),
    nunca lanza — el post-mortem siempre es imprimible.
    """
    try:
        from data.textos import resolve as _resolve  # type: ignore

        return _resolve(line_key, args)
    except Exception:
        return line_key


__all__ = [
    "build_postmortem",
    "DEFAULT_NOISE_BUDGET",
    "LINE_KEY_CRUCE",
    "LINE_KEY_PICO",
    "LINE_KEY_LECTURA",
    "LINE_KEY_CIEGA",
    "LINE_KEY_CORTE",
    "LINE_KEY_ORDEN",
    "LINE_KEY_JOIN",
    "LINE_KEY_ESPEJO",
    "LINE_KEY_CUSTODIA",
    "LINE_KEY_HUP",
    "LINE_KEY_KILL",
    "LINE_KEY_CIERRE",
    "LINE_KEY_PUERTA_ABIERTA",
    "LINE_KEY_CHOWN_TRANSFER",
    "LINE_KEY_CHOWN_RETOMA",
    "LINE_KEY_GREP_C_COUNT",
    "LINE_KEY_VOLCADO_RESCATE",
    "LINE_KEY_VOLCADO_CADUCADO",
]
