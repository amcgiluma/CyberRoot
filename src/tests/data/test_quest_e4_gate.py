"""test_quest_e4_gate.py — GATE OWNER Smough 26/09: story.ch6.e4 El trato (Faro E4).

GATE OWNER = Smough (único que toca curriculum.json). Verifica que la quest
grey story.ch6.e4 existe con requires ['c.join'] (cero conceptos nuevos),
gate 25/31 -> 25/32, y que los textos resuelven con voz formulario y la
palanca «cruzo y camino al reloj» (dos testigos /tmp/prueba-custodia/).

No toca allowlists ni session.py (cap.6 sin flujo materializado es
esperado: prereqs se verifican al ABRIR contrato, no al generar sala).
"""
from __future__ import annotations

import pytest
from core.curriculum.loader import load_curriculum
from data.textos import load_textos, resolve


def test_gate_25_32_quest_existe():
    cur = load_curriculum()
    assert len(cur.concepts) == 25, "cero conceptos nuevos"
    assert len(cur.quests) == 32, f"gate 25/31 -> 25/32, got {len(cur.quests)}"
    q = cur.quest("story.ch6.e4")
    assert q is not None, "quest story.ch6.e4 debe existir"
    assert q.chapter == 6
    assert q.tint == "grey"
    assert list(q.requires) == ["c.join"]
    assert q.title_key == "story.ch6.e4.title"
    assert q.beat_key == "story.ch6.e4.beat"


def test_requires_c_join_transitivos_vivos():
    cur = load_curriculum()
    c_join = cur.concept("c.join")
    assert c_join is not None
    assert c_join.chapter == 6
    # prereqs ya vivos: c.cut (4) y c.sort (6)
    assert set(c_join.prerequisites) == {"c.cut", "c.sort"}
    by_id = {c.id: c for c in cur.concepts}
    for p in c_join.prerequisites:
        assert by_id[p].chapter <= c_join.chapter

    # dato4/dato5 ya vivos usan c.join y c.ps — misma filosofía
    assert cur.quest("story.ch6.dato4") is not None
    assert cur.quest("story.ch6.dato5") is not None


def test_abrible_via_prereqs_met():
    from core.generator.model import Contract
    cur = load_curriculum()
    q = cur.quest("story.ch6.e4")
    assert q is not None
    contract = Contract(chapter=q.chapter, objective_key=q.id, brief_text_key=f"{q.id}.briefing")
    # con c.join -> abrible True (usa la MISMA puerta que el motor: prereqs_met)
    assert contract.prereqs_met(cur, {"c.join"}) is True
    # sin c.join -> falta
    assert contract.prereqs_met(cur, set()) is False
    # solo c.join basta, no necesita enumerar transitivos (filosofía dato4)
    assert list(q.requires) == ["c.join"]


def test_textos_resuelven_y_palanca():
    t = load_textos()
    # 4 filas originales + hint_2 HOME persona
    for key in ["story.ch6.e4.title", "story.ch6.e4.beat", "story.ch6.e4.briefing", "story.ch6.e4.hint_1", "story.ch6.e4.hint_2", "story.ch6.e4.detail"]:
        assert key in t, f"{key} ausente en textos.json"
        txt = resolve(key, textos=t)
        assert txt.strip(), f"{key} vacío"
    assert resolve("story.ch6.e4.title", textos=t) == "El trato"
    beat = resolve("story.ch6.e4.beat", textos=t)
    assert "11:04" in beat or "reloj" in beat.lower()
    briefing = resolve("story.ch6.e4.briefing", textos=t)
    # palanca: dos pruebas, cruce y reloj
    assert "/tmp/prueba-custodia/" in briefing
    assert "PR-0091" in briefing
    assert "11:04" in briefing
    # vuelta a HOME persona — hint_2 la lleva
    hint2 = resolve("story.ch6.e4.hint_2", textos=t)
    assert "HOME" in hint2 or "cd" in hint2
    assert "persona" in hint2.lower() or "casa" in hint2.lower()


def test_sin_conceptos_nuevos_y_json_plano():
    cur = load_curriculum()
    assert len(cur.concepts) == 25
    # valida que el fichero sigue siendo JSON plano estricto (loader ya lo hace)
    t = load_textos()
    assert "story.ch6.e4.title" in t
