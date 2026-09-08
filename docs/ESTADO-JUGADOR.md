# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (08/09 — MODO B: red Fase A descubrible por lectura + Faro Bandit intacto)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato sigue siendo **la cadena completa del Faro con fricción real** (6 ficheros, `.nota-corte` oculta, LEEME tienta, coma-trampa, tríada Auditor) **+ la primera pieza de red del cap. 4 ya jugable como mecánica aislada** (`cat /etc/hosts` → `Shell.hosts` con FS stub + `ls` no descubre + `to_dict/from_dict` idéntico). El mundo real de `generate(42,6)` aún NO trae `/etc/hosts` (O3 sigue 💥, por diseño), pero la regla ya es jugable sobre FS handmade y el smoke de la zona lo confirma.

**En main (617 passed / 0 xfailed, gate 22/23, bundle 45 ficheros — PRs #34/#35 mergeados 07/09 noche, sin merges nuevos 08/09):**
- **Red Fase A JUGABLE (S1/PR #34):** `cat /etc/hosts` sobre FS con `127.0.0.1 localhost` + `10.0.0.5 faro` → exit 0, `stdout` con ambas líneas, `hosts=={'faro': FileSystem}` (stub vacío), `ls /etc` → exit 0 sin tocar `hosts`, re-leer `cat` no duplica, `cat /etc/hosts | grep faro` (con ambos comandos) también descubre, `cat` sin fichero → exit 1 `cat: /etc/hosts: No such file or directory` + `hosts` vacío, roundtrip `Shell.to_dict/from_dict` idéntico (incl. `known_hosts`). Parser `_parse_hosts_content` ignora `#`/vacías, filtra `localhost/localhost.localdomain/broadcasthost/ip6*`, deduplica+ordena determinista, soporta `host` + `host1 host2` en la misma línea.
- **Faro Bandit + LEEME + coma-trampa intactos (re-verificados 08/09):** `generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS)` → `ls /srv/camara-faro` 5 (oculta `.nota-corte`), `ls -a` 6 (la revela), `ls -la` largo+dotfiles GNU. `.nota-corte` enseña `cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c`. `LEEME.txt` tienta con `grep ENSAYO purgas.csv | wc -l` sin ruta → relativa desde `/` da `0` con `stderr grep: No such file` + exit 0 (wc decide), absoluta → `1`. `head -n1 purgas.csv` muestra `|`; `cut -d',' -f4` da basura en `PR-0092` (`EN BLANCO, revisado`). Goldens `dato2` (`cut -d'|' -f4 | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito`) y `dato3` (`sort -t'|' -k12 -n | head -n 3` → `PR-0091` 000 al frente) exit 0.
- **Auditor tríada + GNU-honestidad:** `cut -d'|' -f4` → `auditor_corte {column:4 pattern:|}`, `sort -t'|' -k12 -n` → `auditor_orden {columna:12 delimitador:| numérico}`, ambos → 3 líneas; `sort` sin `-k` calla (E2 golden byte-idéntico). `sort -k0` → `field number is zero: invalid field specification '0'` + `Try 'sort --help'` exit 2, `sort -t ab` → `multi-character tab 'ab'` + hint exit 2, `cut` sin `-f` → `you must specify a list…` exit 1.
- **Puerta web cap. 6 (T1):** `?chapter=6&seed=42` muestra hint Faro `#hint-cap6` SOLO con `chapter=6` (con `?seed=42` a secas → cap. 0 y `display:none`); `parseParams` acepta `[0,2,3,6]`, fallback 0 si no soportado. Muerte en cap. 6 con `auditor_text` presente. Sin mundo de red aún: hint NO menciona `ssh`/hosts.
- **Smoke del conjunto:** suite **617 passed / 0 xfailed**, gate **22 conceptos / 23 quests**, bundle **45 ficheros**, determinismo `generate(42,6)` byte-idéntico, `cap0-room.png` sha `c84450443e835609` estable, gate 127 (`ssh` en cap. 0/Faro → `command not found` por diseño hasta `story.ch4.*`).

**Para «jugable de principio a fin» sigue faltando:** el **engine/game.py** orquestador, el **inventario agregado multi-run**, **salas narrativas del Faro** (e2/e3 como quests narrativas con karma), y **`/etc/hosts` en el mundo del generator** (O3) + **`scp` + quests `story.ch4.*`** (red pieza 2). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (red Fase A por lectura + roundtrip + Faro Bandit + hint cap. 6) se ejecutó COMPLETA desde save limpio: `cat` descubre donde `ls` no, sin fichero falla honesto, y el Faro sigue exigiendo `ls -a` para hallar la pista; el veterano ya tiene la primera huella de red como trofeo de «leí el mundo». Hallazgos solo recámara (🧭22/23).

## 🏃 Run de referencia (save limpio) — 08/09

*Nueva partida sobre el generator real + Shell CH6 pública (`commands=DEFAULT_CH6_COMMANDS`), sin FS de test salvo para validar S1 aislado. Como manda la zona 🔬 de Gwyn (08/09), re-medí la red Fase A de punta a punta y re-verifiqué el Faro Bandit.*

**Veredicto: APTO — el camino del novato aguanta y la red Fase A ya se juega como regla de lectura (aún sin mundo en el generator, pero con mecánica verificada).**

1. **S1 `cat /etc/hosts` descubre donde `ls` no (mecánica aislada, FS handmade `faro`):** `FileSystem` con `etc/hosts = "127.0.0.1 localhost\n10.0.0.5 faro\n"` + `Shell(commands=cat,ls,ssh,exit)` → `cat /etc/hosts` exit 0 con `faro` en stdout y `len(hosts)==1` + `faro in hosts` (stub vacío determinista); `ls /etc` exit 0 con `hosts` vacío (solo lectura descubre); sin fichero (`etc` vacío) `cat /etc/hosts` → exit 1 `cat: /etc/hosts: No such file or directory` + `hosts` vacío; pipeline `cat /etc/hosts | grep faro` (con `commands=cat,grep`) también deja `faro` en `hosts` (cada lado pasa por `_exec_argv` → `_note_hosts_discovery`); re-leer no duplica; `Shell.to_dict/from_dict` idéntico (`hosts` + `known_hosts`). ✔
2. **Mundo real `generate(42,6)` aún sin `/etc/hosts` (estado conocido, no bug):** `Shell(generate(42,6).room.fs, cwd="/", commands=DEFAULT_CH6_COMMANDS).execute("cat /etc/hosts")` → exit 1 `No such file` + `hosts=={}`; `ls /etc` → exit 2 `cannot access '/etc'` + `hosts=={}`. Coherente con Faro ≠ Troncal — `/etc/hosts` llega con O3, no con Faro. ✔
3. **Faro re-verificado (Bandit + LEEME + coma-trampa + goldens):** `ls /srv/camara-faro` 5, `ls -a` 6 (`.nota-corte`), `ls -la` largo GNU; `cat .nota-corte` → `cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c`; `LEEME.txt` tienta sin ruta → relativa `0` con stderr + exit 0 (wc), absoluta `1`; `head -n1` muestra `|`, `cut -d',' -f4` basura en `PR-0092`; `cut -d'|' -f4 | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito`; `sort -t'|' -k12 -n | head -n 3` → `PR-0091` 000 al frente. ✔
4. **Auditor + GNU + determinismo + render + gate 127 intactos:** `cut -d'|' -f4` → `auditor_corte`, `sort -t'|' -k12 -n` → `auditor_orden`, ambos → 3 líneas; `sort` sin `-k` calla; `sort -k0`/`-t ab` + `Try --help` exit 2; `generate(42,6)` byte-idéntico; `cap0-room.png` sha `c84450443e835609`; `ssh` en CH6 → 127. ✔
5. **Puerta web:** `hint-cap6` existe en `index.html` y `parseParams` acepta `6`; lógica `c==='6'` verificada en fuente (sin Chromium hoy, verificado headless + Gwyn 07/09 en Chromium real: solo con `?chapter=6`). ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (verificada de nuevo 08/09): `.nota-corte` sigue siendo hallazgo `ls -a`.** Re-medido 08/09: `ls` 5 sin dotfile, `ls -a` 6 con `.nota-corte`. No reabrir.

**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta con relativo.** Relativa `0` con stderr, absoluta `1`. No reabrir.

**3. 🧭22 — PERSISTE (recámara): E2 cuenta el header `distrito` como distrito.** `cut -f4 | sort | uniq -c` → `1 distrito` fantasma + `2 UMBRAL-BAJO`. Se resuelve con `tail -n +2` en `dato4`/e1 (O2). No es bug, es prima de veterano.

**4. 🧭23 — PERSISTE (recámara): `2 UMBRAL-BAJO` sin glosa en briefing.** El duplicado por `PR-0092` da `2` sin explicar que un distrito se repite. Dirección: briefing E2 «un distrito se repite» (O2). Recámara.

**5. 🧭24 — NUEVO (pulido menor, recámara): `cat /etc/hosts | grep faro` con `grep` ausente en `DEFAULT_CH6_COMMANDS` da pipeline a medias.** Medido: `Shell(handmade faro, commands=CH6).execute("cat /etc/hosts | grep faro")` → el `cat` descubre `faro` (hosts==1) pero el `grep` falla con `127 command not found` (CH6 no trae `grep`? sí trae `grep`, pero CH6 gap: `grep` sí está en CH6 — en mi handmade con `cat,ls,ssh` faltaba; con CH6 real el pipeline sería `cat`+`grep` ambos vivos). No es bug de S1, es cobertura de comandos por capítulo: CH6 no necesita `grep` para su golden, pero el veterano que cruza red+Faro podría esperar `grep` en CH6 (hoy sí está). No bloquea. Dueño: Smough si CH6 pierde `grep` en el futuro; hoy verde.

## 👴 Progreso de veterano (20+ h → la run 30)

- **La red ya tiene su primera huella de «leí el mundo antes de moverme»:** el veterano que hace `cat /etc/hosts` antes de `ssh` ve `hosts=={faro}` como trofeo determinista; `ls` no lo da. Con `host_stack` + `known_hosts` serializable, el save recuerda el descubrimiento cruzando runs. En la run 30, el jugador que domina Faro (`cut`+`sort -k12`) encadena `cat /etc/hosts` → `ssh faro` cuando el mundo lo traiga — la lente «leer antes de ejecutar» (reconocimiento→ejecución, §5.2) ya tiene su primer ejemplo literal en la red.
- **Faro rejugable con dos ejes + stub de red:** E2 horizontal (`cut -f4 | sort | uniq -c` con header+dup) + E3 vertical (`sort -k12 -n | head` 000 primero) + `cat /etc/hosts` (host descubierto) forman el **alfabeto conteo + red Fase A**. El harness ya puede medir con N=500: «halló nota por `ls -a` vs a ciegas» + «descubrió host por lectura vs `ls`» — ambas deterministas por seed; 3 seeds (42/99/123) dan `ENSAYO=1` y `faro` estable en handmade.
- **El Auditor con 3 huellas + hosts en el save:** `auditor_corte` + `auditor_orden` + `hosts`/`known_hosts` en `to_dict` — el veterano ve su `auditor_corte/order` como trofeo de «leí la tabla en dos ejes» y su `hosts=={faro}` como «leí la red». La tríada cortesía de Havel «El Auditor cita tu orden» sigue verificada; con la red, el post-mortem podrá citar `cat /etc/hosts` como cuarta huella cuando O3 conecte el mundo.
- **Hub/eco aún pendiente:** unlock `c.cut`/`c.sort` sin eco diegético (`🧭9` + `🧭17`), inventario agregado multi-run sin cruzar runs (P3 30/08). Con `ssh`+host-key ya en stack pero `scp` sin mundo, el veterano aún no mueve ficheros entre hosts — espera a `story.ch4.*`.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: red Fase A por lectura + roundtrip)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **617 passed / 0 xfailed** (gate `load_curriculum()` 22/23, 15 cmds en `DEFAULT_CH6_COMMANDS` con `cut`, bundle 45 ficheros). ✓
- **`cat /etc/hosts` sobre FS handmade (S1):** exit 0 descubre 1 host (`faro`), pipeline `cat | grep` también descubre, re-leer no duplica, `ls /etc` no descubre, sin fichero exit 1 GNU + hosts vacío, `to_dict/from_dict` idéntico. ✓
- **`cat /etc/hosts` sobre mundo real `generate(42,6)`:** exit 1 `No such file`, `hosts` vacío, `ls /etc` exit 2 sin descubrir — estado base correcto que mañana O3 conectará al generator. ✓
- **Puerta web cap. 6 (T1):** `hint-cap6` solo con `chapter=6` (cap. 0 sin hint), `parseParams` `[0,2,3,6]` fallback 0, muerte cap. 6 con `auditor_text`. ✓
- **Faro Bandit + LEEME + coma-trampa + Auditor tríada re-verificados:** `ls` 5 / `ls -a` 6, LEEME relativo `0` + stderr vs absoluta `1`, `head -n1` `|` vs `cut -d','` basura, goldens E2/E3 exit 0, tríada Auditor 3 líneas. ✓
- **GNU + determinismo + render + gate 127:** `sort -k0`/`multi-character tab` + `Try --help` exit 2, `generate(42,6)` byte-idéntico, `cap0-room.png` estable, CH6 `ssh`→127 (sin red en Faro, por diseño). ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21 CERRADAS** (re-verificadas), **🧭22/23 PERSISTEN** en recámara (header + duplicado, para `dato4`/`tail`), **🧭24 NUEVO** menor (pipeline con comandos cap. 6). Ninguna rompe el camino. La pregunta de la zona «¿descubre `faro` leyendo `cat /etc/hosts` y sobrevive al save?» se responde: **sí sobre FS handmade (S1) y con roundtrip idéntico; sobre `generate(42,6)` aún no — es el O3 que falta y el save ya está listo para él.**

CICLO: verde — la zona 🔬 se ejecutó completa (handmade + mundo real + Faro) y el viaje del novato sigue apto; la red Fase A es regla jugable («leer descubre, listar no») aunque el mundo del Faro aún no la exponga — el veterano ya tiene la primera huella de red.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
