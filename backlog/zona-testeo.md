# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-09-04)

Zona prioritaria: **el cap. 3 con el sudo GANADO (gate de lectura 🧭14b) y su demonio en el generator (O1), + la puerta web de Juanma (deploy Vercel)** — main a **529 passed / 0 xfailed**, gate de datos **21/21** (PRs #22 sandbox, #23 engine, #24 meta-ui mergeados esta noche; deltas +7/+6/+1)
- Primero (Oscar, ojos de experiencia): el cap. 3 desde save limpio — `generate(<seed>, 3)` + `Shell(DEFAULT_CH3_COMMANDS)`: `sudo …` SIN leer la orden debe rechazar diegético NOMBRANDO `/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt` (exit 1, ruido 0, SIN firma en auth.log); leerla con `cat` (relativa o absoluta) gana la marca y `sudo` eleva/factura (cat 1 + sudo 3) y firma `tick N operator : sudo …`. Pregunta de diseño: ¿el rechazo basta para que el novato ENCUENTRE la orden por su cuenta (la sala nace en `/`)? ¿Leer antes de elevar se siente lección o fricción? Y el demonio: `ps aux` muestra `ceniza 521 --ventana` vs `censo 522 --vigilar-censo`, `kill -9 522` mata (desaparece), `kill -HUP 521` deja `HUP_521=1` en `env` — ¿se INTUYE quién es quién sin que nadie lo explique?
- Segunda (Havel, ojos de novedad): **la puerta web** — https://cyberroot-psi.vercel.app con navegador real (Chromium/playwright-core, como el de `web/verificar_repl.js`): ¿carga, arranca Pyodide, responde el REPL del cap. 0 con el core REAL (`cat …/nombre_de_proveedor.txt` → CANDELAS)? ¿La terminal se siente jugable (teclear, prompt, output) o solo demostrable? Si Vercel fallara: servir local (`python -m http.server 8000 --directory web`) y anotarlo. Y el briefing nuevo del Faro: `resolve('story.ch6.e1.title'/'beat')` → «El número que sobra» con rutas absolutas — ¿la prosa invita a jugar la Lista o suena a instrucciones?
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **529 passed / 0 xfailed sí o sí** (515 + 6 de #23 + 7 de #22 + 1 de #24). Gate de datos: `load_curriculum()` → **21/21**. Regresiones: `generate(42,0)` byte-idéntica, gate 127 en cap. 0/2 (`sudo`/`ps`/`kill` → command not found), canónico del Faro `grep ENSAYO …|wc -l` → 1 y cebo `grep 000 …|wc -l` → 0, línea golden cap. 2, roundtrip de save con `read_marks` nuevo, render sha `c84450443e835609`.

Contexto: esta noche el sudo dejó de ser ambiental — se GANA LEYENDO la orden (rechazo diegético, ruido 0, la marca viaja en el estado) — y el cap. 3 real tiene demonio (par 521/522 inyectado LAZY por la quest). Además el juego tiene URL pública por primera vez (REPL Pyodide del cap. 0, core real verificado por Gwyn con Chromium). El rechazo sin leer y la firma tras leer ya fueron verificados en vivo por Gwyn sobre main (`tick 2 operator : sudo cat /etc/hosts`); lo que falta es la lectura con SILLA DE JUGADOR: ¿el viaje enseña el gesto sin tutorial?
