"""test_session_ch5.py — puerta COMPLETA Subestación (cap. 5) via session.

O1 20/09 (Ornstein): los 4 encargos e1/e2/e3/e4 abren por la misma puerta
(misma rutina que e2), con volcado condicional en TODOS.

- SUPPORTED_CHAPTERS incluye 5; _commands_for(5) == ("cat","scp")
- listar_encargos(cur,5) devuelve 4 encargos, todos abribles con knowledge completa
- abrir_encargo e1/e3/e4 → abrible True con prereqs correctos del curriculum
- volcado condicional en e1/e4 (y e3/e2): True→cat exit 0 TR-003; False→No such file exit 1
- e2 intacta (misma semántica)
- determinismo ×2 seeds byte-idéntico (generate 42,5 / 99,5)
- volcado_del_save helper
"""

from core.curriculum import load_curriculum
from core.engine.session import SUPPORTED_CHAPTERS, _commands_for, abrir_encargo, listar_encargos, volcado_del_save
from core.generator import generate


def test_supported_incluye_5_y_commands():
    assert 5 in SUPPORTED_CHAPTERS
    assert _commands_for(5) == ("cat", "scp")
    assert _commands_for(5, "story.ch5.e2") == ("cat", "scp", "ps", "grep")
    # base intacta: nova añade, no reempaza (forma <=, plan 24/09)
    assert {"cat", "scp"} <= set(_commands_for(5, "story.ch5.e2"))
    # SUPPORTED debe ser exactamente {0,2,4,5}
    assert SUPPORTED_CHAPTERS == frozenset({0, 2, 4, 5})


def test_listar_ch5_todos_presentes():
    cur = load_curriculum()
    lst = listar_encargos(cur, 5, knowledge={"c.cat", "c.scp", "c.ls-la", "c.chmod", "c.chown", "c.grep", "c.ps", "c.env"})
    ids = sorted(x["id"] for x in lst)
    assert ids == ["story.ch5.e1", "story.ch5.e2", "story.ch5.e3", "story.ch5.e4"]
    # con knowledge completa, los 4 deben ser abribles
    for x in lst:
        assert x["abrible"] is True, f"{x['id']} debería ser abrible con knowledge completa"


def test_abrir_ch5_e1_requires_y_abrible():
    cur = load_curriculum()
    # requires de e1: c.ls-la, c.cat, c.chmod
    q = cur.quest("story.ch5.e1")
    assert set(q.requires) == {"c.ls-la", "c.cat", "c.chmod"}
    # sin knowledge suficiente → no abrible con missing honesto
    r = abrir_encargo(cur, "story.ch5.e1", {"c.cat"}, run_seed=1)
    assert r["abrible"] is False
    assert "c.ls-la" in r["missing"]
    # con knowledge justa → abrible
    r2 = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=True)
    assert r2["abrible"] is True
    assert "session" in r2


def test_abrir_ch5_e3_requires_y_abrible():
    cur = load_curriculum()
    q = cur.quest("story.ch5.e3")
    assert set(q.requires) == {"c.ps", "c.env"}
    r = abrir_encargo(cur, "story.ch5.e3", {"c.ps"}, run_seed=1)
    assert r["abrible"] is False
    assert "c.env" in r["missing"]
    r2 = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=7, volcado_rescatado=False)
    assert r2["abrible"] is True


def test_abrir_ch5_e4_requires_y_abrible():
    cur = load_curriculum()
    q = cur.quest("story.ch5.e4")
    assert set(q.requires) == {"c.chmod", "c.chown", "c.cat", "c.grep"}
    r = abrir_encargo(cur, "story.ch5.e4", {"c.cat"}, run_seed=1)
    assert r["abrible"] is False
    r2 = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=3, volcado_rescatado=True)
    assert r2["abrible"] is True


def test_abrir_ch5_e2_intacta():
    cur = load_curriculum()
    q = cur.quest("story.ch5.e2")
    assert set(q.requires) == {"c.cat", "c.scp", "c.grep"}
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    sess = r["session"]
    assert sess.shell.available_commands == {"cat", "scp", "ps", "grep"}
    assert {"cat", "scp"} <= sess.shell.available_commands
    res = sess.ejecutar("cat /tmp/volcado-custodia.csv")
    assert res.exit_code == 0
    assert "TR-003|faro|troncal-01|512|EN_COLA" in res.stdout


def test_abrir_ch5_e2_caducado_cat_falla():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=False)
    assert r["abrible"] is True
    sess = r["session"]
    res = sess.ejecutar("cat /tmp/volcado-custodia.csv")
    assert res.exit_code != 0
    assert "No such file" in (res.stderr + res.stdout)


def test_volcado_condicional_e1():
    cur = load_curriculum()
    # rescatado → testigo presente
    r = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    res = r["session"].ejecutar("cat /tmp/volcado-custodia.csv")
    assert res.exit_code == 0
    assert "TR-003" in res.stdout
    # caducado → ausencia honesta
    r2 = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=False)
    assert r2["abrible"] is True
    res2 = r2["session"].ejecutar("cat /tmp/volcado-custodia.csv")
    assert res2.exit_code == 1
    assert "No such file" in (res2.stderr + res2.stdout)


def test_volcado_condicional_e4():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=99, volcado_rescatado=True)
    assert r["abrible"] is True
    res = r["session"].ejecutar("cat /tmp/volcado-custodia.csv")
    assert res.exit_code == 0
    assert "TR-003|faro|troncal-01|512|EN_COLA" in res.stdout
    r2 = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=99, volcado_rescatado=False)
    assert r2["abrible"] is True
    res2 = r2["session"].ejecutar("cat /tmp/volcado-custodia.csv")
    assert res2.exit_code == 1
    assert "No such file" in (res2.stderr + res2.stdout)


def test_volcado_condicional_e3():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=10, volcado_rescatado=True)
    assert r["abrible"] is True
    assert r["session"].ejecutar("cat /tmp/volcado-custodia.csv").exit_code == 0
    r2 = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=10, volcado_rescatado=False)
    assert r2["abrible"] is True
    assert r2["session"].ejecutar("cat /tmp/volcado-custodia.csv").exit_code == 1


def test_ch5_determinismo_x2_seeds():
    cur = load_curriculum()
    # seed 42 byte-idéntico rescatado
    r1 = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=True)
    r2 = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=True)
    assert r1["session"].incursion.room.fs.to_dict() == r2["session"].incursion.room.fs.to_dict()
    # seed 99 byte-idéntico caducado
    r3 = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=99, volcado_rescatado=False)
    r4 = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=99, volcado_rescatado=False)
    assert r3["session"].incursion.room.fs.to_dict() == r4["session"].incursion.room.fs.to_dict()
    # rescatado vs caducado difieren en misma seed
    assert r1["session"].incursion.room.fs.to_dict() != abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=False)["session"].incursion.room.fs.to_dict()
    # determinismo directo del generador (AC del plan)
    assert generate(42, 5, volcado_rescatado=True).room.fs.to_dict() == generate(42, 5, volcado_rescatado=True).room.fs.to_dict()
    assert generate(99, 5, volcado_rescatado=False).room.fs.to_dict() == generate(99, 5, volcado_rescatado=False).room.fs.to_dict()
    assert generate(42, 5, volcado_rescatado=True).room.fs.to_dict() != generate(42, 5, volcado_rescatado=False).room.fs.to_dict()


def test_volcado_del_save_helper():
    assert volcado_del_save({"volcado": "rescatado"}) is True
    assert volcado_del_save({"volcado": "caducado"}) is False
    assert volcado_del_save({}) is False
    assert volcado_del_save(None) is False
    assert volcado_del_save({"volcado": "rescatado", "extra": 1}) is True
