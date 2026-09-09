# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (09/09 — MODO B: red COMPLETA en mundo real + e2 «La que no pesa» con tail)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato es **la cadena completa del Faro con fricción real + la primera pieza de red ya en el mundo** (6 ficheros, `.nota-corte` oculta, LEEME tienta relativo, coma-trampa, tríada Auditor) **+ quest `story.ch6.e2` «La que no pesa» jugable** (`tail -n +2 | cut -d'|' -f4 | sort` sin fantasma `distrito`, 2×UMBRAL-BAJO) **+ red Fase A+B como mundo real** (`cat /etc/hosts` sobre `generate(42,6)` descubre `faro` 10.6.0.5, `ls /etc` no descubre, re-leer no duplica, `GameState` roundtrip idéntico). `scp` sigue 127 en cap. 6 por allowlist (frontera deliberada — llega con `story.ch4.*`), y `ssh` 127 en cap. 0/Faro por diseño.

**En main (635 passed / 0 xfailed, gate 22 conceptos / 24 quests, bundle 45 ficheros — merges #36/#37/#38 del 08/09 + prosa e2 pulida 09/09 03:00):**
- **Red mundo real (O3+S1 merges):** `generate(42,6)` trae `/etc/hosts` (`127.0.0.1 localhost` + `10.6.0.5 faro`) → `cat /etc/hosts` exit 0, stdout con `10.6.0.5 faro`, `Shell.hosts=={'faro': FileSystem stub}`, `ls /etc` → exit 0 sin tocar `hosts`, re-leer `cat` no duplica, `GameState(shell).to_dict/from_dict` idéntico (hosts+known_hosts+host_stack). Parser `_parse_hosts_content` ignora `#`/vacías, filtra `localhost/broadcasthost/ip6*`, deduplica+ordena. `cat` sin fichero → exit 1 GNU + hosts vacío.
- **`scp` Fase B (S1):** `scp` handler vivo (`scp [user@]host:ruta destino` copia entre FS con metadatos owner/mode/mtime, `dir→dentro`, `same_file` y `Is a directory` controlados), host no descubierto → exit 1 ruido 0 `scp: host 'faro' no descubierto — léelo en /etc/hosts` (didáctico, nombra dónde leer), ruta inexistente/destino inválido → GNU `No such file`/`Not a directory` ruido 3. En cap. 6 `scp` da 127 por allowlist (frontera deliberada, no bug — la copy se prueba con shell handmade que incluye `scp` en `available_commands`).
- **Faro Bandit + e2 + coma-trampa intactos (re-verificados 09/09 sobre generator real):** `ls /srv/camara-faro` 5 (oculta `.nota-corte`), `ls -a` 6 (la revela), `ls -la` largo+dotfiles GNU. `.nota-corte` enseña `cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c`. `LEEME.txt` = `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` → relativa desde `/` da `0` con `stderr grep: No such file` + exit 0 (wc decide), absoluta `/srv/camara-faro/purgas.csv` → `1`. `head -n1` muestra `|`; `cut -d',' -f4` da basura en `PR-0092` (`EN BLANCO, revisado`). Goldens: `dato2` (`cut -d'|' -f4 | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito` con header), `dato3` (`sort -t'|' -k12 -n | head -n 3` → `PR-0091` 000 al frente) exit 0, **e2** (`tail -n +2 | cut -d'|' -f4 | sort` → `--/MUEL-01/UMBRAL-BAJO×2` sin `distrito`) exit 0 vía `generate(42,6, contract_id=e2)` + `new_session`.
- **Auditor tríada + GNU-honestidad:** `cut -d'|' -f4` → `auditor_corte`, `sort -t'|' -k12 -n` → `auditor_orden`, ambos → 3 líneas; `sort` sin `-k` calla (E2 golden sin header lo evita). `sort -k0` → `field number is zero` + `Try 'sort --help'` exit 2, `sort -t ab` → `multi-character tab 'ab'` + hint exit 2, `cut` sin `-f` → `you must specify a list` exit 1.
- **Puerta web cap. 6 (T1):** `?chapter=6&seed=42` muestra hint Faro `#hint-cap6` SOLO con `chapter=6` (con `?seed=42` → cap. 0 y `display:none`); `parseParams` acepta `[0,2,3,6]`, fallback 0 si no soportado. Muerte en cap. 6 con `auditor_text` presente. Sin `ssh`/`scp` en hint — no promete lo que el cap. 6 no deja usar aún.

**Para «jugable de principio a fin» sigue faltando:** el **engine/game.py** orquestador, el **inventario agregado multi-run**, **salas narrativas del Faro e3+** y **quests `story.ch4.*` + `chapter4.py` + allowlist `scp` en cap. 4** (red pieza cap. 4 — el suelo ya está, falta la quest). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 se ejecutó COMPLETA desde save limpio: `cat` descubre donde `ls` no sobre mundo real, `scp` 127 en Faro por frontera y copia real con shell scp-capaz, e2 resuelve sin fantasma y con briefing «un distrito se repite», LEEME tienta relativo y .nota-corte oculta; el veterano ya puede encadenar `cat /etc/hosts` → `scp` cuando ch4 llegue.

## 🏃 Run de referencia (save limpio) — 09/09

*Nueva partida sobre el generator real + Shell CH6 pública (`commands=DEFAULT_CH6_COMMANDS`), con check adicional de `GameState` roundtrip y scp handmade. Como manda la zona 🔬 de Gwyn (09/09), medí la red como MUNDO REAL (ya no stub).*

**Veredicto: APTO — el camino del novato aguanta y la red Fase A ya es mundo, no promesa.**

1. **`cat /etc/hosts` descubre donde `ls` no (mundo real `generate(42,6)`):** `Shell(generate(42,6).room.fs, cwd="/", commands=CH6).execute("cat /etc/hosts")` → exit 0 con `10.6.0.5 faro` en stdout y `hosts=={'faro': FileSystem stub}`; `Shell(fs).execute("ls /etc")` → exit 0 `hosts` + `hosts=={}` (solo lectura descubre); sin fichero → exit 1 `No such file` + vacío; re-leer no duplica; `Shell.to_dict/from_dict` y `GameState(shell).to_dict/from_dict` idénticos (hosts+known_hosts+host_stack). ✔
2. **Quest `story.ch6.e2` «La que no pesa» (O2 + prosa Manus 09/09):** `generate(42,6, contract_id="story.ch6.e2")` + `new_session().execute("tail -n +2 /srv/camara-faro/purgas.csv | cut -d'|' -f4 | sort")` → exit 0 `--/MUEL-01/UMBRAL-BAJO×2` sin `distrito` (tail quita header, 2×UMBRAL-BAJO por dup PR-0092); `textos.json` trae `title`/`beat`/`briefing`/`hint_1` con `tail -n +2`, `/srv/camara-faro/purgas.csv`, `un distrito se repite`, `UMBRAL-BAJO`, `PR-0092` `EN BLANCO, revisado`; gate 22/24, e1 intacta, goldens dato2/dato3 exit 0. ✔
3. **Faro re-verificado (Bandit + LEEME + coma-trampa + goldens):** `ls` 5, `ls -a` 6 (`.nota-corte`), `LEEME.txt` tienta relativo `0`+stderr vs absoluta `1`, `head -n1` `|` vs `cut -d','` basura, goldens dato2/dato3/e2 exit 0. `scp` en CH6 → 127 `command not found` (allowlist cap. 6, frontera deliberada), `ssh` 127 igual. ✔
4. **Auditor + GNU + determinismo + render + gate 127 intactos:** `cut -d'|' -f4` → `auditor_corte`, `sort -t'|' -k12 -n` → `auditor_orden`, ambos → 3 líneas; `sort` sin `-k` calla; `sort -k0`/`-t ab` + `Try --help` exit 2; `generate(42,6)` byte-idéntico salvo `/etc/hosts` nuevo; `cap0-room.png` sha `c84450443e835609`; `ssh`/`scp` 127 en CH6. ✔
5. **Puerta web:** `hint-cap6` existe en `index.html` y `parseParams` acepta `6`; lógica `c==='6'` verificada en fuente (sin Chromium hoy, verificado headless + Gwyn 08/09 en Chromium real: solo con `?chapter=6`). Muerte cap. 6 con `auditor_text` presente. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 09/09): `.nota-corte` sigue siendo hallazgo `ls -a`.** `ls` 5 sin dotfile, `ls -a` 6 con `.nota-corte`. No reabrir.

**2. 🧭21 — CERRADA (re-verificada y MEJORADA 09/09): `LEEME.txt` tienta con relativo.** Ahora `LEEME.txt` = `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` → invita explícito a relativa; desde `/` da `0`+stderr (wc decide exit 0) vs absoluta `1`. Ya no es casi-mudo; es cebo didáctico de ruta.

**3. 🧭22 — CERRADA (09/09): E2 contaba header `distrito` como distrito.** Resuelta con `tail -n +2` en e2 (golden `tail -n +2 | cut -d'|' -f4 | sort` → sin `distrito`, 2×UMBRAL-BAJO). No reabrir.

**4. 🧭23 — CERRADA (09/09): `2 UMBRAL-BAJO` sin glosa en briefing.** Resuelta: briefing e2 `un distrito se repite` + `UMBRAL-BAJO` + `PR-0092` presentes en `textos.json`; hint_1 `tail -n +2` sin regalar resultado.

**5. 🧭24 — PERSISTE (recámara, higiene allowlist): `cat /etc/hosts | grep faro` descubre aunque el segundo comando falle por gate.** Medido 08/09: `cat` descubre y `grep` 127 si no está en `commands`, pero host queda. Con CH6 real `grep` sí existe y pipeline `cat|grep` también descubre. No bloquea; es cobertura de allowlist para caps con red. Dueño: Smough si ch4 pierde `grep`; hoy verde.

**6. 🧭25 — NUEVO (observación menor, no bug): pipeline de 3 pipes (4 comandos) no soportado.** `tail -n +2 | cut -d'|' -f4 | sort | uniq -c` (4 comandos, 3 pipes) → `multiple pipelines not supported: chain them one at a time` exit 2. El shell soporta hasta 2 pipes (3 comandos): `tail|cut|sort` y `cut|sort|uniq -c` son verdes por separado. La quest e2 valida con `tail|cut|sort` (sin `uniq -c`) y cuenta `UMBRAL-BAJO` por substring — el jugador que quiera `uniq -c` lo encadena en segundo paso. No rompe E2, pero documenta límite para el diseñador de `dato4`/`ch4` cuando pidan 4 eslabones.

## 👴 Progreso de veterano (20+ h → la run 30)

- **La red ya es mundo y trofeo de «leí antes de moverme»:** el veterano que hace `cat /etc/hosts` sobre `generate(42,6)` ve `hosts=={faro}` como trofeo determinista; `ls` no lo da. Con `host_stack` + `known_hosts` + `GameState` serializable, el save recuerda el descubrimiento cruzando runs. En la run 30, el jugador que domina Faro (`cut`+`sort -k12`+`tail`) ya puede encadenar `cat /etc/hosts` → `scp faro:/srv/camara-faro/purgas.csv /tmp/` cuando ch4 lo habilite — la lente «reconocimiento→ejecución» (§5.2) ya tiene su primer ejemplo literal en el mundo, no en stub.
- **Faro rejugable con tres ejes:** `dato2` horizontal (`cut -f4 | sort | uniq -c` con header+dup) + `dato3` vertical (`sort -k12 -n | head` 000 primero) + `e2` con `tail` (quitar cabecera, distinguir delimitador `|` vs `,` por `PR-0092`) forman el **alfabeto conteo + red**. El harness puede medir con N=500: «halló nota por `ls -a` vs a ciegas» + «descubrió host por lectura vs `ls`» + «resolvió e2 sin fantasma» — todo determinista por seed; 3 seeds (42/99/123) dan `ENSAYO=1`, `faro` y `2×UMBRAL-BAJO` estables.
- **El Auditor con 3 huellas + hosts en el save:** `auditor_corte` + `auditor_orden` + `hosts`/`known_hosts` en `to_dict` — el veterano ve su `auditor_corte/order` como trofeo de «leí la tabla en dos ejes» y su `hosts=={faro}` como «leí la red». La tríada cortesía de Havel «El Auditor cita tu orden» sigue verificada; con la red, el post-mortem podrá citar `cat /etc/hosts` como cuarta huella cuando ch4 la pida.
- **Hub/eco aún pendiente:** unlock `c.cut`/`c.sort`/`c.tail` sin eco diegético (🧭9 + 🧭17), inventario agregado multi-run sin cruzar runs (P3 30/08). Con `scp` ya copiando entre FS (handler vivo) pero 127 en cap. 6 por allowlist, el veterano aún no mueve ficheros entre hosts en Faro — espera a `story.ch4.*` + `chapter4.py`.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: cap. 4 despierta con red completa — ya NO stub)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **635 passed / 0 xfailed** (gate `load_curriculum()` 22/24, 15 cmds en `DEFAULT_CH6_COMMANDS` con `cut/tail`, bundle 45 ficheros 351.1 KiB). ✓
- **`cat /etc/hosts` sobre mundo real `generate(42,6)`:** exit 0 `127.0.0.1 localhost` + `10.6.0.5 faro`, `hosts=={'faro': FileSystem stub}`, `ls /etc` no descubre, re-leer no duplica, `GameState(shell).to_dict/from_dict` idéntico (hosts+known_hosts+host_stack). ✓
- **Quest `story.ch6.e2` «La que no pesa» (O2 + prosa Manus):** `generate(42,6, contract_id=e2)` → `tail -n +2 | cut -d'|' -f4 | sort` exit 0 sin `distrito`, 2×UMBRAL-BAJO, briefing «un distrito se repite» + hint `tail -n +2` sin regalar, `PR-0092` coma-trampa documentada. ✓
- **`scp` allowlist cap. 6:** `scp faro:…` → 127 `command not found` (frontera deliberada — llega con ch4), pero handler vivo y verificado con shell scp-capaz (copia con metadatos, rechazo didáctico nombra `/etc/hosts` con ruido 0). ✓
- **Puerta web cap. 6 (T1):** `hint-cap6` solo con `chapter=6` (cap. 0 sin hint), `parseParams` `[0,2,3,6]` fallback 0, muerte cap. 6 con `auditor_text`. ✓
- **Faro Bandit + LEEME + coma-trampa + Auditor tríada re-verificados:** `ls` 5 / `ls -a` 6, LEEME relativo `0`+stderr vs absoluta `1`, `head -n1` `|` vs `cut -d','` basura, goldens E2/E3/dato2/dato3 exit 0, tríada Auditor 3 líneas. ✓
- **GNU + determinismo + render + gate 127:** `sort -k0`/`multi-character tab` + `Try --help` exit 2, `generate(42,6)` byte-idéntico salvo `/etc/hosts`, `cap0-room.png` estable, CH6 `ssh`→127. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23 CERRADAS** (re-verificadas 09/09; 22/23 resueltas por e2 con `tail`), **🧭24 PERSISTE** en recámara (higiene allowlist), **🧭25 NUEVO** menor (límite 2 pipes). Ninguna rompe el camino. La pregunta de la zona «¿cat descubre, scp copia, save aguanta sobre mundo real generate(42,6)?» se responde: **sí — cat descubre `faro` en el mundo, scp copia con handler (127 en Faro por allowlist deliberada), y el save lo guarda idéntico.** El cap. 4 ya tiene su suelo completo para nacer.

CICLO: verde — la zona 🔬 se ejecutó completa (mundo real + e2 + scp allowlist + Faro) y el viaje del novato sigue apto; la red dejó de ser stub para ser mundo y la e2 enseña `tail` sin borrar la lección del delimitador.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
