"""core.sandbox.__main__ — REPL (S2, Smough 29/08): `python -m core.sandbox`.

El primer punto de entrada TOCABLE del sandbox sin esperar al engine (Oscar,
`[PENDIENTE][P2]`, 28/08): abre una sesión real del cap. 0 con prompt
diegético (`operador@oficina-vecinal:~$`, estilo DESIGN §6.1), lee una línea,
ejecuta contra el `Shell`, e imprime stdout y stderr tal cual la sesión
testeada, anotando el exit code cuando ≠0. `exit` / `quit` / Ctrl-D cierran la
sesión.

Sin dependencias nuevas y sin lógica fuera del sandbox: el bucle reutilizable
`run_repl` recibe la sesión, un iterable de líneas y un par de callables de
escritura para poder TESTEARSE de forma programática (no hace falta TTY, AC de
S2). `main()` solo la cablea sobre `sys.stdin`/`sys.stdout`/`sys.stderr`.

Determinismo puro (ARCHITECTURE §2.2): el FS de la escena es estático y la
sesión no usa RNG, así que la salida es reproducible byte a byte entre
procesos.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from typing import TextIO

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell

#: Saludo diegético al conectar (estilo §6.1: la terminal enmarca la escena).
_BANNER = "conectando → oficina-vecinal-muelle-norte...\n"

#: Comandos que cierran la sesión (además de Ctrl-D / EOF).
_EXIT_WORDS = frozenset({"exit", "quit"})


def build_cap0_session() -> Shell:
    """Sesión real del cap. 0 «Trabajo en frío» (escena de `CAPITULOS/
    00-la-firma.md`: la oficina-vecinal-muelle-norte con su dossier, y el USB
    de 512 MB colgando de la raíz — opción B, DESIGN §6.1).

    El FS replica EXACTAMENTE la piel de `test_session_cap0._fs_oficina()`
    (mismos ficheros, contenidos y mtimes) para que lo que se juega en el REPL
    sea idéntico a la secuencia congelada en el test de sesión.
    """
    fs = FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "oficina-vecinal-muelle-norte": DirNode(
                            name="oficina-vecinal-muelle-norte",
                            children={
                                "nombre_de_proveedor.txt": FileNode(
                                    name="nombre_de_proveedor.txt",
                                    content=(
                                        "CANDELAS  ·  proveedor nº 47  ·  "
                                        "facturación externa  ·  114 facturas/mes\n"
                                    ),
                                    owner="recepcion",
                                    group="empleados",
                                    mtime=1044,  # 11:04, tiempo simulado
                                ),
                                "log.txt": FileNode(
                                    name="log.txt",
                                    content="08:59 turno de mañana\n11:04 SIN REGISTRO\n",
                                    mtime=1030,
                                ),
                                "README": FileNode(
                                    name="README",
                                    content="Sistema de gestion de la oficina vecinal.\n",
                                    mtime=900,
                                ),
                            },
                        )
                    },
                ),
                "usb": DirNode(name="usb", children={}),  # el USB de 512 MB
            },
        )
    )
    return Shell(
        fs,
        user="operador",
        host="oficina-vecinal",
        cwd="/",
        commands=("cat", "cd", "cp", "ls"),
    )


def _prompt(shell: Shell) -> str:
    """Prompt diegético `usuario@host:cwd$ `; la raíz/home se muestra como `~`."""
    cwd = "~" if shell.cwd == "/" else shell.cwd
    return f"{shell.user}@{shell.host}:{cwd}$ "


def run_repl(
    shell: Shell,
    lines: Iterable[str],
    *,
    write_out: Callable[[str], None] | None = None,
    write_err: Callable[[str], None] | None = None,
) -> int:
    """Bucle REATIVO: lee líneas, ejecuta, imprime; devuelve el tick de cierre.

    `write_out` recibe stdout y el prompt (flujo normal); `write_err` recibe
    stderr y los avisos de exit code ≠0. Separados para imitar un terminal real
    (stdout vs stderr) y para que el test capture cada canal por su cuenta.
    `exit`/`quit`/fin de iterable cierran. No gestiona TTY: recibe un iterable
    de líneas, así que es 100 % testeable sin terminal (AC de S2).
    """
    out = write_out or (lambda s: None)
    err = write_err or (lambda s: None)
    out(_BANNER)
    for raw in lines:
        line = raw.rstrip("\n")
        out(_prompt(shell))
        stripped = line.strip()
        if stripped in _EXIT_WORDS:
            break
        result = shell.execute(line)
        if result.stdout:
            out(result.stdout)
        if result.stderr:
            err(result.stderr)
        if result.exit_code != 0:
            err(f"[exit {result.exit_code}]\n")
    return shell.tick


def main() -> int:
    """Cablea `run_repl` sobre la terminal real (stdin/stdout/stderr)."""

    def _out(s: str) -> None:
        sys.stdout.write(s)

    def _err(s: str) -> None:
        sys.stderr.write(s)

    shell = build_cap0_session()
    return run_repl(shell, sys.stdin, write_out=_out, write_err=_err)


if __name__ == "__main__":
    raise SystemExit(main())