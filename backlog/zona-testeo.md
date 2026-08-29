# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-08-30)

Zona prioritaria: **el CIRCUITO COMPLETO competencia→unlock→save** — generator (curriculum real, opción B) + sandbox (REPL, GNU honesto) + progression (primer unlock) conviven en main tras los 3 merges de hoy (342 passed, PRs #7/#8/#9)
- Primero (Oscar, ojos de experiencia): recorre el camino del cap. 0 DESDE SAVE LIMPIO con el árbol nuevo — misma secuencia canónica del dossier (ls→cat→cp→verificación) sobre la sala que produce `generate(seed, 0)`, y comprueba que el viaje sigue siendo POR NECESIDAD (4 comandos + curiosidad, cumbre `cp` alcanzable) con cwd naciendo en `/`. En la cumbre: completar el contrato debe dejar `c.cp` dominado en el save — verifica roundtrip (load lo recupera) y que el unlock NO se dispara sin la evidencia (§4.2: competencia, no grind).
- Segunda (Havel, ojos de novedad): el unlock es lo nuevo jugable — completa el contrato y JUEGA con él: ¿qué se siente que el save «recuerde» tu competencia? Prueba el post-mortem mental del Auditor sobre la sesión (¿qué habría dicho de tu ruido?). Y los errores GNU nuevos como sabor: `cat fichero/` (*Is a directory*) y `cp dir` (*omitting directory*, culpando al origen) — ¿enseñan, o solo estorban? Los errores honestos son método, no castigo (§2.6.8).
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **342 passed + 1 xfail sí o sí** (316 + deltas 9/7/10; el xfail 🧭8 es intencional: decisión (b) firmada esta noche en DESIGN §6.1, se materializa mañana). Guard de layout vivo (cero `src/assets/tests/`).

Contexto: hoy entraron PR #7 (generator consume `curriculum.json` + harness v0 en `tools/harness/`), #8 (pasada GNU cp/cat + REPL `python -m core.sandbox`) y #9 (fachadas core.state/core.sandbox + progression v0 con `c.cp` como primer unlock). Errores GNU cerrados en negativo: los 2 [BUG][P3] de Havel del 28/08.
