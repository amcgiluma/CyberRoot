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
    """
    noise = noise_event(LS_NAME, argv, tick)
    files_out: list[str] = []
    dir_blocks: list[str] = []
    err_lines: list[str] = []
    had_error = False

    if not argv:
        # Sin operandos GNU lista `.`: contenido de la cwd, sin cabecera.
        dir_blocks.append("".join(f"{n}\n" for n in fs.list_dir(cwd)))
    for arg in argv:
        try:
            node = fs.resolve(arg, cwd)
        except FsError as e:
            had_error = True
            err_lines.append(_ls_kind_message(e.kind, arg))
            continue
        if isinstance(node, DirNode):
            children = "".join(f"{n}\n" for n in fs.list_dir(arg, cwd))
            if len(argv) == 1:
                dir_blocks.append(children)  # un solo operando: sin cabecera
            else:
                dir_blocks.append(f"{_dir_header(arg)}\n{children}")
        else:
            # GNU imprime el OPERANDO tal cual; con barra final sobre un
            # fichero es error «Not a directory».
            if arg.endswith("/"):
                had_error = True
                err_lines.append(_ls_kind_message("not_a_directory", arg))
                continue
            files_out.append(f"{arg}\n")

    groups = []
    if files_out:
        groups.append("".join(files_out))
    groups.extend(dir_blocks)
    # Los bloques YA terminan en '\n': el separador añade solo el blanco GNU.
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
        # 0 args → home = raíz (decisión v0: cd de vuelta a `~` ≡ `/`).
        return CommandResult(new_cwd="/", noise=noise)
    if n > 1:
        return CommandResult(stderr="cd: too many arguments", exit_code=1, noise=noise)

    # Aquí n == 1 (la typer no puede estrechar un `tuple[str, ...]`).
    target = list(argv)[0]
    # Validación PRIMERO: los errores salen antes de tocar la cwd.
    try:
        fs.get_dir(target, cwd)
    except FsError as e:
        return CommandResult(
            stderr=_cd_kind_message(e.kind, target), exit_code=1, noise=noise
        )
    # Normalización de string pura; el destino ya está validado.
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