"""base.py — contratos y registro de comandos (ARCHITECTURE §2.2, PLAN §Estructura).

`CommandResult` empaqueta el resultado observable de un comando: `stdout` /
`stderr` TAL CUAL el comando los emite (newlines incluidos, reproducibilidad
byte a byte), exit code, eventos de ruido y, en su caso, la nueva cwd (`cd`).
Inmutable y serializable ida y vuelta exacta (ARCHITECTURE §1.5).

`CommandSpec` declara qué sabe hacer un comando: nombre, conceptos que alimentan
el pool del generador (§6.4.2), coste de ruido y el callable de ejecución. El
callable recibe (fs, cwd, argv, tick) y devuelve un `CommandResult`.

`CommandRegistry` guarda las specs SIN estado mutable global (ARCHITECTURE §3):
la instancia vive en el shell que la crea; aquí solo contenedor + órdenes
(por codepoint para names/specs; dict por inserción internamente).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from core.sandbox.fs import FileSystem
from core.sandbox.noise import NoiseMeter

#: Firmado de un comando: recibe el FS, la cwd, los argv y el tick simulado.
CommandRunner = Callable[[FileSystem, str, tuple[str, ...], int], "CommandResult"]


def noise_event(command: str, argv: tuple[str, ...], tick: int) -> tuple[dict, ...]:
    """Evento(s) de ruido que emite un comando (forma Event, PLAN decisión 4).

    Cada invocación emite UN evento via `NoiseMeter.emit` (cantidad del perfil
    de noise.py); el coste de DETECCIÓN lo decide el engine, no el sandbox
    (ARCHITECTURE §2.2: «aquí solo se emite»).
    """
    return (NoiseMeter().emit(command, argv, tick),)


@dataclass(frozen=True)
class CommandResult:
    """Resultado observable de un comando (stdout/stderr byte a byte).

    `stdout` lleva EXACTAMENTE lo que imprimió el comando — cada elemento de
    `ls` con su `\n`, el contenido de `cat` tal cual — para golden tests
    exactos. `new_cwd` lo rellena solo `cd` (None = la cwd no cambia).
    """

    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    noise: tuple[dict, ...] = ()
    new_cwd: str | None = None

    @property
    def ok(self) -> bool:
        """Éxito GNU: exit code 0."""
        return self.exit_code == 0

    def to_dict(self) -> dict[str, Any]:
        """Serializa (noise como lista); ida y vuelta exacta con from_dict."""
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "noise": list(self.noise),
            "new_cwd": self.new_cwd,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "CommandResult":
        """Inverso exacto de `to_dict`."""
        return cls(
            stdout=str(d["stdout"]),
            stderr=str(d["stderr"]),
            exit_code=int(d["exit_code"]),
            noise=tuple(d["noise"]),
            new_cwd=d["new_cwd"],
        )


@dataclass(frozen=True)
class CommandSpec:
    """Receta de un comando registrable (nombre, conceptos, noise, run)."""

    name: str
    concepts: frozenset[str]
    noise: int
    run: CommandRunner


class CommandRegistry:
    """Tabla nombre→spec, construida por el shell (sin globals mutables)."""

    def __init__(self) -> None:
        # Ordenado por inserción; las consultas exteriores van por codepoint.
        self._by_name: dict[str, CommandSpec] = {}

    def register(self, spec: CommandSpec) -> None:
        """Registra (sobrescribe) una spec por su nombre."""
        self._by_name[spec.name] = spec

    def get(self, name: str) -> CommandSpec | None:
        """Devuelve la spec o None si el comando no está registrado."""
        return self._by_name.get(name)

    def names(self) -> tuple[str, ...]:
        """Nombres registrados ordenados por codepoint (determinismo PLAN §5)."""
        return tuple(sorted(self._by_name.keys()))

    def specs(self) -> tuple[CommandSpec, ...]:
        """Specs en el mismo orden codepoint que `names`."""
        return tuple(self._by_name[n] for n in self.names())


def build_registry(specs: tuple[CommandSpec, ...]) -> CommandRegistry:
    """Crea una registry con las specs dadas (comodidad para el shell y tests)."""
    reg = CommandRegistry()
    for spec in specs:
        reg.register(spec)
    return reg