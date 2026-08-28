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
from core.sandbox.commands.files import SPECS as FILE_SPECS
from core.sandbox.commands.navigation import SPECS as NAVIGATION_SPECS
from core.sandbox.fs import FileSystem
from core.sandbox.noise import NoiseMeter

#: Comandos del set del cap. 0 (tutorial). 🧭1 APROBADA por Gwyn (27/08):
#: `cp` es el 4.º concepto del cap. 0 — copiar ES el objetivo del primer
#: encargo (aprender-por-necesidad, DESIGN §6.1).
DEFAULT_CAP0_COMMANDS: tuple[str, ...] = ("cat", "cd", "cp", "ls")

#: Todas las specs implementadas (registro completo del módulo v0).
SPECS_ALL = NAVIGATION_SPECS + FILE_SPECS

#: Caracteres de sintaxis NO soportada en v0 (fuera de comillas). `|` = pipes,
#: `*?<` = globs, `>` = redirección; `&`/`;` = encadenado (BUG de Oscar,
#: zona 🔬 28/08: `cd /srv && ls` producía «cd: too many arguments» — engañoso).
#: Entre comillas SON literales reales (`cat "a&b.txt"` es un nombre válido).
_UNSUPPORTED_SYNTAX = frozenset("|*?<>&;")

#: Mensaje didáctico de sintaxis futura (caps. 1–2; PLAN §3 + 🧭3 de Oscar:
#: la terminal también ENSEÑA qué no sabe hacer AÚN — nunca culpar al comando
#: equivocado: «esta sesión va comando a comando; el encadenado llega después»).
_SYNTAX_MSG = (
    "sh: syntax not supported in this session: it runs one command at a time "
    "(pipes and chaining arrive later)"
)


def _has_unsupported_syntax(line: str) -> bool:
    """True si hay `|*?<>` FUERA de comillas (entre comillas son literales)."""
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
        self.registry = build_registry(
            tuple(spec for spec in SPECS_ALL if spec.name in wanted)
        )

    # ---- ejecución -------------------------------------------------------

    def execute(self, line: str) -> CommandResult:
        """Ejecuta una línea; muta cwd/tick/historial y devuelve el resultado.

        Línea vacía → éxito sin efecto (como pulsar Enter en una terminal
        real). Comandos desconocidos → exit 127 con stderr de `sh` real.
        """
        stripped = line.strip()
        if not stripped:
            return CommandResult()

        if _has_unsupported_syntax(stripped):
            return self._record(line, CommandResult(stderr=_SYNTAX_MSG, exit_code=2))

        try:
            argv = tuple(shlex.split(stripped, posix=True))
        except ValueError:
            # Comillas sin cerrar u otros errores léxicos de shell real.
            return self._record(
                line,
                CommandResult(
                    stderr="sh: syntax error: unexpected end of file", exit_code=2
                ),
            )

        name, args = argv[0], argv[1:]
        spec = self.registry.get(name)
        if spec is None:
            result = CommandResult(
                stderr=f"sh: command not found: {name}", exit_code=127
            )
            return self._record(line, result)

        result = spec.run(self.fs, self.cwd, args, self.tick)
        if result.new_cwd is not None:
            self.cwd = result.new_cwd
        return self._record(line, result)

    def _record(self, line: str, result: CommandResult) -> CommandResult:
        """Anota historial, suma el ruido del resultado y avanza el tick.

        El ruido total suma los eventos que YA viajan en `result.noise`
        (única fuente de verdad: cada comando emite el suyo). Comandos
        desconocidos y errores de sintaxis no suman ruido (perfil 0), pero
        sí consumen un tick: el tiempo simulado corre igual.
        """
        self.history.append({"line": line, "result": result.to_dict()})
        self.total_noise += sum(int(ev.data["amount"]) for ev in result.noise)
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
