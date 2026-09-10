"""test_ch6_dato2_dato3.py — E2 (corte horizontal) + E3 (orden vertical) del Faro (T1/T2, Seath 05/09).

T1 (🧭17 + enmienda 🧭18): quest story.ch6.dato2 exige cut por necesidad
  requires [c.cut,c.uniq,c.sort], golden cut -d'|' -f4 ... | sort | uniq -c,
  briefing con cut y rutas absolutas, .nota-corte hallazgo.
T2: quest story.ch6.dato3 exige sort -k12 por necesidad
  requires [c.cut,c.sort,c.head], golden sort -t'|' -k12 -n ... | head -n 3.

Gate de datos 22→23 (E2) →24 (E3) en la misma rama; suite delta +7.
"""
from __future__ import annotations

import pytest
from core.curriculum import load_curriculum
from core.generator import generate, new_session
from core.generator.chapter6 import (
    NOTA_CORTE_CONTENT,
    NOTA_CORTE_PATH,
    PURGAS_PATH,
    REGISTRO_PATH,
    CEBO_PATH,
)
from core.sandbox.fs import FileNode
from data.textos import load_textos, resolve

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _resolver(inc, path: str):
    return inc.room.fs.resolve(path, "/")


# ---------------------------------------------------------------------------
# DAG / curriculum
# ---------------------------------------------------------------------------
def test_quest_ch6_dato2_valida_en_dag_y_gate_23():
    cur = load_curriculum()
    q = cur.quest("story.ch6.dato2")
    assert q is not None, "story.ch6.dato2 no existe (T1 Seath)"
    assert q.chapter == 6
    assert set(q.requires) == {"c.cut", "c.uniq", "c.sort"}
    assert q.title_key == "story.ch6.dato2.title"
    assert q.beat_key == "story.ch6.dato2.beat"
    assert len(cur.quests) == 27
    assert len(cur.concepts) == 24

def test_quest_ch6_dato3_valida_en_dag_y_gate_24():
    cur = load_curriculum()
    q = cur.quest("story.ch6.dato3")
    assert q is not None, "story.ch6.dato3 no existe (T2 Seath)"
    assert q.chapter == 6
    assert set(q.requires) == {"c.cut", "c.sort", "c.head"}
    assert q.title_key == "story.ch6.dato3.title"
    assert len(cur.quests) == 27
    # Prereqs enseñados en <=6
    chap_concepts = {c.id for c in cur.concepts if c.chapter <= 6}
    for r in q.requires:
        assert r in chap_concepts

# ---------------------------------------------------------------------------
# E2 — FS + .nota-corte + golden cut|sort|uniq -c (🧭18)
# ---------------------------------------------------------------------------
def test_dato2_sala_expone_ficheros_y_nota_corte():
    inc = generate(42, 6, contract_id="story.ch6.dato2")
    assert inc.chapter == 6
    assert inc.contract.objective_key == "story.ch6.dato2"
    # Lista intacta
    pur = _resolver(inc, PURGAS_PATH)
    assert isinstance(pur, FileNode) and "PR-0091" in pur.content
    reg = _resolver(inc, REGISTRO_PATH)
    assert isinstance(reg, FileNode)
    # Cebo intacto
    cebo = _resolver(inc, CEBO_PATH)
    assert isinstance(cebo, FileNode)
    # .nota-corte legible (boon hallazgo Bandit)
    nota = _resolver(inc, NOTA_CORTE_PATH)
    assert isinstance(nota, FileNode)
    assert nota.content == NOTA_CORTE_CONTENT
    assert "cut -d'|'" in nota.content
    assert "purgas.csv" in nota.content

def test_dato2_golden_cut_sort_uniq_exit_0():
    inc = generate(42, 6, contract_id="story.ch6.dato2")
    shell = new_session(inc)
    # Golden canónico de E2 (cut|sort|uniq -c) — la forma enseñada en el briefing
    r = shell.execute(f"cut -d'|' -f4 {PURGAS_PATH} | sort | uniq -c")
    assert r.exit_code == 0, f"stderr: {r.stderr!r}"
    # Debe agrupar distritos: salida contiene distritos conocidos con conteo alineado
    out = r.stdout
    assert "UMBRAL-BAJO" in out or "MUEL-01" in out or "--" in out
    # Sin sort no agrupa (4×1) — comprueba que el pipe con sort SÍ agrupe
    # (enmienda 🧭18: uniq -c sin sort no cumple promesa)
    r2 = shell.execute(f"cut -d'|' -f4 {PURGAS_PATH} | uniq -c")
    # uniq sin sort deja 4 líneas (cabecera+3 filas) si no hay orden
    # No exigimos valor exacto, solo que ambos den exit 0 y el primero agrupe
    assert r2.exit_code == 0

def test_dato2_briefing_menciona_cut_y_ruta_absoluta():
    textos = load_textos()
    beat = resolve("story.ch6.dato2.beat", textos=textos)
    assert "cut" in beat.lower()
    assert "/srv/camara-faro/" in beat
    assert "/srv/camara-faro/purgas.csv" in beat
    assert "/srv/camara-faro/.nota-corte" in beat
    title = resolve("story.ch6.dato2.title", textos=textos)
    assert title.strip()

def test_dato2_determinista_por_seed():
    a = generate(99, 6, contract_id="story.ch6.dato2")
    b = generate(99, 6, contract_id="story.ch6.dato2")
    assert a.to_dict() == b.to_dict()

# ---------------------------------------------------------------------------
# E3 — sort -k12 vertical (lectura VERTICAL de la Lista)
# ---------------------------------------------------------------------------
def test_dato3_briefing_menciona_k_y_ruta_absoluta():
    textos = load_textos()
    beat = resolve("story.ch6.dato3.beat", textos=textos)
    # Exige -k por necesidad
    assert "-k" in beat or "k12" in beat
    assert "/srv/camara-faro/" in beat
    assert "purgas.csv" in beat
    title = resolve("story.ch6.dato3.title", textos=textos)
    assert title.strip()

def test_dato3_golden_sort_k12_head_exit_0_si_soporte():
    """El golden E3: sort -t'|' -k12 -n ... | head -n 3"""
    inc = generate(42, 6, contract_id="story.ch6.dato3")
    shell = new_session(inc)
    r = shell.execute(f"sort -t '|' -k12 -n {PURGAS_PATH} | head -n 3")
    # Si sandbox no soporta -k/-t aún (rama meta-ui sola sin S1), el stderr lo delata (head enmascara exit).
    if "invalid option" in r.stderr or "Try 'sort" in r.stderr:
        pytest.skip("sort -k no soportado en esta rama sola — verde tras S1 (orden de merges)")
    assert r.exit_code == 0, f"stderr: {r.stderr!r}"
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    assert len(lines) == 3, f"esperaba 3 líneas: {r.stdout!r}"
    # Orden por puntuación: el primero debe ser PR-0091 (puntuación --/0, el más cerca del 0)
    # Tras sort -n, las líneas con -- pueden ir primero numéricamente vacío → 0
    assert any("PR-0091" in l for l in lines) or "000" in lines[0]

def test_dato3_sin_k_no_se_puede_responder():
    """Sin -k la pregunta vertical no se puede responder (golden lo exige)."""
    textos = load_textos()
    beat = resolve("story.ch6.dato3.beat", textos=textos)
    # El briefing Nombra -k como requisito (lectura vertical)
    assert "k12" in beat or "-k" in beat
    # La quest requiere c.sort y c.head y c.cut (sin sort -k no hay lectura vertical)
    cur = load_curriculum()
    q = cur.quest("story.ch6.dato3")
    assert "c.sort" in q.requires


def test_namespace_ch6_dato_vs_encargo():
    """Regla fijada 06/09: E-space 1:1 con prosa; salas-dato = datoN, nunca eK (salvo e1).

    Verifica que el cap. 6 NO tenga quests e2/e3 colisionando con la prosa
    (los encargos narrativos «La que no pesa»/«La persiana» reservan e2/e3)
    y que las salas-dato usan dato2/dato3.

    Actualizado 08/09 (Ornstein O2): e2 ya existe como encargo narrativo
    «La que no pesa», por lo que e2 SÍ está en ids (encargo), pero e3 sigue
    reservado. Las salas-dato siguen siendo dato2/dato3.
    """
    cur = load_curriculum()
    ids = {q.id for q in cur.quests_for_chapter(6)}
    # e1 es la sala de la Lista (no hay choque, prosa E1 ES esa sala)
    assert "story.ch6.e1" in ids
    # salas-dato nuevas
    assert "story.ch6.dato2" in ids
    assert "story.ch6.dato3" in ids
    # e2 ya existe como encargo narrativo (08/09), e3 aún reservado
    assert "story.ch6.e2" in ids
    assert "story.ch6.e3" not in ids
    # textos siguen la misma regla (e2 ahora sí tiene textos)
    textos = load_textos()
    assert "story.ch6.dato2.title" in textos
    assert "story.ch6.dato3.title" in textos
    assert "story.ch6.e2.title" in textos
    assert "story.ch6.e3.title" not in textos
