"""texto.py — `grep` y `wc` (familia texto/pipes, cap. 2, ARCHITECTURE §2.2).

Llegan con S1 (30/08) junto a las tuberías: el cap. 2 «Facturas» los exige
(`$ grep 11:04 centralita/turnos/turno.log | wc -l`). Semántica REAL de GNU
(DESIGN §2.6.8): `grep` filtra líneas que CONTIENEN el patrón (match de
subcadena, caso exacto) y las emite con `\\n`; `wc` cuenta líneas/bytes.
Ambos leen de `stdin` (el buffer de la tubería) cuando no reciben fichero.
Prohibido `random`: todo es determinista sobre el contenido dado.

v1 simplificado y DOCUMENTADO: `wc` sin flags emite `nlines nwords nbytes`
separados por un espacio (sin la alineación de columnas de GNU — el cap. 2
solo usa `-l`/`-c`, que SÍ son exactos). El default no tiene golden.
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import FileSystem, FsError
from core.sandbox.noise import NOISE_PROFILE

GREP_NAME = "grep"
WC_NAME = "wc"


def _grep_fs_message(kind: str, arg: str) -> str:
    """Mensaje GNU de `grep` para un error de FS sobre `arg` (S1 30/08)."""
    if kind == "not_found":
        return f"grep: {arg}: No such file or directory"
    return f"grep: {arg}: {kind}"


def _run_grep(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`grep PATRON [FICHERO...]`: líneas que contienen el patrón.

    Sin ficheros lee de `stdin` (la tubería). Emite las líneas coincidentes
    TODAS, en orden, con su `\\n`. Exit codes GNU: 0 si hubo al menos una
    coincidencia, 1 si ninguna, 2 si hubo algún error de FS o de uso.
    """
    noise = noise_event(GREP_NAME, argv, tick)
    if not argv:
        return CommandResult(
            stderr="grep: missing pattern", exit_code=2, noise=noise
        )
    pattern = argv[0]
    files = tuple(argv[1:])

    matched: list[str] = []
    err_lines: list[str] = []
    had_error = False

    def _scan(text: str) -> None:
        """Añade a `matched` las líneas que contienen el patrón (GNU grep)."""
        for line in text.splitlines():
            if pattern in line:
                matched.append(line)

    if not files:
        # No hay ficheros: grep lee de stdin (el buffer de la tubería).
        if stdin:
            _scan(stdin)
        return CommandResult(
            stdout="".join(f"{ln}\n" for ln in matched),
            stderr="\n".join(err_lines),
            exit_code=2 if had_error else (1 if not matched else 0),
            noise=noise,
        )

    for f in files:
        try:
            _scan(fs.read_file(f, cwd))
        except FsError as e:
            had_error = True
            err_lines.append(_grep_fs_message(e.kind, f))

    return CommandResult(
        stdout="".join(f"{ln}\n" for ln in matched),
        stderr="\n".join(err_lines),
        exit_code=2 if had_error else (1 if not matched else 0),
        noise=noise,
    )


def _wc_lines(text: str) -> int:
    """Líneas GNU de `wc`: cuenta los `\\n` (un texto sin barra final tiene 0).
    """
    return text.count("\n")


def _wc_words(text: str) -> int:
    """Palabras GNU de `wc`: secuencias de no-espacio separadas por espacios.
    """
    if not text.strip():
        return 0
    return len(text.split())


def _wc_fs_message(kind: str, arg: str) -> str:
    """Mensaje GNU de `wc` para un error de FS sobre `arg`."""
    if kind == "not_found":
        return f"wc: {arg}: No such file or directory"
    return f"wc: {arg}: {kind}"


def _run_wc(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`wc [-l] [-c] [FICHERO...]`: líneas / caracteres del input.

    Sin operandos de fichero lee de `stdin`. `-l` → solo líneas; `-c` → solo
    bytes/caracteres; sin flags → `nlines nwords nbytes` (formato v1 simple).
    GNU real verificado (30/08): con input por stdin, `wc -l` imprime SOLO el
    número (sin nombre de fichero); con fichero en argv, imprime `N nombre`.
    """
    noise = noise_event(WC_NAME, argv, tick)
    count_lines = True
    count_bytes = True
    files: list[str] = []
    for a in argv:
        if a == "-l":
            count_bytes = False
        elif a == "-c":
            count_lines = False
        elif a.startswith("-") and a != "-":
            return CommandResult(
                stderr=f"wc: invalid option -- '{a[1:]}'", exit_code=1, noise=noise
            )
        else:
            files.append(a)

    inputs: list[tuple[str, str | None]] = []  # (texto, nombre|None)
    err_lines: list[str] = []
    had_error = False
    if files:
        for f in files:
            try:
                inputs.append((fs.read_file(f, cwd), f))
            except FsError as e:
                had_error = True
                err_lines.append(_wc_fs_message(e.kind, f))
    else:
        inputs.append((stdin, None))  # wc lee del buffer de la tubería

    out_lines: list[str] = []
    for text, name in inputs:
        lines = _wc_lines(text)
        nbytes = len(text.encode("utf-8"))
        words = _wc_words(text)
        if count_lines and not count_bytes:
            cols = str(lines)
        elif count_bytes and not count_lines:
            cols = str(nbytes)
        else:
            cols = f"{lines} {words} {nbytes}"
        out_lines.append(f"{cols}{' ' + name if name else ''}\n")

    return CommandResult(
        stdout="".join(out_lines),
        stderr="\n".join(err_lines),
        exit_code=1 if had_error else 0,
        noise=noise,
    )


GREP_SPEC = CommandSpec(
    name=GREP_NAME,
    concepts=frozenset({"grep"}),
    noise=NOISE_PROFILE[GREP_NAME],
    run=_run_grep,
)

WC_SPEC = CommandSpec(
    name=WC_NAME,
    concepts=frozenset({"wc"}),
    noise=NOISE_PROFILE[WC_NAME],
    run=_run_wc,
)

SPECS: tuple[CommandSpec, ...] = (GREP_SPEC, WC_SPEC)