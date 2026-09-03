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
    """Con credencial LEÍDA, `sudo cat <credencial>` ejecuta y emite."""
    shell = _shell()
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")  # ganarse la llave (S1 03/09)
    res = shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    assert res.exit_code == 0, res.stderr
    assert SUDO_AUTHZ_MARKER in res.stdout  # el comando envuelto SÍ se ejecutó


def test_sudo_ejecutado_factura_base_mas_premium() -> None:
    """`sudo cat` factura cat(1) + premium sudo(3) = 4 en ruido del sudo."""
    shell = _shell()
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")  # ganarse la llave (S1 03/09)
    res = shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    assert _noise_sum(res) == 4  # base envuelto (1) + premium (3)
    assert shell.total_noise == 1 + 4  # + el cat que ganó la llave
    # El comando base y el wrapper quedan en eventos separados.
    cmds = [ev.data["command"] for ev in res.noise]
    assert cmds == ["cat", "sudo"]


def test_sudo_deja_firma_en_auth_log() -> None:
    """Cada sudo con credencial LEÍDA appenda la firma (usuario+comando+tick)."""
    shell = _shell()
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")  # ganarse la llave (S1 03/09)
    shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
    auth = shell.fs.read_file(AUTH_LOG_PATH)
    assert "operator : sudo cat" in auth
    assert "tick 1" in auth  # el cat previo consumió el tick 0
    # El ruido previo del scaffold se conserva (append, no overwrite).
    assert "session opened" in auth


def test_sudo_comando_envuelto_inexistente_127() -> None:
    """Con credencial LEÍDA pero comando desconocido → `not found` (127)."""
    shell = _shell()
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")  # ganarse la llave (S1 03/09)
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


# ---- gate de LECTURA (S1, 03/09, 🧭14b: el sudo se GANA LEYENDO) -----------

def test_sudo_credencial_sin_leer_rechaza_nombrando_orden() -> None:
    """Credencial PRESENTE pero SIN `cat` previo → rechazo que NOMBRA la
    orden, exit 1, ruido 0 y SIN firma en el auth.log."""
    shell = _shell()
    res = shell.execute("sudo ls")
    assert res.exit_code == 1
    assert _noise_sum(res) == 0
    assert shell.total_noise == 0  # intentar no es delinquir
    assert "not read" in res.stderr
    assert SUDO_CREDENTIAL_PATH in res.stderr  # NOMBRA la orden
    assert "cat " in res.stderr  # y manda leerla
    auth = shell.fs.read_file(AUTH_LOG_PATH)
    assert "sudo" not in auth  # SIN firma: el rechazo no es un delito


def test_cat_relativo_tambien_gana_la_marca() -> None:
    """La marca no exige ruta absoluta: `cat orden-ceniza.txt` desde su
    directorio también GANA la llave (el jugador vive en relativas)."""
    shell = Shell(
        _fs_sudo(),
        commands=DEFAULT_CH3_COMMANDS,
        cwd=SUDO_CREDENTIAL_PATH.rsplit("/", 1)[0],
    )
    r = shell.execute(SUDO_CREDENTIAL_FILE)
    assert r.exit_code == 127  # cordura: sin comando no hay lectura
    r = shell.execute(f"cat {SUDO_CREDENTIAL_FILE}")
    assert r.exit_code == 0
    assert SUDO_CREDENTIAL_PATH in shell.read_marks
    res = shell.execute("sudo ls")
    assert res.exit_code == 0


def test_cat_de_otro_fichero_no_gana_la_marca() -> None:
    """Un fichero AJENO con el marcador NO autoriza: la llave se gana en su
    sitio, no adivinando el texto en otro lado."""
    fs = _fs_sudo()
    # Copia con el marcador en otro sitio: mismo texto, distinto fichero.
    fs.copy_file(SUDO_CREDENTIAL_PATH, "/chuleta.txt")
    shell = Shell(fs, commands=DEFAULT_CH3_COMMANDS)
    r = shell.execute("cat /chuleta.txt")
    assert r.exit_code == 0
    assert shell.read_marks == set()
    res = shell.execute("sudo ls")
    assert res.exit_code == 1


def test_lectura_emite_evento_al_bus_una_sola_vez() -> None:
    """El `cat` que gana la marca publica `event.credential.read` (ruta +
    tick); releer NO re-emite (solo la transición)."""
    from core.common.events import EventBus
    from core.sandbox.commands.escalada import SUDO_READ_EVENT_TYPE

    seen: list = []
    bus = EventBus()
    bus.subscribe(SUDO_READ_EVENT_TYPE, seen.append)
    shell = Shell(_fs_sudo(), commands=DEFAULT_CH3_COMMANDS, bus=bus)
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")  # releer: sin evento
    assert len(seen) == 1
    assert seen[0].data["path"] == SUDO_CREDENTIAL_PATH
    assert seen[0].tick == 0


def test_marca_sobrevive_roundtrip_y_save_viejo_carga_vacio() -> None:
    """La marca viaja en el estado serializable (ida y vuelta exacta); un
    dict de save v1 SIN la clave carga con el set vacío (compatibilidad)."""
    shell = _shell()
    shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")
    d = shell.to_dict()
    assert d["read_marks"] == [SUDO_CREDENTIAL_PATH]
    restored = Shell.from_dict(d)
    assert restored.to_dict() == d
    assert restored.read_marks == {SUDO_CREDENTIAL_PATH}
    # Save viejo (sin la clave): sesión sin lecturas, sin romper nada.
    d_old = {k: v for k, v in d.items() if k != "read_marks"}
    assert Shell.from_dict(d_old).read_marks == set()