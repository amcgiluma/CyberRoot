"""chapter4.py — la piel de la sala de red del cap. 4 «Troncales» como DATOS (hoja).

HOJA (leaf) igual que chapter0/2/3/6: solo constantes + constructora del FS.
NO importa `core.generator.model` (para que `model` pueda importarla sin ciclo).

Materializa la red del cap. 4 (Fase B, 09/09 — O1 Ornstein):
- `/etc/hosts` con 2-3 hosts por seed: `faro` 10.6.0.5 + `troncal-01` 10.6.1.10
  (+ `troncal-02` 10.6.1.11 si el RNG decide 3). Incluye línea de comentario
  `#` que el parser ya ignora (regla «leer descubre, listar no»).
- Cada host con FS remoto determinista:
  * `faro` reusa la piel del cap. 6 (registro/purgas del Faro)
  * `troncal-01`/`troncal-02` con un volcado `volcado.csv` propio.

Sin random, sin reloj real. `fs_rng` es `Rng` seedeada del generator.
"""

from __future__ import annotations

from typing import Any

from core.sandbox.fs import DirNode, FileNode, FileSystem

# ---------------------------------------------------------------------------
# Rutas y hosts del cap. 4 (contrato O1↔S, nombres EXACTOS del plan 09/09)
# ---------------------------------------------------------------------------

#: Ruta canónica de hosts (reusa constante de shell.py HOSTS_PATH).
HOSTS_PATH = "/etc/hosts"
HOSTS_FILE = "hosts"

#: IPs fijas del plan (faro + troncal-01 obligatorios).
HOST_IPS: dict[str, str] = {
    "faro": "10.6.0.5",
    "troncal-01": "10.6.1.10",
    "troncal-02": "10.6.1.11",
}

#: Directorio y fichero del volcado troncal.
TRONCAL_DIR = "/srv/archivo-troncal"
TRONCAL_FILE = "volcado.csv"
TRONCAL_PATH = f"{TRONCAL_DIR}/{TRONCAL_FILE}"

#: Cabecera del volcado troncal (tabla `|` como el Faro).
TRONCAL_HEADER = "id|origen|destino|bytes|estado"

#: Contenido determinista del volcado (3 filas + cabecera).
TRONCAL_CONTENT = (
    TRONCAL_HEADER + "\n"
    + "TR-001|faro|troncal-01|1024|OK\n"
    + "TR-002|troncal-01|nodo-02|2048|OK\n"
    + "TR-003|faro|troncal-01|512|EN_COLA\n"
)

# Variante para troncal-02 (mismo formato, distinto contenido para distinguir hosts)
TRONCAL_CONTENT_02 = (
    TRONCAL_HEADER + "\n"
    + "TR-101|faro|troncal-02|4096|OK\n"
    + "TR-102|troncal-02|nodo-03|1024|OK\n"
)

# ---------------------------------------------------------------------------
# Helpers deterministas por seed
# ---------------------------------------------------------------------------

def _hosts_for_seed(fs_rng: Any) -> list[str]:
    """Lista de hosts para esta seed (2 o 3, determinista).

    Usa `fork("ch4-hosts")` si existe, si no `below` directo.
    Siempre incluye `faro` y `troncal-01`; el tercero (`troncal-02`)
    aparece cuando el RNG decide 3.
    """
    try:
        r = fs_rng.fork("ch4-hosts")  # type: ignore[attr-defined]
    except Exception:
        r = fs_rng
    # 0 => 2 hosts, 1 => 3 hosts
    try:
        n = r.below(2)  # type: ignore[attr-defined]
    except Exception:
        # fallback si fs_rng no es Rng (test handmade con stub)
        n = 0
    base = ["faro", "troncal-01"]
    if n == 1:
        base.append("troncal-02")
    return base


def _hosts_content(hosts: list[str]) -> str:
    """Texto de `/etc/hosts` para `hosts` (con comentario `#`)."""
    lines: list[str] = ["127.0.0.1 localhost", "# Troncal — red cap.4 (faro + troncal)"]
    for h in hosts:
        ip = HOST_IPS.get(h, "10.6.1.99")
        lines.append(f"{ip} {h}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# FS remotos por host
# ---------------------------------------------------------------------------

def build_ch4_remote_fs(host: str) -> FileSystem:
    """FS remoto determinista para `host` (usado por Shell discovery y new_session).

    - `faro` → reusa la piel del cap. 6 (registro/purgas) para que
      `scp faro:/srv/camara-faro/purgas.csv /tmp/` funcione.
    - `troncal-*` → FS con `/srv/archivo-troncal/volcado.csv`.
    - otro → FS vacío.
    """
    if host == "faro":
        # Reusa la piel del Faro sin importar ciclo: construye aquí
        # la misma estructura que chapter6.build_chapter6_fs pero inline
        # para no crear dependencia de importación en la hoja.
        # Contenido copiado de chapter6 para determinismo idéntico.
        from core.generator.chapter6 import (
            REGISTRO_FILE,
            REGISTRO_CONTENT,
            PURGAS_FILE,
            PURGAS_CONTENT,
            CEBO_FILE,
            CEBO_CONTENT,
            AVISO_FILE,
            AVISO_CONTENT,
            CEBO_RUTA_FILE,
            CEBO_RUTA_CONTENT,
            NOTA_CORTE_FILE,
            NOTA_CORTE_CONTENT,
        )

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
                                    REGISTRO_FILE: FileNode(name=REGISTRO_FILE, content=REGISTRO_CONTENT, owner="lumen", group="censo", mode="644"),
                                    PURGAS_FILE: FileNode(name=PURGAS_FILE, content=PURGAS_CONTENT, owner="lumen", group="censo", mode="644"),
                                    CEBO_FILE: FileNode(name=CEBO_FILE, content=CEBO_CONTENT, owner="lumen", group="censo", mode="644"),
                                    AVISO_FILE: FileNode(name=AVISO_FILE, content=AVISO_CONTENT, owner="root", group="root", mode="644"),
                                    CEBO_RUTA_FILE: FileNode(name=CEBO_RUTA_FILE, content=CEBO_RUTA_CONTENT, owner="lumen", group="censo", mode="644"),
                                    NOTA_CORTE_FILE: FileNode(name=NOTA_CORTE_FILE, content=NOTA_CORTE_CONTENT, owner="cero", group="cero", mode="644"),
                                },
                            ),
                        },
                    ),
                    "etc": DirNode(name="etc", children={HOSTS_FILE: FileNode(name=HOSTS_FILE, content="127.0.0.1 localhost\n10.6.0.5 faro\n", owner="root", group="root", mode="644")}),
                    "tmp": DirNode(name="tmp", children={}),
                },
            ),
        )
    if host.startswith("troncal"):
        content = TRONCAL_CONTENT_02 if host == "troncal-02" else TRONCAL_CONTENT
        return FileSystem(
            root=DirNode(
                name="/",
                children={
                    "srv": DirNode(
                        name="srv",
                        children={
                            "archivo-troncal": DirNode(
                                name="archivo-troncal",
                                children={
                                    TRONCAL_FILE: FileNode(name=TRONCAL_FILE, content=content, owner="lumen", group="troncal", mode="644"),
                                },
                            ),
                        },
                    ),
                    "tmp": DirNode(name="tmp", children={}),
                    "etc": DirNode(name="etc", children={HOSTS_FILE: FileNode(name=HOSTS_FILE, content="127.0.0.1 localhost\n", owner="root", group="root", mode="644")}),
                },
            ),
        )
    return FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={}) }))


# ---------------------------------------------------------------------------
# FS local del cap. 4
# ---------------------------------------------------------------------------

def build_chapter4_fs(fs_rng: Any) -> FileSystem:
    """Monta el árbol local de la sala de red del cap. 4 «Troncales».

    El FS local contiene SIEMPRE:
      - `/etc/hosts` con 2-3 hosts (determinista por `fs_rng`);
      - `/tmp` vacío para `scp ... /tmp/`;
      - `/srv` vacío (piel mínima del nodo troncal local).

    Los FS remotos NO van aquí: los crea `build_ch4_remote_fs(host)`
    y los pre-puebla `new_session` / `Shell._note_hosts_discovery`.
    """
    hosts = _hosts_for_seed(fs_rng)
    content = _hosts_content(hosts)
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "etc": DirNode(
                    name="etc",
                    children={
                        HOSTS_FILE: FileNode(name=HOSTS_FILE, content=content, owner="root", group="root", mode="644"),
                    },
                ),
                "tmp": DirNode(name="tmp", children={}),
                "srv": DirNode(name="srv", children={}),
            },
        ),
    )


# ---------------------------------------------------------------------------
# Secuencia canónica del cap. 4
# ---------------------------------------------------------------------------

#: v0: descubrir hosts + traer volcado del troncal.
#: `cat /etc/hosts` → descubre; `scp troncal-01:.../volcado.csv /tmp/` → deja fichero.
CANON_STEPS_RAW_CH4: tuple[tuple[str, ...], ...] = (
    ("cat", HOSTS_PATH),
    ("scp", f"troncal-01:{TRONCAL_PATH}", "/tmp/"),
)
