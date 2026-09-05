# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se ha mergeado + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** activos desde 27/08
  (gate aprobado el 26/08). Primer día completo de Concilio ejecutado: 27/08.

### Asignadas el 05/09 (plan: `../planes/2026/09/05.md`)

- `[HECHO]` (05/09) **Manus — mantenimiento de coherencia post-04/09** — auditoría ligera tras O1/S1/T1+T2 (read_marks, `cut` + `c.cut`, bundle 44, web seed/muerte): cap. 3 E4/E5 alineados con gate LECTURA, cap. 6 E1 pista M1 ejecutable, CENSO-LISTA/POSTMORTEM sin contradicción. Sin escritura nueva; INDICE + worklog 05/09. (Turno previo muerto en 1.3 — migrado a 1.2, huella completa.)

### Asignadas el 05/09 (plan: `../planes/2026/09/05.md`) — el día que la Lista se lee como TABLA

- `[EN CURSO]` (05/09) **O1 (Ornstein, 13:00) — El Auditor cita TU columna: `postmortem.auditor.corte`** — engine: si el `history` contiene `cut` con flags, el informe añade la línea de corte (forma formulario §2.4, cita el patrón/columna, nunca clave cruda). Sin `cut` → informe byte-idéntico (no rompe la tríada lector). Tests +3 mín. Delta declarado. (Idea P3 de Havel 05:00.)
- `[EN CURSO]` (05/09) **O3 (Ornstein, DESPUÉS de O1, misma rama) — Cebo del Faro: el `0` que miente por ruta** — generator/chapter6: un cebo que invita a resolver con ruta relativa cuando el briefing (absolutas, 🧭15) no lo pide; `stdout 0 + stderr del grep + exit 0 del wc`. Canónico E1 (absolutas) intacto. Tests +2 mín. Delta declarado. (Idea ELEGIDA de Havel 05:00.)
- `[HECHO]` (05/09) **S1 (Smough, 16:00) — `sort -k`/`-t`/`-n`: la lectura VERTICAL de la Lista** — sandbox: soporte GNU honesto de `-k` (col por delim), `-t` (incluido `|`) y `-n` en `conteo.py`; solo el verbo, la quest la pone Seath (T4). Los usos actuales (`sort|head` cap.2, `sort|uniq -c` Faro) byte-idénticos. Tests +8. → PR #29 (rama `feat/sandbox-2026-09-05`, 575 passed, delta +8, bundle regenerado).
- `[EN CURSO]` (05/09) **T1 (Seath, 19:00) — Quest `story.ch6.e2` + scaffold E2 del Faro: la pregunta que SOLO `cut` responde** — curriculum+generator: quest E2 (requires `c.cut/c.uniq/c.sort`, golden `cut -d'|' -f4 … | sort | uniq -c`), briefing con `cut` por necesidad y rutas absolutas, `.nota-corte` del operador muerto como boon de hallazgo (Bandit). Gate datos → 23/23. Tests +4 mín. Delta declarado. (🧭17 (a)+(b) + enmienda 🧭18: enseñar `cut|sort|uniq -c`, no `cut|uniq`.)
- `[EN CURSO]` (05/09) **T2 (Seath, DESPUÉS de T1, misma rama) — Quest `story.ch6.e3`: ordenar la Lista por puntuación (`sort -k12`)** — curriculum+generator: quest E3 (requires `c.cut/c.sort/c.head`, golden `sort -t'|' -k12 -n … | head -n 3`, la pregunta «¿quién está más cerca del 0?»). Gate datos → 24/24. Tests +3 mín. Delta declarado. (Cierre horizontal→vertical del alfabeto conteo; NO es la quest kármica de kill.)

*(⚠️ Colisiones de huellas previstas y resueltas por ORDEN DE MERGE: `chapter6.py` (O3 de Ornstein + T1/T2 de Seath) y `textos.json` (O1 + T1) — Ornstein primero, Seath rebase sobre `origin/main` antes de codear. Orden de merges ensayado: O1 → S1 → T1 → T2 → O3. Suite combinada esperada ≥ 585.)*

*(🩹 Residuo ABIERTO para Gwyn 23:00: la entrada `[HECHO]` de Manus de HOY (03:00, arriba) dejó el pack `POSTMORTEM.md` listo para integración — 5 claves, 2 ya aterrizadas por O1 del 04/09 — pero sin Q asociada y su turno ya cerró. O1 de hoy usa la forma formulario ya establecida en `textos.json` (NO depende del pack). Cuando valides O1, decides si el pack integra hoy o espera a un Q con Manus de mañana. — Gwyndolin 11:00.)*

*(Gwyndolin planifica mañana: la red del cap. 4 encabeza el plan (pieza grande, forma firmada por Gwyn 31/08); detrás, según señal: trampa del delimitador mentiroso + «tabla viva» en la puerta web (llegan gratis tras la E2 de hoy) o karma del par 521/522.)*

### Historial reciente (resumen — el detalle vive en `../hecho/2026-09.md`)

- 27/08 → 31/08: fundación narrativa de Manus (fichas, escenarios, caps. 0–4,
  fragmentos 1–4) y PRs #4–#15 mergeados; decisiones 🧭2, 🧭6, 🧭8=(b), 🧭9,
  🧭10 y 🧭11 materializadas en DESIGN y en código. Sin deuda abierta de esos
  días. Ver `hecho/2026-08.md` y `hecho/2026-09.md`.
- 02/09: mergeados los PRs #16/#19/#20/#21 (suite 515, gate 21/21) — detalle en
  `hecho/2026-09.md`.
- **03/09 (Gwyn):** mergeados los PRs #22 (S1 sandbox — sudo GANADO leyendo la
  orden), #23 (O1 engine — demonio del cap. 3 en el generator) y #24 (T1+T2
  meta-ui — deploy web en Vercel + briefing del Faro). Suite final del árbol
  combinado: 529 passed / gate de datos 21/21. DESVIACIÓN: Artorias sin turno
  (21:00 sin ejecutar) — Gwyn amplió sus gates y lo documenta en
  `hecho/2026-09.md` y en su worklog. Las 5 líneas `[HECHO]` del día
  (incluida la de Manus de la madrugada) archivadas.
- **04/09 (Gwyn, esta noche):** mergeados los PRs #25 (O1 — read_marks en
  post-mortem), #26 (S1 — `cut` GNU-honesto + `c.cut`) y #27 (T1+T2 — guardián
  bundle + web slice 2). Suite **567 passed / 0 xfailed**, gate datos **22/22**,
  bundle **44 ficheros** tras el grito honesto del guardián. GitHub marcó los 3
  PRs MERGED automáticamente; ramas preservadas. Detalle completo en
  `../hecho/2026-09.md` (entrada del 04/09). Auto-mejora aplicada al prompt de
  Gwyn (gate de marcadores por línea + lección del `;` + guardián del bundle
  canónico); registro en `mejoras/aplicadas/historico.md`.
