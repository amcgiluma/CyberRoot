"""files.py — `cat` y `cp` (familia texto/pipes, ARCHITECTURE §2.2).

`cat` vuelca ficheros a stdout TAL CUAL su contenido (newlines YA incluidos,
aquí NO se añade ninguno) y termina con exit 1 ante cualquier error, aunque
haya impreso los buenos (GNU cat). `cp` copia UN fichero con sus metadatos
(`fs.copy_file`), sobrescribiendo el destino si ya es fichero; v0 no soporta
destino-directorio ni copia múltiple (PLAN decisión 1-cp). Salidas y mensajes
en inglés GNU (DESIGN §2.6.8). Prohibido `random`: nada aleatorio aquí.
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import DirNode, FileNode, FileSystem, FsError
from core.sandbox.noise import NOISE_PROFILE

CAT_NAME = "cat"
CP_NAME = "cp"

#: kind → texto GNU para `cp` (PLAN §decisión 3, simplificado).
#:
#: ⚠️ GNU real (verificado contra coreutils en Ubuntu 27/08): `cp fichero
#: dir_existente/` copia DENTRO del dir (fs.copy_file lo hace) — el error
#: «omitting directory» solo aplica a FUENTES-dir, que v0 rechaza antes.
_CP_KIND_MESSAGE: dict[str, str] = {
    "not_found": "No such file or directory",
    "not_a_directory": "Not a directory",
    "is_a_directory": "Is a directory",
    "permission_denied": "Permission denied",
    "not_empty": "Directory not empty",
    "invalid_argument": "Invalid argument",
    "same_file": "are the same file",
}


def _cat_kind_message(kind: str, arg: str) -> str:
    """Texto GNU de `cat` para un error `kind` sobre el operando `arg`."""
    if kind == "not_a_directory":
        return f"cat: {arg}: Not a directory"
    return f"cat: {arg}: {_CP_KIND_MESSAGE.get(kind, kind)}"


def _run_cat(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int) -> CommandResult:
    """`cat`: concatena los contenidos byte a byte; exit 1 si hubo cualquier error.

    Cada contenido se apenda TAL CUAL (`read_file` ya trae sus newlines; NO se
    añade ninguno). Con 0 operandos GNU leería stdin y colgaría esperando EOF;
    como v0 no tiene stdin virtual (no hay pipes/redirecciones, PLAN §3),
    cerramos con un error didáctico claro en vez de colgarnos.
    """
    noise = noise_event(CAT_NAME, argv, tick)
    if not argv:
        return CommandResult(
            stderr="cat: no input file given", exit_code=1, noise=noise
        )

    chunks: list[str] = []
    err_lines: list[str] = []
    for arg in argv:
        # GNU real: una barra final fuerza a tratar el operando como RUTA A
        # DIRECTORIO. `cat fichero/` → «Not a directory» (el nodo es un
        # fichero); `cat dir/` → «Is a directory» (cat sobre un dir). Sin la
        # barra, `cat fichero` vuelca el contenido y `cat dir` da «Is a
        # directory» — la barra solo añade el caso «Not a directory».
        if arg.endswith("/"):
            try:
                node = fs.resolve(arg, cwd)
            except FsError as e:
                err_lines.append(_cat_kind_message(e.kind, arg))
                continue
            if isinstance(node, FileNode):
                err_lines.append(_cat_kind_message("not_a_directory", arg))
                continue
            # Es un directorio: dejamos que read_file emita «Is a directory».
        try:
            chunks.append(fs.read_file(arg, cwd))
        except FsError as e:
            err_lines.append(_cat_kind_message(e.kind, arg))

    return CommandResult(
        stdout="".join(chunks),
        stderr="\n".join(err_lines),
        exit_code=1 if err_lines else 0,
        noise=noise,
    )


def _cp_src_message(kind: str, src: str) -> str:
    """Mensaje GNU para un fallo al RESOLVER el fuente (pre-validación).

    Un fuente inexistente es el caso real «cannot stat» de cp; cualquier otro
    kind se traduce con el mapa de texto del destino.
    """
    if kind == "not_found":
        return f"cp: cannot stat '{src}': No such file or directory"
    return f"cp: {src}: {_CP_KIND_MESSAGE.get(kind, kind)}"


def _run_cp(fs: FileSystem, cwd: str, argv: tuple[str, ...], tick: int) -> CommandResult:
    """`cp`: copia un fichero con sus metadatos; stdout vacío en éxito.

    El mapeo src/dst del mensaje es por ORDEN: primero pre-valido el fuente con
    `resolve(src, cwd)` (errores → mensaje con el src); luego dejo que
    `copy_file` resuelva su parte de destino (errores → mensaje con el dst).
    Requiere exactamente 2 operandos; más de 2 implicaría destino-directorio
    (no soportado en v0) → mensaje GNU real de target no-directorio.
    """
    noise = noise_event(CP_NAME, argv, tick)
    n = len(argv)
    if n == 0:
        return CommandResult(stderr="cp: missing file operand", exit_code=1, noise=noise)
    if n == 1:
        return CommandResult(
            stderr="cp: missing destination file operand", exit_code=1, noise=noise
        )
    if n > 2:
        # Con >2 operandos GNU copiaría dentro del último como directorio.
        return CommandResult(
            stderr=f"cp: target '{argv[-1]}' is not a directory",
            exit_code=1,
            noise=noise,
        )

    src = argv[0]
    dst = argv[1]
    # Distinguir src vs dst por orden: pre-validar el fuente primero.
    try:
        src_node = fs.resolve(src, cwd)
    except FsError as e:
        return CommandResult(
            stderr=_cp_src_message(e.kind, src), exit_code=1, noise=noise
        )
    # GNU real: copiar un DIRECTORIO sin `-r` diagnostica el ORIGEN y aborta
    # antes de tocar nada («omitting directory»), no culpa al destino. Reproduc
    # de Havel (28/08): `cp /srv /usb/` debía decir esto, no «cp: /usb/: ...».
    if isinstance(src_node, DirNode):
        return CommandResult(
            stderr=f"cp: -r not specified; omitting directory '{src}'",
            exit_code=1,
            noise=noise,
        )
    try:
        fs.copy_file(src, dst, cwd)
    except FsError as e:
        if e.kind == "same_file":
            # GNU: cp: 'f' and 'f' are the same file
            msg = f"cp: '{src}' and '{dst}' are the same file"
        else:
            msg = f"cp: {dst}: {_CP_KIND_MESSAGE.get(e.kind, e.kind)}"
        return CommandResult(stderr=msg, exit_code=1, noise=noise)
    return CommandResult(noise=noise)


CAT_SPEC = CommandSpec(
    name=CAT_NAME,
    concepts=frozenset({"cat"}),
    noise=NOISE_PROFILE[CAT_NAME],
    run=_run_cat,
)

CP_SPEC = CommandSpec(
    name=CP_NAME,
    concepts=frozenset({"cp"}),
    noise=NOISE_PROFILE[CP_NAME],
    run=_run_cp,
)

SPECS: tuple[CommandSpec, ...] = (CAT_SPEC, CP_SPEC)