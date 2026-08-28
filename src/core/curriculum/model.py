"""model.py — objetos de valor del currículo (ARCHITECTURE §2.3, DESIGN §6.2/§6.4).

`Concept` y `Quest` son dataclasses FROZEN: conocimiento puro sin estado
mutable global (§3). El currículo NO conoce runs ni salas: responde «qué está
desbloqueado» y «qué pool corresponde a este capítulo» — el muestreo con RNG
es del GENERADOR (§6.4.2), nunca de aquí.

Todo texto visible viaja como CLAVE (`summary_key`, `title_key`, `beat_key`):
core nunca hardcodea prosa (§3 Convenciones); el render las resuelve contra
`data/`.

Errores: `CurriculumError` (aquí, porque loader y validador la comparten).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from core.common.errors import CyberRootError

#: Familias del catálogo (DESIGN §6.2 — las ocho, cerradas en Fase 0).
FAMILIES: frozenset[str] = frozenset(
    {
        "navegacion",
        "permisos",
        "texto",
        "procesos",
        "red",
        "auditoria",
        "escalada",
        "hallazgo",
    }
)

#: Tinte kármico de un encargo (DESIGN §3.3: azul, rojo o gris — visible en la
#: descripción del trabajo, nunca un icono moral).
TINTS: frozenset[str] = frozenset({"blue", "red", "grey"})

#: Versión de formato que carga este módulo (saves/datos versionados, §1.5).
SCHEMA_VERSION = 1

#: Capítulos de la campaña (DESIGN §6.1).
CHAPTERS: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6)


class CurriculumError(CyberRootError):
    """Datos de currículo inválidos (estructura, prereqs, ciclo, versión)."""


@dataclass(frozen=True)
class Concept:
    """Un concepto enseñable del DAG (~60 boons, §4.4/§6.2).

    - `chapter`: capítulo de ENSEÑANZA (se introduce); los siguientes lo
      mantienen vivo como mantenimiento (§6.0.4) — eso se deriva, no se
      almacena.
    - `prerequisites`: ids de conceptos que hay que dominar antes. El DAG se
      valida en `validation.py` (sin ciclos, referencias existentes).
    """

    id: str
    family: str
    chapter: int
    prerequisites: tuple[str, ...]
    summary_key: str


@dataclass(frozen=True)
class Quest:
    """Un encargo de la mesa del Hub (nodo-dato del capítulo, §2.6.1).

    El `id` ES la clave de historia (`story.ch1.e1`): los textos vive en
    `backlog/historia/` y entran a `data/` como claves. `requires` son los
    conceptos que la solución canónica usa — el invariante pedagógico §6.4.1
    exige que estén todos enseñados en capítulos ≤ `chapter`.
    """

    id: str
    chapter: int
    tint: str
    requires: tuple[str, ...]
    title_key: str
    beat_key: str | None = None


@dataclass(frozen=True)
class Curriculum:
    """El DAG único de verdad (§6.4.1) + los encargos como nodos-dato.

    Índices derivados se reconstruyen por llamada (N≈60: coste trivial) para
    mantener la dataclass frozen sin duplicar estado.
    """

    version: int
    concepts: tuple[Concept, ...]
    quests: tuple[Quest, ...]

    # ---- consultas (API de consumo: generator hoy, engine/progression luego) --

    def concept(self, concept_id: str) -> Concept | None:
        """El concepto por id, o None."""
        for c in self.concepts:
            if c.id == concept_id:
                return c
        return None

    def quest(self, quest_id: str) -> Quest | None:
        """El encargo por id (clave de historia), o None."""
        for q in self.quests:
            if q.id == quest_id:
                return q
        return None

    def quests_for_chapter(self, chapter: int) -> tuple[Quest, ...]:
        """Encargos del capítulo, ordenados por id (determinismo §3)."""
        return tuple(sorted((q for q in self.quests if q.chapter == chapter), key=lambda q: q.id))

    def chapter_concepts(self, chapter: int) -> tuple[Concept, ...]:
        """Conceptos cuya ENSEÑANZA es ese capítulo, ordenados por id."""
        return tuple(
            sorted((c for c in self.concepts if c.chapter == chapter), key=lambda c: c.id)
        )

    def unlocked(self, mastered: Iterable[str]) -> frozenset[str]:
        """Conceptos DESBLOQUEADOS dado lo dominado (§6.4.1: el generador
        comprueba el pool desbloqueado del jugador, NUNCA la etiqueta del
        capítulo — nadie recibe un reto sin sus herramientas).

        Un concepto está desbloqueado si todos sus prereqs ⊆ `mastered`.
        NO es transitivo a propósito: el generador itera (`unlocked` sobre
        `mastered ∪ anteriores`) si quiere propagar; aquí solo el paso puro.
        """
        have = frozenset(mastered)
        return frozenset(c.id for c in self.concepts if have.issuperset(c.prerequisites))

    def campaign_pool(
        self, chapter: int, mastered: Iterable[str]
    ) -> tuple[Concept, ...]:
        """Pool de práctica para el capítulo (insumo del muestreo §6.4.2):
        conceptos enseñados en capítulos ≤ `chapter` Y desbloqueados por
        `mastered`. Ordenado por id — determinista sin RNG (la semilla la
        aporta el generador al ELEGIR del pool).
        """
        have = frozenset(mastered)
        return tuple(
            sorted(
                (
                    c
                    for c in self.concepts
                    if c.chapter <= chapter and have.issuperset(c.prerequisites)
                ),
                key=lambda c: c.id,
            )
        )
