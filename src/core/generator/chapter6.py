"""chapter6.py — la piel de la sala-dato del cap. 6 «Faro» como DATOS (hoja).

HOJA (leaf) igual que `chapter0.py`/`chapter2.py`/`chapter3.py`: solo
constantes + la constructora del FS. NO importa `core.generator.model`
(para que `model.py` pueda importarla sin ciclo).

Materializa el worldbuilding del censo de Manus (`CENSO-LISTA.md`) como
FICHEROS del mundo que se cruzan con la familia conteo (head/tail/sort/uniq
+ grep/wc/pipe). Formato EXACTO de `CENSO-LISTA.md`:
- delimitador `|`
- `registro.csv` con cabecera y 3 filas (Vera/E. Roldan/J. Herrera)
- `purgas.csv` con cabecera y 3 filas, la anomalía `PR-0091` con
  `fecha=EN BLANCO`, `sujeto=000`, `motivo_codigo=ENSAYO` (la purga de nadie)
- cebo pipe-0: un fichero trampa que devuelve 0 con `grep 000 <cebo> | wc -l`
  (nombre mal escrito / fichero sin la cadena), el «0 miente» de Havel/Gwyn.

Sin random, sin reloj real. `fs_rng` se acepta por firma para el
determinismo futuro (mismo convenio que los otros capítulos); en v0 se
ignora.
"""

from __future__ import annotations

from typing import Any

from core.sandbox.fs import DirNode, FileNode, FileSystem

# ---------------------------------------------------------------------------
# Rutas y ficheros de la Lista (contrato O3↔S2 por literales)
# ---------------------------------------------------------------------------

#: Directorio de la cámara del Faro (nodo del cap. 6).
CAP6_DIR = "/srv/camara-faro"

#: Ficheros de la Lista.
REGISTRO_FILE = "registro.csv"
PURGAS_FILE = "purgas.csv"

#: Rutas absolutas (contrato con S2: la quest apunta a estos ficheros).
REGISTRO_PATH = f"{CAP6_DIR}/{REGISTRO_FILE}"
PURGAS_PATH = f"{CAP6_DIR}/{PURGAS_FILE}"

#: Cabeceras exactas de CENSO-LISTA.md.
REGISTRO_HEADER = "residente_id|nombre|fecha_nac|distrito|vivienda|empleador|ingresos_mes|antiguedad_meses|chequeo|sanciones|marcas_purga|puntuacion|estado"
PURGAS_HEADER = "purga_id|fecha|sujeto|distrito|motivo_codigo|prev_puntuacion|post_credito|puerta_cerrada|archivo_referencia"

#: Contenidos EXACTOS de la Lista (ejemplo de CENSO-LISTA.md).
REGISTRO_CONTENT = (
    REGISTRO_HEADER + "\n"
    + "000291|VERA MONTEJO G.|12-03-1987|UMBRAL-ALTO|B14-E3-P14|LUMEN DIV. FACTURACION|2140|214|SIN CHEQUEO|0|0|712|ACTIVO\n"
    + "000462|E. ROLDAN S.|03-11-2001|UMBRAL-BAJO|C07-E1-P02|LAVANDERIA CICLON|1280|96|HOSP-47-C|1|1|438|EN DEUDA\n"
    + "000537|J. HERRERA V.|27-08-1963|MUEL-01|D03-E2-P01|ASTILLEROS DEL MUEL SE|0|0|EN BLANCO|0|2|0|PURGADO 19\n"
)

PURGAS_CONTENT = (
    PURGAS_HEADER + "\n"
    + "PR-0144|03-07|000462|UMBRAL-BAJO|CONTINUIDAD|438|0|1|OH-UBA-14-0007\n"
    + "PR-0151|11-07|000537|MUEL-01|REASIGNACION|0|0|1|OH-HOSP-47-C-0191\n"
    + "PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C\n"
)

# ---------------------------------------------------------------------------
# Cebo pipe-0 (Havel/Gwyn): el «0 miente»
# ---------------------------------------------------------------------------

#: Fichero trampa que produce conteo 0 con `grep 000 <cebo> | wc -l`.
#: Nombre plausiblemente confundible pero sin la cadena 000.
CEBO_FILE = "censo-borrador.csv"
CEBO_PATH = f"{CAP6_DIR}/{CEBO_FILE}"

#: Contenido del cebo: cabecera correcta pero SIN filas con 000 (solo
#: comentario de borrador). `grep 000 censo-borrador.csv | wc -l` → 0.
CEBO_CONTENT = (
    REGISTRO_HEADER + "\n"
    + "# borrador — pendiente de volcado completo\n"
)

# También un aviso suelto (coste de lectura, sin 000).
AVISO_FILE = "aviso-faro.txt"
AVISO_PATH = f"{CAP6_DIR}/{AVISO_FILE}"
AVISO_CONTENT = "Faro — luz continua. Acceso restringido a personal autorizado.\n"

# ---------------------------------------------------------------------------
# E2 — .nota-corte del operador muerto (boon hallazgo Bandit)
# ---------------------------------------------------------------------------

#: Fichero oculto del operador muerto: documenta cut por necesidad.
NOTA_CORTE_FILE = ".nota-corte"
NOTA_CORTE_PATH = f"{CAP6_DIR}/{NOTA_CORTE_FILE}"
NOTA_CORTE_CONTENT = (
    "# nota del operador — 11-07 foco Faro\n"
    + "# si quieres saber qué distritos hay y cuántos vecinos por distrito,\n"
    + "# corta la columna: cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c\n"
    + "# la Lista es tabla, no texto — sin corte no se responde\n"
)

def build_chapter6_fs(fs_rng: Any) -> FileSystem:
    """Monta el árbol de la sala-dato del cap. 6 «Faro».

    El FS de la sala contiene SIEMPRE:
      - la Lista como dos ficheros del mundo (`registro.csv` + `purgas.csv`)
        al formato EXACTO de `CENSO-LISTA.md`;
      - el cebo pipe-0 (`censo-borrador.csv`) que devuelve 0 al contar;
      - E2: `.nota-corte` del operador muerto (boon hallazgo, Bandit).

    La sala concreta se elige de `curriculum.json` (cap. 6) en el generator;
    esta hoja solo aporta la piel.
    """
    _ = fs_rng
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "camara-faro": DirNode(
                            name="camara-faro",
                            children={
                                REGISTRO_FILE: FileNode(
                                    name=REGISTRO_FILE,
                                    content=REGISTRO_CONTENT,
                                    owner="lumen",
                                    group="censo",
                                    mode="644",
                                ),
                                PURGAS_FILE: FileNode(
                                    name=PURGAS_FILE,
                                    content=PURGAS_CONTENT,
                                    owner="lumen",
                                    group="censo",
                                    mode="644",
                                ),
                                CEBO_FILE: FileNode(
                                    name=CEBO_FILE,
                                    content=CEBO_CONTENT,
                                    owner="lumen",
                                    group="censo",
                                    mode="644",
                                ),
                                AVISO_FILE: FileNode(
                                    name=AVISO_FILE,
                                    content=AVISO_CONTENT,
                                    owner="root",
                                    group="root",
                                    mode="644",
                                ),
                                NOTA_CORTE_FILE: FileNode(
                                    name=NOTA_CORTE_FILE,
                                    content=NOTA_CORTE_CONTENT,
                                    owner="cero",
                                    group="cero",
                                    mode="644",
                                ),
                            },
                        ),
                    },
                ),
            },
        ),
    )

# ---------------------------------------------------------------------------
# Secuencia canónica de la sala-dato (argv crudos, sin acoplar a model)
# ---------------------------------------------------------------------------

#: v0: revelar la purga de nadie contando `ENSAYO` en purgas.csv.
#: `grep ENSAYO <purgas> | wc -l` → "1" (la fila PR-0091). `grep 000` daría 3
#: por los `000462`/`000537`, pero el dato que delata la anomalía es ENSAYO.
CANON_STEPS_RAW_CH6: tuple[tuple[str, ...], ...] = (
    ("grep", "ENSAYO", PURGAS_PATH, "|", "wc", "-l"),
)

#: E2: qué distritos y cuántos vecinos por distrito — exige cut por necesidad.
#: `cut -d'|' -f4 purgas.csv | sort | uniq -c` — la forma Bandit enseñada
#: (enmienda 🧭18: cut|sort|uniq -c, no cut|uniq directo).
CANON_STEPS_RAW_CH6_E2: tuple[tuple[str, ...], ...] = (
    ("cut", "-d'|'","-f4", PURGAS_PATH, "|", "sort", "|", "uniq", "-c"),
)

#: E3: ordenar la Lista por puntuación (col 12) — lectura vertical.
#: `sort -t'|' -k12 -n purgas.csv | head -n 3` — los 3 más cerca del 0.
CANON_STEPS_RAW_CH6_E3: tuple[tuple[str, ...], ...] = (
    ("sort", "-t", "'|'", "-k12", "-n", PURGAS_PATH, "|", "head", "-n", "3"),
)

#: Resultado esperado de la golden del cap. 6.
CH6_GREP_WC_EXPECTED = "1"
