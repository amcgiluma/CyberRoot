"""O1 (29/08, Ornstein): el generator consume `curriculum.json` real.

La sala ya NO saca ni la quest ni el concept_pool de constantes hardcodeadas:
- `concept_pool` = los ids de los conceptos que el capítulo enseña
  (`Curriculum.chapter_concepts(0)` → `c.ls/cd/cat/cp`).
- `objective.story_key` = la quest del pool del capítulo
  (`quests_for_chapter(0)` → `story.ch0.ventana`), con su `requires` cubierto
  por el pool (§6.4.1).
- La sesión que produce la Incursión nace en `initial_cwd` del DEFAULT del
  scaffold (opción B → "/"), NO en el default de la Shell (🧭2).
"""
from __future__ import annotations

import pytest

from core.curriculum import load_curriculum
from core.generator import generate, new_session

CUR = load_curriculum()
SEEDS = (0, 7, 42, 99)


def _expected_pool() -> tuple[str, ...]:
    return tuple(c.id for c in CUR.chapter_concepts(0))


def test_concept_pool_viene_del_curriculum() -> None:
    """El pool de la sala es EXACTAMENTE lo que el cap. 0 enseña en el JSON."""
    expected = _expected_pool()
    assert expected == ("c.cat", "c.cd", "c.cp", "c.ls")
    for seed in SEEDS:
        for variant in ("canonical", "practice"):
            inc = generate(seed, 0, variant=variant)
            assert inc.room.concept_pool == expected, f"seed={seed} {variant}"


def test_quest_viene_del_pool_del_capitulo() -> None:
    """objective.story_key es la quest del cap. 0 del JSON (story.ch0.ventana)."""
    q = CUR.quests_for_chapter(0)
    assert q and q[0].id == "story.ch0.ventana"
    for seed in SEEDS:
        inc = generate(seed, 0)
        assert inc.room.objective.story_key == q[0].id


def test_quest_requires_cubiertos_por_pool() -> None:
    """Invariante pedagógico §6.4.1: la quest contratada usa solo conceptos
    que el cap. 0 enseña (nadie recibe un reto sin sus herramientas)."""
    q = CUR.quests_for_chapter(0)[0]
    assert set(q.requires) <= set(_expected_pool())


def test_generate_acepta_curriculum_inyectado() -> None:
    """El harness puede cargar el currículo UNA vez y reusarlo en N seeds."""
    a = generate(7, 0, curriculum=CUR).to_dict()
    b = generate(7, 0, curriculum=CUR).to_dict()
    assert a == b
    # Inyectado e implícito producen la misma Incursion (misma fuente de datos).
    assert b == generate(7, 0).to_dict()


def test_generate_sin_quests_del_capitulo_falla_con_motivo() -> None:
    """Si el capítulo no ofrece ninguna quest, generar es un ERROR accionable
    (la sala no tendría encargo — viola §6.4.1)."""
    from core.generator.errors import GeneratorError

    class SinQuests:
        """Curriculum mínimo que acepta la firma pero no tiene quests del cap."""

        def chapter_concepts(self, chapter: int):
            return CUR.chapter_concepts(chapter)

        def quests_for_chapter(self, chapter: int):
            return ()

    with pytest.raises(GeneratorError):
        generate(7, 0, curriculum=SinQuests())  # type: ignore[arg-type]


def test_sesion_nace_en_cwd_del_scaffold_default() -> None:
    """🧭2 opción B como comportamiento: la sesión montada arranca en
    `initial_cwd` del DEFAULT del scaffold (opción B → "/"), no en el default
    de la Shell (que aquí coinciden, pero la fuente es el scaffold)."""
    for seed in SEEDS:
        inc = generate(seed, 0, variant="canonical")
        assert inc.scaffold.default == "option_b"
        assert inc.scaffold.initial_cwd() == "/"
        s = new_session(inc)
        assert s.cwd == inc.scaffold.initial_cwd() == "/"


def test_nueva_sesion_no_muta_el_fs_de_la_incursion() -> None:
    """new_session trabaja sobre COPIA: la Incursión conserva SU FS intacto."""
    inc = generate(7, 0)
    before = inc.room.fs.to_dict()
    s = new_session(inc)
    s.execute("cp /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt /usb/")
    assert inc.room.fs.to_dict() == before  # la Incursión intacta