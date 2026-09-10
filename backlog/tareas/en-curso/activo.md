# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se ha mergeado + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

> *(cierre 09/09, 23:00 — las 6 líneas `[HECHO]` archivadas en `../hecho/2026-09.md` §09/09; detalle del merge allí. NADA retenido.)*

### Asignaciones 10/09 (Gwyndolin 11:00 — plan `../planes/2026/09/10.md`)

- `[HECHO]` (10/09) **O1 — `dato5` «La persiana» (generator)** — Ornstein: piel de procesos determinista por seed en `_generate_cap6` (3 procesos, 1 binario compartido, `START 11:04` delata la noche de `PR-0091`; init `Aug25`). Cero sandbox (`ps.py` ya imprime START, verificado 11:00). Contract para S2: id `dato5`, requires `c.ps`, golden `ps aux | grep 11:04`. Criterio: determinismo byte-idéntico, dato2/dato3/e2/e1 intactos, gate 127 y allowlist sin cambios, suite 648+4–5, commit solo Ornstein. → PR #42 (rama `feat/engine-2026-09-10`, tests 648→653 +5) **💥 NO MERGEAR — integración rota en combinado (1 failed/680). Culpa: `src/tests/core/generator/test_ch6_dato5_persiana.py:116` exige `set(DEFAULT_CH6_COMMANDS)=={cat,cd,cp,cut,env,grep,head,kill,ls,ps,sort,sudo,tail,uniq,wc}` exacto; tras merge con S2 (que añade `join` a `DEFAULT_CH6_COMMANDS`) falla con `Extra items: 'join'` (ensayo 679 passed/1 failed). ARREGLO EXACTO (1 línea): cambiar `assert set(DEFAULT_CH6_COMMANDS)=={…}` por `assert {"cat","cd","cp","cut","env","grep","head","kill","ls","ps","sort","sudo","tail","uniq","wc"} <= set(DEFAULT_CH6_COMMANDS)` o `assert set(DEFAULT_CH6_COMMANDS)=={…}|{"join"}` permitiendo `join`. Aislado verde (5/5), combinado exige parche.**
- `[HECHO]` (10/09) **S2 — `dato4` «El cruce» + handler `join` + altas dato4/dato5** — Smough: handler `join` GNU-honesto (`-t/-1/-2/-v 1`, errores GNU reales) + `c.join` (cap. 6, prereqs `c.cut`+`c.sort`) + quest `dato4` (requires `c.join`, golden `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → fantasma `PR-0091`/`000`, sin pipes) + quest `dato5` según contract de O1 + textos de ambas (rutas absolutas 🧭15). Criterio: `load_curriculum()` 24 conceptos / 27 quests con DAG válido, shell SIN cambios (2 pipes intactos), golden dato4 exit 0 en `generate(42,6)`, suite 648+4–6. → PR #43 (rama `feat/sandbox-2026-09-10`, tests 648→668 +20) **✅ LISTA PARA MERGE — handler join GNU-honesto determinista, 20 tests verdes, DAG 24/27 válido,allowlist CH6 16 cmds con `join`, shell 2 pipes intacto, bundle 47 fresco. Aislado 47 passed; en combinado es quien añade `join` correctamente — el fail es de O1, no de este PR.**
- `[HECHO]` (10/09) **T1 — verificación del circuito datos (ch6)** — Seath: `src/tests/core/state/test_ch6_datos_circuit.py` — dato4 end-to-end en mundo real (fallback handmade si O1/S2 no están mergeados), dato5 START forense, `GameState` roundtrip con procesos nuevos, gate por aritmética (24/27), bundle fresco. Cero toques fuera de `src/tests/core/state/` + `docs/`. → PR #44 (rama `feat/meta-ui-2026-09-10`, tests 648→655 +7) **✅ LISTA PARA MERGE — 7 tests circuito ch6 (join anti-join + ps forense + roundtrip + gate/pipes) verdes, handmade fallback honesto, solo toca `src/tests/core/state/`+`docs/`, gate flexible 23/25→24/27. Aislado 7/7; en combinado suma +7 real (680 total).**

### Asignaciones 09/09 (Gwyndolin 11:00 — plan `../planes/2026/09/09.md`)


### Asignaciones 07/09 (Gwyndolin 11:00 — plan `../planes/2026/09/07.md`)

> *(08/09, Gwyndolin — reposición: las 3 tareas de abajo se replanifican ARRIBA (Asignaciones 08/09) con la clave corregida (`e2`); veredictos 💥 de Artorias conservados como constancia.)*


> *(07/09, Gwyn 23:00 — cierre: PRs #34/#35 mergeados en orden sandbox→meta-ui,
> suite **617 passed**, gate 22/23, bundle 45. Las 4 líneas `[HECHO]` del día
> archivadas en `../hecho/2026-09.md` §07/09. NADA retenido: las 2 ramas del
> día borradas tras merge MERGED (la de engine nunca existió). Queda vivo de
> hoy: O1/O2/O3 💥 (arriba), crons y piezas/recámara de abajo.)*

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
- **07/09 (Gwyn, esta noche):** mergeados los PRs #34 (S1 hosts descubribles
  por lectura + S2 `Try 'sort --help'` — Smough) y #35 (T1 selector cap. 6
  verificado + hint web + T2 roundtrip red en el save — Seath), orden
  sandbox→meta-ui. Suite final del árbol combinado: **617 passed / 0 failed**
  (607 +7 +3, deltas declarados verificados por aritmética), gate de datos
  **22 conceptos / 23 quests** (S1/S2/T1/T2 no tocan curriculum), bundle
  **45 ficheros** fresco (regen NO necesario, guardián verde). Huellas
  resueltas por script con assertions (2 merges, 4 regiones; `activo.md`
  gana HEAD por subset 7/7, `worklog` unión cronológica 03→21). Ensayo
  previo en worktree desechable (614/617 antes de tocar main). Merge
  commits `cedb7b1` → `ebabb36`. **Chromium real de T1 verificado por Gwyn**:
  hint cap. 6 SOLO con `?chapter=6` (ver worklog). **O1/O2/O3 de Ornstein
  SIN RAMA** — reposición mañana, prioridad 1 de Gwyndolin.
- **08/09 (Gwyn, esta noche):** mergeados los PRs #36/#37/#38 en orden
  engine→sandbox→meta-ui, suite **635 passed**, gate **22 conceptos / 24
  quests** (`story.ch6.e2` «La que no pesa» nueva; `e1` intacta), bundle **45
  ficheros** regenerado (351.1 KiB). Las 6 líneas `[HECHO]` del día archivadas
  en `../hecho/2026-09.md` §08/09; NADA retenido; las 3 ramas borradas tras
  merge MERGED (SHAs locales verificados en GitHub). Gate de diseño 23/23 en
  verde (leer descubre, listar no; golden e2 sin fantasma; scp enseña dónde
  leer; save aguanta). **La sección «Piezas listas para integrar» queda SIN
  CAMBIOS de destino**: el pack `POSTMORTEM.md` sigue esperando a un Q con
  Manus — `corte`/`orden` siguen cubriendo la voz del interrogatorio en
  formulario y la cualidad del pack (claves de SEÑAL) no es urgente. Vivo de
  mañana: quests `ch4` (scp como prereq), `dato4/dato5`, karma 521/522 y
  🧭24 (allowlist `cat+grep` de caps con red).

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
  `backlog/historia/POSTMORTEM.md` §Reglas. Sin cambio de destino esta noche
  (07/09: revisado de nuevo — `corte`/`orden` siguen cubriendo la voz del
  interrogatorio en formulario; la pieza sigue sin urgencia).

> **(08/09, Gwyn 23:00 — cierre del día):** PRs #36/#37/#38 mergeados en orden
> engine→sandbox→meta-ui, suite **635 passed**, gate **22 conceptos / 24
> quests** (`story.ch6.e2` «La que no pesa» nueva; `e1` intacta), bundle **45
> ficheros** regenerado (351.1 KiB). Las 6 líneas `[HECHO]` del día archivadas
> en `../hecho/2026-09.md` §08/09; NADA retenido; las 3 ramas borradas tras
> merge MERGED (SHAs locales verificados en GitHub). Gate de diseño 23/23 en
> verde (leer descubre, listar no; golden e2 sin fantasma; scp enseña dónde
> leer; save aguanta). **La sección «Piezas listas para integrar» queda SIN
> CAMBIOS de destino**: el pack `POSTMORTEM.md` sigue esperando a un Q con
> Manus — `corte`/`orden` siguen cubriendo la voz del interrogatorio en
> formulario y la cualidad del pack (claves de SEÑAL) no es urgente. Vivo de
> mañana: quests `ch4` (scp como prereq), `dato4/dato5`, karma 521/522 y
> 🧭24 (allowlist `cat+grep` de caps con red).
