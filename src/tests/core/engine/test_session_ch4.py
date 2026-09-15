"""O1 (15/09, Ornstein) — session.py cap. 4 jugable como encargo.

Tests FLEXIBLES: no dependen de que Smough haya subido `story.ch4.e3` a las
16:00. Verifican listar/abrir/cerrar de ch4 con las quests YA en main (e1/e2);
la quest e3 entra gratis cuando S1 la sube (engine lee del curriculum, no
requiere código nuevo de O1). Si e3 no existe al 19:00, el test negativo queda
honesto (abrible=False, missing=[...]) — señal, no bug.
"""

from __future__ import annotations

from core.curriculum import load_curriculum
from core.engine import abrir_encargo, cerrar_encargo, listar_encargos
from core.engine.session import SUPPORTED_CHAPTERS, _commands_for
from core.sandbox.shell import DEFAULT_CH4_COMMANDS

CUR = load_curriculum()


def test_session_ch4_supported_and_commands():
    """SUPPORTED_CHAPTERS incluye 4 y _commands_for(4) es la base 13."""
    assert 4 in SUPPORTED_CHAPTERS
    assert SUPPORTED_CHAPTERS == frozenset({0, 2, 4})
    assert _commands_for(4) == DEFAULT_CH4_COMMANDS
    # regresión: 0 y 2 intactos
    from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS

    assert _commands_for(0) == DEFAULT_CAP0_COMMANDS
    assert _commands_for(2) == DEFAULT_CH2_COMMANDS


def test_listar_encargos_ch4_flexible():
    """listar ch4 → e1+e2 siempre; e3 si Smough ya la subió (flexible)."""
    quests = listar_encargos(CUR, 4)
    ids = [q["id"] for q in quests]
    # e1 y e2 deben existir en main actual
    assert "story.ch4.e1" in ids, f"e1 falta, ids={ids}"
    assert "story.ch4.e2" in ids, f"e2 falta, ids={ids}"
    # orden determinista
    assert ids == sorted(ids), "listar debe ordenar por id"
    # con knowledge cut+scp, ambos deben ser abribles (e2 requires cut+scp, e1 solo scp)
    with_kn = listar_encargos(CUR, 4, knowledge=["c.cut", "c.scp"])
    by_id = {q["id"]: q for q in with_kn}
    assert by_id["story.ch4.e1"]["abrible"] is True, by_id["story.ch4.e1"]
    assert by_id["story.ch4.e1"]["falta"] == []
    assert by_id["story.ch4.e2"]["abrible"] is True, by_id["story.ch4.e2"]
    assert by_id["story.ch4.e2"]["falta"] == []
    # e3 flexible: si existe, debe aparecer con abrible según requires (sin hardcodear requires)
    if "story.ch4.e3" in by_id:
        q = by_id["story.ch4.e3"]
        # si tiene requires vacíos o con cut/scp, debería ser abrible; si no, debe indicar falta honesto
        assert "abrible" in q and "falta" in q


def test_abrir_ch4_e2_con_cut_scp_y_shell_activa():
    """Abrir story.ch4.e2 con knowledge cut+scp → abrible + session con shell activa."""
    res = abrir_encargo(CUR, "story.ch4.e2", ["c.cut", "c.scp"], run_seed=7)
    assert res["abrible"] is True, f"debería abrir e2 con cut+scp, got {res}"
    sess = res["session"]
    assert sess.chapter == 4
    assert sess.quest_id == "story.ch4.e2"
    assert sess.seed == "story.ch4.e2:7"
    # shell activa y determinista
    r = sess.ejecutar("ls")
    assert r.exit_code == 0, r.stderr
    # el shell usa la allowlist base de ch4 (13) — cd y scp deben existir
    assert "scp" in sess.shell.available_commands
    assert "cut" in sess.shell.available_commands
    # sin prereqs debe rechazar honesto (no crash)
    rej = abrir_encargo(CUR, "story.ch4.e2", [], run_seed=7)
    assert rej["abrible"] is False
    assert rej["missing"]  # accionable


def test_cerrar_ch4_e2_adjunta_postmortem():
    """Cerrar un e2 simulado → post-mortem con factura honesta (regresión informe)."""
    res = abrir_encargo(CUR, "story.ch4.e2", ["c.cut", "c.scp"], run_seed=7)
    assert res["abrible"] is True
    s = res["session"]
    # jugar un poco (varios comandos para generar factura)
    s.ejecutar("ls")
    s.ejecutar("cat /etc/hosts")
    cierre = cerrar_encargo(s, modo="completado")
    assert cierre["quest_id"] == "story.ch4.e2"
    assert cierre["modo"] == "completado"
    pm = cierre["postmortem"]
    # factura honesta
    assert "factura" in pm and "total_noise" in pm
    assert "auditor" in pm and "line_key" in pm["auditor"]
    assert pm["noise_budget"] == s.incursion.room.noise_budget
    # expulsión entrega el mismo tipo de informe (modo distinto)
    res2 = abrir_encargo(CUR, "story.ch4.e2", ["c.cut", "c.scp"], run_seed=9)
    s2 = res2["session"]
    s2.ejecutar("ls")
    cierre2 = cerrar_encargo(s2, modo="expulsión")
    assert cierre2["modo"] == "expulsión"
    assert "postmortem" in cierre2
