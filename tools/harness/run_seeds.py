#!/usr/bin/env python3
"""run_seeds.py — harness v0: runner de N seeds (O2, 29/08, Ornstein).

Corre el generador sobre N seeds del cap. 0 y saca tres métricas:
  - % resolubles (una sala irresoluble = `UnsolvableRoomError` = bug, no `0%`);
  - determinismo (2.ª pasada byte-idéntica: misma seed ⇒ misma Incursion);
  - distribución de conceptos por run (base para 🧭6, la calibración del
    budget de ruido y el «ánimo de novedad» de Havel).

Uso:
    PYTHONPATH=src .venv/bin/python tools/harness/run_seeds.py \
        --chapter 0 --seeds 50 [--variant canonical] [--start 0] [--export out.json]

Vive fuera de `src/` (raíz, per propuesta del Arquitecto): consume la API de
`core.generator`, no el motor de render. Solo stdlib.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

# Permitir ejecutarlo desde la raíz del repo sin instalación.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from core.curriculum import Curriculum, load_curriculum  # noqa: E402
from core.generator import (  # noqa: E402
    UnsolvableRoomError,
    generate,
    validate_incursion,
)


def run_batch(
    chapter: int,
    n_seeds: int,
    *,
    variant: str,
    start: int,
    curriculum: Curriculum,
) -> list[dict[str, Any]]:
    """Genera y valida N seeds; una irresoluble se registra, no rompe el batch."""
    results: list[dict[str, Any]] = []
    for i in range(n_seeds):
        seed = start + i
        try:
            inc = generate(seed, chapter, variant=variant, curriculum=curriculum)
            validate_incursion(inc)
            results.append(
                {
                    "seed": seed,
                    "ok": True,
                    "room_id": inc.room.id,
                    "concepts": sorted(inc.room.concept_pool),
                }
            )
        except UnsolvableRoomError as exc:
            results.append(
                {"seed": seed, "ok": False, "room_id": None, "concepts": [], "error": str(exc)}
            )
    return results


def determinismo_2da_pasada(
    chapter: int,
    n_seeds: int,
    *,
    variant: str,
    start: int,
    curriculum: Curriculum,
) -> int:
    """Cuántas seeds dan EXACTAMENTE la misma Incursion en una 2.ª generación."""
    iguales = 0
    for i in range(n_seeds):
        seed = start + i
        a = generate(seed, chapter, variant=variant, curriculum=curriculum).to_dict()
        b = generate(seed, chapter, variant=variant, curriculum=curriculum).to_dict()
        iguales += 1 if a == b else 0
    return iguales


def distribucion_conceptos(results: list[dict[str, Any]]) -> Counter[str]:
    """Conteo de veces que cada concepto aparece en el pool de las salas."""
    c: Counter[str] = Counter()
    for r in results:
        for cpt in r.get("concepts", []):
            c[cpt] += 1
    return c


def _imprimir_reporte(
    chapter: int,
    variant: str,
    results: list[dict[str, Any]],
    mismatch: int,
    dist: Counter[str],
    elapsed: float,
) -> None:
    total = len(results)
    resolubles = sum(1 for r in results if r["ok"])
    pct = 100.0 * resolubles / total if total else 0.0
    print(f"== CyberRoot harness v0 — cap. {chapter} · variante {variant} ==")
    print(f"seeds     : {total}")
    print(f"resolubles: {resolubles}/{total}  ({pct:.1f}%)")
    print(f"determ.   : {total - mismatch}/{total} byte-idénticas (2.ª pasada)")
    print(f"tiempo    : {elapsed:.2f}s")
    print("conceptos (veces en el pool de las salas):")
    for cpt, n in sorted(dist.items()):
        print(f"  {cpt:<12} {n}")
    if mismatch:
        print("⚠️  ALERTA: hay seeds cuya 2.ª pasada difiere — inviable determinismo.")
    if resolubles < total:
        print("⚠️  ALERTA: hay salas irresolubles — bug de generación, revisar.")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Harness v0: N seeds del generador.")
    p.add_argument("--chapter", type=int, default=0, help="capítulo (solo 0 en v0)")
    p.add_argument("--seeds", type=int, default=50, help="número de seeds")
    p.add_argument("--variant", choices=("canonical", "practice"), default="canonical")
    p.add_argument("--start", type=int, default=0, help="primera seed (offset)")
    p.add_argument(
        "--export",
        type=Path,
        default=None,
        help="ruta .json opcional para volcar los resultados y métricas",
    )
    args = p.parse_args(argv)

    if args.chapter < 0:
        p.error("chapter debe ser >= 0")
    if args.seeds <= 0:
        p.error("seeds debe ser > 0")

    curriculum = load_curriculum()
    t0 = time.time()
    results = run_batch(
        args.chapter, args.seeds, variant=args.variant, start=args.start, curriculum=curriculum
    )
    misma = determinismo_2da_pasada(
        args.chapter, args.seeds, variant=args.variant, start=args.start, curriculum=curriculum
    )
    mismatch = args.seeds - misma
    dist = distribucion_conceptos(results)
    elapsed = time.time() - t0

    _imprimir_reporte(args.chapter, args.variant, results, mismatch, dist, elapsed)

    if args.export is not None:
        payload = {
            "chapter": args.chapter,
            "variant": args.variant,
            "seeds": args.seeds,
            "start": args.start,
            "resolubles": sum(1 for r in results if r["ok"]),
            "determinismo_2da_pasada_iguales": misma,
            "conceptos": dict(sorted(dist.items())),
            "runs": results,
        }
        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"exportado → {args.export}")
    ok = mismatch == 0 and all(r["ok"] for r in results)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())