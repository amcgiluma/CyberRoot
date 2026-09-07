# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (07/09 — MODO B: Faro con fricción Bandit RESTAURADA — `ls` oculta, LEEME tienta, coma trampa y Auditor tríada completa)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya es **la cadena completa del Faro con fricción real**: generar la sala-dato (`generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS)` 15 cmds), descubrir la nota escondida con `ls -a`, caer en el atajo del LEEME y aprender de su `0` mentiroso, y leer la Lista como tabla cortando (`cut`) y ordenando (`sort -k`). El cap. 3 sigue siendo circuito completo de verbo: leer → elevar → facturar → citar.

**En main (607 passed / 0 xfailed, gate 22/23, bundle 45 ficheros — PRs #31/#32/#33 mergeados 06/09 noche):**
- **Faro JUGABLE con Bandit restaurado + LEEME tienta + trampa delimitador:** `ls /srv/camara-faro` → 5 ficheros (oculta `.nota-corte`), `ls -a` → 6 (la revela), `ls -la` → largo + dotfiles con perms/size/mtime GNU. `.nota-corte` enseña `cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c` con ruta absoluta. `LEEME.txt` = `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` — invita a relativa; desde `/` → `0` con `stderr grep: purgas.csv: No such file` + exit 0 (mentira honesta), con absoluta → `1`. `head -n1 purgas.csv` muestra `|` como delimitador; `cut -d',' -f4` devuelve basura (fila `PR-0092` con `EN BLANCO, revisado`) — el delimitador se lee, no se adivina.
- **Sala-dato 6 ficheros, 4 filas de purga:** `registro.csv`, `purgas.csv` (header + `PR-0144|UMBRAL-BAJO|CONTINUIDAD`, `PR-0151|MUEL-01|REASIGNACION`, `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C`, `PR-0092|UMBRAL-BAJO|EN BLANCO, revisado|500`), `censo-borrador.csv`, `aviso-faro.txt`, `LEEME.txt`, `.nota-corte`. E2 golden `cut -d'|' -f4 purgas.csv | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito` (header contado, duplicado UMBRAL-BAJO por PR-0092); E3 golden `sort -t'|' -k12 -n purgas.csv | head -n 3` → `PR-0091` (000) al frente, `PR-0092` (500), `PR-0144` (438) — el 000 sigue primero pese a la 4ª fila.
- **Auditor tríada completa (leer→cortar→ordenar):** `cut -d'|' -f4` → `auditor_corte {column:4, pattern:|}` + `auditor_corte_text`; `sort -t'|' -k12 -n` → `auditor_orden {columna:12, delimitador:|, numerico:numérico}` + `auditor_orden_text`; ambos en history → 3 líneas (`pico` + `corte` + `orden`). `sort` sin `-k` calla (E2 golden `sort` plano intacto, informe byte-idéntico). Nunca expone datos del censo.
- **GNU-honestidad:** `sort -k0` → `field number is zero: invalid field specification '0'` exit 2, `sort -t ab` → `multi-character tab 'ab'` exit 2, con `Try 'sort --help'` según handler; `cut` sin `-f` → `you must specify a list…` exit 1. `head -n1`/`tail` presentes en CH6.
- **Red cap. 4 pieza 1 sin mundo:** `ssh` + host-key + stack existen en `src/core/sandbox/commands/red.py` y Shell, pero `DEFAULT_CH6_COMMANDS` no lo expone — gate 127 intacto (`ssh: command not found` en Faro/cap.0). `known_hosts` serializable, fingerprint `SHA256:` determinista, `yes` cachea. Sin hosts en generator (llegan con `story.ch4.*`).
- **Cap. 3 circuito sudo + lazy 521/522:** `generate(42,3)` con credencial + par demonio; `sudo` sin leer → exit 1 ruido 0 nombrando orden, sin firma; tras `cat` → `read_marks` + `sudo` eleva/firma; `kill -9 522` borra, `kill -HUP 521` → `--reloaded`.
- **Render + puerta web:** `python -m render.demo` → `cap0-room.png` sha `c84450443e835609` estable; `?chapter=6&seed=42` jugable por URL; Tabla del Faro solo tras `cut -d'|' -f4` (columna `distrito` destacada), verificada por Gwyn en Chromium.

**Para «jugable de principio a fin» sigue faltando:** el **engine/game.py** orquestador que encadene capítulos consecutivos (se ejercita vía `generate`+`Shell`), el **inventario agregado multi-run** (qué dominas cruzando runs — 🧭9), y **salas narrativas del Faro** (e2 «La que no pesa» / e3 «La persiana» ya desbloqueadas por rename `dato2/dato3`, pero aún no integradas como quests narrativas con karma). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (Faro Bandit restaurado + LEEME tienta + coma trampa + Auditor tríada) se ejecutó COMPLETA desde save limpio y el camino aguanta: el hallazgo exige `ls -a`, el atajo miente y enseña, la 4ª fila no rompe goldens, y el Auditor distingue `sort` de `sort -k12`. Hallazgos son pulido de didáctica, no roturas.

## 🏃 Run de referencia (save limpio) — 07/09

*Nueva partida sobre el generator real + Shell CH6 pública (`commands=DEFAULT_CH6_COMMANDS`), sin FS de test, sin atajos. Como manda la zona 🔬 de Gwyn (07/09), re-medí el arco de descubrimiento del Faro con la fricción RESTAURADA.*

**Veredicto: APTO — el Faro ya se juega con fricción Bandit real y el Auditor ya tiene memoria COMPLETA (leer→cortar→ordenar).**

1. **La sala nace en `/` y expone 5/6 según `ls`:** `ls /srv/camara-faro` → 5 (`LEEME.txt`, `aviso-faro.txt`, `censo-borrador.csv`, `purgas.csv`, `registro.csv`); `ls -a` → 6 (añade `.nota-corte`); `ls -la` → 6 en largo con perms `rwx`, size, owner/group, mtime. `ls -l` sin `-a` sigue ocultando dotfiles (GNU). La nota ya no se regala — es hallazgo. ✔
2. **E2 «El corte de la Lista» — ahora SÍ es hallazgo Bandit:** `cat /srv/camara-faro/.nota-corte` → `# corta la columna: cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c` + `# la Lista es tabla, no texto — sin corte no se responde`. `cut -d'|' -f4 purgas.csv | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito` (4 líneas, header + duplicado UMBRAL-BAJO por PR-0092). `grep ENSAYO|wc -l` → `1` no responde «qué distritos» — **sin `cut` la pregunta se queda sin respuesta**. El novato que hace `ls` plano NO ve la pista; necesita `ls -a` o probatura. ✔
3. **LEEME tienta y el 0 miente honesto:** `cat LEEME.txt` → `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` `grep ENSAYO purgas.csv | wc -l` desde `/` → `0` con `stderr grep: purgas.csv: No such file or directory` + exit 0 del wc (la mentira honesta); con absoluta `/srv/camara-faro/purgas.csv` → `1`. El texto invita a caer y el caer enseña sin cartel. ✔
4. **Trampa del delimitador — se lee en `head -n1`:** `head -n1 purgas.csv` → `purga_id|fecha|sujeto|distrito|…|archivo_referencia` (`|` visible); `cut -d',' -f4 purgas.csv` → `purga_id|fecha|…` intacto para filas sin coma, pero `PR-0092|…|EN BLANCO, revisado|…` devuelve basura (` revisado|500|…` cortado por la coma interna). El jugador que adivina `,` ve caos; el que lee `|` acierta. ✔
5. **E3 «Los más cerca del cero» — vertical que solo `sort -k12 -n` responde:** `sort -t'|' -k12 -n purgas.csv | head -n 3` → `PR-0091|EN BLANCO|000|--|ENSAYO` al frente, `PR-0092|…|500`, `PR-0144|…|438` (PR-0091 sigue primero pese a la 4ª fila). `cat purgas.csv | head -n 3` muestra crudo con 0091 tercera — **sin `-k12 -n` el 000 no sale primero**. ✔
6. **Auditor tríada completa:** `Shell(fs, cwd="/", commands=CH6).execute("cut -d'|' -f4 … | sort | uniq -c")` + `build_postmortem` → 2 líneas (`pico` + `corte registrado — columna 4 (|)`); `sort -t'|' -k12 -n …` solo → 2 líneas (`pico` + `orden registrado — columna 12 (|), numérico`); ambos en history → 3 líneas (`pico` + `corte` + `orden`). `sort` sin `-k` (E2 golden `sort | uniq -c`) → solo `corte`, sin `orden` (correcto, byte-idéntico al informe sin ordenar). Determinista, sin imports sandbox. ✔
7. **Goldens estables con la 4ª fila:** `generate(42,6, contract_id=story.ch6.dato2)` → `cut -d'|' -f4 | sort | uniq -c` exit 0 (con header + duplicado); `generate(42,6, dato3)` → `sort -t'|' -k12 -n | head -n 3` exit 0, PR-0091 al frente. La coma no rompe ninguno. ✔
8. **Tríada lector + gate 127 + determinismo + render intactos:** `sudo` sin leer sigue rechazando nombrando orden con ruido 0; `generate(42,6)` y `generate(42,0)` fs.to_dict byte-idénticos por seed; `cap0-room.png` sha `c84450443e835609` estable; `ssh` en CH6 → exit 127 (gate Faro sin red, correcto). ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA: `.nota-corte` ya es hallazgo escondido (Bandit restaurado).** Medido 07/09: `ls /srv/camara-faro` → 5 sin dotfile, `ls -a` → 6 con `.nota-corte`, `ls -la` → largo+dotfiles. El PR #32 (S2) filtró `.*` sin `-a` y el hallazgo volvió. E2 ya exige `ls -a` o probatura. No reabrir.

**2. 🧭21 — CERRADA: `LEEME.txt` ya tienta con atajo relativo.** Medido: `LEEME.txt` = `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` La invitación explícita produce `0` con stderr + exit 0 desde `/` (wc decide) y `1` con absoluta. El cebo diegético ya se lee como trampa y enseña ruta. No reabrir.

**3. 🧭22 — PERSISTE: E2 cuenta el header `distrito` como distrito (uniq -c con cabecera).** Medido 07/09: `cut -d'|' -f4 purgas.csv | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito` (header contado, ahora con duplicado UMBRAL-BAJO ×2 por PR-0092). GNU-honesto, no bug, pero el veterano en la run 30 nota el fantasma. Dirección ya priorizada por Gwyn en recámara (entra con `dato4`/`tail -n +2`); si E2 enseña `tail -n +2 | cut …` sería prima de veterano natural. No bloquea (quest valida exit 0).

**4. 🧭23 — NUEVO (pulido didáctico menor): E2 ahora enseña duplicado sin avisar — `2 UMBRAL-BAJO` sin pista.** Medido: `uniq -c` con `sort` previo da `2 UMBRAL-BAJO` por la 4ª fila `PR-0092` (mismo distrito que `PR-0144`). El jugador que cuenta ve `2` y no sabe por qué se repite — la fila duplicada no declara que comparte distrito. No es bug (la tabla es honesta, el dup es intencional para probar que `uniq -c` sin `sort` no agruparía), pero el briefing de E2 no menciona que un distrito puede aparecer dos veces. Dirección: briefing de E2 que anticipe «un distrito se repite» o que la golden enseñe `sort | uniq -c` como detector de duplicados (ya lo hace, pero el `2` sin contexto puede parecer error). Dueño: Manus + `chapter6.py` (prosa E2). Recámara, no señal.

## 👴 Progreso de veterano (20+ h → la run 30)

- **El Faro ya es rejugable por SEED con hallazgo + dos lecturas cruzadas:** E2 horizontal (`cut -f4 | sort | uniq -c` → `2 UMBRAL-BAJO` con hallazgo `ls -a`) + E3 vertical (`sort -k12 -n | head` → 000 al frente pese a la 4ª fila) forman el **alfabeto conteo completo CON fricción**. El veterano en la run 30 encadena `ls -a` → `cat .nota-corte` → `cut -f4 | sort | uniq -c` (4 líneas con header+dup) → `sort -k12 -n | head` (000 primero). Con N=500 seeds el harness ya puede medir «halló nota por `ls -a` vs a ciegas» (harness §8.6) — determinismo por seed lo permite; 3 seeds (42/99/123) dan `ENSAYO=1` estable con la anomalía 000 siempre destacada.
- **El Auditor como interrogatorio con memoria de proceso COMPLETA:** con tres huellas (`lectura` + `corte` + `orden`) el post-mortem ya cita **qué leíste, qué columna cortaste y cómo ordenaste** (pattern `|` + `column:4` + `columna 12 numérico`), sin exponer datos. La variante sin `cut`/`sort -k` queda byte-idéntica (1 línea); `cut|sort` plano sin `-k` solo cita `corte`. El veterano que optimiza ve su `auditor_corte`/`auditor_orden` como trofeo de «leí la tabla en dos ejes» (idea P3 Havel «El Auditor cita tu orden» materializada y verificada).
- **El cebo de ruta + trampa de delimitador como lecciones de 10 segundos:** el veterano reconoce `0` con stderr como «estoy en `/`» y `cut -d','` basura como «leí mal el delimitador» — dos mentiras honestas que enseñan más que un cartel. `head -n1` ya es verbo de diagnóstico (CH6 lo incluye).
- **El hub/eco sigue pendiente:** el unlock `c.cut`/`c.sort` existe en datos pero sin eco diegético visible (mi 🧭9 del 30/08 + 🧭17 de Havel). El veterano que domina `cut` no ve cambiar stock de Gris ni Hub — es la llave del Espejo de Gris (§4.3) y del HOSP-47-C cruzado por `env`. La deuda `inventario agregado multi-run` sigue viva (P3 30/08): cada run parte de `GameState` fresco, no hay «ya dominas cut» cruzando runs. Con la red pieza 1 sin mundo, el veterano aún no puede usar `ssh`/`scp` en mundo (gate 127) — la rejugabilidad de red espera a `story.ch4.*`.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: Faro con fricción Bandit restaurada + Auditor tríada)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **607 passed / 0 xfailed** (590 base +0 #31 +16 #32 +1 #33). Gate datos **22/23** (22 conceptos / 23 quests, `dato2` `c.cut+c.uniq+c.sort`, `dato3` `c.cut+c.sort+c.head`). Bundle 45 ficheros (330.8 KiB). ✓
- **Arco de descubrimiento re-medido con `ls` GNU real:** `ls` → 5 oculta `.nota-corte`, `ls -a` → 6 la revela, `ls -la` → largo+dotfiles — fricción Bandit restaurada (🧭20 cerrada). Sin la nota, E2 requiere `cut` a ciegas; con la nota, el novato ve la columna exacta. Calibración: el novato sufre ~1-2 comandos extra (`ls -a` + `cat .nota-corte`) antes de acertar, no se queda sin respuesta — pista Bandit suficiente, no necesita pista más barata. ✓
- **LEEME que tienta + trampa delimitador:** `LEEME.txt` invita a relativa; relativa desde `/` → `0` con `stderr grep: purgas.csv: No such file` + exit 0 (wc decide), absoluta → `1`; `head -n1` muestra `|` y `cut -d',' -f4` da basura en `PR-0092` (coma interna) — jugador lee cabecera o adivina mal primero. ✓
- **Goldens E2/E3 con 4ª fila:** `cut -d'|' -f4 | sort | uniq -c` → exit 0 (`2 UMBRAL-BAJO` por duplicado), `sort -t'|' -k12 -n | head -n 3` → PR-0091 al frente — la 4ª fila no rompe. ✓
- **Auditor tríada (leer→cortar→ordenar):** `cut -d'|' -f4` → `auditor_corte` cita columna 4 (|), `sort -t'|' -k12 -n` → `auditor_orden` cita columna 12 (|) numérico, ambos → 3 líneas; `sort` sin `-k` no dispara orden (E2 golden intacto, byte-idéntico). ✓
- **GNU + determinismo + render + gate 127:** `sort -k0`/`multi-character tab` → exit 2, `generate(42,6)` byte-idéntico, `cap0-room.png` sha `c84450443e835609` estable, cap0 `ssh` → 127 (gate Faro sin red, por diseño). ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21 CERRADAS** (Bandit restaurado + LEEME tienta verificados en vivo); **🧭22 PERSISTE** en recámara (header contado, ahora con dup `2 UMBRAL-BAJO`); **🧭23 NUEVA** (dup sin contexto, pulido menor). Ninguna rompe el camino. La pregunta de Gwyn «¿el viaje 30-40 min aguanta con la fricción restaurada?» se responde: **sí — la fricción restaurada añade 1-2 pasos de descubrimiento, no bloquea**; el novato con `ls -a` encuentra la nota en <2 min extra, sin ella aún puede adivinar `cut -d'|'` por `head -n1`.

CICLO: verde — la zona 🔬 se ejecutó completa sobre el generator real y el viaje del novato ya exige `ls -a` para hallar la pista, lee el LEEME y cae/ aprende, distingue `|` de `,` y corta/ordena con goldens estables; el veterano lee la Lista en dos ejes y el Auditor lo cita todo; los hallazgos son pulido de prosa, ninguno bloquea la run.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
