"""test_ch5_e2_grep_intruso.py — O1 24/09 E2 «grep del intruso».

AC del plan 24/09:
- e2 abrible con prereqs (c.cat,c.grep,c.scp), missing ['c.grep'] honesto sin él
- grep censo exit 0 1 línea vía abrir_encargo (pipe ps aux | grep censo)
- grep ceniza exit 1 (motivo derecho)
- frontera 127 honesta (chmod/kill en e2 →127)
- base e2 {'cat','scp'} intacta (<=)
- determinismo ×2 seeds byte-idéntico
- bundle regen, CUSTODIA intacta
"""

from core.curriculum import load_curriculum
from core.engine.session import _commands_for, abrir_encargo
from core.sandbox.shell import DEFAULT_CH5E2_COMMANDS, DEFAULT_CH5_COMMANDS


def test_e2_requires_incluye_grep():
    cur = load_curriculum()
    q = cur.quest("story.ch5.e2")
    assert set(q.requires) == {"c.cat", "c.grep", "c.scp"}
    assert "c.grep" in q.requires


def test_e2_missing_grep_honesto():
    cur = load_curriculum()
    # sin c.grep → no abrible, missing honesto solo c.grep
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=1)
    assert r["abrible"] is False
    assert r["missing"] == ["c.grep"]
    assert r["requires"] == tuple(sorted(["c.cat", "c.grep", "c.scp"]))
    # sin nada → missing los tres
    r2 = abrir_encargo(cur, "story.ch5.e2", set(), run_seed=1)
    assert r2["abrible"] is False
    assert sorted(r2["missing"]) == ["c.cat", "c.grep", "c.scp"]


def test_e2_abrible_con_grep():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    assert "session" in r
    sess = r["session"]
    assert sess.shell.available_commands == {"cat", "scp", "ps", "grep"}
    assert {"cat", "scp"} <= sess.shell.available_commands
    assert set(DEFAULT_CH5_COMMANDS) <= set(DEFAULT_CH5E2_COMMANDS)
    assert set(DEFAULT_CH5E2_COMMANDS) == {"cat", "scp", "ps", "grep"}


def test_e2_grep_censo_via_pipe_exit0_1linea():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=True)
    sess = r["session"]
    # ps aux solo → debe contener intruso censo
    res_ps = sess.ejecutar("ps aux")
    assert res_ps.exit_code == 0
    assert "intruso --vigilar-censo" in res_ps.stdout
    assert "censo" in res_ps.stdout
    # pipe con grep censo → 1 línea, exit 0
    res = sess.ejecutar("ps aux | grep censo")
    assert res.exit_code == 0, f"stdout={res.stdout!r} stderr={res.stderr!r}"
    lines = [l for l in res.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, f"esperaba 1 línea, got {lines!r}"
    assert "censo" in lines[0]
    assert "intruso" in lines[0]
    # variante -i también casa (SEVA veterano, ya soportado en texto.py)
    res_i = sess.ejecutar("ps aux | grep -i CENSO")
    assert res_i.exit_code == 0
    assert "censo" in res_i.stdout.lower()


def test_e2_grep_ceniza_exit1_motivo_derecho():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=True)
    sess = r["session"]
    res = sess.ejecutar("ps aux | grep ceniza")
    assert res.exit_code == 1, f"grep ceniza debe dar 1 (ninguna línea), got {res.exit_code} stdout={res.stdout!r}"
    assert res.stdout.strip() == ""
    # grep ceniza directo sobre fichero inexistente? prueba grep ceniza sin pipe = busca en stdin vacío → 1
    res2 = sess.ejecutar("ps aux | grep -i Ceniza")
    assert res2.exit_code == 1


def test_e2_frontera_127_chmod_kill():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=True)
    sess = r["session"]
    assert sess.ejecutar("chmod 600 /tmp/x").exit_code == 127
    assert sess.ejecutar("kill 1").exit_code == 127
    assert "command not found" in sess.ejecutar("chmod 600 /tmp/x").stderr
    # ps y grep sí permitidos
    assert sess.ejecutar("ps aux | grep censo").exit_code == 0


def test_e2_grep_directo_sobre_ps_output():
    """grep censo también funciona leyendo de stdin aunque se pruebe grep censo sin fichero."""
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=99, volcado_rescatado=False)
    sess = r["session"]
    res = sess.ejecutar("ps aux | grep censo")
    assert res.exit_code == 0
    assert "03:14" in res.stdout  # firma horaria del intruso, misma que el volcado


def test_e2_determinismo_seed():
    cur = load_curriculum()
    r1 = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=True)
    r2 = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=42, volcado_rescatado=True)
    assert r1["session"].incursion.room.fs.to_dict() == r2["session"].incursion.room.fs.to_dict()
    # pipe idempotente
    res1 = r1["session"].ejecutar("ps aux | grep censo")
    res2 = r2["session"].ejecutar("ps aux | grep censo")
    assert res1.stdout == res2.stdout
    assert res1.exit_code == res2.exit_code
    # seed distinta → pid distinto pero misma firma censo/03:14
    r3 = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp", "c.grep"}, run_seed=99, volcado_rescatado=True)
    res3 = r3["session"].ejecutar("ps aux | grep censo")
    assert res3.exit_code == 0
    assert "censo" in res3.stdout


def test_e2_hint_texto_presente():
    from data.textos import load_textos
    t = load_textos()
    assert "story.ch5.e2.hint_2" in t
    hint = t["story.ch5.e2.hint_2"]
    assert "grep censo" in hint
    assert "ceniza" in hint
    assert "grep -i" in hint.lower()

