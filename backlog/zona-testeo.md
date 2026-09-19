# 🔬 Zona de testeo — 19/09 (definida por Gwyn el 18/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge: suite **760 passed**,
> gate **24 conceptos / 31 quests**, bundle **48 ficheros (445.4 KiB)**
> regenerado canónicamente (guardián verde).

## Prioridad 1 — LA PUERTA: cap. 5 «Subestación» jugable por `abrir_encargo` (NUEVO, PR #64+PR #65)

- **Dónde:** POR FIN por la puerta normal (ya no solo por generator+Shell directo):
  `abrir_encargo(c, 'story.ch5.e2', ['c.cat','c.scp'], volcado_rescatado=True/False)`
  con `SUPPORTED_CHAPTERS {0,2,4,5}` y `_commands_for(5)=(cat,scp)`. El kwarg
  `volcado_rescatado` propaga la geografía condicional del cap. 4 (rescate
  `scp`→ rescatado / `rm` o 30 ticks → caducado) al FS del asalto: el testigo
  `/tmp/volcado-custodia.csv` (`TR-003|faro|troncal-01|512|EN_COLA`) EXISTE solo
  si rescataste; si caducaste, `cat` → exit 1 `No such file` (trayectoria
  válida, el briefing lo dice como pista) y el proceso `intruso
  --vigilar-censo` (USER censo, `START 03:14`) patrulla igual en ambos mundos.
- **Qué verificar:** (a) `story.ch5.e2` abrible por session en AMBAS variantes
  con determinismo ×2 seeds byte-idéntico (`fork("ps-subestacion")` estable);
  (b) `story.ch5.e1`/`.e3`/`.e4` → abrible False (solo e2 hoy, guard honesto);
  (c) helper `volcado_del_save(pm)` lee el post-mortem del Hub: True con
  `{'volcado':'rescatado'}`, False con save vacío/caducado; (d) cambiar of
  chapter 4 e3 (scp rescate → custodia presente; rm → ausente) y comprobar
  que la decisión del e3 viaja por el flujo nativo, no solo por Shell directo;
  (e) `DEFAULT_CH4*` INTACTA (13 base / 14 e3) — la allowlist nova NO sangra;
  (f) no-regresión: goldens `generate(42,0/2/3/4/6)` byte-idénticos
  (incl. dato7 con ambas variantes de `volcado_rescatado`).
- **Por qué importa:** hasta hoy la cadena troncal→Faro→Subestación era
  jugable por atajos de harness; si `abrir_encargo` la sabe servir,
  el jugador real la vive sin atajos.
- Pregunta de sabor: ¿la puerta normal sostiene el peso diegético del
  capítulo oscuro o el bypass técnico de ayer (MODO B) era la única forma
  de hacerlo respirar?

## Prioridad 2 — LA CUARTA HUELLA: `postmortem.auditor.custodia` (NUEVO, PR #65)

- **Dónde:** completa el encargo e2 con `cat /tmp/volcado-custodia.csv`
  (exit 0) → `build_postmortem` → `auditor_custodia` con
  «Expediente 000: custodia leída en casa: el testigo viajó. Continuidad del
  ensayo: estable.». Si caducaste (sin fichero / exit 1), la huella NO
  aparece (byte-idéntico al post-mortem sin custodia — detector por exit 0,
  no por presencia del fichero).
- **Qué verificar:** (a) la cuarta huella es INDEPENDIENTE: coexiste con
  `postmortem.volcado.rescate` y con el espejo (3 firmas vivas en un
  solo informe — grep 'custodia' en el dict del build);
  (b) prefijo `postmortem.auditor.custodia` NO colisiona con
  `postmortem.espejo.*` ni `postmortem.volcado.*` (disyunción por prefijo
  ya verificada por Smough, re-verificar con juego real);
  (c) el texto «el testigo viajó» se siente como cierre de la trilogía
  TR-003 (Faro `join` → Subestación `cat` → post-mortem «viajó») o como
  repetición (¿el Auditor ENUMERA o ya LISTA?).
- **Por qué importa:** es la primera vez que el Auditor VERIFICA un dato
  del FS del jugador (no solo lo que ejecutaste); si suena a entusiasmo
  técnico más que a expediente, muerde el tono.
- Pregunta de sabor: ¿«el testigo viajó» cierra el arco o lo adelgaza?

## Smoke del conjunto (post prioridades)

- `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **760 passed**
  (gate 24/31, bundle 48 ficheros 445.4 KiB fresco, guardián verde);
  `grep -v` sigue honesto (exit 2 filtro positivo, 🧭27 P3 recámara);
  toggle badge + tooltip N/30 + lente Faro byte-idénticos (🧭34/37/38 CERRADOS).
