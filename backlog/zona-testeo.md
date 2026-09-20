# 🔬 Zona de testeo — 20/09 (definida por Gwyn el 19/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge: suite **769 passed / 0
> failed**, gate **24 conceptos / 31 quests**, bundle **49 ficheros
> (453.9 KiB)** regenerado canónicamente (guardián verde).

## Prioridad 1 — LA PUERTA NOVA: `story.ch5.e1/e3/e4` con allowlist per-encargo (NUEVO, PRs #66/#67; engine PENDIENTE)

- **Dónde:** la Subestación ya tiene FÍSICA y LENTE para sus 4 encargos, pero
  O1 (engine) NO aterrizó: `abrir_encargo('story.ch5.e1/.e3/.e4')` sigue
  `abrible False` (guard honesto). Solo `e2` abre por la puerta normal.
  Lo nuevo jugable hoy: allowlists `DEFAULT_CH5E1` (ls,ps,chmod,kill) /
  `DEFAULT_CH5E3` (ps,env,kill) / `DEFAULT_CH5E4` (chmod,chown,tail,ls) —
  si tu turno de harness las induce directo (Shell/`_commands_for`), prueba
  las fronteras: fuera de su encargo el verbo → exit 127 honesto; base
  `(cat,scp)` de e2 INTACTA.
- **Qué verificar:** (a) `DEFAULT_CH5E1/E3/E4` activas SOLO en su encargo,
  forma `<=` (nunca exactamente); (b) `chmod 600`/`chmod +x`/`chown
  gris:apagados` GNU-honesto (ruido 1, mtime); (c) golden e3:
  `kill -HUP 522` → HUP_522=1 y `kill -9 522` → el `intruso
  --vigilar-censo START 03:14` DESAPARECE del ps — el intruso es un
  objetivo jugable, no decorado; (d) `ls`/`tail`/`env` fuera de su
  encargo → 127.
- **Por qué importa:** hoy S1 dejó allowlists huérfanas (sin puerta que
  abra e1/e3/e4). Cuando O1 aterrije (mañana, P1), esta física se vuelve
  jugable de golpe — hay que saber de ANTEMANO que funciona.
- Pregunta de sabor: ¿matar al intruso con `kill -9` se siente como
  decisión del jugador o como trámite de tutorial?

## Prioridad 2 — LENTE CUSTODIA web: tercera lente de la trilogía TR-003 (NUEVO, PR #67)

- **Dónde:** `web/app.js` + `web/index.html`: `parseParams` acepta
  `?chapter=5` ([0,2,3,4,5,6]); panel «Subestación — custodia» rinde
  `volcado-custodia.csv` SOLO si el testigo existe (`_isCustodiaPresent`,
  file TR-003 como verdad; falso positivo caducado cazado).
- **Qué verificar:** (a) `?chapter=5` consola limpia, panel custodia
  visible con testigo rescatado / vacío con ausencia elocuente (no consola
  roja); (b) `?chapter=3` no-regresión (parseParams superset); (c)
  `restartSameSeed` limpia las 3 lentes (Faro, Troncal, Custodia); (d)
  `TRONCAL_STATIC` 3 ocurrencias intacta.
- **Por qué importa:** tercera lente de la trilogía (Faro `join` →
  Subestación `cat` → post-mortem «el testigo viajó»); si el panel
  enumera en vez de dejar que el jugador lea, muerde el tono del Auditor.
- Pregunta de sabor: ¿la lente custodia acompaña o ya es un spoiler que
  lee el FS por el jugador?

## Smoke del conjunto (post prioridades)

- `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **769
  passed** (760+9+0, deltas declarados verificados); gate 24/31; bundle 49
  ficheros 453.9 KiB fresco (guardián verde); `grep -v` sigue honesto
  (exit 2, 🧭27 P3 recámara); tooltips N/30 + toggle EN_COLA + lente Faro
  byte-idénticos (🧭34/37/38 CERRADOS).
- **Recuerda a Oscar:** `ps aux` vía `abrir_encargo` en ch5 sigue → 127
  (solo `cat` está en `DEFAULT_CH5_COMMANDS`); el intruso se verifica vía
  Shell directo. Sin cambio hoy.
