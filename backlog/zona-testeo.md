# 🔬 ZONA DE TESTEO — la decide Gwyn al cierre (23:00)

> Protocolo: `docs/TESTEO-DIARIO.md` §4. **El relevo de la zona es
> Gwyn → Oscar → Havel**: Oscar (05:00) la recorre COMPLETA desde save limpio
> (¿el viaje del jugador aguanta?); Havel (07:00) se centra en lo nuevo + smoke
> del conjunto (¿lo añadido funciona y mola?). No es duplicación: cada uno
> responde SU pregunta sobre la misma zona.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-09-07)

Zona prioritaria: **el Faro con su fricción Bandit RESTAURADA y el Auditor que
ya cita tu ORDEN — `ls` vuelve a esconder los dotfiles (S2), el LEEME tienta de
verdad y `purgas.csv` esconde la trampa del delimitador (O2)** — main a
**607 passed / 0 xfailed**, gate de datos **22 conceptos / 23 quests**
(`story.ch6.dato2/dato3`, `e2/e3` fuera), bundle **45 ficheros** (PRs
#31/#32/#33 mergeados esta noche; deltas +0/+16/+1)

- Primero (Oscar, ojos de experiencia, TODO headless, desde save limpio): **el
  arco de descubrimiento de E2 RE-MEDIDO con `ls` GNU real** — anoche el
  novato tropezaba con `.nota-corte` SIN buscar (🧭20); HOY `ls` plano la
  OCULTA (5 ficheros) y solo `ls -a` la revela (6). Pregunta de diseño #1:
  ¿AHORA sí es hallazgo? Cuánto sufre el novato sin la nota (¿la encuentra por
  el briefing, por probatura, o se queda sin respuesta? — eso calibra si falta
  una pista más barata). Segundo: **el LEEME ahora TIENTA** (O2) — lees
  `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta…`; si sigues el atajo
  desde `/` → `0` con stderr + exit 0 (la mentira honesta); ¿el texto invita a
  caer y el caer ENSEÑA (vs. el LEEME mudo de ayer)? Tercero: **la trampa del
  delimitador** — `head -n1 purgas.csv` y luego `cut -d',' -f4`: la fila
  `PR-0092|…|EN BLANCO, revisado|…` (coma interna) devuelve basura; ¿el
  jugador lee el delimitador en la cabecera o lo adivina mal primero?
  Cuarto: goldens E2 (`cut -d'|' -f4 … | sort | uniq -c`) y E3
  (`sort -t'|' -k12 -n … | head -n 3`, PR-0091 al frente) siguen exit 0 y la
  4.ª fila NO rompe ninguno. Pregunta de cierre: ¿el viaje del novato (E1→E2→E3)
  sigue en 30-40 min con la fricción restaurada, o la `.nota-corte` escondida
  lo rompe?
- Segunda (Havel, ojos de novedad): **el Auditor que cita tu ORDEN (O1)** —
  run CON `cut -d'|' -f4 … | sort -t'|' -k12 -n` en history → el informe cita
  AMBAS huellas (`corte registrado` + `orden registrado — columna 12 (|),
  numérico`, 3 líneas); la MISMA run con `sort` SIN `-k` → informe
  byte-idéntico (el `sort` plano del golden E2 no dispara NADA). Cruzar con la
  tríada de ayer: ¿el Auditor ya se siente un interrogatorio con memoria de
  proceso COMPLETA (leer→cortar→ordenar)? **Nota del sistema:** `ssh` (S1) aún
  NO está cableado al mundo (sin hosts en el generator — llegan con las quests
  `story.ch4.*`); NO abráis [BUG] por `ssh: command not found` en cap. 0/6, es
  el gate 127 intacto por diseño de hoy. Su verificación vive en la suite
  (`test_ssh.py`, 9 tests, FS handmade). La Tabla del Faro web ya la verificó
  Gwyn en Chromium (panel solo tras `cut`, columna `distrito` destacada) — no
  duplicar.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` →
  **607 passed / 0 xfailed sí o sí** (590 base +0 #31 +16 #32 +1 #33). Gate de
  datos: `load_curriculum()` → **22/23** (22 conceptos / 23 quests;
  `dato2/dato3` presentes, `e2/e3` SOLO en asserts negativos del guard
  `test_namespace_ch6_dato_vs_encargo`). Regresiones: bundle **45 ficheros**
  (`test_bundle_fresco.py` verde fresco; S1 añadió `red.py`), canónico E1
  `grep ENSAYO /srv/…/purgas.csv | wc -l` → 1 y cebo relativo → 0+stderr+exit 0,
  `generate(42,0)` fs.to_dict byte-idéntico, gate 127 en cap. 0/2 (`sudo`/`ps`/
  `kill`/`cut`/`ssh` → command not found), cap. 0 sin sudo → post-mortem de
  1 línea byte-idéntico, render `cap0-room.png` sha `c84450443e835609` estable.

Contexto: esta noche la red pieza 1 (`ssh`+host-key) entró como MECÁNICA sin
mundo (correcto: gate 127 intacto, quests ch4 mañana); el Faro recibió su
pulido de sabor (`ls -a` Bandit, LEEME tienta, coma trampa) y el Auditor
cerró la tríada lector→corte→orden. La deuda de namespace e2/e3 está
RESUELTA (rename mergeado, guard puesto) — los encargos narrativos e2–e5 del
cap. 6 ya se pueden planificar sin colisión. Deuda viva señalada: los +4
tests de `auditor_orden` (O1 entró con delta +0) — higiene, no bug.
