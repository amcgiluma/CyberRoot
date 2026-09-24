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
            familias = distribucion_familias_run(curriculum, inc.room.canon)
            results.append(
                {
                    "seed": seed,
                    "ok": True,
                    "room_id": inc.room.id,
                    "concepts": sorted(inc.room.concept_pool),
                    "familias": dict(sorted(familias.items())),
                    "familia_dominante": dominancia_familia(familias),
                }
            )
        except UnsolvableRoomError as exc:
            results.append(
                {
                    "seed": seed,
                    "ok": False,
                    "room_id": None,
                    "concepts": [],
                    "familias": {},
                    "familia_dominante": None,
                    "error": str(exc),
                }
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


# ---------------------------------------------------------------------------
# O2 (01/09, Ornstein) — «ánimo de novedad»: distribución de FAMILIAS de
# comando por run. El mapa comando→familia vive en curriculum.json (cada
# concepto `c.<comando>` tiene su `family`); aquí lo consultamos por run de
# la solución canónica (la huella de comandos REAL de la sala).
# ---------------------------------------------------------------------------

def _comandos_de_paso(argv: tuple[str, ...]) -> list[str]:
    """Comandos efectivos de un paso del canon, respetando las tuberías.

    Cada `CanonStep` es una LÍNEA de shell: el 1.er token es un comando y
    cada token tras `|` también (`grep … | wc -l` → [`grep`, `wc`]). Flag y
    rutas no cuentan.
    """
    cmds: list[str] = []
    if not argv:
        return cmds
    cmds.append(argv[0])
    for prev, tok in zip(argv, argv[1:]):
        if prev == "|":
            cmds.append(tok)
    return cmds


def familia_comando(curriculum: Curriculum, comando: str) -> str | None:
    """Familia del comando vía su concepto `c.<comando>` (curriculum.json)."""
    cpt = curriculum.concept(f"c.{comando}")
    return cpt.family if cpt else None


def distribucion_familias_run(
    curriculum: Curriculum, canon: Any
) -> Counter[str]:
    """Distribución de familias de comando que UNA run ejercita (su canon).

    Devuelve un `Counter` familia→nº de comandos de la solución canónica.
    Es la base del «ánimo de novedad»: si el generador repitiera siempre la
    misma familia, el histograma lo delata.
    """
    fams: Counter[str] = Counter()
    for step in canon.steps:
        for cmd in _comandos_de_paso(step.argv):
            fam = familia_comando(curriculum, cmd)
            if fam:
                fams[fam] += 1
    return fams


def dominancia_familia(
    fams: Counter[str], umbral: float = 0.6
) -> tuple[str, float] | None:
    """Si una familia concentra > `umbral` de los comandos de la run, la avisa.

    Devuelve `(familia, fracción)` o None. Umbral AC: >60 % → dominancia.
    """
    total = sum(fams.values())
    if total == 0:
        return None
    fam, n = fams.most_common(1)[0]
    frac = n / total
    if frac > umbral:
        return (fam, round(frac, 3))
    return None


def distribucion_familias_global(results: list[dict[str, Any]]) -> Counter[str]:
    """Histograma global de familias sumando todas las runs."""
    c: Counter[str] = Counter()
    for r in results:
        c.update(r.get("familias", {}))
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



# ---------------------------------------------------------------------------
# S1 Smough 24/09 — calibración micro-karma N=8 (§3.4, §8.6, 🧭45)
# ---------------------------------------------------------------------------
def _karma_delta_from_pm(pm: dict) -> int:
    mk = pm.get("micro_karma") or {}
    if mk.get("blue") == 1:
        return 1
    if mk.get("red") == 1:
        return -1
    tint = pm.get("karma_tint")
    if tint == "blue":
        return 1
    if tint == "red":
        return -1
    return 0

def _ventana_k(deltas: list[int], N: int = 8) -> list[int]:
    out = []
    for i in range(len(deltas)):
        s = sum(deltas[max(0, i - N + 1): i + 1])
        out.append(s)
    return out

def _pct_cruce(Ks: list[int], umbral: int, signo: int) -> float:
    if not Ks:
        return 0.0
    if signo > 0:
        c = sum(1 for k in Ks if k >= umbral)
    else:
        c = sum(1 for k in Ks if k <= -umbral)
    return 100.0 * c / len(Ks)

def _probar_micro_real(curriculum, run_seed: int = 42) -> dict:
    from core.engine.session import abrir_encargo
    from core.engine import build_postmortem
    import re
    out = {}
    for mode, label in [("600", "chmod600"), ("777", "chmod777")]:
        r = abrir_encargo(curriculum, "story.ch5.e1", {"c.ls-la", "c.cat", "c.chmod"}, run_seed=run_seed, volcado_rescatado=True)
        s = r["session"]
        s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
        s.ejecutar(f"chmod {mode} /srv/subestacion/sesiones/pts0")
        pm = build_postmortem(s.shell_dict(), s.state())
        out[label] = _karma_delta_from_pm(pm)
    for spec, label in [("gris:apagados", "chown_gris"), ("root:root", "chown_root")]:
        r = abrir_encargo(curriculum, "story.ch5.e4", {"c.chmod", "c.chown", "c.cat", "c.grep"}, run_seed=run_seed, volcado_rescatado=True)
        s = r["session"]
        s.ejecutar("ls -l /srv/subestacion/sesiones/pts0")
        s.ejecutar(f"chown {spec} /srv/subestacion/sesiones/pts0")
        pm = build_postmortem(s.shell_dict(), s.state())
        out[label] = _karma_delta_from_pm(pm)
    for kill_flag, label in [("-HUP", "hup"), ("-9", "kill")]:
        r = abrir_encargo(curriculum, "story.ch5.e3", {"c.ps", "c.env"}, run_seed=run_seed, volcado_rescatado=True)
        s = r["session"]
        ps_out = s.ejecutar("ps aux").stdout
        m = re.search(r"censo\s+(\d+).*--vigilar-censo", ps_out)
        pid = m.group(1) if m else "424"
        s.ejecutar(f"kill {kill_flag} {pid}")
        pm = build_postmortem(s.shell_dict(), s.state())
        out[label] = _karma_delta_from_pm(pm)
    return out

def calibrar_micro_karma(n: int = 20, N: int = 8, weight_blue: int = 1, weight_red: int = 1, curriculum=None) -> dict:
    ancla = {}
    if curriculum is not None:
        try:
            ancla = _probar_micro_real(curriculum)
        except Exception as e:
            ancla = {"error": str(e)}
    pares = {
        "HUP_vs_KILL": ([weight_blue]*n, [-weight_red]*n),
        "chmod600_vs_777": ([weight_blue]*n, [-weight_red]*n),
        "chown_gris_vs_root": ([weight_blue]*n, [-weight_red]*n),
    }
    perfil_azul = [weight_blue]*n
    perfil_rojo = [-weight_red]*n
    perfil_azul_x3 = [weight_blue*3]*n
    perfil_rojo_x3 = [-weight_red*3]*n
    perfil_azul_w2 = [2]*n
    perfil_rojo_w2 = [-2]*n
    def metrica(deltas):
        Ks = _ventana_k(deltas, N=N)
        return {
            "K_final": Ks[-1] if Ks else 0,
            "K_max": max(Ks) if Ks else 0,
            "K_min": min(Ks) if Ks else 0,
            "pct_K_ge_3": round(_pct_cruce(Ks, 3, 1), 1),
            "pct_K_le_minus3": round(_pct_cruce(Ks, 3, -1), 1),
            "runs_hasta_K_ge3": next((i+1 for i,k in enumerate(Ks) if k>=3), None),
            "runs_hasta_K_le_minus3": next((i+1 for i,k in enumerate(Ks) if k<=-3), None),
            "Ks": Ks,
        }
    result = {
        "N": N,
        "n": n,
        "weight_actual": {"blue": weight_blue, "red": weight_red},
        "ancla_real": ancla,
        "pares": {k: {"azul": metrica(v[0]), "rojo": metrica(v[1])} for k,v in pares.items()},
        "perfil_azul_20": metrica(perfil_azul),
        "perfil_rojo_20": metrica(perfil_rojo),
        "perfil_azul_x3_por_run_hipotesis": metrica(perfil_azul_x3),
        "perfil_rojo_x3_por_run_hipotesis": metrica(perfil_rojo_x3),
        "proyeccion_weight2_azul": metrica(perfil_azul_w2),
        "proyeccion_weight2_rojo": metrica(perfil_rojo_w2),
    }
    return result

def _imprimir_reporte_karma(m: dict) -> None:
    print("\n== Micro-karma N=8 — calibración 20x3 pares ==")
    print(f"n={m['n']}  N={m['N']}  weight actual blue:{m['weight_actual']['blue']} red:{m['weight_actual']['red']}")
    if m.get("ancla_real"):
        print(f"ancla real (1 run por huella, weight 1): {m['ancla_real']}")
    for nombre, par in m["pares"].items():
        a = par["azul"]; r = par["rojo"]
        print(f"[{nombre}] azul: K_final={a['K_final']} max={a['K_max']} pct>=3={a['pct_K_ge_3']}% hasta={a['runs_hasta_K_ge3']} | rojo: K_final={r['K_final']} min={r['K_min']} pct<=-3={r['pct_K_le_minus3']}% hasta={r['runs_hasta_K_le_minus3']}")
    az = m["perfil_azul_20"]; ro = m["perfil_rojo_20"]
    print(f"[perfil 20 azul puro] pct>=3={az['pct_K_ge_3']}% (hasta {az['runs_hasta_K_ge3']} runs) K_final={az['K_final']}")
    print(f"[perfil 20 rojo puro] pct<=-3={ro['pct_K_le_minus3']}% (hasta {ro['runs_hasta_K_le_minus3']} runs) K_final={ro['K_final']}")
    ax3 = m["perfil_azul_x3_por_run_hipotesis"]
    print(f"[hipotesis 3 verbos apilados por run] azul pct>=3={ax3['pct_K_ge_3']}% hasta={ax3['runs_hasta_K_ge3']} K_final={ax3['K_final']} (hoy NO existe: ultimo-manda -> 1 por run)")
    w2a = m["proyeccion_weight2_azul"]; w2r = m["proyeccion_weight2_rojo"]
    print(f"[proyeccion weight=2] azul pct>=3={w2a['pct_K_ge_3']}% hasta={w2a['runs_hasta_K_ge3']} K_final={w2a['K_final']} | rojo pct<=-3={w2r['pct_K_le_minus3']}% hasta={w2r['runs_hasta_K_le_minus3']}")
    print("nota: v1 weight:1 -> 3 runs cruzan umbral 3; weight:2 -> 2 runs. Cumular 3 verbos por run hoy no suma (ultimo-manda). Stock Gris: sin contraste karmico aun (estatico).")

def _imprimir_reporte(
    chapter: int,
    variant: str,
    results: list[dict[str, Any]],
    mismatch: int,
    dist: Counter[str],
    fam_global: Counter[str],
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
    # O2 — «ánimo de novedad»: distribución de familias de comando por run.
    print("\nfamilias de comando por run (del canon — «ánimo de novedad»):")
    for r in results:
        fams = r.get("familias") or {}
        if fams:
            print(f"  seed {r['seed']:<5} {dict(sorted(fams.items()))}")
    print("distribución GLOBAL de familias:")
    for fam, n in sorted(fam_global.items()):
        print(f"  {fam:<12} {n}")
    dominancias = [r for r in results if r.get("familia_dominante")]
    if dominancias:
        print("⚠️  DOMINANCIA (>60 % de los comandos en una familia):")
        for r in dominancias:
            fam, frac = r["familia_dominante"]
            print(f"  seed {r['seed']}: {fam} {frac*100:.1f}%")
    else:
        print("  (ninguna run con familia dominante)")
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
        "--micro-karma",
        action="store_true",
        help="S1 Smough 24/09 — calibración micro-karma N=8: 20×3 pares",
    )
    p.add_argument(
        "--karma-seeds",
        type=int,
        default=20,
        help="n para micro-karma (default 20)",
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
    fam_global = distribucion_familias_global(results)
    elapsed = time.time() - t0

    _imprimir_reporte(
        args.chapter, args.variant, results, mismatch, dist, fam_global, elapsed
    )

    if args.export is not None:
        payload = {
            "chapter": args.chapter,
            "variant": args.variant,
            "seeds": args.seeds,
            "start": args.start,
            "resolubles": sum(1 for r in results if r["ok"]),
            "determinismo_2da_pasada_iguales": misma,
            "conceptos": dict(sorted(dist.items())),
            "familias_global": dict(sorted(fam_global.items())),
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


    if args.micro_karma:
        print("\n== Calibración micro-karma (S1 24/09) ==")
        mk = calibrar_micro_karma(n=args.karma_seeds, N=8, curriculum=curriculum)
        _imprimir_reporte_karma(mk)
        if args.export is not None:
            payload["micro_karma"] = mk
            args.export.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"micro-karma exportado → {args.export}")
    ok = mismatch == 0 and all(r["ok"] for r in results)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())