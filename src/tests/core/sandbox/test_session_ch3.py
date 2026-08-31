"""S1 (31/08) — Sesión END-TO-END del cap. 3 «Bombas» (subestación del Alto).

Replica el patrón de `test_session_ch2.py` con el FS extendido del cap. 3: la
subestación secundaria con el demonio de la 03:00 y el servicio del censo que
COMPARTEN imagen pero no propietario. La prosa de Manus (post-mortem de Ceniza)
dice justo esto: «los procesos comparten imagen; lo que no comparten es el
propietario. Lee `ps aux`. La diferencia entre los dos cabe en una columna.»

El sandbox es CERO RNG: los procesos son piel del generator (aquí fijos en el
fixture). Comprobamos que `ps` y `ps aux` los reproducen Y que el roundtrip de
la sesión conserva procesos y entorno byte a byte (§1.5).
"""

from __future__ import annotations

from core.sandbox.fs import DirNode, FileNode, FileSystem, Proceso
from core.sandbox.shell import DEFAULT_CH3_COMMANDS, Shell

SUBESTACION = "/srv/subestacion-alto-norte"


def _fs_subestacion() -> FileSystem:
    """Subestación del cap. 3: demonio y servicio con misma imagen, distinto
    user (lo que delata en la prosa de Manus) + un proceso de mantenimiento."""
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
                                            content=(
                                                "PIDFile=/run/demonio-11:04.pid\n"
                                                "User=ceniza\n"
                                                "No apagar hasta nuevo aviso.\n"
                                            ),
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
            Proceso(
                pid=1, user="root",
                cmd="/usr/lib/systemd/systemd --system",
                tty="?", cpu="0.0", mem="0.1", vsz="22288", rss="10888",
                stat="Ss", start="Aug25", time="0:38",
            ),
            Proceso(
                pid=521, user="ceniza",
                cmd="/usr/sbin/demonio-11:04 --ventana",
                tty="?", cpu="0.1", mem="0.2", vsz="12784", rss="2104",
                stat="S", start="11:04", time="11:34:02",
            ),
            Proceso(
                pid=522, user="censo",
                cmd="/usr/sbin/demonio-11:04 --vigilar-censo",
                tty="?", cpu="0.0", mem="0.3", vsz="13100", rss="2440",
                stat="S", start="11:04", time="11:33:58",
            ),
        ),
        environment={
            "LANG": "C.UTF-8",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin",
            "SHELL": "/bin/sh",
            "USER": "operator",
        },
    )


def test_ps_aux_delata_el_propietario_el_hijo_del_hub() -> None:
    """`ps aux` muestra 521(ceniza) y 522(censo): la columna USER es la que
    distingue al demonio gemelo del servicio (prosa de Manus)."""
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    shell.execute(f"cd {SUBESTACION}")
    res = shell.execute("ps aux")
    assert res.exit_code == 0, res.stderr
    lines = res.stdout.splitlines()
    assert lines[0].startswith("USER         PID")
    # Ambos procesos de imagen compartida tienen user DISTINTO (521 ceniza).
    d521 = [l for l in lines if l.startswith("ceniza") and "demonio-11:04" in l]
    d522 = [l for l in lines if l.startswith("censo") and "demonio-11:04" in l]
    assert d521 and d522, res.stdout


def test_ps_compacto_muestra_pids_y_comandos() -> None:
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    res = shell.execute("ps")
    assert res.exit_code == 0
    assert "    PID TTY          TIME CMD" == res.stdout.splitlines()[0]
    assert "demonio-11:04" in res.stdout
    assert len(res.stdout.splitlines()) == 4  # cabecera + 3 procesos


def test_env_muestra_las_variables_de_la_sesion() -> None:
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    res = shell.execute("env")
    assert res.exit_code == 0
    assert "USER=operator" in res.stdout
    assert "SHELL=/bin/sh" in res.stdout


def test_ruido_de_ps_y_env_1_cada_uno() -> None:
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    shell.execute("ps")
    shell.execute("env")
    assert shell.total_noise == 2


def test_roundtrip_sesion_conserva_procesos_y_entorno() -> None:
    """Ida y vuelta exacta (§1.5): procesos y environment sobreviven."""
    shell = Shell(_fs_subestacion(), host="subestacion-alto-norte", commands=DEFAULT_CH3_COMMANDS)
    shell.execute("cd /srv")
    shell.execute("ps aux")
    d = shell.to_dict()
    restored = Shell.from_dict(d)
    assert restored.to_dict() == d
    assert [p.pid for p in restored.fs.processes] == [1, 521, 522]
    assert restored.fs.environment["USER"] == "operator"


def test_regresion_cap0_y_cap2_no_exponen_ps_env() -> None:
    """Cap. 0 y cap. 2 quedan INTACTOS: en sus sesiones `ps`/`env` NO existen
    (exit 127) — el proceso solo se enseña en el cap. 3 (§6.4.1)."""
    from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS

    fs0 = FileSystem(root=DirNode(name="/", children={"etc": DirNode(name="etc", children={})}))
    s0 = Shell(fs0, commands=DEFAULT_CAP0_COMMANDS)
    r = s0.execute("ps")
    assert r.exit_code == 127
    assert "not found" in r.stderr

    s2 = Shell(fs0, commands=DEFAULT_CH2_COMMANDS)
    r2 = s2.execute("env")
    assert r2.exit_code == 127
    assert "not found" in r2.stderr