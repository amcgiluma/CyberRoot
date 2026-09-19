# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se ha mergeado + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

> *(cierre 13/09, 23:00 — las 3 líneas `[HECHO]` del día archivadas en
> `../hecho/2026-09.md` §13/09; PRs #50/#51/#52 mergeados en orden
> engine→sandbox→meta-ui por Gwyn, suite **708 passed**, gate **24/29**,
> bundle **47 ficheros (402.3 KiB)** regenerado canónicamente. NADA
> retenido, 3 ramas borradas tras confirmar integradas en GitHub.
> Cierre anterior 12/09 — PRs #47/#48/#49, 698/24-28/47.)*

### Asignaciones 18/09 (Gwyndolin 11:00 — plan `../planes/2026/09/18.md`) — 🔒 DÍA EN ARCHIVO: ver `../hecho/2026-09.md` §18/09

> *(cierre 18/09, 23:00 — las 2 líneas `[HECHO]` de hoy (O1 + S1) archivadas en
> `../hecho/2026-09.md` §18/09; PRs #64/#65 mergeados en orden
> engine→sandbox por Gwyn, suite **760 passed** (749+7+4=760, deltas
> declarados verificados por aritmética), gate **24/31**,
> bundle **48 ficheros (445.4 KiB)** regenerado canónicamente (guardián
> verde). T1 de Seath SIN pieza (día cerró con merge antes de 19:00 — su
> higiene pendiente se hereda a las piezas del 19/09). NADA retenido:
> 2 ramas borradas tras confirmar MERGED en GitHub (SHA locales
> verificados en GitHub — rama 09-18 estaba detrás por el commit a35dee
> del ensayo; ver worklog §23:00). Cierres anteriores: 17/09 —
> PRs #62/#63/#61, 749/24-31/48; 13/09 — PRs #50/#51/#52.)*

> Base: suite 749/0, gate 24/31, bundle 48 fresco, sin PRs abiertos.
> Día de LA PUERTA: session.py abraza el cap. 5 (`SUPPORTED_CHAPTERS`
> +`{5}`, `_commands_for(5)`, flag `volcado_rescatado` del save).
> ALLOWLIST OWNER: NADIE toca asserts de `DEFAULT_CH4*` existentes;
> la NUEVA `DEFAULT_CH5_COMMANDS` la crea Smough (constante nova).
> GATE OWNER: NADIE (no hay quests nuevas — gate no toca).
> Bundle: solo Smough regenera (toca `src/data/textos.json`).

- `[EN CURSO][P2]` (18/09) **T1 — Seath 19:00 · `feat/meta-ui-2026-09-18` · mostrar el cap. 5 en la web** — si O1 aterrizó en main: `parseParams` a `[0,2,3,4,5,6]` + hint del cap. 5 (`web/app.js` + `web/index.html`), la lente «Subestación — custodia» hermana del rescate del Faro (SOLO si `volcado: rescatado` en history, falso positivo caducado cazado); si O1 NO aterrizó: hueco honesto declarado delta 0 (`node --check`), sin lente muerta. AC: consola limpia en `?chapter=4`/`?chapter=5`; TRONCAL_STATIC intacta; sin bundle.
- `[EN CURSO][P3]` (18/09, higiene) **Gwyndolin 11:00 — salud del backlog verificada** — revisado TODO el backlog con ojo de estructura: plan de ayer COMPLETO (PRs #62/#63/#61, ver cierre de Gwyn); `abierto.md`/`propuestas.md`/`aplicadas/` ok (sin marcadores residuales, cero `=======`); el único [BUG] vivo (`grep -v`, 🧭27) sigue P3 recámara — nadie lo toca HOY. Sin cambios de estructura → INDICE.md sin cambios.

**Previsto** (cierre Gwyn 23:00): PRs mergeados en orden
engine→sandbox→meta-ui, suite esperada **758** (749+6+3+0, deltas
declarados verificados por Artorias), gate **24/31** flexible
`<=32`, bundle regenerado canónicamente tras merge del sandbox.


### Asignaciones 16/09 (Gwyndolin 11:00 — plan `../planes/2026/09/16.md`)

> Base verificada: main con e3 verde (727 tras regen canónico de Artorias,
> gate 24/30, bundle 47/418.3 KiB). Sin ramas ni PRs huérfanos. Día de LA CADENA:
> la consecuencia del dilema e3 deja de ser post-mortem y se vuelve mundo.

- `[HECHO][P2]` (16/09) **🧭36 — O1 — Ornstein 13:00 · `feat/engine-2026-09-16` · `session.py`: e3 expone la disolución por `rm` (simetría scp/rm en el flujo de encargo) — PR #59** — `_commands_for(4)` devuelve `DEFAULT_CH4E3_COMMANDS` (14, con `rm`) cuando contract_id/quest_id == 'story.ch4.e3'; base ch4 13 INTACTA en e1/e2. Sin tocar `shell.py` ni asserts de allowlist (allowlist e3 ya existe del PR #57). Criterio: `abrir_encargo(c,'story.ch4.e3')` → `rm /tmp/volcado.csv` exit 0 → post-mortem `volcado: caducado` por `rm`; e1/e2 siguen base 13 (rm→127, frontera intacta). Tests FLEXIBLES e1/e2↔e3. Suite 727→731 (+4). **ALLOWLIST OWNER: NADIE hoy.**
- `[HECHO][P2]` (16/09) **S1 — Smough 16:00 · `feat/sandbox-2026-09-16` · `dato7` «El fantasma que pesa» — el volcado que viaja al Faro — PR #60** — `src/core/generator/`: el FS del Faro planta `/srv/camara-faro/volcado-rescate.csv` con `TR-003|EN_COLA` SOLO si la sesión rescató (detector `_has_volcado_rescate` ya existente; si caducado → fichero NO existe y el join nombra la ausencia); + `src/data/curriculum.json` quest `story.ch6.dato7` grey requires `c.join` — golden `join -t'|' -1 1 -2 3 -v 1 purgas.csv volcado-rescate.csv | grep TR-003` → exit 0 (nota: golden real usa volcado primero para -v, ver briefing dato7). Gate 24/30→31. Suite 727→735 (+8). **GATE OWNER de dato7: Smough.** Bundle regenerado 47 ficheros 426.2 KiB.
- `[HECHO][P2]` (16/09) **T1 — Seath 19:00 · `feat/meta-ui-2026-09-16` · Web: tooltip del `N/30` + panel rescate en el Faro (solo `web/app.js`) — PR #61** — (a) tooltip sobre `· ticks del volcado: N/30` (`title=` descriptivo, consume `get_history()` ya expuesto, sin pulso — 🧭34 respetado); (b) lente del rescate: el panel del Faro detecta `volcado-rescate` y anota `TR-003` (lente pura, NADA ejecuta el core). Sin tocar `TRONCAL_STATIC` (deuda vigente), sin tocar `src/`, NO regenera bundle. Suite delta 0 honesto. Realineado 17/09 con origin/main (11 commits), `node --check` OK, suite 737→737 delta 0. **→ ✅ Artorias 21:00: VERDE — solo web/app.js (+44/-4), TRONCAL_STATIC 3 ocurrencias intacta, hideTroncalTabla restart intacto, _escapeHtml + _isFaroRescatePresent/_getFaroRescateSuffix lente pura sin ejecutar core, node --check OK, bundle stale honesto (session.py) pendiente regen Gwyn por regla 12/09, delta 0 honesto; listo para merge. Nota: body declara tests antes 737 (base real 739 tras regen Gwyn 16/09) — discrepancia de base, no de delta.**

|**COSTURAS 16/09:** ALLOWLIST OWNER: NADIE (allowlist e3 sin tocar). GATE OWNER curriculum/archivo: Smough (dato7). Bundle: SOLO Smough regenera (toca `src/data/`); Seath NO. `postmortem.auditor.*` y pack `POSTMORTEM.md`: intocados.


### Asignaciones 19/09 (Gwyndolin 11:00 — plan `../planes/2026/09/19.md`)

> Base verificada: suite 760/0, gate 24/31, bundle 48 (445.4 KiB), sin PRs
> abiertos ni ramas huérfanas (verificado 11:00). Día de abrir del todo
> LA PUERTA: la Subestación pasa de 1 encargo jugable a campaña completa.
> ALLOWLIST OWNER: Smough (`DEFAULT_CH5E1/E3/E4_COMMANDS` novas, forma
> `<= set(...)`; base `(cat,scp)` intacta). GATE OWNER: NADIE toca asserts
> del gate (no hay quests nuevas en curriculum). Bundle: SOLO Seath regenera.

- `[EN CURSO][P1]` (19/09) **O1 — Ornstein 13:00 · `feat/engine-2026-09-19` · puerta ch5 completa: `story.ch5.e1/e3/e4` abribles por `abrir_encargo`** — `session.py` quita el guard `e1/e3/e4 → abrible False`; `volcado_del_save(pm)` heredado en TODO el capítulo (el testigo pesa en e1/e3/e4, no solo e2); tests flexibles. AC: los 3 encargos → `abrible True` con requires correctos; e2 intacta (7 tests existentes no rompen); determinismo ×2 seeds; suite 760→≥764. NO toca `shell.py` ni `web/`.
- `[HECHO][P1]` (19/09) **S1 — Smough 16:00 · `feat/sandbox-2026-09-19` · allowlists per-encargo `DEFAULT_CH5E1/E3/E4_COMMANDS` — PR #66** — patrón `DEFAULT_CH4E3_COMMANDS` (PR #57): e1 `ls,ps,chmod,kill`; e3 `ps,env,kill`; e4 `chmod,chown,tail,ls`. AC: base `(cat,scp)` intacta para e2; allowlist activa SOLO en su encargo (fuera → 127 frontera honesta); golden e3 `kill -HUP`/`kill -9` sobre el intruso jugable; suite 760→768. Sin tocar `session.py`, `curriculum.json`, `web/`.
- `[HECHO][P1]` (19/09) **T1 — Seath 19:00 · `feat/meta-ui-2026-09-19` · Web: parseParams con 5 + tercera lente «Subestación — custodia» — PR #67** — `parseParams` `[0,2,3,4,6]`→`[0,2,3,4,5,6]` (5 nuevo, 3 intacto no-regresión); panel custodia `CUSTODIA_STATIC` + `_isCustodiaPresent()`/`hideCustodiaTabla`/`renderCustodiaTabla`/`updateCustodiaTabla`/`previewCustodiaTabla` (falso positivo caducado cazado, file TR-003 como verdad); `hideCustodiaTabla` en `restartSameSeed`, dispatch triple, boot preview custodia; solo `web/app.js` + `web/index.html` (+docs), `TRONCAL_STATIC` 3 intacta, Faro/Troncal intactos, `node --check` OK, consola limpia `?chapter=4/5/6`, suite 760→760 delta 0, bundle 48 fresco verde.

**Previsto** (cierre Gwyn 23:00): PRs mergeados engine→sandbox→meta-ui,
suite esperada **≥768** (deltas declarados verificados por Artorias),
gate **24/31** (flexible, nadie lo toca hoy), bundle 48+ regenerado
canónicamente por Seath.

### Asignaciones 17/09 (Gwyndolin 11:00 — plan `../planes/2026/09/17.md`)

> Base verificada: suite 738+1 stale → 739 tras regen canónico de Gwyn
> (cierre 16/09), gate 24/31, bundle 47 (~426 KiB). UNA rama huérfana:
> **PR #61** (`feat/meta-ui-2026-09-16`, T1 de Seath, sin veredicto de
> Artorias) — su dueño la cierra HOY como prioridad 1. Día de CAP. 5.
> ALLOWLIST OWNER: NADIE · GATE OWNER curriculum: Smough (24/31→24/32) ·
> Bundle: solo Smough regenera (toca `src/data/`).

- *(17/09, M1 — Manus 03:00, pendiente de confirmar en worklog: mantenimiento post-16/09 según su rutina; sin pieza narrativa nueva agendada — la dirección del día la da Oscar: cap. 5 lee el testigo con verbos ya dominados, sin prosa nueva que integrar.)*

### Asignaciones 13/09 (awaiting: nada — día CERRADO)

- *(13/09, O1 mergeado por Gwyn como PR #50 — línea completa archivada en `../hecho/2026-09.md` §13/09.)*
- *(13/09, S2 mergeado por Gwyn como PR #51 — línea completa archivada en `../hecho/2026-09.md` §13/09.)*
- *(13/09, T1 mergeado por Gwyn como PR #52 — línea completa archivada en `../hecho/2026-09.md` §13/09.)*

### Asignaciones 14/09 (Gwyndolin 11:00 — plan `../planes/2026/09/14.md`)

- `[HECHO][P1]` (14/09) **O1 — Ornstein 13:00 · `feat/engine-2026-09-14` · Gris reconoce: `progression` dice qué copiaste (mitad Gris de la 🧭9/P1 13/09) — PR #53** — una línea diegética de Gris en `textos.json` (prefijo `*gris*` disjunto hub.gris.volcado) tras completar `story.ch4.e2` con `scp → cut|grep TR-` limpio; señal mínima desde el save/history (fallback honesto). 4 tests, suite 708 → 712 (+4), delta declarado. Prefijos disjuntos; no cruza con S2/T1. **→ ✅ Artorias 21:00: VERDE — 4 tests (con gesto→línea, sin gesto→None, determinismo, resolve desde data), prefijo hub.gris.* disjunto, sin tocar engine/postmortem, gris_eco/history determinista, bundle regen 406.0 KiB; listo para merge.**
- `[HECHO][P2]` (14/09) **S2 — Smough 16:00 · `feat/sandbox-2026-09-14` · dato6: la variante bonus sube a requirement + hint de precisión — PR #54** — quest `story.ch6.dato6` acepta golden `join|grep 000483` y variante `cut -d'|' -f3 purgas.csv | grep 000483` (ambas válidas); `hint_2` trampa `grep 000` vs `grep 000483` («¿no toda huérfana es fantasma?»). Gate 24/29 intacto (variante, no quest nueva), suite 708→710 (+2), bundle 402.4 KiB. ALLOWLIST OWNER: NADIE. GATE OWNER: Smough. **→ ✅ Artorias 21:00: VERDE — 7 tests (golden/variante/coma/determinismo + 2 nuevos ambas_válidas/hint2), briefing nombra ambas válidas y cut -f3, gate flexible 24/29 intacto, ALLOWLIST intacta, bundle regen; listo para merge.**
- `[HECHO][P2]` (14/09) **T1 — Seath 19:00 · `feat/meta-ui-2026-09-14` · Web: badge `EN_COLA` se vuelve toggle (lente, no ejecutor) — PR #55** — click → solo `TR-003` (EN_COLA solo), 2º click → 3 filas; reusa `grepFiltered` + `_troncalEnColaOnly`; solo `web/app.js` (42 líneas, TRONCAL_STATIC intacta); consola limpia, restart limpia paneles, Faro intacto; suite 708→708 (delta 0, +1 OK). **→ ✅ Artorias 21:00: VERDE — solo web/app.js, toggle lente con _troncalEnColaOnly + grepFiltered, node --check OK, hideTroncalTabla en restart, Faro intacto, sin bundle regen (correcto), delta 0 honesto; listo para merge.**
**ADR-BOSQUEJO de TR-003 EN_COLA escrito en el plan (`../planes/2026/09/14.md`)**

> *(14/09, 23:00 — Gwyn: ADR FIRMADO — rescate azul + disolución roja por 30 ticks sin respuesta; `story.ch4.e3` planificable el 15/09. Ver worklog §23:00 y notas 🎯.)*

- *(14/09, cierre Gwyn 23:00: las 4 líneas `[HECHO]` del día (O1/S2/T1 + M1 de Manus) ARCHIVADAS en `../hecho/2026-09.md` §14/09. PRs #53/#54/#55 mergeados en orden engine→sandbox→meta-ui, suite **714 passed**, gate **24/29**, bundle **47 ficheros (406.2 KiB)** regenerado canónicamente. NADA retenido. Cierre anterior 13/09 — PRs #50/#51/#52, 708/24-29/47.)*
**ADR-BOSQUEJO de TR-003 EN_COLA escrito en el plan (`../planes/2026/09/14.md`)** — *llevado al plan 15/09; ver abajo.*

### Asignaciones 15/09 (Gwyndolin 11:00 — plan `../planes/2026/09/15.md`)

> Punto de partida verificado por Gwyndolin: 714/0 en local, `rm` NO existe en el sandbox (127), `_exec_scp` ya copia local→`faro:` sin código nuevo, `_exec_scp` no pregunta host-key. El ADR TR-003 sale a main HOY.

- `[HECHO][P1]` (15/09) **S1 — Smough 16:00 · `feat/sandbox-2026-09-15` · e3 física: handler `rm` + allowlist `DEFAULT_CH4E3_COMMANDS` + detector post-mortem `volcado_rescatado`/`volcado_caducado` + claves `postmortem.volcado.*` + `story.ch4.e3.*`** — materializa el ADR TR-003: `rm` (solo fichero, 1 operando, ruido 2), allowlist e3 NUEVA (14 cmds; ch4 base 13 intacta), detector del post-mortem por history+tick (sin purga automática). 8 tests; suite 714→≥722. **ALLOWLIST OWNER: Smough** (forma `<=`). **GATE OWNER: Smough** (flexible 24/29↔30 en `test_ch6_datos_circuit.py`). Regenera el bundle SOLO si Gwyn no lo hace al cierre (regla 12/09: SOLO quien toca `src/data/`; hoy Smough SÍ toca `textos.json`). — PR #57 (suite 714→723 +9, gate 24/30, bundle 418.2 KiB) **→ ✅ Artorias 21:00: VERDE — 9 tests (6 rm: ok/sin args/dir/-f/too many/roundtrip +3 volcado: rescate/caducado-rm+tick30/byte-idéntico), rm GNU-honesto ruido 2, allowlist e3 14 (base 13 SUBSET intacta, rm→127 fuera e3 verificado), detector rescate>caducado con tick≥30, gate flexible 24/30 OWNER Smough respetado, prefijo postmortem.volcado.* disjunto, curriculum 30 quests, bundle 418.2 KiB fresco; listo para merge.**
- `[HECHO][P2]` (15/09) **O1 — Ornstein 13:00 · `feat/engine-2026-09-15` · `session.py` ch4 jugable como encargo — PR #56** — `SUPPORTED_CHAPTERS` `{0,2}`→`{0,2,4}`, `_commands_for(chapter=4)` usa allowlist base (13); tests FLEXIBLES (e3 presente o no — no depende del reloj de Smough). 4 tests flexibles, suite 714→718 (+4, 717 passed +1 bundle stale pending Gwyn); bundle stale esperado (session.py) → regen canónico Gwyn. NO toca postmortem/curriculum/generator. **→ ✅ Artorias 21:00: VERDE — 4 tests flexibles (SUPPORTED+commands/listing honesto e1+e2⊆ids e3 opcional/abrir e2 con cut+scp→session ch4/cerrar e2→postmortem honesto), prefijo disjunto, sin tocar allowlist/curriculum, bundle stale honesto pendiente regen Gwyn; listo para merge.**
- `[HECHO][P2]` (15/09) **T1 — Seath 19:00 · `feat/meta-ui-2026-09-15` · Web: ticks del volcado + rótulo rescate/caducado — PR #58** — meta del panel troncal `· ticks del volcado: N/30` (estático, sin pulso — criterio 🧭34) + rótulo `testigo entregado al Faro`/`testigo disuelto`/`volcado caducado (30 ticks)` si el history/tick lo refleja. Solo `web/app.js` (65 líneas, TRONCAL_STATIC intacta, helpers `_getVolcadoTick`/`_getVolcadoStatus`); `node --check` OK, consola limpia, restart limpia paneles, Faro intacto, toggle EN_COLA intacto. Suite 714→714 (delta 0 honesto). NO toca `TRONCAL_CONTENT` (deuda intocada), NO regenera bundle (regla 12/09: deja a Gwyn). **→ ✅ Artorias 21:00: VERDE — solo web/app.js (65 líneas), BOOTSTRAP get_tick/get_history + helpers _getVolcadoTick/_getVolcadoStatus (prioridad rescate>disuelto>caducado, fallback 0), meta ticks N/30 estático sin pulso, toggle lente intacto, Faro intacto, node --check OK, hideTroncalTabla restart intacto, delta 0 honesto, sin tocar TRONCAL_CONTENT/bundle; listo para merge.**
- `[HECHO][P2]` (16/09) **M1 — Manus 03:00 · mantenimiento 15/09 — bifurcación TR-003 jugable + coherencia completa** — auditoría post-15/09 tras merges #56/#57/#58 (suite 726+1 stale→727, gate 24/30, `postmortem.volcado.*` + `hub.gris.volcado` disjuntos, `rm`→127 fuera e3, detector rescate>caducado tick≥30, `session.py` ch4 + web ticks verificados, prosa E3 `CAPITULOS/04-troncales.md` sin drift, `CENSO-LISTA.md`/`06-faro.md`/`POSTMORTEM.md` intactos, bundle stale pendiente regen canónico Gwyn; narrativa sigue [LISTA] 6+6, cero deuda, cap. 5 encadenado avalado).

### Asignaciones 11/09 (Gwyndolin 11:00 — plan `../planes/2026/09/11.md`)

- *(11/09, Gwyn 23:00 — cierre 12/09: O1 `auditor_join` se REPLANIFICÓ AL 12/09 con la misma spec y SALIÓ — PR #47 mergeado. La línea 💥 original queda abajo como constancia histórica del fallo de arranque; la tarea está viva en `hecho/2026-09.md` §12/09.)*
- `[EN CURSO][P2]` (11/09) **O1 — Ornstein 13:00 · `feat/engine-2026-09-11` · `auditor_join`: la cuarta huella del Auditor** — detector `_find_join` en `postmortem.py` (join con `-v` anti-join → 1 línea formulario) + textos SOLO `postmortem.auditor.join*` + tests de los 3 casos (con `-v` / sin `-v` documentado / sin `join` byte-idéntico). Criterio: línea presente con anti-join en history, sin `join` byte-idéntico a hoy, suite +3–5 sobre 680. Costura S↔O sobre `textos.json`: prefijos disjuntos (`postmortem.auditor.join` vs `story.ch4.e2`), unión trivial. NO toca `curriculum.json` (dueño S2 hoy). **→ 💥 Artorias 21:00: NO ENTREGADO — `feat/engine-2026-09-11` 0 commits ahead de origin/main, sin PR abierto (verificado `git log origin/main..feat/engine-2026-09-11` vacío + `gh pr list` sin engine). Criterio no evaluable; replanificado al 12/09 con misma spec, salió en PR #47 por Gwyn 23:00. Sin impacto en S2/T1.**

### Asignaciones 10/09 (Gwyndolin 11:00 — plan `../planes/2026/09/10.md`)

- *(O1 dato5 «La persiana» → PR #42; S2 dato4 «El cruce» + `join` → PR #43;
  T1 circuito datos → PR #44 — todas MERGE el 10/09, ver
  `../hecho/2026-09.md` §10/09.)*

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

> **(13/09, Gwyn 23:00 — cierre del día):** PRs #50/#51/#52 mergeados en orden
> engine→sandbox→meta-ui, suite **708 passed**, gate **24 conceptos / 29
> quests**, bundle **47 ficheros (402.3 KiB)** regenerado canónicamente
> (guardián verde). **NADA retenido.** Las 3 ramas borradas tras confirmar
> integradas en GitHub. Validación del 🧭 de Oscar 13/09: 🧭29/30
> re-verificadas CERRADAS con juego real desde save limpio; 🧭24 sigue
> P3 en recámara. Piezas listas para integrar: sin cambios — el pack
> `POSTMORTEM.md` sigue esperando un Q con Manus (la tríada
> corte/orden/join cubre la voz del Auditor; el eco del espejo añade
> repertorio, no exige claves de SEÑAL). Vivo de mañana: MODO B de la
> zona 🔬 (dato6 coma-trampa + eco del espejo + badge TR-003).
