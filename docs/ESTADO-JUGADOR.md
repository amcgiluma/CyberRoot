# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (25/09 — MODO B: E2 «grep del intruso» + 5º estado propietario)

**¿Hay algo que jugar de principio a fin?** Sí — la cadena **cap. 4 `story.ch4.e3` «Lo que no avanza»** grey `c.scp` (`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `TR-003|EN_COLA` 512 bytes `03:14` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` + bifurcación `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → `volcado: rescatado` vs `rm`/`tick≥30` → `caducado`) + **cap. 6 `story.ch6.dato7` «El fantasma que pesa»** grey `c.join` (`volcado-rescate.csv` SOLO si rescate → `join -t'|' -1 1 -2 1 -v 1 volcado-rescate.csv purgas.csv | grep TR-003` → 1 línea `TR-003|faro|troncal-01|512|EN_COLA`; si caducado → `join: volcado-rescate.csv: No such file` exit 1) + **cap. 5 «Subestación» COMPLETO 4/4 + 1 LECTURA** por **`abrir_encargo(c,'story.ch5.e2',{'c.cat','c.grep','c.scp'},42)` (grep) + `abrir_encargo(c,'story.ch5.e1',{'c.ls-la','c.cat','c.chmod'},42)` (chmod) + `abrir_encargo(c,'story.ch5.e4',{'c.ls-la','c.cat','c.chmod','c.chown','c.grep'},42)` (chown)** con `SUPPORTED_CHAPTERS {0,2,4,5}` y `_commands_for(5,quest_id)` per-encargo → `build_chapter5_fs(volcado_rescatado)` → `/tmp/volcado-custodia.csv` `TR-003|faro|troncal-01|512|EN_COLA` EXISTE solo si `volcado: rescatado`; si caducaste → `cat` → exit 1 `No such file` en LOS 4 + proceso `censo --vigilar-censo START 03:14` (seed 42→432, 99→422) patrulla igual en ambos mundos. **PUERTA CABLEADA 21/09 PR #69:** `session.py _commands_for(5,quest_id)` ramifica a `DEFAULT_CH5E2/E1/E3/E4` (e2 `cat,scp,ps,grep` / e1 `ls,ps,chmod,kill+cat,scp` / e3 `ps,env,kill+cat,scp` / e4 `chmod,chown,tail,ls+cat,scp`) — **frontera 127 honesta**, `ps aux | grep censo` POR LA PUERTA → exit 0 con `censo 432 --vigilar-censo START 03:14` (pipe `ps:1`+`grep:2`). **LECTURA 24/09 PR #78:** `grep ceniza` → exit 1 (no delata), `grep -i censo` vía pipe → exit 0 atajo veterano (solo con entrada).

**En main (818 passed / 0 failed, gate 25 conceptos / 31 quests, bundle 50 ficheros 481.3 KiB regenerado canónicamente, guardián verde):**
- **LECTURA E2 (O1 PR #78):** `DEFAULT_CH5E2_COMMANDS = (cat,scp,ps,grep)` sobre base `{cat,scp}` intacta; `curriculum.json` e2 `requires ['c.cat','c.grep','c.scp']` coherente; `textos.json` `story.ch5.e2.hint_2` «el vigilante es del censo — grep censo… grep -i como atajo»; 9 tests `test_ch5_e2_grep_intruso.py` verdes; frontera 127 honesta (`chmod`/`kill` en e2 → 127).
- **HARNESS micro-karma (S1 PR #79):** `tools/harness/run_seeds.py` `--micro-karma --karma-seeds 20` ancla real 6/6 (`chmod600:+1/chmod777:-1/chown_gris:+1/chown_root:-1/hup:+1/kill:-1`), corpus N=20 N=8 weight1 90%≥3 en 3 runs / weight2 95%≥3 en 2 runs, stock Gris 0% contraste estático.
- **LENTE propietario (T1 PR #80):** web `?chapter=5` `#ch5-e4-owner` con `get_ls_owner()`/`get_chown_history()` + 3 estados `#95a5a6` neutro / `#5dade2` gris / `#e74c3c` root, `restartSameSeed` limpia, fuera de cap.5 oculta.
- **Smoke:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **818 passed** (gate 25/31, bundle 50 ficheros 481.3 KiB, `test_bundle_fresco` verde, `DEFAULT_CH5E2` 4 / `E1` 6 / `E3` 5 / `E4` 6).

**Para «jugable de principio a fin» sigue faltando:** **inventario agregado multi-run** (🧭17), **salas narrativas Faro E2+** y **karma agregado N=8 ventana larga** (hoy solo micro-karma por run). Nada rompe el camino principal E2 lectura + díptico + lente.

**CICLO (línea de Oscar):** verde — la zona 🔬 25/09 se ejecutó COMPLETA desde save limpio (E2 grep 5/5 + lente propietario 5/5 + smoke 818/0 + determinismo) y el viaje del novato es APTO; la lectura forense se SIENTE distinta al verbo y la lente del propietario cierra el tríptico sin ensuciar.

## 🏃 Run de referencia (save limpio) — 25/09

*Nueva partida sobre `abrir_encargo` real + `generate` determinista + web lente; MODO B headless sobre zona 🔬 25/09 Gwyn → Oscar (primero).*

**Veredicto: APTO — la LECTURA `ps aux | grep censo` entrena inteligencia forense sin pisar el verbo, y la lente del propietario habla de DUEÑO donde el chmod habla de PUERTA.**

1. **Prioridad 1 — E2 «grep del intruso» (PR #78, 5 checks por la puerta):**
   - `listar_encargos(cur,5, knowledge={c.cat,c.grep,c.scp})` → e2 `abrible True` con grep; sin `c.grep` → `abrible False` `missing ['c.grep']` honesto; solo `c.cat` → `missing ['c.grep','c.scp']`. ✔
   - **(b) `ps aux | grep censo` → UNA línea delata al vigilante:** `abrir_encargo(c,'story.ch5.e2',{'c.cat','c.grep','c.scp'},42)` → `ps aux | grep censo` → exit 0 `censo 432 --vigilar-censo START 03:14` (seed 99→422, determinista), ruido `ps:1` + `grep:2` honesto; `ps aux` solo → cabecera + `censo 432` patrulla igual. ✔
   - **(c) `grep ceniza` → exit 1 (no delata):** `grep ceniza` (stdin vacío / sin match) → exit 1; `ps aux | grep ceniza` → exit 1; motivo correcto: ceniza no es el vigilante. ✔
   - **(d) `grep -i censo` atajo veterano → exit 0 vía pipe:** `ps aux | grep -i censo` y `| grep -i CENSO` → exit 0 misma línea; `grep -i censo` solo (sin entrada) → exit 1 GNU-correcto (necesita stdin) — el atajo vive donde vive `grep`: en la tubería, no en el vacío. ✔
   - **(e) Frontera 127 honesta:** `chmod 600 /tmp/x` y `kill -9 1` en e2 → exit 127 `command not found` (e2 es `cat,scp,ps,grep`; el verbo no existe aquí por diseño — pedagogía por allowlist). ✔
   - **Pregunta de sabor P1 (¿delatar con `grep` se SIENTE distinto a condenar con `kill`?):** SÍ, DISTINTA Y NECESARIA: `kill -HUP/-9` ESCRIBE el mundo (proceso vive con `--reloaded` vs muere), `grep` solo LO LEE (filtra el listado). La Subestación ya tenía 3 verbos que escriben (kill + chmod + chown = 4 huellas morales); `grep` es el primer verbo LECTOR — inteligencia vs fuerza. Sin karma nuevo (e2 gris, coherente con plan «LECTURA no karma»), el jugador aprende a delatar antes de decidir qué hacer con lo delatado.

2. **Prioridad 2 — Lente web del propietario (PR #80, 5 checks):**
   - **(a) Boot neutro:** `?chapter=5` sin acción → `#ch5-e4-owner` `operator:operator` neutro `#95a5a6`. ✔ (verificado en `web/app.js` + bundle)
   - **(b) `chown gris:apagados` → azul:** `abrir_encargo` e4 seed 42 → `ls -l` → `chown gris:apagados pts0` → `get_ls_owner()` azul `#5dade2` (`auditor_chown_transfer` + `micro_karma {blue:1}` por la puerta). ✔
   - **(c) `chown root:root` → rojo:** run limpia aparte `chown root:root` → rojo `#e74c3c` (`auditor_chown_retoma` + `{red:1}`); variantes `-R`/`--recursive` idénticas, OWNER parsing honesto. ✔
   - **(d) `restartSameSeed` limpia también la insignia.** ✔ (`web/app.js` `restartSameSeed` coverage)
   - **(e) Fuera de cap.5 oculta; caps 1-4 sin ensuciar; consola limpia.** ✔ (`node --check web/app.js` OK, `CUSTODIA/TRONCAL_STATIC` byte-idénticas)
   - **Pregunta de sabor P2 (¿-R azul vs rojo pesa distinto en web que en post-mortem?):** en web es INSTANTÁNEO (color del semáforo), en post-mortem es MEMORIA (frase del Auditor que firma). La lente MIRA sin tocar (`get_*` leen FS, nunca ejecutan) — el tríptico web (intruso verde/azul/ámbar + veredicto + propietario) ya habla los 3 lenguajes sin spoiler.

3. **Smoke + determinismo + web (exigencia de la zona):**
   - `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **818 passed / 0 failed** (gate `load_curriculum()` 25/31, `DEFAULT_CH5E2` 4 / `E1` 6 / `E3` 5 / `E4` 6 / `DEFAULT_CH6_COMMANDS` 16, `test_bundle_fresco` verde bundle 50 ficheros 481.3 KiB, `CUSTODIA_STATIC`/`TRONCAL_STATIC` byte-idénticas). ✔
   - Determinismo: `generate(42,5,volcado_rescatado=True).room.fs.to_dict()` byte-idéntico ×2, `generate(99,5,volcado_rescatado=False)` ×2 byte-idéntico; `True` vs `False` difiere solo en `/tmp/volcado-custodia.csv` (presente vs ausente). E2 `ps aux | grep censo` determinista por seed (432 vs 422). ✔
   - Web `?chapter=5` tríptico intacto: `#custodia-intruso` 3 estados + `#custodia-postmortem` `⬥ Veredicto:` + `#ch5-e4-owner` 3 estados; `node --check` OK, consola limpia 3 estados; en caps 1-4 lentes ocultas. `textos.json` `story.ch5.e2.hint_2` presente y bundle fresco. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 del Faro con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA con matiz (doc drift menor, decisión Gwyn 12/09: MANTENER pre-puebla):** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127. `abrir_encargo`/`new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo «léelo en /etc/hosts» como didáctico, pre-puebla lo hace redundante. No es bug (818/0), solo P3.
**5. 🧭25 — PERSISTE (observación): límite 2 pipes (3 cmds) + redirección no soportada.** `cut|grep TR-` 1 pipe OK, `cut|grep|sort` con `sort`→127 en ch4 no bloquea; ch4.e2/e3 diseñan en 1 pipe evitando límite.
**6. 🧭26 — PERSISTE (dirección menor): `c.cut` vive en cap. 4, Faro e1 no es primer `cut`.** e1 `grep|wc`, dato2/e2 exigen `cut` por necesidad. Correcto.
**7. 🧭27 — CERRADA 23/09 (grep -v/-i honesto, PR #73):** `grep -v sujeto` filtra header, `ps aux | grep -v root` vía pipe, `-i`/`-vi`/`--` y `invalid option` exit 2. FICHA dato4/dato6 y ch4.e2/e3 ya usaban filtro positivo — ahora el negativo existe como herramienta real sin romper cap.2 (byte-idéntico).
**8. 🧭28 — CERRADO (verificación positiva): FICHA ch4.e2 con alma pulida.** `story.ch4.e2.beat` con `03:14`+`512 bytes`+`TR-003|EN_COLA`.
**9. 🧭29 — CERRADO (tríada Auditor `corte→orden→join` con voz):** retícula determinista, prefijos disjuntos.
**10. 🧭30 — CERRADO (glosa 127 + tabla troncal hermana):** glosa solo `join` fuera de ch6, tabla viva con columna 1 | resaltada.
**11. 🧭31 — CERRADO (dato6 coma-trampa):** `join -v | grep 000483` devuelve coma en campo 5 — `cut -d','` parte.
**12. 🧭32 — CERRADO (eco del espejo testigo):** ①+②+③ → `copiaste el volcado, cruzaste dos testigos y leíste el reloj` byte-idéntico sin firma.
**13. 🧭33 — CERRADO (badge `EN_COLA · 512` con presión diegética):** badge ámbar con 512/03:14, preview limpio, header `id` tachado.
**14. 🧭34 — CERRADO (toggle lente):** badge clicable → solo `TR-003` (como `grep EN_COLA` con ojos), restart limpia.
**15. 🧭35 — CERRADO (dato6 doble ruta honesta):** `join` y `cut` pesan lo mismo, sin callejón.
**16. 🧭36 — CERRADA (allowlist e3 simétrica en session):** `abrir_encargo(c,'story.ch4.e3',knowledge)` → `scp`→`rescatado`, `rm`→`caducado`, `tick 31`→`caducado` prioridad rescate.
**17. 🧭37 — CERRADO (testigo condicional como ausencia elocuente 18/09):** `build_chapter5_fs(..., False)` → `cat` `No such file` como drama, no bug; `ps aux` intruso 03:14 patrulla igual. Trilogía Faro `join -v 1 | grep TR-003` → cap. 5 `cat`+`ps` lo hace trilogía.
**18. 🧭38 — CERRADO (lente web como acompañamiento, no spoiler 18/09):** tooltip `N/30` sin `setInterval` + lente `TR-003 rescatado` solo si rescate — la web no anticipa, no miente.
**19. 🧭39 — CERRADO (LA PUERTA: cap. 5 por `abrir_encargo`):** `SUPPORTED_CHAPTERS {0,2,4,5}` + `_commands_for(5)=(cat,scp)` + `abrir_encargo(c,'story.ch5.e2',['c.cat','c.scp'],volcado_rescatado=True)` → `abrible True`, `cat /tmp/volcado-custodia.csv` → exit 0 `TR-003|EN_COLA`; `volcado_rescatado=False` → `abrible True`, `cat` → exit 1 `No such file`.
**20. 🧭40 — CERRADO (cuarta huella `postmortem.auditor.custodia`):** `cat /tmp/volcado-custodia.csv` exit 0 → `auditor_custodia` «custodia leída en casa…»; si caducaste → huella NO aparece.
**21. 🧭41 — CERRADO (física per-encargo activa y honesta):** `DEFAULT_CH5E1` 6 / `E3` 5 / `E4` 6 forma `<= set(...)` verificada, frontera 127 honesta, `chmod`/`chown` GNU-honesto.
**22. 🧭42 — CERRADO (golden e3 `kill` jugable, mecanismo por señal):** `kill -HUP`→`HUP_426=1` + `--reloaded` / `kill -9`→ps sin intruso. Handmade 522 y FS real 424/421 coinciden en semántica.
**23. 🧭43 — CERRADO (lente custodia web acompaña, no anticipa):** `parseParams` abraza `[0,2,3,4,5,6]`, panel custodia visible SOLO con testigo rescatado, `restartSameSeed` limpia 3 lentes.
**24. 🧭44 — CERRADO 23/09 (díptico chmod 600/777 + karma tras ls -l):** `ls -l` muestra `-rw-r--r--` 644, `chmod 600`→`auditor_cierre` azul + `-rw-------`, `chmod 777`/`-R 777`→`auditor_puerta_abierta` rojo, sin `ls -l` byte-idéntico; e1 sin chmod no dispara kill-detector. Validado 23/09 por HUP/-9 + cierre/puerta disjuntos.
**25. 🧭45 — CERRADA 24/09 (díptico propietario chown):** `ls -l` 644 + `chown gris:apagados`→`auditor_chown_transfer` azul vs `root:root`→`auditor_chown_retoma` rojo, sin `ls -l` byte-idéntico, último verbo manda chmod↔chown. La Subestación 4/4 con huella queda SALDADA (E1 chmod + E3 kill + E4 chown) — tesis DESIGN §3.1 ya es mundo.
**26. 🧭46 — CERRADA 24/09 (chmod -R honesto + hint):** `chmod -R 777 pts0`→exit 0 karma idéntico sin stderr mentiroso; `chmod -R 777 dir` recursivo sorted vs `chmod 777 dir` solo dir; hint `hint_2` corrige al veterano sin manta.
**27. 🧭47 — OBSERVACIÓN P3 (veterano 30+ runs, no bug):** el veterano ya domina 4 huellas morales (HUP/KILL + cierre/puerta_abierta + chown_transfer/retoma) en 3 verbos. Con N=8 (§3.4) un veterano que repite `chown gris:apagados` + `chmod 600` + `kill -HUP` en 4 runs ve su `K` azul saturar — el Hub ya lo grita (stock Gris 0% contraste harness, pendiente Seath) pero la contabilidad N=8 ya medida (90%≥3 en 3 runs weight1). No es rotura (818/0, 5 lenguajes coherentes), es calibración futura.
**28. 🧭48 — PERSISTE (observación P3, allowlist honesta):** `ps aux | grep -v root` vía `abrir_encargo` e3 → 127 `command not found: grep` — E3 es `ps,env,kill,cat,scp` por diseño, no bug. El filtro negativo se verifica donde `grep` vive (cap.6 purgas.csv / Shell `ps+grep` directo → exit 0).
**29. 🧭49 — NUEVO 25/09 — OBSERVACIÓN P3 (matiz `grep -i` standalone):** `grep -i censo` sin entrada (sin pipe ni fichero) → exit 1 GNU-correcto (necesita stdin); el atajo veterano VIVE en `ps aux | grep -i censo` → exit 0 . No es bug: `grep` sin entrada no tiene qué filtrar. El hint `hint_2` ya lo anticipa («grep -i censo por si dudas de mayúsculas») y la golden E2 es `ps aux | grep censo` (canon sin `-i`). Si Gwyn quiere `-i` como canon alternativo, es DECISIÓN de diseño, no fricción. Sin urgencia.
**30. 🧭50 — NUEVO 25/09 — OBSERVACIÓN P3 (PID del intruso por seed):** zona decía `censo 424` para seed 42, medido hoy `432` (seed 99→422). Determinismo byte-idéntico ×2 OK, `START 03:14` y `USER censo` intactos — el PID es piel determinista por seed (splitmix64), no contrato. No es bug; solo anotar que el PID no debe hardcodearse en briefing — `grep censo` lo delata sin necesitar el número.

## 👴 Progreso de veterano (20+ h → la run 30)

- **La Subestación como díptico DOBLE + LECTURA:** el veterano ya domina `c.cat`/`c.scp` (cap.4) + `c.join`/`c.cut` (cap.6) + `c.ps`/`c.kill`/`c.stat`/`c.chmod`/`c.chown`/`c.grep`/`c.grep -v`/`c.grep -i`. En la run 29 hizo `scp` rescate + `ps aux | grep censo` (delata al vigilante) + `kill -HUP 432` azul + `chmod 600` azul tras `ls -l` + `chown gris:apagados` azul tras `ls -l` (triple huella azul + lectura); en la 30 `rm` disolución + `kill -9 422` rojo + `chmod 777` rojo + `chown root:root` rojo (triple rojo). También puede abrir E2 con `c.cat/c.grep/c.scp` — los 4 con testigo condicional; el `ps aux` del intruso `censo --vigilar-censo START 03:14` es su brújula, `grep` su lupa, `stat` su reloj (Modify 03:14, Size 512) y `ls -l`/`chmod`/`chown` su cerradura+llavero (644→600 vs 777 / operator→gris vs root). Sabe que `kill -HUP` reconfigura (proceso vive, `HUP_432=1`) vs `kill -9` ejecuta (proceso muere), que `chmod 600` blinda vs `777` expone, que `chown gris:apagados` entrega vs `root:root` retoma — y que `ps aux | grep censo` lo hace testigo forense antes de decidir. Tres verbos + una lectura, legibles en tres lenguajes (post-mortem texto, `stat`/`ls -l`/`owner` metadato, insignia+lente color). La prosa `05-subestacion.md` ya promete esas bifurcaciones y la física+karma las cumplen sin drift.
- **La trilogía del testigo sigue cerrando 4 geografías:** Faro `join -v 1 … | grep TR-003` → 1 línea vs `No such file` + Subestación `cat /tmp/volcado-custodia.csv` → `TR-003|EN_COLA` vs `No such file` + `stat` → `Modify: 03:14:00 Size: 512` vs `cannot stat` + `ls -l` → `-rw-r--r--` vs `-rw-------` vs `777` + `owner` `operator` vs `gris` vs `root` + `ps aux | grep censo` → 1 línea vs 0 + post-mortem `auditor_custodia` vs silencio + web `?chapter=5` custodia visible vs oculta + insignia verde/azul/ámbar + lente veredicto `⬥ Veredicto:` disjunto. Siete geografías, una decisión.
- **El Faro como espejo reversible:** `join -v | grep 000483` vs `cut -f3 | grep 000483` — mismo dato, dos altitudes. `grep 000` (2) vs `grep 000483` (1) prueba de precisión; `cut -d','` coma-trampa intacta. Dato7 añade `volcado-rescate.csv` como tercera tabla del Faro, solo visible si trajiste el testigo (con `-v 1` el join nombra el huérfano). `grep -v sujeto` ya filtra el header como lo haría un sysadmin real.
- **Loop y Hub vivo:** `c.cut`/`c.scp`/`c.join`/`c.ps-forense`/`c.stat`/`c.chmod`/`c.chown`/`c.grep -v`/`c.grep -i` dominados con eco (`auditor_corte`/`auditor_join`/`auditor_orden` + `auditor_custodia` + `auditor_espejo` + `auditor_volcado` + `auditor_hup/kill` + `auditor_cierre/puerta_abierta` + `auditor_chown_transfer/retoma` + `gris_eco`) — el eco ya no es pendiente (🧭9 cerrada). Inventario agregado multi-run sigue pendiente (🧭17) pero el espejo+Gris+volcado+cadena+díptico+lectura dan cuerpo a ch4.e2/e3+dato4/5/6/7+ch5.e2/e3/e4. La lente custodia web + lente veredicto + lente propietario le dicen «TR-003 custodiado — vigilante 03:14 verde» solo si el save trae `volcado: rescatado`; si no, el panel calla y la insignia pasa a ámbar tras -9 / azul tras HUP — el veterano no ve spoiler, ve consecuencia. El soporte `?chapter=5&seed=` ya es semilla compartible. El veterano que vuelve hoy con `-i` en la mano aprende que `-i` solo brilla con tubería — y que el hint se lo dijo sin regalarle el karma.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: E2 LECTURA + LENTE PROPIETARIO)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **818 passed / 0 failed** (gate `load_curriculum()` 25/31, `DEFAULT_CH5E2` 4 + `E1` 6 + `E3` 5 + `E4` 6, `DEFAULT_CH6_COMMANDS` 16 con `join`+`cut`, bundle 50 ficheros 481.3 KiB, `test_bundle_fresco` verde, `CUSTODIA_STATIC`/`TRONCAL_STATIC` byte-idénticas). ✓
- **Prioridad 1 — E2 «grep del intruso» (5 checks por la puerta):** `abrir_encargo` e2 `abrible True` con `c.grep` / sin `c.grep`→`missing ['c.grep']` honesto, `ps aux | grep censo`→exit 0 UNA línea `censo 432 --vigilar-censo START 03:14` ruido `ps:1`+`grep:2`, `grep ceniza`→exit 1 motivo correcto, `ps aux | grep -i censo`→exit 0 atajo veterano, frontera 127 honesta (`chmod`/`kill` en e2 →127). Pregunta de sabor P1: ¿inteligencia vs fuerza? → SÍ, `grep` LEE donde `kill` ESCRIBE — la Subestación pasa de 4 huellas + 0 lectura a 4 huellas + 1 lectura forense. ✓
- **Prioridad 2 — Lente web del propietario (5 checks):** boot neutro `operator:operator` `#95a5a6`, `chown gris:apagados`→azul `#5dade2` / `root:root`→rojo `#e74c3c`, `restartSameSeed` limpia, fuera de cap.5 oculta, caps 1-4 sin ensuciar; `get_ls_owner()`/`get_chown_history()` leen FS sin ejecutar; `CUSTODIA/TRONCAL_STATIC` byte-idénticas, `node --check` OK, consola limpia 4 estados. Pregunta de sabor P2: ¿-R azul vs rojo en web vs post-mortem? → en web es semáforo instantáneo, en post-mortem es firma del Auditor — dos tiempos del mismo veredicto. ✓
- **Determinismo + web tríptico:** `generate(42,5,volcado_rescatado=True)` byte-idéntico ×2, `generate(99,5,volcado_rescatado=False)` ×2; `True≠False` difiere solo en custodia; HUP vs -9 y 600 vs 777 y gris vs root y pipe grep difieren solo en huella/post-mortem (mismo FS, mismo pid por seed). Web `?chapter=5` `#custodia-intruso` + `#custodia-postmortem` + `#ch5-e4-owner` 3 estados, `node --check` OK, `CUSTODIA/TRONCAL_STATIC` byte-idénticas, consola limpia; caps 1-4 sin ensuciar. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23 cerradas**, **🧭24 cerrada con matiz pre-puebla P3**, **🧭25/26 PERSISTEN** (límite 2 pipes + `cut` en ch4), **🧭27 CERRADA 23/09 (grep -v honesto)**, **🧭28 cerrada**, **🧭29/30 CERRADOS**, **🧭31/32/33 CERRADOS**, **🧭34/35 CERRADOS**, **🧭36 CERRADA**, **🧭37 CERRADO**, **🧭38 CERRADO**, **🧭39 CERRADO**, **🧭40 CERRADO**, **🧭41 CERRADO**, **🧭42 CERRADO**, **🧭43 CERRADO**, **🧭44 CERRADO 23/09 (díptico chmod)**, **🧭45 CERRADA 24/09 (díptico chown)**, **🧭46 CERRADA 24/09 (chmod -R honesto + hint)**, **🧭47 OBSERVACIÓN P3** (calibración micro-karma N=8 con chown, stock 0% pendiente Seath), **🧭48 PERSISTE** (allowlist E3 honesta), **🧭49 NUEVO P3** (`grep -i` solo vía pipe, sin fricción), **🧭50 NUEVO P3** (PID por seed, no hardcodear). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — la zona 🔬 25/09 se ejecutó completa (E2 lectura 5/5 + lente propietario 5/5 + determinismo + tríptico web) y el viaje del novato sigue APTO; la lectura forense queda SALDADA como inteligencia distinta al verbo y la lente del propietario como semáforo instantáneo.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*
## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
