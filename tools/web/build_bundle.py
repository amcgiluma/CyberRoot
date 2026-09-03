#!/usr/bin/env python3
"""build_bundle.py — empaqueta el core real (stdlib puro) para Pyodide en web/.

T1-deploy HITO B: construir en web/ una página estática list para Vercel que da
juego REAL en el navegador. El core (`src/core/`) es headless y stdlib-only
(ARCHITECTURE §1.1 / §2), así que se puede cargar en Pyodide sin cambios.

Este script NO toca `src/core/`, `src/data/`, `src/render/`, ni `src/tests/`:
solo LEE sus .py/.json y escribe debajo de `web/`. Rutas disjuntas.

Genera:
- `web/bundle/core.json`  → manifest {ruta_virtual: contenido} para escribir
  los fuentes del core en el FS virtual de Pyodide y poder
  `from core.generator import generate, new_session`.
- Copia los PNG golden del render (evidencia jugable, mínimo aceptable) a
  `web/assets/golden/`.

Uso:
    .venv/bin/python web/build_bundle.py        # desde la raíz del repo

Nota de diseño: los fuentes se incrustan COMO TEXTO en un único manifest
(una sola petición al montar), no se sirven como decenas de ficheros .py.
`core.json` es un artefacto GENERADO y se regenera con este script; no se edita
a mano.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]          # raíz del repo
CORE_SRC = REPO / "src" / "core"
DATA_SRC = REPO / "src" / "data" / "curriculum.json"
GOLDEN_SRC = REPO / "src" / "render" / "golden"

WEB = REPO / "web"
BUNDLE = WEB / "bundle"
ASSETS = WEB / "assets" / "golden"

#: Prefijos virtuales dentro del FS de Pyodide (altura == parents[2]).
VIRT_LIB = "/lib"        # sys.path; core/ vive aquí -> data/ resuelve a /lib/data
VIRT_CORE = f"{VIRT_LIB}/core"
VIRT_DATA = f"{VIRT_LIB}/data"


def collect() -> dict[str, str]:
    """ruta_virtual -> contenido de los fuentes del core + curriculum.json."""
    out: dict[str, str] = {}

    for py in sorted(CORE_SRC.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        rel = py.relative_to(CORE_SRC)            # p.ej. generator/generator.py
        virtual = f"{VIRT_CORE}/{rel.as_posix()}"
        out[virtual] = py.read_text(encoding="utf-8")

    if not DATA_SRC.exists():
        raise SystemExit(f"falta {DATA_SRC}: no se puede empaquetar el core")
    out[f"{VIRT_DATA}/curriculum.json"] = DATA_SRC.read_text(encoding="utf-8")

    return out


def copy_golden() -> list[str]:
    """Copia los PNG golden del render v0 (evidencia jugable) a web/assets/."""
    assets: list[str] = []
    ASSETS.mkdir(parents=True, exist_ok=True)
    for png in ("cap0-room.png", "cap0-room.zoom3x.png"):
        src = GOLDEN_SRC / png
        if src.exists():
            shutil.copyfile(src, ASSETS / png)
            assets.append(png)
    return assets


def main() -> int:
    manifest = collect()
    BUNDLE.mkdir(parents=True, exist_ok=True)
    target = BUNDLE / "core.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    pngs = copy_golden()

    print(f"core.json: {len(manifest)} ficheros virtuales → {target.relative_to(REPO)}")
    print(f"golden copiados: {pngs or 'NINGUNO (falta src/render/golden)'}")
    nbytes = len(target.read_bytes())
    print(f"tamaño manifest: {nbytes/1024:.1f} KiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())