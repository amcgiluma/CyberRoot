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

## Asignadas por Gwyndolin (01/09, plan del día 02/09 para Manus) — turno de Manus (03:00)

> Origen de cada línea: plan del 01/09 (Gwyndolin), sección «Manus (03:00 del
> 02/09)» — M1 (worldbuilding del censo, puerta del Acto 3) y M2 (cap. 6 +
> fragmento 6). Este fichero lo releva Gwyndolin a las 11:00 con el plan del
> día; Manus deja aquí su huella `[HECHO]` (regla HARD §AGENTS-PLAN 2.5).

- `[EN CURSO]` **M1 — Worldbuilding del censo: qué se puntúa exactamente**
  (Manus, 02/09): mecanismo de la Lista de Lumen (§2.4/§9) en un doc
  consultable por los ejecutores (campos, ejemplo de fila) para las salas-dato
  del cap. 6.
- `[EN CURSO]` **M2 — Capítulo 6 «Faro» (beats 10–12) + fragmento 6
  «hoja de cierre» GARANTIZADO** (Manus, 02/09): 4–5 encargos `story.ch6.*`
  con finales como decisiones de karma (§1/§9), giro del Auditor (3.ª sombra,
  sin resolver), fragmento 6 `[LISTA]` en `FRAGMENTOS.md` (6/6).

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
- `[EN CURSO]` **O2 — Harness: métrica de «ánimo de novedad»** (distribución
  de familias de comando por run; aviso de dominancia). Módulo:
  `tools/harness/` (sin tocar `src/core/`). Dueño: Ornstein.
- `[EN CURSO]` **S1 — `sudo` GANADO en el sandbox** (forma DESIGN §6.1: sin
  credencial → rechazo diegético accionable; con credencial → ejecuta + ruido
  premium + firma en auth.log) + concepto `c.sudo` a `curriculum.json` con
  prereq en la quest sudo del cap. 3. Dueño: Smough.
- `[EN CURSO]` **S2 — Familia conteo: `head`/`tail`/`sort`/`uniq` en el
  sandbox** (golden contra coreutils; `tee`/`less` fuera de hoy). Dueño:
  Smough.
- `[EN CURSO]` **T1 — Primer paquete de TEXTOS en `src/data/`** (🧭12):
  `postmortem.auditor.cruce|pico` con voz formulario del Auditor + textos de
  `story.ch1.e1–e5` desde la prosa de Manus; resolvedor `line_key`+`args` →
  texto; test de cobertura de claves. Dueño: Seath.
- `[EN CURSO]` **T2 — `story.ch5.*` al currículo** (cap. 5 de Manus de esta
  madrugada; prereqs SOLO con conceptos vivos — sin inventar). Dueño: Seath.
