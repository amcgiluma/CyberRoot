"""loader.py — carga de `src/data/curriculum.json` (S2, ARCHITECTURE §2.3).

Contrato con el fichero de datos: `{"version": 1, "concepts": [...],
"quests": [...]}` con el esquema documentado en el README del módulo.
Cualquier desviación → `CurriculumError` (estructura) o `NotPlainDataError`
(via `ensure_plain`: el JSON debe ser plano estricto — claves str, sin
tuplas, sin NaN).

Sin I/O de red, sin globals: `load_curriculum()` lee el fichero por llamada.
El muestreo con RNG nunca vive aquí (eso es del generador, §6.4.2).
"""

from __future__ import annotations

import json
from pathlib import Path

from core.common.types import ensure_plain
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

#: Ruta canónica de los datos (desde la raíz del repo).
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "curriculum.json"


def load_curriculum(path: Path | str | None = None) -> Curriculum:
    """Lee y valida el currículo; devuelve el objeto `Curriculum` sano.

    `path=None` usa `src/data/curriculum.json`. Levanta `CurriculumError`
    con mensaje accionable si el fichero falta, no es JSON, no es plano o
    viola el esquema/validación.
    """
    p = Path(path) if path is not None else DATA_PATH
    try:
        raw_text = p.read_text(encoding="utf-8")
    except OSError as e:
        raise CurriculumError(f"no se pudo leer {p}: {e}") from e
    try:
        doc = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise CurriculumError(f"{p} no es JSON válido: {e}") from e
    return curriculum_from_dict(doc)


def curriculum_from_dict(doc: object) -> Curriculum:
    """dict JSON → `Curriculum` validado (punto de entrada para tests)."""
    if not isinstance(doc, dict):
        raise CurriculumError(
            f"curriculum debe ser un objeto JSON, no {type(doc).__name__}"
        )
    try:
        ensure_plain(doc)
    except Exception as e:  # NotPlainDataError u otra variante de common
        raise CurriculumError(f"curriculum no es JSON plano estricto: {e}") from e

    version = doc.get("version")
    if version != SCHEMA_VERSION:
        raise CurriculumError(
            f"version de curriculum.json no soportada: {version!r} "
            f"(esperada {SCHEMA_VERSION})"
        )
    concepts_raw = doc.get("concepts")
    quests_raw = doc.get("quests")
    if not isinstance(concepts_raw, list) or not concepts_raw:
        raise CurriculumError("concepts debe ser una lista no vacía")
    if not isinstance(quests_raw, list):
        raise CurriculumError("quests debe ser una lista (puede estar vacía)")

    concepts = tuple(_concept_from_dict(d, i) for i, d in enumerate(concepts_raw))
    quests = tuple(_quest_from_dict(d, i) for i, d in enumerate(quests_raw))
    cur = Curriculum(version=SCHEMA_VERSION, concepts=concepts, quests=quests)
    validate(cur)
    return cur


def _concept_from_dict(d: object, index: int) -> Concept:
    if not isinstance(d, dict):
        raise CurriculumError(f"concepts[{index}] debe ser un objeto")
    try:
        cid = str(d["id"])
        family = str(d["family"])
        chapter = int(d["chapter"])
        prereqs_raw = d.get("prerequisites", [])
        summary_key = str(d["summary_key"])
    except KeyError as e:
        raise CurriculumError(f"concepts[{index}]: falta el campo {e}") from e
    except (TypeError, ValueError) as e:
        raise CurriculumError(f"concepts[{index}]: tipos inválidos ({e})") from e
    if not isinstance(prereqs_raw, list) or any(
        not isinstance(x, str) for x in prereqs_raw
    ):
        raise CurriculumError(
            f"concepts[{index}]: prerequisites debe ser una lista de strings"
        )
    if family not in FAMILIES:
        raise CurriculumError(
            f"concepts[{index}] ({cid!r}): familia desconocida {family!r} "
            f"(válidas: {sorted(FAMILIES)})"
        )
    if chapter not in CHAPTERS:
        raise CurriculumError(
            f"concepts[{index}] ({cid!r}): capítulo fuera de rango {chapter}"
        )
    return Concept(
        id=cid,
        family=family,
        chapter=chapter,
        prerequisites=tuple(prereqs_raw),
        summary_key=summary_key,
    )


def _quest_from_dict(d: object, index: int) -> Quest:
    if not isinstance(d, dict):
        raise CurriculumError(f"quests[{index}] debe ser un objeto")
    try:
        qid = str(d["id"])
        chapter = int(d["chapter"])
        tint = str(d["tint"])
        requires_raw = d.get("requires", [])
        title_key = str(d["title_key"])
    except KeyError as e:
        raise CurriculumError(f"quests[{index}]: falta el campo {e}") from e
    except (TypeError, ValueError) as e:
        raise CurriculumError(f"quests[{index}]: tipos inválidos ({e})") from e
    beat_key_raw = d.get("beat_key")
    if beat_key_raw is not None and not isinstance(beat_key_raw, str):
        raise CurriculumError(f"quests[{index}]: beat_key debe ser string o null")
    if not isinstance(requires_raw, list) or any(
        not isinstance(x, str) for x in requires_raw
    ):
        raise CurriculumError(
            f"quests[{index}]: requires debe ser una lista de strings"
        )
    if tint not in TINTS:
        raise CurriculumError(
            f"quests[{index}] ({qid!r}): tint desconocido {tint!r} "
            f"(válidos: {sorted(TINTS)})"
        )
    return Quest(
        id=qid,
        chapter=chapter,
        tint=tint,
        requires=tuple(requires_raw),
        title_key=title_key,
        beat_key=beat_key_raw,
    )
