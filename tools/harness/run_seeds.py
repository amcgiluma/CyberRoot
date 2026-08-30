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
    new_session,
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


def viaje_honesto(
    seed: int,
    chapter: int,
    variant: str,
    curriculum: Curriculum,
    noise_budget: int,
) -> dict[str, Any]:
    """Ejecuta la solución canónica sobre la sesión sembrada y mide su ruido.

    El «viaje honesto» (deshacer la run bien, sin errores) genera la
    incursión y la resuelve con su SECUENCIA CANÓNICA (`room.canon.steps`).
    Devuelve métricas de calibración del budget de ruido (§6.0.2 / 🧭6):
    `total_noise` del viaje honesto, si algún paso falló (primer error), y la
    holgura respecto a `noise_budget` (misma unidad, 🧭10).

    Determinsta: la secuencia canónica es fija por sala, así que el coste del
    viaje honesto de UNA seed es igual en todas las que resevan la misma
    sala; lo que varía entre seeds son la piel (decoys en `practice`) y el
    error de sintaxis/flag que el jugador NO comete al ir bien.
    """
    inc = generate(seed, chapter, variant=variant, curriculum=curriculum)
    shell = new_session(inc)
    errores: list[int] = []
    for step in inc.room.canon.steps:
        line = " ".join(step.argv)
        result = shell.execute(line)
        if result.exit_code != step.expect_exit:
            errores.append(int(step.expect_exit))
    return {
        "seed": seed,
        "variant": variant,
        "total_noise": shell.total_noise,
        "errores": errores,
        "dentro_presupuesto": shell.total_noise <= noise_budget,
    }


def calibrar_budget(
    chapter: int,
    n_seeds: int,
    *,
    variant: str,
    start: int,
    curriculum: Curriculum,
    noise_budget: int,
) -> list[dict[str, Any]]:
    """N seeds × viaje honesto → métricas de calibración del budget (O3)."""
    return [
        viaje_honesto(seed, chapter, variant, curriculum, noise_budget)
        for seed in range(start, start + n_seeds)
    ]


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
    p.add_argument(
        "--calibrar",
        action="store_true",
        help="O3: 50 seeds × {canonical, practice} → distribución del RUIO del "
        "viaje honesto vs noise_budget y frecuencia del primer error (calibración 🧭6). "
        "Combínese con --export para la tabla JSON.",
    )
    p.add_argument(
        "--budget",
        type=int,
        default=12,
        help="noise_budget de la sala (misma unidad que total_noise, 🧭10; default 12 ⚠️ v1)",
    )
    args = p.parse_args(argv)

    if args.chapter < 0:
        p.error("chapter debe ser >= 0")
    if args.seeds <= 0:
        p.error("seeds debe ser > 0")

    curriculum = load_curriculum()
    t0 = time.time()
    payload: dict[str, Any] = {}
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

    if args.calibrar:
        print("\n== Calibración del budget (O3) — viaje honesto vs ruido ==")
        cal = {"noise_budget": args.budget, "variants": {}}
        for variant in ("canonical", "practice"):
            runs = calibrar_budget(
                args.chapter,
                args.seeds,
                variant=variant,
                start=args.start,
                curriculum=curriculum,
                noise_budget=args.budget,
            )
            totales = Counter(r["total_noise"] for r in runs)
            excede = sum(1 for r in runs if not r["dentro_presupuesto"])
            con_error = sum(1 for r in runs if r["errores"])
            print(f"[{variant}] total_noise del viaje honesto: {dict(sorted(totales.items()))}")
            print(f"[{variant}] % que excede budget {args.budget}: {excede}/{len(runs)} "
                  f"({100.0*excede/len(runs):.1f}%)")
            print(f"[{variant}] runs con error en la secuencia canónica: {con_error}/{len(runs)}")
            cal["variants"][variant] = {
                "distribucion_total_noise": dict(sorted(totales.items())),
                "excede_budget": excede,
                "con_error_en_canonica": con_error,
                "budget": args.budget,
            }
        if args.export is not None:
            payload["calibracion_budget"] = cal
            args.export.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"calibración exportada → {args.export}")

    ok = mismatch == 0 and all(r["ok"] for r in results)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())