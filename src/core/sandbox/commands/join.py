"""join.py — `join` (familia texto/tabla, cap. 6, quest dato4).

GNU-honesto (S3, 10/09): empareja líneas de DOS ficheros por un campo de
unión común, como `join` de coreutils. Smough lo necesita para la quest
dato4 del cap. 6 «Faro» sobre la Lista (`purgas.csv` + `registro.csv`).

Semántica contrastada contra coreutils real (Ubuntu, join 9.4, 10/09):

- `join [-t CHAR] [-1 N] [-2 M] [-v 1|-2] [-a 1|-2] FILE1 FILE2` — une líneas
  de FILE1 y FILE2 cuyo campo de unión coincide. Campo de unión default: el 1
  (1-indexed); `-1 N`/`-2 M` lo cambian por fichero.
- Delimiter: default espacio/blanco; `-t CHAR` usa CHAR (incluye `|`), forma
  separada `-t` CHAR y pegada `-t'|'` → argv token `-t|`. Multi-char → error
  GNU `multi-character tab 'X'` exit 1.
- `-v FILENUM` imprime SOLO las líneas de FILE FILENUM sin pareja (con el
  campo de unión primero, como GNU) y SUPRIME la salida combinada. Sin `-v`,
  salida normal: cada pareja en una línea `unión|resto FILE1|resto FILE2`
  (o espacio si delimiter blanco).
- `-a FILENUM` imprime además las líneas sin pareja de FILE FILENUM sin
  suprimir la salida combinada (combinable con `-v`).
- Errores GNU (exit 1, ASCII-quote para bytes reproducibles):
  - sin operandos       → `join: missing operand` + `Try 'join --help'...`
  - un operando         → `join: missing operand after 'FILE'` + help
  - >2 operandos        → `join: extra operand 'F'` + help
  - campo inválido      → `join: invalid field number: 'N'` (solo 1..; -v/-a 1|2)
  - fichero inexistente → `join: F: No such file or directory`
  - opción desconocida  → `join: invalid option -- 'q'` + help
  - `-t` multi-char     → `join: multi-character tab 'X'`
- `--help` / `--version` de GNU (stdout, exit 0).

Determinismo / honestidad sobre la no-ordenación: GNU `join` exigiría input
SORTED por campo de unión y avisa `is not sorted`. Aquí unimos con índice
(map) por campo de unión conservando el ORDEN de aparición de FILE1 en la
salida (y el de FILE2 para sus no-parejas): es la MISMA salida GNU que daría
un input ordenado, y es determinista para los ficheros del briefing (que NO
vienen ordenados). No emitimos warnings de ordenación — el contrato de
CyberRoot es reproducibilidad byte a byte (ARCHITECTURE §1.5).

No implementado v0: `-o FORMAT`, `-e`, `-i`, `-j FIELD`, `--header`,
`--check-order`, `-z`. Ruido 2 (cruce de dos ficheros; más caro que un `wc`,
familia tabla).
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import FileSystem, FsError
from core.sandbox.noise import NOISE_PROFILE

JOIN_NAME = "join"

_HELP_SUFFIX = "Try 'join --help' for more information."

_JOIN_HELP = """Usage: join [OPTION]... FILE1 FILE2
For each pair of input lines with identical join fields, write a line to
standard output.  The default join field is the first, delimited by blanks.

  -a FILENUM        also print unpairable lines from file FILENUM, where
                      FILENUM is 1 or 2, corresponding to FILE1 and FILE2
  -t CHAR           use CHAR as input and output field separator
  -v FILENUM        like -a FILENUM, but suppress joined output lines
  -1 FIELD          join on this FIELD of file 1
  -2 FIELD          join on this FIELD of file 2
      --help        display this help and exit
      --version     output version information and exit"""

_JOIN_VERSION = "join (GNU coreutils) 9.4"


def _split_fields(line: str, delim: str | None) -> list[str]:
    """Campos de `line` según el delim (None = blanco/espacio)."""
    if delim is None:
        return line.split()
    return line.split(delim)


def _key_of(fields: list[str], field: int) -> str:
    """Campo de unión de una línea (1-indexed); ausente → vacío (GNU)."""
    if 1 <= field <= len(fields):
        return fields[field - 1]
    return ""


def _rest(fields: list[str], field: int) -> list[str]:
    """Resto de los campos de una línea excluyendo su campo de unión."""
    if 1 <= field <= len(fields):
        return fields[: field - 1] + fields[field:]
    return fields


def _join_err_text(errs: list[tuple[str, str]]) -> str:
    """Mensajes GNU de `join` para errores de FS (exit 1)."""
    lines: list[str] = []
    for f, kind in errs:
        if kind == "not_found":
            lines.append(f"join: {f}: No such file or directory")
        elif kind == "is_a_directory":
            lines.append(f"join: {f}: Is a directory")
        else:
            lines.append(f"join: {f}: {kind}")
    return "\n".join(lines)


def _run_join(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str = "") -> CommandResult:
    """`join` GNU-honesto: une FILE1 y FILE2 por campo de unión común.

    Lee de stdin (tubería) si FILE1 o FILE2 es `-` (solo uno). Emite la salida
    determinista por orden de FILE1 (y de FILE2 para sus no-parejas). Exitoso
    exit 0; errores de uso/FS → exit 1 con mensajes GNU (`Try 'join --help'`).
    """
    noise = noise_event(JOIN_NAME, argv, tick)
    delim: str | None = None
    j1 = 1
    j2 = 1
    pa1 = False
    pa2 = False
    suppress_paired = False  # cualquier `-v` suprime la salida combinada
    files: list[str] = []
    i = 0

    while i < len(argv):
        a = argv[i]
        # Long opts (deben ir solos).
        if a == "--help":
            return CommandResult(stdout=_JOIN_HELP + "\n", exit_code=0, noise=noise)
        if a == "--version":
            return CommandResult(stdout=_JOIN_VERSION + "\n", exit_code=0, noise=noise)
        if a.startswith("--"):
            opt = a[2:]
            return CommandResult(stderr=f"join: invalid option -- '{opt}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
        if a.startswith("-") and a != "-":
            body = a[1:]
            if not body:
                # "-" solo es un operando (stdin); no debe ocurrir (se cae abajo)
                files.append(a)
                i += 1
                continue
            opt = body[0]
            if body[0] == "t":
                if len(body) > 1:
                    delim = body[1:]
                    i += 1
                else:
                    if i + 1 >= len(argv):
                        return CommandResult(stderr=f"join: option requires an argument -- 't'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
                    i += 1
                    delim = argv[i]
                    i += 1
                if len(delim) != 1:
                    return CommandResult(stderr=f"join: multi-character tab '{delim}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
                continue
            if body[0] in ("1", "2"):
                if len(body) > 1:
                    val_tok = body[1:]
                    if not val_tok.isdigit() or int(val_tok) < 1:
                        return CommandResult(stderr=f"join: invalid field number: '{val_tok}'", exit_code=1, noise=noise)
                    n = int(val_tok)
                    i += 1
                else:
                    if i + 1 >= len(argv):
                        return CommandResult(stderr=f"join: option requires an argument -- '{body[0]}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
                    i += 1
                    val_tok = argv[i]
                    if not val_tok.isdigit() or int(val_tok) < 1:
                        return CommandResult(stderr=f"join: invalid field number: '{val_tok}'", exit_code=1, noise=noise)
                    n = int(val_tok)
                    i += 1
                if body[0] == "1":
                    j1 = n
                else:
                    j2 = n
                continue
            if body[0] in ("v", "a"):
                if len(body) > 1:
                    val_tok = body[1:]
                    if val_tok not in ("1", "2"):
                        return CommandResult(stderr=f"join: invalid field number: '{val_tok}'", exit_code=1, noise=noise)
                    n = int(val_tok)
                    i += 1
                else:
                    if i + 1 >= len(argv):
                        return CommandResult(stderr=f"join: option requires an argument -- '{body[0]}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
                    i += 1
                    val_tok = argv[i]
                    if val_tok not in ("1", "2"):
                        return CommandResult(stderr=f"join: invalid field number: '{val_tok}'", exit_code=1, noise=noise)
                    n = int(val_tok)
                    i += 1
                if n == 1:
                    pa1 = True
                else:
                    pa2 = True
                if body[0] == "v":
                    suppress_paired = True
                continue
            return CommandResult(stderr=f"join: invalid option -- '{body[0]}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
        files.append(a)
        i += 1

    # ---- operandos --------------------------------------------------------
    if not files:
        return CommandResult(stderr=f"join: missing operand\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
    if len(files) == 1:
        return CommandResult(stderr=f"join: missing operand after '{files[0]}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
    if len(files) > 2:
        return CommandResult(stderr=f"join: extra operand '{files[2]}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)

    file1, file2 = files[0], files[1]

    # ---- lectura ----------------------------------------------------------
    def _read(f: str, from_stdin: bool) -> str:
        if from_stdin:
            return stdin
        return fs.read_file(f, cwd)

    errs: list[tuple[str, str]] = []
    try:
        text1 = _read(file1, file1 == "-")
    except FsError as e:
        errs.append((file1, e.kind))
        text1 = ""
    try:
        text2 = _read(file2, file2 == "-")
    except FsError as e:
        errs.append((file2, e.kind))
        text2 = ""

    sep = delim if delim is not None else " "

    # ---- índice de unión de FILE2 (mapa clave → [línea_filtrada,...]) -----
    lines2: list[tuple[str, list[str]]] = []  # (key, resto_fields) por orden
    idx2: dict[str, list[list[str]]] = {}
    for raw in text2.splitlines():
        flds = _split_fields(raw, delim)
        key = _key_of(flds, j2)
        rest = _rest(flds, j2)
        lines2.append((key, rest))
        idx2.setdefault(key, []).append(rest)

    keys2: set[str] = set(idx2.keys())
    keys1_set: set[str] = set()

    out_parts: list[list[str]] = []

    # Salida normal: parejas en orden de FILE1 (producto con duplicados FILE2).
    for raw in text1.splitlines():
        flds = _split_fields(raw, delim)
        key = _key_of(flds, j1)
        rest1 = _rest(flds, j1)
        if not key:
            keys1_set.add(key)
            continue
        keys1_set.add(key)
        if key in idx2:
            if not suppress_paired:
                for rest2 in idx2[key]:
                    out_parts.append([key] + rest1 + rest2)
            # pareja encontrada → no es no-pareja de FILE1
            continue
        if pa1:
            out_parts.append([key] + rest1)

    # No-parejas de FILE2 (cuando -a2/-v2 y su clave no está en FILE1).
    if pa2:
        # claves presentes en FILE1 (sin vacío): claves relevantes
        for key, rest2 in lines2:
            if key not in keys1_set:
                out_parts.append([key] + rest2)

    stdout = "".join((sep.join(p) + "\n") for p in out_parts)
    return CommandResult(
        stdout=stdout,
        stderr=_join_err_text(errs),
        exit_code=1 if errs else 0,
        noise=noise,
    )


JOIN_SPEC = CommandSpec(
    name=JOIN_NAME,
    concepts=frozenset({"join"}),
    noise=NOISE_PROFILE[JOIN_NAME],
    run=_run_join,
)

SPECS: tuple[CommandSpec, ...] = (JOIN_SPEC,)