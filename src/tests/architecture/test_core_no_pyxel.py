"""Guardián nº 1 de la frontera (ARCHITECTURE §1.1): `core/` NO importa pyxel JAMÁS.

Basado en AST (los comentarios no engañan al escáner). Si este test falla,
alguien está metiendo la capa de render dentro del core — moverla a `src/render/`.
Cambiar/quitar este test exige propuesta en backlog/mejoras/pendiente/.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2]
CORE_DIR = SRC_DIR / "core"


def _imports_of(tree: ast.AST) -> list[str]:
    """Nombres de módulo raíz importados en el árbol (incluye imports locales)."""
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            # Solo imports absolutos; los relativos no salen del paquete.
            if node.module:
                found.append(node.module)
    return found


def _py_files(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*.py") if "__pycache__" not in p.parts)


def test_core_no_importa_pyxel() -> None:
    assert CORE_DIR.is_dir(), f"No existe {CORE_DIR} — ¿se movió el árbol src/core?"
    violaciones: list[str] = []
    for path in _py_files(CORE_DIR):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for module in _imports_of(tree):
            root = module.split(".")[0]
            if root == "pyxel":
                violaciones.append(f"{path.relative_to(SRC_DIR)}: import {module}")
    assert not violaciones, (
        "La frontera core/render está rota (ARCHITECTURE §1.1):\n" + "\n".join(violaciones)
    )
