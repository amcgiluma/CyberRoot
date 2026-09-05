# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-09-06)

Zona prioritaria: **el cap. 6 «Faro» cerrado como alfabeto: la Lista se CORTA (E2) y se ORDENA (E3), con boon de hallazgo, cebo de ruta y un Auditor que CITA tu corte en el post-mortem** — main a **590 passed / 0 xfailed**, gate de datos **22 conceptos / 23 quests** (+2: e2/e3), bundle **44 ficheros** (PRs #28/#29/#30 mergeados esta noche; deltas +6/+8/+8)

- Primero (Oscar, ojos de experiencia, TODO headless, desde save limpio): **el arco de descubrimiento de E2/E3 en `generate(<seed>, 6)` + Shell(DEFAULT_CH6_COMMANDS)** — entras al Faro, `ls /srv/camara-faro` → 6 ficheros, `cat LEEME.txt` te invita a relativa (si caes: `grep ENSAYO purgas.csv | wc -l` desde `/` → `0` con stderr del grep y exit 0 del wc — la mentira honesta), `cat .nota-corte` → el operador muerto te enseña `cut -d'|' -f4 | sort | uniq -c`; la PREGUNTA de E2 («¿qué distritos hay y cuántos vecinos?») SOLO se responde cortando (golden exit 0) y la de E3 («¿quién está más cerca del 0?») SOLO con `sort -t'|' -k12 -n … | head -n 3` (3 líneas, PR-0091 al frente). Pregunta de diseño: ¿el novato encuentra la nota SIN cartel (hallazgo, no tutorial)? ¿Tras E2/E3 la Lista se siente TABLA y no muro de texto?
- Segunda (Havel, ojos de novedad): **el post-mortem que CITA tu corte (O1, PR #28)** — una run CON `cut -d'|' -f4 …` en history → el informe añade `Expediente 000: corte registrado — columna 4 (|)…` (nunca clave cruda); la MISMA run SIN `cut` → informe byte-idéntico a lo de ayer (sin línea de corte). Cruzar con la tríada lector (sudo sin leer / cat orden → sudo / cap. 0 sin sudo 1 línea): ¿el Auditor ya se siente un interrogatorio con memoria de proceso? Detalle GNU de S1 (PR #29): `sort -k0` → `field number is zero`, `-t` multi-char → error con `Try 'sort --help'`, líneas sin columna → fallback vacío sin crash.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **590 passed / 0 xfailed sí o sí** (567 base +6 #28 +8 #29 +8 #30, con el skip honesto de E3 ya convertido en pass tras S1). Gate de datos: `load_curriculum()` → **22/23** (22 conceptos / 23 quests, e2 requiere `c.cut+c.uniq+c.sort`, e3 `c.cut+c.sort+c.head`). Regresiones: bundle 44 ficheros (`test_bundle_fresco.py` verde fresco / rojo ante mutación), canónico E1 `grep ENSAYO /srv/…/purgas.csv | wc -l` → 1 y cebo de borrador → 0, `generate(42,0)` fs.to_dict byte-idéntico, gate 127 en cap. 0/2 (`sudo`/`ps`/`kill`/`cut` → command not found), cap. 0 sin sudo → post-mortem de 1 línea byte-idéntico, render `cap0-room.png` sha `c84450443e835609` estable.

Contexto: esta noche el Faro cerró su alfabeto conteo — `cut` (ayer) + `sort -k` (hoy) + las dos quests que los exigen por necesidad, con la `.nota-corte` como boon Bandit y el `LEEME.txt` como cebo de ruta. El Auditor aprendió a citar TU columna (`postmortem.auditor.corte`), hermano del `lectura`/`ciega` de ayer. NOTA del guardián: la `.nota-corte` es hallazgo escondido — si el novato no la encuentra, E2 se queda sin respuesta; medid CUÁNTO se sufre sin la nota (eso calibra si mañana hace falta una pista más barata). No abrir `[BUG]` por la deuda de namespace e2/e3 (decisiones de prosa en `activo.md`, no afecta al juego de hoy).
