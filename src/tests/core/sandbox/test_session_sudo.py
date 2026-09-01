"""S1 (01/09) — Sesión END-TO-END del `sudo` GANADO en la sala del cap. 3.

Replica el patrón de test_session_ch3.py con el FS que O1 (feat/engine, PR
#16) coloca en la sala sudo «Bombas»: credencial narrativa como FICHERO del
mundo (`/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt`, con el
marcador `AUTORIZACION: CENIZA`) y `/var/log/auth.log` presente.

La canónica del cap. 3 (O1) lee la credencial con `cat`; S1 añade la EJECUCIÓN
real: sin llave gana → `sudo` rechaza diegético y accionable; con la llave leída
→ `sudo` eleva el comando, factura ruido premium y DEJA firma en el auth.log
(«el poder deja factura», DESIGN §6.1). Es el circuito completo que Artorias
verifica esta noche en el ensayo de integración contra el generator real.
"""

from __future__ import annotations

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import DEFAULT_CH3_COMMANDS, Shell
from core.sandbox.commands.escalada import (
    AUTH_LOG_PATH,
    SUDO_CREDENTIAL_PATH,
)

SUDO_CREDENTIAL_CONTENT = (
    "ORDEN DE ACCESO — SUBESTACION ALTO NORTE\n"
    "AUTORIZACION: CENIZA\n"
    "Destino: consola del servicio demonio-11:04\n"
    "Alcance: elevacion de privilegios (sudo) durante la ventana de las 11:04\n"
    "Vigencia: esta sesion, y no mas alla\n"
    "Firmado: -C\n"
)
AUTH_LOG_PRE = "11:02 operator : session opened\n11:03 operator : session closed\n"


def _fs_sala_sudo() -> FileSystem:
    """El FS exacto que monta O1 (chapter3.py, PR #16) para la sala sudo."""
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
                                "autorizaciones": DirNode(
                                    name="autorizaciones",
                                    children={
                                        "orden-ceniza.txt": FileNode(
                                            name="orden-ceniza.txt",
                                            content=SUDO_CREDENTIAL_CONTENT,
                                            owner="ceniza",
                                            group="operadores",
                                            mode="644",
                                        ),
                                    },
                                ),
                            },
                        ),
                    },
                ),
                "var": DirNode(
                    name="var",
                    children={
                        "log": DirNode(
                            name="log",
                            children={
                                "auth.log": FileNode(
                                    name="auth.log",
                                    content=AUTH_LOG_PRE,
                                    owner="root",
                                    group="root",
                                    mode="640",
                                ),
                            },
                        ),
                    },
                ),
            },
        ),
    )


def _shell() -> Shell:
    return Shell(
        _fs_sala_sudo(),
        host="subestacion-alto-norte",
        cwd="/srv/subestacion-alto-norte/autorizaciones",
        commands=DEFAULT_CH3_COMMANDS,
    )


def test_canonica_lee_la_credencial_con_cat() -> None:
    """La canónica de O1 (`cat <credencial>`) SÍ lee la llave del mundo."""
    shell = _shell()
    res = shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")
    assert res.exit_code == 0
    assert "AUTORIZACION: CENIZA" in res.stdout
    assert "Firmado: -C" in res.stdout


def test_sin_leer_llave_sudo_rechaza_y_no_firma() -> None:
    """En una sala SIN credencial, ejecutar `sudo` → rechazo diegético y el
    auth.log NO gana la firma (el rechazo no es un delito). La sala sudo de
    O1 SÍ trae credencial; este caso usa un FS limpio para aislar el rechazo.
    (El caso «credencial presente» se cubre en el test de elevación.)"""
    from core.sandbox.commands.escalada import AUTH_LOG_PATH as _AUTH

    fs_limpio = FileSystem()
    shell = Shell(fs_limpio, commands=DEFAULT_CH3_COMMANDS)
    res = shell.execute("sudo cat /etc/shadow")
    assert res.exit_code == 1
    assert "authorization order" in res.stderr
    # El rechazo no crea nada: el FS limpio sigue sin auth.log (sin firma).
    from core.sandbox.fs import FsError

    try:
        fs_limpio.read_file(AUTH_LOG_PATH)
        raised = False
    except FsError:
        raised = True
    assert raised


def test_con_llave_leida_sudo_eleva_y_firma() -> None:
    """Tras leer la llave con `cat`, `sudo` eleva: ejecuta el comando, suma
    ruido premium y appenda la firma al auth.log (columna que delata)."""
    shell = _shell()
    r1 = shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")  # ganarse la llave
    assert r1.exit_code == 0

    res = shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    assert res.exit_code == 0
    # Ruido total: cat(llave 1) + [sudo cat = cat 1 + premium 3].
    assert shell.total_noise == 1 + (1 + 3)
    auth = shell.fs.read_file(AUTH_LOG_PATH)
    assert auth.startswith(AUTH_LOG_PRE)  # append, no overwrite
    assert "operator : sudo cat" in auth


def test_roundtrip_sesion_conserva_credencial_y_firma() -> None:
    """Ida y vuelta (§1.5): la credencial y la firma sobreviven al save."""
    shell = _shell()
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")
    shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    d = shell.to_dict()
    restored = Shell.from_dict(d)
    assert restored.to_dict() == d
    assert "operator : sudo cat" in restored.fs.read_file(AUTH_LOG_PATH)


def test_sudo_de_nuevo_mismo_comando_vuelve_a_firmar() -> None:
    """DOS `sudo` → DOS firmas en el auth.log (reutilizar la llave no borra
    la factura; el poder deja rastro cada vez)."""
    shell = _shell()
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")
    shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    auth = shell.fs.read_file(AUTH_LOG_PATH)
    assert auth.count("sudo cat") == 2