"""Guardián nº 3 (ARCHITECTURE §1.3): prohibido `random` global en `src/core/`.

Toda aleatoriedad del juego pasa por `core/common/rng.Rng(seed)` para que las
runs sean reproducibles y los bugs, reproducibles por el harness. Un
`import random` suelto equivale a sembrar caos no-reproducible.
Basado en AST. Cambiar/quitar este test exige propuesta en backlog/mejoras/.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2]
CORE_DIR = SRC_DIR / "core"


def test_core_sin_random_global() -> None:
    assert CORE_DIR.is_dir(), f"No existe {CORE_DIR}"
    violaciones: list[str] = []
    for path in sorted(CORE_DIR.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "random" or alias.name.startswith("random."):
                        violaciones.append(f"{path.relative_to(SRC_DIR)}:{node.lineno}")
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                if node.module == "random" or (node.module or "").startswith("random."):
                    violaciones.append(f"{path.relative_to(SRC_DIR)}:{node.lineno}")
    assert not violaciones, (
        "`import random` detectado en src/core/ (ARCHITECTURE §1.3 — usa "
        "common/rng.Rng(seed)):\n" + "\n".join(sorted(set(violaciones)))
    )
