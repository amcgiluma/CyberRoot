"""test_loader.py — `load_curriculum` / `curriculum_from_dict` (S2).

Doble cara:
1. Sobre el fichero REAL `src/data/curriculum.json`: carga sin excepción, y
   verifica los contratos con el generador/sandbox y la invariante pedagógica
   §6.4.1 sobre datos de producción (no sobre juguetes de test).
2. `curriculum_from_dict` EN NEGATIVO: cada desviación estructural del esquema
   (versión, tipos, campos faltantes, familia/tint desconocidos, JSON no plano,
   fichero roto o inexistente) debe convertirse en `CurriculumError` con mensaje
   accionable — nunca una `NotPlainDataError` cruda ni un `KeyError` al usuario.

Solo stdlib + pytest; sin `import random`; cero I/O de red (el fichero real es
local al repo y se lee por ruta de módulo).
"""

from __future__ import annotations

import json

import pytest

from core.curriculum.loader import curriculum_from_dict, load_curriculum
from core.curriculum.model import CurriculumError, FAMILIES, TINTS


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _concept_d(
    concept_id: str,
    chapter: int,
    prerequisites: list[str],
    family: str = "navegacion",
) -> dict:
    """Un dict de concepto válido del esquema JSON (para tocar tests negativos)."""
    return {
        "id": concept_id,
        "family": family,
        "chapter": chapter,
        "prerequisites": prerequisites,
        "summary_key": f"concept.{concept_id}.summary",
    }


def _quest_d(quest_id: str, chapter: int, requires: list[str], tint: str = "grey") -> dict:
    """Un dict de quest válido del esquema JSON."""
    return {
        "id": quest_id,
        "chapter": chapter,
        "tint": tint,
        "requires": requires,
        "title_key": f"{quest_id}.title",
        "beat_key": f"{quest_id}.beat",
    }


def _doc() -> dict:
    """Documento JSON-plano VÁLIDO y pequeño: a→b + una quest del cap. 0."""
    return {
        "version": 1,
        "concepts": [
            _concept_d("a", 0, []),
            _concept_d("b", 1, ["a"]),
        ],
        "quests": [_quest_d("story.ch0.q1", 0, ["a"])],
    }


# ----------------------------------------------------------------------------
# Sobre el fichero REAL — contratos con el generador/sandbox
# ----------------------------------------------------------------------------
def test_load_curriculum_carga_sin_excepcion() -> None:
    """El fichero real de producción se carga y valida sin lanzar nada."""
    cur = load_curriculum()
    assert cur is not None
    assert cur.version == 1


def test_load_curriculum_21_conceptos_16_quests() -> None:
    """El catálogo real: 21 conceptos y 16 encargos (S2 01/09 añade cap. 3).

    Conteo del 01/09: 16 (31/08: caps. 0–3) + c.sudo (escalada, cap. 3) + la
    familia conteo c.head/c.tail/c.sort/c.uniq (texto, cap. 6, barrera hacia
    el Faro). Ornstein/generator consumen este conteo vía datos reales; el
    generator de O1 EXIGE al menos una quest del cap. 3 con `c.sudo`
    (story.ch3.e4 y e5 la llevan desde 01/09).
    """
    cur = load_curriculum()
    assert len(cur.concepts) == 21
    assert len(cur.quests) == 16


def test_capitulo6_conteo_enseñado() -> None:
    """La familia conteo se ENSEÑA en el cap. 6 (barrera técnica hacia el
    Faro): c.head/c.tail/c.sort/c.uniq, todos a chapter 6 — prereqs vivos."""
    cur = load_curriculum()
    ids = {c.id for c in cur.chapter_concepts(6)}
    assert {"c.head", "c.tail", "c.sort", "c.uniq"} <= ids


def test_capitulo0_tiene_exactamente_ls_cd_cat_cp() -> None:
    """Contrato con el sandbox/generator: los 4 conceptos del cap. 0 son
    EXACTAMENTE {c.ls, c.cd, c.cat, c.cp} — nada más, nada menos."""
    cur = load_curriculum()
    assert {c.id for c in cur.chapter_concepts(0)} == {"c.ls", "c.cd", "c.cat", "c.cp"}


def test_story_ch0_ventana_es_grey_y_requiere_los_cuatro() -> None:
    """La quest del cap. 0 es la puerta de entrada (grey) y exige los 4 conceptos
    del cap. 0 — coherente con el pool de práctica que entrega el generador."""
    cur = load_curriculum()
    q = cur.quest("story.ch0.ventana")
    assert q is not None
    assert q.chapter == 0
    assert q.tint == "grey"
    assert sorted(q.requires) == ["c.cat", "c.cd", "c.cp", "c.ls"]


def test_las_cinco_quests_del_cap1_tienen_tints_esperados_por_id() -> None:
    """Las 5 quests del cap. 1 (story.ch1.e1..e5) tienen, POR ID, los tints
    [blue, blue, grey, red, grey] — contrato de diseño §3.3 sobre datos reales."""
    cur = load_curriculum()
    quests = cur.quests_for_chapter(1)
    assert [q.id for q in quests] == [
        "story.ch1.e1",
        "story.ch1.e2",
        "story.ch1.e3",
        "story.ch1.e4",
        "story.ch1.e5",
    ]
    assert [q.tint for q in quests] == ["blue", "blue", "grey", "red", "grey"]


def test_las_cinco_quests_del_cap2_tints_y_requires_segun_manus() -> None:
    """S2 (30/08): las 5 quests del cap. 2 siguen a Manus (02-facturas.md).

    Tints E1/E2 blue, E3 grey, E4 red, E5 de cierre grey; `requires` ⊆
    conceptos del cap. 2 (grep/wc/pipe) + básicos del cap. 0 (cp en e5).
    """
    cur = load_curriculum()
    quests = cur.quests_for_chapter(2)
    assert [q.id for q in quests] == [
        "story.ch2.e1",
        "story.ch2.e2",
        "story.ch2.e3",
        "story.ch2.e4",
        "story.ch2.e5",
    ]
    assert [q.tint for q in quests] == ["blue", "blue", "grey", "red", "grey"]
    # Cada quest usa SOLO conceptos enseñados en capítulos <= el suyo (invariante
    # del validador, verificado además en negativo por test_validation).
    concept_chapter = {c.id: c.chapter for c in cur.concepts}
    for q in quests:
        assert all(concept_chapter[r] <= q.chapter for r in q.requires)
    # La sinergia c.pipe es la primera de texto y une grep+wc.
    pipe = cur.concept("c.pipe")
    assert pipe is not None and sorted(pipe.prerequisites) == ["c.grep", "c.wc"]


def test_las_cinco_quests_del_cap3_tints_y_requires_segun_manus() -> None:
    """S2 (31/08): las 5 quests del cap. 3 «Bombas» siguen a Manus.

    El cap. 3 abre la familia procesos con c.ps/c.env (cap. 3). Tints E1 blue,
    E2 grey, E3 red, E4 red, E5 de cierre grey; `requires` ⊆ conceptos del
    cap. 3 (ps/env) + básicos del cap. 0 (ls como prereq de ps).
    """
    cur = load_curriculum()
    quests = cur.quests_for_chapter(3)
    assert [q.id for q in quests] == [
        "story.ch3.e1",
        "story.ch3.e2",
        "story.ch3.e3",
        "story.ch3.e4",
        "story.ch3.e5",
    ]
    assert [q.tint for q in quests] == ["blue", "grey", "red", "red", "grey"]
    # Cada quest usa SOLO conceptos enseñados en capítulos <= el suyo (invariante
    # del validador, verificado además en negativo por test_validation).
    concept_chapter = {c.id: c.chapter for c in cur.concepts}
    for q in quests:
        assert all(concept_chapter[r] <= q.chapter for r in q.requires)
    # La familia procesos la abren exactamente c.ps (prereq c.ls) y c.env
    # (prereq c.ps) en el cap. 3.
    ps = cur.concept("c.ps")
    env = cur.concept("c.env")
    assert ps is not None and ps.family == "procesos" and ps.chapter == 3
    assert env is not None and env.family == "procesos" and env.chapter == 3
    assert sorted(ps.prerequisites) == ["c.ls"]
    assert sorted(env.prerequisites) == ["c.ps"]


def test_ningun_concepto_tiene_prereq_de_capitulo_posterior() -> None:
    """Invariante pedagógica §6.4.1 sobre los datos reales: todo concepto se
    enseña en el mismo capítulo o después que sus prereqs."""
    cur = load_curriculum()
    by_id = {c.id: c for c in cur.concepts}
    for c in cur.concepts:
        for p in c.prerequisites:
            assert by_id[p].chapter <= c.chapter


def test_campaign_pool_cap1_mastered_cap0_devuelve_7_conceptos() -> None:
    """Con los 4 conceptos del cap. 0 dominados, el pool del cap. 1 son los 4
    del cap. 0 + c.ls-la, c.find y c.man (7 en total) — las cadenas que necesitan
    permisos/fechas todavía NO están abiertas."""
    cur = load_curriculum()
    mastered = {"c.ls", "c.cd", "c.cat", "c.cp"}
    pool = {c.id for c in cur.campaign_pool(1, mastered)}
    assert pool == {"c.ls", "c.cd", "c.cat", "c.cp", "c.ls-la", "c.find", "c.man"}
    assert len(pool) == 7


def test_curriculum_from_dict_acepta_el_fichero_real() -> None:
    """El dict del fichero real pasa `curriculum_from_dict` (no solo la ruta)."""
    cur = load_curriculum()
    restored = curriculum_from_dict(
        {
            "version": cur.version,
            "concepts": [
                {"id": c.id, "family": c.family, "chapter": c.chapter,
                 "prerequisites": list(c.prerequisites),
                 "summary_key": c.summary_key}
                for c in cur.concepts
            ],
            "quests": [
                {"id": q.id, "chapter": q.chapter, "tint": q.tint,
                 "requires": list(q.requires), "title_key": q.title_key,
                 "beat_key": q.beat_key}
                for q in cur.quests
            ],
        }
    )
    assert [c.id for c in restored.concepts] == [c.id for c in cur.concepts]
    assert [q.id for q in restored.quests] == [q.id for q in cur.quests]


# ----------------------------------------------------------------------------
# NEGATIVO — curriculum_from_dict (esquema)
# ----------------------------------------------------------------------------
def test_doc_no_dict_rechazado() -> None:
    """La raíz debe ser un objeto JSON; un str no lo es."""
    with pytest.raises(CurriculumError, match="objeto JSON"):
        curriculum_from_dict("hola")  # type: ignore[arg-type]


def test_version_ausente_rechazada() -> None:
    """Sin `version` el loader no sabe qué esquema aplicar."""
    d = _doc()
    del d["version"]
    with pytest.raises(CurriculumError, match="version"):
        curriculum_from_dict(d)


def test_version_no_soportada_rechazada() -> None:
    """`version` distinta de 1 (p.ej. 2) es un formato futuro no entendido."""
    d = _doc()
    d["version"] = 2
    with pytest.raises(CurriculumError, match="version de curriculum.json"):
        curriculum_from_dict(d)


def test_concepts_vacio_rechazado() -> None:
    """Un catálogo sin conceptos no es un currículo (no hay nada que enseñar)."""
    d = _doc()
    d["concepts"] = []
    with pytest.raises(CurriculumError, match="concepts debe ser una lista no vacía"):
        curriculum_from_dict(d)


def test_concepts_no_lista_rechazado() -> None:
    """`concepts` no-lista (p.ej. un str) rompe el esquema."""
    d = _doc()
    d["concepts"] = "no soy lista"
    with pytest.raises(CurriculumError, match="concepts debe ser una lista no vacía"):
        curriculum_from_dict(d)


def test_quests_no_lista_rechazado() -> None:
    """`quests` debe ser una lista (puede estar vacía); un dict no vale."""
    d = _doc()
    d["quests"] = {"id": "x"}
    with pytest.raises(CurriculumError, match="quests debe ser una lista"):
        curriculum_from_dict(d)


def test_concept_sin_campo_id_rechazado() -> None:
    """Campo `id` ausente en un concept → error accionable indicando la ruta."""
    d = _doc()
    del d["concepts"][0]["id"]
    with pytest.raises(CurriculumError, match="falta el campo"):
        curriculum_from_dict(d)


def test_prerequisites_no_lista_rechazado() -> None:
    """`prerequisites` debe ser una lista de strings: un str suelto no vale."""
    d = _doc()
    d["concepts"][0]["prerequisites"] = "c.ls"
    with pytest.raises(CurriculumError, match="lista de strings"):
        curriculum_from_dict(d)


def test_familia_inventada_rechazada_y_msg_lista_validas() -> None:
    """Familia fuera de las ocho → el mensaje enumera las válidas (accionable,
    no solo «no», sino «válidas: [...]»)."""
    d = _doc()
    d["concepts"][0]["family"] = "inventada"
    with pytest.raises(CurriculumError, match="familia desconocida") as exc_info:
        curriculum_from_dict(d)
    for fam in sorted(FAMILIES):
        assert fam in str(exc_info.value)


def test_tint_dorado_rechazado_y_msg_lista_validos() -> None:
    """Tint fuera de {blue, red, grey} → mensaje con los válidos."""
    d = _doc()
    d["quests"][0]["tint"] = "dorado"
    with pytest.raises(CurriculumError, match="tint desconocido") as exc_info:
        curriculum_from_dict(d)
    for t in sorted(TINTS):
        assert t in str(exc_info.value)


def test_beat_key_entero_rechazado() -> None:
    """`beat_key` solo admite string o null; un entero es tipo inválido."""
    d = _doc()
    d["quests"][0]["beat_key"] = 7
    with pytest.raises(CurriculumError, match="beat_key debe ser string o null"):
        curriculum_from_dict(d)


def test_doc_no_plano_es_curriculum_error_no_notplain() -> None:
    """Un dict con una tupla dentro NO es JSON plano estricto → `CurriculumError`
    envuelto (no una `NotPlainDataError` cruda filtrándose al llamador)."""
    d = _doc()
    d["extra"] = (1, 2)  # tupla → viola ensure_plain
    with pytest.raises(CurriculumError, match="JSON plano"):
        curriculum_from_dict(d)


# ----------------------------------------------------------------------------
# NEGATIVO — load_curriculum sobre Path (tmp_path)
# ----------------------------------------------------------------------------
def test_json_roto_via_load_curriculum(tmp_path) -> None:
    """Un fichero no-JSON en disco se rechaza con mensaje de parseo accionable."""
    broken = tmp_path / "curriculum.json"
    broken.write_text("{no json", encoding="utf-8")
    with pytest.raises(CurriculumError, match="no es JSON válido"):
        load_curriculum(broken)


def test_fichero_inexistente_mensaje_no_se_pudo_leer(tmp_path) -> None:
    """Un Path que no existe → CurriculumError con «no se pudo leer» y la ruta."""
    missing = tmp_path / "no_existe.json"
    with pytest.raises(CurriculumError, match="no se pudo leer"):
        load_curriculum(missing)


def test_json_valido_via_load_curriculum_desde_tmp(tmp_path) -> None:
    """Un JSON válido en un Path arbitrario carga igual que el fichero real:
    prueba el contrato del parámetro `path`, no solo el default."""
    good = tmp_path / "curso.json"
    good.write_text(json.dumps(_doc(), ensure_ascii=False), encoding="utf-8")
    cur = load_curriculum(good)
    assert [c.id for c in cur.concepts] == ["a", "b"]