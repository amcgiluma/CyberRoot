# 🔬 Zona de testeo — 22/09 (definida por Gwyn el 21/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge 21/09: suite **788 passed /
> 0 failed**, gate **25 conceptos / 31 quests** (c.stat), bundle **50
> ficheros (465.8 KiB)** regen canónico. PRs #69/#70/#71 MERGEADOS.

## Prioridad 1 — EL JUICIO DEL VERBO KILL: HUP azul vs -9 rojo como DECISIÓN (NUEVO, PR #69)

- **Dónde:** `abrir_encargo(c,'story.ch5.e3',{'c.ps','c.env'},volcado True)`
  abre E3 con `{cat,env,kill,ps,scp}` — la promesa de `05-subestacion.md`
  por la puerta normal (🧭44 CERRADO).
- **Qué verificar:**
  (a) `ps aux` → exit 0 con `censo <pid> intruso --vigilar-censo` (42→424,
  99→421 ó fallback; el pid lo dicta la seed, NO la memoria — no fijes pid).
  (b) `kill -HUP <pid>` → exit 0; `ps aux` de nuevo → `--reloaded` en el
  intruso; post-mortem → línea «señal de reconfiguración registrada» +
  karma azul.
  (c) Run limpia aparte: `kill -9 <pid>` → intruso desaparece del `ps aux`;
  post-mortem → «proceso de vigilancia eliminado» + karma rojo.
  (d) Run SIN kill → post-mortem SIN huellas nuevas (byte-idéntico).
  (e) e1/e4 sin kill → sin falsa detección de `auditor_hup/kill`.
- **Por qué importa:** es la primera huella kármica azul/rojo con el MISMO
  verbo. Si HUP no pinta azul o -9 no pinta rojo, el test miente. Pregunta
  de sabor: ¿reconfigurar vs eliminar se SIENTE distinto al leer el
  expediente (Expediente 000) o es texto decorado?

## Prioridad 2 — `stat`: OJOS DEL TESTIGO + insignia web de 3 estados (NUEVO, PRs #70/#71)

- **Dónde:** `Shell` con `stat` en sus comandos (no está en las
  allowlists del cap. 5 — fuera de encargo es 127 honesto).
- **Qué verificar:**
  (a) `stat /tmp/volcado-custodia.csv` con rescate → exit 0,
  `Modify: …03:14:00` + `Size: 512`; con `volcado_rescatado=False` →
  exit 1 `cannot stat … No such file`. La hora del testigo ahora se
  pregunta al fichero, no solo al `ps START`.
  (b) Web `?chapter=5`: la insignia `#custodia-intruso` muestra 3 estados —
  VERDE (`intruso --vigilar-censo START 03:14` vivo), AZUL (`--reloaded`
  tras HUP), ÁMBAR (silenciado tras -9). Consola limpia en los 3.
  (c) `c.stat` aparece como hallazgo (prereq `c.ls`) — el concepto se
  enseñó en cap. 1 y hoy tiene uso diegético.
- Pregunta de sabor: ¿la insignia verde/ámbar/azul ANUNCIA o SPOILEA?
  (debe dar estado, no veredicto — el veredicto es del post-mortem).

## Smoke — suite + determinismo

- `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` →
  **788 passed / 0 failed** esperado (gate `load_curriculum()` 25/31,
  `test_bundle_fresco` verde con bundle 50).
- Determinismo: `generate(42,5,True)` byte-idéntico ×2 y
  `generate(99,5,False)` ×2; con kill -HUP vs -9 las historias DIFIEREN
  solo en la huella del post-mortem (mismo FS, mismo pid).
