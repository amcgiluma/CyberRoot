# 🔬 Zona de testeo — 21/09 (definida por Gwyn el 20/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge: suite **774 passed / 0
> failed**, gate **24 conceptos / 31 quests**, bundle **49 ficheros
> (453.5 KiB)** regenerado canónicamente (guardián verde), PR #68 MERGED.

## Prioridad 1 — LA PUERTA ABRE: campaña COMPLETA del cap. 5 por `abrir_encargo` (NUEVO, PR #68)

- **Dónde:** `session.py` sin guard — hoy `abrir_encargo` abre los 4
  encargos de la Subestación (e1/e2/e3/e4) con requires correctos:
  e1 `c.ls-la/c.cat/c.chmod`, e2 `c.cat/c.scp`, e3 `c.ps/c.env`,
  e4 `c.chmod/c.chown/c.cat/c.grep`. El rechazo honesto de
  `missing [...]` (sin prereqs seleccionados) funciona igual que e2.
- **Qué verificar:** (a) `abrir_encargo(c,'story.ch5.e1/e3/e4',
  <requires del curriculum>, volcado_rescatado=True)` → `abrible True`;
  sin knowledge → rechazo accionable `missing [...]` (NO un crash);
  (b) testigo condicional: `volcado_rescatado=True` → `cat
  /tmp/volcado-custodia.csv` exit 0 con `TR-003`; `False` → `cat` exit 1
  `No such file` (misma semántica en los 4 encargos); (c) pid del intruso
  e3 estabile por seed (426/427 golden vs 522 fallback) y
  determinismo ×2 seeds de `generate(42,5)`/`(99,5)` byte-idéntico;
  (d) e2 intacta (física y allowlist `{'cat','scp'}` sin sangrar).
- **Por qué importa:** la deuda P0 de 2 días se salda esta noche. Si la
  puerta abre violando determinismo o el guard `missing` se rompe, deja
  main roto SIN suite colándose (el test ya lo cubre, pero el jugo hay
  que sentirlo en vivo).
- Pregunta de sabor: ¿al abrir e1/e3/e4 sin guard extra, el capítulo se
  siente ABIERTO (mapa que respira) o DESGUARDado (sin pared que dé
  sentido a las restricciones)?

## Prioridad 2 — SINERGIA puerta+lente: encargos abiertos llena la lente custodia web (NUEVO jugable HOY)

- **Dónde:** con la puerta abierta, `abrir_encargo` + `cat
  volcado-custodia.csv` + post-mortem + `?chapter=5` web ahora forman
  un circuito completo; el panel «Subestación — custodia» en la web
  refleja `TR-003` SOLO si el testigo viajó.
- **Qué verificar:** (a) flujo completo: abrir e2 (o e1/e3/e4 con
  prereqs), rescate caminos, web `?chapter=5` consola limpia con lente
  visible; (b) falso positivo caducado: sin testigo el panel calla
  (`hideCustodiaTabla`, sin consola roja); (c) con e3: intruso `kill
  -HUP`/`kill -9` (pid jugable) + web custodia coexisten sin recursos
  muertos ni huérfanos.
- **Por qué importa:** la tríada física+puerta+lente atravesada
  end-to-end era la deuda del 19/09. Hoy jugable COMPLETO.
- Pregunta de sabor: ¿el circuito trilogía Faro `join` → Subestación
  `cat` → web custodia se siente como un caso cerrado o como el primer
  expediente del jugador?

## Smoke del conjunto (post prioridades)

- `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` →
  **774 passed** (769+5, delta real verificado por Artorias: +5 tests
  en test_session_ch5, off-by-1 honesto del PR); gate 24/31; bundle 49
  ficheros 453.5 KiB fresco (guardián verde); `grep -v` sigue honesto
  (exit 2, 🧭27 P3 recámara); tooltips N/30 + toggle EN_COLA + lente
  Faro/Troncal byte-idénticos (🧭34/37/38 CERRADOS).
- **Recuerda a Oscar:** `ps aux` vía `abrir_encargo` en e3 ya NO
  debería dar 127 — con la puerta abierta, `ps` está en la allowlist
  correcta y el intruso se lee por la puerta normal (artorias 💡:
  verificar). Si sigue 127, abrir [BUG] y documentar.
