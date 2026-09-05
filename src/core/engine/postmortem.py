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
]
