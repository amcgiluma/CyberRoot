"""shell.py — la sesión interactiva del sandbox (ARCHITECTURE §2.2).

parser shlex POSIX + registro de comandos + cwd/tick/historial
SIMULADOS. El shell NO sabe qué comandos existen: recibe specs registradas;
v0 expone `DEFAULT_CAP0_COMMANDS = ("cat", "cd", "cp", "ls")` — `cp` entra en
el set por decisión 🧭1 de Gwyn (27/08): copiar ES el objetivo del tutorial.

Sintaxis NO soportada v0 (pipes, globs, redirección — caps. 1–2): se detecta
FUERA de comillas (GNU real: `cat "a*b.txt"` es literal y válido) y se
rechaza con error didáctico + exit 2 (PLAN decisión 3). Sin RNG, sin reloj
real, sin globals mutables; `to_dict`/`from_dict` de la sesión es ida y
vuelta exacta (§1.5).
"""

from __future__ import annotations

import shlex
from typing import Any

from core.sandbox.commands.base import CommandResult, build_registry
from core.sandbox.commands.conteo import SPECS as CONTEO_SPECS
from core.sandbox.commands.senal import SPECS as SENAL_SPECS
from core.sandbox.commands.escalada import (
    AUTH_LOG_PATH,
    SUDO_NAME,
    SUDO_NO_CRED_MSG,
    check_credential,
    signature_line,
)
from core.sandbox.commands.files import SPECS as FILE_SPECS
from core.sandbox.commands.navigation import SPECS as NAVIGATION_SPECS
from core.sandbox.commands.procesos import SPECS as PROCESOS_SPECS
from core.sandbox.commands.texto import SPECS as TEXT_SPECS
from core.sandbox.fs import FileSystem
from core.sandbox.noise import NoiseMeter

#: Comandos del set del cap. 0 (tutorial). 🧭1 APROBADA por Gwyn (27/08):
#: `cp` es el 4.º concepto del cap. 0 — copiar ES el objetivo del primer
#: encargo (aprender-por-necesidad, DESIGN §6.1).
DEFAULT_CAP0_COMMANDS: tuple[str, ...] = ("cat", "cd", "cp", "ls")

#: Comandos del set del cap. 2 (S1, 30/08): añade las tuberías (`grep`, `wc`)
#: al set base. `DEFAULT_CAP0_COMMANDS` sigue intacto (cap. 0 es escenario sin
#: pipes — 🧭8=(b): evalúan los prereqs al abrir, no lo genera el capítulo).
DEFAULT_CH2_COMMANDS: tuple[str, ...] = ("cat", "cd", "cp", "grep", "ls", "wc")

#: Comandos del set del cap. 3 (S1, 31/08): añade la familia procesos (`ps`,
#: `env`) al set del cap. 2. Cap. 0 y cap. 2 quedan INTACTOS (el proceso solo
#: existe cuando el currículo lo presenta — regresión explícita en tests).
#: S1 (01/09): `sudo` entra en el cap. 3 — es donde se GANA la credencial
#: narrativa (DESIGN §6.1). NO existe en cap. 0/2 (exit 127, como `ps`/`env`).
#: S1 (02/09): `kill` entra en el cap. 3 — operar sobre el par ceniza/censo
#: (ps 521/522). Sin `kill` no hay bisturí para la persiana del Faro.
DEFAULT_CH3_COMMANDS: tuple[str, ...] = (
    "cat", "cd", "cp", "env", "grep", "kill", "ls", "ps", "sudo", "wc",
)

#: Comandos del set del cap. 6 (S2, 02/09): desbloquea la familia conteo
#: (head/tail/sort/uniq) sobre la base del cap. 3. El cap. 6 «Faro» lee la
#: Lista de Lumen con grep/wc/pipe + conteo; necesita TODO lo anterior
#: (ps/env/sudo/kill para la persiana) más la lectura frugal. Cap. 0/2/3
#: quedan INTACTOS (regresión 127 en tests).
DEFAULT_CH6_COMMANDS: tuple[str, ...] = (
    "cat", "cd", "cp", "env", "grep", "head", "kill", "ls", "ps", "sort",
    "sudo", "tail", "uniq", "wc",
)

#: Todas las specs implementadas (registro completo del módulo v0 → S2; conteo
#: añadido en S2 01/09, kill en S1 02/09). `sudo` NO es una spec: es un wrapper del shell.
SPECS_ALL = (
    NAVIGATION_SPECS + FILE_SPECS + TEXT_SPECS + PROCESOS_SPECS + CONTEO_SPECS + SENAL_SPECS
)

#: Caracteres de sintaxis NO soportada todavía (fuera de comillas). `*?<` =
#: globs, `>` = redirección, `&`/`;` = encadenado. `|` (tubería) SÍ entra en
#: S1 (30/08): los pipes llegan en el cap. 2. Entre comillas SON literales
#: reales (`cat "a&b.txt"` es un nombre válido).
_UNSUPPORTED_SYNTAX = frozenset("*?<>&;")

#: Mensaje didáctico de sintaxis futura (caps. 2+; PLAN §3 + 🧭3 de Oscar:
#: la terminal también ENSEÑA qué no sabe hacer AÚN — nunca culpar al comando
#: equivocado). Reformulado en S1 (30/08): las tuberías YA están; lo que
#: queda pendiente es encadenado, redirección y globs.
_SYNTAX_MSG = (
    "sh: syntax not supported in this session: it runs one pipeline at a time "
    "(chaining, redirection and globbing arrive later)"
)

#: Mensaje didáctico para >1 pipe (`a | b | c`): el cap. 2 pide UNA tubería.
_PIPE_MSG = (
    "sh: multiple pipelines not supported in this session: chain them one "
    "at a time"
)


def _has_unsupported_syntax(line: str) -> bool:
    """True si hay `*?<>&;` FUERA de comillas (entre comillas son literales).

    `|` (tubería) ya NO está en el set desde S1 (30/08): los pipes llegan en
    el cap. 2 y se parsean aparte en `_split_pipeline`.
    """
    quote: str | None = None
    for ch in line:
        if quote is not None:
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch in _UNSUPPORTED_SYNTAX:
            return True
    return False


def _split_pipeline(line: str) -> list[str]:
    """Trocea `line` por `|` FUERA de comillas (una tubería de N comandos).

    Los pipes entre comillas son literales (`cat "a|b"` no es una tubería).
    Devuelve los trozos tal cual (sin strip interior); el shell valida que
    el cap. 2 solo necesite UNA tubería (2 comandos).
    """
    parts: list[str] = []
    cur: list[str] = []
    quote: str | None = None
    for ch in line:
        if quote is not None:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            cur.append(ch)
        elif ch == "|":
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _join_err(*stderrs: str) -> str:
    """Concatena los stderr de los comandos de una tubería (orden, `\n`).

    GNU escribe cada stderr a su salida; aquí los juntamos en el orden de
    ejecución para que el post-mortem/o el jugador lea ambos diagnósticos.
    Evita líneas en blanco y vacíos.
    """
    non_empty = [s for s in stderrs if s]
    return "\n".join(non_empty)


class Shell:
    """Una sesión de terminal virtual sobre un FileSystem (serializable)."""

    def __init__(
        self,
        fs: FileSystem,
        *,
        user: str = "operator",
        host: str = "node",
        cwd: str = "/",
        tick: int = 0,
        commands: tuple[str, ...] = DEFAULT_CAP0_COMMANDS,
    ) -> None:
        self.fs = fs
        self.user = user
        self.host = host
        self.cwd = cwd
        self.tick = tick
        self.total_noise = 0
        self.history: list[dict[str, Any]] = []
        wanted = set(commands)
        self.available_commands = wanted.copy()
        self.registry = build_registry(
            tuple(spec for spec in SPECS_ALL if spec.name in wanted)
        )

    # ---- ejecución -------------------------------------------------------

    def _exec_argv(
        self, argv: tuple[str, ...], stdin: str = ""
    ) -> CommandResult:
        """Ejecuta UN comando (argv ya parseado) con su stdin virtual.

        Resuelve la spec, invoca `spec.run(fs, cwd, argv, tick, stdin)` y
        aplica `new_cwd` si el comando cambió de directorio. NO registra en
        el historial ni suma ruido: eso lo hace `execute`/`_record` una vez
        por LÍNEA (para que una tubería quede como UNA entrada con el ruido
        de AMBOS comandos).

        `sudo` (S1, 01/09) es un WRAPPER de orquestación, no una spec: se
        despacha aquí SI la sesión lo expone (`available_commands`). Si la
        sesión no lo expone (cap. 0/2), `SUDO_NAME` no está en el registry y
        cae al `command not found` de abajo (exit 127), igual que `ps`/`env`.
        """
        if argv[0] == SUDO_NAME and SUDO_NAME in self.available_commands:
            return self._exec_sudo(argv, stdin)
        spec = self.registry.get(argv[0])
        if spec is None:
            return CommandResult(
                stderr=f"sh: command not found: {argv[0]}", exit_code=127
            )
        result = spec.run(self.fs, self.cwd, argv[1:], self.tick, stdin)
        if result.new_cwd is not None:
            self.cwd = result.new_cwd
        return result

    def _exec_sudo(
        self, argv: tuple[str, ...], stdin: str = ""
    ) -> CommandResult:
        """`sudo <cmd> [args...]` — elevación con credencial narrativa (cap. 3).

        Forma firma DESIGN §6.1 (S1, 01/09):
          - sin credencial  → rechazo diegético accionable, exit 1, ruido 0.
          - con credencial  → ejecuta el comando envuelto (registry), factura
            ruido PREMIUM (extra sobre el base del comando) y deja firma en
            `AUTH_LOG_PATH` (usuario, comando, tick) via `fs.append_file`.
        Si el comando envuelto no existe → `sh: command not found: cmd`
        (exit 127), igual que el shell sin sudo. La credencial vive en el FS de
        la sala (contrato O1↔S1); NO es una contraseña tecleada.
        """
        if len(argv) < 2:
            return CommandResult(
                stderr="sudo: no command given\n", exit_code=1
            )
        # Sin credencial: intentar no es delinquir — rechazo sin ruido.
        if not check_credential(self.fs, self.cwd):
            return CommandResult(stderr=SUDO_NO_CRED_MSG + "\n", exit_code=1)

        wrapped = argv[1:]
        spec = self.registry.get(wrapped[0])
        if spec is None:
            return CommandResult(
                stderr=f"sh: command not found: {wrapped[0]}", exit_code=127
            )
        result = spec.run(self.fs, self.cwd, wrapped[1:], self.tick, stdin)
        if result.new_cwd is not None:
            self.cwd = result.new_cwd

        # Ruido PREMIUM: el wrapper emite el extra (base + premium = factura)
        # y deja firma en el auth.log — el poder deja factura (§6.1).
        premium = NoiseMeter().emit(SUDO_NAME, tuple(wrapped), self.tick)
        noise = result.noise + (premium,)
        self.fs.append_file(
            AUTH_LOG_PATH,
            signature_line(self.user, wrapped[0], tuple(wrapped[1:]), self.tick),
        )
        return CommandResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            noise=noise,
            new_cwd=result.new_cwd,
        )

    def execute(self, line: str) -> CommandResult:
        """Ejecuta una línea; muta cwd/tick/historial y devuelve el resultado.

        Línea vacía → éxito sin efecto (como pulsar Enter en una terminal
        real). Comandos desconocidos → exit 127 con stderr de `sh` real.
        Una tubería `cmd1 | cmd2` (S1, 30/08) ejecuta `cmd1` con stdin vacío,
        captura su stdout y lo alimenta como stdin de `cmd2`; el resultado se
        registra como UNA línea con el ruido de ambos comandos.
        """
        stripped = line.strip()
        if not stripped:
            return CommandResult()

        if _has_unsupported_syntax(stripped):
            return self._record(line, CommandResult(stderr=_SYNTAX_MSG, exit_code=2))

        pipeline = _split_pipeline(stripped)
        if len(pipeline) > 2:
            # El cap. 2 solo pide UNA tubería; más de un `|` es fuera de alcance.
            return self._record(line, CommandResult(stderr=_PIPE_MSG, exit_code=2))

        try:
            argv = tuple(shlex.split(pipeline[-1], posix=True))
        except ValueError:
            # Comillas sin cerrar u otros errores léxicos de shell real.
            return self._record(
                line,
                CommandResult(
                    stderr="sh: syntax error: unexpected end of file", exit_code=2
                ),
            )

        if not argv:
            return self._record(line, CommandResult())

        if len(pipeline) == 1:
            return self._record(line, self._exec_argv(argv))

        # Tubería: `cmd1 | cmd2`. El primer comando arranca sin stdin.
        try:
            argv1 = tuple(shlex.split(pipeline[0], posix=True))
        except ValueError:
            return self._record(
                line,
                CommandResult(
                    stderr="sh: syntax error: unexpected end of file", exit_code=2
                ),
            )
        if not argv1:
            return self._record(
                line, CommandResult(stderr=_PIPE_MSG, exit_code=2)
            )
        left = self._exec_argv(argv1)
        # stdbuf del pipe: el stdout del izquierdo es el stdin del derecho.
        result = self._exec_argv(argv, stdin=left.stdout)
        # Combinar: stdout del último, stderr de ambos (el orden manda),
        # ruido de AMBOS (la tubería no es gratis — AC S1), exit del último.
        combined = CommandResult(
            stdout=result.stdout,
            stderr=_join_err(left.stderr, result.stderr),
            exit_code=result.exit_code,
            noise=left.noise + result.noise,
            new_cwd=result.new_cwd,
        )
        return self._record(line, combined)

    def _record(self, line: str, result: CommandResult) -> CommandResult:
        """Anota historial, suma el ruido del resultado y avanza el tick.

        El ruido total suma los eventos que YA viajan en `result.noise`
        (única fuente de verdad: cada comando emite el suyo). Comandos
        desconocidos y errores de sintaxis no suman ruido (perfil 0), pero
        sí consumen un tick: el tiempo simulado corre igual.
        """
        self.history.append({"line": line, "result": result.to_dict()})
        self.total_noise += sum(int(ev.data.get("amount", 0)) for ev in result.noise)
        self.tick += 1
        return result

    # ---- serialización (ARCHITECTURE §1.5) -------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Sesión completa a dict plano (fs, cwd, tick, historial)."""
        return {
            "fs": self.fs.to_dict(),
            "user": self.user,
            "host": self.host,
            "cwd": self.cwd,
            "tick": self.tick,
            "total_noise": self.total_noise,
            "history": [
                {"line": h["line"], "result": h["result"]} for h in self.history
            ],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Shell":
        """Reconstruye la sesión; copia independiente del original."""
        shell = cls(
            FileSystem.from_dict(d["fs"]),
            user=str(d["user"]),
            host=str(d["host"]),
            cwd=str(d["cwd"]),
            tick=int(d["tick"]),
        )
        shell.total_noise = int(d["total_noise"])
        shell.history = [dict(h) for h in d["history"]]
        return shell
