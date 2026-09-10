"""chapter6.py — la piel de la sala-dato del cap. 6 «Faro» como DATOS (hoja).

HOJA (leaf) igual que `chapter0.py`/`chapter2.py`/`chapter3.py`: solo
constantes + la constructora del FS. NO importa `core.generator.model`
(para que `model.py` pueda importarla sin ciclo).

Materializa el worldbuilding del censo de Manus (`CENSO-LISTA.md`) como
FICHEROS del mundo que se cruzan con la familia conteo (head/tail/sort/uniq
+ grep/wc/pipe). Formato EXACTO de `CENSO-LISTA.md`:
- delimitador `|`
- `registro.csv` con cabecera y 3 filas (Vera/E. Roldan/J. Herrera)
- `purgas.csv` con cabecera y 4 filas: la anomalía `PR-0091` con
  `fecha=EN BLANCO`, `sujeto=000`, `motivo_codigo=ENSAYO` (la purga de nadie),
  más `PR-0092` con `motivo_codigo=EN BLANCO, revisado` (trampa delimitador O2:
  coma dentro de campo, `cut -d','` devuelve basura)
- cebo pipe-0: un fichero trampa que devuelve 0 con `grep 000 <cebo> | wc -l`
  (nombre mal escrito / fichero sin la cadena), el «0 miente» de Havel/Gwyn.

O1 10/09 — «La persiana» (dato5): la sala gana PIEL DE PROCESOS determinista
por seed — 3 procesos que comparten binario (init Aug25 + 2 faro-sync) donde
solo el START 11:04 delata cuál arrancó la noche de la firma PR-0091.
Cero sandbox (ps.py ya imprime START).

Sin random, sin reloj real. `fs_rng` se usa vía `fork("ps-faro")` para la
piel de procesos; fallback estático si no hay RNG (tests handmade).
"""

from __future__ import annotations

from typing import Any

from core.sandbox.fs import DirNode, FileNode, FileSystem, Proceso

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
    + "PR-0092|11-07|000483|UMBRAL-BAJO|EN BLANCO, revisado|500|0|1|OH-UBA-14-0092\n"
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
# Cebo del Faro O3 (05/09, Ornstein): el 0 que miente por ruta
# ---------------------------------------------------------------------------
#: Fichero-señuelo que invita a resolver con ruta relativa.
#: No contiene ENSAYO: `grep ENSAYO purgas.csv | wc -l` desde / da 0 honesto.
#: El briefing ya exige absolutas (🧭15); este fichero es piel, no lógica.
CEBO_RUTA_FILE = "LEEME.txt"
CEBO_RUTA_PATH = f"{CAP6_DIR}/{CEBO_RUTA_FILE}"
CEBO_RUTA_CONTENT = (
    "Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.\n"
)

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

# ---------------------------------------------------------------------------
# O3 — /etc/hosts en el mundo (host `faro`) — Fase A real (08/09, Ornstein)
# ---------------------------------------------------------------------------
#: Directorio y fichero de hosts (red pieza A, DESIGN §6.1).
HOSTS_FILE = "hosts"
HOSTS_PATH = "/etc/hosts"
HOSTS_CONTENT = "127.0.0.1 localhost\n10.6.0.5 faro\n"

# ---------------------------------------------------------------------------
# O1 10/09 — Piel de procesos «La persiana» (dato5) — 3 procesos, 1 binario
# ---------------------------------------------------------------------------

#: Binario compartido por los dos procesos del Faro (la persiana).
FARO_SYNC_BINARY = "/usr/sbin/faro-sync"

#: START del init (siempre Aug25, como en chapter3).
FARO_INIT_START = "Aug25"

#: START del culpable (la noche de la firma PR-0091).
FARO_GUILTY_START = "11:04"

#: STARTs posibles para el señuelo (nunca 11:04).
_FARO_DECOY_STARTS: tuple[str, ...] = ("08:17", "09:33", "10:11", "06:42", "07:58")

#: Entorno base de la sesión del Faro (visible en `env`).
CHAPTER6_ENVIRONMENT: dict[str, str] = {
    "LANG": "C.UTF-8",
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin",
    "SHELL": "/bin/sh",
    "USER": "operator",
}

def _ch6_processes_for_rng(fs_rng: Any) -> tuple[Proceso, ...]:
    """Genera los 3 procesos del Faro deterministas por seed.

    - pid 1: init, START Aug25
    - pid A: faro-sync --purga PR-0091, START 11:04 (el culpable)
    - pid B: faro-sync --purga PR-0092, START distinto de 11:04 (señuelo)

    Ambos faro-sync comparten binario; solo el START delata la noche de
    PR-0091. PIDs y START del señuelo derivan de `fs_rng.fork("ps-faro")`
    para determinismo byte-idéntico sin tocar el FS. Fallback estático si
    fs_rng no tiene fork (tests handmade con None).
    """
    init = Proceso(
        pid=1, user="root", cmd="/sbin/init --system",
        tty="?", cpu="0.0", mem="0.1", vsz="22288", rss="10888",
        stat="Ss", start=FARO_INIT_START, time="0:38",
    )
    # Determinismo por seed — pids y START señuelo varían, culpable siempre 11:04+PR-0091
    try:
        ps_rng = fs_rng.fork("ps-faro")  # type: ignore[union-attr]
        # PIDs deterministas pero estables por seed: rangos disjuntos para orden fijo
        pid_guilty = 412 + ps_rng.below(10)  # 412-421
        pid_decoy = 430 + ps_rng.below(10)   # 430-439 (siempre > guilty)
        decoy_start = _FARO_DECOY_STARTS[ps_rng.below(len(_FARO_DECOY_STARTS))]
        # Asegura decoy nunca 11:04 (ya filtrado por lista)
    except Exception:
        pid_guilty = 412
        pid_decoy = 431
        decoy_start = "08:17"

    guilty = Proceso(
        pid=pid_guilty, user="faro", cmd=f"{FARO_SYNC_BINARY} --purga PR-0091",
        tty="?", cpu="0.1", mem="0.2", vsz="12784", rss="2104",
        stat="S", start=FARO_GUILTY_START, time="11:34:02",
    )
    decoy = Proceso(
        pid=pid_decoy, user="faro", cmd=f"{FARO_SYNC_BINARY} --purga PR-0092",
        tty="?", cpu="0.0", mem="0.3", vsz="13100", rss="2440",
        stat="S", start=decoy_start, time="09:11:44",
    )
    # Orden por PID para que `ps aux` siempre liste sorted (determinista)
    procs = tuple(sorted((init, guilty, decoy), key=lambda p: p.pid))
    return procs


def build_chapter6_fs(fs_rng: Any) -> FileSystem:
    """Monta el árbol de la sala-dato del cap. 6 «Faro».

    El FS de la sala contiene SIEMPRE:
      - la Lista como dos ficheros del mundo (`registro.csv` + `purgas.csv`)
        al formato EXACTO de `CENSO-LISTA.md`;
      - el cebo pipe-0 (`censo-borrador.csv`) que devuelve 0 al contar;
      - el cebo de ruta (`LEEME.txt`, O3) y la `.nota-corte` (boon E2, Bandit);
      - E2: `.nota-corte` del operador muerto (boon hallazgo, Bandit).
      - O1 10/09: piel de procesos determinista por seed (3 procesos,
        1 binario compartido, START 11:04 delata PR-0091) + environment.

    La sala concreta se elige de `curriculum.json` (cap. 6) en el generator;
    esta hoja solo aporta la piel.
    """
    processes = _ch6_processes_for_rng(fs_rng)
    environment = dict(CHAPTER6_ENVIRONMENT)
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
                                CEBO_RUTA_FILE: FileNode(
                                    name=CEBO_RUTA_FILE,
                                    content=CEBO_RUTA_CONTENT,
                                    owner="lumen",
                                    group="censo",
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
                "etc": DirNode(
                    name="etc",
                    children={
                        HOSTS_FILE: FileNode(
                            name=HOSTS_FILE,
                            content=HOSTS_CONTENT,
                            owner="root",
                            group="root",
                            mode="644",
                        ),
                    },
                ),
            },
        ),
        processes=processes,
        environment=environment,
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

#: E2 — «La que no pesa» (08/09, Ornstein): tail -n +2 + cut|sort
#: `tail -n +2 purgas.csv | cut -d'|' -f4 | sort | uniq -c` sin header fantasma
#: Se valida en generator.py rama story.ch6.e2 (2 UMBRAL-BAJO, sin distrito).
CANON_STEPS_RAW_CH6_E2_TAIL: tuple[tuple[str, ...], ...] = (
    ("tail", "-n", "+2", PURGAS_PATH, "|", "cut", "-d'|'","-f4", "|", "sort"),
)

#: Resultado esperado de la golden del cap. 6.
CH6_GREP_WC_EXPECTED = "1"
