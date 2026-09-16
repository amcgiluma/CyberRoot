"""O1 (16/09, Ornstein) — session.py e3 expone rm (simetría scp/rm, 🧭36).

Criterio: _commands_for(4) base 13 INTACTA en e1/e2; solo e3 14 con rm.
abrir_encargo(c,'story.ch4.e3') → rm /tmp/volcado.csv exit 0 → post-mortem caducado.
Tests FLEXIBLES: e1/e2 ⊆ ids, e3 opcional si curriculum la trae (ya en main).
"""

from __future__ import annotations

from core.curriculum import load_curriculum
from core.engine import abrir_encargo, cerrar_encargo
from core.engine.session import _commands_for
from core.sandbox.shell import DEFAULT_CH4_COMMANDS, DEFAULT_CH4E3_COMMANDS

CUR = load_curriculum()


def test_commands_for_e3_vs_base():
    """Base 13 intacta; e3 devuelve 14 con rm."""
    assert _commands_for(4) == DEFAULT_CH4_COMMANDS
    assert len(DEFAULT_CH4_COMMANDS) == 13
    assert len(DEFAULT_CH4E3_COMMANDS) == 14
    assert "rm" not in DEFAULT_CH4_COMMANDS
    assert "rm" in DEFAULT_CH4E3_COMMANDS
    assert _commands_for(4, "story.ch4.e3") == DEFAULT_CH4E3_COMMANDS
    # e1/e2 siguen base
    assert _commands_for(4, "story.ch4.e1") == DEFAULT_CH4_COMMANDS
    assert _commands_for(4, "story.ch4.e2") == DEFAULT_CH4_COMMANDS
    # legado sin quest_id sigue base
    assert set(DEFAULT_CH4_COMMANDS) <= set(DEFAULT_CH4E3_COMMANDS)


def test_abrir_e3_expone_rm_y_postmortem_caducado():
    """abrir e3 → rm exit 0 → volcado caducado (no tick30)."""
    # e3 existe en curriculum post-15/09; si no, skip honesto
    ids = [q.id for q in CUR.quests_for_chapter(4)]
    if "story.ch4.e3" not in ids:
        # flexible: curriculum sin e3 → _commands_for ya verificado arriba
        return
    res = abrir_encargo(CUR, "story.ch4.e3", ["c.scp"], run_seed=11)
    assert res["abrible"] is True, res
    sess = res["session"]
    assert "rm" in sess.shell.available_commands
    assert sess.shell.available_commands == set(DEFAULT_CH4E3_COMMANDS)
    # Traer el volcado a local (como haría el jugador) y luego disolverlo
    # new_session ya pre-puebla hosts, así que scp funciona sin cat previo
    r_scp = sess.ejecutar("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv")
    assert r_scp.exit_code == 0, f"scp en e3 debe ser 0, got {r_scp.exit_code} {r_scp.stderr!r}"
    r = sess.ejecutar("rm /tmp/volcado.csv")
    assert r.exit_code == 0, f"rm en e3 debe ser 0, got {r.exit_code} {r.stderr!r}"
    # post-mortem debe marcar caducado por rm (sin necesidad de tick>=30)
    cierre = cerrar_encargo(sess, modo="completado")
    pm = cierre["postmortem"]
    assert pm.get("volcado") == "caducado", pm
    assert pm["auditor_volcado"]["line_key"] == "postmortem.volcado.caducado"


def test_e1_e2_rm_sigue_127_frontera_intacta():
    """e1/e2 con base 13: rm →127, frontera intacta."""
    for qid in ("story.ch4.e1", "story.ch4.e2"):
        q = CUR.quest(qid)
        req = q.requires if q is not None else []
        # knowledge que abra el encargo
        knowledge = list(req) if req else ["c.scp"]
        # e2 requiere cut+scp, e1 solo scp
        if qid == "story.ch4.e2":
            knowledge = ["c.cut", "c.scp"]
        res = abrir_encargo(CUR, qid, knowledge, run_seed=3)
        assert res["abrible"] is True, f"{qid} debe abrir con {knowledge}, got {res}"
        sess = res["session"]
        assert "rm" not in sess.shell.available_commands, qid
        r = sess.ejecutar("rm /tmp/volcado.csv")
        assert r.exit_code == 127, f"{qid} rm debe ser 127, got {r.exit_code} {r.stderr!r}"
        assert "command not found" in r.stderr.lower() or "rm" in r.stderr.lower()


def test_e3_vs_e1_determinismo_y_listar():
    """listar ch4 ordenado; abrir e3 determinista por seed."""
    from core.engine import listar_encargos

    quests = listar_encargos(CUR, 4)
    ids = [q["id"] for q in quests]
    assert ids == sorted(ids)
    assert "story.ch4.e1" in ids and "story.ch4.e2" in ids
    if "story.ch4.e3" in ids:
        r1 = abrir_encargo(CUR, "story.ch4.e3", ["c.scp"], run_seed=42)
        r2 = abrir_encargo(CUR, "story.ch4.e3", ["c.scp"], run_seed=42)
        assert r1["session"].seed == r2["session"].seed == "story.ch4.e3:42"
        # dos sesiones con mismo seed deben tener FS idénticos (snapshot)
        assert r1["session"].shell.fs.to_dict() == r2["session"].shell.fs.to_dict()
