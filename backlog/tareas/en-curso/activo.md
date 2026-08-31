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

### Manus (03:00 del 31/08) — pendientes de merge por Gwyn

- `[HECHO][P2]` (30/08, noche) **M1 Fragmento 4 (la cuenta que recibió pagos de una filial de Lumen)** — Manus (03:00 del 31/08): HECHO. `[LISTA]` en `FRAGMENTOS.md`, formato Souls, H1/H2, cruce con la Lista (§2.4) y con fragmentos 1-3 (47/44), sin contradecir la cronología de Vela. Detalle: `../historia/INDICE.md`.
- `[HECHO][P2]` (30/08, noche) **M2 Capítulo 4 «Troncales» (beats 7–8: el expediente + el giro del Auditor)** — Manus (03:00 del 31/08): HECHO. 5 encargos `story.ch4.e1`–`e5` (1 azul, 1 gris, 2 rojos, 1 de cierre), familia Red real (`ssh`/`scp`/túneles), regla de la luz en MÁXIMO (Faro). Giro del Auditor PLANTADO (beat 8, §9 sin resolver) + expediente beat 7 con fila 000 vacía. AC en `../historia/CAPITULOS/04-troncales.md` + `../historia/INDICE.md`.

## Asignadas por Gwyndolin (31/08, plan del día) — ver `../planes/2026/08/31.md`

> Origen de cada línea: (O1) dirección #1 de Gwyn 30/08 · (O2) continuación natural de O1 + post-mortem del PR #10 · (S1) dirección #2 de Gwyn + nota de Artorias 30/08 · (S2) cap. 3 «Bombas» de Manus (31/08) · (T1) 🧭11 de Oscar + factura medida por Havel 31/08 (dirección #4) · (T2) dirección #3 + decisión 🧭9 firmada en DESIGN §6.1. Entrada verificada a las 11:00: solo `main`, sin PRs abiertos; suite 385/0 (Oscar/Havel). Sin bugs del día. La red simulada del cap. 4 quedó registrada como tarea propia en `../pendiente/abierto.md` (forma pendiente de Gwyn).

- `[HECHO][P1]` (31/08, PR #13) **O1 — Puerta del cap. 2: flujo completo de ENCARGO (listar → abrir → validar → generar → jugar)** — Ornstein (13:00, `feat/engine`): nuevo fichero en `src/core/engine/` (p. ej. `session.py`); con datos reales (`story.ch2.e1–e5` ya en currículo desde PR #11): listar encargos del capítulo → abrir `story.ch2.e1` con `Contract.prereqs_met(knowledge)` (rechazo accionable con los conceptos que faltan) → generar sala determinista del contrato → jugar la sesión. La línea golden del cap. 2 pasa de demo a JUGADA dentro del flujo. AC: flujo completo headless testeado; `prereqs_met` al ABRIR (🧭8=(b) intacta); regresión explícita de `generate(seed,0)`; sin tocar `src/data/`; suite verde + delta en el PR. **ARTORIAS ✅ (PR #13)**: flujo real jugado (abr e1→golden `grep 11:04 … | wc -l`→2→cerrar, noise 3); rechazo accionable sin prereqs; regresión `generate(seed,0)` byte-idéntica (52 tests engine+generator verdes); seed determinista quest+run.
- `[HECHO][P2]` (31/08, PR #13) **O2 — Post-mortem conectado: el informe del Auditor entra en el cierre del encargo** — Ornstein (13:00, `feat/engine`): al CERRAR la sesión (completado o expulsión), el flujo adjunta `build_postmortem(shell_dict, state)` como dato estructurado (factura, total vs budget, línea del Auditor como `line_key`+`args`). Sin prosa nueva (claves `postmortem.auditor.*` → 🧭12, no hoy). AC: cierre → informe adjunto testeado (completado y expulsión); función pura intacta; suite verde + delta. **ARTORIAS ✅ (PR #13)**: `cerrar_encargo` adjunta post-mortem en ambos modos (completado y expulsión); función pura del PR #10 intacta; `total_noise=3` y `dentro_presupuesto=True` en el cierre real.
- `[HECHO][P2]` (31/08, PR #14) **S1 — `ps`/`env` en el sandbox (familia Procesos del cap. 3)** — Smough (16:00, `feat/sandbox`): `ps` con procesos simulados de la sala (2–3, determinista por seed) + `env` de solo-lectura; semántica contrastada contra GNU real (§2.6.8); ruido por acción facturado. AC: golden contra coreutils; `&&`/`;` siguen rechazados; sin regresión cap. 0 (`test_session_cap0.py` 3/3) ni cap. 2 (línea golden intacta); suite verde + delta. **ARTORIAS ✅ (PR #14)**: `ps`/`ps aux` real contra Shell cap. 3 (cabeceras GNU, USER que delata ceniza-521/censo-522); `env` ordenado por clave; `&&` rechazado exit 2; cap. 0/2 NO exponen ps/env (exit 127, regresión probada).
- `[HECHO][P2]` (31/08, PR #14) **S2 — `story.ch3.*` al currículo (cap. 3 «Bombas» de Manus entra en datos)** — Smough (16:00, `feat/sandbox` + `src/data/`): 5 quests `e1`–`e5` (blue/grey/red/red/grey, `CAPITULOS/03-bombas.md`) + conceptos `c.ps`/`c.env`. **FUERA de alcance: el `sudo` GANADO** — salto de diseño, lo decide Gwyn con datos antes de codearse. AC: `load_curriculum` OK (gate de datos), validador en negativo, tints según Manus; suite verde + delta. **ARTORIAS ✅ (PR #14)**: GATE DE DATOS OK — 16 conceptos/16 quests; `story.ch3.e1–e5` con tints blue/grey/red/red/grey (según Manus); `c.ps`(prereq listar)/`c.env`(prereq ps); cap. 2 intacto (`c.grep/c.pipe/c.wc`); validador negativo pasa.
- `[HECHO][P2]` (31/08, PR #15) **T1 — Recalibrado «Cero rastro» (🧭11: el umbral 4 es imposible de ganar honesto)** — Seath (19:00, `feat/meta-ui`): datos verificados hoy de forma independiente (Oscar 05:00 + Havel 07:00): min honesto **5**, canónico §6.4.4 **6**, puro `cp` memorizado **3**. Propuesta planificada (Gwyn valida al mergear): `UMBRAL_CERO_RASTRO=5` + condición «sin exit≠0» como acompañante («Mano de seda» queda intacto y distinto). AC: la run canónica (6) NO lo gana; una sesión min-honesto (5) sin errores SÍ; roundtrip + idempotencia intactos; suite verde + delta. **ARTORIAS ✅ (PR #15)**: `UMBRAL_CERO_RASTRO=5` real; tests: canónica6-no-gana, ruido-justo-sobre-threshold-no-gana, min-honesto5-sin-errores-SÍ-gana, error-mata-ambos; roundtrip/idempotencia intactos. **CRUCE 🧭11 RESUELTO**: el `[BUG][P2]` de Oscar/Havel de esta mañana tiene su causa aquí y esta PR lo ARREGLA — verificar Gwyn al mergear (decide umbral5+sin-errores o la otra opción de 🧭11, mismo coste).
- `[HECHO][P2]` (31/08, PR #15) **T2 — Eco 🧭9 pre-render: `evaluate_unlocks` emite `progression.unlocked` al bus común** — Seath (19:00, `feat/meta-ui`): al dominar un concepto, evento `{concepto, tick, order}` al bus de `core.common.events` (datos ya en `state.mastered` desde PR #12; forma firmada por Gwyn en DESIGN §6.1: diegético, cap. 1, Gris nombra lo dominado, prohibido el toast de sistema). El render futuro pinta el eco sin tocar el core. ⚠️ Frontera: si el evento exige tocar `common/` (de Ornstein), TODO mínimo en el PR y lo cobra Ornstein mañana. AC: suscriptor de prueba recibe payload completo; re-evaluar NO re-emite duplicado; roundtrip intacto; suite verde + delta. **ARTORIAS ✅ (PR #15)**: SIN tocar `common/` — `UNLOCK_EVENT_TYPE` vive en `progression/`; `bus` opcional (None = backward-compat). Tests reales contra `EventBus` común: payload completo `{concepto,tick,order}`, sin-bus-no-emite, re-evaluar-no-re-emite-duplicado. 22 tests progression verdes.
