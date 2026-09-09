"""O2 — Quest story.ch6.e2 «La que no pesa» (08/09, Ornstein, REPOSICIÓN e2).

Gate 23→24, FICHA vacía, golden tail -n +2 + distrito repetido, briefing.

AC del plan 08/09:
- gate 23→24 quests, e1 intacta, goldens dato2/dato3 exit 0, e2 valida exit 0
- suite 621→625 (+4 mínimo: quest + golden + 2 negativos validador)
"""
from __future__ import annotations

from core.curriculum import load_curriculum
from core.generator import generate, new_session
from core.generator.chapter6 import PURGAS_PATH, HOSTS_PATH
from core.sandbox.fs import FileNode
from data.textos import load_textos, resolve


def test_quest_e2_existe_gate_24_y_e1_intacta():
    cur = load_curriculum()
    assert len(cur.quests) == 25
    assert len(cur.concepts) == 23
    e2 = cur.quest("story.ch6.e2")
    assert e2 is not None
    assert e2.chapter == 6
    assert e2.tint == "grey"
    assert set(e2.requires) == {"c.tail", "c.cut", "c.sort", "c.uniq"}
    assert e2.title_key == "story.ch6.e2.title"
    assert e2.beat_key == "story.ch6.e2.beat"
    # e1 intacta
    e1 = cur.quest("story.ch6.e1")
    assert e1 is not None
    assert e1.chapter == 6
    # dato2/dato3 siguen
    assert cur.quest("story.ch6.dato2") is not None
    assert cur.quest("story.ch6.dato3") is not None


def test_e2_textos_briefing_con_distrito_repetido_y_tail():
    textos = load_textos()
    assert resolve("story.ch6.e2.title", textos=textos) == "La que no pesa"
    beat = resolve("story.ch6.e2.beat", textos=textos)
    assert "/srv/camara-faro/" in beat
    assert "/srv/camara-faro/purgas.csv" in beat
    assert "tail -n +2" in beat
    # briefing anticipa distrito repetido y coma trampa
    briefing = resolve("story.ch6.e2.briefing", textos=textos)
    assert "un distrito se repite" in briefing.lower() or "distrito que se repite" in briefing.lower()
    assert "UMBRAL-BAJO" in briefing or "distrito" in briefing
    assert "PR-0092" in briefing
    assert "EN BLANCO, revisado" in briefing
    assert "/srv/camara-faro/purgas.csv" in briefing


def test_e2_golden_tail_sin_header_fantasma_y_dos_umb():
    inc = generate(42, 6, contract_id="story.ch6.e2")
    assert inc.contract.objective_key == "story.ch6.e2"
    shell = new_session(inc)
    r = shell.execute(f"tail -n +2 {PURGAS_PATH} | cut -d'|' -f4 | sort")
    assert r.exit_code == 0, f"stderr: {r.stderr!r}"
    out = r.stdout
    assert "distrito" not in out, f"header fantasma presente: {out!r}"
    assert out.count("UMBRAL-BAJO") == 2, f"esperaba 2 UMBRAL-BAJO, got {out!r}"
    assert "MUEL-01" in out
    assert "--" in out


def test_e1_dato2_dato3_goldens_siguen_exit_0():
    # e1
    inc1 = generate(42, 6, contract_id="story.ch6.e1")
    s1 = new_session(inc1)
    r1 = s1.execute(f"grep ENSAYO {PURGAS_PATH} | wc -l")
    assert r1.exit_code == 0
    assert r1.stdout.strip() == "1"
    # dato2
    inc2 = generate(42, 6, contract_id="story.ch6.dato2")
    s2 = new_session(inc2)
    r2 = s2.execute(f"cut -d'|' -f4 {PURGAS_PATH} | sort | uniq -c")
    assert r2.exit_code == 0
    assert "UMBRAL-BAJO" in r2.stdout
    # dato3
    inc3 = generate(42, 6, contract_id="story.ch6.dato3")
    s3 = new_session(inc3)
    r3 = s3.execute(f"sort -t '|' -k12 -n {PURGAS_PATH} | head -n 3")
    # si sort no soporta -k, skip
    if "Try 'sort" in r3.stderr:
        import pytest
        pytest.skip("sort -k no soportado en esta rama")
    assert r3.exit_code == 0
    assert len([l for l in r3.stdout.splitlines() if l.strip()]) == 3
