"""generator — generador procedural determinista del cap. 0 (v0).

Módulo `src/core/generator/` de CyberRoot. ENTREGADA DE LA TAREA O2 del plan
28/08 (Gwyndolin): la primera API determinista del generador. Contrato §4.5,
dueño Ornstein.

Qué hace:
- `generate(seed, chapter=0, *, variant="canonical")` → `Incursion`: UNA sala
  del cap. 0 con la piel EXACTA del capítulo (oficina-vecinal-muelle-norte,
  ventana de las 11:04, CANDELAS proveedor nº 47) y el encargo del cap. 1
  (`story.ch1.e1`). Misma seed ⇒ misma Incursion en cualquier proceso.
- No depende de `curriculum.json` en v0: usa los conceptos ya activados
  (`ls/cd/cat/cp`).
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
en `scaffold`.options (a/b/c) y sigue a la espera de la decisión de Gwyn
(🧭2, plan 28/08 §4) — NO la decidimos aquí.
"""

from __future__ import annotations

from core.generator.errors import GeneratorError, UnsolvableRoomError
from core.generator.generator import generate, validate_incursion
from core.generator.model import (
    CanonSolution,
    CanonStep,
    Contract,
    Incursion,
    Objective,
    Room,
    RunScaffold,
)

__version__ = "0.1.0"

__all__ = [
    "generate",
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