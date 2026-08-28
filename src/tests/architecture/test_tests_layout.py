"""Guardián del layout de tests (tarea O1, 28/08 — regla propuesta por Artorias).

Histórico: el PR #3 colocó tests en `src/assets/tests/` con un `__init__.py`
propio → DOS paquetes `tests` en el árbol → 13 errores de colección al
integrar las ramas. Esta regla lo impide ESTRUCTURALMENTE: los tests viven
SIEMPRE en `src/tests/<módulo>/...` espejando el árbol de `src/`, y ningún
directorio `tests` fuera de `src/tests/` contiene `.py` (ni siquiera vacío
con `__init__.py`). Cambiar/quitar este test exige propuesta en
backlog/mejoras/pendiente/ — es constitución del repo, no un capricho.
"""

from __future__ import annotations

import os
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2]
TESTS_DIR = SRC_DIR / "tests"


def test_src_tests_existe_y_es_el_canonico() -> None:
    assert TESTS_DIR.is_dir(), f"No existe {TESTS_DIR} — ¿se movió el árbol src/tests?"


def test_ningun_directorio_tests_fuera_de_src_tests() -> None:
    """Ningún `tests` anidado en src/ fuera de src/tests/ contiene ficheros.

    Comprueba tanto ficheros Python (colección rota) como cualquier otro
    (fixtures olvidados al migrar). `src/tests/` en sí queda excluido porque
    ES la ubicación canónica.
    """
    assert TESTS_DIR.is_dir()
    intrusos: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(SRC_DIR):
        here = Path(dirpath)
        if here == TESTS_DIR or TESTS_DIR not in here.parents:
            continue
        # No descendemos por las subcarpetas de src/tests (corte de poda).
        if here.name == "tests" and filenames:
            intrusos.append(
                f"{here.relative_to(SRC_DIR)}/ ({len(filenames)} ficheros: "
                + ", ".join(sorted(filenames)[:5])
                + ("..." if len(filenames) > 5 else "")
                + ")"
            )
    assert not intrusos, (
        "Regla de convención de tests (src/tests/README.md) VIOLADA: hay\n"
        "directorios `tests` fuera de src/tests/ con ficheros. Mueve esos\n"
        "tests espejando el árbol (src/tests/<modulo>/...) y borra el resto.\n"
        "Historial: esto causó 13 errores de colección en el PR #3.\n"
        "Intrusos:\n  " + "\n  ".join(intrusos)
    )


def test_assets_tests_no_deja_restos() -> None:
    """Regresión puntual de la migración O1 (28/08): src/assets/tests no existe."""
    assert not (SRC_DIR / "assets" / "tests").exists(), (
        "src/assets/tests/ ha vuelto a existir: los tests de assets viven en "
        "src/tests/assets/ (convención única de tests, tarea O1 del 28/08)."
    )
