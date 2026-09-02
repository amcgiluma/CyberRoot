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


# ---------------------------------------------------------------------------
# O2 (01/09) — «ánimo de novedad»: distribución de familias de comando por run
# ---------------------------------------------------------------------------

def test_distribucion_familias_run_cap0() -> None:
    """El canon del cap. 0 son 5 comandos de la familia navegacion."""
    cur = load_curriculum()
    inc = run_seeds.generate(7, 0, variant="canonical", curriculum=cur)
    fams = run_seeds.distribucion_familias_run(cur, inc.room.canon)
    assert dict(fams) == {"navegacion": 5}


def test_dominancia_familia_detecta_monofamilia() -> None:
    """100 % navegacion en el cap. 0 ⇒ dominancia (>60 %) avisada."""
    from collections import Counter

    assert run_seeds.dominancia_familia(Counter({"navegacion": 5})) == (
        "navegacion",
        1.0,
    )
    # Una mezcla equilibrada NO domina (2/4 = 50 % ≤ 60 %).
    assert run_seeds.dominancia_familia(Counter({"texto": 2, "red": 2})) is None


def test_tuberia_cuenta_ambos_comandos() -> None:
    """`grep … | wc -l` cuenta grep Y wc (ambos de la familia texto)."""
    cur = load_curriculum()
    # Reutilizamos la golden del cap. 2 (prosa "11:04"): la tubería viaja en
    # UN CanonStep.
    pasos = run_seeds._comandos_de_paso(("grep", "11:04", "f.log", "|", "wc", "-l"))
    assert pasos == ["grep", "wc"]
    assert all(run_seeds.familia_comando(cur, c) == "texto" for c in pasos)


def test_global_familias_desde_run_batch() -> None:
    """El agregado de familias se computa de los resultados enriquecidos."""
    cur = load_curriculum()
    results = run_seeds.run_batch(0, 4, variant="canonical", start=0, curriculum=cur)
    assert all(r["ok"] for r in results)
    # Cada run enganchó su distribución y (cap. 0) avisó dominancia.
    assert all(r["familias"] == {"navegacion": 5} for r in results)
    assert all(r["familia_dominante"] is not None for r in results)
    g = run_seeds.distribucion_familias_global(results)
    assert g["navegacion"] == 4 * 5