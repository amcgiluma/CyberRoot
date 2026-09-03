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
- `[HECHO]` (03/09) **Manus — coherencia gate sudo LECTURA (🧭14b) + pulido cap. 3** — Manus: alineada prosa de `CAPITULOS/03-bombas.md` con la decisión de Gwyn de exigir LECTURA de `orden-ceniza.txt` antes de `sudo`; E4/E5 explicitan `cat` previo. Sin fichas nuevas. INDICE actualizado.

## Historial reciente (resumen — el detalle vive en `../hecho/2026-08.md`)

- 27/08 → 31/08: fundación narrativa de Manus (fichas, escenarios, caps. 0–4,
  fragmentos 1–4) y PRs #4–#15 mergeados; decisiones 🧭2, 🧭6, 🧭8=(b), 🧭9,
  🧭10 y 🧭11 materializadas en DESIGN y en código. Sin deuda abierta de esos
  días. Ver `hecho/2026-08.md` y `hecho/2026-09.md`.

> **MERGEADAS por Gwyn (02/09, 23:00) — PRs #16, #19, #20 y #21** (detalle en
> `../hecho/2026-09.md`): #16 (sala sudo cap. 3 + fix tests stale) → #19 (chapter6
> + cebo pipe-0 + voz post-mortem) → #20 (kill/señales + quest ch6.e1) → #21
> (render v0). Suite final: **515 passed** (gate de Artorias exacto). Gate de
> datos **21/21**. Costura ch6 O3↔S2 verificada con sesión real (fila
> `PR-0091|EN BLANCO|000|--|ENSAYO` exacta; cebo pipe-0: `grep ENSAYO|wc` → 1 y
> `grep 000` → 0). Conflictos de huellas resueltos por script (HEAD gana
> veredictos; worklog en orden cronológico completo). En GitHub: #16 MERGED,
> #19/#20/#21 CLOSED con motivo (contenido ya en main); sus ramas preservadas.
