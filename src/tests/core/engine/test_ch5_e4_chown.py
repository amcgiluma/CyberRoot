"""test_ch5_e4_chown.py — O1 23/09 díptico E4: chown gris:apagados vs root:root tras ls -l.

AC del plan 23/09:
- abrir_encargo e4 abrible con {c.chmod,c.chown,c.cat,c.grep}
- ls -l + chown gris:apagados → auditor_chown_transfer azul {blue:1}
- ls -l + chown root:root → auditor_chown_retoma rojo {red:1}
- sin ls -l → byte-idéntico sin huella
- sin chown → byte-idéntico sin huella
- coexistencia chmod+chown último manda
- sin falsa detección kill/hup y chmod
- determinismo ×2 seeds y textos resuelven
"""
from __future__ import annotations

from core.curriculum import load_curriculum
from core.engine.session import abrir_encargo
from core.engine import build_postmortem
from core.engine.postmortem import LINE_KEY_CHOWN_TRANSFER, LINE_KEY_CHOWN_RETOMA
from core.generator import generate
from data.textos import load_textos, resolve


def _sess_e4(seed=42, volcado=True):
    cur = load_curriculum()
    r = abrir_encargo(cur, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=seed, volcado_rescatado=volcado)
    assert r["abrible"] is True
    return r["session"]


def test_abrir_e4_abrible_y_owner_operator():
    s = _sess_e4(42, True)
    assert s.shell.available_commands == {"cat", "chmod", "chown", "ls", "scp", "tail"}
    node = s.shell.fs.resolve("/srv/subestacion/sesiones/pts0", "/")
    assert node.owner == "operator"
    assert node.group == "operator"
    assert node.mode == "644"


def test_chown_transfer_azul_y_fs():
    s = _sess_e4(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    assert s.ejecutar("chown gris:apagados /srv/subestacion/sesiones/pts0").exit_code == 0
    node = s.shell.fs.resolve("/srv/subestacion/sesiones/pts0", "/")
    assert node.owner == "gris"
    assert node.group == "apagados"
    pm = build_postmortem(s.shell_dict(), s.state())
    assert pm["auditor_chown_transfer"]["line_key"] == LINE_KEY_CHOWN_TRANSFER
    assert pm["micro_karma"] == {"blue": 1}
    assert pm["karma_tint"] == "blue"
    assert pm["auditor_chown_transfer_text"] in pm["lines_resolved"]


def test_chown_root_retoma_rojo():
    s = _sess_e4(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("chown root:root /srv/subestacion/sesiones/pts0")
    node = s.shell.fs.resolve("/srv/subestacion/sesiones/pts0", "/")
    assert node.owner == "root"
    pm = build_postmortem(s.shell_dict(), s.state())
    assert pm["auditor_chown_retoma"]["line_key"] == LINE_KEY_CHOWN_RETOMA
    assert pm["micro_karma"] == {"red": 1}
    assert pm["karma_tint"] == "red"


def test_sin_ls_l_byte_identico_sin_huella():
    s = _sess_e4(42, True)
    s.ejecutar("chown gris:apagados /srv/subestacion/sesiones/pts0")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert "auditor_chown_transfer" not in pm
    assert "auditor_chown_retoma" not in pm
    assert "micro_karma" not in pm
    assert "karma" not in pm
    # con cat previa pero sin ls -l tampoco
    s2 = _sess_e4(42, True)
    s2.ejecutar("cat /tmp/volcado-custodia.csv")
    s2.ejecutar("chown root:root /srv/subestacion/sesiones/pts0")
    pm2 = build_postmortem(s2.shell_dict(), s2.state())
    assert "auditor_chown_retoma" not in pm2


def test_sin_chown_sin_huella_chown():
    s = _sess_e4(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("cat /tmp/volcado-custodia.csv")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert "auditor_chown_transfer" not in pm
    assert "auditor_chown_retoma" not in pm
    assert "micro_karma" not in pm


def test_coexistencia_chmod_chown_ultimo_manda():
    # chmod 600 luego chown root -> chown gana (rojo)
    s = _sess_e4(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("chmod 600 /srv/subestacion/sesiones/pts0")
    s.ejecutar("chown root:root /srv/subestacion/sesiones/pts0")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert "auditor_chown_retoma" in pm
    assert "auditor_cierre" not in pm
    assert pm["micro_karma"] == {"red": 1}
    # chown gris luego chmod 777 -> chmod gana (rojo)
    s2 = _sess_e4(42, True)
    s2.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s2.ejecutar("chown gris:apagados /srv/subestacion/sesiones/pts0")
    s2.ejecutar("chmod 777 /srv/subestacion/sesiones/pts0")
    pm2 = build_postmortem(s2.shell_dict(), s2.state())
    assert "auditor_puerta_abierta" in pm2
    assert "auditor_chown_transfer" not in pm2
    # último chown gana dentro del mismo verbo
    s3 = _sess_e4(42, True)
    s3.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s3.ejecutar("chown gris:apagados /srv/subestacion/sesiones/pts0")
    s3.ejecutar("chown root:root /srv/subestacion/sesiones/pts0")
    pm3 = build_postmortem(s3.shell_dict(), s3.state())
    assert "auditor_chown_retoma" in pm3
    assert "auditor_chown_transfer" not in pm3


def test_sin_falsa_deteccion_kill_chmod():
    s = _sess_e4(42, True)
    s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s.ejecutar("ps aux")
    pm = build_postmortem(s.shell_dict(), s.state())
    assert "auditor_hup" not in pm
    assert "auditor_kill" not in pm
    assert "auditor_chown_transfer" not in pm
    # chown no dispara cierre
    s2 = _sess_e4(42, True)
    s2.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
    s2.ejecutar("chown gris:apagados /srv/subestacion/sesiones/pts0")
    pm2 = build_postmortem(s2.shell_dict(), s2.state())
    assert "auditor_cierre" not in pm2
    assert "auditor_puerta_abierta" not in pm2


def test_determinismo_x2_seeds():
    assert generate(42, 5, volcado_rescatado=True).room.fs.to_dict() == generate(42, 5, volcado_rescatado=True).room.fs.to_dict()
    assert generate(99, 5, volcado_rescatado=False).room.fs.to_dict() == generate(99, 5, volcado_rescatado=False).room.fs.to_dict()
    assert generate(42, 5, volcado_rescatado=True).room.fs.to_dict() != generate(42, 5, volcado_rescatado=False).room.fs.to_dict()
    textos = load_textos()
    assert resolve(LINE_KEY_CHOWN_TRANSFER, {}, textos) != LINE_KEY_CHOWN_TRANSFER
    assert resolve(LINE_KEY_CHOWN_RETOMA, {}, textos) != LINE_KEY_CHOWN_RETOMA
