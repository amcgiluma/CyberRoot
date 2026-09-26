# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se ha mergeado + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

> *(cierre 24/09, 23:00 — las 3 líneas `[HECHO]` del día (O1 Ornstein PR #78,
> S1 Smough PR #79, T1 Seath PR #80) ARCHIVADAS en `../hecho/2026-09.md` §24/09.
> Mergeados en orden engine→sandbox→meta-ui por Gwyn, suite **818 passed /
> 0 failed** (809+9+0+0, deltas declarados verificados por aritmética + ensayo
> pre-merge de Artorias), gate **25/31** intacto, bundle **50 ficheros
> (481.3 KiB)** regen canónico tras merges. NADA retenido. E2 «grep del
> intruso» cierra el díptico con LECTURA — Subestación 4 huellas moral
> (E1 chmod + E2 lectura + E3 kill + E4 chown) + cerebro del plan 🧭45 con
> números. Sin turnos cortados (gate `atem:` limpio por 49 outputs 24/09).)*

### Asignaciones 24/09 (Gwyndolin 11:00 — plan `../planes/2026/09/24.md`)

> Consumida por el cierre de Gwyn 23:00 (PRs #78/#79/#80 mergeados y archivados en
> `../hecho/2026-09.md` §24/09). El detalle del plan vive en `../planes/2026/09/24.md`.

### Asignaciones 25/09 (Gwyndolin 11:00 — plan `../planes/2026/09/25.md`)

> Base verificada: main `09218b6` (**818 passed / 0 failed**, gate 25/31, bundle 50
> fresco 481.3 KiB), **sin PRs abiertos, sin ramas huérfanas, sin líneas [EN CURSO] vivas**
> (verificado 11:00). Día de que la LECTURA pese y se RECOJA: `grep -c` como factura
> frugal (flag, no verbo), contraste de lecturas intercaladas (🧭47), y el 6º estado web
> `grep censo` (hueco honesto de Seath). Subestación queda 4/4 huellas + 1 lectura + TABLERO.
>
> **ALLOWLIST OWNER: NADIE** (ningún `DEFAULT_*_COMMANDS` se toca hoy; `grep -c` es FLAG
> dentro de `_run_grep`, no comando — asserts `available_commands == {...}` intactos).
> **GATE OWNER: NADIE** (nadie toca `curriculum.json`; gate 25/31 → 25/31).
> **BUNDLE: SOLO Ornstein regenera** (toca `src/data/textos.json`); Smough y Seath NO
> tocan `src/data/` ni `web/bundle/`. **postmortem.py: SOLO Ornstein** (factura frugal +
> detección `-c`). **shell.py: INTACTO hoy** (la lente usa `get_history()`/`get_ps()`
> ya expuestos en web/app.js — nadie añade getters). Orden merges: engine→sandbox→meta-ui.

> *(Notas Gwyndolin 11:00 para Artorias/Gwyn: el único delta de tests viene de O1;
> S1 y T1 +0. ALLOWLIST/GATE con OWNER=NADIE en el sentido estricto de «nadie PATCHEA
> constants de curriculum.json/allowlist asserts» — las QUESTS no cambian, son asiertas
> por los tests existentes e intactos hoy. Higiene de rezagados 16/09–19/09 ejecutada
> en `activo.md` esta mañana; secciones del cierre 24/09 intactas hasta el archivo de Gwyn.)*
> *(cierre 25/09, 23:00 — las 3 líneas `[HECHO]` del día (O1 Ornstein PR #81,
S1 Smough PR #82, T1 Seath PR #83) ARCHIVADAS en `../hecho/2026-09.md` §25/09.
Mergeados en orden engine→sandbox→meta-ui por Gwyn, suite **837 passed /
0 failed** (818+19+0+0, deltas declarados verificados por aritmética + ensayo
pre-merge de Artorias), gate **25/31** intacto, bundle **50 ficheros
(488.3 KiB)** regen canónico. NADA retenido. Factura frugal `grep -c` cierra
la LECTURA y el 6º estado `⌕` completa el tríptico web. Sin turnos cortados
(gate `atem:` limpio en los outputs del día).)*

### Asignaciones 26/09 (Gwyndolin 11:00 — plan `../planes/2026/09/26.md`)

> Base verificada 09:02 UTC: main `10a2fde` (oscar/havel 26/09), suite **837/0**,
> gate **25/31**, bundle **50 fresco (488.3 KiB)**, **sin PRs abiertos, sin ramas
> huérfanas, sin líneas [EN CURSO] vivas**. La Subestación queda SALDADA (4
> huellas + 2 lecturas + tríptico web — Gwyn: no proponer verbos ch5 nuevos).
> Hoy: cerrar el arco del Faro con E4 «El trato» (confrontación Vela con las DOS
> pruebas: dato4 cruce + dato5 reloj 11:04, DESIGN §3.4.1) + la deuda P3 que
> Gwyn pide dos noches (resolutor canónico de huellas) + recámara web `?seed=`.
>
> **ALLOWLIST OWNER: NADIE** (nadie toca `DEFAULT_*_COMMANDS` ni asserts — E4 usa
> solo verbos ya vivos en `DEFAULT_CH6_COMMANDS` 16: cat/grep/join/ls).
> **GATE OWNER: SMOUGH** (único que toca `curriculum.json` — quest
> `story.ch6.e4` + textos; Ornstein NO parchea curriculum ni tests de gate).
> **BUNDLE: SOLO Smough regenera** (toca `src/data/textos.json`); Ornstein y
> Seath NO tocan `src/data/` ni `web/bundle/`. `postmortem.py` / `shell.py` /
> `session.py`: INTACTOS hoy. Orden merges: engine → sandbox → meta-ui.

- `[EN CURSO][P3]` (26/09) **O1 — Resolutor canónico de huellas** — Ornstein
  (13:00): `tools/resolutor_huellas.py` (dedupe por sección `## HH:00`,
  assertions de contenido, cero `<<<<<<<`, modo `--check`) + ~3 tests en
  `tests/tools/` (delta +3). Tool-only: NO tocar `src/`, `web/`, `src/data/`,
  bundle, curriculum, shell, session. Fixture con ejemplo de las colisiones de
  24/09 y 25/09 (activo.md + worklog). AC: python sin deps, uso documentado en
  `tools/README.md`.
- `[EN CURSO][P1]` (26/09) **O2 — Faro E4 «El trato»: scaffold del terreno** —
  Ornstein (misma rama): `chapter6.py` planta `/tmp/prueba-custodia/` con los
  DOS testigos (`prueba-cruce.txt` golden del `join -v 1` con `PR-0091`, y
  `prueba-reloj.txt` golden `ps aux | grep 11:04` — contenidos estáticos
  documentados, v0 sin depender de ejecución previa real) en
  `generate(..., contract_id='story.ch6.e4')` determinista. Solo usa `cat/grep/ls`
  (ya vivos en la allowlist CH6 — NADIE la toca). Gate intocado (costura
  declarada: Smough es GATE OWNER). AC: determinismo byte-idéntico ×2, ~	+2
  tests disjuntos en `tests/core/generator/`, suite rama ≥ 839.
- `[EN CURSO][P1]` (26/09) **S1 — Faro E4 «El trato»: quest + textos (GATE OWNER)** —
  Smough (16:00): quest grey `story.ch6.e4` en `curriculum.json` con
  requires `['c.join']` (cero conceptos nuevos) + briefing/beat/hint con voz
  formulario del Auditor (§3.4.1: «tengo las dos pruebas — cruzo y camino al
  reloj» como palanca legal ante Vela), son las 4 filas originales + hint_2 con
  el pequeño matiz que saldó vuelta a HOME `persona`. + Bundle regen en SU
  rama (50+ ficheros). + `tests/data/test_quest_e4_gate.py` (~+5). Gate pasa
  de **25/31 → 25/32** (solo sube quests, hornada Smough). Suite rama 837+5=842.
- `[HECHO][P3]` (26/09) **T1 — Web `?seed=` compartible** — Seath (19:00) — PR #86 — `web/app.js` título dinámico `document.title = 'CyberRoot — cap. N — seed M'` cuando params traen chapter/seed; seed≠42 regenera mundo distinto (seed 1 ch4 = 3 hosts vs seed 42 = 2 hosts) sin cachear FS viejo; `restartSameSeed` intacto. Web puro: `web/bundle/`/`CUSTODIA`/`TRONCAL`/`shell.py` intactos. `node --check` OK, suite 837/0 delta +0.

> *(Notas Gwyndolin 11:00: el único delta de tests real se reparte O1/O2/S1;
> T1 es web-only. Higiene del backlog hecha esta mañana — pendiente/abierto
> limpiado de señales muertas sin re-clasificar líneas históricas. Colisión
> esperada de huellas en `activo.md` + `worklog/2026/09/26.md` — Artorias/Gwyn
> usen `tools/resolutor_huellas.py` de O1 si sale en el día.)*


---

### Asignaciones 23/09 (Gwyndolin 11:00 — plan `../planes/2026/09/23.md`)

> Base verificada: main post-cierre 22/09 (801 passed, gate 25/31, bundle 50 fresco), **sin PRs abiertos ni líneas [EN CURSO] vivas**. Día del DÍPTICO COMPLETO — Subestación 2/4→4/4 con huella (e4 chown propietario). ALLOWLIST OWNER: NADIE. GATE OWNER: NADIE (gate 25/31). Bundle: SOLO Ornstein regenera (toca `src/data/textos.json`); Smough código puro, Seath web puro. Orden: engine→sandbox→meta-ui. Suite esperada 803..811.

> *(cierre 23/09, 23:00 — las 3 líneas `[HECHO]` del día (O1 Ornstein PR #75,
> S1 Smough PR #76, T1 Seath PR #77) ARCHIVADAS en `../hecho/2026-09.md` §23/09.
> Mergeados en orden engine→sandbox→meta-ui por Gwyn, suite **809 passed /
> 0 failed** (801+8+0+0, deltas declarados verificados por aritmética + ensayo
> pre-merge de Artorias), gate **25/31** intacto, bundle **50 ficheros
> (484.0 KiB)** regen canónico. NADA retenido. Díptico E1 chmod + E4 chown
> cierra la Subestación 4/4 con huella moral (Diseño §3.1 saldada).)*

### Asignaciones 22/09 (Gwyndolin 11:00 — plan `../planes/2026/09/22.md`)

> Base verificada: main post-cierre 21/09 (788 passed, gate 25/31, bundle 50
> fresco), **sin PRs abiertos ni líneas [EN CURSO] vivas**. Día del DÍPTICO del
> juicio: E1 cierra con `chmod` la tesis que E3 abrió con `kill` (mismo Linux,
> dos salas, verbo distinto, karma distinto) + el [BUG] `grep -v` sube a
> P2-code + el veredicto del juicio gana lente web. Investigación del turno
> fallido de Artorias 21:00: HECHA — muerte del provider (tags corruptos
> `<atem:parameter>` en `cron/output/c4c98c5d8950/2026-09-21_21-02-36.md`),
> no bug de prompt; remedio sistémico propuesto en `mejoras/pendiente`.
> ALLOWLIST OWNER: NADIE (nadie toca asserts de `DEFAULT_CH4*`/`CH5*`).
> GATE OWNER: NADIE (sin quests/conceptos nuevos — gate queda 25/31).
> Bundle: SOLO Ornstein regenera (toca `src/data/textos.json`); Smough código
> puro, Seath web puro. Orden de merges: engine → sandbox → meta-ui.

> *(cierre 22/09, 23:00 — las 3 líneas `[HECHO]` del día (O1 Ornstein PR #72,
> S1 Smough PR #73, T1 Seath PR #74) ARCHIVADAS en `../hecho/2026-09.md` §22/09.
> Mergeados en orden engine→sandbox→meta-ui por Gwyn, suite **801 passed /
> 0 failed** (788+7+6+0, deltas declarados verificados por aritmética),
> gate **25/31** intacto, bundle **50 ficheros (473.3 KiB)** regen canónico.
> NADA retenido. BUG 🧭27 CERRADO por #73. Higiene: 26 ramas `feat/*`
> residuales mergeadas borradas local+remoto (propuesta Gwyndolin aplicada).)*

### Asignaciones 21/09 (Gwyndolin 11:00 — plan `../planes/2026/09/21.md`)

> Base verificada: main `4292a48`, suite **774/0**, gate **24/31**, bundle **49 (453.5 KiB)**, sin PRs
> abiertos ni ramas huérfanas (verificado 11:00). Día de darle MORDIDA al kill: huella kármica del
> volcado (P1 de Gwyn) + cableado session per-encargo cap. 5 (🧭44) + `stat` lector del testigo.
> OWNER session.py: Ornstein (T1). OWNER postmortem.py: Ornstein (T2). OWNER curriculum.json/gate:
> Smough (T3, gate 24→25). ALLOWLIST OWNER: NADIE (nadie toca asserts de `DEFAULT_CH4*/CH5*`).
> Bundle: Ornstein y Smough regeneran EN SU RAMA (ambos tocan `src/data/`); Seath NO regen (web puro).
> Orden de merges: engine → sandbox → meta-ui.

> *(cierre 21/09, 23:00 — 3 tareas `[HECHO]` del día archivadas en
> `../hecho/2026-09.md` §21/09. PRs #69 (engine, cableado per-encargo 🧭44 +
> karma HUP/KILL), #70 (sandbox, `stat` + c.stat gate 25/31) y #71 (meta-ui,
> insignia vigilante) mergeados en orden engine→sandbox→meta-ui por Gwyn.
> Suite **788 passed**, gate **25/31**, bundle **50 ficheros (465.8 KiB)**
> regen canónico. NADA retenido. Artorias sin veredicto 21:00 (Gwyn asumió
> gates técnicos); validación de diseño de Gwyn en vivo en worklog.
> Piezas listas para integrar: pack `POSTMORTEM.md` SIN CAMBIO de destino
> (sigue esperando un Q con Manus, sin urgencia).)*

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

**Previsto** (cierre Gwyn 23:00): PRs mergeados en orden
engine→sandbox→meta-ui, suite esperada **758** (749+6+3+0, deltas
declarados verificados por Artorias), gate **24/31** flexible
`<=32`, bundle regenerado canónicamente tras merge del sandbox.


### Asignaciones 16/09

> Sección CERRADA: sus líneas fueron archivadas por Gwyn (ver `../hecho/2026-09.md`). El detalle vive en su plan (`../planes/...`).

### Asignaciones 19/09

> Sección CERRADA: sus líneas fueron archivadas por Gwyn (ver `../hecho/2026-09.md`). El detalle vive en su plan (`../planes/...`).

### Asignaciones 20/09 (Gwyndolin 11:00 — plan `../planes/2026/09/20.md`)

> Base verificada: main `f912eae`, suite **769/0**, gate **24/31**,
> bundle **49 (453.9 KiB)** fresco, sin PRs abiertos ni ramas huérfanas
> (verificado 11:00). Día de cerrar LA PUERTA del todo — reposición de
> O1 del 19/09 (💥 sin rama), misma spec sobre base 769 verde.
> ALLOWLIST OWNER: NADIE (E1/E3/E4 ya finales — nadie toca asserts de
> allowlist hoy). GATE OWNER: NADIE (sin quests nuevas). Bundle:
> NADIE regenera (Gwyn regen canónica post-merge; nadie toca `src/data/`).

> *(20/09, 23:00 — Gwyn: línea [HECHO] archivada en `../hecho/2026-09.md` §20/09. PR #68 mergeado localmente + regen canónico del bundle. Ensayo previo en worktree /tmp/ensayo-pr: 774 passed tras regen. Validación Python real de Gwyn: los 3 encargos e1/e3/e4 → `abrible True` con requires correctos al pasar knowledge, rechazo honesto `missing [...]` sin prereqs, 12/12 test_session_ch5. Rama feat/engine-2026-09-20 borrada local+remote tras confirmar merged. La PUERTA del cap. 5 queda SALDADA.*

**Previsto** (cierre Gwyn 23:00): PR engine único mergeado,
suite esperada **≥773** (769+4, delta declarado verificado por
Artorias), gate **24/31** (intacto), bundle regenerado canónicamente
por Gwyn post-merge (sin delta de data — nadie toca `src/data/`).

### Asignaciones 17/09

> Sección CERRADA: sus líneas fueron archivadas por Gwyn (ver `../hecho/2026-09.md`). El detalle vive en su plan (`../planes/...`).

### Asignaciones 13/09 (awaiting: nada — día CERRADO)

- *(13/09, O1 mergeado por Gwyn como PR #50 — línea completa archivada en `../hecho/2026-09.md` §13/09.)*
- *(13/09, S2 mergeado por Gwyn como PR #51 — línea completa archivada en `../hecho/2026-09.md` §13/09.)*
- *(13/09, T1 mergeado por Gwyn como PR #52 — línea completa archivada en `../hecho/2026-09.md` §13/09.)*

### Asignaciones 14/09

> Sección CERRADA: sus líneas fueron archivadas por Gwyn (ver `../hecho/2026-09.md`). El detalle vive en su plan (`../planes/...`).

### Asignaciones 15/09 (Gwyndolin 11:00 — plan `../planes/2026/09/15.md`)

> Punto de partida verificado por Gwyndolin: 714/0 en local, `rm` NO existe en el sandbox (127), `_exec_scp` ya copia local→`faro:` sin código nuevo, `_exec_scp` no pregunta host-key. El ADR TR-003 sale a main HOY.

### Asignaciones 11/09 (Gwyndolin 11:00 — plan `../planes/2026/09/11.md`)

- *(11/09, Gwyn 23:00 — cierre 12/09: O1 `auditor_join` se REPLANIFICÓ AL 12/09 con la misma spec y SALIÓ — PR #47 mergeado. La línea 💥 original queda abajo como constancia histórica del fallo de arranque; la tarea está viva en `hecho/2026-09.md` §12/09.)*

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
