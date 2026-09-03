"""chapter3.py — la piel de la sala sudo del cap. 3 «Bombas» como DATOS (hoja).

HOJA (leaf) igual que `chapter0.py`/`chapter2.py`: solo constantes + la
constructora del FS. NO importa `core.generator.model` (para que `model.py`
pueda importarla sin ciclo).

Materializa la forma FIRMADA de Gwyn (DESIGN §6.1, O1 del plan 01/09): el
`sudo` GANADO del cap. 3 es una CREDENCIAL NARRATIVA, nunca una contraseña
tecleada. Como objeto del mundo de la red simulada (filosofía «hosts como
FS»), la credencial se materializa como FICHERO del FS de la sala, que se
LEE con comandos que ya existen (`cat`), no como un flag invisible del
estado.

═══ CONTRATO O1↔S1 (compartir, no importar) ═══════════════════════════════
El sandbox NO importa del generator (dependencia prohibida, ARCHITECTURE
§2); el contrato es una CONVENCIÓN por literales compartidos que Artorias
verifica en el ensayo de integración de esta noche:

  - S1 (`feat/sandbox`) hace que `sudo` lea la credencial como fichero del
    FS de la sala ubicado en `SUDO_CREDENTIAL_PATH`. Presencia + fichero de
    texto (se detecta por la ruta convencional, como acordó Gwyndolin en el
    plan 01/09: «filcreación-credencial + auth.log»).
  - S1 hace que cada `sudo` AÑADA una línea de firma a `AUTH_LOG_PATH`
    (usuario, comando, tick) — «el poder deja factura» y su columna USER.
  - O1 (este fichero) COLOCA ambos: la credencial en `SUDO_CREDENTIAL_PATH`
    y el `auth.log` (con el ruido previo del scaffold) en `AUTH_LOG_PATH`.

Si estas dos rutas cambian, cambia AQUÍ y en `feat/sandbox` (S1) A LA VEZ;
Artorias verifica la coincidencia de literales en el gate.
═══════════════════════════════════════════════════════════════════════════

Sin random, sin reloj real. `fs_rng` se acepta por firma para el
determinismo futuro (mismo convenio que los otros capítulos); en v0 se
ignora.
"""

from __future__ import annotations

from typing import Any

from core.sandbox.fs import DirNode, FileNode, FileSystem, Proceso

# ---------------------------------------------------------------------------
# CONTRATO O1↔S1: rutas de la credencial y del auth.log (ver cabecera)
# ---------------------------------------------------------------------------

#: Nodo del cap. 3 (subestación secundaria del Alto, coherente con la piel de
#: `test_session_ch3.py`): host donde vive la credencial ganada.
CAP3_NODE_DIR = "/srv/subestacion-alto-norte"

#: Directorio de autorizaciones (relativo a CAP3_NODE_DIR): la credencial es
#: un objeto del mundo, en un sitio legible con `ls`/`cat`.
AUTORIZACIONES_DIR = "autorizaciones"

#: Nombre del fichero-credencial narrativa (la «orden firmada por Ceniza»).
SUDO_CREDENTIAL_FILE = "orden-ceniza.txt"

#: Ruta ABSOLUTA de la credencial en el FS de la sala (contrato con S1).
SUDO_CREDENTIAL_PATH = f"{CAP3_NODE_DIR}/{AUTORIZACIONES_DIR}/{SUDO_CREDENTIAL_FILE}"

#: Contenido EXACTO de la credencial: una orden de elevación firmada por
#: Ceniza. Es la credencial NARRATIVA (DESIGN §6.1); NUNCA una contraseña
#: tecleada. Incluye una línea-marcador `AUTORIZACION: CENIZA` para que S1
#: pueda detectarla por contenido además de por la ruta convencional
#: (método «por contenido/ruta» del plan O1/S1).
SUDO_CREDENTIAL_CONTENT = (
    "ORDEN DE ACCESO — SUBESTACION ALTO NORTE\n"
    "AUTORIZACION: CENIZA\n"
    "Destino: consola del servicio demonio-11:04\n"
    "Alcance: elevacion de privilegios (sudo) durante la ventana de las 11:04\n"
    "Vigencia: esta sesion, y no mas alla\n"
    "Firmado: -C\n"
)

#: Directorio de logs del sistema (contrato con S1: firmas de sudo).
AUTH_LOG_DIR = "/var/log"

#: Fichero de `auth.log` del sistema simulado (contrato con S1).
AUTH_LOG_FILE = "auth.log"

#: Ruta ABSOLUTA del `auth.log` donde S1 firmará cada `sudo`.
AUTH_LOG_PATH = f"{AUTH_LOG_DIR}/{AUTH_LOG_FILE}"

#: Ruido previo del bufete del `auth.log` (el scaffold): sesiones de operador
#: normales de antes de la ventana. S1 AÑADE aquí cada firma de sudo.
AUTH_LOG_CONTENT = (
    "11:02 operator : session opened\n"
    "11:03 operator : session closed\n"
)

# ---------------------------------------------------------------------------
# EL DEMONIO (O1, 03/09 — 🧭16 opción a): el par ceniza:521/censo:522
# ---------------------------------------------------------------------------

#: Procesos del cap. 3, réplica EXACTA del FS handmade de
#: `test_session_kill.py` (el golden de la física `kill`): el demonio de la
#: ventana (`ceniza:521 --ventana`) y el servicio del censo que comparte
#: imagen pero no propietario (`censo:522 --vigilar-censo`), más el init.
#: PIEL estática (cero RNG): el generator los inyecta LAZY — solo cuando la
#: quest de la sala requiere `c.ps`/`c.kill` — y el sandbox los renderiza.
CHAPTER3_PROCESSES: tuple[Proceso, ...] = (
    Proceso(
        pid=1, user="root", cmd="/usr/lib/systemd/systemd --system",
        tty="?", cpu="0.0", mem="0.1", vsz="22288", rss="10888",
        stat="Ss", start="Aug25", time="0:38",
    ),
    Proceso(
        pid=521, user="ceniza", cmd="/usr/sbin/demonio-11:04 --ventana",
        tty="?", cpu="0.1", mem="0.2", vsz="12784", rss="2104",
        stat="S", start="11:04", time="11:34:02",
    ),
    Proceso(
        pid=522, user="censo", cmd="/usr/sbin/demonio-11:04 --vigilar-censo",
        tty="?", cpu="0.0", mem="0.3", vsz="13100", rss="2440",
        stat="S", start="11:04", time="11:33:58",
    ),
)

#: Entorno de la sesión del cap. 3 (misma réplica del golden): lo que `env`
#: muestra antes de que `kill -HUP` deje su marca (`HUP_<pid>=1`).
CHAPTER3_ENVIRONMENT: dict[str, str] = {
    "LANG": "C.UTF-8",
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin",
    "SHELL": "/bin/sh",
    "USER": "operator",
}


def build_chapter3_fs(fs_rng: Any, *, with_processes: bool = False) -> FileSystem:
    """Monta el árbol de la sala sudo del cap. 3 «Bombas».

    El FS de la sala contiene SIEMPRE:
      - la credencial narrativa en `SUDO_CREDENTIAL_PATH` (objeto del mundo);
      - el `auth.log` presente en `AUTH_LOG_PATH` (donde S1 firmará cada sudo).

    Con `with_processes=True` inyecta ADEMÁS el demonio (`CHAPTER3_PROCESSES`
    + `CHAPTER3_ENVIRONMENT`): el `ps aux` vacío deja de ser lectura vacía y
    pasa a ser lectura con diana. El generator lo pide LAZY — solo cuando la
    quest de la sala requiere `c.ps`/`c.kill` (O1, plan 03/09).

    La sala concreta se elige de `curriculum.json` (cap. 3) en el generator;
    esta hoja solo aporta la piel.
    """
    _ = fs_rng
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                DIR_SEG: _dir_for_cap3(DIR_SEG) for DIR_SEG in _cap3_dirs()
            },
        ),
        processes=CHAPTER3_PROCESSES if with_processes else (),
        environment=dict(CHAPTER3_ENVIRONMENT) if with_processes else None,
    )


def _cap3_dirs() -> tuple[str, ...]:
    """Segmentos raíz que puebla el cap. 3: `/srv` y `/var`."""
    return ("srv", "var")


def _dir_for_cap3(seg: str) -> DirNode:
    if seg == "srv":
        return DirNode(
            name="srv",
            children={
                "subestacion-alto-norte": DirNode(
                    name="subestacion-alto-norte",
                    children={
                        "autorizaciones": DirNode(
                            name="autorizaciones",
                            children={
                                SUDO_CREDENTIAL_FILE: FileNode(
                                    name=SUDO_CREDENTIAL_FILE,
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
        )
    return DirNode(
        name="var",
        children={
            "log": DirNode(
                name="log",
                children={
                    AUTH_LOG_FILE: FileNode(
                        name=AUTH_LOG_FILE,
                        content=AUTH_LOG_CONTENT,
                        owner="root",
                        group="root",
                        mode="640",
                    ),
                },
            ),
        },
    )


# ---------------------------------------------------------------------------
# Secuencia canónica de la sala sudo (argv crudos, sin acoplar a model)
# ---------------------------------------------------------------------------

#: v0 materialización: leer la credencial con `cat`. La EJECUCIÓN real del
#: `sudo` (elevación sobre un comando envuelto + ruido premium + firma en
#: auth.log) es tarea de S1 (sandbox) y la cubre el ensayo de integración de
#: Artorias esta noche. Como el sandbox aún no expone `sudo`, la validación
#: canónica de HOY verifica que la credencial existe y es legible (el «la
#: llave está en el mundo»); cuando S1 aterrice, la integración prolonga el
#: canon hasta el `sudo` real.
CANON_STEPS_RAW_CH3_SUDO: tuple[tuple[str, ...], ...] = (
    ("cat", SUDO_CREDENTIAL_PATH),
)