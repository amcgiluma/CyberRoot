"""test_validation.py — el validador del DAG rechaza, en negativo, cada regla
de `validation.validate` (S2, criterio de Gwyndolin).

Criterio S2: «el validador rechaza DAG con ciclo y con prereq inexistente
(tests en negativo)». Aquí cubrimos TODAS las reglas con un test por regla,
usando helpers con defaults sanos para no repetir estructura. Un DAG acíclico
con prereqs todos existentes garantiza alcanzabilidad desde las raíces, por lo
que NO hace falta un rechazo separado de «prereq no alcanzable» — el validador
lo deriva (ver `validation._validate_reachability` y su docstring).

Y en positivo: un currículo sano pequeño pasa sin excepción, y las consultas
(`unlocked`, `campaign_pool`, `quests_for_chapter`, `chapter_concepts`) tienen
la semántica documentada en `model.py` — no-transitividad, filtrado por prereqs
dominados y orden determinista por id.

Solo stdlib + pytest; sin `import random`; cero I/O de red.
"""

from __future__ import annotations

import pytest

from core.curriculum.model import Concept, Curriculum, CurriculumError, Quest
from core.curriculum.validation import validate


# ----------------------------------------------------------------------------
# Constructores con defaults sanos (evitan repetir estructura en cada test)
# ----------------------------------------------------------------------------
def _concept(
    concept_id: str = "a",
    family: str = "navegacion",
    chapter: int = 0,
    prerequisites: tuple[str, ...] = (),
    summary_key: str = "concept.a.summary",
) -> Concept:
    """Un Concept válido por defecto; se sobrescribe solo el campo bajo test."""
    return Concept(
        id=concept_id,
        family=family,
        chapter=chapter,
        prerequisites=prerequisites,
        summary_key=summary_key,
    )


def _quest(
    quest_id: str = "story.ch0.q1",
    chapter: int = 0,
    tint: str = "grey",
    requires: tuple[str, ...] = ("a",),
    title_key: str = "story.ch0.q1.title",
    beat_key: str | None = None,
) -> Quest:
    """Un Quest válido por defecto; se sobrescribe solo el campo bajo test."""
    return Quest(
        id=quest_id,
        chapter=chapter,
        tint=tint,
        requires=requires,
        title_key=title_key,
        beat_key=beat_key,
    )


def _curriculum(concepts: tuple[Concept, ...], quests: tuple[Quest, ...]) -> Curriculum:
    """Curriculum ya construido (sin validar); el test decide qué llama a validate."""
    return Curriculum(version=1, concepts=concepts, quests=quests)


def _sano() -> Curriculum:
    """Currículo mínimo VÁLIDO: a→b→c encadenados + una quest del cap. 1."""
    a = _concept("a", chapter=0)
    b = _concept("b", chapter=1, prerequisites=("a",))
    c = _concept("c", chapter=1, prerequisites=("b",))
    q = _quest("story.ch1.q1", chapter=1, tint="blue", requires=("a", "b"))
    return _curriculum((a, b, c), (q,))


# ----------------------------------------------------------------------------
# NEGATIVO — ciclos en el DAG
# ----------------------------------------------------------------------------
def test_ciclo_simple_a_b_rechazado() -> None:
    """Ciclo de longitud 2 (a↔b) debe romperse con mensaje de 'ciclo', porque
    un prereq recíproco hace que ningún concepto sea alcanzable desde la base."""
    a = _concept("a", chapter=0, prerequisites=("b",))
    b = _concept("b", chapter=0, prerequisites=("a",))
    with pytest.raises(CurriculumError, match="ciclo"):
        validate(_curriculum((a, b), ()))


def test_ciclo_de_tres_nodos_rechazado() -> None:
    """Ciclo a→b→c→a: la DFS por color debe reportar el camino legible completo
    «a → b → c → a», no solo un indicio de que algo está mal."""
    a = _concept("a", chapter=0, prerequisites=("b",))
    b = _concept("b", chapter=0, prerequisites=("c",))
    c = _concept("c", chapter=0, prerequisites=("a",))
    with pytest.raises(CurriculumError, match="ciclo"):
        validate(_curriculum((a, b, c), ()))


def test_auto_prereq_rechazado() -> None:
    """Un concepto NO puede ser prereq de sí mismo: instantáneo de detectar,
    independiente de la DFS — es la regla dura más barata del §6.4.1."""
    a = _concept("a", chapter=0, prerequisites=("a",))
    with pytest.raises(CurriculumError, match="sí mismo"):
        validate(_curriculum((a,), ()))


# ----------------------------------------------------------------------------
# NEGATIVO — prereqs inválidos
# ----------------------------------------------------------------------------
def test_prereq_inexistente_rechazado() -> None:
    """Prereq que apunta a un concepto que no está en el catálogo: el DAG debe
    rechazarlo (¿cómo dominas algo que nadie enseña?)."""
    a = _concept("a", chapter=0, prerequisites=("fantasma",))
    with pytest.raises(CurriculumError, match="prereq inexistente"):
        validate(_curriculum((a,), ()))


def test_prereq_de_capitulo_posterior_rechazado() -> None:
    """Regla pedagógica §6.4.1 DURA: un concepto (cap. 1) no puede exigir como
    prereq algo que se enseña MÁS TARDE (cap. 2) — sería imposible de dominar
    en orden."""
    a = _concept("a", chapter=2)
    b = _concept("b", chapter=1, prerequisites=("a",))
    with pytest.raises(CurriculumError, match="posterior a 1"):
        validate(_curriculum((a, b), ()))


# ----------------------------------------------------------------------------
# NEGATIVO — quests
# ----------------------------------------------------------------------------
def test_quest_requires_inexistente_rechazado() -> None:
    """Una quest que pide un concepto fuera del catálogo no puede resolverse."""
    a = _concept("a", chapter=0)
    q = _quest(requires=("a", "fantasma"))
    with pytest.raises(CurriculumError, match="inexistente"):
        validate(_curriculum((a,), (q,)))


def test_quest_requires_enseñado_despues_rechazado() -> None:
    """Quest del cap. 1 que requiere un concepto enseñado en el cap. 2: sería
    irresoluble cuando llega (invariante §6.4.1)."""
    a = _concept("a", chapter=2)
    q = _quest("story.ch1.q1", chapter=1, requires=("a",))
    with pytest.raises(CurriculumError, match="posterior a 1"):
        validate(_curriculum((a,), (q,)))


def test_quest_duplicada_rechazada() -> None:
    """El id de quest ES la clave de historia: duplicado rompería el resolve."""
    a = _concept("a", chapter=0)
    q1 = _quest("story.ch0.q1", requires=("a",))
    q2 = _quest("story.ch0.q1", requires=("a",))
    with pytest.raises(CurriculumError, match="quest duplicada"):
        validate(_curriculum((a,), (q1, q2)))


def test_quest_chapter_fuera_rango_rechazado() -> None:
    """Capítulo 7 no es un capítulo de campaña (CHAPTERS va de 0 a 6)."""
    a = _concept("a", chapter=0)
    for bad in (7, -1):
        q = _quest("story.ch0.q1", chapter=bad, requires=("a",))
        with pytest.raises(CurriculumError, match="capítulo fuera de rango"):
            validate(_curriculum((a,), (q,)))


def test_quest_tint_desconocido_rechazado() -> None:
    """Tinte 'dorado' no está en TINTS (solo blue/red/grey) — sería una quest
    que el render no sabría pintar."""
    a = _concept("a", chapter=0)
    q = _quest(tint="dorado", requires=("a",))
    with pytest.raises(CurriculumError, match="tint desconocido"):
        validate(_curriculum((a,), (q,)))


def test_quest_title_key_vacia_rechazada() -> None:
    """El render resuelve claves de texto: una title_key vacía entrega una quest
    sin título visible."""
    a = _concept("a", chapter=0)
    q = _quest(title_key="   ", requires=("a",))
    with pytest.raises(CurriculumError, match="title_key vacía"):
        validate(_curriculum((a,), (q,)))


def test_quest_id_vacio_rechazado() -> None:
    """Id vacío (espacios) no es una clave de historia usable."""
    a = _concept("a", chapter=0)
    q = _quest(quest_id="   ", requires=("a",))
    with pytest.raises(CurriculumError, match="quest con id vacío"):
        validate(_curriculum((a,), (q,)))


# ----------------------------------------------------------------------------
# NEGATIVO — concepts
# ----------------------------------------------------------------------------
def test_concept_duplicado_rechazado() -> None:
    """Dos conceptos con el mismo id: el índice by_id no tendría qué responder."""
    a1 = _concept("a", chapter=0)
    a2 = _concept("a", chapter=1)
    with pytest.raises(CurriculumError, match="concept duplicado"):
        validate(_curriculum((a1, a2), ()))


def test_familia_desconocida_rechazada() -> None:
    """Una familia fuera de las ocho del catálogo (§6.2, cerradas en Fase 0)."""
    a = _concept("a", family="magia")
    with pytest.raises(CurriculumError, match="familia desconocida"):
        validate(_curriculum((a,), ()))


def test_concept_chapter_fuera_rango_rechazado() -> None:
    """Capítulo fuera de 0..6 (tanto por arriba como por abajo) es no-campaña."""
    for bad in (7, -1):
        a = _concept("a", chapter=bad)
        with pytest.raises(CurriculumError, match="capítulo fuera de rango"):
            validate(_curriculum((a,), ()))


def test_summary_key_vacia_rechazada() -> None:
    """El resumen del concepto viaja como clave: vacío es un hueco de contenido."""
    a = _concept("a", summary_key="")
    with pytest.raises(CurriculumError, match="summary_key vacía"):
        validate(_curriculum((a,), ()))


def test_concept_id_vacio_rechazado() -> None:
    """El id es la dirección del concepto: sin él no hay a quién referirse."""
    a = _concept(concept_id="  ")
    with pytest.raises(CurriculumError, match="concept con id vacío"):
        validate(_curriculum((a,), ()))


# ----------------------------------------------------------------------------
# POSITIVO — currículo sano y consultas
# ----------------------------------------------------------------------------
def test_curriculum_sano_pasa_sin_excepcion() -> None:
    """El currículo mínimo (a→b→c + quest cap. 1) es VÁLIDO: validate no lanza."""
    validate(_sano())


def test_unlocked_no_es_transitivo() -> None:
    """`unlocked` hace UN paso (prereqs ⊆ mastered), NO propaga por la cadena:
    tener 'a' desbloquea 'a' y 'b' (prereq directo) pero NO 'c' (hijo de 'b')."""
    cur = _sano()
    unlocked = cur.unlocked({"a"})
    assert "a" in unlocked
    assert "b" in unlocked          # prereq ⊆ mastered
    assert "c" not in unlocked      # NO transitivo: 'b' aún no dominado


def test_campaign_pool_filtra_por_prereqs_y_ordena_por_id() -> None:
    """`campaign_pool(1, {a})` incluye los dominados por {a} (no 'c', que pide
    'b') y devuelve el pool ordenado por id — determinista sin RNG."""
    a = _concept("a", chapter=0)
    e = _concept("e", chapter=0)
    b = _concept("b", chapter=1, prerequisites=("a",))
    d = _concept("d", chapter=1, prerequisites=("a",))
    c = _concept("c", chapter=1, prerequisites=("b",))
    cur = _curriculum((a, b, c, d, e), ())

    pool = [c.id for c in cur.campaign_pool(1, {"a"})]
    # b alcanza (prereq 'a' dominado), c no ('b' fuera); orden alfabético.
    assert pool == ["a", "b", "d", "e"]


def test_campaign_pool_respeta_capitulo_limite() -> None:
    """Nada del capítulo 2 entra al pool del capítulo 1, aunque esté dominado."""
    a = _concept("a", chapter=0)
    late = _concept("late", chapter=2, prerequisites=("a",))
    cur = _curriculum((a, late), ())
    assert [c.id for c in cur.campaign_pool(1, {"a"})] == ["a"]


def test_quests_for_chapter_filtra_y_ordena_por_id() -> None:
    """`quests_for_chapter(1)` devuelve SOLO las del capítulo 1, por id."""
    a = _concept("a", chapter=0)
    q0 = _quest("z", chapter=0, requires=("a",))
    q1 = _quest("e1", chapter=1, requires=("a",))
    q2 = _quest("e2", chapter=1, requires=("a",))
    cur = _curriculum((a,), (q0, q1, q2))
    assert [q.id for q in cur.quests_for_chapter(1)] == ["e1", "e2"]


def test_chapter_concepts_filtra_y_ordena_por_id() -> None:
    """`chapter_concepts(n)` devuelve los de ENSEÑANZA de ese capítulo, por id."""
    a = _concept("a", chapter=0)
    b = _concept("b", chapter=1, prerequisites=("a",))
    c = _concept("c", chapter=1, prerequisites=("b",))
    cur = _curriculum((a, b, c), ())
    assert [c.id for c in cur.chapter_concepts(1)] == ["b", "c"]
    assert [c.id for c in cur.chapter_concepts(0)] == ["a"]