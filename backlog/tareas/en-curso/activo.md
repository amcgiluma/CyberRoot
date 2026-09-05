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

### ⚠️ Deuda de NAMESPACE para Gwyndolin (abierta por Gwyn, 05/09 23:00)

- Las quests `story.ch6.e2` (sala-dato «El corte de la Lista») y
  `story.ch6.e3` (sala-dato «Los más cerca del cero») entradas hoy en
  `curriculum.json` **OCUPAN los IDs que la prosa del cap. 6 reserva para los
  encargos narrativos E2 «La que no pesa» y E3 «La persiana»**
  (`CAPITULOS/06-faro.md`; las e4/e5 narrativas quedarían igualmente
  colisionadas más adelante). Precedente ch1/ch3/ch5: curriculum E-space = 1:1
  con los encargos de la prosa. Al integrar el cap. 6 completo (los encargos
  narrativos con su beat de karma), hay que resolver ANTES de tocar
  `curriculum.json`: renombrar las quests-sala-dato (p. ej.
  `story.ch6.dato2/dato3` o `story.ch6.e2.sala`) y actualizar sus `requires`,
  scaffolds, tests y briefings, o renumerar los encargos narrativos en la prosa
  (requiere tocar `CAPITULOS/06-faro.md` + `textos.json`). Las salas-dato de
  hoy son correctas pedagógicamente (boon de hallazgo + necesidad Bandit,
  §4.4) — solo es un choque de números, no de diseño. **NO planificar encargos
  narrativos del cap. 6 sin decidir esto primero.**

### Piezas listas para integrar (sección nueva — Gwyn 05/09, aplicación de la propuesta de Gwyndolin)

- **Pack `POSTMORTEM.md` de Manus (04/09, entrada `[HECHO]` 05/09 03:00)**: 5
  claves del Auditor (`prueba`/`sin_lectura`/`senal_muerte`/`senal_recarga`/
  `ceniza.llave`) listas para `src/data/textos.json`; 2 ya aterrizadas por O1
  del 04/09 vía forma formulario. DECISIÓN de Gwyn (05/09): **espera a un Q
  con Manus** — la pieza no es urgente (O1 ya cubrió la voz equivalente) y
  merece un turno con dueño en caliente, no una integración nocturna. Dueño
  propuesto: Manus con Ornstein de integrador. Contrato del pack: reglas de
  montaje en `backlog/historia/POSTMORTEM.md` §Reglas.

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
- **05/09 (Gwyn, esta noche):** mergeados los PRs #28 (O1 —
  `postmortem.auditor.corte` + O3 — cebo de ruta `LEEME.txt`), #29 (S1 —
  `sort -k`/`-t`/`-n` GNU honesto) y #30 (T1+T2 — quests E2/E3 salas-dato del
  Faro + `.nota-corte`). Suite final del árbol combinado: **590 passed /
  0 failed** (567 base +6 +8 +8; el +1 sobre 589 es el skip honesto de E3 que
  pasa tras S1), gate de datos **22 conceptos / 23 quests** (+2 quests e2/e3),
  bundle **44 ficheros (310.0 KiB)** regenerado como paso canónico. Gate de
  diseño de Gwyn en vivo: 8/8 PASS sobre `generate(42,6)`. Las 6 líneas
  `[HECHO]` del día (incluida la de Manus de la madrugada) archivadas en
  `hecho/2026-09.md`. Deuda de namespace e2/e3 abierta arriba (para
  Gwyndolin).
