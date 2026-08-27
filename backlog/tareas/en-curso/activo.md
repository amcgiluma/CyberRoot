# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se mergeó + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** creados y PAUSADOS
  (Manus/Havel/Gwyndolin/Ornstein/Smough/Seath/Artorias/Gwyn). Se activan
  tras el gate de Juanma → pendiente de su visto bueno en `../pendiente/abierto.md`.
  → Gate aprobado 26/08; crons `scheduled` desde 27/08 («[GATE APROBADO]» en worklog).

## Asignadas por Gwyndolin (27/08 — plan `../planes/2026/08/27.md`)

- `[EN CURSO][P1]` (24/08→27/08) **Fuente bitmap 5×7 validada** para terminal
  in-game (paleta CRT, capturas reales Pyxel headless) — Seath (`feat/meta-ui`,
  `src/assets/`): es EL riesgo visual nº1 del stack; generar ≥2 capturas
  reproducibles con textos del juego + veredicto de legibilidad en el README.
  *(Recuperada del abierto 24/08; sigue vigente y es ejecutable sin build.)*
- `[HECHO][P1]` (27/08) **Módulo `common`**: RNG seedeada reproducible +
  bus de eventos + tipos base + pytest headless verde desde raíz — Ornstein
  (`feat/engine`, `src/core/common/`): fundamento de sandbox/generator/engine;
  test de reproducibilidad entre procesos incluido. **(PR #1)** 105 tests
  verdes en 0,43 s · cross-proceso verificado (PYTHONHASHSEED distintos +
  Python 3.11/3.12) · guardianes de arquitectura AST probados en negativo.
- `[EN CURSO][P1]` (27/08) **Sandbox mínimo del cap. 0**: FS virtual + shell
  con `ls/cd/cat` (+`cp` SOLO si Gwyn aprueba 🧭1) determinista y ruido por
  acción — Smough (`feat/sandbox`, `src/core/sandbox/`): semántica Linux real,
  tests propios, cero `import pyxel`; pipes/globbing quedan para caps. 1–2.
- `[EN CURSO][P1]` (27/08) **Capítulo 1 «Los Muelles»** (beats 3–4: pacto +
  primera elección azul/rojo, con 🧭3 integrada) — Manus (03:00 siguiente,
  `CAPITULOS/01-los-muelles.md`). D1 condicional: retoque cap. 0 por 🧭1/🧭2
  solo si Gwyn dejó decisión escrita esta noche.

## Manus (27/08, primer turno real)

- `[HECHO]` (27/08) **Fichas de voz 6/6** en `backlog/historia/PERSONAJES.md`
  (Ceniza, Gris, Zeta, El Auditor, Vela, Cero). Desbloquea todo diálogo. ✅
- `[HECHO]` (27/08) **Escenarios con datos base 6/6** en
  `backlog/historia/ESCENARIOS.md` (Subestación, Faro, Umbral bajo/alto,
  Muelles, nodos tipo). ✅
- `[HECHO]` (27/08) **Fragmento 1 `[LISTA]`** (la foto) en
  `backlog/historia/FRAGMENTOS.md` — formato Souls, H1/H2 simultáneos. ✅
- `[HECHO]` (27/08) **Capítulo 0** `backlog/historia/CAPITULOS/00-la-firma.md`
  (Acto 1 beats 1–3: Trabajo en frío → La firma → La Subestación), con
  decisión de karma 1.ª, post-mortem nº 1 y gancho. `[LISTA]` integrable. ✅
- `[PENDIENTE][P1]` (27/08) Worldbuilding fino del **censo** (qué se puntúa
  exactamente) — dueño Manus/Fase 1; bloquea salas-dato del cap. 6 (§9/§6.6.4),
  no cap. 0–4. (Registrado en INDICE.md de historia para Gwyndolin.)
