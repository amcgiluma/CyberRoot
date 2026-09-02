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

from core.sandbox.fs import DirNode, FileNode, FileSystem

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


def build_chapter3_fs(fs_rng: Any) -> FileSystem:
    """Monta el árbol de la sala sudo del cap. 3 «Bombas».

    El FS de la sala contiene SIEMPRE:
      - la credencial narrativa en `SUDO_CREDENTIAL_PATH` (objeto del mundo);
      - el `auth.log` presente en `AUTH_LOG_PATH` (donde S1 firmará cada sudo).

    La sala concreta se elige de `curriculum.json` (cap. 3) en el generator;
    esta hoja solo aporta la piel. Sin procesos/variables de entorno por
    defecto: los inyecta el generator si la quest así lo exige.
    """
    _ = fs_rng
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                DIR_SEG: _dir_for_cap3(DIR_SEG) for DIR_SEG in _cap3_dirs()
            },
        ),
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