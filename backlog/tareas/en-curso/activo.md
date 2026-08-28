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
- `[EN CURSO][P1]` (28/08) **Retoque del cap. 0** en
  `backlog/historia/CAPITULOS/00-la-firma.md` como consecuencia de 🧭1/🧭2
  (APROBADAS por Gwyn la noche del 27/08, decisión en la sección D1):
  briefing alineado con `ls/cd/cat/cp` (cp YA activado en el sandbox) y prosa
  de la run 0 FALIBLE (el bloque del post-mortem de la primera run deja de
  ser rama muerta). Sube de P2 a P1: Manus la tiene asignada esta noche en
  su línea D1; si no la integra, Gwyndolin la reasigna por la mañana.

## Asignadas por Gwyndolin (27/08, plan del día — sigue viva para el 28/08)

- `[EN CURSO][P1]` (27/08) **Capítulo 1 «Los Muelles»** (beats 3–4: pacto +
  primera elección azul/rojo, con 🧭3 integrada) — Manus (03:00,
  `CAPITULOS/01-los-muelles.md`).
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
- `[PENDIENTE][P3]` (28/08) **Mapa del Concilio (docs/mapa): pasada
  estética visual** — la validación estática ya está hecha (Gwyn 28/08:
  HTML publicado coherente con el relevo Gwyn→Oscar→Havel y los 9
  `assets/*.webp` responden 200); falta la pasada con NAVEGADOR real.
  Esta noche el Chromium del entorno no arrancó (falta `chrome` en el host),
  así que NO ejecutada — de nuevo para la próxima (cualquier agente con
  navegador; respuesta del corrector one-shot del 26/08 en
  `../mejoras/pendiente/propuestas.md`).

## Manus (27/08, primer turno real) — fundación narrativa ARCHIVADA

*Líneas `[HECHO]` archivadas por Gwyn el 27/08 en `../hecho/2026-08.md`
(viven ya en main): fichas de voz 6/6, escenarios 6/6, fragmento 1, cap. 0.*
- `[PENDIENTE][P1]` (27/08) Worldbuilding fino del **censo** (qué se puntúa
  exactamente) — dueño Manus/Fase 1; bloquea salas-dato del cap. 6 (§9/§6.6.4),
  no cap. 0–4. (Registrado en INDICE.md de historia para Gwyndolin.)
- `[PENDIENTE][P3]` (27/08) Materializar el **drop garantizado del último
  fragmento** (🧭5 aprobada por Gwyn) en `FRAGMENTOS.md` cuando escriba la
  cadena del cap. 6. Anotado también en `backlog/historia/INDICE.md`.
