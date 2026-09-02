"""test_session_kill.py — sesión end-to-end del cap. 3 con `kill` (S1, 02/09).

Replica el patrón de `test_session_ch3.py` pero ejercita la física de
`kill` sobre el par ceniza-521/censo-522: -9 mata (desaparece de `ps`),
-HUP reinicia con config distinta (visible en `ps` y `env`). Gate 127
intacto en cap. 0/2, roundtrip conserva procesos mutados.
"""

from __future__ import annotations

from core.sandbox.fs import DirNode, FileNode, FileSystem, Proceso
from core.sandbox.shell import DEFAULT_CH3_COMMANDS, Shell

SUBESTACION = "/srv/subestacion-alto-norte"


def _fs_subestacion() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "subestacion-alto-norte": DirNode(
                            name="subestacion-alto-norte",
                            children={
                                "config": DirNode(
                                    name="config",
                                    children={
                                        "servicio-demonio.conf": FileNode(
                                            name="servicio-demonio.conf",
                                            content="PIDFile=/run/demonio-11:04.pid\nUser=ceniza\n",
                                        ),
                                    },
                                ),
                            },
                        )
                    },
                ),
            },
        ),
        processes=(
            Proceso(pid=1, user="root", cmd="/usr/lib/systemd/systemd --system", tty="?", cpu="0.0", mem="0.1", vsz="22288", rss="10888", stat="Ss", start="Aug25", time="0:38"),
            Proceso(pid=521, user="ceniza", cmd="/usr/sbin/demonio-11:04 --ventana", tty="?", cpu="0.1", mem="0.2", vsz="12784", rss="2104", stat="S", start="11:04", time="11:34:02"),
            Proceso(pid=522, user="censo", cmd="/usr/sbin/demonio-11:04 --vigilar-censo", tty="?", cpu="0.0", mem="0.3", vsz="13100", rss="2440", stat="S", start="11:04", time="11:33:58"),
        ),
        environment={"LANG": "C.UTF-8", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin", "SHELL": "/bin/sh", "USER": "operator"},
    )


def test_kill_9_vs_hup_observables_en_ps() -> None:
    """-9 mata (desaparece), -HUP reinicia (sigue pero con --reloaded)."""
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    # -9 mata 522
    r = shell.execute("kill -9 522")
    assert r.exit_code == 0, r.stderr
    ps = shell.execute("ps aux").stdout
    assert "censo" not in ps or "demonio-11:04 --vigilar-censo" not in ps  # 522 gone
    assert "ceniza" in ps  # 521 still

    # HUP sobre 521 lo mantiene pero con marca
    r2 = shell.execute("kill -HUP 521")
    assert r2.exit_code == 0, r2.stderr
    ps2 = shell.execute("ps aux").stdout
    assert "--reloaded" in ps2
    assert "ceniza" in ps2
    env = shell.execute("env").stdout
    assert "HUP_521=1" in env


def test_kill_hup_env_visible_y_ps_cambia_stat() -> None:
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    shell.execute("kill -HUP 522")
    # env delata el reload
    env = shell.execute("env").stdout
    assert "HUP_522=1" in env
    # ps muestra cmd reloaded y stat R
    ps = shell.execute("ps aux").stdout
    line = [l for l in ps.splitlines() if l.startswith("censo") and "522" in l][0]
    assert "--reloaded" in line
    assert " R " in line or "R" in line.split()[7]  # stat column


def test_kill_roundtrip_conserva_mutacion() -> None:
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    shell.execute("kill -9 522")
    shell.execute("kill -HUP 521")
    d = shell.to_dict()
    restored = Shell.from_dict(d)
    assert restored.to_dict() == d
    assert [p.pid for p in restored.fs.processes] == [1, 521]
    assert any("reloaded" in p.cmd for p in restored.fs.processes)
    assert restored.fs.environment.get("HUP_521") == "1"


def test_kill_gate_127_cap0_y_no_ps_sin_kill() -> None:
    from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS
    fs = _fs_subestacion()
    s0 = Shell(fs, commands=DEFAULT_CAP0_COMMANDS)
    assert s0.execute("kill 521").exit_code == 127
    s2 = Shell(fs, commands=DEFAULT_CH2_COMMANDS)
    assert s2.execute("kill -HUP 521").exit_code == 127
