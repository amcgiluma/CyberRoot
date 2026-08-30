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


def test_harness_calibrar_budget_viaje_honesto() -> None:
    """O3 (30/08): la calibración del budget es determinista y dentro del
    presupuesto — el viaje honesto del cap. 0 cuesta SIEMPRE lo mismo (6) y
    nunca supera el budget 12, en ambas variantes."""
    cur = load_curriculum()
    canon = run_seeds.calibrar_budget(0, N, variant="canonical", start=0, curriculum=cur, noise_budget=12)
    práct = run_seeds.calibrar_budget(0, N, variant="practice", start=0, curriculum=cur, noise_budget=12)
    for runs in (canon, práct):
        assert len(runs) == N
        # Viaje honesto determinista: coste idéntico en todas las seeds.
        assert len({r["total_noise"] for r in runs}) == 1
        assert all(r["dentro_presupuesto"] for r in runs)
        assert all(r["errores"] == [] for r in runs)
    # Ambos comparten el coste del viaje honesto (la piel no lo cambia).
    assert {r["total_noise"] for r in canon} == {r["total_noise"] for r in práct}