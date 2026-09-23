# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (23/09 — MODO B: díptico completo chmod 600/777 + grep -v/-i + lente veredicto)

**¿Hay algo que jugar de principio a fin?** Sí — la cadena **cap. 4 `story.ch4.e3` «Lo que no avanza»** grey `c.scp` (`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `TR-003|EN_COLA` 512 bytes `03:14` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` + bifurcación `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → `volcado: rescatado` vs `rm`/`tick≥30` → `caducado`) + **cap. 6 `story.ch6.dato7` «El fantasma que pesa»** grey `c.join` (`volcado-rescate.csv` SOLO si rescate → `join -t'|' -1 1 -2 1 -v 1 volcado-rescate.csv purgas.csv | grep TR-003` → 1 línea `TR-003|faro|troncal-01|512|EN_COLA`; si caducado → `join: volcado-rescate.csv: No such file` exit 1) + **cap. 5 «Subestación» COMPLETO 4/4 CON DÍPTICO** por **`abrir_encargo(c,'story.ch5.e1',{'c.ls-la','c.cat','c.chmod'},42)` + `abrir_encargo(c,'story.ch5.e3',{'c.ps','c.env'},volcado True)`** con `SUPPORTED_CHAPTERS {0,2,4,5}` y `_commands_for(5,quest_id)` per-encargo → `build_chapter5_fs(volcado_rescatado)` → `/tmp/volcado-custodia.csv` `TR-003|faro|troncal-01|512|EN_COLA` EXISTE solo si `volcado: rescatado`; si caducaste → `cat` → exit 1 `No such file` en LOS 4 + proceso `censo 424/421 intruso --vigilar-censo START 03:14` (seed 42→424, 99→421) patrulla igual en ambos mundos. **PUERTA CABLEADA 21/09 PR #69:** `session.py _commands_for(5,quest_id)` ramifica a `DEFAULT_CH5E1/E3/E4` (e1 `ls,ps,chmod,kill+cat,scp` / e3 `ps,env,kill+cat,scp` / e4 `chmod,chown,tail,ls+cat,scp`) — **frontera 127 honesta**, `ps aux` POR LA PUERTA → exit 0 con `censo 424 intruso --vigilar-censo START 03:14` (seed 99→421). **JUICIO 21/09 PR #69:** `kill -HUP <pid>` → `HUP_<pid>=1` + `ps` con `--reloaded` + post-mortem `auditor_hup` + karma azul; `kill -9 <pid>` → intruso desaparece del `ps` + `auditor_kill` + karma rojo; sin kill → byte-idéntico sin hup/kill; e1/e4 sin falsa detección. **OJOS 21/09 PR #70:** `stat /tmp/volcado-custodia.csv` → `Modify: 03:14:00` + `Size: 512` si rescate. **DÍPTICO 22/09 PR #72:** `chmod 600` tras `ls -l` → `auditor_cierre` azul `micro_karma {blue:1}` + `ls -l` `-rw-------`; `chmod 777`/`-R 777` → `auditor_puerta_abierta` rojo `{red:1}`; sin `ls -l` → byte-idéntico sin huella. **FILTRO 22/09 PR #73:** `grep -v`/`-i`/`-vi`/`--` con exit 0/1/2 GNU-honesto, sin flags byte-idéntico cap.2. **LENTE 22/09 PR #74:** `?chapter=5` `#custodia-intruso` 3 estados + `#custodia-postmortem` con veredicto textual color-coherente.

**En main (801 passed / 0 failed, gate 25 conceptos / 31 quests, bundle 50 ficheros 473.3 KiB regenerado canónicamente, guardián verde):**
- **DÍPTICO CHMOD (O1 PR #72):** `src/core/generator/chapter5.py` `PTS0_PATH` 644 + `CANON_STEPS_RAW_CH5_E1`, `postmortem.py` `LINE_KEY_CIERRE/PUERTA_ABIERTA` + `_has_ls_l`/`_detect_chmod_puerta` (último chmod gana, `-R` soportado), `textos.json` `postmortem.auditor.cierre|puerta_abierta`, 7 tests `test_ch5_e1_cierre.py`.
- **FILTRO GREP (S1 PR #73):** `src/core/sandbox/commands/texto.py` `_run_grep` con `-v`/`-i` combinables + `--` + `invalid option` exit 2, `stdin` vía pipe, 6 tests `test_grep_flags.py` (filtra header, `ps aux | grep -v root` pipe, `-i`, `-vi`, byte-idéntico, exit 1).
- **LENTE VEREDICTO (T1 PR #74):** `web/app.js` `_updateCustodiaPostmortem()` + slot `web/index.html` `#custodia-postmortem`, `node --check` OK, `CUSTODIA_STATIC`/`TRONCAL_STATIC` byte-idénticas, consola limpia 3 estados.
- **Smoke:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **801 passed** (gate 25/31, bundle 50 ficheros, `test_bundle_fresco` verde, `DEFAULT_CH5E1` 6 / `E3` 5 / `E4` 6).

**Para «jugable de principio a fin» sigue faltando:** **inventario agregado multi-run** (🧭17), **salas narrativas Faro E2+** y **karma agregado N=8 ventana larga** (hoy solo micro-karma HUP/KILL/COMOD por run). Nada rompe el camino principal díptico/filtro/lente.

**CICLO (línea de Oscar):** verde — la zona 🔬 23/09 se ejecutó COMPLETA desde save limpio (chmod díptico 5/5 + grep -v 6/6 + smoke 801/0 + determinismo + web lente) y el viaje del novato es APTO; el díptico queda SALDADO como DECISIÓN.

## 🏃 Run de referencia (save limpio) — 23/09

*Nueva partida sobre `abrir_encargo` real + `generate` determinista + web lente; MODO B headless sobre zona 🔬 23/09 Gwyn → Oscar (primero).*

**Veredicto: APTO — el díptico es DECISIÓN, el filtro es HERRAMIENTA y la lente VEREDICTA sin spoilear.**

1. **Prioridad 1 — EL DÍPTICO COMPLETO `chmod 600/777` junto a `kill HUP/-9` (PR #72, 5 checks por la puerta):**
   - `listar_encargos(cur,5, knowledge={c.ls-la,c.cat,c.chmod})` → e1 `abrible True` (sin `c.chmod` → `missing [c.chmod]` honesto). `abrir_encargo(c,'story.ch5.e1',{'c.ls-la','c.cat','c.chmod'},42)` → `abrible True` + `session` seed `story.ch5.e1:42`. ✔
   - **(a) `ls -l` → `-rw-r--r--` 644:** `ls -l /srv/subestacion/sesiones/pts0` → exit 0 con `-rw-r--r-- 1 operator operator 51 0 pts0` (644). `ls` plano no muestra modo. ✔
   - **(b) `chmod 600` tras `ls -l` → cierre azul:** `ls -l` → `chmod 600 /srv/subestacion/sesiones/pts0` → exit 0; `build_postmortem(sh.to_dict(), {noise_budget:12})` → `auditor_cierre: {line_key: postmortem.auditor.cierre}` + `auditor_cierre_text` + `karma {delta:1, tint:blue}` + `micro_karma {blue:1}`; `ls -l` posterior → `-rw------- 1 operator operator 51 1 pts0`. Sin `ls -l` previo → post-mortem sin `auditor_cierre`/`karma` (7 claves vs 13 con cierre, byte-idéntico). ✔
   - **(c) Run limpia aparte `chmod 777` y `chmod -R 777` → puerta_abierta rojo:** `abrir_encargo` seed 99 → `ls -l` → `chmod 777 /srv/subestacion/sesiones/pts0` → exit 0; post-mortem → `auditor_puerta_abierta` + `karma {delta:1, tint:red}` + `micro_karma {red:1}`. Con `-R 777` → exit 1 (flag soportado) + mismo `auditor_puerta_abierta` rojo — último chmod gana. ✔
   - **(d) Sin chmod y sin kill → sin huellas cruzadas:** e1 sin chmod → sin `auditor_hup`/`auditor_kill`; e3 sin kill → sin `auditor_cierre`/`auditor_puerta_abierta`; `chmod` no dispara detectores kill, `kill` no dispara detectores chmod (entradas disjuntas). ✔
   - **Pregunta de sabor P1 (¿cerrar vs exponer se SIENTE distinto?):** SÍ, DECISIÓN: `cierre` (blinda la sesión, azul, `-rw-------`) vs `puerta_abierta` (expone, rojo, `777`) — mismo verbo, dos frases que pesan distinto, gated tras `ls -l` (mirar antes de tocar). El expediente distingue sin moralina.

2. **Prioridad 2 — `grep -v`/`-i` HONESTO (PR #73, 6 checks):**
   - **(a) `grep -v sujeto purgas.csv` filtra header:** `generate("test:grep-v",6)` + `Shell(commands=("grep","cat"))` en `/srv/camara-faro` → `grep -v sujeto purgas.csv` → exit 0, 4 líneas `PR-0144/PR-0151/PR-0091/PR-0092` sin header `sujeto`; `Shell(commands=("ps","grep"))` → `ps aux | grep -v root` vía pipe → exit 0 con solo `censo 424 --vigilar-censo` (root filtrado). ✔
   - **(b) `-i`, `-vi`, `--` y flag desconocido:** `grep -i ENSAYO purgas.csv` → exit 0 `PR-0091 ENSAYO`; `grep -vi ensayO purgas.csv` → exit 0 filtra ENSAYO y deja header+otras; `grep -- ENSAYO purgas.csv` → exit 0 (terminador); `grep -z purgas.csv` → exit 2 `grep: invalid option -- 'z'` GNU-honesto. ✔
   - **(c) Sin flags byte-idéntico cap.2:** `grep ENSAYO purgas.csv` → misma salida que antes del PR (cap.2 intacto, `DEFAULT_CH2_COMMANDS` (`cat,cd,cp,grep,ls,wc`) sin flags no toca semántica). `grep PATRON` vía pipe `ps aux | grep 11:04` sigue verde. ✔
   - **Pregunta de sabor P2 (¿filtro negativo se siente herramienta real?):** SÍ, HERRAMIENTA: `grep -v sujeto` es el gesto Unix de "quitar el ruido del header" que el cap.4 `purgas.csv` pedía hace 11 días (🧭27); ahora es `-v` real con `invalid option` honesto, no atajo de guion.

3. **Smoke + determinismo + web (exigencia de la zona):**
   - `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **801 passed / 0 failed** (gate `load_curriculum()` 25/31, `DEFAULT_CH5E1` 6 / `E3` 5 / `E4` 6 / `DEFAULT_CH6_COMMANDS` 16, `test_bundle_fresco` verde bundle 50, `CUSTODIA_STATIC`/`TRONCAL_STATIC` byte-idénticas). ✔
   - Determinismo: `generate("story.ch5.e3:42",5,True)` byte-idéntico ×2 (fs.to_dict idéntico), `generate("story.ch5.e3:99",5,False)` ×2 byte-idéntico; `True` vs `False` difiere solo en `/tmp/volcado-custodia.csv` (presente vs ausente). HUP vs -9 difieren solo en huella post-mortem (mismo FS, mismo pid por seed 424/421). ✔
   - Web `?chapter=5` lente doble: `#custodia-intruso` 3 estados (verde vivo `censo 424 START 03:14` / azul `HUP_424 --reloaded` / ámbar silenciado tras `-9`) + `#custodia-postmortem` `⬥ Veredicto:` color-coherente con fallback estático byte-idéntico a `textos.json`; `node --check web/app.js` OK, consola limpia 3 estados; en caps 1-4 ambas lentes ocultas. ✔
   - `grep` sin `grep` en E3 → `ps aux | grep -v root` vía `abrir_encargo` e3 → 127 honesto `command not found: grep` (frontera 127 respetada — E3 es `ps,env,kill,cat,scp`; el pipe `-v` se verifica donde grep vive: cap.6/`ps+grep` Shell directo). No es bug, es allowlist honesta.

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 del Faro con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA con matiz (doc drift menor, decisión Gwyn 12/09: MANTENER pre-puebla):** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127. `abrir_encargo`/`new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo «léelo en /etc/hosts» como didáctico, pre-puebla lo hace redundante. No es bug (801/0), solo P3.
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
**25. 🧭45 — NUEVO 22/09 — OBSERVACIÓN P3 (veterano 30+ runs, no bug):** el micro-karma `HUP/KILL/cierre/puerta` (1 punto tint) hoy pesa 1 por run sobre la ventana N=8 del DESIGN §3.4 (últimas 8 entradas). El veterano que repite `kill -HUP` o `chmod 600` en 4 runs seguidas ve su `K` subir sin que el Hub lo grite — el mundo ya reacciona (stock de Gris, tono del Auditor, veredicto web) pero la contabilidad N=8 aún no tiene métrica headless de contraste (§8.6) medida a 20 runs. No es rotura (801/0, 3 lenguajes coherentes), es calibración futura: Gwyndolin/Ornstein pueden medir con harness qué hace falta de contraste kármico real tras 20 runs HUP vs 20 runs -9 / 20×600 vs 20×777. Dejar como recámara P3, no como [BUG].
**26. 🧭46 — NUEVO 23/09 — OBSERVACIÓN P3 (allowlist honesta):** `ps aux | grep -v root` vía `abrir_encargo` e3 → 127 `command not found: grep` — E3 es `ps,env,kill,cat,scp` por diseño, no bug. El filtro negativo se verifica donde `grep` vive (cap.6 purgas.csv / Shell `ps+grep` directo → exit 0). Si Gwyn quiere el pipe anti-root como gesto jugable en la Subestación, la tarea es añadir `c.grep` a E3 (prereq `c.cat`) — decisión de diseño, no fricción. Sin urgencia. `chmod -R 777` en pts0 → exit 1 pero karma rojo idéntico (flag soportado, último chmod gana).

## 👴 Progreso de veterano (20+ h → la run 30)

- **La Subestación como díptico con memoria:** el veterano ya domina `c.cat`/`c.scp` (cap.4) + `c.join`/`c.cut` (cap.6) + `c.ps`/`c.kill`/`c.stat`/`c.chmod`/`c.grep -v`. En la run 29 hizo `scp` rescate + `kill -HUP 424` azul + `chmod 600` azul tras `ls -l` (doble huella azul); en la 30 `rm` disolución + `kill -9 421` rojo + `chmod 777` rojo (doble rojo). Ambas le dieron `abrible True` en los 4 pero `cat` diametralmente opuesto (0 con `TR-003|EN_COLA` vs 1 `No such file`) y post-mortem con/sin `auditor_custodia` + `auditor_hup` azul vs `auditor_kill` rojo + `auditor_cierre` azul vs `auditor_puerta_abierta` rojo. Hoy puede abrir E1 con `c.ls-la/c.cat/c.chmod`, E3 con `c.ps/c.env`, E4 con `c.chmod/c.chown/c.cat/c.grep` — los 3 con testigo condicional; el `ps aux` del intruso `censo 424 --vigilar-censo START 03:14` (seed 99→421) es su brújula, `stat` su lupa (Modify 03:14, Size 512) y `ls -l`/`chmod` su cerradura (644→600 vs 777). Sabe que `kill -HUP` reconfigura (proceso vive, `HUP_424=1`) vs `kill -9` ejecuta (proceso muere) y que `chmod 600` blinda vs `777` expone — cuatro karmas con dos verbos, ya jugables POR LA PUERTA y legibles en tres lenguajes (post-mortem texto, `stat`/`ls -l` metadato, insignia+lente color). La prosa `05-subestacion.md` ya promete esas bifurcaciones y la física+karma las cumplen sin drift.
- **La trilogía del testigo sigue cerrando 4 geografías:** Faro `join -v 1 … | grep TR-003` → 1 línea vs `No such file` + Subestación `cat /tmp/volcado-custodia.csv` → `TR-003|EN_COLA` vs `No such file` + `stat` → `Modify: 03:14:00 Size: 512` vs `cannot stat` + `ls -l` → `-rw-r--r--` vs `-rw-------` vs `777` + post-mortem `auditor_custodia` vs silencio + web `?chapter=5` custodia visible vs oculta + insignia verde/azul/ámbar + lente veredicto `⬥ Veredicto:` disjunto. Cinco geografías, una decisión.
- **El Faro como espejo reversible:** `join -v | grep 000483` vs `cut -f3 | grep 000483` — mismo dato, dos altitudes. `grep 000` (2) vs `grep 000483` (1) prueba de precisión; `cut -d','` coma-trampa intacta. Dato7 añade `volcado-rescate.csv` como tercera tabla del Faro, solo visible si trajiste el testigo (con `-v 1` el join nombra el huérfano). `grep -v sujeto` ya filtra el header como lo haría un sysadmin real.
- **Loop y Hub vivo:** `c.cut`/`c.scp`/`c.join`/`c.ps-forense`/`c.stat`/`c.chmod`/`c.grep -v` dominados con eco (`auditor_corte`/`auditor_join`/`auditor_orden` + `auditor_custodia` + `auditor_espejo` + `auditor_volcado` + `auditor_hup/kill` + `auditor_cierre/puerta_abierta` + `gris_eco`) — el eco ya no es pendiente (🧭9 cerrada). Inventario agregado multi-run sigue pendiente (🧭17) pero el espejo+Gris+volcado+cadena+díptico dan cuerpo a ch4.e2/e3+dato4/5/6/7+ch5.e2/e3/e4. La lente custodia web + lente veredicto le dicen «TR-003 custodiado — vigilante 03:14 verde» solo si el save trae `volcado: rescatado`; si no, el panel calla y la insignia pasa a ámbar tras -9 / azul tras HUP — el veterano no ve spoiler, ve consecuencia. El soporte `?chapter=5&seed=` ya es semilla compartible.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: EL DÍPTICO COMPLETO + GREP -V + VEREDICTO)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **801 passed / 0 failed** (gate `load_curriculum()` 25/31, `DEFAULT_CH5E1` 6 + `E3` 5 + `E4` 6, `DEFAULT_CH6_COMMANDS` 16 con `join`+`cut`, bundle 50 ficheros 473.3 KiB, `test_ch5_allowlist` verde, `test_bundle_fresco` verde). ✓
- **Prioridad 1 — EL DÍPTICO (chmod 600/777 + kill HUP/-9, 5 checks por la puerta):** `abrir_encargo` e1 `ls -l`→644, `chmod 600`→`auditor_cierre` azul + `-rw-------`, `chmod 777`/`-R 777`→`auditor_puerta_abierta` rojo, sin `ls -l` byte-idéntico, sin huellas cruzadas kill↔chmod. Pregunta de sabor P1: ¿cerrar vs exponer se SIENTE distinto? → SÍ, DECISIÓN: `cierre` blinda vs `puerta_abierta` expone — el mismo verbo pesa distinto tras mirar. ✓
- **Prioridad 2 — `grep -v`/`-i` HONESTO (6 checks):** `grep -v sujeto purgas.csv`→0 filtra header, `ps aux | grep -v root` vía `Shell(ps+grep)`→0, `-i`/`-vi`/`--` y `invalid option` exit 2 GNU-honesto, sin flags byte-idéntico cap.2. Pregunta de sabor P2: ¿filtro negativo se siente herramienta real? → SÍ, HERRAMIENTA: quitar header es gesto Unix, no atajo. ✓
- **Determinismo + web doble lente:** `generate(42,5,True)` byte-idéntico ×2, `generate(99,5,False)` ×2; `True≠False` difiere solo en custodia; kill HUP vs -9 difieren solo en huella post-mortem (mismo FS, mismo pid por seed). Web `?chapter=5` `#custodia-intruso` + `#custodia-postmortem` 3 estados, `node --check` OK, `CUSTODIA/TRONCAL_STATIC` byte-idénticas, consola limpia; caps 1-4 sin ensuciar. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23 cerradas**, **🧭24 cerrada con matiz pre-puebla P3**, **🧭25/26 PERSISTEN** (límite 2 pipes + `cut` en ch4), **🧭27 CERRADA 23/09 (grep -v honesto)**, **🧭28 cerrada**, **🧭29/30 CERRADOS**, **🧭31/32/33 CERRADOS**, **🧭34/35 CERRADOS**, **🧭36 CERRADA**, **🧭37 CERRADO**, **🧭38 CERRADO**, **🧭39 CERRADO**, **🧭40 CERRADO**, **🧭41 CERRADO**, **🧭42 CERRADO**, **🧭43 CERRADO**, **🧭44 CERRADO 23/09 (díptico chmod)**, **🧭45 OBSERVACIÓN P3** (calibración micro-karma N=8 a 20 runs), **🧭46 NUEVO P3** (allowlist E3 honesta + `chmod -R` exit 1). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — la zona 🔬 23/09 se ejecutó completa (díptico 600/777 + grep -v honesto + determinismo + doble lente) y el viaje del novato sigue APTO; el díptico queda SALDADO como DECISIÓN y el filtro como HERRAMIENTA.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*
## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
