"""stat.py — `stat` lector del testigo (T3 21/09, Smough).

Muestra atributos del FileNode custodiado `/tmp/volcado-custodia.csv`
como lector diegético de la hora 03:14 y el peso 512. Si el fichero
existe → stdout con `Size: 512` y `Modify: 03:14:00` (contenido
TR-003|EN_COLA), exit 0. Si no existe → GNU-honesto
`stat: cannot stat '...': No such file or directory` exit 1.

Fuera de la allowlist del cap. 5 el shell lo rechaza con 127 (frontera
honesta: el comando existe pero el encargo no lo expone).
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import FileNode, FsError

STAT_NAME = "stat"

# Literal custodiado — must match chapter5.CUSTODIA_PATH
CUSTODIA_PATH = "/tmp/volcado-custodia.csv"
# Tamaño narrativo (bytes del volcado EN_COLA) — no len(content)
CUSTODIA_SIZE = 512
CUSTODIA_MODIFY = "03:14:00"


def _run_stat(
    fs,  # FileSystem
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`stat FICHERO` — atributos del nodo.

    - 0 operandos → GNU `stat: missing operand` exit 1
    - 1 operando → intenta `fs.resolve`; si falta → cannot stat + exit 1
    - si existe → stdout con File/Size/Modify + exit 0
    - múltiples operandos → procesa cada uno (GNU); el primero que falla marca exit 1
    """
    noise = noise_event(STAT_NAME, argv, tick)
    if len(argv) == 0:
        return CommandResult(
            stderr="stat: missing operand\nTry 'stat --help' for more information.\n",
            exit_code=1,
            noise=noise,
        )
    # --help honesto (no cuenta como fallo del testigo)
    if argv[0] in ("--help", "-h"):
        return CommandResult(
            stdout="Usage: stat FILE\nDisplay file status.\n",
            exit_code=0,
            noise=noise,
        )
    # GNU: -- fin de opciones
    paths = list(argv)
    if paths and paths[0] == "--":
        paths = paths[1:]
        if not paths:
            return CommandResult(
                stderr="stat: missing operand\nTry 'stat --help' for more information.\n",
                exit_code=1,
                noise=noise,
            )
    # Procesar (para AC basta uno, pero soportamos varios)
    out_parts: list[str] = []
    err_parts: list[str] = []
    exit_code = 0
    for p in paths:
        # rechazo de opciones no soportadas → GNU
        if p.startswith("-") and p != "-":
            err_parts.append(f"stat: invalid option -- '{p.lstrip('-')}'\nTry 'stat --help' for more information.")
            exit_code = 1
            continue
        try:
            node = fs.resolve(p, cwd)
        except FsError as e:
            if e.kind == "not_found":
                err_parts.append(f"stat: cannot stat '{p}': No such file or directory")
            elif e.kind == "not_a_directory":
                err_parts.append(f"stat: cannot stat '{p}': Not a directory")
            else:
                err_parts.append(f"stat: cannot stat '{p}': {e.kind}")
            exit_code = 1
            continue
        # Éxito — construir salida
        abs_path = fs.abspath(p, cwd)
        is_dir = not isinstance(node, FileNode)
        # Size: para custodia → 512 narrativo, resto → len(content) o 4096 si dir
        if abs_path == CUSTODIA_PATH and isinstance(node, FileNode):
            size = CUSTODIA_SIZE
        else:
            if isinstance(node, FileNode):
                size = len(node.content)
            else:
                size = 4096
        # Modify: custodia → 03:14:00, resto → derivado de mtime (00:00:00 si 0)
        if abs_path == CUSTODIA_PATH and isinstance(node, FileNode):
            modify = CUSTODIA_MODIFY
        else:
            # mtime 0 → 00:00:00, mtime con valor → formateado simple
            if node.mtime == 0:
                modify = "00:00:00"
            else:
                # mtime simulado → mostrar como segundos desde epoch fake
                # Para no inventar fecha, mostramos solo la hora derivada
                secs = node.mtime % 86400
                h = secs // 3600
                m = (secs % 3600) // 60
                s = secs % 60
                modify = f"{h:02d}:{m:02d}:{s:02d}"
        # Formato: mínima réplica de GNU stat que contiene los dos campos clave
        if isinstance(node, FileNode):
            file_type = "regular file"
        else:
            file_type = "directory"
        out_parts.append(
            f"  File: {abs_path}\n"
            f"  Size: {size}\t\tBlocks: 8\t  IO Block: 4096   {file_type}\n"
            f"Device: 0h/0d\tInode: 1\t  Links: 1\n"
            f"Access: ({node.mode}/{(node.mode)})  Uid: ( 1000/ {node.owner})   Gid: ( 1000/ {node.group})\n"
            f"Modify: 2025-09-21 {modify}.000000000 +0000\n"
        )
    stdout = "".join(out_parts)
    stderr = "\n".join(err_parts)
    if stderr and not stderr.endswith("\n"):
        stderr += "\n" if err_parts else ""
        # GNU termina errores con newline — asegurar
        if err_parts and not stderr.endswith("\n"):
            stderr += "\n"
    # Ajuste: si hubo errores, GNU stat emite una línea por fichero fallido con \n
    # Ya añadimos \n por cada err_part; join con \n ya lo tiene. Normalizar doble \n
    if err_parts:
        # Cada err_part ya sin \n final salvo que lo añadimos; asegurar formato
        stderr = "\n".join(err_parts) + ("\n" if err_parts else "")
    return CommandResult(stdout=stdout, stderr=stderr, exit_code=exit_code, noise=noise)


STAT_SPEC = CommandSpec(
    name=STAT_NAME,
    concepts=frozenset({"stat"}),
    noise=1,
    run=_run_stat,
)

SPECS: tuple[CommandSpec, ...] = (STAT_SPEC,)
