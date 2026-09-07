# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se ha mergeado + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

### Asignaciones 07/09 (Gwyndolin 11:00 — plan `../planes/2026/09/07.md`)

- `[EN CURSO][P3]` (06/09, higiene) **O1 — Tests `auditor_orden` (+4)** — Ornstein
  (`feat/engine-2026-09-07`): `src/tests/core/engine/test_auditor_orden.py`, los 4
  casos de la línea de Artorias; SOLO tests, `postmortem.py`/`textos.json` intactos.
  AC: 607→611, delta declarado. Origen: deuda técnica Artorias 06/09 (`abierto.md`).
- `[EN CURSO][P1]` (07/09) **O2 — e1 «La que no pesa» (cap. 6)** — Ornstein
  (`feat/engine-2026-09-07`): quest `story.ch6.e1` + FICHA vacía (Manus la llena
  mañana) + golden con `tail -n +2` (🧭22) + briefing con «un distrito se repite»
  (🧭23) + columna `marcas_purga` del beat como diana + textos `story.ch6.e1.*` con
  placeholders GNU-honestos + validador. AC: gate 23→24 quests, suite 611→615,
  goldens del Faro intactos. Origen: dirección #1 de Gwyn (06/09) + prosa
  `06-faro.md` §E2 + 🧭22/23 de Oscar.
- `[EN CURSO][P2]` (07/09) **O3 — `/etc/hosts` en el mundo (host `faro`)** — Ornstein
  (`feat/engine-2026-09-07`): generator escribe `/etc/hosts` legible (ancla red pieza
  2). AC: `cat /etc/hosts` exit 0 en `generate(42,6)` (y/o cap. 0), determinismo,
  suite ≥617. Costura O↔S: `faro` es el nombre que S1 resuelve. Origen: red
  simulada P2 (31/08) — ELEGIDA PARCIAL (hosts ANTES que scp, Gwyn 06/09).
- `[HECHO][P2]` (07/09) **S1 — Hosts descubribles leyendo el mundo (FASE A)** — Smough (`feat/sandbox-2026-09-07`) — PR #34: `cat /etc/hosts` registra hostname en `Shell.hosts` (L182); solo lectura; stub si O3 no llega; AC: descubre solo por lectura, vacío sin fichero, roundtrip. Origen: red simulada P2 (31/08).
- `[HECHO][P3]` (06/09) **S2 — `Try 'sort --help'` en `conteo.py`** — Smough (`feat/sandbox-2026-09-07`) — PR #34: hint coreutils en `sort -k0`/`sort -t ab`, exits/stdout válidos intactos; suite 614 (+7).
- `[HECHO][P2]` (07/09) **T1 — Selector de capítulo 6 en la puerta web** — Seath (`feat/meta-ui-2026-09-07`) — PR #35: `?chapter=6&seed=42` ya cubría el 6 (`parseParams [0,2,3,6]`); verificado headless `generate(42,6)` Faro con familia conteo + `ls`/`ls -a` Bandit + LEEME tienta + muerte `auditor_text` (postmortem); añadido hint cap. 6 en `web/index.html` + doc `web/app.js`. Suite +0 (verificación).
- `[HECHO][P2]` (07/09) **T2 — Roundtrip red en el save** — Seath (`feat/meta-ui-2026-09-07`) — PR #35: 3 tests refuerzo `src/tests/core/state/test_state_red.py` — `cat /etc/hosts` descubre `faro` + `known_hosts` sobreviven `GameState.to_dict/from_dict` idénticos; vacío sin fichero. Sin tocar comportamiento. Suite 617 (+3 T2, +7 S1+S2 en rama).

> *(07/09, Gwyn 23:00 — cierre: los 3 PRs del día mergeados (#31/#32/#33),
> suite 607, gate 22/23, bundle 45. Las 7 líneas `[HECHO]` del día archivadas
> en `../hecho/2026-09.md` §06/09. Sin retenciones: NADA queda vivo de hoy
> salvo los crons y las piezas/recámara de abajo.)*

- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** activos desde 27/08
  (gate aprobado el 26/08). Primer día completo de Concilio ejecutado: 27/08.

### Historial reciente (resumen — el detalle vive en `../hecho/2026-09.md`)

- 27/08 → 31/08: fundación narrativa de Manus (fichas, escenarios, caps. 0–4,
  fragmentos 1–4) y PRs #4–#15 mergeados; decisiones 🧭2, 🧭6, 🧭8=(b), 🧭9,
  🧭10 y 🧭11 materializadas en DESIGN y en código. Sin deuda abierta de esos
  días. Ver `hecho/2026-08.md` y `hecho/2026-09.md`.
- 02/09: mergeados los PRs #16/#19/#20/#21 (suite 515, gate 21/21) — detalle en
  `hecho/2026-09.md`.
- 03/09: mergeados los PRs #22 (S1 sandbox — sudo GANADO leyendo la orden),
  #23 (O1 engine — demonio del cap. 3 en el generator) y #24 (T1+T2 meta-ui —
  deploy web en Vercel + briefing del Faro). Suite final del árbol combinado:
  529 passed / gate de datos 21/21. DESVIACIÓN: Artorias sin turno (21:00 sin
  ejecutar) — Gwyn amplió sus gates y lo documentó.
- 04/09: mergeados los PRs #25 (O1 — read_marks en post-mortem), #26 (S1 —
  `cut` GNU-honesto + `c.cut`) y #27 (T1+T2 — guardián bundle + web slice 2).
  Suite **567 passed / 0 xfailed**, gate datos **22/22**, bundle **44 ficheros**
  tras el grito honesto del guardián.
- 05/09: mergeados los PRs #28 (O1 — `postmortem.auditor.corte` + O3 — cebo de
  ruta `LEEME.txt`), #29 (S1 — `sort -k`/`-t`/`-n` GNU honesto) y #30 (T1+T2 —
  quests E2/E3 salas-dato del Faro + `.nota-corte`). Suite **590 passed**,
  gate **22/23**, bundle **44 ficheros**. Deuda de namespace e2/e3 abierta
  (decidida al día siguiente por Gwyndolin).
- **06/09 (Gwyn, esta noche):** mergeados los PRs #31 (O1 — `auditor_orden` el
  Auditor cita tu `sort -k12` + O2 — LEEME que tienta 🧭21 + trampa del
  delimitador), #32 (S1 — `ssh` básico + host-key OpenSSH + stack de conexión,
  la red pieza 1 del cap. 4 + S2 — [BUG] `ls -a` cerrado con GNU real,
  `.nota-corte` vuelve a hallazgo Bandit) y #33 (T1 — rename namespace
  `story.ch6.e2/e3` → `dato2/dato3` EJECUTANDO la decisión de Gwyndolin + T2 —
  tabla viva del Faro en la puerta web). Suite final del árbol combinado:
  **607 passed / 0 failed** (590 +0 +16 +1, deltas declarados verificados),
  gate de datos **22 conceptos / 23 quests** (`dato2/dato3`, `e2/e3` fuera),
  bundle **45 ficheros (330.8 KiB)** regenerado como paso canónico (S1 añade
  `red.py`). Resoluciones de huellas por script con assertions (3 merges,
  7 regiones; `textos.json` unión `orden` + `dato2/dato3` con JSON validado).
  Gate de diseño de Gwyn en vivo: 13/13 esencia sobre `generate(42,6)` + FS
  handmade de `ssh` + post-mortem. **Verificación Chromium real de T2**: panel
  «Tabla del Faro» aparece solo tras `cut` con la columna `distrito`
  destacada — consola limpia. Deuda de tests de O1 (`auditor_orden` +4) queda
  señalada como higiene para mañana.

### ⚠️ Deuda de NAMESPACE — ✅ RESUELTA (T1 mergeado esta noche)

> La decisión de Gwyndolin (06/09, `../planes/2026/09/06.md`) quedó EJECUTADA
> en PR #33 y mergeada por Gwyn: `e2`/`e3` → `dato2`/`dato3` en
> `curriculum.json`/`textos.json`/`generator.py`, con guard
> `test_namespace_ch6_dato_vs_encargo` que impide el retorno del choque.
> Regla fijada para el proyecto: **encargo narrativo = `eK`; sala-dato =
> `datoN`**. Los encargos narrativos e2–e5 del cap. 6 están LIBRES para
> planificar mañana. El detalle histórico vive en `../hecho/2026-09.md` y en
> el plan del 06/09 — no se borra, se cierra.

### Piezas listas para integrar (sección — Gwyn 05/09, propuesta de Gwyndolin)

- **Pack `POSTMORTEM.md` de Manus (04/09, entrada `[HECHO]` 05/09 03:00)**: 5
  claves del Auditor (`prueba`/`sin_lectura`/`senal_muerte`/`senal_recarga`/
  `ceniza.llave`) listas para `src/data/textos.json`; 2 ya aterrizadas por O1
  del 04/09 vía forma formulario. DECISIÓN de Gwyn (05/09, REVISADA 06/09):
  **sigue esperando a un Q con Manus** — la pieza no es urgente (los O1
  `corte`/`orden` ya cubren la voz del interrogatorio en formulario, y la
  cualidad nueva del pack son claves de SEÑAL, no de formulario) y merece un
  turno con dueño en caliente. Dueño propuesto: Manus con Ornstein de
  integrador. Contrato del pack: reglas de montaje en
  `backlog/historia/POSTMORTEM.md` §Reglas. Sin cambio de destino esta noche.
