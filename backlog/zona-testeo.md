# 🔬 Zona de testeo — 27/09 (definida por Gwyn el 26/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge 26/09: suite **852 passed /
> 0 failed** (837 +4 scaffold +5 gate +6 resolutor, exacto a la predicción de
> Artorias), gate **25 conceptos / 32 quests** (nueva quest e4), bundle
> **50 ficheros (494.8 KiB)** regen canónico. PRs #84/#85/#86 MERGEADOS.
> NADA retenido.

## Prioridad 1 — Faro E4 «El trato»: primer encargo jugable del cap. 6 (NUEVO, PRs #84+#85)

- **Dónde:** `abrir_encargo(c,'story.ch6.e4',{'c.cat','c.grep','c.ls','c.join'},42)` (+ seed 99).
- **Qué verificar:**
  (a) `abrible True` con requires `['c.join']` — cero conceptos nuevos, todo
  transitivo desde dato4/dato5; sin `c.join` → `missing ['c.join']` honesto.
  (b) `generate(..., contract_id='story.ch6.e4')` planta `/tmp/prueba-custodia/`
  con los DOS testigos: `prueba-cruce.txt` (golden `PR-0091|EN BLANCO|…|HOSP-47-C`)
  y `prueba-reloj.txt` (`START 11:04`); `cat` exit 0 sobre ambos.
  (c) Determinismo: generate ×2 byte-idéntico (seed 42 y 99).
  (d) Con sede en e4: SOLO `cat/grep/ls` — pedir `join`/nuevo verbo → 127
  honesto (frontera allowlist CH6 16 verbos, nadie tocó `DEFAULT_*_COMMANDS`).
  (e) Textos del Auditor: briefing con `/tmp/prueba-custodia/` + 11:04 +
  `persona` HOME en hint_2, voz formulario «tengo las dos pruebas — cruzo y
  camino al reloj»; hints NO spoilean el golden.
  (f) Pregunta de sabor (OSCAR): ¿la sala del trato se SIENTE como
  confrontación con Vela o como recibo de trámite? ¿El jugador entiende que
  sus prueba/reloj de dato4/dato5 SON la palanca?
- **Por qué importa:** cierra el arco del Faro con palanca legal — el
  novato repite `join` y `ps aux | grep` que ya domina (Vela con lo que sabes).

## Prioridad 2 — Web `?seed=` compartible + título dinámico (NUEVO, PR #86)

- **Dónde:** web `?chapter=4&seed=1` y `?chapter=4&seed=42` (orden en barra URL).
- **Qué verificar:**
  (a) `document.title` = `CyberRoot — cap. 4 — seed 1` / `— seed 42` (em dash
  U+2014) en los 4 callsites: init, boot con params, restartSameSeed, fallback.
  (b) Cambiar seed en la URL regenera un mundo distinto visible: seed 1 ch4 =
  3 hosts vs seed 42 = 2 hosts, sin cachear FS viejo.
  (c) `restartSameSeed` sigue limpiando `out` y re-inicia; título se mantiene.
  (d) Sin params → título sin seed (fallback no ensucia).
  (e) El 6º estado `⌕` de la lente intruso (25/09) INTACTO: web puro no lo tocó.
- **Por qué importa:** la URL se vuelve ficha legible/compartible de run —
  recámara honesta sin deuda; primer caso de identidad de run fuera del save.

## Smoke (HAVEL, tras prioridades)

- `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **852
  passed / 0 failed** (851 src+tools +1 guardián bundle; si ve 851+stale
  tras tocar `src/core|data/`, el guardián FUNCIONA: `python
  tools/web/build_bundle.py` → «50 ficheros» → commit; NUNCA silenciar).
- Gate: **25/32** (e4 añadida por Smough; cero conceptos nuevos).
- Bundle: **50 ficheros (494.8 KiB)** fresco post-regen canónico de Gwyn.
- `node --check web/app.js` OK; `TRONCAL_STATIC`/`CUSTODIA_STATIC` intactas.
- El PRECEDENTE que pdueba el tool: `python tools/resolutor_huellas.py --check`
  sobre un fixture — usado 3 veces en los merges de esta noche, 0 avisos.
