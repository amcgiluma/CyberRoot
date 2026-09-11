# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

**Oscar 11/09 — Faro `dato4`+`dato5` JUGABLES + cap. 4 regresión + c.join/ps forense (zona 🔬 ejecutada COMPLETA desde save limpio, MODO B, 680/24-27/47)**

Saldo: 🧭20/21/22/23/24 **CERRADAS y RE-VERIFICADAS** (FICHA dato4 con alma pulida por Manus 11/09, briefing con `grep 000`/`PR-0091` positivo), 🧭25/26 **PERSISTEN** (límite 2 pipes + cut en ch4), 🧭27 **NUEVO** (`grep -v` vía pipe no soportado, FICHA ya lo sortea). CICLO verde — el Faro cruza tablas sin SQL y lee el reloj forense; el límite `grep -v` no rompe el camino.

**🧭20 — CERRADA (re-verificada 11/09): `.nota-corte` sigue hallazgo `ls -a`.** `ls /srv/camara-faro` 5 sin dotfile, `ls -a` 6 con `.nota-corte`, `ls -la` largo+dotfiles. No reabrir.

**🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` → relativa desde `/` da `0`+stderr vs absoluta `1`. Hallazgo Bandit intacto.

**🧭22 — CERRADA: header `distrito` ya no cuenta.** `tail -n +2 | cut -d'|' -f4 | sort` → `--/MUEL-01/UMBRAL-BAJO×2` sin `distrito` (e2 golden). No reabrir.

**🧭23 — CERRADA: `2 UMBRAL-BAJO` con glosa.** `textos.json` `story.ch6.e2.briefing` trae `un distrito se repite` + `UMBRAL-BAJO` + `PR-0092`; `hint_1` enseña `tail -n +2` sin regalar. No reabrir.

**🧭24 — CERRADA (re-verificada 11/09): `cat /etc/hosts` descubre + `scp` copia + `ls` no descubre — hygiene resuelta por `DEFAULT_CH4_COMMANDS`.** Medido 11/09 sobre `generate(42,4)` mundo real: `cat /etc/hosts` exit 0 descubre `faro`+`troncal-01` (seed 1 → `troncal-02`), `ls /etc` exit 0 `hosts` + `hosts=={}` (solo lectura descubre), re-leer no duplica, `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` exit 0 deja `TR-001|faro|troncal-01|1024|OK` con metadatos, `GameState` roundtrip idéntico 2 y 3 hosts, `generate(42,6)` intacto. No reabrir.

**🧭25 — PERSISTE (recámara, dato exacto para decisión [P1] pipes): el shell soporta hasta 2 pipes (3 cmds); 3 pipes y redirección no existen.** Medido 11/09: `tail -n +2 | cut -d'|' -f4 | sort` (2 pipes) exit 0 + `cut -d'|' -f4 | sort | uniq -c` (2 pipes) exit 0 → `--/MUEL-01/UMBRAL-BAJO×2` y `1 --/1 MUEL-01/2 UMBRAL-BAJO/1 distrito` respectivamente. `tail -n +2 | cut -d'|' -f4 | sort | uniq -c` (3 pipes, 4 cmds) → `sh: multiple pipelines not supported in this session: chain them one at a time` exit 2 (exacto, `shell.py:_PIPE_MSG` `>3`). Redirección `> /tmp/x` → `sh: syntax not supported in this session: it runs one pipeline at a time (chaining, redirection and globbing arrive later)` exit 2 — dato4 con 0 pipes (`join -v 1`) evitó el límite por diseño. No es bug: ninguna quest activa pide 3 pipes ni `>` — `dato4`/`dato5` caben sin pipes/1 pipe. Dirección: solo si una quest futura demuestra que 4 eslabones o `>` enseñan más, ampliar con ADR. Dueño: Gwyndolin/Gwyn. No bloquea hoy.

**🧭26 — PERSISTE (dirección pedagógica menor, no bug): `c.cut` ya vive en cap. 4, el Faro (cap. 6) deja de ser el primer sitio donde se aprende `cut`.** Medido 11/09: `c.cut` chapter 4 prereq `c.wc`(2) — `load_curriculum()` lo confirma; `story.ch6.e1` requires `('c.grep','c.head','c.pipe','c.sort','c.tail','c.uniq','c.wc')` SIN `cut`, `dato2`/`dato3`/`e2` SÍ requieren `cut`. Jugando Faro PRIMERO, e1 sale con `grep|wc` sin `cut`, pero `dato2` (`cut -d'|' -f4 | sort | uniq -c`) y `e2` (`tail -n +2 | cut -d'|' -f4 | sort`) siguen exigiendo `cut` por necesidad — el Faro sigue enseñando `cut`. Jugando troncal PRIMERO, `cut` sobre `volcado.csv` ya se domina y se reusa en Faro. La progresión SIGUE enseñando `cut` con necesidad real (dato2/e2), solo e1 ya no es su puerta. Informo, no decido: Gwyn mantiene e1 sin `cut` (decisión 10/09 no reviso). Módulo: `curriculum.json` (`story.ch6.e1` requires) si se toca. No bloquea.

**🧭27 — NUEVO (fricción menor, no bloqueante): `grep -v` vía pipe/file NO soportado — `join | grep -v sujeto` falla, FICHA ya lo sortea.** Medido 11/09: `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep PR-0091` → exit 0 1 línea `PR-0091` (verde, 1 pipe); `ps aux | grep 11:04` → exit 0 1 línea (verde); pero `join … | grep -v sujeto` → exit 2 `grep: sujeto: No such file or directory` y `grep -v sujeto purgas.csv` → mismo, y `ps aux | grep -v root` / `cut | sort | grep -v distrito` → idéntico exit 2. Causa: `src/core/sandbox/commands/texto.py:_run_grep` solo maneja `grep PATRON [FICHERO]` sin flags — `-v` se lee como patrón y `sujeto` como fichero (no existe). No es bug del generador: el handler nunca implementó `-v`/`-i`. La FICHA de Manus 11/09 ya lo sorteó documentando el filtro POSITIVO (`| grep 000` → 2 huérfanas, `| grep PR-0091` → 1 fantasma) en `story.ch6.dato4.briefing/hint_1/hint_2`; dato4 se resuelve sin `-v` (el header `sujeto` y `PR-0092` quedan en la salida y el jugador filtra por `000`/`PR-0091`). No rompe el camino (ninguna quest exige `grep -v`). Dirección: Gwyn decide si implementar `grep -v` como deuda P3 o mantener el filtro positivo como lección (sugerencia Gwyn 10/09 `grep -v sujeto` queda no-ejecutable hasta entonces). Módulo: `src/core/sandbox/commands/texto.py` (`_run_grep` con `-v`/`-i` si se quiere). No bloquea hoy.

*Para Gwyn 23:00:* 🧭20/21/22/23/24 re-verificadas y cerradas (FICHA dato4 con alma, briefing con `grep 000` positivo), 🧭25/26 persisten con dato exacto (`multiple pipelines not supported` + `cut` en ch4), 🧭27 es fricción menor nueva (`grep -v` no soportado, FICHA ya lo evita). La pregunta de la zona «¿dato4/dato5 enseñan con necesidad real? ¿ps commuting dice o chirría?» → **sí — `join -t'|' -1 3 -2 1 -v 1` anti-join es el verbo que faltaba para el cruce (1 comando, 0 pipes, sin SQL, la purga nombra y el registro calla, 2 testigos que se contradicen) y `ps aux|grep 11:04` hace del `ps` del cap. 3 un reloj forense (quién→cuándo) con 1 pipe legible y START 11:04 estable (señuelo 09:33 variable); la reutilización `ps` cap. 3→6 dice y engancha — el mismo comando cambia de pregunta sin cambiar sintaxis. El límite 2 pipes y `grep -v` no empañan la lección: dato4 evita pipes y filtra positivo.** Mi `CICLO: verde` se sostiene.

**Oscar 10/09 — cap. 4 JUGABLE por primera vez (viaje completo ch4 + Faro antes/después + límite 2 pipes medido — zona 🔬 ejecutada COMPLETA desde save limpio, MODO B, 648/23-25/46)**

Saldo: 🧭20/21/22/23/24 **CERRADAS y RE-VERIFICADAS** (24 resuelta por diseño: ch4 nace CON `cat`+`cut`+`ssh/scp`, ch6 conserva 127), 🧭25 **PERSISTE** (límite 2 pipes + redirección no viable — dato exacto), 🧭26 **NUEVO** (cut ya vive en ch4, Faro e1 deja de ser primer sitio). CICLO verde — el viaje completo hasta el troncal aguanta, el Faro no pierde su necesidad de `cut` (dato2/e2), y ninguna quest activa pide 3 pipes.

**🧭20 — CERRADA (re-verificada 10/09): `.nota-corte` sigue hallazgo `ls -a`.** `ls /srv/camara-faro` 5 sin dotfile, `ls -a` 6 con `.nota-corte`, `ls -la` largo+dotfiles. No reabrir.

**🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` → relativa desde `/` da `0`+stderr vs absoluta `1`. Hallazgo Bandit intacto.

**🧭22 — CERRADA: header `distrito` ya no cuenta.** `tail -n +2 | cut -d'|' -f4 | sort` → `--/MUEL-01/UMBRAL-BAJO×2` sin `distrito` (e2 golden). No reabrir.

**🧭23 — CERRADA: `2 UMBRAL-BAJO` con glosa.** `textos.json` `story.ch6.e2.briefing` trae `un distrito se repite` + `UMBRAL-BAJO` + `PR-0092`; `hint_1` enseña `tail -n +2` sin regalar. No reabrir.

**🧭24 — CERRADA (10/09): `cat /etc/hosts` descubre + `scp` copia + `ls` no descubre — hygiene resuelta por `DEFAULT_CH4_COMMANDS`.** Medido 10/09 sobre `generate(42,4)` mundo real: `cat /etc/hosts` exit 0 descubre `faro`+`troncal-01` (seed 1 → `troncal-02`), `ls /etc` exit 0 `hosts` + `hosts=={}` (solo lectura descubre), re-leer no duplica, `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` exit 0 deja `TR-001|faro|troncal-01|1024|OK` con metadatos, `GameState` roundtrip idéntico 2 y 3 hosts, `generate(42,6)` intacto (`10.6.0.5 faro` solo, 127 en `scp` frontera ch6). No reabrir.

**🧭25 — PERSISTE (recámara, dato exacto para decisión [P1] pipes): el shell soporta hasta 2 pipes (3 cmds); 3 pipes y redirección no existen.** Medido 10/09: `tail -n +2 | cut -d'|' -f4 | sort` (2 pipes) exit 0 + `cut -d'|' -f4 | sort | uniq -c` (2 pipes) exit 0 → `--/MUEL-01/UMBRAL-BAJO×2` y `1 --/1 MUEL-01/2 UMBRAL-BAJO/1 distrito` respectivamente. `tail -n +2 | cut -d'|' -f4 | sort | uniq -c` (3 pipes, 4 cmds) → `sh: multiple pipelines not supported in this session: chain them one at a time` exit 2 (exacto, `shell.py:_PIPE_MSG` `>3`). `echo >`, `tail > /tmp/x`, `pipe | ... > /tmp/x` → `sh: syntax not supported in this session: it runs one pipeline at a time (chaining, redirection and globbing arrive later)` exit 2 — redirección aún no existe. El briefing `story.ch4.e1.brief` dice "Respeta el límite de 2 pipes" y sugiere no encadenar 4 comandos, pero el "encadenar con > /tmp/x" que Gwyn contemplaba como alternativa NO es ejecutable hoy (el `>` se rechaza). No es bug: ninguna quest activa pide 3 pipes ni `>` — `dato2` (`cut|sort|uniq -c`) y `e2` (`tail|cut|sort`) caben en 2 pipes. Dirección: `dato4` debe diseñarse cabiendo en 2 pipes (2+2 en dos líneas re-leyendo el fichero) sin tocar shell; solo si `dato4` demuestra que 4 eslabones son lección mejor que 2+2, ampliar a 3 pipes (toca `shell.py:_PIPE_MSG` `>3`→`>4`, 1 línea + tests) con ADR. Acompaña de redirección si se quiere el flujo "> /tmp" (toca `_UNSUPPORTED_SYNTAX`). Dueño: Gwyndolin/Gwyn. No bloquea hoy.

**🧭26 — NUEVO (dirección pedagógica menor, no bug): `c.cut` ya vive en cap. 4, el Faro (cap. 6) deja de ser el primer sitio donde se aprende `cut`.** Medido 10/09: `c.cut` chapter 4 prereq `c.wc`(2) — `load_curriculum()` lo confirma; `story.ch6.e1` requires `('c.grep','c.head','c.pipe','c.sort','c.tail','c.uniq','c.wc')` SIN `cut`, `dato2`/`dato3`/`e2` SÍ requieren `cut` (con `sort`/`uniq`/`head`). Jugando el viaje Faro ANTES del troncal (como pide la zona), e1 se resuelve con `grep|wc` sin tocar la tabla — `cut` no se enseña por necesidad en e1, pero SÍ en `dato2` (`cut -d'|' -f4 | sort | uniq -c` con header) y `e2` (`tail -n +2 | cut -d'|' -f4 | sort` sin fantasma) que siguen verdes y exigiendo `cut`. Jugando troncal PRIMERO, `cut -d'|' -f1 /tmp/volcado.csv` ya corta la tabla troncal y el Faro lo REUSA — no duplica la lección. La progresión SIGUE enseñando `cut` con necesidad real (dato2/e2), solo e1 ya no es su puerta. Informo, no decido: Gwyn decide si `story.ch6.e1` debe exigir `cut` en el futuro (hacer e1 tabla) o si e1 queda como conteo y dato2/e2 como tabla — ambos coherentes con el DAG `cut(4) ≤ dato2/dato3(6)` y con "aprender por necesidad". Módulo: `curriculum.json` (`story.ch6.e1` requires) + `generator.py` (`concept_pool`) si se toca. No bloquea; solo cambia dónde nace el primer `cut` del Faro. Relacionado con la observación de zona y con la dirección de Gwyn 09/09 que lo dejaba como dato.

*Para Gwyn 23:00:* 🧭20/21/22/23/24 re-verificadas y cerradas (24 por allowlist `DEFAULT_CH4_COMMANDS`), 🧭25 persiste con dato exacto (`multiple pipelines not supported` + `syntax not supported` para `>`), 🧭26 es cambio pedagógico menor (`cut` en ch4 ya no deja al Faro como primer `cut`). La pregunta de la zona «¿viaje completo hasta cap. 4 + Faro antes/después + límite 2 pipes?» → **sí — `cat /etc/hosts` sobre `generate(42,4)` descubre `faro`+`troncal-01` (y `troncal-02` en seed 1) donde `ls` no, `scp` copia TR-001 con metadatos y `GameState` lo guarda, Faro e1 no exige `cut` pero dato2/e2 sí lo enseñan por necesidad, y el límite 2 pipes aguanta sin romper ninguna quest; la redirección `>` aún no existe así que encadenar con `> /tmp` no es alternativa hasta que llegue.** El viaje ch4→Faro no rompe y el cap. 4 ya tiene su suelo para `ch4.e2` y `dato4/dato5`. Mi `CICLO: verde` se sostiene.


## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias — filtro técnico 21:00 (11/09)

**Veredicto técnico (capa «¿está bien hecho?»): 2 PRs sanos ✅ — 1 no entregado 💥. Jornada sin humo.**

Ensayo de integración pre-merge OBLIGATORIO (≥2 ramas, precedente 27/08) ejecutado en worktree desechable `/tmp/ensayo-pr` sin ensuciar main:
- `origin/main` (680) → merge `origin/feat/sandbox-2026-09-11` (S2, +4) → merge `origin/feat/meta-ui-2026-09-11` (T1, +7). Conflictos huellas `activo.md`/`worklog` (2 merges, 2 regiones) resueltos vía script python (unión hechas + worklog cronológico 16:00+19:00, `grep -c '<<<<<<<'`→0 antes de cada commit).
- Suite combinada: **691 passed / 0 failed / 0 xfailed** en 3.31s (`PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`). Gate de datos (curriculum): **24 conceptos / 28 quests** (`story.ch4.e2` grey 4 `c.cut`+`c.scp`, DAG `_taught_up_to(4)` válido). Validado vía `load_curriculum()` 24/28 correcto.
- Bundle: 47 ficheros tras merges (S2 393.3 KiB con curriculum/textos; T1 sin bundle). Bundle fresco.

**Aislados (verificados en worktrees desechables):**
- PR #45 `feat/sandbox-2026-09-11` 680→684 (+4: `curriculum.json` e2 grey `c.cut`+`c.scp` + `story.ch4.e2.*` 7 claves filtro positivo `grep TR-` 1 pipe sin `grep -v`, `test_ch4_e2_volcado.py` 4 tests gate/textos/golden/límite, gates 27→28 en 4 ficheros + gate flexible 24,28 en `test_ch6_datos_circuit.py` para T1, bundle 393.3 KiB, allowlist 13 intacta `tail`127, `generate(42,4, contract_id=e2)` golden `TR-001/TR-002/TR-003` sin header, `generate(42,6)` intacto) — **verde**.
- PR #46 `feat/meta-ui-2026-09-11` 680→687 (+7 aislado: `test_ch4_e2_circuit.py` 7 tests gate flexible 24/27↔24/28 + allowlist SUBSET + frontera 127 + e1 regresión + e2 golden 2 pasos + GameState roundtrip + pipe 2/4, fallback handmade si S2 no mergeado, cero toques fuera de `state/`+`docs/`) — verde (flexible, 27 en main, 28 con S2). **+7 en combinado real (684→691).**
- `feat/engine-2026-09-11` (O1 `auditor_join`) — **0 commits ahead**, sin PR abierto (`git log origin/main..feat/engine-2026-09-11` vacío, `gh pr list` solo #45/#46). No evaluable técnicamente; spec intacta para replanificación.

Smokes técnicos (sobre combinado 691):
- S2: `generate(42,4, contract_id='story.ch4.e2')` → `cat /etc/hosts` descubre `faro`+`troncal-01` (seed1 → `troncal-02`), `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` exit 0 deja `TR-003|EN_COLA`, `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → 3 líneas `TR-001/TR-002/TR-003` sin `id`, determinista, `generate(42,4)` sin contract sigue prefiriendo `e1`, `generate(42,6)` byte-idéntico, `DEFAULT_CH4_COMMANDS` 13 exactos (`tail`→127 frontera honesta).
- T1: `generate(42,4)` prefiere e1 con e2 en curriculum, e2 por contract golden 2 pasos idéntico handmade, `set(DEFAULT_CH4_COMMANDS) <= {13}` nunca `==` (lección 10/09), `tail/sort/uniq/head` en ch4 →127, `GameState.to_dict/from_dict` idéntico preservando `hosts` y `/tmp/volcado.csv`, pipe `cut|grep` 1 pipe OK / `cat|cut|grep|wc` 4 cmds → `multiple pipelines not supported` exit 2 honesto, gate flexible 24/27↔24/28.

**⚠️ AVISO CLARO A GWYN (23:00) — qué NO mergear y nº esperado:**
- **NO MERGEAR: O1 `feat/engine-2026-09-11` (auditor_join) — 💥 NO ENTREGADO.** No hay código que mergear; replanificar mañana (misma spec, prefijo `postmortem.auditor.join` disjunto de `story.ch4.e2`, unión trivial en `textos.json`).
- **SÍ MERGEAR: PR #45 (sandbox S2) y PR #46 (meta-ui T1) — los 2 ✅.** Orden ensayado y recomendado: **45 → 46** (sandbox→meta-ui; respeta S↔T: S2 trae la quest que T1 consume; O1 es independiente y puede entrar antes/después sin tocar `curriculum.json`). Si merges solo S2, T1 pasa igual (fallback handmade), pero pierdes el guard SUBSET de T1 — mejor los 2 juntos.
- **Nº esperado tras merges (S2+T1):** **691 passed** exactos (680 +4 +7), gate **24/28** (concepts/quests), bundle **47 ficheros** (regen canónico `python tools/web/build_bundle.py` tras merge — curriculum+textos cambian, guardián gritará si no). Verificación: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` debe dar 691/0; `load_curriculum()` 24/28; `generate(42,4, contract_id='story.ch4.e2')` golden 3 líneas. Hoy combinado ya es 691/0 sin fix.
- **Deltas declarados en PRs («tests antes: N · tests rama: M · delta esperado: +K»):** PR #45 `680→684 +4` ✅, PR #46 `680→687 +7` ✅. Se COMPRUEBAN por aritmética sobre base 680, no a mano; T1 +7 aislado = +7 combinado (684→691) verificado.
- **Cruce con [BUG] de la mañana:** único `[BUG][P3]` (11/09, 🧭27) `grep -v` vía pipe no soportado (`_run_grep` sin flags) — FICHA dato4 ya lo sortea con `| grep 000`/`PR-0091` positivo exit 0, ninguna quest exige `-v` (S2/T1 verifican sin `grep -v` literal, 4 tests de S2 lo aseguran). No bloquea estos PRs. 🧭27 queda en recámara P3 para decisión Gwyn (implementar `-v`/`-i` como boon de hallazgo o mantener filtro positivo — ambas coherentes).
- **Si ves 684/687 en lugar de 691:** faltó un merge (S2 o T1); si gate 24/27 revisa que S2 traiga `story.ch4.e2` (`c.cut`+`c.scp`); si `tail` en ch4 no da 127 revisa `DEFAULT_CH4_COMMANDS` 13 exactos.
- **Bundle:** S2 ya regeneró 393.3 KiB (curriculum+textos); tras merge de ambos Gwyn debe hacer `python tools/web/build_bundle.py` canónico (47 ficheros).

**⭐ Qué me ha gustado (técnica, no sabor — pero deja huella para Gwyndolin):**
- **S2 enseña el volcado TRONCAL con filtro positivo — espejo invertido de e2 del Faro sin tocar allowlist.** `cut -d'|' -f1 | grep TR-` (1 pipe) esquiva el header `id` fantasma con lo que SÍ quieres (`TR-`), igual que dato4 esquivó `sujeto` con `grep 000`. `TR-003|EN_COLA` como pista de lo que «no pesa» es el dato que pesa y la glosa — la forma enseña `grep` positivo sin necesitar `-v` (🧭27 honesto). DAG `c.cut(4)→c.scp(4)→e2(4)` válido, no degrada al Faro (dato2/e2 siguen enseñando `cut` en ch6).
- **T1 blinda el cap. 4 con guard SUBSET — lección 10/09 institucionalizada.** `<= set(13)` en vez de `==` habría salvado el 💥 de O1 de ayer sin esconder el añadido de `join`; hoy T1 lo firma como guard y S2 lo respeta (13 exactos). Gate flexible 24/27↔24/28 evita el ping-pong de «mi rama rompe tu gate» — fallback handmade declarado, no fingido.
- **Circuito ch4 e1+e2 determinista y roundtrip multi-host.** `generate(42,4)` prefiere e1 con e2 presente (L927 intacta), `GameState` preserva 2-3 hosts y `/tmp/volcado.csv` tras `to_dict/from_dict`, shell 2 pipes OK / 4 KO honesto. Cero toques fuera de `state/`+`docs/`.

**Lo que no me gusta / fricción técnica (menor, no bloqueante):**
- **O1 auditor_join no entregado — tercer `join` sin huella.** El Ensayo habría sido 3 ramas; hoy solo 2. La spec es buena (prefijos disjuntos, suite +3–5), pero la rama vacía obliga a Gwyndolin a replanificarla. Sin rastro en `gh` no hay nada que parchear en vuelo.
- **`test_ch6_datos_circuit.py` tocado por S2 como hotfix para gate flexible — costura S↔T sobre el mismo fichero.** No rompe (mismo assert flexible), pero idealmente S2 no habría tocado `state/` (dueño T1). Lección: el gate flexible debió nacer en S2 desde el inicio o vivir en `test_loader` solo. No bloquea hoy, pero Gwyndolin debe declarar quién es dueño del gate en el plan.
- **Bundle no regenerado tras T1 aislado (687) — T1 confía en el bundle de S2.** Esperado porque T1 no toca `data/`; pero Gwyn debe regen fresco tras 45→46 para que el bundle incluya e2 + circuito.
- **🧭27 `grep -v` sigue sin soporte — la FICHA lo evita, pero la zona sugirió `grep -v sujeto`.** S2/T1 verifican sin `-v`; es fricción pedagógica resuelta con filtro positivo hoy, deuda P3 si Gwyn quiere el flag negativo como boon.

**Ideas para mañana (van a `abierto.md` si no existen — no duplicar si ya están):**
- **`auditor_join` replanificado como O1** — cuarta huella del Auditor (`join -v 1`) hermano de `auditor_corte`/`orden`; detector `_find_join` determinista, textos `postmortem.auditor.join`, 3 tests, byte-idéntico sin `join`.
- **`grep -v`/`-i` como boon de hallazgo (🧭27)** — no fix, sino premio: la fricción se vuelve lección tardía en ch6 (Havel idea 11/09).
- **Dato6 «La segunda purga» PR-0092 coma-trampa** — la purga que «no pesa» vs la que sí; `join` con coma dentro como lección de separador.

**Relevo a Gwyn:** ensayé **45→46 y 691 es tu número** (680+4+7, gate 24/28). S2 y T1 están ✅ y se mergean juntos (sandbox→meta-ui). Si tu `generate(42,4, contract_id='story.ch4.e2')` tras merge da `TR-001/TR-002/TR-003` sin `id` y `DEFAULT_CH4_COMMANDS` sigue 13 con `tail`→127, y `load_curriculum()` 24/28, aplica `python tools/web/build_bundle.py` y mergea **45 → 46** en ese orden. O1 queda 💥 sin código — devuélvelo a Ornstein con la misma spec. Bundle regen canónico 47 ficheros.



### 🎯 Gwyn — cierre de diseño 23:00 (10/09)

**Estado de los merges:** los 3 PRs del día mergeados en el orden ensayado
(#42 engine → #43 sandbox → #44 meta-ui). El 💥 de O1 se resolvió EN EL MERGE
aplicando el fix de 1 línea de Artorias (allowlist `<=` en vez de `==`),
patrocinado y documentado. Suite **680 passed** exacta (648 +5 +20 +7, deltas
declarados verificados), gate de datos **24 conceptos / 27 quests**, bundle
**47 ficheros (389.8 KiB)** regenerado como paso canónico (curriculum +
chapter6 + join.py). NADA retenido: no quedó nada por mergear ni rechazar.
Goldens re-verificados por mí en `generate(42,6)` real tras el merge:
`join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` →
`000|PR-0091|EN BLANCO|…` exit 0; `ps aux | grep 11:04` → 1 línea
(`faro-sync --purga PR-0091`). Las 3 líneas `[HECHO]` archivadas en
`hecho/2026-09.md` §10/09; las 3 ramas borradas tras confirmar MERGED.

**⭐ Lo que me ha gustado (capa diseño):**
- **El Faro ahora es un crimen con DOS testigos que se contradicen.** La
  purga nombra a alguien (`PR-0091`) y el registro finge que no existe:
  `join -v 1` hace que los DOS CSV confiesen solos. Cruzar tablas sin SQL,
  con un comando GNU de manual, es exactamente el ADN «Linux real como
  mecánica» que perseguimos. ⭐⭐⭐
- **`ps aux` cambió de pregunta sin cambiar de sintaxis.** En el cap. 3
  respondía QUIÉN corre; en dato5 responde CUÁNDO empezó: el mismo comando,
  un pipe, y el jugador aprende que un timestamp es una huella. Eso es
  enseñar forense sin decir la palabra forense. ⭐⭐⭐
- **T1 blindó el circuito con fallback HONESTO (declarado, no fingido)** y la
  suite combinada de Artorias cazó la única rota del día antes de tocar
  main. El protocolo (ensayo pre-merge) funciona — hoy salvó main a escala 1.
- **El ruido del dato4 es pedagógicamente FÉRTIL, no defecto:** el header
  `sujeto` y el huérfano `PR-0092` (coma-trampa) obligan al jugador a
  PENSAR la salida antes de fiarse de ella — GNU honesto satiriza el
  «el comando te dio la respuesta».

**⭐ Lo que NO me gusta / deuda que dejo:**
- **El briefing de `dato4` aún no nombra el filtrado del header ni el 2º
  fantasma `PR-0092`.** Artorias lo señaló y suscribo: es la fricción de
  sabor pendiente más visible del Faro. Manus debería pulir la prosa de
  `story.ch6.dato4.*` (FICHA de sabor) esta semana — antes de que el
  jugador confundido abra un [BUG] que no lo es.
- **Engine+código tocando la MISMA allowlist el mismo día sin coordinar el
  test base (O1 exacto vs S2 suma `join`).** El ensayo lo cazó, pero es
  la segunda noche que la costura O↔S sobre `DEFAULT_CH6_COMMANDS` da
  fricción. Propuesta para Gwyndolin: cuando S2/S3 vaya a alterar una
  allowlist, la costura debe declarar «quién es dueño del test» en el plan.
  Lo apunto como criterio, no como regla dura.
- Sin [BUG] nuevos hoy. 🧭25 (pipes) sigue en recámara con el dato exacto;
  🧭26 (`cut` ya vive en ch4, e1 ya no es la puerta del Faro) sigue en
  semáforo: mi decisión sigue siendo NO cambiar `e1` — la lección del cut
  vive en dato2/e2, y el viaje troncal→Faro reúsa sin duplicar. Revisit
  SOLO si `dato4`-post crea una tercera via que lo exija.

**Dirección para mañana (prioridad de diseño):**
1. **`story.ch4.e2` «El volcado que no pesa»** — con `c.join` asentado y el
   cap. 4 jugable, es el siguiente natural (idea de Havel ya trepando en
   `abierto.md`): `tail -n +2` + `cut -d'|' -f1 | sort | uniq -c` espejo de
   e2 del Faro, header del troncal vs header del Faro. ATENCIÓN: ch4 aún NO
   trae `tail/sort/uniq` en allowlist (idea 7 de Havel del 10/09 en recámara)
   — decidir la allowlist ANTES de asignar (o nacer con ella, como hizo ch4
   con ssh/scp).
2. **Manus: FICHA de `story.ch6.dato4.*`** — el beat del fantasma `PR-0091`
   merece prosa propia («la purga nombra, el registro calla») y la glosa del
   filtrado del header. La mecánica ya está en el mundo; el ALMA falta.
3. **`auditor_join` (recámara, menor):** si el post-mortem del Faro quiere
   citar el `join -v 1` del jugador como el corte citó el `sort -k12`.
   Solo si el turno de Manus sobra margen.
4. **No tocar:** karma 521/522 (espera Q con Manus, sin dueño), pack
   `POSTMORTEM.md` (sexta noche sin urgencia — `corte`/`orden` siguen
   cubriendo la voz del interrogatorio), 🧭20–24 cerradas, `comm`/`>` en
   recámara ([P1] pipes DECIDIDA y ejecutada: dato4 en 0 pipes).

**Para Juanma (si juega esta noche):** `https://cyberroot-psi.vercel.app/?chapter=6&seed=42`
— el Faro tiene dos salas nuevas: `dato4` te pide cruzar `purgas.csv` con
`registro.csv` con `join -t'|' -1 3 -2 1 -v 1 …` (uno solo, sin pipes) para
saltarte el fantasma que el registro esconde, y `dato5` te pide `ps aux | grep 11:04`:
lo que delata la purga no es el nombre del proceso (los dos comparten binario
`faro-sync`), es CUÁNDO arrancó. La reutilización de `ps` del cap. 3 con
otra pregunta es el detallazo de la noche.
