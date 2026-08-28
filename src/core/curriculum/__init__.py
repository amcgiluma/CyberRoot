"""core.curriculum — el DAG único de verdad (ARCHITECTURE §2.3, dueño Smough).

Carga `src/data/curriculum.json` y responde:
- ¿qué conceptos tiene DESBLOQUEADOS este jugador? (`Curriculum.unlocked`)
- ¿qué pool de práctica corresponde a este capítulo? (`Curriculum.campaign_pool`,
  insumo del muestreo §6.4.2 — la ELECCIÓN con RNG es del generador)

No conoce runs ni salas: conocimiento puro. Un solo DAG alimenta currículo y
generador (DESIGN §6.4.1). API pública estable para el consumo de Ornstein
(generator) — contrato anunciado en la PR #5.
"""

from core.curriculum.loader import (
    DATA_PATH,
    curriculum_from_dict,
    load_curriculum,
)
from core.curriculum.model import (
    CHAPTERS,
    FAMILIES,
    SCHEMA_VERSION,
    TINTS,
    Concept,
    Curriculum,
    CurriculumError,
    Quest,
)
from core.curriculum.validation import validate

__all__ = [
    "CHAPTERS",
    "DATA_PATH",
    "FAMILIES",
    "SCHEMA_VERSION",
    "TINTS",
    "Concept",
    "Curriculum",
    "CurriculumError",
    "Quest",
    "curriculum_from_dict",
    "load_curriculum",
    "validate",
]
