# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-09-03)

Zona prioritaria: **el cap. 6 «Faro» JUGABLE de verdad (quest `story.ch6.e1` + sala-dato de la Lista) y el cap. 3 real sobre el generator** — main a **515 passed / 0 xfailed**, gate de datos **21/21** tras mergear esta noche #16 (sala sudo + fix), #19 (chapter6 + voz), #20 (kill + DEFAULT_CH6) y #21 (render v0)
- Primero (Oscar, ojos de experiencia): el cap. 6 desde save limpio — `generate(<seed>, 6)` + Shell con `DEFAULT_CH6_COMMANDS`, `cd /srv/camara-faro` (la sala nace en `/` y ahí el cebo miente por ruta: nota abajo), listar los 4 ficheros, y jugar la historia de la Lista: `grep PR-0091 purgas.csv` → `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` (el sujeto 000 y la purga de nadie, cruzando con la pulsera HOSP-47-C del fragmento 2); canónico `grep ENSAYO purgas.csv | wc -l` → **1**; y el CEBO: `grep 000 censo-borrador.csv | wc -l` → **0 con exit 0** — ¿se siente como trampa descubrible o como ruido? Y como veterano: ¿la familia conteo ya se siente ALFABETO (leer Vesper) o sigue siendo demo técnica? Además, deuda de ayer: la sala del cap. 3 ahora SÍ es generable desde main (`generate(seed, 3)`) — re-jugar el circuito sudo COMPLETO sobre el generator real (credencial en `/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt`, `sudo` sin leer → rechazo, leer → eleva/factura/firma; decisión 🧭14(b) de esta noche la cambiará mañana, mide el estado ACTUAL como línea base).
- Segunda (Havel, ojos de novedad): lo nuevo por capas — (1) **kill/señales**: `kill -9 522` mata (desaparece de `ps aux`), `kill -HUP 521` → `--reloaded` + `HUP_521=1` en env, golden GNU `kill: (522) - No such process`, y en cap. 0/2 sigue el gate 127; (2) **voz del post-mortem**: `build_postmortem` del cierre de cap. 0/2 devuelve texto resuelto («Expediente 000…»), nunca `line_key` crudo ni crash; (3) **render v0**: `python -m render.demo` → `cap0-room.png` con sha estable `c84450443e835609`, prompt `cero@…:/$` con cwd real.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **515 passed / 0 xfailed sí o sí** (466 + 12 de #16 + 6 netos de #19 + 19 de #20 + 12 de #21, con la división de test del fix = +1). Gate de datos: `load_curriculum()` → **21 conceptos / 21 quests** (ch6.e1 presente). Regresiones: `generate(seed,0)` byte-idéntica, línea golden del cap. 2 (`grep 11:04 centralita/turnos/turno.log | wc -l` → 2 con `cd` previo), roundtrip de save sin `mastered` no explota.

Contexto: esta noche el cap. 6 pasó de isla a CAMINO (sala-dato + quest + comandos, costura O3↔S2 verificada por literales Y por sesión real de Gwyn), kill entró como física con evento para karma futuro, la voz del Auditor es audible desde el REPL y el juego tiene su primer píxel (render v0, PNG real). La zona es enorme pero es UNA zona: la primera cadena narrativa completa (encontrar la purga que no debió existir) jugable de principio a fin. La decisión 🧭14(b) (sudo se gana LEYENDO la llave) entra como tarea de Smough el 03/09 — no la testeéis hoy, mañana cambia.
