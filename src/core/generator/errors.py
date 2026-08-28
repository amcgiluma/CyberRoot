"""errors.py — errores de dominio del generador procedural (§6.4.4).

Tipos base de excepción del módulo `core/generator`. Todo fallo de la etapa
de generación se señala con `GeneratorError` (subclase de `RuntimeError`,
no de `CyberRootError`, porque el generador es un proceso INTERNO del core:
los dicts planos que produce se validan antes de cruzar la frontera, y los
fallos de validación son bugs de generación, no errores de datos del usuario).

Solo stdlib; prohibido `import random`.
"""

from __future__ import annotations

from typing import Any


class GeneratorError(RuntimeError):
    """Base de los errores del módulo `core/generator`."""


class UnsolvableRoomError(GeneratorError):
    """La validación canónica falló: la sala generada NO deja resolver el
    encargo (§6.4.4).

    Una sala que no deja copiar el fichero al USB, o cuya secuencia canónica
    (la de `00-la-firma.md`) ya no devuelve exit 0 byte a byte, es IRRESOLUBLE:
    eso es un bug de generación (un cambio en el FS o en los comandos rompió
    el invariante), no un sesgo de dificultad calibrable. El mensaje guarda el
    `step` exacto que falló (argv + exit_code real + stderr recortado) para
    hacer debugeable el fallo sin depender del estado mutable de la sesión.
    """

    def __init__(
        self,
        message: str,
        *,
        step_index: int,
        argv: tuple[str, ...],
        expect_exit: int,
        exit_code: int,
        stderr: str,
    ) -> None:
        super().__init__(message)
        self.step_index = step_index
        self.argv = argv
        self.expect_exit = expect_exit
        self.exit_code = exit_code
        self.stderr = stderr

    @classmethod
    def from_step(
        cls,
        *,
        step_index: int,
        argv: tuple[str, ...],
        expect_exit: int,
        exit_code: int,
        stderr: str,
        _stderr_max: int = 300,
    ) -> "UnsolvableRoomError":
        """Construye el error con un mensaje stderr recortado (anti-basura)."""
        clipped = stderr if len(stderr) <= _stderr_max else stderr[:_stderr_max] + "…"
        return cls(
            (
                "sala irresoluble en el paso "
                f"{step_index}: {' '.join(argv)!r} esperado exit "
                f"{expect_exit}, obtuvo {exit_code} (stderr={clipped!r})"
            ),
            step_index=step_index,
            argv=argv,
            expect_exit=expect_exit,
            exit_code=exit_code,
            stderr=stderr,
        )

    #: Para que el mensaje del error (no su constructor) no rompa el contrato
    #: de JSON-plano: los atributos estructurados viven como datos sin tocar.
    def as_dict(self) -> dict[str, Any]:
        return {
            "step_index": self.step_index,
            "argv": list(self.argv),
            "expect_exit": self.expect_exit,
            "exit_code": self.exit_code,
            "stderr": self.stderr,
        }