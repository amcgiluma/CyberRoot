"""engine — el motor roguelite (ARCHITECTURE §2.5, DESIGN §4.1/§7).

v0 (O2, 30/08) abre el módulo con su primer fichero: `postmortem.py` (la
pieza que el Hub muestra SIEMPRE primero, §4.7). El motor completo (mapa de
nodos, detección, economía) llega en siguientes turnos de Ornstein; aquí va
lo que los datos ya permiten hoy: el informe post-mortem del Auditor leyendo
el HISTORIAL REAL de la sesión.

Reglas duras heredadas de ARCHITECTURE:
- core NO importa pyxel (vigilado por `tests/architecture`).
- frontiera: entra como dict de sesión (`Shell.to_dict()`), sale Event/dict
  plano; sin estado global mutable.
- RNG seedeada por el generador, jamás `random` global.
- Los textos visibles del post-mortem viajan como CLAVES, no cadenas
  hardcodeadas (el render las resuelve contra `data/`).
"""

from __future__ import annotations

from core.engine.postmortem import (
    DEFAULT_NOISE_BUDGET,
    LINE_KEY_CIEGA,
    LINE_KEY_CORTE,
    LINE_KEY_CRUCE,
    LINE_KEY_LECTURA,
    LINE_KEY_PICO,
    build_postmortem,
)
from core.engine.session import (
    EncargoSession,
    SUPPORTED_CHAPTERS,
    abrir_encargo,
    cerrar_encargo,
    listar_encargos,
    rechazo_accionable,
)

__version__ = "0.2.0"

__all__ = [
    "build_postmortem",
    "DEFAULT_NOISE_BUDGET",
    "LINE_KEY_CIEGA",
    "LINE_KEY_CORTE",
    "LINE_KEY_CRUCE",
    "LINE_KEY_LECTURA",
    "LINE_KEY_PICO",
    "EncargoSession",
    "SUPPORTED_CHAPTERS",
    "abrir_encargo",
    "cerrar_encargo",
    "listar_encargos",
    "rechazo_accionable",
    "__version__",
]