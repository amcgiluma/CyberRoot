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

- `[EN CURSO][P1]` (27/08→28/08) **Canje dicts→`common.events.Event`** en
  `src/core/sandbox/noise.py` — Smough (16:00): los eventos de ruido son hoy
  dicts con la FORMA de `Event`; con PR #1 ya mergeada, el canje es una
  importación + ajuste de tests (lo dejó documentado en su worklog). Que
  Smough lo haga PRIMERO en su turno de mañana, antes de cualquier cosa
  nueva del sandbox.
- `[HECHO][P1]` (28/08) **Retoque del cap. 0** en
  `backlog/historia/CAPITULOS/00-la-firma.md` como consecuencia de 🧭1/🧭2
  (APROBADAS por Gwyn la noche del 27/08, decisión en la sección D1):
  briefing alineado con `ls/cd/cat/cp` (cp YA activado en el sandbox) y prosa
  de la run 0 FALIBLE (el bloque del post-mortem de la primera run deja de
  ser rama muerta). Sube de P2 a P1: Manus la tiene asignada esta noche en
  su línea D1; si no la integra, Gwyndolin la reasigna por la mañana.
  ✅ [HECHO] (28/08, Manus 03:00): dossier con `destino: /usb`, escena técnica
  reescrita con `cp` (misma secuencia canónica del sandbox, salida línea a
  línea), recibo del Auditor actualizado y bloque nuevo «run 0 falible» con
  línea de expulsión + reintento. Prosa alineada D1.

## Asignadas por Gwyndolin (27/08, plan del día — sigue viva para el 28/08)

- `[HECHO][P1]` (27/08) **Capítulo 1 «Los Muelles»** (beats 3–4: pacto +
  primera elección azul/rojo, con 🧭3 integrada) — Manus (03:00,
  `CAPITULOS/01-los-muelles.md`).
  ✅ [HECHO] (28/08, Manus 03:00): capítulo completo — apertura del pacto
  (Ceniza), regla de la luz diegética vía Gris (🧭3: 23:20 del Umbral bajo,
  22 min de patrulla en el alto, «el Faro no tiene tarifa, tiene dueño»),
  5 encargos integrables (`story.ch1.e1`–`e5`, 2 azules / 1 gris / 1 rojo /
  cierre) con técnico+beat+karma+gancho, escenas reactivas de Zeta, cola de
  post-mortem de Ceniza (3 clases de evento) y gancho al cap. 2 (la ventana
  de las 11:04 se abrió dos veces). Auto-pass anti-slop documentado en
  worklog. Coherencia: grúa nº 9 y lavandería Ciclón registradas en
  ESCENARIOS.md.
  **DECISIÓN DE GWYN (27/08 23:00) — D1 DESBLOQUEADO y OBLIGATORIO esta noche:**
  - 🧭1 **APROBADA**: `cp` es el 4.º concepto del cap. 0. Ya activado en el
    sandbox (`DEFAULT_CAP0_COMMANDS`, suite 225 passed) y DESIGN §6.1/§6.3
    actualizados. El briefing del cap. 0 puede enseñar `cp` POR NECESIDAD:
    copiar ES el objetivo del primer encargo.
  - 🧭2 **APROBADA**: la run 0 SÍ puede fallar, conservando la guía (§2.6.2
    «morir avanza»; enseña muerte=método desde el minuto uno; prometer éxito
    falso es peor). Adecuar la prosa del cap. 0: el bloque del post-mortem de
    la primera run deja de ser rama muerta. (DESIGN ya alineado: §2.5 beat 1
    y fila 0 de la tabla de capítulos retocadas por Gwyn el 28/08.)
- `[HECHO][P3]` (28/08) **Mapa del Concilio (docs/mapa): pasada estética
  visual** — CERRADA por Gwyn (3.ª ejecución del turno del 28/08):
  Chromium headless de Playwright; 73/73 imágenes cargan tras scroll completo
  (las 3 «rotas» iniciales eran `loading="lazy"` fuera de viewport — falso
  positivo), 0 errores JS, 0 peticiones fallidas. Archivada en
  `../hecho/2026-08.md`.

## Manus (27/08, primer turno real) — fundación narrativa ARCHIVADA

*Líneas `[HECHO]` archivadas por Gwyn el 27/08 en `../hecho/2026-08.md`
(viven ya en main): fichas de voz 6/6, escenarios 6/6, fragmento 1, cap. 0.*
> *(28/08, Gwyndolin: el censo (P1→P2) y el drop del último fragmento (P3)
> vuelven a `pendiente/abierto.md` — un `[PENDIENTE]` vive allí, no aquí.)*

## Asignadas por Gwyndolin (28/08, plan del día)

- `[HECHO][P1]` (28/08) **O1 Convención única de tests** — Ornstein
  (13:00): regla escrita en `src/tests/README.md` (espejo del árbol, sin
  `__init__.py` alternativos); cero paquetes `tests` duplicados; 225 passed.
<<<<<<< HEAD
  ✅ ARTORIAS (21:00, PR #4): regla materializada en `src/tests/README.md` Y
  en ley ejecutable (guard `test_tests_layout.py` rompe la suite si aparece
  un `tests/` fuera de `src/tests/`); migración `src/assets/tests/` →
  `src/tests/assets/` hecha; grep negativo verificado en el ensayo de
  integración: **0** `__init__.py` bajo `src/**/tests` fuera de `src/tests/`.
  LISTA PARA MERGE.
- `[EN CURSO][P1]` (28/08) **O2 generator v0: seed→sala con piel real** —
  Ornstein (13:00): sala del cap. 0 + encargo `story.ch1.e1`, determinista
  por seed; andamiaje de la run 0 (cwd/rutas) como DATOS a la espera de la
  decisión de Gwyn esta noche; NO tocar `src/data/curriculum.json` (Smough).
  ✅ ARTORIAS (21:00, PR #4): smoke técnico REAL ejecutado por mí —
  `generate(seed, chapter)` + ciclo de sala completo a mano (5 pasos
  canónicos sobre snapshot del FS, copia CANDELAS verificada en `/usb`);
  determinismo verificado (misma seed → dict idéntico; seeds distintas →
  distintas); validación canónica §6.4.4 con `UnsolvableRoomError` probado
  en negativo (sala rota la detecta). No toca `curriculum.json` (solo lo
  cita en el error de `chapter != 0`). Cumple diseño §4.5/§6.4.4. LISTA
  PARA MERGE.
=======
  ✅ [HECHO] (28/08, Ornstein, PR #4): `src/assets/tests/` → `src/tests/assets/`
  (los 29 tests de Seath intactos, `sys.path` normalizado a import de paquete);
  guard nuevo `src/tests/architecture/test_tests_layout.py` (rompe la suite si
  reaparece un `tests/` fuera de `src/tests/` — la causa del PR #3, ahora
  estructuralmente imposible); README reescrito con la regla + quién toca qué.
  **Suite: 228 passed** (225 + 3 del guard; nota para Artorias: el número
  canónico sube porque el guard añade 3 tests).
- `[HECHO][P1]` (28/08) **O2 generator v0: seed→sala con piel real** —
  Ornstein (13:00): sala del cap. 0 + encargo `story.ch1.e1`, determinista
  por seed; andamiaje de la run 0 (cwd/rutas) como DATOS a la espera de la
  decisión de Gwyn esta noche; NO tocar `src/data/curriculum.json` (Smough).
  ✅ [HECHO] (28/08, Ornstein, PR #4): `core/generator` v0 — `generate(seed,
  chapter, variant)` → `Incursion` determinista (splitmix64 + forks, sin
  `random`); piel EXACTA del cap. 0 verificada byte a byte contra
  `test_session_cap0.py` (variante `canonical`; `practice` añade 1–2 decoys
  por seed); validación canónica §6.4.4 SIEMPRE contra `Shell` real sobre
  copia del FS (irresoluble ⇒ `UnsolvableRoomError`); contrato `story.ch1.e1`
  (azul) con textos solo como claves; andamiaje run 0 como DATOS
  (`scaffold.options` a/b/c, `default=option_b` = «la más barata», decisión
  NO adelantada). 27 tests nuevos (determinismo cross-proceso,
  resolubilidad 50 seeds, roundtrip ensure_plain→JSON, errores, variante).
  **Suite completa: 255 passed.** O3 (harness) queda para mañana: S2
  (curriculum.json de Smough) la hace mucho más útil.
>>>>>>> origin/feat/engine
- `[EN CURSO][P1]` (28/08) **S2 `curriculum.json` v0** — Smough (16:00, tras
  S1): DAG mínimo REAL cap. 0–1 + validador (ciclos/prereqs) + esquema en
  README curriculum. La pieza que desbloquea generator.
  ✅ ARTORIAS (21:00, PR #5): `load_curriculum()` carga desde
  `src/data/curriculum.json` (11 conceptos, 6 quests `story.ch0.ventana` +
  `ch1.e1–e5` con prereqs coherentes con los encargos de Manus); validador
  con 46 tests incl. negativos de ciclo y prereq inexistente. Gate de datos
  (propuesta de Gwyndolin) YA aplicado hoy: el JSON de la rama valida. LISTA
  PARA MERGE.
- `[EN CURSO][P2]` (28/08) **S3 [BUG] `&&`/`;` → rechazo didáctico** — Smough
  (16:00, truncable a mañana): `&;` a `_UNSUPPORTED_SYNTAX` + mensaje que
  insinúe futuro + los 3 repros de Oscar en negativo.
  ✅ ARTORIAS (21:00, PR #5): los 3 repros EXACTOS de Oscar ejecutados en
  vivo sobre la rama → TODOS `exit 2` con el mensaje didáctico («sh: syntax
  not supported in this session: it runs one command at a time (pipes and
  chaining arrive later)»); nadie ya culpa a `cd` ni trata `&&` como
  operando. Cierra el `[BUG][P2]` del 28/08. Cumple 🧭3 (la terminal enseña
  qué llega después). LISTA PARA MERGE. También en PR #5: S1 canje
  dicts→`Event` verificado (deuda del 27/08 saldada, 96 tests sandbox).
- `[EN CURSO][P1]` (28/08) **T1 `state` v0: primer save** — Seath (19:00):
  GameState serializable roundtrip JSON con `version` de formato, envolviendo
  la Shell del cap. 0.
  ✅ ARTORIAS (21:00, PR #6): save/load a DISCO REAL verificado por mí
  (roundtrip idéntico; `saved_at` = tick simulado; `version` 1); versión
  desconocida (9999) rechazada con `SaveVersionError` claro; JSON escrito a
  mano carga igual (§1.5); atomicidad y migraciones probadas en la suite
  (10 tests). Nota NO bloqueante: `core/state/__init__.py` NO re-exporta la
  API pública (`GameState`/`save`/`load` viven en `core.state.state`) —
  Seath: re-exporta antes de que engine/main la consuma. LISTA PARA MERGE.
- `[EN CURSO][P3]` (28/08) **T2 paleta: un idioma en SEMANTIC** — Seath
  (19:00, opcional si T1 verde pronto): claves a UN solo idioma (propuesta);
  Gwyn valida al mergear.
  ✅ ARTORIAS (21:00, PR #6): SEMANTIC 16↔16 en castellano, cero usos de
  claves viejas (grep negativo sobre todo `src/` limpio), suite assets 29
  dentro de la rama. Gwyn valida al mergear. LISTA PARA MERGE.
- `[EN CURSO][P2]` (28/08) **M1 prosa↔FS cap. 0** — Manus (03:00 29/08):
  listado de UNA entrada tras `cd /srv`; `/usb` permanece en raíz (canónico
  para dossier y test); prosa verificada contra `test_session_cap0.py`.
- `[EN CURSO][P1]` (28/08) **M2 fragmento 2 + cap. 2 «Facturas»** — Manus
  (03:00 29/08): pulsera HOSP-47-C (piel propuesta por Havel) + beats del
  cap. 2; auto-pass anti-slop + relectura completa.
