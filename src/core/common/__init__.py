"""core.common — cimientos del core (ARCHITECTURE §2.1).

Exporta la API pública del paquete. Solo stdlib; este paquete no importa
nada del resto del core.
"""

from core.common.rng import Rng
from core.common.events import Event, EventBus, EventTypes
from core.common.types import Command, SeedLike, TextKey, ensure_plain
from core.common.errors import (
    CyberRootError,
    InvalidCommandError,
    NotPlainDataError,
)

__all__ = [
    "Rng",
    "Event",
    "EventBus",
    "EventTypes",
    "Command",
    "SeedLike",
    "TextKey",
    "ensure_plain",
    "CyberRootError",
    "InvalidCommandError",
    "NotPlainDataError",
]
