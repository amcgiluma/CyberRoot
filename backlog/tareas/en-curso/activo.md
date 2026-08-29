# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se mergeó + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** activos desde 27/08
  (gate aprobado el 26/08). Primer día completo de Concilio ejecutado: 27/08.

## Deuda técnica del merge del 27/08 (Gwyn)

- `[HECHO][P1]` (27/08→28/08) **Canje dicts→`common.events.Event`** — SALDADA: entró mergeado en PR #5 esta noche (Smough). Detalle: `../hecho/2026-08.md`.

## Manus (27/08, primer turno real) — fundación narrativa ARCHIVADA

*Líneas `[HECHO]` archivadas por Gwyn el 27/08 en `../hecho/2026-08.md`
(viven ya en main): fichas de voz 6/6, escenarios 6/6, fragmento 1, cap. 0.*
> *(28/08, Gwyndolin: el censo (P1→P2) y el drop del último fragmento (P3)
> vuelven a `pendiente/abierto.md` — un `[PENDIENTE]` vive allí, no aquí.)*
> *(28/08, Gwyn: cap. 1 «Los Muelles», el retoque del cap. 0 (D1) y el mapa del
> Concilio también archivados — ver `../hecho/2026-08.md`.)*

## Asignadas por Gwyndolin (28/08, plan del día) — MERGEADAS por Gwyn (23:00)

- MERGE: PR #4 (O1+O2) → PR #5 (S1+S2+S3) → PR #6 (T1+T2), en el orden ensayado
  por Artorias. Suite tras merges: **316 passed** (225 + deltas 30/51/10).
  Veredictos ✅ de Artorias y detalle de cada tarea: `../hecho/2026-08.md`.
- Decisión de Gwyn al mergear (🧭2, andamiaje de la run 0): **OPCIÓN B** —
  `initial_cwd=/` y el dossier SIEMPRE con rutas completas; las relativas se
  enseñan en el cap. 1. Escrita en DESIGN §6.1; ya es el `default` del scaffold
  del generator (Ornstein la montó como datos: bien a ciegas). PENDIENTE v0.1:
  que generator CONSUMA el scaffold en la sesión que produce.

- `[HECHO][P2]` (28/08→29/08) **M1 prosa↔FS cap. 0** — Manus (03:00 29/08):
  HECHO. El listado tras `cd /srv` muestra UNA entrada (la oficina);
  `/usb` permanece en raíz (canónico para dossier y test). Prosa verificada
  contra `test_session_cap0.py` (3/3 passed) + sesión canónica ejecutada a
  mano byte a byte. Cierre del `[PENDIENTE][P2]` de Oscar (28/08).
- `[HECHO][P1]` (28/08→29/08) **M2 fragmento 2 + cap. 2 «Facturas»** — Manus
  (03:00 29/08): HECHO. Fragmento 2 «La pulsera» `[LISTA]` en
  `FRAGMENTOS.md` (piel HOSP-47-C propuesta por Havel; NHC 47-C-0191 que
  cruza Muelle/Subestación/Vela y sostiene H1+H2) + `CAPITULOS/
  02-facturas.md` `[LISTA]` (beats del cap. 2: la segunda ventana de las
  11:04, 5 encargos `story.ch2.e1`–`e5` con karma, pipes como primera
  sinergia, la Lista nombrada por Ceniza, gancho al cap. 3). Auto-pass
  anti-slop + relectura completa documentados en el worklog. ⚠️ Para el
  integrador: el bloque de terminal del cap. 2 usa pipes que el sandbox aún
  no soporta (nota en el propio fichero); las claves `story.ch2.*` NO están
  aún en `curriculum.json` (dueño Smough cuando toque el cap. 2).

## Asignadas por Gwyndolin (29/08, plan del día) — detalle completo en `../planes/2026/08/29.md`

- `[HECHO][P1]` (29/08, **PR #7**) **O1 Generator consume `curriculum.json` real + opción B como comportamiento (🧭7)** — Ornstein (13:00, `feat/engine`): ✅ **Artorias — VEREDICTO LISTO PARA MERGE** (ensayo de integración, 3 ramas juntas: 342 passed + 1 xfail; gate de datos curriculum OK). La sala toma quest del pool del capítulo y concept_pool del currículo (adiós al cap. 0 hardcodeado); la sesión nace del scaffold (`initial_cwd` del `default`, opción B, `/`) vía `new_session`, no del default de la Shell; `generate(seed,0,curriculum=None)` acepta currículo inyectado. Costura 🧭8 NO resuelta a propósito: test xfail documentado; Gwyn decide (a)/(b) esta noche.
- `[HECHO][P3]` (29/08, **PR #7**) **O2 Harness v0: runner de N seeds** — Ornstein (13:00, `tools/harness/`; O1 cerró con holgura): ✅ **Artorias — LISTO PARA MERGE.** `run_seeds.py --seeds 5` verificado a mano sobre el árbol combinado: 100% resolubles, determinismo byte-idéntico, distribución correcta. AC del plan (50/50 resolubles, 2.ª pasada idéntica) verificado por Ornstein; export JSON + README.
- `[HECHO][P2]` (29/08, **PR #8**) **S1 Pasada GNU sistemática `cp`/`cat`** — Smough (16:00, `feat/sandbox`): ✅ **Artorias — LISTO PARA MERGE.** Cierra los 2 `[BUG][P3]` de Havel (cat fichero/ → Not a directory exit 1; cp dir → omitting directory exit 1); tests golden en negativo contrastados contra coreutils real; sin regresión en `test_session_cap0.py` (`mtime` sin `-p` queda como limitación documentada).
- `[HECHO][P2]` (29/08, **PR #8**) **S2 REPL `python -m core.sandbox`** — Smough (16:00, `feat/sandbox`): ✅ **Artorias — LISTO PARA MERGE.** `__main__.py` con prompt diegético, una línea = un comando, stdout/stderr separados, exit code cuando ≠0; `run_repl` reutilizable y testeable sin TTY; no toca `__init__.py` de sandbox (re-export de Seath en T1). Smoke técnico real: la sesión canónica (ls→cat→cp→ls /usb) se juega en el REPL; `test_repl.py` 4/4.
- `[HECHO][P2]` (29/08, **PR #9**) **T1 Fachadas uniformes** — Seath (19:00, `feat/meta-ui`): ✅ **Artorias — LISTO PARA MERGE.** `from core.state import GameState, save_game, load_game` y `from core.sandbox import Shell` verificados desde raíz sobre el árbol combinado; sin circulares.
- `[HECHO][P2]` (29/08, **PR #9**) **T2 progression v0: primer unlock por competencia** — Seath (19:00, `feat/meta-ui`): ✅ **Artorias — LISTO PARA MERGE.** `evaluate_unlocks` importa y existe; respeta §4.2 (unlock por competencia, no grind); roundtrip usando `GameState.knowledge`.
- `[EN CURSO][P2]` (29/08, noche) **M1 Fragmento 3 (contrato de alquiler a nombre de nadie)** — Manus (03:00 del 30/08): `[LISTA]` en `FRAGMENTOS.md`, formato Souls, H1/H2, sin contradecir fragmentos 1-2. Dirección de Gwyn (28/08).
- `[EN CURSO][P2]` (29/08, noche) **M2 Capítulo 3 «Bombas» (beats 5–6)** — Manus (03:00 del 30/08): 4-5 encargos `story.ch3.e1–eN` con tints del descenso del Acto 2, escalada Umbral→Faro (regla de la luz §6.0) y la grieta de Ceniza PLANTADA (beat 6 §2.5), sin resolver. AC en el plan.
