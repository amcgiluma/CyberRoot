"""types.py — tipos base e invariantes del core (ARCHITECTURE §2.1) y utilidad
`ensure_plain` para datos JSON-plano estrictos.

Diseño (ver PLAN.md decisión 7):
- `Command` es un comando ida-y-vuelta plano (§1.2, `{"cmd": ..., ...}`):
  el "cmd" canónico gana siempre; los argumentos NO pueden colisionar con esa
  clave (prohibido en `__post_init__`), de modo que `to_dict`/`from_dict` son
  inversas exactas sin ambigüedad.
- `SeedLike` / `TextKey` son alias documentados: `SeedLike` es coherente con
  la interfaz de `rng.Rng`; `TextKey` marca las claves de texto que el core
  ENTREGA y el render RESUELVE (§3: textos jamás hardcodeados en core).
- `ensure_plain` valida que un objeto sea JSON plano ESTRICTO. El core solo
  persiste/atraviesa tales datos (§3, §4.5); esta utilidad es reusable por
  `state/` (Seath) para garantizar la serializabilidad antes de guardar.
- Solo stdlib; prohibido `import random`; sin estado global mutable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Mapping

from core.common.errors import InvalidCommandError, NotPlainDataError

# --- aliases documentados ----------------------------------------------------

#: Fuente de semilla del RNG (§1.3): sesiones se siembran con un entero o un
#: str/bytes (se dispersa vía sha256 en `rng.py`). Coherente con `Rng`.
SeedLike = int | str | bytes

#: Clave de texto que el core carga y entrega; el RENDER la resuelve a texto
#: visible (§3, ARCHITECTURE §3: «Core carga y devuelve claves de texto; el
#: render las resuelve»). Doc-only alias: en runtime es un `str` puro.
TextKey = str

# --- utilidad JSON-plano -----------------------------------------------------

#: Profundidad máxima de anidamiento permitida (anti-ciclos y anti-abuso).
#: Suficiente para cualquier estructura de estado real y muy por debajo del
#: límite de recursión de CPython (1000): un ciclo auto-referenciado se corta
#: aquí antes de agotar la pila.
_MAX_DEPTH = 64


def ensure_plain(obj: Any, *, _depth: int = 0, _root: str = ".") -> None:
    """Valida que `obj` sea JSON plano ESTRICTO; lanza NotPlainDataError si no.

    Permitido (recursivo): `None | bool | int | float finito | str | list |
    dict[str, ...]`. Por el contrario RECHAZA: tuple, set, bytes, floats no
    finitos (nan/inf/-inf), objetos arbitrarios, claves de dict no-str, y
    cualquier estructura de anidamiento > `_MAX_DEPTH` (64) — esto último
    corta ciclos auto-referenciados y abuso de profundidad.

    El mensaje de error contiene la RUTA al punto exacto del fallo en formato
    punto+corchete: `a.b[0]` significa `b[0]` dentro del dict `a`.

    Parámetros:
    - `obj`: raíz a validar.
    - `_depth`: contador interno de recursión — NO pasar por el usuario.
    - `_root`: nombre simbólico de la raíz para el mensaje de ruta (por
      defecto `"."`); p.ej. `_root="run"` produce rutas `run.x.y`.
    """
    # Guard de profundidad: un ciclo o una estructura demasiado profunda se
    # corta aquí, antes de que la recursión nativa del intérprete estalle.
    if _depth > _MAX_DEPTH:
        raise NotPlainDataError(
            f"profundidad máx ({_MAX_DEPTH}) superada en '{_root}' — posible ciclo"
        )

    # Escalares permitidos. `bool` es subclase de int en Python; lo tratamos
    # por separado solo para claridad, pero ambos son JSON-plano válidos.
    if obj is None or isinstance(obj, (bool, int, str)):
        return

    if isinstance(obj, float):
        if not math.isfinite(obj):
            raise NotPlainDataError(
                f"float no finito ({obj!r}) en '{_root}' — JSON plano no lo admite"
            )
        return

    if isinstance(obj, list):
        for index, item in enumerate(obj):
            ensure_plain(item, _depth=_depth + 1, _root=f"{_root}[{index}]")
        return

    if isinstance(obj, Mapping):
        for key, value in obj.items():
            if not isinstance(key, str):
                raise NotPlainDataError(
                    f"clave de dict no str en '{_root}' "
                    f"(clave {key!r} de tipo {type(key).__name__})"
                )
            ensure_plain(value, _depth=_depth + 1, _root=f"{_root}.{key}")
        return

    # Todo lo demás viola el JSON plano estricto: tuple, set, bytes, objetos,
    # generadores, etc.
    raise NotPlainDataError(
        f"tipo no JSON-plano {type(obj).__name__} en '{_root}'"
    )


# --- Command -----------------------------------------------------------------

@dataclass(frozen=True)
class Command:
    """Un comando plano ida-y-vuelta (§1.2, `{"cmd": ..., ...}`).

    Inmutable (frozen). Campos:
    - `cmd`: str NO vacío, tipo canónico del comando («exec», «move», ...).
    - `args`: Mapping[str, Any] con argumentos adicionales. Las claves DEBEN
      ser str y la clave reservada `"cmd"` está PROHIBIDA aquí (la lleva el
      campo canónico de arriba); violarlo lanza ValueError al construir.

    Invariantes (verificadas en `__post_init__`):
    - `cmd` no vacío (ValueError).
    - `args` es un Mapping (ValueError) y se almacena como dict propio.
    - Todas las claves de `args` son str (TypeError).
    - `"cmd"` no puede aparecer en `args` (ValueError) — así `to_dict` es
      trivialmente seguro y `from_dict(to_dict(c)) == c` sin ambigüedades.

    `to_dict` / `from_dict` son inversas exactas: el "cmd" canónico gana
    siempre y los argumentos nunca lo pisotean.
    """

    cmd: str
    args: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Frozen dataclass: los campos se fijan con object.__setattr__.
        if not isinstance(self.cmd, str):
            raise ValueError(f"Command.cmd debe ser str, no {type(self.cmd).__name__}")
        if not self.cmd:
            raise ValueError("Command.cmd no puede ser la cadena vacía")

        raw = self.args
        if raw is None:
            args: Mapping[str, Any] = {}
        elif isinstance(raw, Mapping):
            args = dict(raw)
        else:
            raise ValueError(
                f"Command.args debe ser Mapping o None, no {type(raw).__name__}"
            )

        if "cmd" in args:
            raise ValueError(
                "Command.args no puede contener la clave reservada 'cmd' "
                "(el comando canónico la lleva: usar Command.cmd)"
            )
        for key in args:
            if not isinstance(key, str):
                raise TypeError(
                    f"Command.args exige claves str, encontrada {key!r} "
                    f"de tipo {type(key).__name__}"
                )
        object.__setattr__(self, "args", args)

    def to_dict(self) -> dict[str, Any]:
        """Serializa a dict plano §1.2: `{"cmd": ..., **args}`.

        Devuelve SIEMPRE un dict nuevo. Como `"cmd"` está prohibido en `args`
        (ver `__post_init__`), el "cmd" canónico manda sin colisiones: el
        operador `**args` jamás puede pisar la clave `"cmd"`.
        """
        return {"cmd": self.cmd, **self.args}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Command":
        """Reconstruye un Command desde un dict plano §1.2.

        Lanza `InvalidCommandError` (no ValueError) ante basura:
        - la entrada no es un Mapping (lista, str, None, ...);
        - falta la clave canónica `"cmd"`;
        - `"cmd"` no es str o es vacío.
        El resto de claves distintas de `"cmd"` se convierten en `args`; las
        invariantes de `args` (claves str, sin `"cmd"`) se re-validan en
        `__post_init__`.
        """
        if not isinstance(d, Mapping):
            raise InvalidCommandError(
                f"Command.from_dict espera Mapping, no {type(d).__name__}"
            )
        if "cmd" not in d:
            raise InvalidCommandError("Command.from_dict: falta la clave 'cmd'")
        cmd = d["cmd"]
        if not isinstance(cmd, str) or not cmd:
            raise InvalidCommandError(
                f"Command.from_dict: 'cmd' debe ser str no vacío, recibido {cmd!r}"
            )
        args = {k: v for k, v in d.items() if k != "cmd"}
        return cls(cmd=cmd, args=args)