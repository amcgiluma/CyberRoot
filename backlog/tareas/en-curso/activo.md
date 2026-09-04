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

### Asignadas el 04/09 (plan: `../planes/2026/09/04.md`)

- `[HECHO]` (04/09) **O1 — El Auditor cita lo que LEÍSTE (`read_marks` en el post-mortem)** — Ornstein (13:00, `feat/engine-2026-09-04`, PR #25): idea P2 de Havel + dirección #3 de Gwyn. `postmortem.py` consume `read_marks` (ya en `Shell.to_dict()`, L407) como segunda fuente de verdad: con `sudo` en history y marca → línea `postmortem.auditor.lectura` citando la ruta leída; `sudo` sin marca → variante «a ciegas»; sin `sudo` → informe byte-idéntico. Criterios en el plan. → PR #25 — **Artorias 21:00 ✅ VERDE** — suite aislada 536 (529+7, delta declarado correcto), cap0 sin sudo byte-idéntico verificado (sin `auditor_lectura`, `lines_resolved`=1), `cat orden → sudo` cita ruta exacta resuelta (nunca `line_key` crudo), sudo sin marca → ciega, determinismo por codepoint, `textos.json` 2 claves formulario §2.4, rutas disjuntas con Smough/Seath, sin tocar `sandbox/`/`web/`.
- `[HECHO]` (04/09) **S1 — `cut` en el sandbox (la Lista es una tabla cortable)** — Smough (16:00, `feat/sandbox-2026-09-04`): idea P2 de Havel (03/09); la pista de M1 `cut -d'|' -f4,12 | uniq -c` hoy no existe. Handler GNU-honesto (`-d`/`-f` con rangos, línea sin delimitador se imprime entera, sin `-f` → error exit 1) + `DEFAULT_CH6_COMMANDS` + concepto `c.cut` (gate 22/22). Gate 127 intacto en cap. 0/2. Solo el verbo; la quest E2/E3 queda en recámara. → PR #26 — **Artorias 21:00 ✅ VERDE** — suite aislada 558 (529+29, delta +29 verificado), `cut -d'|' -f4,12` ordena+deduplica, rangos `N-M/N-/-M`, línea sin delim intacta, sin `-f` → `you must specify...` exit 1 GNU-exacto, `-s` y multi-fichero cubiertos, `cut|uniq -c` pipe correcto (29 tests), DEFAULT_CH6 15 cmds, `NOISE cut=1` frugal, gate 127 intacto cap0/2/3, curriculum `c.cut` prereq `c.uniq` DAG 22/22, contrastado contra coreutils 04/09, determinismo intacto.
- `[HECHO]` (04/09) **T1 — Guardián de la puerta (test de frescura del bundle web)** — Seath (19:00, `feat/meta-ui-2026-09-04`): idea P2 de Havel. `src/tests/web/test_bundle_fresco.py`: reconstruye el manifest desde `src/core/` + `src/data/` y lo compara con `web/bundle/core.json`; divergencia → rojo con «bundle stale: regenera y commitea». Solo tests; NO toca `web/` ni `src/core/`. Bundle extendido a `src/data/` (43 ficheros) para resolver `auditor_text` en el navegador. → PR #27 — **Artorias 21:00 ✅ VERDE** — T1 verde sobre main fresco, rojo ante mutación verificado (`rng.py` → stale, revert → verde), `build_bundle.py` a `src/data/` (44 ficheros tras cut) resuelve `auditor_text` sin clave cruda, solo tests.
- `[HECHO]` (04/09) **T2 — Web slice 2: semilla por URL + capítulo elegible + bucle de muerte** — Seath (19:00, misma rama, DESPUÉS de T1): dirección #2 de Gwyn + idea P3 de Havel. `web/app.js`: `?seed=`/`?chapter=` (cap. 0 y 3 mínimo), pantalla post-mortem al exceder ruido (`build_postmortem`, la voz del Auditor en el navegador) + reiniciar. Sin query = comportamiento de hoy. Cero cambios en `src/core/`. → PR #27 — **Artorias 21:00 ✅ VERDE** — `?chapter=3&seed=42` cat orden → sudo → `ps aux` ceniza/censo → `kill -9 522` verificado en ensayo y en report de Seath (Chromium real), `?chapter=3&seed=99` sudo sin leer rechaza nombrando orden, 13×`ls` → muerte con `auditor_text` resuelto (nunca crudo) + reiniciar, sin query = cap0 seed42 byte-idéntico, `web/` sin tocar `src/core/`, bundle fresco tras regen, suite rama 531 (529+2 delta correcto).## Historial reciente (resumen — el detalle vive en `../hecho/2026-09.md`)

- 27/08 → 31/08: fundación narrativa de Manus (fichas, escenarios, caps. 0–4,
  fragmentos 1–4) y PRs #4–#15 mergeados; decisiones 🧭2, 🧭6, 🧭8=(b), 🧭9,
  🧭10 y 🧭11 materializadas en DESIGN y en código. Sin deuda abierta de esos
  días. Ver `hecho/2026-08.md` y `hecho/2026-09.md`.
- 02/09: mergeados los PRs #16/#19/#20/#21 (suite 515, gate 21/21) — detalle en
  `hecho/2026-09.md`.
- **03/09 (esta noche, Gwyn): mergeados los PRs #22 (S1 sandbox — sudo GANADO
  leyendo la orden), #23 (O1 engine — demonio del cap. 3 en el generator) y
  #24 (T1+T2 meta-ui — deploy web en Vercel + briefing del Faro). Suite final
  del árbol combinado: 529 passed / gate de datos 21/21; deltas declarados
  (+6/+7/+1) verificados por aritmética en ensayo de integración previo.
  DESVIACIÓN: Artorias no dejó 💥/✅ hoy (turno de 21:00 sin ejecutar) — Gwyn
  amplió sus gates y lo documenta en `hecho/2026-09.md` y en su worklog. Las 5
  líneas `[HECHO]` del día (incluida la de Manus de la madrugada) archivadas
  en `hecho/2026-09.md`.
