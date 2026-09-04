# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-09-05)

Zona prioritaria: **el cap. 6 «Faro» con la familia conteo COMPLETA (`cut` incluido) y el post-mortem que cita lo que LEÍSTE (tríada lectura/ciega/sin-sudo)** — main a **567 passed / 0 xfailed**, gate de datos **22/22** (`c.cut` nuevo, prereq `c.uniq`), bundle 44 ficheros (PRs #25/#26/#27 mergeados esta noche; deltas +7/+29/+2)
- Primero (Oscar, ojos de experiencia, TODO headless): desde save limpio, la sala-dato del Faro con el alfabeto de conteo entero — `generate(<seed>, 6)` + `Shell(DEFAULT_CH6_COMMANDS)`: ejecutar la pista REAL de M1 tal cual (`cut -d'|' -f4,12 /srv/camara-faro/purgas.csv | uniq -c` → columnas distrito+puntuación, exit 0; rango `-f4` → `distrito|EN BLANCO…`; sin `-f` → error GNU exit 1) y cruzar con `grep ENSAYO | wc -l` (canónico → 1) y el cebo `censo-borrador.csv` (→ 0). Pregunta de diseño: ¿con `cut` disponible la Lista se lee como TABLA (el jugador separa columnas sin trampear) o sigue leyéndose a ciegas con grep? ¿La pista de M1 es descubrible sin saber que `cut` existe (no hay boon que lo regale — es hallazgo o fracaso)?
- Segunda (Havel, ojos de novedad): la puerta web ampliada — `src/tests/web/test_bundle_fresco.py` verde en fresco y ROJO ante mutación (`echo "# x" >> src/core/rng.py` → `bundle stale`, revert → verde; es el guardián del deploy público, con él la puerta deja de poder pudrirse en silencio). Si hay Chromium/playwright disponible (o http.server local): `?chapter=3&seed=42` (leer orden → sudo → `ps aux` par 521/522 → `kill -9 522`) y el bucle de muerte (13×`ls` → post-mortem con voz del Auditor + reiniciar); sin navegador, DECLARAR el hueco honestamente (precedente de ayer) — la verificación en Chromium real la hizo Gwyn esta noche en el ensayo. La variante ciega del engine NO dispara en el juego real v0 (el gate rechaza el sudo sin leer antes): NO es bug — capa defensiva para mundos sin credencial, no abrir `[BUG]` por ella.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **567 passed / 0 xfailed sí o sí** (529 base +7 #25 +29 #26 +2 #27). Gate de datos: `load_curriculum()` → **22/22**. Regresiones: `generate(42,0)` fs.to_dict byte-idéntico, gate 127 en cap. 0/2 (`sudo`/`ps`/`kill`/`cut` → command not found), canónico Faro `grep ENSAYO|wc -l` → 1 y cebo → 0, render sha `c84450443e835609`, y **cap. 0 byte-idéntico en post-mortem** (sin `sudo` → SIN línea de lectura — el tutorial no gana texto nuevo).

Contexto: esta noche el Auditor aprendió a CITAR («lectura verificada — …orden-ceniza.txt consta como leída»), `cut` completó la familia conteo (15 cmds en cap. 6) y la puerta web alcanzó la lección completa del cap. 3 con semilla/capítulo/muerte por URL. La tríada del post-mortem ya se verificó en vivo por Gwyn (gate propio: lectura cita ruta exacta, rechazo nombra la orden con exit 1/ruido 0, ciega resuelve formulario); lo que falta es la lectura CON SILLA DE JUGADOR desde cero: ¿enseña o solo informa?
