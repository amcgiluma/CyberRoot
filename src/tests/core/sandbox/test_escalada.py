"""S1 (01/09) — `sudo` GANADO: golden de la elevación con credencial narrativa.

Verifica la forma FIRMADA de DESIGN §6.1 sin credencial (rechazo diegético
accionable, ruido 0, exit 1) y con credencial (ejecuta el comando envuelto,
factura ruido PREMIUM sobre el base y deja firma en `/var/log/auth.log`).
El FS reproduce la piel que O1 coloca en la sala sudo del cap. 3 (contrato
O1↔S1: credencial como fichero del mundo + auth.log presente).

Regresión explícita: `sudo` NO existe en cap. 0/2 (exit 127, como `ps`/`env`).
"""

from __future__ import annotations

from core.sandbox.commands.escalada import (
    AUTH_LOG_PATH,
    SUDO_AUTHZ_MARKER,
    SUDO_CREDENTIAL_PATH,
    SUDO_NO_CRED_MSG,
)
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS, DEFAULT_CH3_COMMANDS, Shell

SUDO_CREDENTIAL_FILE = SUDO_CREDENTIAL_PATH.rsplit("/", 1)[-1]
SRAIZ = SUDO_CREDENTIAL_PATH.rsplit("/", 3)[0]  # /srv/subestacion-alto-norte


def _fs_sudo(codigo_filename: str = SUDO_CREDENTIAL_FILE) -> FileSystem:
    """Piel de la sala sudo del cap. 3 (como la monta O1, PR #16): credencial
    narrativa en `SUDO_CREDENTIAL_PATH` + `auth.log` presente y con ruido."""
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
                                        codigo_filename: FileNode(
                                            name=codigo_filename,
                                            content=(
                                                "ORDEN DE ACCESO — SUBESTACION ALTO NORTE\n"
                                                f"{SUDO_AUTHZ_MARKER}\n"
                                                "Destino: consola del servicio demonio-11:04\n"
                                                "Alcance: elevacion de privilegios (sudo)\n"
                                                "Firmado: -C\n"
                                            ),
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
                                    content="11:02 operator : session opened\n",
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
    return Shell(_fs_sudo(), commands=DEFAULT_CH3_COMMANDS, cwd=SRAIZ)


def _noise_sum(res) -> int:
    return sum(int(ev.data["amount"]) for ev in res.noise)


# ---- sin credencial -------------------------------------------------------

def test_sudo_sin_credencial_rechaza_diegetico_sin_ruido() -> None:
    """FS sin credencial: `sudo cat ...` → rechazo accionable, exit 1, ruido 0."""
    fs = FileSystem()
    shell = Shell(fs, commands=DEFAULT_CH3_COMMANDS)
    res = shell.execute("sudo cat /etc/shadow")
    assert res.exit_code == 1
    assert res.ok is False
    assert _noise_sum(res) == 0
    assert shell.total_noise == 0  # intentar no es delinquir
    # Accionable: NOMBRA qué falta y dónde vive.
    assert "authorization order" in res.stderr
    assert SUDO_CREDENTIAL_PATH in res.stderr
    assert "cat " in res.stderr


def test_sudo_credencial_sin_marcador_no_autoriza() -> None:
    """Fichero en la ruta PERO sin el marcador → no autoriza (llave falsa)."""
    fs = FileSystem(
        root=DirNode(name="/", children={
            "srv": DirNode(name="srv", children={
                "subestacion-alto-norte": DirNode(name="subestacion-alto-norte", children={
                    "autorizaciones": DirNode(name="autorizaciones", children={
                        SUDO_CREDENTIAL_FILE: FileNode(
                            name=SUDO_CREDENTIAL_FILE,
                            content="ORDEN REVOCADA — no vale\n",
                        ),
                    }),
                }),
            }),
        }),
    )
    shell = Shell(fs, commands=DEFAULT_CH3_COMMANDS)
    res = shell.execute("sudo ls")
    assert res.exit_code == 1
    assert _noise_sum(res) == 0


def test_sudo_sin_comando_uso() -> None:
    shell = _shell()
    res = shell.execute("sudo")
    assert res.exit_code == 1
    assert "command" in res.stderr


# ---- con credencial -------------------------------------------------------

def test_sudo_con_credencial_ejecuta_envuelto() -> None:
    """Con credencial, `sudo cat <credencial>` ejecuta y emite el contenido."""
    shell = _shell()
    res = shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    assert res.exit_code == 0, res.stderr
    assert SUDO_AUTHZ_MARKER in res.stdout  # el comando envuelto SÍ se ejecutó


def test_sudo_ejecutado_factura_base_mas_premium() -> None:
    """`sudo cat` factura cat(1) + premium sudo(3) = 4 en ruido total."""
    shell = _shell()
    res = shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    assert _noise_sum(res) == 4  # base envuelto (1) + premium (3)
    assert shell.total_noise == 4
    # El comando base y el wrapper quedan en eventos separados.
    cmds = [ev.data["command"] for ev in res.noise]
    assert cmds == ["cat", "sudo"]


def test_sudo_deja_firma_en_auth_log() -> None:
    """Cada sudo con credencial appenda la firma (usuario+comando+tick)."""
    shell = _shell()
    shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    auth = shell.fs.read_file(AUTH_LOG_PATH)
    assert "operator : sudo cat" in auth
    assert "tick 0" in auth
    # El ruido previo del scaffold se conserva (append, no overwrite).
    assert "session opened" in auth


def test_sudo_comando_envuelto_inexistente_127() -> None:
    """Con credencial pero comando desconocido → `command not found` (127)."""
    shell = _shell()
    res = shell.execute("sudo nosuchcmd x")
    assert res.exit_code == 127
    assert "not found" in res.stderr


# ---- gate por capítulo ----------------------------------------------------

def test_regresion_sudo_no_existe_cap0_cap2() -> None:
    """Cap. 0 y cap. 2: `sudo` NO existe (exit 127) — la elevación se enseña
    en el cap. 3. Mismo patrón que `ps`/`env` (test_session_ch3)."""
    fs = _fs_sudo()
    s0 = Shell(fs, commands=DEFAULT_CAP0_COMMANDS)
    r = s0.execute("sudo ls")
    assert r.exit_code == 127
    assert "not found" in r.stderr

    s2 = Shell(fs, commands=DEFAULT_CH2_COMMANDS)
    r2 = s2.execute("sudo ls")
    assert r2.exit_code == 127


def test_sudo_ruido_premium_constante_documentada() -> None:
    from core.sandbox.commands.escalada import SUDO_PREMIUM_NOISE
    assert SUDO_PREMIUM_NOISE == 3