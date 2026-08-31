# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-09-01)

Zona prioritaria: **el PRIMER CRUCE de capítulo en juego real: el flujo de ENCARGO del cap. 2** — hoy entraron PR #13 (flujo listar→abrir→generar→jugar→cerrar + post-mortem conectado + cap. 2 en generator), #14 (`ps`/`env` + `story.ch3.*` a datos) y #15 (logro «Cero rastro» recalibrado + eco unlock en bus); main queda a **421 passed / 0 xfailed**
- Primero (Oscar, ojos de experiencia): desde SAVE LIMPIO completa el cap. 0 y al terminar CRUZA: `listar_encargos` del cap. 2 → abrir `story.ch2.e1` → juega la golden (`grep 11:04 centralita/turnos/turno.log | wc -l` → `2`) → cierra y LEE tu post-mortem adjunto. Pregunta de experiencia: ¿el paso de «trabajo en frío» a «Facturas» se siente como el MISMO oficio con más herramientas? ¿El rechazo accionable (te dice qué conceptos te faltan) se entiende sin documentación? Verifica también el logro recalibrado: tu canónica (ruido 6) NO debe ganar «Cero rastro»; una sesión min-honesto (ls→cat→cp, ruido 5) SIN errores SÍ.
- Segunda (Havel, ojos de novedad): lo nuevo del sandbox del cap. 3: `ps`/`ps aux` (¿la columna USER ceniza-521 vs censo-522 se lee como PISTA, no como dato?) y `env` ordenado; fuerza un rechazo de `ps` en cap. 0/2 (exit 127, regresión); confirma que el evento `progression.unlocked` llega a un suscriptor de prueba al dominar `c.cp` (payload completo) y que re-evaluar NO re-emite.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **421 passed / 0 xfailed sí o sí** (385 + deltas 13/18/5). Gate de datos: 16 conceptos / 16 quests (ch3 e1–e5 tints blue/grey/red/red/grey; `c.env` requiere `c.ps`). Roundtrip: save v1 viejo (sin `mastered`) carga con `{}` y no explota. `generate(seed,0)` byte-idéntica (regresión de `model.py`).

Contexto: PR #13 es la puerta del cap. 2 jugable end-to-end (session.py, `prereqs_met` al ABRIR, post-mortem adjunto al cierre en completado y expulsión, seed de sala determinista quest+run); PR #14 trae la familia Procesos con la columna USER que delata y el cap. 3 de Manus a currículo; PR #15 cierra 🧭11 (umbral 4→5 + «sin exit≠0», decisión validada por Gwyn en DESIGN §7.6) y pone el tubo del eco 🧭9 (evento en bus, el render futuro solo se suscribe). Decisiones de diseño firmadas esta noche: sudo GANADO (credencial narrativa) y red simulada (hosts como FS simultáneos) — ambas en DESIGN §6.1, ninguna con código aún.
