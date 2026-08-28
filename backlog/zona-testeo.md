# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-08-29)

Zona prioritaria: el CÓDIGO como sistema — curriculum + generator + state conviven por primera vez en main (PRs #4/#5/#6, suite 316)
- Primero (Oscar, ojos de experiencia): recorre el CAMINO del cap. 0 con las piezas ya integradas — la sesión canónica (`PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/sandbox/test_session_cap0.py -o addopts= -v`) sigue siendo el mapa; verifica que lo que generator produce (`generate(seed, 0)` → sala → `Shell` real) respeta el VIAJE del dossier: 4 comandos POR NECESIDAD, cumbre `cp` alcanzable, errores honestos. La decisión 🧭2 (opción B: cwd en `/`, dossier con rutas completas — DESIGN §6.1) debe cortar el tropiezo de ayer (el «no puedo copiar con el nombre del dossier» ya no puede pasar con rutas completas).
- Segunda (Havel, ojos de novedad): juega el CONTRATO de datos nuevo — `load_curriculum()` sobre `src/data/curriculum.json`: ¿los prereqs de `story.ch1.e1` cuentan la misma historia que el cap. 1 de Manus (permisos como «quién puede tocar esto»)? ¿el validador rechaza lo que debe rechazar? Y sabor: el mensaje didáctico de `&&`/`;` (PR #5) — ¿enseña o da la lata?
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **316 passed sí o sí** (225 + 30 engine + 51 sandbox/curriculum + 10 state); el guard `test_tests_layout.py` debe seguir vivo (cero `src/assets/tests/`).

Contexto: hoy entraron PR #4 (generator v0 + guard de layout), #5 (curriculum.json v0 + canje Event + rechazo didáctico `&&`/`;`) y #6 (state v0: primer save atómico/versionado + SEMANTIC a un idioma). Decisión 🧭2: opción B (DESIGN §6.1).
