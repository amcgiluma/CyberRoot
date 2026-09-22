"""test_ch5_e1_cierre.py — O1 22/09 díptico E1: chmod 600 vs 777 tras ls -l.

AC del plan 22/09:
- abrir_encargo e1 abrible con {c.ls-la,c.cat,c.chmod}
- chmod 600 tras ls -l → auditor_cierre azul {blue:1} + ls -l confirma -rw-------
- chmod 777 / -R 777 → auditor_puerta_abierta rojo {red:1}
- sin chmod → byte-idéntico sin huella (sin cierre/puerta/karma)
- e1 sin falsa detección kill/hup
- determinismo ×2 seeds
- textos resuelven
"""
from __future__ import annotations

from core.curriculum import load_curriculum
from core.engine.session import abrir_encargo
from core.engine import build_postmortem
from core.engine.postmortem import LINE_KEY_CIERRE, LINE_KEY_PUERTA_ABIERTA
from core.generator import generate
from data.textos import load_textos, resolve


def _sess_e1(seed=42, volcado=True):
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=seed, volcado_rescatado=volcado)
    assert r["abrible"] is True
    return r["session"]


def test_abrir_e1_abrible_y_modo_644():
    s = _sess_e1(42, True)
    assert s.shell.available_commands == {"cat", "chmod", "kill", "ls", "ps", "scp"}
    node = s.shell.fs.resolve("/srv/subestacion/sesiones/pts0", "/")
    assert node.mode == "644"
    res = s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    assert res.exit_code == 0
    assert "-rw-r--r--" in res.stdout


def test_chmod_600_cierre_azul_y_ls_rw():
    s = _sess_e1(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    assert s.ejecutar("chmod 600 /srv/subestacion/sesiones/pts0").exit_code == 0
    node = s.shell.fs.resolve("/srv/subestacion/sesiones/pts0", "/")
    assert node.mode == "600"
    assert "-rw-------" in s.ejecutar("ls -l /srv/subestacion/sesiones/pts0").stdout
    pm = build_postmortem(s.shell_dict(), s.state())
    assert pm["auditor_cierre"]["line_key"] == LINE_KEY_CIERRE
    assert pm["micro_karma"] == {"blue": 1}
    assert pm["karma_tint"] == "blue"
    assert pm["auditor_cierre_text"] in pm["lines_resolved"]


def test_chmod_777_puerta_roja():
    s = _sess_e1(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("chmod 777 /srv/subestacion/sesiones/pts0")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert pm["auditor_puerta_abierta"]["line_key"] == LINE_KEY_PUERTA_ABIERTA
    assert pm["micro_karma"] == {"red": 1}
    assert pm["karma_tint"] == "red"


def test_chmod_R_777_puerta_roja():
    s = _sess_e1(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("chmod -R 777 /srv/subestacion/sesiones/pts0")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert "auditor_puerta_abierta" in pm
    assert pm["micro_karma"] == {"red": 1}


def test_sin_chmod_byte_identico_sin_huella():
    s = _sess_e1(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("cat /tmp/volcado-custodia.csv")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert "auditor_cierre" not in pm
    assert "auditor_puerta_abierta" not in pm
    assert "micro_karma" not in pm
    assert "karma" not in pm
    # sin ls -l tampoco dispara aunque haya chmod
    s2 = _sess_e1(42, True)
    s2.ejecutar("chmod 600 /srv/subestacion/sesiones/pts0")
    pm2 = build_postmortem(s2.shell_dict(), s2.state())
    assert "auditor_cierre" not in pm2


def test_e1_sin_falsa_deteccion_kill_hup():
    s = _sess_e1(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("ps aux")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert "auditor_hup" not in pm
    assert "auditor_kill" not in pm


def test_determinismo_x2_seeds():
    assert generate(42, 5, volcado_rescatado=True).room.fs.to_dict() == generate(42, 5, volcado_rescatado=True).room.fs.to_dict()
    assert generate(99, 5, volcado_rescatado=False).room.fs.to_dict() == generate(99, 5, volcado_rescatado=False).room.fs.to_dict()
    assert generate(42, 5, volcado_rescatado=True).room.fs.to_dict() != generate(42, 5, volcado_rescatado=False).room.fs.to_dict()
    textos = load_textos()
    assert resolve(LINE_KEY_CIERRE, {}, textos) != LINE_KEY_CIERRE
    assert resolve(LINE_KEY_PUERTA_ABIERTA, {}, textos) != LINE_KEY_PUERTA_ABIERTA
