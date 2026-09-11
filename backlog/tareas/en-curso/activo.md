# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se ha mergeado + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

> *(cierre 10/09, 23:00 — las 3 líneas `[HECHO]` del día archivadas en
> `../hecho/2026-09.md` §10/09; detalle del merge allí. NADA retenido.
> PRs #42/#43/#44 mergeados en orden engine→sandbox→meta-ui con el fix de
> 1 línea de O1 aplicado EN EL MERGE (patrocinado por Artorias): suite
> **680 passed**, gate **24/27**, bundle **47 ficheros (389.8 KiB)**.
> Las 3 ramas del día borradas tras confirmar MERGED en GitHub.)*

### Asignaciones 11/09 (Gwyndolin 11:00 — plan `../planes/2026/09/11.md`)

- `[EN CURSO][P2]` (11/09) **O1 — Ornstein 13:00 · `feat/engine-2026-09-11` · `auditor_join`: la cuarta huella del Auditor** — detector `_find_join` en `postmortem.py` (join con `-v` anti-join → 1 línea formulario) + textos SOLO `postmortem.auditor.join*` + tests de los 3 casos (con `-v` / sin `-v` documentado / sin `join` byte-idéntico). Criterio: línea presente con anti-join en history, sin `join` byte-idéntico a hoy, suite +3–5 sobre 680. Costura S↔O sobre `textos.json`: prefijos disjuntos (`postmortem.auditor.join` vs `story.ch4.e2`), unión trivial. NO toca `curriculum.json` (dueño S2 hoy). **→ 💥 Artorias 21:00: NO ENTREGADO — `feat/engine-2026-09-11` 0 commits ahead de origin/main, sin PR abierto (verificado `git log origin/main..feat/engine-2026-09-11` vacío + `gh pr list` sin engine). Criterio no evaluable; replanificar mañana con misma spec y prefijo `postmortem.auditor.join` disjunto. Sin impacto en S2/T1.**
- `[HECHO][P2]` (11/09) **S2 — Smough 16:00 · `feat/sandbox-2026-09-11` · quest `story.ch4.e2` «El volcado que no pesa»** — `curriculum.json` (quest ch4 requires `['c.cut','c.scp']`, golden 2 pasos `scp troncal-01:…volcado.csv /tmp/` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-`) + textos SOLO `story.ch4.e2.*` + gates 24/28. ALLOWLIST OWNER: NADIE — `DEFAULT_CH4_COMMANDS` y `DEFAULT_CH6_COMMANDS` INTACTOS (decisión Gwyndolin por delegación de Gwyn: NO ampliar; `tail/sort/uniq` siguen frontera 127, filtro positivo `grep TR-`). PROHIBIDO `grep -v` (🧭27). Máximo 2 pipes. NO toca `src/core/generator/` (la sala materializa e2 vía `contract_id` sin cambios en dispatch). Único committer de `curriculum.json` hoy. → PR #45 (680→684 +4) **→ ✅ Artorias 21:00: VERDE aislado 684/0 y combinado 691/0 con T1. Gate 24/28 DAG válido (`c.cut` 4←`c.wc` 2, `c.scp` 4←`c.cut` 4), textos 7 claves rutas absolutas + filtro positivo `grep TR-` sin `grep -v`, golden exit 0 `TR-001/TR-002/TR-003` sin header (TR-003 EN_COLA), allowlist 13 exactos `tail`127 intacta, `generate(42,4, contract_id=e2)` + fallback, `generate(42,6)` intacto, bundle 393.3 KiB. Lista para merge sandbox→meta-ui.**
- `[HECHO][P2]` (11/09) **T1 — Seath 19:00 · `feat/meta-ui-2026-09-11` · circuito ch4 completo (e1+e2) + guard de frontera** — tests `src/tests/core/state/test_ch4_e2_circuit.py` (7 tests): regresión e1 intacta con e2 en curriculum, e2 por contract golden 2 pasos `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header (filtro positivo, TR-003 EN_COLA pista), guard allowlist SUBSET (`<= set(13)` nunca `==`), `tail/sort/uniq/head` →127 frontera, `GameState` roundtrip, gate flexible 24/27↔24/28, 2 pipes OK / 4 rechazado. → PR #46 (680→687 +7) **→ ✅ Artorias 21:00: VERDE aislado 687/0 (flexible 27/28 + fallback handmade) y combinado 691/0. Guard SUBSET `<= set(13)` lección 10/09 institucionalizada, frontera 127 documentada, regresión e1 byte-idéntica, golden 2 pasos determinista, roundtrip idéntico, pipe 2 OK/4 KO `multiple pipelines not supported` exit 2 honesto. CERO toques fuera de `src/tests/core/state/`+`docs/`. Lista para merge tras S2.**

### Asignaciones 10/09 (Gwyndolin 11:00 — plan `../planes/2026/09/10.md`)

- *(O1 dato5 «La persiana» → PR #42; S2 dato4 «El cruce» + `join` → PR #43;
  T1 circuito datos → PR #44 — todas MERGE el 10/09, ver
  `../hecho/2026-09.md` §10/09.)*

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
