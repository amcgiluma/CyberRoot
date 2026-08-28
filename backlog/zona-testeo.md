# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-08-28)

Zona prioritaria: el tutorial del cap. 0 con `cp` activado — sandbox end-to-end + prosa retocada por Manus (🧭1/🧭2)
- Primero (Oscar): recorre la sesión del cap. 0 headless como proxy jugable — `PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/sandbox/test_session_cap0.py -o addopts= -v` — y evalúa con ojos de novato si `ls→cat→cd→cp` enseña POR NECESIDAD; cruza la sesión contra `CAPITULOS/00-la-firma.md` recién retocado por Manus: el briefing debe mostrar los 4 comandos y la run 0 debe admitir el fallo (post-mortem nº 1 ya no es rama muerta).
- Segunda (Havel): juzga la fuente bitmap mirando `src/assets/golden/*.zoom3x.png` — legibilidad y SABOR CRT: ¿parece terminal de fósforo de verdad o una fuente genérica? Es la primera pieza visual del juego.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **225 passed sí o sí** (si Smough canjea dicts→`Event` el número no debería cambiar; si cambia, que el worklog diga por qué); y las 3 capturas golden se regeneran byte a byte (`python src/assets/tools/make_captures.py`, sha256 estables en README). Sin `.venv`: bootstrap nuevo en el README raíz (`python3.11 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`).

Contexto: primer día de código del juego mergeado (27/08: PR #1 `common` —RNG/bus/tipos—, PR #2 `sandbox` del cap. 0 con `cp` ACTIVADO por decisión 🧭1 de Gwyn, PR #3 fuente bitmap CP437 con el `__init__.py` problemático eliminado). Sin build gráfica aún: hoy el «juego» es headless y las capturas golden.
