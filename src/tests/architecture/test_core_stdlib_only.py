"""Guardián nº 2 (ARCHITECTURE §3): `src/core/` es stdlib-ONLY.

El core debe poder testearse sin instalar Pyxel ni ninguna otra dependencia
de runtime. Cualquier import externo aquí abajo rompe esa promesa.

Límite conocido y aceptado en v1: un paquete LOCAL de src/ (core, render,
assets...) pasa este filtro; lo que atrapa son dependencias EXTERNAS
(pyxel, numpy, requests...). El test hermano de pyxel cubre la frontera clave.
Cambiar/quitar este test exige propuesta en backlog/mejoras/pendiente/.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2]
CORE_DIR = SRC_DIR / "core"

# Raíces locales permitidas: los paquetes que viven en src/ (core hoy; más
# adelante render/assets como propios de otras capas).
_LOCAL_ROOTS = {
    p.name for p in SRC_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")
}

_STDLIB = frozenset(sys.stdlib_module_names)


def test_core_solo_stdlib_y_paquetes_locales() -> None:
    assert CORE_DIR.is_dir(), f"No existe {CORE_DIR}"
    externos: list[str] = []
    for path in sorted(CORE_DIR.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            mods: list[str] = []
            if isinstance(node, ast.Import):
                mods = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level > 0 or node.module is None:
                    continue  # import relativo: interno por definición
                mods = [node.module]
            for module in mods:
                root = module.split(".")[0]
                if root not in _STDLIB and root not in _LOCAL_ROOTS:
                    externos.append(
                        f"{path.relative_to(SRC_DIR)}: import {module}"
                    )
    assert not externos, (
        "src/core/ depende de paquetes EXTERNOS (ARCHITECTURE §3, stdlib only):\n"
        + "\n".join(externos)
    )
