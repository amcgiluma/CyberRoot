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
- `sort [-u]`: ordena líneas por BYTE (LC_ALL=C; determinismo §5); `-u`
  elimina duplicados (salida única).
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


def _run_sort(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str = "") -> CommandResult:
    """`sort [-u] [FICHERO...]` — líneas en orden de byte.

    GNU `sort` ordena por bytes en entorno C; nosotros usamos el orden de
    codepoint (determinismo §5, coherente con el resto del sandbox). `-u`
    elimina duplicados. Fichero inexistente → `sort: cannot read: F: No such
    file or directory`, exit 2 (GNU). Sin ficheros lee de stdin.
    """
    noise = noise_event(SORT_NAME, argv, tick)
    unique = False
    files: list[str] = []
    for a in argv:
        if a == "-u":
            unique = True
        elif a.startswith("-"):
            return CommandResult(
                stderr=f"sort: invalid option -- '{a.lstrip('-')}'",
                exit_code=2, noise=noise,
            )
        else:
            files.append(a)

    inputs, errs = _read_input(fs, cwd, tuple(files), stdin)
    lines: list[str] = []
    for text, _name in inputs:
        lines.extend(_lines(text))
    lines.sort()  # byte/codepoint deterministic (§5)
    if unique:
        dedup: list[str] = []
        for l in lines:
            if not dedup or dedup[-1] != l:
                dedup.append(l)
        lines = dedup
    return CommandResult(
        stdout="".join(f"{l}\n" for l in lines),
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