"""test_rng.py — especificación determinista de Rng (DESIGN §4.5, ARCHITECTURE §1.3).

Garantías bajo test:
- Reproducibilidad TOTAL: misma seed ⇒ misma secuencia en cualquier proceso,
  plataforma o versión de CPython. Incluye el test CRÍTICO cross-proceso con
  PYTHONHASHSEED distinto (criterio duro del plan 27/08).
- Seeds str/bytes via sha256, JAMÁS via hash() (PYTHONHASHSEED).
- API pura de sub-sistemas (fork/state) sin semántica de juego.

Los literales "dorados" se generaron con ./.venv/bin/python ejecutando el
código real (splitmix64), NO se inventaron.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

from core.common.rng import Rng, mix_seeds

# --------------------------------------------------------------------------
# Constantes. Literales dorados calculados EJECUTANDO la implementación real:
#   seed = "cyberroot-golden-seed-v1", primeras 20 uint64(), luego 5 float(),
#   luego 5 below(6). El subprocess imprime exactamente la tupla (u, f, b).
# --------------------------------------------------------------------------
GOLDEN_U64 = [
    7791427192335564746, 11378700479169487196, 1601472935718763439,
    3388083698990874357, 422664715005726371, 8509645662479600110,
    4023451254465407885, 17180453079907469471, 8643430592673119572,
    5829135799206375382, 4499018531933301098, 16090028483906235040,
    16208246197072574358, 13984508503883604776, 15506532384929275366,
    17831821246080303652, 15317099870342293847, 14657339529963046800,
    4594773340942937393, 4879350763168427429,
]
GOLDEN_FLOATS = [0.7449670520458908, 0.022862179105559544, 0.6802351974861405,
                 0.55538851657137, 0.7036910614244821]
GOLDEN_BELOW = [3, 4, 3, 3, 5]
GOLDEN_CROSS = (list(GOLDEN_U64), list(GOLDEN_FLOATS), list(GOLDEN_BELOW))

# Distintos PYTHONHASHSEED explícitos para demostrar independencia de hash().
CROSS_HASH_SEEDS = (1, 424_242)

_SRC_DIR = Path(__file__).resolve().parents[3] / "src"

# Snippet idéntico en ambos subprocesos: imprime una única línea (repr) con
# u64s + floats + below(6) para seed fija.
_CROSS_SNIPPET = (
    "from core.common.rng import Rng\n"
    "def probe():\n"
    '    rng = Rng("cyberroot-golden-seed-v1")\n'
    "    u = [rng.uint64() for _ in range(20)]\n"
    "    f = [rng.float() for _ in range(5)]\n"
    "    b = [rng.below(6) for _ in range(5)]\n"
    "    return (u, f, b)\n"
    "print(repr(probe()))\n"
)


def _run_cross_probe(hash_seed: int) -> str:
    """Ejecuta el snippet como subproceso con PYTHONHASHSEED dado."""
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = str(hash_seed)
    env["PYTHONPATH"] = str(_SRC_DIR)
    proc = subprocess.run(
        [sys.executable, "-c", _CROSS_SNIPPET],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_SRC_DIR.parent),
        check=True,
    )
    return proc.stdout


# --------------------------------------------------------------------------
# 1. Determinismo in-proceso
# --------------------------------------------------------------------------
def test_determinismo_misma_seed_primeras_100_uint64() -> None:
    a = Rng("cyberroot-golden-seed-v1")
    b = Rng("cyberroot-golden-seed-v1")
    assert [a.uint64() for _ in range(100)] == [b.uint64() for _ in range(100)]


# --------------------------------------------------------------------------
# 2. REPRODUCIBILIDAD CROSS-PROCESO (criterio duro del plan 27/08)
# --------------------------------------------------------------------------
def test_cross_proceso_pythonhashseed_distinto_byte_identico() -> None:
    outs = {h: _run_cross_probe(h) for h in CROSS_HASH_SEEDS}
    # Byte a byte: no depende en absoluto de PYTHONHASHSEED.
    assert outs[CROSS_HASH_SEEDS[0]] == outs[CROSS_HASH_SEEDS[1]]
    assert outs[CROSS_HASH_SEEDS[0]].strip() == outs[CROSS_HASH_SEEDS[1]].strip()


def test_cross_proceso_contra_literales_dorados() -> None:
    parsed = ast.literal_eval(_run_cross_probe(CROSS_HASH_SEEDS[0]).strip())
    assert parsed == GOLDEN_CROSS


# --------------------------------------------------------------------------
# 3. Estadístico ligero determinista
# --------------------------------------------------------------------------
def test_float_10k_en_cero_uno_media_cercana() -> None:
    rng = Rng(20260827)
    vals = [rng.float() for _ in range(10_000)]
    assert all(0.0 <= v < 1.0 for v in vals)
    assert max(vals) < 1.0
    mean = sum(vals) / len(vals)
    assert 0.45 < mean < 0.55


def test_integers_1_6_barrido_de_seeds_cubre_dominio() -> None:
    seen = set()
    for seed in range(500):
        seen.add(Rng(seed).integers(1, 6))
    assert seen == {1, 2, 3, 4, 5, 6}


# --------------------------------------------------------------------------
# 4. Sin sesgo material en below(dado) sobre tiradas deterministas
# --------------------------------------------------------------------------
def test_below_6_60k_sin_desvio_material() -> None:
    rng = Rng(20260827)
    n = 60_000
    buckets = [0] * 6
    for _ in range(n):
        buckets[rng.below(6)] += 1
    ideal = n / 6
    tol = 0.05
    assert all(abs(c - ideal) <= tol * ideal for c in buckets), buckets


# --------------------------------------------------------------------------
# 5. shuffle pura + sample sin repetición + errores de API
# --------------------------------------------------------------------------
def test_shuffle_es_pura_y_permutacion_determinista() -> None:
    src = list(range(52))
    original = list(src)
    rng = Rng(7)
    out1 = rng.shuffle(src)
    assert src == original, "shuffle NO debe mutar la entrada"
    assert out1 is not src
    assert len(out1) == len(src)
    assert sorted(out1) == sorted(src)
    assert set(out1) == set(src)
    rng2 = Rng(7)
    assert rng2.shuffle(original) == out1


def test_sample_sin_repeticion_y_determinista() -> None:
    pop = list(range(100))
    a = Rng(11).sample(pop, 10)
    b = Rng(11).sample(pop, 10)
    assert len(a) == len(set(a)) == 10
    assert set(a).issubset(pop)
    assert a == b  # determinista dado (seed, estado): dos instancias iguales


def test_sample_k_igual_len_es_permutacion_completa() -> None:
    src = list(range(30))
    out = Rng(20260827).sample(src, len(src))
    assert sorted(out) == sorted(src)


def test_errores_valueerror_api() -> None:
    rng = Rng(1)
    with pytest.raises(ValueError):
        rng.below(0)
    with pytest.raises(ValueError):
        rng.below(-3)
    with pytest.raises(ValueError):
        rng.integers(5, 2)
    with pytest.raises(ValueError):
        rng.choice([])
    with pytest.raises(ValueError):
        rng.sample([1, 2, 3], -1)
    with pytest.raises(ValueError):
        rng.sample([1, 2], 3)


# --------------------------------------------------------------------------
# 6. fork(): derivada reproducible desde el estado padre
# --------------------------------------------------------------------------
def test_fork_hija_distinta_del_padre() -> None:
    parent = Rng(5)
    child = parent.fork("mapa")
    assert child.uint64() != parent.uint64()


def test_fork_reproducible_mismo_estado_padre() -> None:
    p1 = Rng(5)
    c1 = p1.fork("mapa")  # no consume tiradas del padre
    p2 = Rng.from_state(p1.state)
    c2 = p2.fork("mapa")
    assert [c1.uint64() for _ in range(5)] == [c2.uint64() for _ in range(5)]


def test_fork_labels_distintos_secuencias_distintas() -> None:
    rng = Rng(5)
    a = rng.fork("mapa")
    b = rng.fork("vigilancia")
    assert [a.uint64() for _ in range(8)] != [b.uint64() for _ in range(8)]


def test_fork_depende_del_estado_actual_no_solo_de_la_seed() -> None:
    rng = Rng(5)
    inicial = rng.fork("x")
    for _ in range(5):
        rng.uint64()
    avanzado = rng.fork("x")
    assert [inicial.uint64() for _ in range(8)] != [avanzado.uint64() for _ in range(8)]


# --------------------------------------------------------------------------
# 7. state/from_state ida-y-vuelta: la secuencia CONTINÚA, no reinicia
# --------------------------------------------------------------------------
def test_state_from_state_continua_secuencia() -> None:
    rng = Rng("save-me")
    for _ in range(50):
        rng.uint64()
    saved = rng.state
    secuencia_original = [rng.integers(1, 100) for _ in range(10)]

    r2 = Rng.from_state(saved)
    secuencia_reanudada = [r2.integers(1, 100) for _ in range(10)]
    assert secuencia_reanudada == secuencia_original

    # No reinicia al principio: desde el estado guardado no se repite Rng(seed).
    r3 = Rng.from_state(saved)
    assert r3.integers(1, 100) != Rng("save-me").integers(1, 100)


# --------------------------------------------------------------------------
# 8. Seeds borde: válidas y deterministas; tipos inválidos → TypeError
# --------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [0, -5, -2**70, b"", "", "semilla-ñ", b"\x00\xff"])
def test_seeds_borde_validas_y_deterministas(seed: int | str | bytes) -> None:
    a = Rng(seed)
    b = Rng(seed)
    assert [a.uint64() for _ in range(10)] == [b.uint64() for _ in range(10)]


@pytest.mark.parametrize("bad", [None, 3.5, True, object()])
def test_seeds_tipos_invalidos_typeerror(bad: object) -> None:
    with pytest.raises(TypeError):
        Rng(bad)  # type: ignore[arg-type]


# --------------------------------------------------------------------------
# 9. mix_seeds: determinista y distinta de sus partes (no requiere conmutar)
# --------------------------------------------------------------------------
def test_mix_seeds_determinista_y_distinta_de_las_partes() -> None:
    assert mix_seeds(1, "x") == mix_seeds(1, "x")
    # No se exige conmutatividad — el orden importa.
    assert mix_seeds(1, "x") != mix_seeds("x", 1)
    # Distinta de seedear con cada parte por separado.
    mix = mix_seeds(7, "zz")
    assert Rng(mix).uint64() != Rng(7).uint64()
    assert Rng(mix).uint64() != Rng("zz").uint64()