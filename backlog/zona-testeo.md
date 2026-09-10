# 🔬 ZONA DE TESTEO — 11/09 (decidida por Gwyn 10/09 23:00)

> Relevo: **Oscar (05:00) la recorre COMPLETA desde save limpio → Havel (07:00)
> se centra en lo nuevo + smoke.** Formato `docs/TESTEO-DIARIO.md` §4.
> Base esperada tras merges del 10/09: suite **680 passed / 0 xfailed**,
> gate **24 conceptos / 27 quests** (`c.join` + `dato4`/`dato5` nuevos),
> bundle **47 ficheros (389.8 KiB)** fresco.

## 1. Lo NUEVO que hay que tocar sí o sí (hoy entró en main)

- **`dato4` «El cruce» (cap. 6)** — primer cruce de tablas con `join`:
  1. `join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv` → exit 0, contiene `PR-0091|EN BLANCO` (el fantasma que el registro esconde). **Medido por Gwyn en `generate(42,6)` real: returncode 0, 1 línea con PR-0091.**
  2. La salida trae TAMBIÉN el header `sujeto` y una 2ª no-pareja (`000483|PR-0092`) — la trampa-delimitador `EN BLANCO, revisado` genera un huérfano real. Probar el pipeline completo `join … | grep -v sujeto` (1 pipe) y constatar en qué queda `PR-0092`: ¿briefing que nombre el filtrado, o fantasma-2 documentado? **Veredicto de sabor, no bug.**
  3. Errores GNU: `join` sin operandos, fichero inexistente, `-t` multi-char. Deben ronronear, no morder.
- **`dato5` «La persiana» (cap. 6)** — `ps aux` como RELOJ forense:
  4. `ps aux` muestra 3 procesos (`init Aug25` + 2 `faro-sync`); el culpable es el que arranca `START 11:04` (día de `PR-0091`); el señuelo tiene START variable.
  5. `ps aux | grep 11:04` → exit 0, **1 línea** con `PR-0091`, sin señuelo. Verifica que `ps` estaba en 127 fuera del cap. 6/3 y que este golden no exige sentir la forcejeo del shell (1 pipe).
  6. Rejuga 2×: determinismo byte-idéntico (3 procesos idénticos por seed).
- **`c.join` (concepto nuevo)** — `load_curriculum()` → 24/27; prereqs `c.cut`+`c.sort`; probar `join` en cap. 0/4 → debe ser 127 (frontera de allowlist, NO bug).

## 2. Smoke del conjunto (mismo pase de siempre)

- `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **680** sí o sí (648+5+20+7). Deltas de los PRs #42 (+5, con el fix de allowlist aplicado por Gwyn en el merge: ahora `{…} <= set(DEFAULT_CH6_COMMANDS)`), #43 (+20), #44 (+7).
- Gate: `load_curriculum()` → **24/27**.
- Bundle: 47 ficheros fresco (guardián verde; si grita `bundle stale`, no lo silencies: `python tools/web/build_bundle.py`).
- Regresión del cap. 4: el día tocó CH6 y curriculum, así que pásale el MUSTERING del cap. 4 (`cat /etc/hosts` descubre, `scp` TR-001, roundtrip) — no lo re-saltes.
- Shell SIN cambios: `tail -n +2 | cut -d'|' -f4 | sort` (2 pipes) exit 0 y `tail|cut|sort|uniq -c` (3 pipes) → `multiple pipelines not supported` exit 2. 🧭25 sigue pernoctando en recámara.

## 3. Preguntón de la noche (diseño, para Oscar y Havel)

- **¿El Faro enseña `join` con necesidad real?** `dato4` funciona sin pipes; ¿se siente como «el verbo que te faltaba» o como un atajo que mata la lección del pipeline? Cuéntale el sabor a Gwyn.
- **¿El commuting de `ps` (quién en cap. 3 → cuándo en cap. 6) dice o chirría?** Juega el viaje cap. 3 → cap. 6 y di si la reutilización del mismo comando cambia de pregunta de forma legible.
- 🧭26 sigue en el semáforo (punto del Faro de `cut` ya no es e1): probad Faro ANTES vs DESPUÉS del troncal moje con `join`/`dato5`, y reportad si `e1` merece exigir `cut` someday (decisión de Gwyn, no cambio hoy).

## 4. Save / smoke para los perezosos

- URL de jugador: `https://cyberroot-psi.vercel.app/?chapter=6&seed=42` — cap. 6 recién servido: `join -t'|' -1 3 -2 1 -v 1 …purgas.csv …registro.csv` en la sala del Faro y `ps aux | grep 11:04` en la persiana.
- CICLO de Gwyn 10/09: **verde** (3/3 PRs mergeados, 0 retenidos, goldens re-verificados en mundo real tras el merge).
