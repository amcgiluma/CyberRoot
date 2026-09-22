"""chapter5.py — la piel de la sala de la Subestación del cap. 5 como DATOS (hoja).

HOJA (leaf) igual que chapter0/2/3/4/6: solo constantes + constructora del FS.
NO importa `core.generator.model` (para que `model` pueda importarla sin ciclo).

Materializa la Subestación tras el troncal del cap. 4:
- El testigo condicional: `/tmp/volcado-custodia.csv` como COPIA LOCAL del
  volcado del troncal. Si `volcado_rescatado=True` (el jugador hizo `scp`
  en ch4.e3 y dejó 30 ticks sin `rm`), el fichero existe con
  `TR-003|faro|troncal-01|512|EN_COLA`; si caducado, NO existe
  (`cat` → `No such file` — ausencia honesta es el detector).
- Proceso intruso `--vigilar-censo` con USER `censo` y `START 03:14`
  (misma hora del volcado — firma que ya midió Oscar en ch4).

Sin random, sin reloj real. `fs_rng` se usa vía `fork("ps-subestacion")`
para la piel de procesos; fallback estático si no hay RNG (tests handmade).

Contrato: Smough construye quest `story.ch5.e2` sobre este FS (requiere
`cat`+`scp`, sin concepto nuevo); la quest NO depende del FS del cap. 5
en la generación — el FS es la geografía que cambia con la decisión de
ch4. La flexibilidad hace que el día no caiga si O1 no entrega.
"""

from __future__ import annotations

from typing import Any

from core.sandbox.fs import DirNode, FileNode, FileSystem, Proceso

# ---------------------------------------------------------------------------
# Rutas y testigo condicional (contrato O1↔S2 por literales)
# ---------------------------------------------------------------------------

#: Directorio temporal local donde vive la copia custodiada.
CUSTODIA_DIR = "/tmp"
CUSTODIA_FILE = "volcado-custodia.csv"
CUSTODIA_PATH = f"{CUSTODIA_DIR}/{CUSTODIA_FILE}"

#: Cabecera del volcado custodiado (misma que TRONCAL/VOLCADO_RESCATE).
CUSTODIA_HEADER = "id|origen|destino|bytes|estado"

#: Contenido exacto de la custodia (mismo TR-003 que viaja entre capítulos).
CUSTODIA_CONTENT = (
    CUSTODIA_HEADER + "\n" + "TR-003|faro|troncal-01|512|EN_COLA\n"
)

# ---------------------------------------------------------------------------
# E1 — La puerta que dejaste: sesión pts0 con modo 644 (canon chmod 600)
# ---------------------------------------------------------------------------

#: Directorio y fichero de la sesión registrada (diegesis: pts/0 del Alto).
SESIONES_DIR = "sesiones"
PTS0_FILE = "pts0"
PTS0_PATH = f"/srv/subestacion/{SESIONES_DIR}/{PTS0_FILE}"

#: Contenido de la sesión (who-like): quien estuvo y cuándo.
PTS0_CONTENT = "operator pts/0        2026-09-21 23:14 (10.6.0.15)\n"

# ---------------------------------------------------------------------------
# Procesos de la Subestación — el intruso que vigila el censo
# ---------------------------------------------------------------------------

#: Binario del intruso (coherente con censo:522 --vigilar-censo del cap. 3).
INTRUSO_BINARY = "intruso"
INTRUSO_ARGS = "--vigilar-censo"
INTRUSO_CMD = f"{INTRUSO_BINARY} {INTRUSO_ARGS}"
INTRUSO_USER = "censo"
INTRUSO_START = "03:14"

#: Entorno base de la sesión de la Subestación.
CHAPTER5_ENVIRONMENT: dict[str, str] = {
    "LANG": "C.UTF-8",
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin",
    "SHELL": "/bin/sh",
    "USER": "operator",
}

#: Procesos estáticos de referencia (fallback sin RNG).
_CHAPTER5_PROCESSES_FALLBACK: tuple[Proceso, ...] = (
    Proceso(
        pid=1,
        user="root",
        cmd="/sbin/init --system",
        tty="?",
        cpu="0.0",
        mem="0.1",
        vsz="22288",
        rss="10888",
        stat="Ss",
        start="Aug25",
        time="0:38",
    ),
    Proceso(
        pid=522,
        user=INTRUSO_USER,
        cmd=INTRUSO_CMD,
        tty="?",
        cpu="0.0",
        mem="0.3",
        vsz="13100",
        rss="2440",
        stat="S",
        start=INTRUSO_START,
        time="03:14:02",
    ),
)


def _ch5_processes_for_rng(fs_rng: Any) -> tuple[Proceso, ...]:
    """Genera los procesos de la Subestación deterministas por seed.

    - pid 1: init, START Aug25 (estable)
    - pid X: intruso --vigilar-censo, USER censo, START 03:14
      (firma horaria del volcado — la hora que Oscar midió en ch4).

    El PID del intruso deriva de `fs_rng.fork("ps-subestacion")` para
    determinismo byte-idéntico sin tocar el FS. Fallback estático si
    fs_rng no tiene fork (tests handmade con None).
    """
    try:
        ps_rng = fs_rng.fork("ps-subestacion")  # type: ignore[union-attr]
        pid_intruso = 420 + ps_rng.below(15)  # 420-434, siempre >1 y estable por seed
    except Exception:
        return _CHAPTER5_PROCESSES_FALLBACK

    init = Proceso(
        pid=1,
        user="root",
        cmd="/sbin/init --system",
        tty="?",
        cpu="0.0",
        mem="0.1",
        vsz="22288",
        rss="10888",
        stat="Ss",
        start="Aug25",
        time="0:38",
    )
    intruso = Proceso(
        pid=pid_intruso,
        user=INTRUSO_USER,
        cmd=INTRUSO_CMD,
        tty="?",
        cpu="0.0",
        mem="0.3",
        vsz="13100",
        rss="2440",
        stat="S",
        start=INTRUSO_START,
        time="03:14:02",
    )
    # Orden por PID para `ps aux` determinista
    return tuple(sorted((init, intruso), key=lambda p: p.pid))


def build_chapter5_fs(fs_rng: Any, volcado_rescatado: bool = False) -> FileSystem:
    """Monta el árbol de la Subestación del cap. 5.

    El FS contiene SIEMPRE:
      - procesos: init + intruso --vigilar-censo (censo, 03:14);
      - /tmp con el testigo CONDICIONAL: `volcado-custodia.csv` existe
        SOLO si `volcado_rescatado=True` (contenido TR-003 EN_COLA);
        si caducado, NO existe — `cat /tmp/volcado-custodia.csv`
        → `No such file` (ausencia honesta como detector).

    Determinista por `fs_rng` (pid del intruso) y por el flag
    `volcado_rescatado` (geografía que cambia con la decisión de ch4).
    """
    processes = _ch5_processes_for_rng(fs_rng)
    environment = dict(CHAPTER5_ENVIRONMENT)

    tmp_children: dict[str, FileNode] = {}
    if volcado_rescatado:
        tmp_children[CUSTODIA_FILE] = FileNode(
            name=CUSTODIA_FILE,
            content=CUSTODIA_CONTENT,
            owner="operator",
            group="censo",
            mode="644",
        )

    # E1 — La puerta que dejaste: sesión pts0 con permisos 644 (canon 600)
    sesiones_children: dict[str, FileNode] = {
        "pts0": FileNode(
            name="pts0",
            content=PTS0_CONTENT,
            owner="operator",
            group="operator",
            mode="644",
        )
    }
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "tmp": DirNode(name="tmp", children=tmp_children),  # type: ignore[arg-type]
                "srv": DirNode(
                    name="srv",
                    children={
                        "subestacion": DirNode(
                            name="subestacion",
                            children={
                                "rack-informes": DirNode(
                                    name="rack-informes",
                                    children={},
                                ),
                                "sesiones": DirNode(
                                    name="sesiones",
                                    children=sesiones_children,  # type: ignore[arg-type]
                                ),
                            },
                        ),
                    },
                ),
                "var": DirNode(
                    name="var",
                    children={
                        "log": DirNode(name="log", children={}),
                    },
                ),
            },
        ),
        processes=processes,
        environment=environment,
    )


# ---------------------------------------------------------------------------
# Secuencia canónica del cap. 5 (referencia para el generador/validador)
# ---------------------------------------------------------------------------

#: v0: leer el testigo si existe; ps para ver al intruso.
CANON_STEPS_RAW_CH5: tuple[tuple[str, ...], ...] = (
    ("cat", CUSTODIA_PATH),
    ("ps", "aux"),
)

#: Variante sin testigo (caducado): solo ps (cat fallaría).
CANON_STEPS_RAW_CH5_CADUCADO: tuple[tuple[str, ...], ...] = (
    ("ps", "aux"),
)

#: E1 — La puerta que dejaste (° canon: ls -l + chmod 600 sobre pts0).
CANON_STEPS_RAW_CH5_E1: tuple[tuple[str, ...], ...] = (
    ("ls", "-l", PTS0_PATH),
    ("chmod", "600", PTS0_PATH),
)

#: E1 variante roja: chmod 777 deja la puerta abierta.
CANON_STEPS_RAW_CH5_E1_RED: tuple[tuple[str, ...], ...] = (
    ("ls", "-l", PTS0_PATH),
    ("chmod", "777", PTS0_PATH),
)
