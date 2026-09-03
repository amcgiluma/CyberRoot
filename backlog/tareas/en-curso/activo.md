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
- `[EN CURSO][P2]` (03/09) **O1 — Demonio del cap. 3 en el mundo real (🧭16)** — Ornstein (`feat/engine-2026-09-03`) [HECHO] (PR #23): inyectar `ceniza:521`/`censo:522` en `chapter3.py` de forma lazy (quest de procesos/sudo), misma física que el golden de `test_session_kill.py`. Criterios en `backlog/planes/2026/09/03.md` (O1).
- `[EN CURSO][P2]` (03/09) **S1 — Gate de lectura del sudo (🧭14b, decisión Gwyn)** — Smough (`feat/sandbox-2026-09-03`): [HECHO] (PR #22) `sudo` exige haber LEÍDO `orden-ceniza.txt` (marca de sesión persistida en `state/`); rechazo diegético que nombra la orden, ruido 0. Criterios en `backlog/planes/2026/09/03.md` (S1).
- `[EN CURSO][P1]` (03/09) **T1 — DEPLOY web (Vercel) del estado jugable** — Seath (`feat/meta-ui-2026-09-03`): empaquetado web desde el render v0 existente (ideal repl cap. 0, mínimo demo render) y URL pública para Juanma. Criterios en `backlog/planes/2026/09/03.md` (T1).
- `[EN CURSO][P3]` (03/09) **T2 — Briefing legible de `story.ch6.e1` (🧭15)** — Seath (`feat/meta-ui-2026-09-03`): textos de `title_key`/`beat_key` con voz de Ceniza/Manus + rutas absolutas `/srv/camara-faro/` en el briefing. Solo `src/data/`. Criterios en `backlog/planes/2026/09/03.md` (T2).

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
