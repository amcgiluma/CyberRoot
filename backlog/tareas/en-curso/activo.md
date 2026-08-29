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

- `[HECHO][P1]` (27/08→28/08) **Canje dicts→`common.events.Event`** — SALDADA: entró mergeado en PR #5 esta noche (Smough). Detalle: `../hecho/2026-08.md`.

## Manus (27/08, primer turno real) — fundación narrativa ARCHIVADA

*Líneas `[HECHO]` archivadas por Gwyn el 27/08 en `../hecho/2026-08.md`
(viven ya en main): fichas de voz 6/6, escenarios 6/6, fragmento 1, cap. 0.*
> *(28/08, Gwyndolin: el censo (P1→P2) y el drop del último fragmento (P3)
> vuelven a `pendiente/abierto.md` — un `[PENDIENTE]` vive allí, no aquí.)*
> *(28/08, Gwyn: cap. 1 «Los Muelles», el retoque del cap. 0 (D1) y el mapa del
> Concilio también archivados — ver `../hecho/2026-08.md`.)*

## Asignadas por Gwyndolin (28/08, plan del día) — MERGEADAS por Gwyn (23:00)

- MERGE: PR #4 (O1+O2) → PR #5 (S1+S2+S3) → PR #6 (T1+T2), en el orden ensayado
  por Artorias. Suite tras merges: **316 passed** (225 + deltas 30/51/10).
  Veredictos ✅ de Artorias y detalle de cada tarea: `../hecho/2026-08.md`.
- Decisión de Gwyn al mergear (🧭2, andamiaje de la run 0): **OPCIÓN B** —
  `initial_cwd=/` y el dossier SIEMPRE con rutas completas; las relativas se
  enseñan en el cap. 1. Escrita en DESIGN §6.1; ya es el `default` del scaffold
  del generator (Ornstein la montó como datos: bien a ciegas). PENDIENTE v0.1:
  que generator CONSUMA el scaffold en la sesión que produce.

- `[HECHO][P2]` (28/08→29/08) **M1 prosa↔FS cap. 0** — Manus (03:00 29/08):
  HECHO. El listado tras `cd /srv` muestra UNA entrada (la oficina);
  `/usb` permanece en raíz (canónico para dossier y test). Prosa verificada
  contra `test_session_cap0.py` (3/3 passed) + sesión canónica ejecutada a
  mano byte a byte. Cierre del `[PENDIENTE][P2]` de Oscar (28/08).
- `[HECHO][P1]` (28/08→29/08) **M2 fragmento 2 + cap. 2 «Facturas»** — Manus
  (03:00 29/08): HECHO. Fragmento 2 «La pulsera» `[LISTA]` en
  `FRAGMENTOS.md` (piel HOSP-47-C propuesta por Havel; NHC 47-C-0191 que
  cruza Muelle/Subestación/Vela y sostiene H1+H2) + `CAPITULOS/
  02-facturas.md` `[LISTA]` (beats del cap. 2: la segunda ventana de las
  11:04, 5 encargos `story.ch2.e1`–`e5` con karma, pipes como primera
  sinergia, la Lista nombrada por Ceniza, gancho al cap. 3). Auto-pass
  anti-slop + relectura completa documentados en el worklog. ⚠️ Para el
  integrador: el bloque de terminal del cap. 2 usa pipes que el sandbox aún
  no soporta (nota en el propio fichero); las claves `story.ch2.*` NO están
  aún en `curriculum.json` (dueño Smough cuando toque el cap. 2).

## Asignadas por Gwyndolin (29/08, plan del día) — detalle completo en `../planes/2026/08/29.md`

- `[EN CURSO][P1]` (29/08) **O1 Generator consume `curriculum.json` real + opción B como comportamiento (🧭7)** — Ornstein (13:00, `feat/engine`): la sala toma quest del pool del capítulo y concept_pool del currículo (adiós al cap. 0 hardcodeado en `chapter0.py` como fuente de datos); la sesión nace del scaffold (`initial_cwd` del `default`, no del default de la Shell). La costura 🧭8 (`contract.objective_key=story.ch1.e1` con prereqs que el cap. 0 no enseña) NO se resuelve hoy: se cubre con test documentado y Gwyn decide esta noche (a)/(b). AC y detalle en el plan.
- `[EN CURSO][P3]` (29/08) **O2 Harness v0: runner de N seeds** — Ornstein (13:00, `tools/harness/`, OPCIONAL si O1 cierra con holgura): 50 seeds cap. 0 → % resolubles (100), determinismo (2.ª pasada idéntica), distribución de conceptos (base para 🧭6 y el «ánimo de novedad» de Havel). AC en el plan.
- `[EN CURSO][P2]` (29/08) **S1 Pasada GNU sistemática `cp`/`cat`** — Smough (16:00, `feat/sandbox`): `cat fichero/` → `Not a directory` exit 1 (hoy vuelca el contenido); `cp dir destino` sin `-r` diagnostica el ORIGEN (`omitting directory`), no el destino. Cierra los 2 `[BUG][P3]` de Havel del 28/08 con tests golden en negativo; `mtime` queda como limitación documentada. Repros exactos en `../pendiente/abierto.md` (28/08).
- `[EN CURSO][P2]` (29/08) **S2 REPL `python -m core.sandbox`** — Smough (16:00, `feat/sandbox`, truncable): `__main__.py` con prompt diegético, una línea = un comando, salida idéntica a la sesión testeada; `exit`/Ctrl-D salen. La primera impresión tangible para Juanma sin esperar al engine. NO tocar `__init__.py` de sandbox (lo hace Seath en T1).
- `[EN CURSO][P2]` (29/08) **T1 Fachadas uniformes** — Seath (19:00, `feat/meta-ui`): re-export en `core/state/__init__.py` (`GameState`, `save_game`, `load_game`) Y en `core/sandbox/__init__.py` (`Shell`) — este segundo fichero lo hace SEATH (dueño meta-ui), no Smough; el `__main__.py` de sandbox es de Smough. Rutas disjuntas garantizadas. Cierra la nota de Artorias y el patrón detectado por Havel hoy.
- `[EN CURSO][P2]` (29/08) **T2 progression v0: primer unlock por competencia** — Seath (19:00, `feat/meta-ui`): `src/core/progression/` mínimo — unlocks de conocimiento en GameState; completar el contrato del cap. 0 marca `c.cp` dominado y persiste en el save. UNA regla, no el árbol entero (§7.6 + §4.2: el espejo acelera, nunca sustituye saber).
- `[EN CURSO][P2]` (29/08, noche) **M1 Fragmento 3 (contrato de alquiler a nombre de nadie)** — Manus (03:00 del 30/08): `[LISTA]` en `FRAGMENTOS.md`, formato Souls, H1/H2, sin contradecir fragmentos 1-2. Dirección de Gwyn (28/08).
- `[EN CURSO][P2]` (29/08, noche) **M2 Capítulo 3 «Bombas» (beats 5–6)** — Manus (03:00 del 30/08): 4-5 encargos `story.ch3.e1–eN` con tints del descenso del Acto 2, escalada Umbral→Faro (regla de la luz §6.0) y la grieta de Ceniza PLANTADA (beat 6 §2.5), sin resolver. AC en el plan.
