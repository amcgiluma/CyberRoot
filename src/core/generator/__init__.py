"""generator — generador procedural determinista (v0.2).

Módulo `src/core/generator/` de CyberRoot. O1/O2 del plan 29/08 (Gwyndolin):
el generator consume `curriculum.json` real. Contrato §4.5, dueño Ornstein.

Qué hace:
- `generate(seed, chapter=0, *, variant="canonical", curriculum=None)` →
  `Incursion`: UNA sala del cap. 0 con la piel EXACTA del capítulo
  (oficina-vecinal-muelle-norte, ventana de las 11:04, CANDELAS proveedor
  nº 47). Su `concept_pool` y su quest (`objective.story_key`) vienen del
  curriculum (cap. 0 → `c.ls/cd/cat/cp` y `story.ch0.ventana`).
  Misma seed ⇒ misma Incursion en cualquier proceso.
- `new_session(incursion)` → la sesión que PRODUCE la Incursión: copia del FS,
  cwd nacido del scaffold default (opción B → "/"), set de comandos del cap. 0.
- VALIDACIÓN CANÓNICA OBLIGATORIA (§6.4.4): toda sala generada se valida
  contra su solución canónica; una sala irresoluble lanza
  `UnsolvableRoomError` (nunca se entrega).

Reglas duras:
- DETERMINISMO: prohibido `import random`; toda variación nace de la seed de
  run vía `Rng.fork` (decoys/mtimes/ids).
- JSON-plano estricto en el contrato: `Incursion.to_dict()` atraviesa
  `ensure_plain` sin excepción.
- Sin estado global mutable; ida-y-vuelta exacta de los modelos.

El andamiaje de la run 0 (cwd inicial/rutas del dossier) se expone como DATOS
en `scaffold`.options (a/b/c) con `default="option_b"` (🧭2): **opción B
materializada** — `new_session` arranca en `initial_cwd` del default.
"""

from __future__ import annotations

from core.generator.errors import GeneratorError, UnsolvableRoomError
from core.generator.generator import generate, new_session, validate_incursion
from core.generator.model import (
    CanonSolution,
    CanonStep,
    Contract,
    Incursion,
    Objective,
    Room,
    RunScaffold,
)

__version__ = "0.2.0"

__all__ = [
    "generate",
    "new_session",
    "validate_incursion",
    "Incursion",
    "Room",
    "CanonSolution",
    "CanonStep",
    "Objective",
    "Contract",
    "RunScaffold",
    "GeneratorError",
    "UnsolvableRoomError",
    "__version__",
]