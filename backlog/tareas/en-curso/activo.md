# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se ha mergeado + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

> *(06/09, Gwyndolin — plan del día: 6 tareas movidas aquí desde `abierto.md`
> y de la deuda abajo. El [BUG] `ls -a` entra como S2. Ver
> `../planes/2026/09/06.md`.)*

- `[EN CURSO][P2]` (06/09) **S1 (Smough) — Red simulada cap. 4, pieza 1: `ssh` básico + host-key + stack de conexión** — sandbox puro, sin `scp`/quests/`curriculum.json` (NADA más de red hoy, dirección #2 de Gwyn). Detalle y criterio en el plan.
- `[EN CURSO][P2]` (06/09) **S2 (Smough, tras S1) — [BUG] `ls -a`/`ls -la` parseo de flags + 🧭20-a: dotfiles ocultos sin `-a`** — `.nota-corte` vuelve a hallazgo (fricción Bandit E2). Relleno opcional: `sort --help` en mensajes.
- `[HECHO][P2]` (06/09) **O1 (Ornstein) — `auditor_orden`: el Auditor cita tu `sort -k12`** (hermano del corte; P2 Havel 06/09) — `sort` SIN `-k` no dispara NADA. — PR #31
- `[HECHO][P2]` (06/09) **O2 (Ornstein, tras O1) — Mala leche del Faro: LEEME que tienta (🧭21) + trampa del delimitador (dirección #3)** — cebos de piel en `chapter6.py`, goldens E1/E2/E3 byte-idénticos, bundle regen. — PR #31
- `[EN CURSO]` (06/09) **T1 (Seath) — Rename namespace: `story.ch6.e2/e3` → `dato2/dato3`** — EJECUTA la decisión de Gwyndolin (abajo); rename puro, gate de datos intacto en conteo, bundle regen. Permiso de ruta cruzada a `generator/generator.py` (precedente).
- `[EN CURSO][P2]` (06/09) **T2 (Seath, tras T1) — La tabla viva en la puerta web** (dirección #4 de Gwyn; P2 Havel 05/09) — panel Tabla del Faro en `web/app.js`, refleja el `cut`, sin cambios de core.

- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** activos desde 27/08
  (gate aprobado el 26/08). Primer día completo de Concilio ejecutado: 27/08.
- `[HECHO]` (06/09) **Manus — mantenimiento de coherencia post-05/09 (Faro cerrado)** — auditoría ligera tras O1/S1/T1+T2 (590 passed, 22/23, bundle 44: `cut` + `sort -k` + E2/E3 sala-dato + LEEME + .nota-corte + corte del Auditor). Verificado `generate(42,6)` 6 ficheros + goldens E2/E3 + cebo ruta honesto; `CENSO-LISTA.md`/`06-faro.md`/`POSTMORTEM.md` sin contradicción; deuda namespace e2/e3 confirmada y documentada en `historia/INDICE.md` con recomendación (`dato2`/`dato3`); suite y bundle verdes, sin escritura nueva de capítulos.

### ⚠️ Deuda de NAMESPACE para Gwyndolin (abierta por Gwyn, 05/09 23:00) — ✅ DECIDIDA por Gwyndolin (06/09, plan del día)

> **DECISIÓN (06/09, Gwyndolin):** E-space 1:1 con la prosa; las salas-dato
> usan **`story.ch6.datoN`** (opción 1 de Manus): `e2`/`e3` →
> `dato2`/`dato3`. La `e1` no se toca (la prosa E1 ES la sala de la Lista).
> La prosa de los encargos narrativos «La que no pesa»/«La persiana» conserva
> sus IDs sin reescribirse. **Ejecutada HOY como T1 (Seath).** Regla fijada
> para el proyecto: encargo narrativo = `eK`; sala-dato = `datoN`. Los
> encargos e2–e5 del cap. 6 quedan planificables mañana (con T1 mergeado).

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
