"""chapter2.py — la piel del cap. 2 «Facturas» como DATOS (hoja, O1 31/08, Ornstein).

HOJA (leaf) igual que `chapter0.py`: solo constantes + la constructora del
FS. NO importa `core.generator.model` (para que `model.py` la importe sin
ciclo). El cap. 2 EXTENDE el escenario del cap. 0: la misma
oficina-vecinal-muelle-norte, ahora con `centralita/turnos/` y
`centralita/facturas/` (nota integrador en `backlog/historia/CAPITULOS/
02-facturas.md`).

La secuencia canónica del cap. 2 VERIFICA la línea EXACTA del capítulo:

    $ cd /srv/oficina-vecinal-muelle-norte
    $ grep 11:04 centralita/turnos/turno.log | wc -l
    2

Golden contra GNU real verificada por Smough en S1 (PR #11). Esta hoja solo
aporta el FS y los argv crudos; `model.py` los convierte a `CanonStep`.
Sin random, sin reloj real.
"""

from __future__ import annotations

from typing import Any

from core.generator.chapter0 import OFFICE_DIR, build_chapter0_fs
from core.sandbox.fs import DirNode, FileNode

# ---------------------------------------------------------------------------
# Rutas del cap. 2 (relativas a la oficina del cap. 0, decisión integrador)
# ---------------------------------------------------------------------------

#: Directorio de la centralita bajo la oficina (relativo a OFFICE_DIR).
CENTRALITA_DIR = "centralita"

#: Log de turnos del cap. 2: la CAUSA de la segunda ventana de las 11:04.
TURNO_DIR = "centralita/turnos"
TURNO_FILE = "turno.log"
TURNO = "centralita/turnos/turno.log"

#: Directorio de facturas del cap. 2 (vacío en la escena de apertura).
FACTURAS_DIR = "centralita/facturas"

#: Contenido EXACTO del turno.log: las 2 líneas de la apertura (ruido 6 y
#: ruido 1) + una de turno de mañana. `grep 11:04` sobre él → exactamente 2.
TURNO_CONTENT = (
    "11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt\n"
    "11:04 sesion 000 ruido 1 objetivo -\n"
    "08:59 turno de manana\n"
)


def build_chapter2_fs(fs_rng: Any) -> Any:
    """Monta el árbol del cap. 2: el fixture del cap. 0 + la centralita.

    Arranca del FS del cap. 0 (`build_chapter0_fs`) y le añade debajo del
    nodo de la oficina el árbol `centralita/turnos/turno.log` y
    `centralita/facturas/`. `fs_rng` se acepta por firma para el determinismo
    futuro (mismo convenio que el cap. 0); en v0 se ignora — la escena es la
    de la apertura de las 11:04.
    """
    _ = fs_rng
    fs = build_chapter0_fs(fs_rng)
    office = fs.get_dir(OFFICE_DIR, "/")
    office.children["centralita"] = DirNode(
        name="centralita",
        children={
            "turnos": DirNode(
                name="turnos",
                children={
                    "turno.log": FileNode(name="turno.log", content=TURNO_CONTENT),
                },
            ),
            "facturas": DirNode(name="facturas", children={}),
        },
    )
    return fs


# ---------------------------------------------------------------------------
# Secuencia canónica del cap. 2 (argv crudos, verbo a verbo con la golden)
# ---------------------------------------------------------------------------

#: cd a la oficina + la tubería golden `grep 11:04 ... | wc -l` → "2". La
#: tubería viaja como UNA línea en la Shell: los tokens se unen con " " y la
#: Shell la parsea como pipeline (S1).
CANON_STEPS_RAW_CH2: tuple[tuple[str, ...], ...] = (
    ("cd", OFFICE_DIR),
    ("grep", "11:04", TURNO, "|", "wc", "-l"),
)

#: Resultado esperado de la línea canónica del cap. 2 (assert final de
#: validación §6.4.4): el conteo de la doble apertura.
CH2_GREP_WC_EXPECTED = "2"