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

- `[HECHO][P1]` (24/08→27/08) **Fuente bitmap 5×7 validada** para terminal
  in-game (paleta CRT, capturas reales Pyxel headless) — Seath (`feat/meta-ui`,
  `src/assets/`): es EL riesgo visual nº1 del stack; generar ≥2 capturas
  reproducibles con textos del juego + veredicto de legibilidad en el README.
  *(Recuperada del abierto 24/08; sigue vigente y es ejecutable sin build.)*
  **(PR #3)** CP437 completo (256 glifos): español de serie + extensión
  →←↑↓/—; 29 tests verdes; 3 capturas golden reproducibles (sha256 estables,
  2 ejecuciones verificadas) + zooms ×3; veredicto README: LEGIBLE a 1×,
  pygame-ce descartada. Plan de hitos en `src/assets/PLAN.md`.
  **✅ Artorias (27/08 21:00)**: VERIFICADO — 29/29 tests verdes reproducidos
  por mí; regeneración de capturas golden ejecutada POR MÍ: sha256 idénticos
  byte a byte (`git status` limpio tras `make_captures`); legibilidad
  confirmada de forma independiente (PNG decodificado a matriz ASCII: glifos
  nítidos a 1×). Frontera core/render respetada (pyxel solo en
  `pyxel_capture.py`). LISTA PARA MERGE con UN arreglo previo OBLIGATORIO:
  **borrar `src/assets/tests/__init__.py`** (vacío) — colisiona como paquete
  `tests` con `src/tests/` de Ornstein/Smough: con las 3 ramas juntas la suite
  da 13 errores de colección; sin ese fichero, 225 passed (ensayo de merge de
  las 3 ramas verificado por mí). Doc menor a alinear: README dice «5
  semánticos §8.5» y DESIGN §8.5 define CUATRO (¿GOLD entra o se corrige? →
  decidir Gwyn).
- `[HECHO][P1]` (27/08) **Módulo `common`**: RNG seedeada reproducible +
  bus de eventos + tipos base + pytest headless verde desde raíz — Ornstein
  (`feat/engine`, `src/core/common/`): fundamento de sandbox/generator/engine;
  test de reproducibilidad entre procesos incluido. **(PR #1)** 105 tests
  verdes en 0,43 s · cross-proceso verificado (PYTHONHASHSEED distintos +
  Python 3.11/3.12) · guardianes de arquitectura AST probados en negativo.
  *(Marca `[HECHO]+PR#1` restaurada por Artorias: se perdió de main — incidente
  documentado por Smough en su worklog; vivía solo en `feat/engine`.)*
  **✅ Artorias (27/08 21:00)**: VERIFICADO — 105/105 tests reproducidos por mí
  (27 rng + 19 events + 55 types + 3 guardianes + 1 smoke); smoke técnico
  propio VERDE (seed→secuencia→state roundtrip→bus+handler→Event/Command
  serialización→ensure_plain + reproducibilidad cross-proceso con
  PYTHONHASHSEED 424242 vs 7 = idéntico); splitmix64 propio justificado y
  sin sesgo; guardianes AST de arquitectura funcionando. LISTA PARA MERGE —
  RECOMENDACIÓN: mergearla PRIMERA (es la base; sandbox hoy no la importa, el
  canje dicts→clase es trivial mañana).
- `[HECHO][P1]` (27/08) **Sandbox mínimo del cap. 0**: FS virtual + shell
  con `ls/cd/cat` (+`cp` SOLO si Gwyn aprueba 🧭1) determinista y ruido por
  acción — Smough (`feat/sandbox`, `src/core/sandbox/`): semántica Linux real,
  tests propios, cero `import pyxel`; pipes/globbing quedan para caps. 1–2.
  **(PR #2)** 91 tests verdes · golden tests contrastados contra coreutils
  real · sesión end-to-end de la escena del cap. 0 con datos de Manus +
  reproducibilidad cross-proceso byte a byte · `cp` implementado y testeado,
  desactivado a la espera de 🧭1 (activarlo = 1 línea en
  `DEFAULT_CAP0_COMMANDS`).
  **✅ Artorias (27/08 21:00)**: VERIFICADO — 91/91 tests reproducidos por mí
  (35 commands + 32 fs + 14 shell + 6 noise + 3 sesión + 1 package); smoke
  técnico propio VERDE: sesión completa de sala cap. 0 con la piel EXACTA de
  la escena de Manus (ls→cat→cd→cat relativo, errores GNU reales: cp fuera de
  set→exit 127, globbing→exit 2 didáctico), sesión to_dict/from_dict
  restaurada ejecutando igual, ruido amount por acción = perfil documentado
  (cd:0/ls:1/cat:1), y `cp` habilitado ad-hoc verificando copia+lectura
  (escenario 🧭1 listo). LISTA PARA MERGE. Matiz de gusto (no bloquea): el
  rechazo de sintaxis futura («syntax not supported») me parece acierto
  didáctico; cuando exista engine, valorar que ese error sugiera la solución
  válida en su lugar.
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
