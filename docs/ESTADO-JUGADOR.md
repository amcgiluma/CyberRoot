# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (22/09 — MODO B: Juicio del verbo kill + stat testigo + insignia 3 estados)

**¿Hay algo que jugar de principio a fin?** Sí — la cadena **cap. 4 `story.ch4.e3` «Lo que no avanza»** grey `c.scp` (`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `TR-003|EN_COLA` 512 bytes `03:14` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` + bifurcación `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → `volcado: rescatado` vs `rm`/`tick≥30` → `caducado`) + **cap. 6 `story.ch6.dato7` «El fantasma que pesa»** grey `c.join` (`volcado-rescate.csv` SOLO si rescate → `join -t'|' -1 1 -2 1 -v 1 volcado-rescate.csv purgas.csv | grep TR-003` → 1 línea `TR-003|faro|troncal-01|512|EN_COLA`; si caducado → `join: volcado-rescate.csv: No such file` exit 1) + **cap. 5 «Subestación» COMPLETO 4/4 CON JUICIO Y OJOS** por **`abrir_encargo(c,'story.ch5.e3',{'c.ps','c.env'},volcado True)`** con `SUPPORTED_CHAPTERS {0,2,4,5}` y `_commands_for(5,quest_id)` per-encargo → `build_chapter5_fs(volcado_rescatado)` → `/tmp/volcado-custodia.csv` `TR-003|faro|troncal-01|512|EN_COLA` EXISTE solo si `volcado: rescatado`; si caducaste → `cat` → exit 1 `No such file` en LOS 4 + proceso `censo 424/421 intruso --vigilar-censo START 03:14` (seed 42→424, 99→421) patrulla igual en ambos mundos. **PUERTA CABLEADA 21/09 PR #69:** `session.py _commands_for(5,quest_id)` ramifica a `DEFAULT_CH5E1/E3/E4` (e1 `ls,ps,chmod,kill+cat,scp` / e3 `ps,env,kill+cat,scp` / e4 `chmod,chown,tail,ls+cat,scp`) — **frontera 127 honesta**, `ps aux` POR LA PUERTA → exit 0 con `censo 424 intruso --vigilar-censo START 03:14` (seed 99→421). **JUICIO 21/09 PR #69:** `kill -HUP <pid>` → `HUP_<pid>=1` + `ps` con `--reloaded` + post-mortem `auditor_hup: «señal de reconfiguración registrada»` + karma azul; `kill -9 <pid>` → intruso desaparece del `ps` + `auditor_kill: «proceso de vigilancia eliminado»` + karma rojo; sin kill → byte-idéntico sin hup/kill; e1/e4 sin falsa detección. **OJOS 21/09 PR #70:** `stat /tmp/volcado-custodia.csv` → `Modify: 03:14:00` + `Size: 512` si rescate, `cannot stat … No such file` si caducado; `c.stat` hallazgo prereq `c.ls` cap.1 cap.1, fuera de ch5 allowlist →127 honesto. **INSIGNIA 21/09 PR #71:** `?chapter=5` `#custodia-intruso` 3 estados — VERDE (`intruso --vigilar-censo START 03:14` vivo), AZUL (`--reloaded` tras HUP), ÁMBAR (silenciado tras -9), consola limpia.

**En main (788 passed / 0 failed, gate 25 conceptos / 31 quests, bundle 50 ficheros 465.8 KiB regenerado canónicamente, guardián verde):**
- **JUICIO + CABLEADO (O1 PR #69):** `session.py` importa `DEFAULT_CH5E1/E3/E4_COMMANDS` con ramificación CH5 per-encargo, `postmortem.py` `LINE_KEY_HUP/KILL` + `_detect_vigilante` (HUP_* + vigilante presente → hup/reloaded azul vs vigilante ausente + kill de muerte → kill rojo), `textos.json` `postmortem.auditor.hup/kill` prefijo disjunto, `test_ch5_per_encargo` 5 + `test_postmortem_hup_kill` 5, suite 774→784+4+0→788 tras regen 50 ficheros.
- **OJOS (S1 PR #70, 21/09):** `src/core/sandbox/commands/stat.py` handler `Modify: 03:14:00` + `Size: 512`, `curriculum.json` `c.stat` hallazgo prereq `c.ls`, `textos.json` `concept.stat.summary`/`help.stat`, gate 24→25, `test_stat` 4 + gates flex 25/31, bundle 50.
- **INSIGNIA (T1 PR #71):** `web/app.js` `_getIntrusoStatus()` (ps+env → verde/azul/ámbar) + `_intrusoBadgeHtml` + `web/index.html` `#custodia-intruso`, `node --check` OK, `CUSTODIA_STATIC` byte-idéntica, consola limpia `?chapter=5` en 3 estados.
- **Smoke:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **788 passed** (gate 25/31, bundle 50 ficheros, `test_ch5_allowlist` verde, `test_bundle_fresco` verde, `DEFAULT_CH5E3_COMMANDS` 5/5 vía session).

**Para «jugable de principio a fin» sigue faltando:** **inventario agregado multi-run** (🧭17), **salas narrativas Faro E4+** y **karma agregado N=8 ventana larga** (hoy solo micro-karma HUP/KILL por run). Nada rompe el camino principal abrible/testigo/juicio/lente.

**CICLO (línea de Oscar):** verde — la zona 🔬 22/09 se ejecutó COMPLETA desde save limpio (kill HUP/-9 con karma + stat testigo + insignia 3 estados + determinismo 788/0); el camino del novato es APTO y la promesa de E3 por la puerta queda SALDADA. Sin matiz ámbar.

## 🏃 Run de referencia (save limpio) — 22/09

*Nueva partida sobre `abrir_encargo` real + `generate` determinista + web lente; MODO B headless sobre zona 🔬 22/09 Gwyn → Oscar (primero).*

**Veredicto: APTO — el juicio es DECISIÓN, los ojos son METADATO y la insignia ANUNCIA sin spoilear.**

1. **Prioridad 1 — EL JUICIO DEL VERBO KILL (PR #69): 5/5 checks verdes por la puerta normal:**
   - `listar_encargos(cur,5, knowledge={c.ps,c.env})` → e3 `abrible True` (missing `c.env` sin él → `missing [c.env]` honesto). `abrir_encargo(c,'story.ch5.e3',{'c.ps','c.env'},volcado True, run_seed 42)` → `abrible True` + `session` seed `story.ch5.e3:42`. ✔
   - **(a) `ps aux` → exit 0 con intruso vivo:** `ps aux` → `censo 424 intruso --vigilar-censo START 03:14` (seed 42; seed 99 → 421, mismo `03:14`, `USER censo` invariante; fallback handmade 522 en tests forma `<=`). `censo` no `ceniza`, `START 03:14` no `Aug25` — el testigo tiene hora y firma. ✔
   - **(b) `kill -HUP <pid>` → reconfigura azul:** `kill -HUP 424` → exit 0; `ps aux` de nuevo → `censo 424 … intruso --vigilar-censo --reloaded` + `env HUP_424=1`; `build_postmortem(sh.to_dict(), {noise_budget:12})` → `auditor_hup: «señal de reconfiguración registrada — proceso de vigilancia reconfigurado. Continuidad del ensayo: estable.»` + `karma {delta:1, tint:blue}` + `micro_karma {blue:1}` + `lines_resolved` gana segunda línea. ✔
   - **(c) Run limpia aparte `kill -9` → ejecuta rojo:** `abrir_encargo` seed 99 → `ps aux` 421 vivo → `kill -9 421` → exit 0; `ps aux` → sin `421` ni `intruso` (solo `root 1 /sbin/init`); post-mortem → `auditor_kill: «proceso de vigilancia eliminado — el testigo queda sin ojos. Continuidad del ensayo: estable.»` + `karma {delta:1, tint:red}`. ✔
   - **(d) Run SIN kill → byte-idéntico sin huella:** `abrir_encargo` seed 42 sin kill → post-mortem SIN `auditor_hup`/`auditor_kill`/`karma` (7 claves vs 11 con HUP, byte-idéntico ×2 runs sin kill). No hay karma gratis por mirar. ✔
   - **(e) e1/e4 sin falsa detección:** `abrir_encargo(c,'story.ch5.e1',{'c.ls-la','c.cat','c.chmod'})` y `e4({'c.chmod','c.chown','c.cat','c.grep'})` por la puerta → `build_postmortem` SIN `auditor_hup/kill` aunque compartan `kill` en allowlist — el detector exige `HUP_*` o ausencia del vigilante con `kill` de muerte, no cualquier `kill`. ✔
   - **Pregunta de sabor P1 (¿reconfigurar vs eliminar se SIENTE distinto?):** SÍ, DECISIÓN: el expediente dice `reconfigurado` (proceso vive con `--reloaded`, señal 1) vs `eliminado` (proceso ausente, el testigo queda sin ojos). Mismo verbo `kill`, dos frases que pesan distinto — azul no es venial, rojo no es épico, es factura.

2. **Prioridad 2 — `stat`: OJOS DEL TESTIGO + insignia web 3 estados (PRs #70/#71):**
   - **(a) `stat /tmp/volcado-custodia.csv` lector del testigo:** con `volcado_rescatado=True` → `Shell(fs, commands=('stat','cat')).execute('stat /tmp/volcado-custodia.csv')` → exit 0, `File: /tmp/volcado-custodia.csv`, `Size: 512  Blocks: 8`, `Modify: 2025-09-21 03:14:00.000000000 +0000` (misma `03:14` del `ps START` + badge web `512`); con `volcado_rescatado=False` → exit 1 `stat: cannot stat '/tmp/volcado-custodia.csv': No such file or directory` (misma semántica que `cat` y `join` sin rescate — tres verbos, un silencio). `stat` vía `abrir_encargo` e3 (allowlist CH5 5 sin stat) → 127 honesto `command not found` — frontera respetada, no fuga. ✔
   - **(b) Web `?chapter=5` insignia `#custodia-intruso` 3 estados:** `web/app.js` `_getIntrusoStatus()` lee `get_ps()`/`get_env()` ya expuestos (verde: intruso vivo `censo 424 --vigilar-censo START 03:14`; azul: `HUP_424=1` + `--reloaded`; ámbar: ni HUP ni intruso → `silenciado`); `_intrusoBadgeHtml` pinta `● vigilante 03:14` verde #2ecc71 / `● reconfigurado HUP_424` azul #5dade2 / `● silenciado` ámbar #f39c12. `web/index.html` `#custodia-intruso` fuera del panel custodia (siempre visible en ch5, no se oculta con tabla). Consola limpia en 3 mocks sin throw (`node --check` OK, `TRONCAL_STATIC` 3 intacta, `CUSTODIA_STATIC` byte-idéntica). `hideIntrusoBadge` en `restartSameSeed` limpia. ✔
   - **(c) `c.stat` como hallazgo (prereq `c.ls`):** `c.stat` prereqs `('c.ls',)` chapter 1 — el concepto se enseñó en cap.1 (hallazgo) y hoy tiene uso diegético en cap.5 (el testigo se pregunta por el fichero, no solo por el reloj). Gate 25/31 coherente (campaña+cap.5). ✔
   - **Pregunta de sabor P2 (¿la insignia ANUNCIA o SPOILEA?):** ANUNCIA: la lente da estado (verde/azul/ámbar) antes del veredicto; el veredicto es del post-mortem (`auditor_hup/kill` + karma). Sin `kill` la insignia es verde y el post-mortem calla — mismo circuito en tres lenguajes (post-mortem texto, metadato `stat`, color insignia) sin contradecirse.

3. **Smoke + determinismo (exigencia de la zona):**
   - `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **788 passed / 0 failed** (gate `load_curriculum()` 25/31, `DEFAULT_CH5E1` 6 / `E3` 5 / `E4` 6 / `DEFAULT_CH6_COMMANDS` 16, `test_bundle_fresco` verde bundle 50). ✔
   - Determinismo: `generate(42,5,True)` byte-idéntico ×2 (fs.to_dict idéntico), `generate(99,5,False)` ×2 byte-idéntico; con kill `-HUP` vs `-9` las historias DIFIEREN solo en la huella del post-mortem (`auditor_hup` vs `auditor_kill`) — mismo FS, mismo pid por seed (424 vs 421). `generate(42,5,True)` vs `False` difiere solo en `/tmp/volcado-custodia.csv` (presente vs ausente). ✔
   - `c.stat` frontera 127 honesta fuera de ch5, `c.ps`/`c.kill` por puerta e3 exit 0 (ya no 127).

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 del Faro con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA con matiz (doc drift menor, decisión Gwyn 12/09: MANTENER pre-puebla):** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127. `abrir_encargo`/`new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo «léelo en /etc/hosts» como didáctico, pre-puebla lo hace redundante. No es bug (788/0), solo P3.
**5. 🧭25 — PERSISTE (observación): límite 2 pipes (3 cmds) + redirección no soportada.** `cut|grep TR-` 1 pipe OK, `cut|grep|sort` con `sort`→127 en ch4 no bloquea; ch4.e2/e3 diseñan en 1 pipe evitando límite.
**6. 🧭26 — PERSISTE (dirección menor): `c.cut` vive en cap. 4, Faro e1 no es primer `cut`.** e1 `grep|wc`, dato2/e2 exigen `cut` por necesidad. Correcto.
**7. 🧭27 — PERSISTE (fricción menor, decisión Gwyn 11/09: filtro positivo): `grep -v` vía pipe NO soportado.** `join|grep -v sujeto` → exit 2. FICHA dato4/dato6 y ch4.e2/e3 usan filtro positivo — Gwyn decidió NO implementar `-v`.
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
**24. 🧭44 — CERRADO 21/09 (cableado `session._commands_for` cap. 5 + karma HUP/KILL):** la puerta ahora entrega `ps/env/kill` por la puerta normal (`abrir_encargo` e3 → `ps aux` 0 con 424/421), y el mismo verbo pesa karma azul/rojo. Propuesta Manus 21/09 CONSUMIDA en PR #69 (engine), validada 22/09 por HUP azul vs -9 rojo + stat + insignia. Sin lunar.
**25. 🧭45 — NUEVO 22/09 — OBSERVACIÓN P3 (veterano 30+ runs, no bug):** el micro-karma `HUP/KILL` (1 punto tint) hoy pesa 1 por run sobre la ventana N=8 del DESIGN §3.4 (últimas 8 entradas). El veterano que repite `kill -HUP` en 4 runs seguidas ve su `K` subir sin que el Hub lo grite — el mundo ya reacciona (stock de Gris, tono del Auditor) pero la contabilidad N=8 aún no tiene métrica headless de contraste (§8.6) medida. No es rotura (788/0, 3 lenguajes coherentes), es calibración futura: Gwyndolin/Ornstein pueden medir con harness qué hace falta de contraste kármico real tras 20 runs HUP vs 20 runs -9. Dejar como recámara P3, no como [BUG].

## 👴 Progreso de veterano (20+ h → la run 30)

- **La Subestación como juicio con memoria:** el veterano ya domina `c.cat`/`c.scp` (cap.4) + `c.join`/`c.cut` (cap.6) + `c.ps`/`c.kill`/`c.stat`. En la run 29 hizo `scp` rescate y `kill -HUP 424` (azul, `--reloaded`); en la 30 `rm` disolución y `kill -9 421` (rojo, silenciado). Ambas le dieron `abrible True` en los 4 pero `cat` diametralmente opuesto (0 con `TR-003|EN_COLA` vs 1 `No such file`) y post-mortem con/sin `auditor_custodia` + `auditor_hup` azul vs `auditor_kill` rojo. Hoy puede abrir E1 con `c.ls-la/c.cat/c.chmod`, E3 con `c.ps/c.env`, E4 con `c.chmod/c.chown/c.cat/c.grep` — los 3 con testigo condicional; el `ps aux` del intruso `censo 424 --vigilar-censo START 03:14` (seed 99→421) es su brújula y `stat` su lupa (Modify 03:14, Size 512). Sabe que `kill -HUP` reconfigura (proceso vive, `HUP_424=1`) vs `kill -9` ejecuta (proceso muere) — dos karmas con el mismo verbo, ya jugables POR LA PUERTA y legibles en tres lenguajes (post-mortem texto, `stat` metadato, insignia color). La prosa `05-subestacion.md` ya promete esas bifurcaciones y la física+karma las cumplen sin drift.
- **La trilogía del testigo sigue cerrando 4 geografías:** Faro `join -v 1 … | grep TR-003` → 1 línea vs `No such file` + Subestación `cat /tmp/volcado-custodia.csv` → `TR-003|EN_COLA` vs `No such file` + `stat` → `Modify: 03:14:00 Size: 512` vs `cannot stat` + post-mortem `auditor_custodia` vs silencio + web `?chapter=5` custodia visible vs oculta + insignia verde/azul/ámbar. Cinco geografías, una decisión. El veterano que vuelve con `?chapter=5&seed=99` ve el mismo `START 03:14` con pid 421 — la hora no miente aunque el pid baile. `volcado_del_save(postmortem)` le deja reusar `rescatado/caducado` sin brujería.
- **El Faro como espejo reversible:** `join -v | grep 000483` vs `cut -f3 | grep 000483` — mismo dato, dos altitudes. `grep 000` (2) vs `grep 000483` (1) prueba de precisión; `cut -d','` coma-trampa intacta. Dato7 añade `volcado-rescate.csv` como tercera tabla del Faro, solo visible si trajiste el testigo (con `-v 1` el join nombra el huérfano).
- **Loop y Hub vivo:** `c.cut`/`c.scp`/`c.join`/`c.ps-forense`/`c.stat` dominados con eco (`auditor_corte`/`auditor_join`/`auditor_orden` + `auditor_custodia` + `auditor_espejo` + `auditor_volcado` + `auditor_hup/kill` + `gris_eco`) — el eco ya no es pendiente (🧭9 cerrada). Inventario agregado multi-run sigue pendiente (🧭17) pero el espejo+Gris+volcado+cadena+juicio dan cuerpo a ch4.e2/e3+dato4/5/6/7+ch5.e2/e3/e4. La lente custodia web + insignia le dicen «TR-003 custodiado — vigilante 03:14 verde» solo si el save trae `volcado: rescatado`; si no, el panel calla y la insignia pasa a ámbar tras -9 / azul tras HUP — el veterano no ve spoiler, ve consecuencia. El soporte `?chapter=5&seed=` ya es semilla compartible (semilla del veterano como enlace).

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: EL JUICIO DEL VERBO KILL + stat + insignia 3 estados COMPLETA)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **788 passed / 0 failed** (gate `load_curriculum()` 25/31, `DEFAULT_CH5E1` 6 + `E3` 5 + `E4` 6, `DEFAULT_CH6_COMMANDS` 16 con `join`+`cut`, bundle 50 ficheros 465.8 KiB, `test_ch5_allowlist` verde, `test_bundle_fresco` verde). ✓
- **Prioridad 1 — EL JUICIO (HUP azul vs -9 rojo, 5 checks por la puerta):** `abrir_encargo` e3 `ps aux`→0 con `censo 424 intruso --vigilar-censo START 03:14` (42→424, 99→421); `kill -HUP 424`→`HUP_424=1` + `ps --reloaded` + post-mortem `auditor_hup` + karma azul; `kill -9 421`→intruso desaparece + `auditor_kill` + karma rojo; sin kill byte-idéntico 7 claves vs 11 con HUP; e1/e4 sin falsa detección. Pregunta de sabor P1: ¿reconfigurar vs eliminar se SIENTE distinto? → SÍ, DECISIÓN: `reconfigurado` (vive con --reloaded) vs `eliminado` (sin ojos) — el mismo verbo pesa distinto. ✓
- **Prioridad 2 — `stat` OJOS + insignia 3 estados:** `Shell(fs, commands=('stat','cat'))` `stat /tmp/volcado-custodia.csv` → `Modify: 03:14:00 Size: 512` si rescate vs `cannot stat … No such file` si caducado; vía `abrir_encargo` e3 →127 honesto (frontera). Web `?chapter=5` `#custodia-intruso` verde (vigilante 424 START 03:14) / azul (HUP_424 --reloaded) / ámbar (silenciado) + consola limpia 3 estados; `c.stat` prereq `c.ls` chapter 1. Pregunta de sabor P2: ¿insignia ANUNCIA o SPOILEA? → ANUNCIA: da estado, no veredicto — el veredicto es del post-mortem. ✓
- **Determinismo:** `generate(42,5,True)` byte-idéntico ×2, `generate(99,5,False)` ×2; `True≠False` difiere solo en custodia; kill HUP vs -9 difieren solo en huella post-mortem (mismo FS, mismo pid por seed). ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23 cerradas**, **🧭24 cerrada con matiz pre-puebla P3**, **🧭25/26/27 PERSISTEN** (límite 2 pipes + `cut` en ch4 + `grep -v` filtro positivo), **🧭28 cerrada**, **🧭29/30 CERRADAS**, **🧭31/32/33 CERRADOS**, **🧭34/35 CERRADOS**, **🧭36 CERRADA**, **🧭37 CERRADO**, **🧭38 CERRADO**, **🧭39 CERRADO**, **🧭40 CERRADO**, **🧭41 CERRADO**, **🧭42 CERRADO**, **🧭43 CERRADO**, **🧭44 CERRADO 21/09 (cableado+karma por la puerta)**, **🧭45 NUEVO P3** (calibración micro-karma N=8 a 20+ runs). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — la zona 🔬 22/09 se ejecutó completa (juicio HUP/-9 + stat + insignia 3 estados + determinismo) y el viaje del novato sigue APTO; la promesa de E3 por la puerta queda SALDADA y el veterano ve el juicio en tres lenguajes.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*
## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
