"""test_session_ch5.py — puerta normal del Asalto (cap. 5) via session.

O1 18/09 (Ornstein): verifica que el cap. 5 es jugable por la puerta normal
(abrir_encargo) con la geografía condicional del volcado.

- SUPPORTED_CHAPTERS incluye 5; _commands_for(5) == ("cat","scp")
- listar_encargos(cur,5) devuelve 4 encargos (e1..e4) y solo e2 abrible
- abrir_encargo ch5.e2 con volcado_rescatado=True -> cat volcado-custodia.csv exit 0 TR-003
- sin flag -> cat -> No such file (ausencia honesta)
- rechazo accionable para e1/e3/e4 nombra missing y NO genera sala
- determinismo x2 seeds byte-idéntico por to_dict del FS
- volcado_del_save helper lee volcado rescatado
"""

from core.curriculum import load_curriculum
from core.engine.session import SUPPORTED_CHAPTERS, _commands_for, abrir_encargo, listar_encargos, volcado_del_save


def test_supported_incluye_5_y_commands():
    assert 5 in SUPPORTED_CHAPTERS
    assert _commands_for(5) == ("cat", "scp")
    # sin quest_id y con quest_id debe ser igual
    assert _commands_for(5, "story.ch5.e2") == ("cat", "scp")


def test_listar_ch5_solo_e2_abrible():
    cur = load_curriculum()
    lst = listar_encargos(cur, 5, knowledge={"c.cat", "c.scp", "c.ls-la", "c.chmod", "c.chown", "c.grep", "c.ps", "c.env"})
    ids = [x["id"] for x in lst]
    assert sorted(ids) == ["story.ch5.e1", "story.ch5.e2", "story.ch5.e3", "story.ch5.e4"]
    # e2 debe estar presente y ser abrible con conocimiento suficiente
    e2 = next(x for x in lst if x["id"] == "story.ch5.e2")
    assert e2["abrible"] is True
    # e2 knowledge mínimo
    lst2 = listar_encargos(cur, 5, knowledge={"c.cat", "c.scp"})
    e2b = next(x for x in lst2 if x["id"] == "story.ch5.e2")
    assert e2b["abrible"] is True
    # e1/e3/e4 no abribles con solo cat+scp (requieren más)
    for qid in ("story.ch5.e1", "story.ch5.e3", "story.ch5.e4"):
        q = next(x for x in lst2 if x["id"] == qid)
        assert q["abrible"] is False


def test_abrir_ch5_e2_rescatado_cat_ok():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    sess = r["session"]
    # allowlist ch5
    assert sess.shell.available_commands == {"cat", "scp"}
    res = sess.ejecutar("cat /tmp/volcado-custodia.csv")
    assert res.exit_code == 0
    assert "TR-003|faro|troncal-01|512|EN_COLA" in res.stdout


def test_abrir_ch5_e2_caducado_cat_falla():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=42, volcado_rescatado=False)
    assert r["abrible"] is True
    sess = r["session"]
    res = sess.ejecutar("cat /tmp/volcado-custodia.csv")
    assert res.exit_code != 0
    assert "No such file" in res.stderr or "No such file" in res.stdout or "No such file" in res.stderr


def test_ch5_solo_e2_abre_otros_rechazados():
    cur = load_curriculum()
    for qid in ("story.ch5.e1", "story.ch5.e3", "story.ch5.e4"):
        r = abrir_encargo(cur, qid, {"c.cat", "c.scp", "c.ls-la", "c.chmod", "c.chown", "c.grep", "c.ps", "c.env"}, run_seed=1)
        assert r["abrible"] is False
        assert "encargo sin flujo materializado en cap. 5 (hoy solo e2)" in r["missing"]


def test_ch5_determinismo_volcado_rescatado():
    cur = load_curriculum()
    r1 = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=99, volcado_rescatado=True)
    r2 = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=99, volcado_rescatado=True)
    assert r1["session"].incursion.room.fs.to_dict() == r2["session"].incursion.room.fs.to_dict()
    # caducado también determinista
    r3 = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=99, volcado_rescatado=False)
    r4 = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=99, volcado_rescatado=False)
    assert r3["session"].incursion.room.fs.to_dict() == r4["session"].incursion.room.fs.to_dict()
    # rescatado vs caducado difieren
    assert r1["session"].incursion.room.fs.to_dict() != r3["session"].incursion.room.fs.to_dict()


def test_volcado_del_save_helper():
    assert volcado_del_save({"volcado": "rescatado"}) is True
    assert volcado_del_save({"volcado": "caducado"}) is False
    assert volcado_del_save({}) is False
    assert volcado_del_save(None) is False
