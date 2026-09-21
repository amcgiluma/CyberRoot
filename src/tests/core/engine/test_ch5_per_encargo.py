"""test_ch5_per_encargo.py — T1 (🧭44) cableado _commands_for per-encargo.

Verifica que `session._commands_for(5, quest_id)` ramifica a las allowlists
per-encargo (patrón CH4E3, 14/09) y que `abrir_encargo` expone la física
prometida en 05-subestacion.md.

- e3 → {cat,env,kill,ps,scp} y ps aux → 0 con intruso censo --vigilar-censo START 03:14
- e1 → ls/chmod → 0
- e4 → chmod/chown/tail → 0
- e2 → (cat,scp) intacta
"""
from __future__ import annotations

import re

from core.curriculum import load_curriculum
from core.engine.session import _commands_for, abrir_encargo
from core.sandbox.shell import DEFAULT_CH5_COMMANDS, DEFAULT_CH5E1_COMMANDS, DEFAULT_CH5E3_COMMANDS, DEFAULT_CH5E4_COMMANDS


def test_commands_for_per_encargo_ramifica():
    assert _commands_for(5) == ("cat", "scp")
    assert _commands_for(5, "story.ch5.e2") == ("cat", "scp")
    assert set(_commands_for(5, "story.ch5.e1")) == set(DEFAULT_CH5E1_COMMANDS)
    assert set(_commands_for(5, "story.ch5.e3")) == set(DEFAULT_CH5E3_COMMANDS)
    assert set(_commands_for(5, "story.ch5.e4")) == set(DEFAULT_CH5E4_COMMANDS)
    # Forma <= en tests (allowlist check)
    assert set(DEFAULT_CH5_COMMANDS) <= set(_commands_for(5, "story.ch5.e3"))
    assert "ps" in _commands_for(5, "story.ch5.e3")
    assert "env" in _commands_for(5, "story.ch5.e3")


def test_e3_ps_aux_jugable_por_puerta():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    sess = r["session"]
    # forma <= en tests
    assert sess.shell.available_commands <= set(DEFAULT_CH5E3_COMMANDS)
    assert sess.shell.available_commands == {"cat", "env", "kill", "ps", "scp"}
    res = sess.ejecutar("ps aux")
    assert res.exit_code == 0
    assert "intruso --vigilar-censo" in res.stdout
    assert "03:14" in res.stdout
    assert re.search(r"censo\s+\d+", res.stdout)
    # seed 99 también jugable (pid distinto pero misma firma)
    r2 = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=99, volcado_rescatado=True)
    res2 = r2["session"].ejecutar("ps aux")
    assert res2.exit_code == 0
    assert "intruso --vigilar-censo" in res2.stdout
    assert "03:14" in res2.stdout


def test_e1_ls_chmod_jugable():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    sess = r["session"]
    assert sess.shell.available_commands == set(DEFAULT_CH5E1_COMMANDS)
    assert sess.ejecutar("ls").exit_code == 0
    assert sess.ejecutar("chmod 600 /tmp/volcado-custodia.csv").exit_code == 0


def test_e4_chmod_chown_tail_jugable():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    sess = r["session"]
    assert sess.shell.available_commands == set(DEFAULT_CH5E4_COMMANDS)
    assert sess.ejecutar("chmod 600 /tmp/volcado-custodia.csv").exit_code == 0
    assert sess.ejecutar("chown operator:operator /tmp/volcado-custodia.csv").exit_code == 0
    assert sess.ejecutar("tail /tmp/volcado-custodia.csv").exit_code == 0


def test_e2_intacta_cat_scp():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e2", {"c.cat", "c.scp"}, run_seed=42, volcado_rescatado=True)
    assert r["abrible"] is True
    sess = r["session"]
    assert sess.shell.available_commands == {"cat", "scp"}
    assert sess.ejecutar("ps aux").exit_code == 127
