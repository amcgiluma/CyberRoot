# 🔬 Zona de testeo — 24/09 (definida por Gwyn el 23/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge 23/09: suite **809 passed /
> 0 failed** (801+8+0+0, deltas verificados por Artorias + regen canónico),
> gate **25 conceptos / 31 quests** intacto, bundle **50 ficheros
> (484.0 KiB)** fresco. PRs #75/#76/#77 MERGEADOS. NADA retenido.

## Prioridad 1 — EL DÍPTICO DEL PROPIETARIO: `chown gris:apagados` vs `chown root:root` (NUEVO, PR #75)

- **Dónde:** `abrir_encargo(c,'story.ch5.e4',{'c.ls-la','c.cat','c.chmod','c.chown','c.grep'},42)`
  abre E4 «El que se queda» — la Subestación ya es 4/4 con huella moral
  (E1 chmod + E3 kill + E4 chown).
- **Qué verificar:**
  (a) e4 abrible SOLO con knowledge completo que incluya `c.grep` (curriculum
  lo exige — es el encargo que ya pide grep, documentarlo como díptico
  honesto); sin prereqs → rechazo honesto `missing [...]`.
  (b) `ls -l` + `chown gris:apagados pts0` → post-mortem
  `auditor_chown_transfer` azul + `micro_karma {blue:1}`.
  (c) Run limpia aparte: `chown root:root pts0` → `auditor_chown_retoma`
  rojo `{red:1}`.
  (d) Sin `ls -l` antes → sin huella, byte-idéntico.
  (e) Coexistencia último-manda: `chmod 600`+`chown root:root` (y al
  revés) → el ÚLTIMO verbo decide la huella; probar también chown→chmod.
- **Por qué importa:** mismo fichero `pts0 644`, mismo gate `ls -l`,
  verbo distinto — la tesis §3.1 «misma materia, lentes distintas» llega
  al propietario. Pregunta de sabor: ¿entregar la casa a Gris frente a
  devolvérsela al Censo se SIENTE como decisiones distintas, o pesa igual
  que el 600/777 de E1?

## Prioridad 2 — `chmod -R` HONESTO + hint veterano (NUEVOS, PRs #76/#77)

- **Dónde:** `chmod -R` en E1/cap. 1 (fichero) y sobre un directorio;
  hint `story.ch5.e1.hint_2` en la web `?chapter=5`.
- **Qué verificar:**
  (a) `chmod -R 777 pts0` (fichero) → exit 0, modo 777, karma rojo
  IDÉNTICO a `chmod 777` (sin stderr mentiroso).
  (b) `chmod --recursive` y `-Rv` → idénticos.
  (c) `chmod -R 777 <dir>` → recursivo determinista; `chmod 777 <dir>`
  → solo el dir, hijo intacto.
  (d) Sin `-R` → byte-idéntico (cap. 1 y e1 cierran con sus 7 tests).
  (e) Web lente: el hint «-R es para directorios — aquí es un fichero…»
  visible; consola limpia; caps 1-4 sin ensuciar.
- **Por qué importa:** el stderr GNU-mentiroso muere y el veterano de
  Havel (23/09) deja de tropezar con el flag que no hace lo que promete.
  Pregunta de sabor: ¿el hint CORREGIR al veterano se siente maestro
  cálido o manta sobre el puzzle?

## Smoke sí o sí

- Suite completa `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`
  → **809 passed** (si sale 808+1 `test_bundle_fresco`, es el guardián
  gritando bundle stale: regen canónico `python tools/web/build_bundle.py`,
  NUNCA silenciar el test).
- Determinismo: `generate(42,5,True)` y `generate(99,5,False)` byte-idénticos
  ×2; HUP vs -9 y 600 vs 777 siguen pesando distinto sin cruzarse.
- Gate de datos **25/31** y `CUSTODIA/TRONCAL_STATIC` intactas; bundle
  **50 ficheros (484.0 KiB)** fresco.
- E1 (chmod) y E3 (kill) siguen BYTE-IDÉNTICOS a ayer: hoy entró E4 al
  díptico, nadie ha tocado los cierres previos del verbo.
