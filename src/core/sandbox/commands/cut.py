"""cut.py — `cut` (familia texto, cap. 6).

GNU-honesto v0 (S1 04/09): la Lista es una tabla cortable (CENSO-LISTA.md).
Semántica contrastada contra coreutils real (Ubuntu, 04/09):

- `cut -d DELIM -f LIST [FILE...]` — filtra columnas por delimitador.
  LIST = coma-separado de rangos N, N-, -M, N-M (1-indexed). Seleccionados se
  ordenan, deduplican y emiten una vez en orden creciente (GNU §).
  Sin -f → "you must specify a list..." exit 1.
  Delim multi-char → "the delimiter must be a single character" exit 1.
  Campos 0 o decrecientes → mensajes GNU correspondientes.
  Línea sin delimitador se imprime entera (a menos que -s).
  Default delimitador TAB si no se da -d.
  Lee de stdin (tubería) cuando no hay FILE, o de FILEs con errores FS
  (exit 1 si algún file falla, ruido igual que head/uniq).

No implementado v0: -b/-c, --complement, --output-delimiter, --zero-terminated,
-n. -s (--only-delimited) sí se soporta (silencia líneas sin delimitador).
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import FileSystem, FsError

CUT_NAME = "cut"

_HELP_SUFFIX = "Try 'cut --help' for more information."

def _parse_fields_to_ranges(spec: str) -> tuple[list[tuple[int, int | None]], str | None]:
    """Parsea LIST a lista de rangos (lo, hi) donde hi=None significa N-.
    Devuelve (ranges, error_msg).
    """
    if spec == "":
        return [], "invalid field value ''"
    parts = spec.split(",")
    ranges: list[tuple[int, int | None]] = []
    for raw in parts:
        if raw == "":
            return [], "fields are numbered from 1"
        if raw.count("-") > 1:
            return [], f"invalid field value '{raw}'"
        if "-" in raw:
            left, right = raw.split("-", 1)
            if left == "" and right == "":
                return [], f"invalid field value '{raw}'"
            if left == "":
                try:
                    m = int(right)
                except ValueError:
                    return [], f"invalid field value '{raw}'"
                if m < 1:
                    return [], "fields are numbered from 1"
                ranges.append((1, m))
            elif right == "":
                try:
                    n = int(left)
                except ValueError:
                    return [], f"invalid field value '{raw}'"
                if n < 1:
                    return [], "fields are numbered from 1"
                ranges.append((n, None))
            else:
                try:
                    n = int(left)
                    m = int(right)
                except ValueError:
                    return [], f"invalid field value '{raw}'"
                if n < 1 or m < 1:
                    return [], "fields are numbered from 1"
                if n > m:
                    return [], "invalid decreasing range"
                ranges.append((n, m))
        else:
            try:
                n = int(raw)
            except ValueError:
                return [], f"invalid field value '{raw}'"
            if n < 1:
                return [], "fields are numbered from 1"
            ranges.append((n, n))
    return ranges, None


def _expand_ranges(ranges: list[tuple[int, int | None]], max_field: int) -> list[int]:
    """Expande rangos a índices ordenados únicos limitados a max_field.
    hi=None → hasta max_field.
    """
    vals: set[int] = set()
    for lo, hi in ranges:
        if hi is None:
            hi = max_field
        for v in range(lo, hi + 1):
            if v <= max_field:
                vals.add(v)
    return sorted(vals)


def _read_input(fs: FileSystem, cwd: str, files: tuple[str, ...], stdin: str):
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


def _cut_err_text(errs: list[tuple[str, str]]) -> str:
    lines: list[str] = []
    for f, kind in errs:
        if kind == "not_found":
            lines.append(f"cut: {f}: No such file or directory")
        elif kind == "is_a_directory":
            lines.append(f"cut: {f}: Is a directory")
        else:
            lines.append(f"cut: {f}: {kind}")
    return "\n".join(lines)


def _run_cut(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int, stdin: str = "") -> CommandResult:
    noise = noise_event(CUT_NAME, argv, tick)
    delim: str | None = None
    delim_given = False
    fields_spec: str | None = None
    only_delimited = False
    files: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-d":
            if i + 1 >= len(argv):
                return CommandResult(stderr="cut: option requires an argument -- 'd'\n" + _HELP_SUFFIX, exit_code=1, noise=noise)
            delim = argv[i + 1]
            delim_given = True
            i += 2
        elif a.startswith("-d") and len(a) > 2:
            delim = a[2:]
            delim_given = True
            i += 1
        elif a == "--delimiter":
            if i + 1 >= len(argv):
                return CommandResult(stderr="cut: option requires an argument -- 'delimiter'\n" + _HELP_SUFFIX, exit_code=1, noise=noise)
            delim = argv[i + 1]
            delim_given = True
            i += 2
        elif a.startswith("--delimiter="):
            delim = a[len("--delimiter="):]
            delim_given = True
            i += 1
        elif a == "-f":
            if i + 1 >= len(argv):
                return CommandResult(stderr="cut: option requires an argument -- 'f'\n" + _HELP_SUFFIX, exit_code=1, noise=noise)
            fields_spec = argv[i + 1]
            i += 2
        elif a.startswith("-f") and len(a) > 2:
            fields_spec = a[2:]
            i += 1
        elif a == "--fields":
            if i + 1 >= len(argv):
                return CommandResult(stderr="cut: option requires an argument -- 'fields'\n" + _HELP_SUFFIX, exit_code=1, noise=noise)
            fields_spec = argv[i + 1]
            i += 2
        elif a.startswith("--fields="):
            fields_spec = a[len("--fields="):]
            i += 1
        elif a in ("-s", "--only-delimited"):
            only_delimited = True
            i += 1
        elif a.startswith("-") and a != "-":
            # opción desconocida o -b/-c/--bytes etc
            # mensaje genérico GNU
            opt = a.lstrip("-")
            # para -b/-c con valor pegado, igualmente inválido en nuestro cut de campos
            return CommandResult(stderr=f"cut: invalid option -- '{opt}'\n{_HELP_SUFFIX}", exit_code=1, noise=noise)
        else:
            files.append(a)
            i += 1

    if fields_spec is None:
        return CommandResult(stderr=f"cut: you must specify a list of bytes, characters, or fields\n{_HELP_SUFFIX}", exit_code=1, noise=noise)

    if delim is None:
        delim = "\t"
    else:
        if len(delim) != 1:
            return CommandResult(stderr=f"cut: the delimiter must be a single character\n{_HELP_SUFFIX}", exit_code=1, noise=noise)

    ranges, err = _parse_fields_to_ranges(fields_spec)
    if err is not None:
        return CommandResult(stderr=f"cut: {err}\n{_HELP_SUFFIX}", exit_code=1, noise=noise)

    inputs, errs = _read_input(fs, cwd, tuple(files), stdin)

    out_lines: list[str] = []
    for text, _name in inputs:
        # splitlines conserva líneas sin \n final; join luego con \n
        # Para no perder última línea vacía trailing, usamos splitlines que
        # ignora trailing newline; luego re-emitimos con \n por línea si original tenía contenido.
        # Modelo de conteo.py: text.splitlines() y luego join con "\n"
        lines = text.splitlines()
        # Si text termina en \n, splitlines ya ignora trailing vacío, pero join con \n + \n final reparará
        has_trailing_nl = text.endswith("\n") if text else False
        for line in lines:
            if delim not in line:
                if only_delimited:
                    continue
                out_lines.append(line)
            else:
                parts = line.split(delim)
                # expandir rangos según max_field de esta línea
                idxs = _expand_ranges(ranges, len(parts))
                selected = [parts[k - 1] for k in idxs if 1 <= k <= len(parts)]
                out_lines.append(delim.join(selected))
        # Nota: si text era vacío, lines==[], no emitimos nada (coherente)
        # El trailing newline se maneja en stdout final

    stderr = _cut_err_text(errs)
    # Construir stdout: cada out_line con \n, incluso última, si hubo alguna línea
    # o si inputs tenía texto no vacío. Si inputs vacío y out vacío → ""
    if out_lines:
        stdout = "\n".join(out_lines) + "\n"
    else:
        # Si no hubo líneas (ej. fichero vacío) → ""
        # Si only_delimited suprimió todo → ""
        stdout = ""

    # Si hubo errs pero ningún input válido, stdout puede ser "" con exit 1
    return CommandResult(stdout=stdout, stderr=stderr, exit_code=1 if errs else 0, noise=noise)


CUT_SPEC = CommandSpec(
    name=CUT_NAME, concepts=frozenset({"cut"}), noise=1, run=_run_cut,
)

SPECS: tuple[CommandSpec, ...] = (CUT_SPEC,)
