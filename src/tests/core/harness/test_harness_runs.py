"""Smoke del harness v0 (O2, 29/08, Ornstein): el runner de N seeds es
consumible en CI y cumple su AC: 100 % resolubles y determinismo perfecto."""
from __future__ import annotations

import sys
from pathlib import Path

from core.curriculum import load_curriculum

_REPO_ROOT = Path(__file__).resolve().parents[4]
_HARNESS = _REPO_ROOT / "tools" / "harness"
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))

import run_seeds  # noqa: E402

N = 8


def test_harness_50_por_ciento_resolubles() -> None:
    cur = load_curriculum()
    results = run_seeds.run_batch(0, N, variant="canonical", start=0, curriculum=cur)
    assert len(results) == N
    assert all(r["ok"] for r in results), [r for r in results if not r["ok"]]
    # El pool de conceptos viene del curriculum en todas.
    assert all(set(r["concepts"]) == {"c.cat", "c.cd", "c.cp", "c.ls"} for r in results)


def test_harness_determinismo_2da_pasada() -> None:
    cur = load_curriculum()
    iguales = run_seeds.determinismo_2da_pasada(0, N, variant="canonical", start=0, curriculum=cur)
    assert iguales == N