"""chapter0.py — la piel del cap. 0 «Trabajo en frío» como DATOS (v0).

ESTE ARCHIVO ES UNA HOJA (leaf): solo constantes + la constructora del FS.
NO importa `core.generator.model` ni ningún otro módulo del paquete, para
que `model.py` pueda importarlo sin ciclo (model → chapter0, unidireccional).

Compromiso v0 (documentado en README.md): la piel vive en CONSTANTES Python
aquí; cuando Smough materialice `src/data/`, este contenido migra a
`src/data/chapters/chapter0.json` (escena, textos, mtimes) y el generador lo
carga — dejamos anotado el contrato para no acoplarnos a ese plazo.

La escena ES la pelada del test canónico `test_session_cap0.py` y de
`backlog/historia/CAPITULOS/00-la-firma.md`: oficina-vecinal-muelle-norte,
ventana de las 11:04, CANDELAS proveedor nº 47. Los tres mtimes base van
FIJOS (la escena es la de las 11:04); el generador puede variar solo los
mtimes de los DECOYS de ambientación. Sin `random`, sin reloj real.
"""

from __future__ import annotations

from typing import Any

from core.sandbox.fs import DirNode, FileNode, FileSystem

# ---------------------------------------------------------------------------
# Rutas y nodo del encargo (constantes de la escena)
# ---------------------------------------------------------------------------

#: Directorio de la oficina vecinal del muelle norte (offset de la escena).
OFFICE_DIR = "/srv/oficina-vecinal-muelle-norte"

#: Fichero del proveedor: el OBJETIVO del encargo (copiarlo al USB).
PROVIDER_FILE = "nombre_de_proveedor.txt"

#: El USB de 512 MB que cuelga de la raíz (NO se lista desde /srv).
USB_DIR = "/usb"

#: Contenido EXACTO del dossier (golden, byte a byte del test canónico).
DOSSIER_CONTENT = "CANDELAS  ·  proveedor nº 47  ·  facturación externa  ·  114 facturas/mes\n"

#: Contenidos de los otros dos ficheros base de la oficina (golden).
LOG_CONTENT = "08:59 turno de mañana\n11:04 SIN REGISTRO\n"
README_CONTENT = "Sistema de gestion de la oficina vecinal.\n"


def build_chapter0_fs(fs_rng: Any) -> FileSystem:
    """Monta el árbol EXACTO de la escena canónica del cap. 0.

    `fs_rng` se acepta por firma para el determinismo futuro (variación de
    mtimes de la ESCENA por seed cuando lo autorice curriculum); en v0 se
    ignora — la escena es la de las 11:04 y los mtimes base van FIJOS.

    Los DECOYS de ambientación los añade el GENERADOR (`generator.py`), no
    esta función, para que la variante canónica se mantenga byte a byte
    idéntica al test `test_session_cap0.py`.

    Árbol (idéntico a `test_session_cap0::_fs_oficina`):
        /
        ├─ srv/
        │   └─ oficina-vecinal-muelle-norte/
        │       ├─ nombre_de_proveedor.txt  (recepcion:empleados, mtime 1044)
        │       ├─ log.txt                 (mtime 1030)
        │       └─ README                  (mtime 900)
        └─ usb/                            (vacío)
    """
    _ = fs_rng  # reservado para variación de mtimes por seed (v1)
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "oficina-vecinal-muelle-norte": DirNode(
                            name="oficina-vecinal-muelle-norte",
                            children={
                                PROVIDER_FILE: FileNode(
                                    name=PROVIDER_FILE,
                                    content=DOSSIER_CONTENT,
                                    owner="recepcion",
                                    group="empleados",
                                    mtime=1044,  # 11:04, tiempo simulado
                                ),
                                "log.txt": FileNode(
                                    name="log.txt",
                                    content=LOG_CONTENT,
                                    mtime=1030,
                                ),
                                "README": FileNode(
                                    name="README",
                                    content=README_CONTENT,
                                    mtime=900,
                                ),
                            },
                        )
                    },
                ),
                "usb": DirNode(name="usb", children={}),  # el USB de 512 MB
            },
        )
    )


# ---------------------------------------------------------------------------
# Secuencia canónica (en FORMATO crudo, sin acoplar a model) y decoys
# ---------------------------------------------------------------------------

#: La secuencia de la escena técnica de Manus (00-la-firma.md) en argv crudos:
#: ls → cat → cp → cd → ls. `model.py` la convierte a `tuple[CanonStep]`
#: (CANON_STEPS) para no crear ciclos de import (este módulo es leaf).
CANON_STEPS_RAW: tuple[tuple[str, ...], ...] = (
    ("ls", OFFICE_DIR),
    ("cat", OFFICE_DIR + "/" + PROVIDER_FILE),
    ("cp", OFFICE_DIR + "/" + PROVIDER_FILE, "/usb/"),
    ("cd", "/srv"),
    ("ls",),
)

#: Piscina de DECOYS (nombres de fichero de ambientación): `practice` cosecha
#: 1–2 de aquí; la `canonical` usa NINGUNO.
DECOY_POOL: tuple[str, ...] = (
    "avisos_comunidad.txt",
    "turnos_recepcion.txt",
    "agua_cerrada.txt",
)

#: Contenidos flavor deterministas de los decoys (español neutro, tono
#: oficina vecinal). SIN datos de juego, SIN horas del encargo: ambientación
#: pura que no filtra la solución ni los tiempos de la escena.
DECOY_CONTENT: dict[str, str] = {
    "avisos_comunidad.txt": (
        "Aviso: el ascensor del muelle norte estará en revisión\n"
        "durante la próxima semana. Disculpen las molestias.\n"
    ),
    "turnos_recepcion.txt": (
        "La recepción se cubre con turno de mañana y turno de tarde.\n"
    ),
    "agua_cerrada.txt": (
        "Corte de agua programado el miércoles de 10:00 a 12:00\n"
        "para labores de mantenimiento en la planta baja.\n"
    ),
}