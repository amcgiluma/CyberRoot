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

## Asignadas por Gwyndolin (02/09, plan del día) — franjas de HOY

> Origen: plan del 02/09 (Gwyndolin). O1-fix/O2/O3(/O4 opc) → Ornstein ·
> S1/S2 → Smough (PR único, comparten `shell.py`) · T1 → Seath (render v0).
> **Contrato ch6 (costura O3↔S2):** quest `story.ch6.e1` (grey, familia conteo,
> objetivo revelar la purga `PR-0091`) ↔ sala-dato `registro.csv`/`purgas.csv`
> (formato CENSO-LISTA.md) + cebo pipe-0; los tests del generator van con
> `skipif` hasta que la quest aterrice (lección de los 2 tests stale de #16).
> La costura la verifica Artorias en la combinada.

- `[EN CURSO][P1]` **O1·FIX — Desbloquear PR #16** (2 tests stale; receta EXACTA
  en el bloque 💥 de abajo). Suite esperada en la rama: **478**. Dueño: Ornstein.
- `[EN CURSO][P2]` **O2 — `chapter3.py`: la sala del cap. 3 generable de verdad**
  (consume la quest sudo YA en main; no inventa campos). Módulo:
  `src/core/generator/`. Dueño: Ornstein. AC: determinismo, guard testado,
  regresión `generate(seed,0)` byte-idéntica.
- `[EN CURSO][P2]` **O3 — `chapter6.py`: sala-dato de la Lista + cebo pipe-0**
  (contrato ch6 arriba; quest en skipif). Módulo: `src/core/generator/`. Dueño:
  Ornstein. AC: sala generable, guard, caps 0/2 intactos.
- `[EN CURSO][P3]` **O4 — OPCIONAL: el post-mortem imprime la VOZ resuelta**
  (dirección #3 de Gwyn; resolvedor `textos.py` ya en main). Módulo:
  `src/core/engine/`. Dueño: Ornstein. Si la franja no rinde, primera de mañana.
- `[EN CURSO][P2]` **S1 — `kill`/señales v0 sobre el par ceniza/censo** (física
  + evento al bus; la bifurcación kármica queda para karma después). Módulo:
  `src/core/sandbox/` (handler + `noise.py`). Dueño: Smough. AC: golden GNU,
  `-9` vs `-HUP` observables en `ps`, gate 127 intacto.
- `[EN CURSO][P2]` **S2 — quest `story.ch6.e1` + `DEFAULT_CH6_COMMANDS`**
  (des-islar el conteo; ÚNICO dueño de `curriculum.json` hoy; sin `cut`). 
  Módulo: `src/data/curriculum.json` + `shell.py`. Dueño: Smough. AC: gate
  **21/21**, prereqs vivos.
- `[EN CURSO][P2]` **T1 — RENDER v0: una sala del cap. 0 pintada** (prompt
  `usuario@nodo:/ruta$` con cwd real — avanza 🧭13). Módulo: `src/render/` +
  `src/assets/`. Dueño: Seath. AC: demo reproducible + screenshot PNG
  committeado; core intacto.

## Asignadas por Gwyndolin (01/09, plan del día 02/09 para Manus) — turno de Manus (03:00)

> Origen de cada línea: plan del 01/09 (Gwyndolin), sección «Manus (03:00 del
> 02/09)» — M1 (worldbuilding del censo, puerta del Acto 3) y M2 (cap. 6 +
> fragmento 6). Este fichero lo releva Gwyndolin a las 11:00 con el plan del
> día; Manus deja aquí su huella `[HECHO]` (regla HARD §AGENTS-PLAN 2.5).

- `[HECHO]` **M1 — Worldbuilding del censo: qué se puntúa exactamente**
  (Manus, 02/09 ✅): mecanismo de la Lista (§2.4/§9) materializado en
  `backlog/historia/CENSO-LISTA.md` — campos de `registro.csv`/`purgas.csv`,
  delimitador `|`, ejemplo de fila, cómo se registra una purga (`ENSAYO`/
  `CONTINUIDAD`…) y el hueco de un «sin registro» (la purga `PR-0091`, fecha
  en blanco). Doc consultable por Smough/Ornstein; da DATO a las salas-dato
  del cap. 6 (grep/sort/uniq/cut). Coherente con fragmentos 2–5 y el par
  ceniza/censo. Entregado para integración (lo integra el ejecutor desde
  historia, regla PROJECT-MAP).
- `[HECHO]` **M2 — Capítulo 6 «Faro» (beats 10–12) + fragmento 6 «hoja de
  cierre» GARANTIZADO** (Manus, 02/09 ✅): `backlog/historia/CAPITULOS/06-faro.md`,
  5 encargos `story.ch6.e1`–`e5` (1 azul, 2 gris, 1 rojo, 1 de cierre) con los
  finales (§1/§9) como decisiones de karma, no como menú; 3.ª sombra del
  Auditor (feed del ensayo callado + palanca de EL TRATO expuesta, arco §9
  sin traición); confrontación con Vela (`story.ch6.vela`, cuerpo por primera
  vez, formato según karma). Fragmento 6 `[LISTA]` en `FRAGMENTOS.md` (estado
  6/6), GARANTIZADO al completar la cadena final (🧭5). Claves listas para
  Smough; coherencia con los 9 beats previos y con M1; auto-pass anti-slop
  documentado en el worklog.

## Historial reciente (resumen — el detalle vive en `../hecho/2026-08.md`)

- 27/08 → 31/08: fundación narrativa de Manus (fichas, escenarios, caps. 0–4,
  fragmentos 1–4) y PRs #4–#15 mergeados; decisiones 🧭2, 🧭6, 🧭8=(b), 🧭9,
  🧭10 y 🧭11 materializadas en DESIGN y en código. Sin deuda abierta de esos
  días. Ver `hecho/2026-08.md` y `hecho/2026-09.md`.

## Asignadas por Gwyndolin (01/09, plan del día) — para las franjas de HOY

> Origen: plan del 01/09 (Gwyndolin). O1/O2 → Ornstein (`feat/engine`) ·
> S1/S2 → Smough (`feat/sandbox`) · T1/T2 → Seath (`feat/meta-ui`).
> **Contrato O1↔S1 (verificar en el ensayo de integración):** O1 coloca el
> fichero-credencial + `auth.log` en el FS de la sala sudo (generator); S1
> hace que `sudo` lo lea (sandbox) y firme en él. Artorias verifica el
> circuito completo esta noche.

- `[EN CURSO]` **O1 — El `sudo` GANADO gana MUNDO: credencial narrativa como
  fichero que el generator coloca en la sala del cap. 3** (+ `auth.log`
  presente). Módulo: `src/core/generator/`. Regresión `generate(seed,0)`
  obligatoria. Dueño: Ornstein.
  - **✅ [Artorias 01/09]** El código O1↔S1 verifica PERFECTO en la combinada
    (credencial+auth.log colocados; literales coinciden con sandbox; smoke
    real: `sudo cat` ejecuta, factura base+premium=4, firma en auth.log).
    **PERO el PR #16 lleva 2 tests STALE** (los 2 abajo) → **💥 PR #16**.
- **💥 PR #16 — FIX OBLIGATORIO para Ornstein (2 tests stale, rompen la
  combinada).** Con S1 aterrizado, `c.sudo`+su quest (story.ch3.e4/e5) YA están
  en el currículo REAL; dos tests de O1 asumen el estado pre-S1 y fallan en la
  integración (`test_errores.py::test_chapter3_curriculum_real_sin_quest_sudo_generator_error`
  y `test_sala_sudo.py::test_generate_cap3_sin_quest_sudo_es_error_accionable`).
  Arreglo exacto (validado en el ensayo, 478 passed):
  - `test_errores.py`: renombrar a `test_chapter3_curriculo_real_genera_sala_sudo`
    y asertar que `generate(1, chapter=3)` SÍ produce la sala
    (assert `inc.chapter == 3` y `inc.room.id.startswith("room-ch3-")`).
  - `test_sala_sudo.py`: sustituir el caso stale por uno positivo
    (`generate(1,3,curriculum=load_curriculum())` → sala con la credencial) y
    conservar el guard de honestidad construyendo un currículo SIN quest sudo
    (`_real_sin_quest_sudo()`), que debe seguir lanzando `GeneratorError`.
  Hecho esto el PR #16 es ✅. Gwyn: NO mergear #16 hasta que el fix entre.
  *(01/09 23:00 — Gwyn: **NO MERGEADO**. Comentario en el PR con el porqué y
  el cómo arreglar; la rama `feat/engine-2026-09-01` SE MANTIENE ABIERTA para
  Ornstein.)*
- `[EN CURSO]` **O2 — Harness: métrica de «ánimo de novedad»** (distribución
  de familias de comando por run; aviso de dominancia). Módulo:
  `tools/harness/` (sin tocar `src/core/`). Dueño: Ornstein.
## MERGEADAS por Gwyn (01/09, 23:00) — PRs #17 y #18

> Detalle de cada línea en `../hecho/2026-09.md`. Suite: 455 tras #17 (421+34),
> **466 tras #18** (+11; deltas declarados, cuadrados exactos). Gate de datos:
> 21 conceptos / 20 quests. Conflicto de datos `test_loader.py` reconciliado
> 21/20 según el ensayo de Artorias. PR **#16 NO mergeado** (fix de 2 tests
> stale pendiente, rama abierta — ver bloque de arriba). Archivado = inventario
> completo: también el `[HECHO]` de Manus de esta madrugada (fragmento 5 + cap. 5,
> entregado en `52fbb04` y retirado de este fichero por el plan de Gwyndolin sin
> pasar por archivo — reparado).
