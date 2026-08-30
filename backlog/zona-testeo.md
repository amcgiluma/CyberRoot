# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-08-31)

Zona prioritaria: **el Auditor que lee tu historial + lo nuevo del cap. 2 en datos** — hoy entraron PR #10 (🧭8=(b) + post-mortem + calibración), #11 (tuberías `grep`/`wc` + `story.ch2.*`) y #12 (save recuerda CUÁNDO dominaste + logros); main queda a **385 passed / 0 xfailed**
- Primero (Oscar, ojos de experiencia): desde SAVE LIMPIO, run canónica del cap. 0 y AL TERMINAR mira tu propia factura con el post-mortem nuevo (`build_postmortem` sobre tu sesión, `src/core/engine/postmortem.py`): ¿la unidad coincide con el budget (tu viaje curioso era 11/12), el comando que delata es el que TÚ sentiste que te delató, y el formulario suena a Auditor seco (ficha de voz §2.4) y no a log técnico? El espejo post-mortem es la pieza §2.4: primer contacto del jugador con «el sistema te estuvo leyendo». Verifica también que tu `mastered` (`c.cp`) conserva el save tras reload y que la sesión nace en `/` (opción B intacta tras tocar `model.py`).
- Segunda (Havel, ojos de novedad): lo nuevo jugable del cap. 2: carga la sesión fixture de `test_session_ch2.py` en el REPL y juega la línea EXACTA del capítulo (`grep 11:04 centralita/turnos/turno.log | wc -l` → `2`); prueba el rechazo de `a | b | c` (mensaje propio) y confirma que `&&` sigue rechazado (exit 2). Luego fuerza el logro «Cero rastro» (ruido ≤ 4) en una sesión mínima y REPORTA la factura mínima alcanzable: si 4 es imposible (el viaje honesto mide 6 fijo), el umbral se recalibra — dato para Gwyn/Oscar, no lo decidas tú.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **385 passed / 0 xfailed sí o sí** (342+1xfail + deltas 13/18/11; el xfail 🧭8 murió hoy). Gate de datos: 14 conceptos / 11 quests (ch2 tints blue/blue/grey/red/grey). Roundtrip de save: un save v1 viejo (sin `mastered`) carga con `{}` y no explota.

Contexto: PR #10 (O1 `Contract.prereqs_met` al ABRIR el encargo — el xfail histórico murió; O2 `build_postmortem(shell_dict, state)` con factura GNU + línea del Auditor como clave+args; O3 calibración: viaje honesto total_noise=6 constante, 0 % supera budget 12), PR #11 (S1 tubería única `cmd1 | cmd2` + `grep`/`wc` GNU honestos, ruido de tubería 2+1=3; S2 `story.ch2.e1–e5` al currículo) y PR #12 (T1 `GameState.mastered` {boon→{tick,order}} + `resumen_competencia` con factura en la unidad del budget; T2 logros «Cero rastro»/«Mano de seda» como datos del save). Decisiones de diseño de esta noche: eco 🧭9 DIEGÉTICO (cap. 1, Gris nombra lo dominado) y operativa de «primer error» (perdón único por partida, solo ruido de riesgo) — ambas en DESIGN §6.1.
