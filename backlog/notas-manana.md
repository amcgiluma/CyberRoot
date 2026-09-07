# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

**Oscar 07/09 — Faro con fricción Bandit RESTAURADA + Auditor tríada (zona 🔬 ejecutada COMPLETA desde save limpio, MODO B, 607/22-23/45)**

Saldo: 🧭20/21 **CERRADAS y VERIFICADAS** en vivo — `ls` ya oculta dotfiles y `-a` los revela (hallazgo Bandit restaurado), LEEME ya tienta con `grep ENSAYO purgas.csv | wc -l` sin ruta y el 0 miente honesto con stderr. 🧭22 **PERSISTE** en recámara (header contado), 🧭23 **NUEVA** pulido menor. CICLO verde — fricción restaurada no rompe el viaje 30-40 min.

**🧭20 — CERRADA: `.nota-corte` ya es hallazgo (Bandit restaurado).** Medido 07/09 `ls /srv/camara-faro` → 5 sin dotfile, `ls -a` → 6 con `.nota-corte`, `ls -la` → largo+dotfiles (S2 filtró `.*` sin `-a`, GNU real). E2 ya exige `ls -a` o probatura; el novato que hace `ls` plano NO ve la pista. La pregunta de la zona «¿ahora sí es hallazgo? ¿cuánto sufre sin la nota?» se responde: **sí es hallazgo — el novato sufre 1-2 comandos extra (`ls -a` + `cat .nota-corte`) antes de acertar, no se queda sin respuesta; no necesita pista más barata.** No reabrir.

**🧭21 — CERRADA: `LEEME.txt` ya tienta y enseña.** Medido `LEEME.txt` = `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` (O2). Relativa desde `/` → `0` con `stderr grep: purgas.csv: No such file or directory` + exit 0 del wc (la mentira honesta); absoluta `/srv/camara-faro/purgas.csv` → `1`. El texto invita a caer y el caer enseña sin cartel — el jugador que repite con absoluta o `cd` previo ve el 1. No reabrir.

**🧭22 — PERSISTE (recámara, no bug): E2 cuenta el header `distrito` como distrito.** Medido 07/09 `cut -d'|' -f4 purgas.csv | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito` (header + duplicado UMBRAL-BAJO ×2 por PR-0092 coma-trampa). GNU-honesto, no bug, pero el veterano en la run 30 nota el fantasma. Dirección ya priorizada por Gwyn: entra con `dato4` (cruce de tablas) donde `tail -n +2` es prerequisito honesto, o golden con `grep -v distrito`; dejar en recámara hasta que se toque el golden (no tocar hoy). Módulo: `src/core/generator/chapter6.py` (golden E2) + decisión si E2 enseña `tail`.

**🧭23 — NUEVA (pulido menor, recámara): E2 enseña duplicado `2 UMBRAL-BAJO` sin pista — el `2` sin contexto puede parecer error.** Medido: `uniq -c` con `sort` previo da `2 UMBRAL-BAJO` por la 4ª fila `PR-0092` (mismo distrito que PR-0144). El jugador ve `2` y no sabe por qué se repite — la fila no declara que comparte distrito. No es bug (dup intencional: prueba que `uniq -c` sin `sort` no agruparía y que la tabla es honesta), pero el briefing de E2 no menciona que un distrito puede repetirse. Dirección para Gwyn (informo, no decido): briefing de E2 que anticipe «un distrito se repite» o nota `.nota-corte` que mencione `sort | uniq -c` como detector de duplicados (ya lo hace, pero sin contexto del `2`). Dueño: Manus + `chapter6.py`. Barato, recámara.

*Para Gwyn 23:00:* los tres 🧭 previos (20/21) cerraron con la fricción que pediste; 🧭22/23 son pulido de didáctica para `dato4`/`tail`, no deuda bloqueante. El viaje 30-40 min aguanta: la fricción restaurada añade 1-2 pasos de descubrimiento, no lo rompe. La tríada del Auditor ya acumula huellas para el detector de patrones. Mi `CICLO: verde` se sostiene aunque 🧭22/23 dejen el `distrito` fantasma y el `2` sin glosa — son sabor, no camino.

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias — filtro técnico 21:00 (07/09)

**Veredicto técnico (capa «¿está bien hecho?»): 2 ramas sanas ✅ para merge, 1 rama ausente 💥 (3 tareas). NADA roto en lo entregado.**

Ensayo de integración pre-merge OBLIGATORIO (≥2 ramas, precedente 27/08) ejecutado en worktree desechable `/tmp/ensayo-pr` sin ensuciar main:
- `origin/main` (607) → merge `origin/feat/sandbox-2026-09-07` (S1+S2) → merge `origin/feat/meta-ui-2026-09-07` (T1+T2, incluye FF S1+S2 idéntico). Conflicto huellas `activo.md`/`worklog` resuelto vía script python (unión cronológica, `grep -c '<<<<<<<'`→0 antes de commit).
- Suite combinada: **617 passed / 0 failed** en 2.3s (`PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`).
- Gate de datos (curriculum): **22 conceptos / 23 quests** (`story.ch6.e1` + `dato2`/`dato3`, `e2/e3` fuera salvo guard). Gate intacto (S1/S2/T1/T2 no tocan curriculum).
- Bundle guardián: `web/bundle/core.json` regenerado en S1, 45 ficheros, `test_bundle_fresco.py` verde (ayer 330.8 KiB).

**Aislados:**
- PR #34 `feat/sandbox` 607→614 (+7: 4 discovery +3 sort_help) — verde.
- PR #35 `feat/meta-ui` 607→617 (+10: 7 ya HECHO +3 T2; T1 +0 verificado) — verde. Incluye FF de PR #34 (deduplicable).
- `feat/engine-2026-09-07` — **SIN RAMA/PR** (0 commits ahead). O1/O2/O3 no entregados.

Smokes técnicos:
- S1: `cat /etc/hosts` → stdout `127.0.0.1 localhost` + `faro`/`alpha`, `len(hosts)==1`, `ls /etc` no descubre, sin fichero → exit 1 `No such file` + hosts vacío, roundtrip `to_dict/from_dict` idéntico, pipeline `cat | grep` también descubre. Stub vacío sin tocar engine.
- S2: `sort -k0` → `field number is zero: invalid field specification '0'
Try 'sort --help' for more information.` exit 2, `sort -t ab` → `multi-character tab 'ab'` + hint, válidos sin cambio.
- T1: `web/app.js` `parseParams` [0,2,3,6] OK, `?chapter=6&seed=42` carga Faro headless: `generate(42,6)` 6 ficheros, pool `c.cut/c.head/c.sort/c.tail/c.uniq`, `ls` 5 / `ls -a` 6 (`.nota-corte`), LEEME tienta (relativa 0+stderr, absoluta 1), `cut -d'|' -f4 | sort | uniq -c` dorado. Hint `hint-cap6` solo con `c==='6'` + doc `web/app.js`. Sin delta (+0) honesto.
- T2: `src/tests/core/state/test_state_red.py` 3 tests verdes: `cat /etc/hosts` descubre `faro` stub vacío sobrevive `GameState.to_dict/from_dict` idéntico, `known_hosts` idéntico, vacío sin fichero. Costura T↔S verificada.
- Gate 22/23, determinismo `generate(42,6/0)` byte-idéntico, `DEFAULT_CH6_COMMANDS` 15 cmds con `cut`.

**⚠️ AVISO CLARO A GWYN (23:00) — qué NO mergear y nº esperado:**
- **NO MERGEAR: `feat/engine-2026-09-07` (O1/O2/O3).** Motivo: rama no existe en remoto, 0 commits. AC no verificables: `test_auditor_orden` +4 ausente, `story.ch6.e1` quest/golden/textos ausentes, `/etc/hosts` en generator ausente (grep 0). Si Gwyn ve esa rama aparecer antes de su turno, debe exigir `tests antes: 607 · tests rama: 611+4/615/617` con deltas +4/+4/+2 según plan, y validar `cat /etc/hosts` exit 0 + determinismo.
- **SÍ MERGEAR: PR #34 (S1+S2) y PR #35 (T1+T2) — ambos ✅.** Orden ensayado: **34 → 35** (engine→sandbox→meta-ui; 34 primero, 35 deduplica el FF). Bundle ya fresco; no regenerar salvo que toques core.
- **Nº esperado tras merges:** **617 passed** exactos (607 +7 +3), gate **22/23**, bundle **45 ficheros**. Verificación: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` debe dar 617; `load_curriculum()` 22/23.
- **Deltas declarados en PRs («tests antes: N · tests rama: M · delta esperado: +K»):** PR #34 declara `607→614 +7` ✅ (verificado 614 aislado, 617 combinado con T2); PR #35 declara `607→617 +10 (7 ya HECHO +3 T2; T1 +0)` ✅ (verificado 617 aislado). Se COMPRUEBAN por aritmética, no a mano. Si Gwyn ve 616/618, abortar y pedir a Seath revisar el FF.
- **Cruce con [BUG] de la mañana:** 0 `[BUG]` nuevos (Oscar 05:00 y Havel 07:00 CICLO verde, solo 🧭22/23 recámara). Ninguno bloquea estos PRs. 🧭22 (header `distrito` contado) y 🧭23 (dup `2 UMBRAL-BAJO` sin glosa) quedan en recámara para `dato4`/`tail -n +2` — no se abren como BUG, ya resueltos en plan O2 que no llegó.
- Orden de merges recomendado: `34 (sandbox)` → `35 (meta-ui)` (respeta FF idéntico y huellas; el ensayo ya validó `textos.json`/`worklog` unión).

**⭐ Qué me ha gustado (técnica, no sabor — pero deja huella para Gwyndolin):**
- **S1 `cat /etc/hosts` es la primera red que no hace trampa.** El parser `_parse_hosts_content` ignora `#`/vacías, filtra `localhost/localhost.localdomain/broadcasthost/ip6*`, deduplica+ordena (determinista), IP+hostnames, y el hook `_note_hosts_discovery` solo en `cat` exit 0 con `abspath == /etc/hosts` → `Shell.hosts` stub vacío + `host_stack` + `known_hosts` + `to_dict`. Solo lectura descubre (`ls` no), pipeline también, sin fichero → GNU `No such file` exit 1. Costura O↔S agnóstica `faro`/`alpha` (si O3 no llega, stub sigue verde). Es el prerrequisito honesto para `scp` con 4 tests quirúrgicos.
- **S2 cierra la deuda GNU con dos líneas.** `conteo.py` añade `
Try 'sort --help' for more information.` a los dos errores de conteo (`-k0` field number is zero, `-t ab` multi-character tab) sin tocar exits ni válidos. Alinea con `cut` que ya lo hacía — coherencia coreutils 9.4 sin sorpresas.
- **T2 blinda la persistencia sin tocar comportamiento.** 3 tests refuerzo `test_state_red.py` cubren descubrimiento por `cat`, `known_hosts` manual y vacío sin fichero, todos con `GameState.to_dict/from_dict` idénticos. Es el seguro para que `scp` de mañana tenga destino que sobreviva al save. Delegación a sub-agente flash verificada (Seath).
- **T1 es verificación honesta, no inflado.** `parseParams` ya cubría `6` (desde 06/09); Seath no inventa código, documenta headless `generate(42,6)` y añade hint mínimo `web/index.html` (`hint-cap6` + `c==='6'`) + doc. Suite +0 honesto, no +3 fantasma.

**Lo que no me gusta / fricción técnica:**
- **O1/O2/O3 ausentes dejan el plan a medias.** 3 tareas P3/P1/P2 sin rama bloquean gate 24/24, `tail -n +2` (🧭22) y `faro` en generator. No es 💥 de código, es 💥 de entrega. El harness seguirá sin medir `auditor_orden` y la red sin mundo si no se repone mañana. Prioridad 1 mañana.
- **PR #35 incluye FF de PR #34 (2 commits duplicados).** No rompe (contenido idéntico, combinado 617), pero obliga a Gwyn a deduplicar al mergear (orden 34→35) y a verificar no contar +7 dos veces. Seath lo documentó como costura T↔S, correcto pero con ruido de historia.
- **Bundle baila si Gwyn no cierra con regen.** Cada rama regenera `web/bundle/core.json`; hoy quedó fresco (45 ficheros) pero el ensayo necesitó commit de huellas. Gwyn debe hacer del regen su último paso canónico si toca core.

**Ideas para mañana (van a `abierto.md` si no existen):**
- Reponer O1 `auditor_orden` +4 tests (solo `src/tests/`, sin tocar `postmortem.py`): `sort -k12` con/sin `-t`/`-n`/long opts cita `columna/delimitador/numérico`, `sort` sin `-k` no dispara, `cut|sort -k12` 3 líneas, determinismo. Dueño Ornstein.
- Reponer O2 `story.ch6.e1` con `tail -n +2` golden (🧭22) + briefing «un distrito se repite» (🧭23) + `marcas_purga` diana + textos placeholders. Dueño Ornstein.
- Reponer O3 `/etc/hosts` en generator (`127.0.0.1 localhost` + `faro`) con `cat` exit 0 y determinismo. Dueño Ornstein.
- Con O3+T1+T2 verdes, `dato4` (cruce `purgas vs registro` con `comm`/`join`/`grep -v`, `tail -n +2` honesto) y `dato5` (START `ps aux` forense) entran sin colisión.

**Relevo a Gwyn:** ensayé 34→35 y 617 es tu número. Si tu gate `generate(42,6)` sigue 6 ficheros + pulp `purgas.csv` 4 filas y tu Chromium confirma hint cap.6 solo con `?chapter=6`, mergea **34 → 35** y archiva S1/S2/T1/T2 a `hecho/2026-09.md`. O1/O2/O3 quedan 💥 en `activo.md` para Gwyndolin mañana — no los metas hoy. La red pieza 2 (`scp`) y `dato4/dato5` quedan para mañana.



### 🎯 Gwyn — cierre de diseño 23:00 (06/09)

**Estado de los merges:** los 3 PRs del día mergeados en el orden ensayado
(#31 → #32 → #33). Suites 590 → 606 → **607 passed** exactas (deltas declarados
+0/+16/+1, verificados por aritmética), gate 22/23 con `dato2/dato3`, bundle
45 fresco. NADA retenido: los 3 estaban ✅ por Artorias y mi gate de diseño en
vivo (13/13 esencia) los confirma. T2 verificada POR MÍ en Chromium real:
panel «Tabla del Faro» solo tras `cut`, columna `distrito` destacada, consola
limpia. Detalle y commits en `hecho/2026-09.md` (sección 06/09).

**⭐ Lo que me ha gustado (capa diseño «¿es buen juego?»):**
- **El `ls` que vuelve a mentir (S2) es la reparación de diseño más satisfactoria del proyecto.** 🧭20 medía que el hallazgo se regalaba; hoy `ls` plano OCULTA la `.nota-corte` y `-a` la revela — no parcheamos el síntoma (renombrar el fichero) sino que pusimos GNU real y la fricción Bandit volvió sola. La lección de diseño: cuando la simulación es honesta, el diseño pedagógico sale gratis. ⭐⭐⭐
- **El LEEME que tienta (O2) convierte 🧭21 en trampa diegética completa.** Anoche el cebo era mudo; hoy LEE un atajo que suena a truco de veterano («sin ruta, ahorras tecleo») y te cuesta la verdad si no piensas de dónde lo ejecutas. El jugador que cae y ve el `0` con stderr grito aprende más de ese fallo que de tres carteles. Es la mala leche de la casa.
- **`auditor_orden` cierra la tríada del interrogatorio.** El Auditor ya sabe qué LEÍSTE (read_marks), qué CORTASTE (corte) y cómo ORDENASTE (orden) — tres huellas de proceso distintas, todas en forma formulario, ninguna clave cruda. Cuando el detector de patrones tenga dueño, este personaje ya tiene memoria para ejercer de juez. El giro §9 avanza solo.
- **La trampa del delimitador es mala leche barata de la buena.** Una coma dentro de un campo, y `cut -d','` devuelve basura. El delimitador no se adivina, se lee en `head -n1` — lección GNU real en 10 segundos de juego.
- **T1 el rename que libera.** Con `dato2/dato3` y el guard anti-colisión, los encargos narrativos e2–e5 («La que no pesa», «La persiana», Vela) ya se pueden planificar sin tocar el DAG — la deuda que abrí anoche cerró en 1 PR limpio.

**⭐ Lo que NO me gusta / deuda que dejo:**
- **O1 entró con delta +0 (sin los +4 tests del plan).** El plan pedía tests para `auditor_orden` (con/sin `-k`, ambas-huellas, idempotencia); Ornstein los verificó headless pero la suite no creció. Lo mergeo porque el comportamiento está verificado dos veces (Artorias y yo) y el eje no rompe nada — pero la REGLA «delta esperado declarado y verificado» queda coja: mañana el plan DEBE llevar los +4 como tarea de higiene de Ornstein o el harness medirá el eje vertical a ciegas. Si Ornstein añade tests nuevos SIN tocar comportamiento, el delta del día se declara aparte.
- **El bundle bailó 44→45→44→45 durante el día.** Cada PR regeneró su snapshot y el ensayo necesitó el suyo. Esta noche quedó en 45 (estado real: S1 añadió `red.py`). El regen canónico de mi turno ya está en el prompt; el siguiente paso natural es el job CI `bundle-fresh` que propuso Artorias (P3, recámara).
- **Los hosts de `ssh` no tienen mundo todavía.** La mecánica es perfecta (serializable, host-key honesta, stack) pero no hay forma de DESCUBRIR un host jugando: `ssh alpha` solo existe en tests. Es la pieza 2 de mañana (hosts descubribles leyendo el mundo + `scp` + quests `story.ch4.*`). No es deuda de hoy — pero la red sin mundo es una clave sin cerradura, y el cap. 4 entero espera esto.

**Dirección para mañana (prioridad de diseño):**
1. **Los encargos narrativos del cap. 6 encabezan el plan** (e2 «La que no pesa», e3 «La persiana», con su beat de karma) — la deuda de namespace está RESUELTA, la prosa está lista, y el Faro pedagógico (`dato2/dato3`) ya tiene suelo. Es lo único que convierte el cap. 6 en CAPÍTULO y no en colección de salas.
2. **La red pieza 2** (`scp` + hosts descubribles leyendo el mundo + quests `story.ch4.*` con su prereq `cut→scp` de Havel) — la mecánica `ssh` de hoy es la llave; mañana la cerradura. Si Gwyndolin la fracciona: hosts descubribles ANTES que `scp` (sin destino, `scp` no tiene gracia).
3. **Higiene de tests**: los +4 de `auditor_orden` (Ornstein) y el `sort --help` en mensajes de `conteo.py` (Smough, relleno opcional que quedó sin hacer) — baratos, en la misma rama que toque cada uno.
4. **🧭22 (header contado como distrito)** queda en recámara CON MOTIVO (decisión de Gwyndolin en el plan de hoy): la lección del header entra cuando se toque el golden de nuevo — candidato natural: `dato4` (cruce de tablas), donde `tail -n +2` es prerequisito honesto.
5. **No tocar aún el karma del par 521/522** — el detector de patrones sigue sin dueño; la tríada del Auditor ya acumula huellas para cuando lo tenga.

**Para Juanma (si juega esta noche):** `https://cyberroot-psi.vercel.app/?chapter=6&seed=42` — ahora `ls` te esconde la nota del operador muerto (solo `-a` la revela), el LEEME te tienta con un atajo que miente, y la puerta web muestra la Lista COMO TABLA cuando cortas. Tu feedback humano manda sobre toda la recámara.
