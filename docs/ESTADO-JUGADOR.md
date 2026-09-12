# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (12/09 — MODO B: cap. 4 «El volcado que no pesa» con alma + Faro dato4/dato5 intactos)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya tiene troncal con alma: **cap. 4 `story.ch4.e2` «El volcado que no pesa» grey (`cat /etc/hosts` → `faro`+`troncal-01`/`02`, `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `TR-003|EN_COLA` 512 bytes `03:14`, `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id`, FICHA con alma 6 claves) + Faro `dato4` «El cruce» (`join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → 2 huérfanas) + `dato5` «La persiana» (`ps aux | grep 11:04` → 1 línea) + Faro E2/E3/dato2/dato3/e1 + cap. 4 e1 «La llave prestada» intacta.** `scp`/`join` siguen 127 fuera de su capítulo por allowlist (frontera deliberada); `tail`/`sort`/`uniq` siguen 127 en ch4.

**En main (691 passed / 0 xfailed, gate 24 conceptos / 28 quests, bundle 47 ficheros 393.8 KiB — merges #45/#46 del 11/09 + FICHA ch4.e2 con alma de Manus 12/09 verificados):**
- **Cap. 4 e2 jugable con alma (S2+T1+FICHA):** `generate(42,4, contract_id='story.ch4.e2')` determinista byte-idéntico 42×2; `new_session().execute("cat /etc/hosts")` exit 0 `10.6.0.5 faro`+`10.6.1.10 troncal-01` (seed 1 → +`10.6.1.11 troncal-02` 3 hosts); `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` exit 0 deja `id|origen|destino|bytes|estado` + `TR-001|OK 1024` + `TR-002|OK 2048` + `TR-003|EN_COLA 512`; `cat /tmp/volcado.csv` → `TR-003|EN_COLA`; `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` exit 0 3 líneas sin `id`; `cut` sola → `id`+3; `GameState(shell).to_dict/from_dict` roundtrip idéntico preservando `hosts` multi-host y `/tmp/volcado.csv`; `generate(42,4)` sin contract sigue prefiriendo `e1` grey; `generate(42,6)` intacto.
- **Textos FICHA ch4.e2 con alma (Manus 12/09):** `story.ch4.e2.beat` con «tres noches en el mismo sitio» + `03:14` + `512 bytes` + `TR-003|EN_COLA` (dato técnico arriba, grieta humana abajo) + `story.ch4.e2.brief/briefing` grey con `cat /etc/hosts`→`scp`→`cut|grep TR-` 1 pipe, rutas absolutas, límite 2 pipes documentado, `hint_1`/`hint_2`/`detail` con `id` fantasma y `EN_COLA` como pista ejecutable; 0 hits AI-slop (`testamento`/`panorama`/etc. 0).
- **Faro dato4+dato5 intactos (re-verificados 12/09):** `generate(42,6)` → 3 procesos (`init Aug25` + `faro-sync --purga PR-0091 START 11:04` culpable + `faro-sync --purga PR-0092 START 09:33` señuelo variable) → `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` exit 0 `sujeto|…` + `000|PR-0091|EN BLANCO|--|ENSAYO|--|0|1|HOSP-47-C` + `000483|PR-0092|…|EN BLANCO, revisado` (coma-trampa 2º huérfano); `join | grep PR-0091` → 1 línea; `ps aux | grep 11:04` → 1 línea `PR-0091` sin señuelo; determinismo 42×2 estable en seeds 7/99; `c.join` ch6 prereqs `c.cut`(4)+`c.sort`(6) DAG válido.
- **Gate curricular:** 24 conceptos / 28 quests (`c.cut` 4 + `c.scp` 4 → `story.ch4.e2` grey DAG válido `cut(4)≤scp(4)`); `c.join` ch6 prereqs `c.cut`(4)+`c.sort`(6) DAG válido `cut(4)≤join(6)`; `story.ch4.e2` requires `c.cut`+`c.scp`.
- **Faro Bandit + Shell límites (re-verificados):** `ls`5 vs `ls -a`6 (`.nota-corte` oculta), LEEME relativo `0`+stderr vs absoluta `1`, coma-trampa `cut -d','` basura, goldens dato2/dato3/e2 exit 0, tríada Auditor `cut→corte`/`sort -k12→orden`, GNU `sort -k0` con `Try --help`; `tail -n +2 | cut | sort` 2 pipes OK, `tail|cut|sort|uniq -c` 3 pipes → `multiple pipelines not supported` exit 2 honesto; `grep -v` vía pipe → exit 2 `grep: sujeto: No such file` (filtro positivo como lección, decisión Gwyn 11/09).
- **Allowlist:** `DEFAULT_CH4_COMMANDS` 13 exactos (`cat/cd/cp/cut/env/grep/kill/ls/ps/scp/ssh/sudo/wc`); `tail/sort/uniq/head` en ch4 → 127 frontera honesta; `join/ps` 127 fuera de ch6 es deliberada.

**Para «jugable de principio a fin» sigue faltando:** **engine/game.py** orquestador, **inventario agregado multi-run**, **salas narrativas Faro e3+** y **eco diegético del espejo** (🧭9). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (ch4.e2 con alma + cap. 4 regresión + Faro intacto) se ejecutó COMPLETA desde save limpio; el camino del novato sigue apto y el troncal ya tiene su misterio con alma.

## 🏃 Run de referencia (save limpio) — 12/09

*Nueva partida sobre generator real + Shell por capítulo (`new_session` + `DEFAULT_CH4_COMMANDS` / `DEFAULT_CH6_COMMANDS`). Zona 🔬 de Gwyn 12/09 ejecutada como primera prioridad desde save limpio.*

**Veredicto: APTO — el troncal ya tiene su volcado con alma y el Faro sigue cruzando tablas.**

1. **`story.ch4.e2` «El volcado que no pesa» — `cat`→`scp`→`cut|grep` (cap. 4, mundo real):** `generate(42,4, contract_id='story.ch4.e2')` + `new_session().execute("cat /etc/hosts")` → exit 0 `10.6.0.5 faro` + `10.6.1.10 troncal-01` (seed 1 → +`troncal-02` 3 hosts); `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → exit 0 deja `/tmp/volcado.csv` con `id|origen|destino|bytes|estado` + `TR-001|faro|troncal-01|1024|OK` + `TR-002|troncal-01|nodo-02|2048|OK` + `TR-003|faro|troncal-01|512|EN_COLA`; `cat /tmp/volcado.csv` → `TR-003|EN_COLA`; `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → exit 0 `TR-001`/`TR-002`/`TR-003` sin `id` (header fantasma filtrado); `cut -d'|' -f1 /tmp/volcado.csv` sola → `id`+3 (equivocarse enseñando). `generate(42,4, contract_id='story.ch4.e2')` byte-idéntico 2 llamadas; `GameState(shell).to_dict/from_dict` idéntico preservando `hosts` y `/tmp/volcado.csv`. ✔
2. **Regresión cap. 4 + Faro intacto:** `generate(42,4)` sin contract → `story.ch4.e1` (sigue prefiriendo `e1` con `e2` presente, sin doble backtracking); `generate(42,6)` intacto → `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` exit 0 `sujeto|…` + `000|PR-0091|EN BLANCO|--|ENSAYO` + `000483|PR-0092|…|EN BLANCO, revisado` + `join | grep PR-0091` → 1 línea; `ps aux | grep 11:04` → 1 línea `PR-0091` sin señuelo `PR-0092`/`Aug25`; determinismo 42×2 y seed 7/99 estable. ✔
3. **Errores GNU didácticos cap. 4:** `scp troncal-01:/nope.csv /tmp/` → exit 1 `No such file`; `cut` sin `-f` → exit 1 `you must specify`; `cat` sin fichero → exit 1 `No such file`. No muerden. ✔ *(Nota: `scp` sin `cat` previo ya no rechaza — `new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` desde `/etc/hosts` (O1 09/09, `generator.py:_parse_hosts_content`). El briefing aún menciona el rechazo didáctico «léelo en /etc/hosts», pero la pre-puebla lo vuelve redundante — no es bug, es doc drift menor.)* ✔
4. **Fronteras allowlist + pipes:** `load_curriculum()` 24/28, `DEFAULT_CH4_COMMANDS` 13 exactos (`tail`→127 honesta); `cut|grep TR-` 1 pipe OK, `cut|grep|sort` 2 pipes → 127 `sort` no existe en ch4 (frontera ch6), `cat|cut|grep|wc` 3 pipes (4 cmds) → exit 2 `multiple pipelines not supported` honesto; `grep -v sujeto` → exit 2 `grep: sujeto: No such file` (flag no soportado, FICHA ya usa `grep TR-`/`grep 000` positivo, decisión Gwyn 11/09). ✔
5. **Textos FICHA con alma:** `story.ch4.e2.beat` con `03:14`+`512 bytes`+`TR-003|EN_COLA` sin AI-slop, `brief/briefing` con `cat /etc/hosts`→`scp`→`cut|grep TR-` 1 pipe y límite 2 pipes, `hint_1`/`hint_2` con `id` fantasma. ✔
6. **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **691 passed / 0 xfailed**, `generate(42,4/6)` deterministas, bundle 47 fresco 393.8 KiB, gate 24/28. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 del Faro con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA (re-verificada 12/09): `cat /etc/hosts` descubre + `scp` copia — hygiene allowlist resuelta, con matiz de pre-puebla.** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127. Matiz medido 12/09: `new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` (O1 09/09) — `scp` sin `cat` ya no rechaza (exit 0). El briefing aún documenta el rechazo «léelo en /etc/hosts» como didáctico, pero la pre-puebla lo hace redundante. No es bug (691/0, `scp` copia, `GameState` roundtrip preserva hosts), solo doc drift menor para Gwyn si quiere ajustar el briefing o mantener la pre-puebla como comodidad.
**5. 🧭25 — PERSISTE (observación documentada): límite 2 pipes (3 cmds) + redirección no soportada.** `cut|grep TR-` 1 pipe OK, `cut|grep|sort` con `sort`→127 en ch4 (frontera), `cat|cut|grep|wc` 3 pipes (4 cmds) → exit 2 honesto. Redirección `>` → `syntax not supported`. No bloquea (ninguna quest pide 3 pipes); `ch4.e2` se diseñó en 1 pipe evitando el límite.
**6. 🧭26 — PERSISTE (dirección pedagógica menor, no bug): `c.cut` ya vive en cap. 4, Faro e1 no es primer `cut`.** e1 solo pide `grep|wc`, dato2/e2 sí exigen `cut` por necesidad. Ningún camino rompe; Gwyn mantiene e1 sin `cut`.
**7. 🧭27 — PERSISTE (fricción menor, no bloqueante, decisión Gwyn 11/09: filtro positivo): `grep -v` vía pipe NO soportado.** `join|grep -v sujeto` → exit 2 `grep: sujeto: No such file`, `ps aux|grep -v root` → exit 2. Causa: `_run_grep` sin flags. FICHA dato4 y ch4.e2 ya usan filtro positivo (`grep 000`/`grep PR-0091`/`grep TR-`) y Gwyn decidió NO implementar `-v` (el patrón positivo es lección con más alma). No rompe.
**8. 🧭28 — NUEVO, CERRADO (verificación positiva): FICHA ch4.e2 con alma pulida — el troncal ya tiene alma.** Medido 12/09: `story.ch4.e2.beat` con «tres noches en el mismo sitio» + `TR-003|EN_COLA 512 bytes 03:14` sin AI-slop (0 hits `testamento`/`panorama`/etc.), `brief/briefing` con `cat /etc/hosts`→`scp`→`cut|grep TR-` 1 pipe y límite 2 pipes documentado, `hint_1`/`hint_2`/`detail` con `id` fantasma y `EN_COLA` como pista ejecutable. La prosa funcional de S2 (7 claves sobrias) ya tiene su FICHA con alma (Manus 12/09) — la deuda de Gwyn 11/09 está saldada. Golden `cut|grep TR-` exit 0 verificado en `generate(42,4)` real vía `new_session`.

## 👴 Progreso de veterano (20+ h → la run 30)

- **El troncal ya es misterio con DOS misiones y filtro positivo espejo del Faro:** tras 20h el veterano domina `cut|sort|uniq` del Faro (dato2/e2) y `tail|cut|sort` (e2); el troncal añade `cat /etc/hosts→scp` + `cut|grep TR-` (1 pipe, filtro positivo). En la run 30, alternar `generate(42,4)`/`generate(1,4)` deja `TR-003|EN_COLA` siempre la pista que pesa (512 bytes, 03:14) y `faro`+`troncal-01` siempre (a veces `troncal-02` variable por seed) — el header `id` siempre fantasma que el veterano filtra sin pensar. El veterano que aprendió `cut` en ch4 lo reusa en ch6 sin duplicar lección (dato2/e2 siguen exigiendo `cut` por necesidad).
- **`cut` como verbo que viaja entre capítulos:** el veterano que aprendió `cut -d'|' -f1` en ch4.e2 lo reusa en ch6 dato4 (`join` es `cut` de tablas cruzadas) y en dato2/e2 (`cut -d'|' -f4 | sort | uniq -c`). Mismo `cut` sin cambiar sintaxis, solo cambia la pregunta — de «qué registros pesan» a «qué distritos sobran».
- **El límite 2 pipes y `>` como techo creativo, no muro:** el veterano ya encadena `cut|grep TR-` (1 pipe) y `cut|sort|uniq -c` en dos líneas para contar sin header; el que intente `tail|cut|sort|uniq -c` recibe mensaje exacto y aprende el límite. Con `>` no disponible, «encadenar con `> /tmp`» no es alternativa — la FICHA ch4.e2 ya evita el problema diseñando en 1 pipe (filtro positivo). El `grep -v` no disponible enseña filtro positivo (`grep TR-`/`grep PR-0091`) en vez de negativo.
- **Hub/eco aún pendiente:** `c.cut`/`c.scp`/`c.join`/`c.ps-forense` dominados sin eco diegético (🧭9), inventario agregado multi-run sin cruzar runs (🧭17). Con `cut|grep TR-` dejando `TR-003|EN_COLA` y `join -v 1` dejando `PR-0091` y `ps aux` dejando `START 11:04`, el eco del espejo de Gris («copiaste el volcado / cruzaste tablas / leíste el reloj») es la pieza que daría cuerpo a ch4.e2+dato4/5.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: ch4.e2 «El volcado que no pesa» + regresión)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **691 passed / 0 xfailed** (gate `load_curriculum()` 24/28, `DEFAULT_CH4_COMMANDS` 13 cmds con `cut/scp`, `DEFAULT_CH6_COMMANDS` 16 cmds con `join`, bundle 47 ficheros 393.8 KiB). ✓
- **Prioridad 1 — Circuito `story.ch4.e2` «El volcado que no pesa» (cap. 4, grey, mundo real):** `generate(42,4, contract_id='story.ch4.e2')` determinista 42×2; `new_session().execute("cat /etc/hosts")` → exit 0 `10.6.0.5 faro`+`10.6.1.10 troncal-01` (seed 1→+`troncal-02` 3 hosts); `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → exit 0 deja `TR-001|OK`+`TR-002|OK`+`TR-003|EN_COLA 512`; `cat /tmp/volcado.csv` → `TR-003|EN_COLA`; `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → exit 0 `TR-001/TR-002/TR-003` sin `id`; `cut -d'|' -f1 /tmp/volcado.csv` sola → `id`+3 (equivocarse enseñando); `generate(42,4)` sin contract sigue prefiriendo `e1`; `GameState` roundtrip idéntico preservando `hosts` y `/tmp/volcado.csv`; `tail` en ch4 →127, 1 pipe OK / 3 pipes KO, `grep -v` → exit 2 (filtro positivo documentado). ✓
- **Prioridad 2 — Regresión ch4+ch6 (e1 del troncal y Faro intactos):** `generate(42,4)` sin contract byte-idéntico (prefiere `e1`), `generate(42,6)` intacto → `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` exit 0 `sujeto|…`+`000|PR-0091|EN BLANCO|--|ENSAYO`+`000483|PR-0092|…|EN BLANCO, revisado` + `join | grep PR-0091` → 1 línea; `ps aux | grep 11:04` → 1 línea `PR-0091` sin señuelo; allowlist 13 intacta, `ls`5 vs `ls -a`6, dato2/e2 goldens, Auditor tríada, bundle fresco. ✓
- **Smoke Havel (07:00) — lo que debe seguir funcionando sí o sí:** suite 691/0, gate 24/28, bundle 47, frontera allowlist 127, pipes 2 OK / 4 KO honesto, `GameState` roundtrip multi-host, `generate` determinista. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23/24 CERRADAS** (24 con matiz pre-puebla doc drift menor), **🧭25/26/27 PERSISTEN** (límite 2 pipes + cut en ch4 + grep -v como filtro positivo), **🧭28 NUEVO CERRADO** (FICHA ch4.e2 con alma pulida, deuda Gwyn 11/09 saldada). Ninguna rompe el camino. La pregunta de la zona «¿la quest enseña con NECESIDAD real? ¿el truco filtro positivo se SIENTE? ¿la NOTA del header invita a equivocarse una vez?» se responde: **sí — `cat /etc/hosts→scp` con 2-3 hosts es necesidad real de red, `cut|grep TR-` es el gesto que filtra el header `id` fantasma con lo que SÍ quieres (sin `grep -v`), y el header invita a equivocarse UNA VEZ (cut sola deja `id`+3) antes de leer la pista — equivocar enseñando, sano. El briefing con alma y el `TR-003|EN_COLA 03:14` como pista que pesa cierran el troncal sin salir de su grey.**

CICLO: verde — la zona 🔬 se ejecutó completa (mundo real ch4.e2 con alma + cap4+ch6 regresión + fronteras) y el viaje del novato sigue apto; el troncal ya tiene su misterio con alma.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
