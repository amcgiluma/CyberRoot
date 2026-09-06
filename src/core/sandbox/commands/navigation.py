"""navigation.py — `ls` y `cd` (familia navegación, ARCHITECTURE §2.2).

Semántica REAL de Linux (DESIGN §2.6.8, PLAN decisiones 2-3): `ls` imprime una
columna ordenada por codepoint (estilo `ls -1` a un pipe); `cd` es builtin,
normaliza la cwd y valida el destino contra el FS (los errores salen ANTES de
tocar la cwd). Salidas y mensajes en inglés GNU exactos; exit codes reales
(`ls` con error grave = 2). Prohibido `random`: todo orden es por codepoint.
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import DirNode, FileSystem, FsError
from core.sandbox.noise import NOISE_PROFILE

LS_NAME = "ls"
CD_NAME = "cd"


def _ls_kind_message(kind: str, arg: str) -> str:
    """Texto GNU de `ls` para un error `kind` sobre el operando `arg`.

    GNU real (verificado contra coreutils 9.x en Ubuntu): «cannot access».
    """
    if kind == "not_found":
        return f"ls: cannot access '{arg}': No such file or directory"
    if kind == "not_a_directory":
        return f"ls: cannot access '{arg}': Not a directory"
    # Otro kind (p.ej. de un FS con permisos): se abrevia con el código.
    return f"ls: {arg}: {kind}"


def _dir_header(arg: str) -> str:
    """Cabecera `arg:` de un directorio, sin barras finales (GNU: `ls /etc/` → `/etc:`)."""
    return arg.rstrip("/") + ":"


def _mode_to_perms(mode: str, is_dir: bool) -> str:
    """Convierte mode tipo "644"/"755" a string GNU de permisos."""
    table = {
        "0": "---", "1": "--x", "2": "-w-", "3": "-wx",
        "4": "r--", "5": "r-x", "6": "rw-", "7": "rwx",
    }
    digits = mode[-3:] if len(mode) >= 3 else mode.rjust(3, "0")
    perms = "".join(table.get(d, "---") for d in digits)
    prefix = "d" if is_dir else "-"
    return prefix + perms


def _ls_long_line(name: str, node) -> str:
    """Línea formato largo v0 para ls -l."""
    is_dir = isinstance(node, DirNode)
    perms = _mode_to_perms(node.mode, is_dir)
    size = 4096 if is_dir else len(node.content) if hasattr(node, "content") else 0
    return f"{perms} 1 {node.owner} {node.group} {size} {node.mtime} {name}\n"


def _run_ls(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`ls` estilo `ls -1`: una columna ordenada por codepoint (PLAN decisión 2).

    Formato GNU real (verificado contra coreutils en Ubuntu, 27/08):
    - UN operando: sin cabecera jamás (dir → solo hijos; fichero → el
      operando tal cual; error → solo stderr).
    - VARIOS operandos: ficheros primero (en orden de argumento), luego cada
      directorio como bloque `op:` + hijos; los grupos se separan con línea
      en blanco.
    - Un operando erróneo anota stderr («cannot access»), marca exit 2 y NO
      corta el procesado del resto.
    - Flags GNU v0 (S2, 06/09): -a muestra dotfiles, -l formato largo; combinables
      (-la/-al). Sin -a, los dotfiles (.*) se OCULTAN (GNU real, 🧭20a).
    """
    noise = noise_event(LS_NAME, argv, tick)

    # ---- parseo de flags (GNU: -a, -l, combinables, -- fin de opciones) ----
    show_all = False
    long_format = False
    paths: list[str] = []
    end_of_options = False
    for arg in argv:
        if end_of_options:
            paths.append(arg)
            continue
        if arg == "--":
            end_of_options = True
            continue
        if arg.startswith("-") and len(arg) > 1 and not arg.startswith("--"):
            is_flag = True
            for ch in arg[1:]:
                if ch not in ("a", "l"):
                    is_flag = False
                    break
            if is_flag:
                if "a" in arg:
                    show_all = True
                if "l" in arg:
                    long_format = True
                continue
            else:
                bad = arg[1]
                return CommandResult(
                    stderr=f"ls: invalid option -- '{bad}'\nTry 'ls --help' for more information.",
                    exit_code=2,
                    noise=noise,
                )
        paths.append(arg)

    effective_argv = tuple(paths)

    def _filtered_children(dir_path: str, cwd_inner: str) -> list[str]:
        names = fs.list_dir(dir_path, cwd_inner)
        if not show_all:
            names = [n for n in names if not n.startswith(".")]
        return names

    def _format_children(dir_path: str, cwd_inner: str) -> str:
        names = _filtered_children(dir_path, cwd_inner)
        if not long_format:
            return "".join(f"{n}\n" for n in names)
        lines = []
        dir_node = fs.get_dir(dir_path, cwd_inner)
        for n in names:
            child = dir_node.children[n]
            lines.append(_ls_long_line(n, child))
        return "".join(lines)

    files_out: list[str] = []
    dir_blocks: list[str] = []
    err_lines: list[str] = []
    had_error = False

    if not effective_argv:
        dir_blocks.append(_format_children(cwd, cwd))
    for arg in effective_argv:
        try:
            node = fs.resolve(arg, cwd)
        except FsError as e:
            had_error = True
            err_lines.append(_ls_kind_message(e.kind, arg))
            continue
        if isinstance(node, DirNode):
            children = _format_children(arg, cwd)
            if len(effective_argv) == 1:
                dir_blocks.append(children)
            else:
                dir_blocks.append(f"{_dir_header(arg)}\n{children}")
        else:
            if arg.endswith("/"):
                had_error = True
                err_lines.append(_ls_kind_message("not_a_directory", arg))
                continue
            if long_format:
                lines = _ls_long_line(arg.split("/")[-1], node)
                files_out.append(lines)
            else:
                files_out.append(f"{arg}\n")

    groups = []
    if files_out:
        groups.append("".join(files_out))
    groups.extend(dir_blocks)
    return CommandResult(
        stdout="\n".join(groups),
        stderr="\n".join(err_lines),
        exit_code=2 if had_error else 0,
        noise=noise,
    )


def _cd_kind_message(kind: str, arg: str) -> str:
    """Texto GNU de `cd` para un error `kind` sobre el destino `arg` (PLAN §3)."""
    if kind == "not_found":
        return f"cd: {arg}: No such file or directory"
    return f"cd: {arg}: Not a directory"


def _run_cd(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`cd` builtin: valida el destino y devuelve la nueva cwd NORMALIZADA.

    0 argumentos → home es la raíz `/`. Un argumento → valida con `get_dir`
    (errores not_found / not_a_directory) y, sólo si es válido, computa la
    nueva cwd normalizada con `change_dir` (colapsa `.`, `//`, `..` y la barra
    final). Más de un argumento → `cd: too many arguments` (bash real). La
    cwd NO cambia ante ningún error (`new_cwd=None`).
    """
    noise = noise_event(CD_NAME, argv, tick)
    n = len(argv)
    if n == 0:
        return CommandResult(new_cwd="/", noise=noise)
    if n > 1:
        return CommandResult(stderr="cd: too many arguments", exit_code=1, noise=noise)

    target = list(argv)[0]
    try:
        fs.get_dir(target, cwd)
    except FsError as e:
        return CommandResult(
            stderr=_cd_kind_message(e.kind, target), exit_code=1, noise=noise
        )
    return CommandResult(new_cwd=fs.change_dir(target, cwd), noise=noise)


LS_SPEC = CommandSpec(
    name=LS_NAME,
    concepts=frozenset({"ls"}),
    noise=NOISE_PROFILE[LS_NAME],
    run=_run_ls,
)

CD_SPEC = CommandSpec(
    name=CD_NAME,
    concepts=frozenset({"cd"}),
    noise=NOISE_PROFILE[CD_NAME],
    run=_run_cd,
)

SPECS: tuple[CommandSpec, ...] = (LS_SPEC, CD_SPEC)
