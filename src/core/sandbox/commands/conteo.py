"""conteo.py — `head`, `tail`, `sort`, `uniq` (familia texto, cap. 6).

Llegan con S2 (01/09): la familia CONTEO abre la barrera técnica hacia el
cap. 6 «Faro» (salas-dato sobre la Lista de Lumen — declarar antes de mirar
entero). Semántica REAL de GNU (DESIGN §2.6.8) contrastada con coreutils real
(Ubuntu, 01/09); todos leen de `stdin` (el buffer de la tubería) cuando no
reciben fichero. Son la familia «lectura frugal»: menos ruido por la misma
información que un `cat` entero. Prohibido `random`: determinista sobre el
contenido dado.

Formato verificado contra GNU real:
- `head [-n N]`: primeras N líneas (default 10). `head -n 0` → vacío.
- `tail [-n N]`: últimas N líneas (default 10). `tail -n 0` → vacío.
- `sort [-u] [-n] [-t SEP] [-k KEYDEF]`: ordena líneas por BYTE (LC_ALL=C;
  determinismo §5); `-u` elimina duplicados; `-n` numérico; `-t SEP`
  delimitador single-char (`|` incluido); `-k F[.C][,F[.C]]` clave por campo
  (rango `N-M` alias `N,M`, sufijo `n` numérico; sin esa columna → fallback
  vacío sin crashear). Sin `-k` → sin cambio (compatibilidad cap.2/Faro).
- `uniq [-c]`: colapsa SOLO adyacentes (sin ordenar — GNU no ordena);
  `-c` antepone la cuenta ALINEADA A LA DERECHA en ancho 7 (`      2 a`),
  como GNU real.

Errores GNU (inglés §2.6.8) con exit codes reales: head/tail/uniq fichero
inexistente → exit 1 `cannot open ... for reading: No such file or directory`;
sort inexistente → exit 2 `cannot read: ...: No such file or directory`.
Opción desconocida → mensaje GNU de la utilidad.
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import FileSystem, FsError
from core.sandbox.noise import NOISE_PROFILE

HEAD_NAME = "head"
TAIL_NAME = "tail"
SORT_NAME = "sort"
UNIQ_NAME = "uniq"

_DEFAULT_N = 10


def _lines(text: str) -> list[str]:
    """Líneas de un texto (coherente con grep/wc del módulo texto)."""
    return text.splitlines()


def _read_input(
    fs: FileSystem, cwd: str, files: tuple[str, ...], stdin: str = ""
) -> tuple[list[tuple[str, str | None]], list[tuple[str, str]]]:
    """(inputs[(texto, nombre|None)], errs[(nombre, kind)]) leyendo fichero o stdin.

    Sin ficheros lee de `stdin` (la tubería), con nombre None. Con ficheros,
    los lee en orden y conserva los errores de FS (nombre + kind), que el
    caller decide cómo emitir (head/tail/uniq exit 1, sort exit 2).
    """
    inputs: list[tuple[str, str | None]] = []
    errs: list[tuple[str, str]] = []
    if not files:
        inputs.append((stdin, None))
        return inputs, errs
    for f in files:
        try:
            inputs.append((fs.read_file(f, cwd), f))
        except FsError as e:
            errs.append((f, e.kind))
    return inputs, errs


def _head_tail_err_text(errs: list[tuple[str, str]], which: str) -> str:
    """Mensajes GNU de head/tail/uniq para errores de FS (exit 1)."""
    lines: list[str] = []
    for f, kind in errs:
        if kind == "not_found":
            lines.append(
                f"{which}: cannot open '{f}' for reading: No such file or directory"
            )
        elif kind == "is_a_directory":
            lines.append(f"{which}: error reading '{f}': Is a directory")
        else:
            lines.append(f"{which}: error reading '{f}': {kind}")
    return "\n".join(lines)


def _head_tail(
    which: str, fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str
) -> CommandResult:
    """`head`/`tail [-n N] [FICHERO...]` — N primeras/últimas líneas.

    GNU: `-n N` entero no negativo; default 10; `-n 0` → vacío. Fichero
    inexistente → `cannot open 'F' for reading: No such file or directory`,
    exit 1. `-n` sin argumento o número inválido → mensaje GNU (exit 1).
    """
    noise = noise_event(which, argv, tick)
    n = _DEFAULT_N
    files: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-n":
            if i + 1 >= len(argv):
                return CommandResult(
                    stderr=f"{which}: option requires an argument -- 'n'",
                    exit_code=1, noise=noise,
                )
            try:
                n = int(argv[i + 1])
            except ValueError:
                return CommandResult(
                    stderr=f"{which}: invalid number of lines: '{argv[i+1]}'",
                    exit_code=1, noise=noise,
                )
            i += 2
        elif a.startswith("-n") and len(a) > 2:  # -n5
            try:
                n = int(a[2:])
            except ValueError:
                return CommandResult(
                    stderr=f"{which}: invalid number of lines: '{a[2:]}'",
                    exit_code=1, noise=noise,
                )
            i += 1
        elif a.startswith("-") and a != "-":
            return CommandResult(
                stderr=f"{which}: invalid option -- '{a.lstrip('-')}'",
                exit_code=1, noise=noise,
            )
        else:
            files.append(a)
            i += 1

    inputs, errs = _read_input(fs, cwd, tuple(files), stdin)
    out_lines: list[str] = []
    for text, _name in inputs:
        ln = _lines(text)
        if which == "head":
            picked = ln[:n]
        else:
            picked = ln[-n:] if n else []
        out_lines.extend(picked)

    return CommandResult(
        stdout="".join(f"{l}\n" for l in out_lines),
        stderr=_head_tail_err_text(errs, which),
        exit_code=1 if errs else 0,
        noise=noise,
    )


def _run_head(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str = "") -> CommandResult:
    return _head_tail(HEAD_NAME, fs, cwd, argv, tick, stdin)


def _run_tail(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str = "") -> CommandResult:
    return _head_tail(TAIL_NAME, fs, cwd, argv, tick, stdin)


def _sort_err_text(errs: list[tuple[str, str]]) -> str:
    """Mensajes GNU de sort para errores de FS (exit 2)."""
    lines: list[str] = []
    for f, kind in errs:
        if kind == "not_found":
            lines.append(f"sort: cannot read: {f}: No such file or directory")
        elif kind == "is_a_directory":
            lines.append(f"sort: cannot read: {f}: Is a directory")
        else:
            lines.append(f"sort: cannot read: {f}: {kind}")
    return "\n".join(lines)


_SORT_HELP = "Try 'sort --help' for more information."

def _parse_sort_key_spec(spec: str) -> tuple[dict | None, str | None]:
    """Parsea KEYDEF `F[.C][OPTS][,F[.C][OPTS]]` (+ alias `N-M` con guion).

    Soporta rangos con `,` (GNU) y con `-` (alias didáctico del plan).
    Extrae F/C y flag `n` (numérico). Retorna (key_dict, error_msg).
    key_dict = {start_field, start_char, end_field, end_char, numeric}
    """
    import re

    if spec == "":
        return None, "invalid field specification ''"
    # Alias guion: `N-M` → `N,M` si no hay coma y patrón simple
    if "," not in spec and "-" in spec:
        # solo si es N-M simple sin punto/complejidad extra (evita `2.2-3`)
        if re.match(r"^\d+[bdfghiMhnRrV]*-\d+[bdfghiMhnRrV]*$", spec):
            spec = spec.replace("-", ",", 1)
    parts = spec.split(",", 1)
    if len(parts) > 2:
        return None, f"invalid field specification '{spec}'"
    # regex por parte: F[.C][OPTS]
    part_re = re.compile(r"^(\d+)(?:\.(\d+))?([bdfghiMhnRrV]*)$")
    parsed: list[tuple[int, int | None, str]] = []
    for p in parts:
        m = part_re.match(p)
        if not m:
            return None, f"invalid field specification '{spec}'"
        f_num = int(m.group(1))
        c_num = int(m.group(2)) if m.group(2) is not None else None
        opts = m.group(3) or ""
        if f_num == 0:
            return None, f"field number is zero: invalid field specification '{spec}'"
        if c_num is not None and c_num == 0:
            return None, f"character position is zero: invalid field specification '{spec}'"
        parsed.append((f_num, c_num, opts))
    if len(parsed) == 1:
        f, c, opts = parsed[0]
        return {"start_field": f, "start_char": c, "end_field": None, "end_char": None, "numeric": ("n" in opts)}, None
    else:
        f1, c1, opts1 = parsed[0]
        f2, c2, opts2 = parsed[1]
        numeric = ("n" in opts1) or ("n" in opts2)
        return {"start_field": f1, "start_char": c1, "end_field": f2, "end_char": c2, "numeric": numeric}, None


def _extract_sort_key(line: str, delim: str | None, key: dict) -> str:
    """Extrae la clave de ordenación de `line` según `delim` y `key`."""
    sf = key["start_field"]
    sc = key["start_char"]
    ef = key["end_field"]
    ec = key["end_char"]
    if delim is not None:
        parts = line.split(delim)
        # slice F..E inclusive (1-indexed)
        if sf > len(parts):
            raw = ""
        else:
            if ef is None:
                raw = delim.join(parts[sf - 1 :])
            else:
                # ef es inclusive; si ef > len(parts) clamp
                end_idx = min(ef, len(parts))
                if sf > end_idx:
                    raw = ""
                else:
                    raw = delim.join(parts[sf - 1 : end_idx])
        # char offset dentro del campo
        if sc is not None:
            # sc es 1-indexed dentro de raw (primer campo del slice)
            if sc > len(raw):
                raw = ""
            else:
                raw = raw[sc - 1 :]
                if ec is not None:
                    # recorta hasta ec inclusive (raro, pero soportado)
                    raw = raw[: ec - sc + 1] if ec >= sc else ""
        elif ec is not None:
            # solo end char sin start char: recorta al prefijo ec
            raw = raw[:ec]
        return raw
    else:
        # Default blank: campos separados por whitespace (GNU: non-blank to blank)
        stripped = line.lstrip(" \t")
        if not stripped:
            return ""
        import re

        tokens = re.split(r"[ \t]+", stripped)
        # tokens ya sin vacíos; field N = tokens[N-1]
        if sf > len(tokens):
            raw = ""
        else:
            if ef is None:
                raw = " ".join(tokens[sf - 1 :])
            else:
                end_idx = min(ef, len(tokens))
                if sf > end_idx:
                    raw = ""
                else:
                    raw = " ".join(tokens[sf - 1 : end_idx])
        if sc is not None:
            if sc > len(raw):
                raw = ""
            else:
                raw = raw[sc - 1 :]
        return raw


def _parse_numeric_key(s: str) -> float:
    """Parsea clave numérica al estilo GNU `sort -n` (strip + float prefix)."""
    import re

    t = s.strip()
    if t == "":
        return 0.0
    m = re.match(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", t)
    if not m:
        return 0.0
    try:
        return float(m.group(0))
    except ValueError:
        return 0.0


def _run_sort(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str = "") -> CommandResult:
    """`sort` con soporte `-t`/`-k`/`-n`/`-u`/`-r` (GNU honesto).

    Sin `-k` ordena por línea entera (byte/codepoint). Con `-k`, extrae clave(s)
    por delimitador (o whitespace si no hay `-t`). `-n` fuerza orden numérico
    (global o por-clave con sufijo `n`). `multi-char tab` y `-k0` emiten errores
    GNU con exit 2.
    """
    noise = noise_event(SORT_NAME, argv, tick)
    unique = False
    reverse = False
    numeric_global = False
    delim: str | None = None
    keys: list[dict] = []
    files: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        # Long opts
        if a in ("-n", "--numeric-sort"):
            numeric_global = True
            i += 1
            continue
        if a in ("-u", "--unique"):
            unique = True
            i += 1
            continue
        if a in ("-r", "--reverse"):
            reverse = True
            i += 1
            continue
        if a == "-t":
            if i + 1 >= len(argv):
                return CommandResult(stderr=f"sort: option requires an argument -- 't'\n{_SORT_HELP}", exit_code=2, noise=noise)
            delim = argv[i + 1]
            if len(delim) != 1:
                return CommandResult(stderr=f"sort: multi-character tab '{delim}'", exit_code=2, noise=noise)
            i += 2
            continue
        if a.startswith("-t") and len(a) > 2:
            delim = a[2:]
            if len(delim) != 1:
                return CommandResult(stderr=f"sort: multi-character tab '{delim}'", exit_code=2, noise=noise)
            i += 1
            continue
        if a.startswith("--field-separator="):
            delim = a[len("--field-separator="):]
            if len(delim) != 1:
                return CommandResult(stderr=f"sort: multi-character tab '{delim}'", exit_code=2, noise=noise)
            i += 1
            continue
        if a == "--field-separator":
            if i + 1 >= len(argv):
                return CommandResult(stderr=f"sort: option requires an argument -- 't'\n{_SORT_HELP}", exit_code=2, noise=noise)
            delim = argv[i + 1]
            if len(delim) != 1:
                return CommandResult(stderr=f"sort: multi-character tab '{delim}'", exit_code=2, noise=noise)
            i += 2
            continue
        if a == "-k":
            if i + 1 >= len(argv):
                return CommandResult(stderr=f"sort: option requires an argument -- 'k'\n{_SORT_HELP}", exit_code=2, noise=noise)
            key_spec = argv[i + 1]
            key, err = _parse_sort_key_spec(key_spec)
            if err is not None:
                return CommandResult(stderr=f"sort: {err}", exit_code=2, noise=noise)
            keys.append(key)  # type: ignore[arg-type]
            i += 2
            continue
        if a.startswith("-k") and len(a) > 2:
            key_spec = a[2:]
            key, err = _parse_sort_key_spec(key_spec)
            if err is not None:
                return CommandResult(stderr=f"sort: {err}", exit_code=2, noise=noise)
            keys.append(key)  # type: ignore[arg-type]
            i += 1
            continue
        if a.startswith("--key="):
            key_spec = a[len("--key="):]
            key, err = _parse_sort_key_spec(key_spec)
            if err is not None:
                return CommandResult(stderr=f"sort: {err}", exit_code=2, noise=noise)
            keys.append(key)  # type: ignore[arg-type]
            i += 1
            continue
        if a == "--key":
            if i + 1 >= len(argv):
                return CommandResult(stderr=f"sort: option requires an argument -- 'k'\n{_SORT_HELP}", exit_code=2, noise=noise)
            key_spec = argv[i + 1]
            key, err = _parse_sort_key_spec(key_spec)
            if err is not None:
                return CommandResult(stderr=f"sort: {err}", exit_code=2, noise=noise)
            keys.append(key)  # type: ignore[arg-type]
            i += 2
            continue
        # Combined short opts like -nu, -un, -rn, -nur
        if a.startswith("-") and a != "-" and not a.startswith("--"):
            # Si es combinación solo de n,u,r (y no contiene t/k que requieren arg)
            body = a[1:]
            if body and all(c in "nur" for c in body):
                for c in body:
                    if c == "n":
                        numeric_global = True
                    elif c == "u":
                        unique = True
                    elif c == "r":
                        reverse = True
                i += 1
                continue
            # Si contiene otra letra, es opción inválida
            if body and body[0] not in "ntkur":
                return CommandResult(stderr=f"sort: invalid option -- '{body[0]}'\n{_SORT_HELP}", exit_code=2, noise=noise)
            # t/k dentro de combinado sin arg separado → error missing arg
            if "t" in body or "k" in body:
                # GNU: requiere arg separado; aquí lo tratamos como missing
                opt = "t" if "t" in body else "k"
                return CommandResult(stderr=f"sort: option requires an argument -- '{opt}'\n{_SORT_HELP}", exit_code=2, noise=noise)
            return CommandResult(stderr=f"sort: invalid option -- '{a.lstrip('-')}'\n{_SORT_HELP}", exit_code=2, noise=noise)
        if a.startswith("-"):
            return CommandResult(stderr=f"sort: invalid option -- '{a.lstrip('-')}'\n{_SORT_HELP}", exit_code=2, noise=noise)
        files.append(a)
        i += 1

    inputs, errs = _read_input(fs, cwd, tuple(files), stdin)
    lines: list[str] = []
    for text, _name in inputs:
        lines.extend(_lines(text))

    # Ordenación
    if not keys:
        if numeric_global:
            # Global -n sin -k: clave numérica de la línea entera
            def _num_key(l: str) -> tuple[float, str]:
                return (_parse_numeric_key(l), l)
            lines_sorted = sorted(lines, key=_num_key, reverse=reverse)
        else:
            lines_sorted = sorted(lines, reverse=reverse)
    else:
        # Con claves: tuple por cada key
        def _compound_key(line: str):
            parts: list = []
            for k in keys:
                raw = _extract_sort_key(line, delim, k)
                is_num = numeric_global or k.get("numeric", False)
                if is_num:
                    parts.append(_parse_numeric_key(raw))
                else:
                    parts.append(raw)
            # last-resort: línea entera para determinismo (como GNU)
            parts.append(line)
            return tuple(parts)

        lines_sorted = sorted(lines, key=_compound_key, reverse=reverse)

    if unique:
        dedup: list[str] = []
        for l in lines_sorted:
            if not dedup or dedup[-1] != l:
                dedup.append(l)
        lines_sorted = dedup
    return CommandResult(
        stdout="".join(f"{l}\n" for l in lines_sorted),
        stderr=_sort_err_text(errs),
        exit_code=2 if errs else 0,
        noise=noise,
    )


def _uniq_err_text(errs: list[tuple[str, str]]) -> str:
    """Mensajes GNU de `uniq` para errores de FS (formato propio, exit 1).

    GNU `uniq` ≠ head/tail: reporta `uniq: F: No such file or directory`
    (sin «cannot open ... for reading»), verificado contra coreutils real.
    """
    lines: list[str] = []
    for f, kind in errs:
        if kind == "not_found":
            lines.append(f"uniq: {f}: No such file or directory")
        elif kind == "is_a_directory":
            lines.append(f"uniq: {f}: Is a directory")
        else:
            lines.append(f"uniq: {f}: {kind}")
    return "\n".join(lines)


def _run_uniq(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str = "") -> CommandResult:
    """`uniq [-c] [FICHERO...]` — colapsa líneas ADYACENTES duplicadas.

    GNU `uniq` NO ordena: solo fusiona duplicados contiguos. `-c` antepone la
    cuenta de cada línea fusionada, derecha-alineada en ancho 7 (verificado
    contra coreutils real: `      2 a`). Fichero inexistente → mensaje GNU,
    exit 1. Sin ficheros lee de stdin.
    """
    noise = noise_event(UNIQ_NAME, argv, tick)
    count = False
    files: list[str] = []
    for a in argv:
        if a == "-c":
            count = True
        elif a.startswith("-"):
            return CommandResult(
                stderr=f"uniq: invalid option -- '{a.lstrip('-')}'",
                exit_code=1, noise=noise,
            )
        else:
            files.append(a)

    inputs, errs = _read_input(fs, cwd, tuple(files), stdin)
    out: list[tuple[str, int]] = []  # (linea, cuenta) en orden de aparición
    for text, _name in inputs:
        for l in _lines(text):
            if out and out[-1][0] == l:
                out[-1] = (l, out[-1][1] + 1)
            else:
                out.append((l, 1))
    rendered = [f"{c:>7} {l}" if count else l for l, c in out]
    return CommandResult(
        stdout="".join(f"{l}\n" for l in rendered),
        stderr=_uniq_err_text(errs),
        exit_code=1 if errs else 0,
        noise=noise,
    )


HEAD_SPEC = CommandSpec(
    name=HEAD_NAME, concepts=frozenset({"head"}), noise=NOISE_PROFILE[HEAD_NAME], run=_run_head,
)
TAIL_SPEC = CommandSpec(
    name=TAIL_NAME, concepts=frozenset({"tail"}), noise=NOISE_PROFILE[TAIL_NAME], run=_run_tail,
)
SORT_SPEC = CommandSpec(
    name=SORT_NAME, concepts=frozenset({"sort"}), noise=NOISE_PROFILE[SORT_NAME], run=_run_sort,
)
UNIQ_SPEC = CommandSpec(
    name=UNIQ_NAME, concepts=frozenset({"uniq"}), noise=NOISE_PROFILE[UNIQ_NAME], run=_run_uniq,
)

SPECS: tuple[CommandSpec, ...] = (HEAD_SPEC, TAIL_SPEC, SORT_SPEC, UNIQ_SPEC)