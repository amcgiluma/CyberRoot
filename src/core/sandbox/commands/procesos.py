"""procesos.py — `ps` y `env` (familia procesos, cap. 3, ARCHITECTURE §2.2).

Llegan con S1 (31/08): el cap. 3 «Bombas» de Manus pide leer qué corre y de
quién (`ps aux`: la columna USER delata al proceso — «la diferencia entre los
dos cabe en una columna») y las variables de entorno de la sesión (`env`).

CERO RNG (§2.2): los procesos simulados son PIEL del generador — viven como
`fs.processes` (Proceso en fs.py) y `env` en `fs.environment`; el sandbox solo
los RENDERIZA en orden de PID (determinista). Semántica REAL de GNU (DESIGN
§2.6.8): cabeceras y mensajes de error en inglés/exit codes reales.

Formato verificado contra coreutils real (Ubuntu, 31/08):
- `ps`          → cabecera `    PID TTY          TIME CMD`
- `ps aux`      → cabecera `USER         PID %CPU %MEM    VSZ   RSS TTY      STAT
                   START   TIME COMMAND`
- `env`         → `VAR=valor` por línea (GNU imprime el entorno real; nosotros
                   fijamos el ORDEN por clave para reproducibilidad §5)
"""

from __future__ import annotations

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import FileSystem
from core.sandbox.noise import NOISE_PROFILE

PS_NAME = "ps"
ENV_NAME = "env"

_PS_HEADER = "    PID TTY          TIME CMD"
_PS_AUX_HEADER = (
    "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
)


def _ps_row(pid: int, tty: str, time: str, cmd: str) -> str:
    """Fila del `ps` compacto (columnas GNU: pid der, tty izq, time der)."""
    return f"{pid:>5} {tty:<10}{time:>8} {cmd}"


def _ps_aux_row(
    user: str, pid: int, cpu: str, mem: str,
    vsz: str, rss: str, tty: str, stat: str, start: str, time: str, cmd: str,
) -> str:
    """Fila del `ps aux` (columnas GNU: USER izq, números der)."""
    return (
        f"{user:<10} {pid:>5} {cpu:>4} {mem:>4} {vsz:>7} {rss:>5} "
        f"{tty:<6} {stat:<4} {start:>5} {time:>8} {cmd}"
    )


def _run_ps(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`ps` / `ps aux`: lista los procesos simulados de la sala (orden por PID).

    `ps` sin flags → cabecera compacta + filas básicas. `ps aux` (o `-aux` /
    `-ef` en su forma `aux`) → cabecera completa con columna USER. Opción
    desconocida → `ps: unknown option -- 'x'` exit 2 (GNU). Sin procesos en la
    sala, imprime solo la cabecera (GNU no lista nada si no hay run).
    """
    noise = noise_event(PS_NAME, argv, tick)

    # Normaliza el flag de «todos los procesos». GNU acepta `aux`, `-aux`, `-ef`,
    # `e`, `-e`. Para el contrato pedagógico del cap. 3 basta `aux` (la forma que
    # pide la prosa de Manus) y su alias `-aux`; el resto de flags → error GNU.
    aux = False
    for a in argv:
        if a in ("aux", "-aux", "-ef", "e", "-e"):
            aux = True
        elif a.startswith("-"):
            return CommandResult(
                stderr=f"ps: unknown option -- '{a.lstrip('-')}'",
                exit_code=2,
                noise=noise,
            )
        else:
            # `ps 123` (buscar por PID) no está en el contrato del cap. 3.
            return CommandResult(
                stderr=f"ps: {a}: no se admiten operandos en esta versión",
                exit_code=2,
                noise=noise,
            )

    procs = sorted(fs.processes, key=lambda p: p.pid)
    if aux:
        lines = [_PS_AUX_HEADER]
        for p in procs:
            lines.append(
                _ps_aux_row(
                    p.user, p.pid, p.cpu, p.mem, p.vsz, p.rss,
                    p.tty, p.stat, p.start, p.time, p.cmd,
                )
            )
    else:
        lines = [_PS_HEADER]
        for p in procs:
            lines.append(_ps_row(p.pid, p.tty, p.time, p.cmd))

    return CommandResult(stdout="\n".join(lines) + "\n", noise=noise)


def _run_env(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`env` de solo-lectura: imprime las variables de la sesión (`VAR=valor`).

    ORDEN por clave (codepoint): GNU imprime el entorno en el orden real de la
    tabla de entorno; nosotros lo fijamos para reproducibilidad byte a byte
    (§5). Flags o programas no soportados → rechazo GNU-honesto. No existe el
    `env VAR=x cmd` ni `env -i` en el contrato pedagógico de momento (cap. 3
    solo LEE variables).
    """
    noise = noise_event(ENV_NAME, argv, tick)
    if argv:
        first = argv[0]
        if first.startswith("-"):
            return CommandResult(
                stderr=f"env: invalid option -- '{first.lstrip('-')}'",
                exit_code=2,
                noise=noise,
            )
        # `env VAR=1 cmd`: ejecutar un programa con entorno modificado no es del
        # contrato v1 del cap. 3 — rechazo didáctico con la voz del shell.
        return CommandResult(
            stderr=(
                "env: running a command with a modified environment is not "
                "supported in this session yet"
            ),
            exit_code=2,
            noise=noise,
        )

    lines = [f"{k}={v}" for k, v in sorted(fs.environment.items())]
    return CommandResult(stdout=("\n".join(lines) + "\n") if lines else "", noise=noise)


PS_SPEC = CommandSpec(
    name=PS_NAME,
    concepts=frozenset({"ps"}),
    noise=NOISE_PROFILE[PS_NAME],
    run=_run_ps,
)

ENV_SPEC = CommandSpec(
    name=ENV_NAME,
    concepts=frozenset({"env"}),
    noise=NOISE_PROFILE[ENV_NAME],
    run=_run_env,
)

SPECS: tuple[CommandSpec, ...] = (PS_SPEC, ENV_SPEC)