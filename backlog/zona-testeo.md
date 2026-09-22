# 🔬 Zona de testeo — 23/09 (definida por Gwyn el 22/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge 22/09: suite **801 passed /
> 0 failed** (788+7+6+0, deltas verificados), gate **25 conceptos / 31
> quests** intacto, bundle **50 ficheros (473.3 KiB)** regen canónico.
> PRs #72/#73/#74 MERGEADOS. BUG 🧭27 CERRADO.

## Prioridad 1 — EL DÍPTICO COMPLETO: `chmod 600/777` junto a `kill HUP/-9` (NUEVO, PR #72)

- **Dónde:** `abrir_encargo(c,'story.ch5.e1',{'c.ls-la','c.cat','c.chmod'},42)`
  abre E1 «La puerta que dejaste» — la Subestación ya tiene 2/4 encargos
  con karma por la puerta normal.
- **Qué verificar:**
  (a) `ls -l` → `-rw-r--r--` en `/srv/subestacion/sesiones/pts0`; sin
  `ls -l` antes → sin huella (byte-idéntico).
  (b) `chmod 600` tras `ls -l` → post-mortem `auditor_cierre` azul +
  `micro_karma {blue:1}` + `ls -l` muestra `-rw-------`.
  (c) Run limpia aparte: `chmod 777` (y `-R 777`) → `auditor_puerta_abierta`
  rojo `{red:1}`.
  (d) E1 sin chmod y runs sin `kill` → sin falsear huellas cruzadas
  (chmod no dispara kill-detectores, kill no dispara chmod).
- **Por qué importa:** mismo verbo, dos karmas — la tesis §3.1 del díptico
  queda cerrada solo si el jugador PERCIBE la diferencia moral sin
  spoiler de la lente. Pregunta de sabor: ¿obstaculizar la sesión pesa
  distinto que dejarla abierta al leer el expediente?

## Prioridad 2 — `grep -v`/`-i` HONESTO: el filtro que faltaba (NUEVO, PR #73)

- **Dónde:** `grep` con flags en cualquier sala con `purgas.csv` o con
  `ps aux` en allowlist (E3 permite `ps`).
- **Qué verificar:**
  (a) `grep -v sujeto purgas.csv` → exit 0 filtra la línea de cabecera;
  `ps aux | grep -v root` vía pipe → 0.
  (b) `-i`, `-vi`, `--` terminador y flag desconocido → `invalid option`
  exit 2 (GNU-honesto).
  (c) `grep PATRON` SIN flags → salida byte-idéntica a la del cap. 2
  (la frontera del cap. 2 ES la prueba de respeto).
- **Por qué importa:** cierra el único [BUG] de código vivo (🧭27, 11 días).
  Pregunta de sabor: ¿el filtro negativo se siente herramienta Unix real
  o un atajo de guion?

## Smoke sí o sí

- Suite completa `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`
  → **801 passed** (si sale 800+1 `test_bundle_fresco`, es el guardián
  gritando bundle stale: regen canónico `python tools/web/build_bundle.py`,
  NUNCA silenciar el test).
- Determinismo: `generate(42,5,True)` y `generate(99,5,False)` byte-idénticos
  ×2; HUP vs -9 difieren solo en huella (mismo FS, mismo pid por seed).
- Web `?chapter=5` con la lente NUEVA `#custodia-postmortem` (PR #74): el
  veredicto TEXTUAL bajo la insignia, color coherente (verde vivo/azul
  reconfigurado/ámbar silenciado), consola limpia en los 3 estados.
  En capítulos 1-4 la lente no debe ensuciar nada.
- Gate de datos **25/31** y `CUSTODIA/TRONCAL_STATIC` intactas.
