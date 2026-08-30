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

## Asignadas por Gwyndolin (29/08, plan del día) — MERGEADAS por Gwyn (23:00)

> Las 6 líneas `[HECHO]` de ayer (O1/O2 PR#7, S1/S2 PR#8, T1/T2 PR#9) fueron
> archivadas por Gwyn en `../hecho/2026-08.md`. Suite tras los 3 merges:
> **342 passed + 1 xfail** (deltas cuadrados). Ramas `feat/*` borradas;
> PRs MERGED en GitHub.

## Asignadas por Gwyndolin (30/08, plan del día) — ver `../planes/2026/08/30.md`

- `[HECHO][P1]` (30/08) **O1 — Materializar 🧭8=(b): prereqs evaluados al ABRIR el encargo** — Ornstein (13:00, `feat/engine`): la sala sigue contratando `story.ch1.e1` (escenario), pero la evaluación de prereqs vive como API del contrato, llamada al abrir — nunca en `generate()`. AC: `test_costura_navig8.py` pasa de xfail a VERDE (0 xfails al cerrar el día). **ARTORIAS ✅ (PR #10)**: `Contract.prereqs_met` verificada en el ensayo combinado; el único xfail de la costura murió (suite 385 passed, 0 xFailed sin errores de colección). Cumple 🧭8=(b): la API evalua al abrir, `generate()` intacta.
- `[HECHO][P2]` (30/08) **O2 — Post-mortem v0: el Auditor lee el HISTORIAL real (factura GNU + comando que delata, en la misma unidad que el budget, 🧭10)** — Ornstein (13:00, `feat/engine`, nuevo `postmortem.py`): `build_postmortem(shell_dict, state)`; función pura headless. Origen: idea de Havel 28/08 + dirección #2 de Gwyn. **ARTORIAS ✅ (PR #10)**: smoke real ejecutado; `build_postmortem` devuelve `factura`/`total_noise`/`noise_budget`/`dentro_presupuesto`/`auditor` en la misma unidad (🧭10 satisfecha). 8 tests verdes.
- `[HECHO][P2]` (30/08) **S1 — Tuberías en el sandbox + `grep`/`wc` (cap. 2)** — Smough (16:00, `feat/sandbox`): una tubería `cmd1 | cmd2`, rechazo didáctico `&&`/`;` se mantiene, ruido por comando de la tubería. AC: `grep 11:04 centralita/turnos/turno.log | wc -l` (línea EXACTA del cap. 2) golden contra GNU real. **ARTORIAS ✅ (PR #11)**: golden jugado a mano (→ `2`, exit 0), ruido de tubería 2+1=3, `&&` sigue rechazado (exit 2). Sin regresión cap. 0.
- `[HECHO][P2]` (30/08) **S2 — `story.ch2.*` al currículo (cap. 2 «Facturas» de Manus)** — Smough (16:00, `feat/sandbox` + `src/data/`): 5 quests (`e1`–`e5`, 2 azules/1 gris/1 rojo/1 cierre) + conceptos mínimos (`c.grep`/`c.wc`/`c.pipe`). AC: `load_curriculum` + validador en negativo. **ARTORIAS ✅ (PR #11)**: gate de datos OK — 14 conceptos / 11 quests; ch2 e1–e5 con tints blue/blue/grey/red/grey y sinergia `c.pipe`; validador pasa en positivo.
- `[HECHO][P2]` (30/08) **T1 — El save recuerda CUÁNDO dominaste (meta de unlock + `resumen_competencia`)** — Seath (19:00, `feat/meta-ui`): datos para el eco de 🧭9 (la FORMA la decide Gwyn; sin UI hoy). Roundtrip + idempotencia intactas. **ARTORIAS ✅ (PR #12)**: roundtrip de `mastered` exitoso, compat v1 (save previo → `{}`), idempotencia cubierta. 31 tests de progression+state verdes.
- `[HECHO][P3]` (30/08) **O3 — Calibración del budget con harness (OPCIONAL)** — Ornstein: 50 seeds × {canonical, practice}, distribución de ruido + propuesta de definición de «primer error» (decide Gwyn/Oscar). Origen: `[PENDIENTE][P2]` de Oscar 29/08. **ARTORIAS ✅ (PR #10)**: harness 5/5 resolubles y determinismo byte-idéntico verificado; viaje honesto total_noise=6 constante (margen limpio sobre budget 12). Definición de «primer error» queda para Gwyn/Oscar (decisión de diseño, no técnica).
- `[HECHO][P3]` (30/08) **T2 — Mecanismo de logros por factura («Cero rastro», «Mano de seda»; OPCIONAL)** — Seath: logros §7.6 como datos del save. Origen: idea de Havel 28/08. **ARTORIAS ✅ (PR #12)**: `evaluate_logros` con 2 logros, persistencia roundtrip, umbral calibrable (`UMBRAL_CERO_RASTRO=4` — ⚠️ quedará por calibrar con O3 del harness). *(Gwyn 23:00: candidata a recalibrado con la definición de «primer error» — ver nota del mismo día en este fichero.)*

<!-- archivadas por Gwyn el 30/08 23:00 → ver `../hecho/2026-08.md` (PRs #10/#11/#12 + M1/M2 de Manus) -->

### Manus (03:00 del 30/08) — pendientes de merge por Gwyn

- `[HECHO][P2]` (29/08, noche) **M1 Fragmento 3 (contrato de alquiler a nombre de nadie)** — Manus (03:00 del 30/08): HECHO. `[LISTA]` en `FRAGMENTOS.md`, formato Souls, H1/H2, sin contradecir fragmentos 1-2. Detalle: `../historia/INDICE.md`.
- `[HECHO][P2]` (29/08, noche) **M2 Capítulo 3 «Bombas» (beats 5–6)** — Manus (03:00 del 30/08): HECHO. 5 encargos `story.ch3.e1`–`e5` (1 azul, 1 gris, 2 rojos, 1 de cierre) con tints del descenso del Acto 2, escalada Umbral→Faro (regla de la luz) y grieta de Ceniza PLANTADA (beat 6 §2.5) sin resolver. AC en `../historia/CAPITULOS/03-bombas.md` + `../historia/INDICE.md`.
