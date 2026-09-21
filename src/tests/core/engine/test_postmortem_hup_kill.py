"""test_postmortem_hup_kill.py — T2 (P1) huella kármica del vigilante.

Detector en postmortem.py: kill -HUP <pid> sobre intruso --vigilar-censo
→ postmortem.auditor.hup + micro-karma azul; kill -9 → postmortem.auditor.kill + rojo.
Lee fs.environment[HUP_*] + ausencia del intruso en ps.

AC: HUP → línea + karma azul; -9 → línea + rojo; sin kill byte-idéntico; e1/e4 sin falsa detección.
"""
from __future__ import annotations

import re

from core.curriculum import load_curriculum
from core.engine.session import abrir_encargo
from core.engine import build_postmortem
from core.engine.postmortem import LINE_KEY_HUP, LINE_KEY_KILL


def _pid_de_ps(stdout: str) -> str:
    m = re.search(r"censo\s+(\d+).*intruso --vigilar-censo", stdout)
    assert m, f"no se encontró pid del intruso en ps aux: {stdout[:500]!r}"
    return m.group(1)


def test_hup_linea_y_karma_azul():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=42, volcado_rescatado=True)
    sess = r["session"]
    pid = _pid_de_ps(sess.ejecutar("ps aux").stdout)
    assert sess.ejecutar(f"kill -HUP {pid}").exit_code == 0
    # el env marca HUP y el ps sigue con --reloaded
    assert f"HUP_{pid}" in sess.shell.fs.environment
    assert "--reloaded" in sess.ejecutar("ps aux").stdout
    pm = build_postmortem(sess.shell_dict(), sess.state())
    assert "auditor_hup" in pm
    assert pm["auditor_hup"]["line_key"] == LINE_KEY_HUP
    assert "auditor_hup_text" in pm
    assert "reconfiguraci" in pm["auditor_hup_text"]
    assert pm["auditor_hup_text"] in pm["lines_resolved"]
    assert pm.get("karma_tint") == "blue"
    assert pm.get("karma") == {"delta": 1, "tint": "blue"}
    assert pm.get("karma_delta") == 1
    # no debe aparecer kill
    assert "auditor_kill" not in pm


def test_kill_linea_y_karma_rojo():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=42, volcado_rescatado=True)
    sess = r["session"]
    pid = _pid_de_ps(sess.ejecutar("ps aux").stdout)
    assert sess.ejecutar(f"kill -9 {pid}").exit_code == 0
    assert "intruso --vigilar-censo" not in sess.ejecutar("ps aux").stdout
    pm = build_postmortem(sess.shell_dict(), sess.state())
    assert "auditor_kill" in pm
    assert pm["auditor_kill"]["line_key"] == LINE_KEY_KILL
    assert "auditor_kill_text" in pm
    assert "eliminado" in pm["auditor_kill_text"] or "vigilancia" in pm["auditor_kill_text"]
    assert pm["auditor_kill_text"] in pm["lines_resolved"]
    assert pm.get("karma_tint") == "red"
    assert pm.get("karma") == {"delta": 1, "tint": "red"}
    assert "auditor_hup" not in pm


def test_sin_kill_byte_identico_sin_hup_kill():
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=42, volcado_rescatado=True)
    sess = r["session"]
    sess.ejecutar("ps aux")
    sess.ejecutar("cat /tmp/volcado-custodia.csv")
    pm = build_postmortem(sess.shell_dict(), sess.state())
    assert "auditor_hup" not in pm
    assert "auditor_hup_text" not in pm
    assert "auditor_kill" not in pm
    assert "auditor_kill_text" not in pm
    assert "karma" not in pm
    assert "karma_delta" not in pm
    assert "karma_tint" not in pm


def test_e1_e4_sin_falsa_deteccion():
    cur = load_curriculum()
    # e1 sin kill
    r1 = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=42, volcado_rescatado=True)
    sess1 = r1["session"]
    sess1.ejecutar("ls")
    sess1.ejecutar("ps aux")
    pm1 = build_postmortem(sess1.shell_dict(), sess1.state())
    assert "auditor_hup" not in pm1
    assert "auditor_kill" not in pm1
    # e4 sin kill
    r4 = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=42, volcado_rescatado=True)
    sess4 = r4["session"]
    sess4.ejecutar("ls")
    pm4 = build_postmortem(sess4.shell_dict(), sess4.state())
    assert "auditor_hup" not in pm4
    assert "auditor_kill" not in pm4


def test_hup_vs_kill_disjuntos_prefijo():
    # prefijo disjunto: postmortem.auditor.hup / .kill no colisionan con existentes
    assert LINE_KEY_HUP.startswith("postmortem.auditor.")
    assert LINE_KEY_KILL.startswith("postmortem.auditor.")
    assert LINE_KEY_HUP != LINE_KEY_KILL
    # textos resuelven
    from data.textos import load_textos, resolve
    textos = load_textos()
    assert resolve(LINE_KEY_HUP, {}, textos) != LINE_KEY_HUP
    assert resolve(LINE_KEY_KILL, {}, textos) != LINE_KEY_KILL
