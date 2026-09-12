# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

**Oscar 12/09 — cap. 4 `story.ch4.e2` «El volcado que no pesa» con alma + Faro intacto (zona 🔬 ejecutada COMPLETA desde save limpio, MODO B, 691/24-28/47)**

Saldo: 🧭20/21/22/23 **CERRADAS y RE-VERIFICADAS**, 🧭24 **CERRADA con matiz** (pre-puebla `shell.hosts` O1 09/09 vuelve redundante el rechazo `scp` sin `cat` — doc drift menor), 🧭25/26/27 **PERSISTEN** (límite 2 pipes + cut en ch4 + `grep -v` como filtro positivo, decisión Gwyn 11/09), 🧭28 **NUEVO CERRADO** (FICHA ch4.e2 con alma pulida por Manus 12/09). CICLO verde — el troncal ya tiene su misterio con alma sin salir de su grey.

**🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** `ls /srv/camara-faro` 5 sin dotfile, `ls -a` 6 con `.nota-corte`, `ls -la` largo+dotfiles. No reabrir.

**🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** `Atajo: grep ENSAYO purgas.csv | wc -l — sin ruta, desde aquí ahorras tecleo.` → relativa desde `/` da `0`+stderr vs absoluta `1`. Hallazgo Bandit intacto.

**🧭22 — CERRADA: header `distrito` ya no cuenta.** `tail -n +2 | cut -d'|' -f4 | sort` → `--/MUEL-01/UMBRAL-BAJO×2` sin `distrito` (e2 golden). No reabrir.

**🧭23 — CERRADA: `2 UMBRAL-BAJO` con glosa.** `textos.json` `story.ch6.e2.briefing` trae `un distrito se repite` + `UMBRAL-BAJO` + `PR-0092`; `hint_1` enseña `tail -n +2` sin regalar. No reabrir.

**🧭24 — CERRADA con matiz (re-verificada 12/09): `cat /etc/hosts` + `scp` — hygiene resuelta, con pre-puebla O1 09/09.** Medido 12/09 sobre `generate(42,4, contract_id='story.ch4.e2')` mundo real: `cat /etc/hosts` exit 0 descubre `faro`+`troncal-01` (seed 1 → `troncal-02` 3 hosts), `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` exit 0 deja `TR-001/TR-002/TR-003|EN_COLA` con `GameState` roundtrip idéntico preservando `hosts` y `/tmp/volcado.csv`. Matiz: `new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` desde `/etc/hosts` (O1 09/09, `generator.py:_parse_hosts_content`) — `scp` sin `cat` previo ya no rechaza (exit 0). El briefing aún documenta el rechazo didáctico «léelo en /etc/hosts», pero la pre-puebla lo vuelve redundante. No es bug (691/0, `scp` copia, roundtrip preserva `hosts`), solo doc drift menor para Gwyn si quiere ajustar el briefing o mantener la pre-puebla como comodidad. `ls /etc` no descubre (solo `cat` por `_note_hosts_discovery`). No reabrir.

**🧭25 — PERSISTE (recámara, dato exacto para decisión [P1] pipes): el shell soporta hasta 2 pipes (3 cmds); 3 pipes y redirección no existen.** Medido 12/09: `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` (1 pipe) exit 0 3 líneas sin `id`; `cut|grep|sort` con `sort` en ch4 →127 `sort` no existe en ch4 (frontera ch6); `cat /tmp/volcado.csv | cut -d'|' -f1 | grep TR- | wc -l` (3 pipes, 4 cmds) → `sh: multiple pipelines not supported in this session: chain them one at a time` exit 2 (exacto, `shell.py:_PIPE_MSG` `>3`). Redirección `> /tmp/x` → `sh: syntax not supported` exit 2 — `ch4.e2` con 1 pipe evita el límite por diseño. No es bug: ninguna quest pide 3 pipes ni `>` — `ch4.e2`/`dato4`/`dato5` caben en 1/0 pipes. Dirección: solo si una quest futura demuestra que 4 eslabones o `>` enseñan más, ampliar con ADR. Dueño: Gwyndolin/Gwyn. No bloquea hoy.

**🧭26 — PERSISTE (dirección pedagógica menor, no bug): `c.cut` ya vive en cap. 4, el Faro (cap. 6) deja de ser el primer sitio donde se aprende `cut`.** `c.cut` chapter 4 prereq `c.wc`(2) — `load_curriculum()` 24/28 lo confirma; `story.ch6.e1` requires `('c.grep','c.head','c.pipe','c.sort','c.tail','c.uniq','c.wc')` SIN `cut`, `dato2`/`dato3`/`e2` SÍ requieren `cut`. Jugando troncal PRIMERO, `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` ya se domina y se reusa en Faro dato2/e2. La progresión SIGUE enseñando `cut` con necesidad real (dato2/e2), solo e1 ya no es su puerta. Informo, no decido: Gwyn mantiene e1 sin `cut` (decisión 10/09). Módulo: `curriculum.json` si se toca. No bloquea.

**🧭27 — PERSISTE (fricción menor, no bloqueante, decisión Gwyn 11/09: filtro positivo): `grep -v` vía pipe/file NO soportado — `join | grep -v sujeto` falla, FICHA ya lo sortea.** Medido 12/09: `join | grep PR-0091` exit 0 1 línea; `ps aux | grep 11:04` exit 0 1 línea; pero `join | grep -v sujeto` → exit 2 `grep: sujeto: No such file` y `grep -v sujeto purgas.csv` → mismo, `ps aux | grep -v root` → exit 2. Causa: `texto.py:_run_grep` sin flags. FICHA ch4.e2 y dato4 ya usan filtro positivo (`grep TR-`/`grep 000`/`grep PR-0091`) y Gwyn decidió NO implementar `-v` (patrón positivo con más alma). No rompe (ninguna quest exige `-v`). Módulo: `src/core/sandbox/commands/texto.py` si se quiere. No bloquea.

**🧭28 — NUEVO, CERRADO (verificación positiva 12/09): FICHA ch4.e2 con alma pulida — el troncal ya tiene alma.** Medido 12/09: `story.ch4.e2.beat` con «El troncal guarda un volcado que lleva tres noches en el mismo sitio. Vive en troncal-01:/srv/archivo-troncal/volcado.csv, tabla con separador \'|\' y cabecera id|origen|destino|bytes|estado. Tres filas: TR-001 y TR-002 con estado OK, ya cruzaron al Faro con 1024 y 2048 bytes; TR-003 con 512 bytes y estado EN_COLA, lleva desde las 03:14 sin moverse. Si copias sin filtrar, el encabezado \'id\' entra como una fila mas y el recuento miente. Cortar la primera columna con cut y quedarte solo con lo que empieza por TR- es el gesto que separa lo que pesa de lo que espera.» + `story.ch4.e2.brief/briefing` con `cat /etc/hosts`→`scp`→`cut|grep TR-` 1 pipe, rutas absolutas, límite 2 pipes, `hint_1`/`hint_2`/`detail` con `id` fantasma y `EN_COLA` como pista ejecutable; 0 hits AI-slop (`testamento`/`panorama`/etc. 0), Dark Souls (dato arriba, grieta abajo), test del nombre tapado. Golden `cut -d\'|\' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin `id` verificado en `generate(42,4)` real. La prosa funcional de S2 (7 claves sobrias) ya tiene su FICHA con alma (Manus 12/09) — deuda Gwyn 11/09 saldada. Bundle 47 393.8 KiB regenerado, guardián verde. No reabrir.

*Para Gwyn 23:00:* 🧭20/21/22/23 cerradas, 🧭24 cerrada con matiz pre-puebla (doc drift menor: briefing dice rechazo `scp` sin `cat` pero `new_session` ya pre-puebla `hosts` — decide si ajustar texto o mantener comodidad), 🧭25/26/27 persisten con dato exacto, 🧭28 es verificación positiva nueva (FICHA ch4.e2 con alma). La pregunta de la zona «¿la quest enseña con NECESIDAD real? ¿el truco filtro positivo se SIENTE o parece arbitrario? ¿la NOTA del header invita a equivocarse UNA VEZ?» → **sí — `cat /etc/hosts` con 2-3 hosts es necesidad real de red, `cut|grep TR-` filtra el header `id` con lo que SÍ quieres (sin `grep -v`, decisión Gwyn 11/09 con alma), y el header invita a equivocarse UNA VEZ (cut sola deja `id`+3) antes de leer la pista `TR-003|EN_COLA 03:14` — equivocar enseñando, sano. El briefing con alma y el volcado que no pesa cierran el troncal sin salir de su grey.** Mi `CICLO: verde` se sostiene.


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

### 🎯 Artorias — filtro técnico 21:00 (12/09)
**Veredicto técnico (capa «¿está bien hecho?»): 3 PRs sanos ✅ — jornada verde sin humo y con la cuarta huella por fin entregada.**

Ensayo de integración pre-merge OBLIGATORIO (≥2 ramas, precedente 27/08) ejecutado en worktree desechable `/tmp/ensayo-pr` sin ensuciar main:
- `origin/main` (691) → merge `origin/feat/engine-2026-09-12` (O1, +3) → merge `origin/feat/sandbox-2026-09-12` (S2, +4) → merge `origin/feat/meta-ui-2026-09-12` (T1, +0). Conflictos huellas `activo.md`/`worklog` (3 merges, 4 regiones) resueltos vía script python (unión HECHOs + worklog cronológico 03→13→16→19, `grep -c '<<<<<<<'`→0 antes de cada commit).
- Suite combinada: **698 passed / 0 failed / 0 xfailed** en 3.31s (`PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`). Gate de datos (curriculum): **24 conceptos / 28 quests** (`story.ch4.e2` grey 4 `c.cut`+`c.scp`, DAG válido). Validado vía `load_curriculum()` 24/28.
- Bundle: 47 ficheros tras merges (O1+S2 ya regeneraron, T1 web-only). Bundle fresco y guardián verde.

**Aislados (verificados en worktrees desechables):**
- PR #47 `feat/engine-2026-09-12` 691→694 (+3: `postmortem.py` `_find_join`/`_extract_join_args` + `postmortem.auditor.join` + `test_auditor_join.py` 3 tests deterministas, prefijo disjunto `postmortem.auditor.join*`, sin tocar `curriculum.json`/`shell.py`) — **verde**.
- PR #48 `feat/sandbox-2026-09-12` 691→695 (+4: `shell.py` 127 glosa `JOIN_NAME` fuera de cap6 + `test_join_frontera.py` 4 tests cap0/ch4 glosa, ch6 sin glosa, generate intacto, importa `JOIN_NAME`, no toca data) — **verde**.
- PR #49 `feat/meta-ui-2026-09-12` 691→691 (+0: `web/app.js` panel «Volcado del Troncal» hermana del Faro + `web/index.html` + `web/README.md`, `parseTroncalCut` filtra solo volcado.csv, capítulo 4 only, fallback estático TR-001/002/003 EN_COLA + live get_csv, sin tocar data/, DUEÑO gate SUBSET respetado) — **verde**.

Smokes técnicos (sobre combinado 698):
- O1: `build_postmortem` con `join -v 1` añade `auditor_join`/`auditor_join_text` en `lines_resolved`, sin `join` byte-idéntico (solo `lines_resolved[0]`), `-v1`/`-av`/`pipe|join` variantes disparan, `join` sin `-v` documentado no dispara.
- S2: `Shell(DEFAULT_CAP0_COMMANDS).execute("join a b")` → 127 + `Try 'join --help' — tables cross there (chapter 6).`, ch4 idem, `foobar` 127 seco sin glosa, `Shell(DEFAULT_CH6_COMMANDS).execute("join a b")` → 0 con `1 x A`, `generate(42,6)` intacto.
- T1: `parseTroncalCut` solo para `volcado.csv` (purgas/registro intactos), `previewTroncalTabla` antes/después de `scp` con fallback estático, `currentChapter!==4` oculta, restart oculta ambos paneles.

**⚠️ AVISO CLARO A GWYN (23:00) — qué NO mergear y nº esperado:**
- **NO HAY NADA QUE NO MERGEAR — los 3 PRs están ✅ y listos.** No hay 💥 hoy. La rama vacía de ayer ya no existe: O1 por fin entregó.
- **SÍ MERGEAR: PR #47 (engine O1 auditor_join) + PR #48 (sandbox S2 127) + PR #49 (meta-ui T1 troncal web) — los 3 ✅.** Orden ensayado y recomendado: **47 → 48 → 49** (engine→sandbox→meta-ui; respeta que nadie toca rutas del otro, prefijos disjuntos, allowlist intacta; S2→T1 el web-preview consume el volcado de S2/Oscar). Si merges solo 47+48, T1 web sigue verde aislado.
- **Nº esperado tras merges (47+48+49):** **698 passed** exactos (691 +3 +4 +0), gate **24/28** (concepts/quests), bundle **47 ficheros** (regen canónico `python tools/web/build_bundle.py` tras merge — O1 tocó `textos.json`, S2 `shell.py` + bundle). Verificación: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` debe dar 698/0; `load_curriculum()` 24/28; `generate(42,6)` intacto; `generate(42,4, contract_id='story.ch4.e2')` golden 3 líneas.
- **Deltas declarados en PRs («tests antes: N · tests rama: M · delta esperado: +K»):** PR #47 `691→694 +3` ✅, PR #48 `691→695 +4` ✅, PR #49 `691→691 +0` ✅. Se COMPRUEBAN por aritmética sobre base 691, no a mano; combinado 691→698 (+7) verificado.
- **Cruce con [BUG] de la mañana:** ningún `[BUG]` bloqueante nuevo (Oscar/Havel 12/09 CICLO verde, smoke 691/0). Único `[BUG][P3]` persistente (🧭27) `grep -v` no soportado — ningún PR de hoy lo toca ni lo necesita (O1 busca `-v` en history, no en grep; S2 usa `JOIN_NAME`, no grep; T1 parsea `cut`). No bloquea. 🧭24 pre-puebla matiz (scp sin cat ya no rechaza) sigue como doc drift menor, ningún PR lo agrava.
- **Si ves 694/695/691 en lugar de 698:** faltó un merge; si gate 24/27 revisa que O1+S2 traigan `postmortem.auditor.join`+`c.cut/c.scp` 24/28; si `join` en ch4 no da 127 revisa `JOIN_NAME` import; si `generate(42,4, contract_id='story.ch4.e2')` no da TR-003 revisa que no hayas pisado volcado.
- **Bundle:** O1 y S2 ya regeneraron; tras merge de los 3 Gwyn debe hacer `python tools/web/build_bundle.py` canónico (47 ficheros, guardián verde).

**⭐ Qué me ha gustado (técnica, no sabor — pero deja huella para Gwyndolin):**
- **O1 auditor_join por fin aterriza — la cuarta huella del Auditor cierra la trilogía corte/orden/join.** `_extract_join_args` via `shlex.split` (pipe-aware, `-v`/`-v1`/`-av`/`-v 1`) es hermano exacto de `_extract_cut_args`/`_extract_sort_args`, determinista y sin imports sandbox. La línea `Expediente 000: cruce registrado — join anti-join (-v): huérfanas…` es formulario puro, sin filtrar datos de fila. Byte-idéntico sin join impecable.
- **S2 127 que enseña sin tocar allowlist — elegancia de frontera.** En vez de mover `c.join` a cap4, el 127 nombra el Faro con la misma energía que el `scp` nombraba `/etc/hosts`. Un `if argv[0]==JOIN_NAME` + import, 7 líneas, 4 tests que prueban frontera real (cap0, ch4, ch6, generate). No duplica textos, no crea `story.ch6.frontera-join*` innecesario, y `generate(42,6)` sigue enseñando `join -v 1` por necesidad.
- **T1 tabla viva del Troncal hermana del Faro — reuse sin duplicar.** Mismo patrón que 05/09: `parseCut` extendido a `volcado.csv` con filtro fino `parseTroncalCut`, `renderTroncalTabla` con columna destacada, `previewTroncalTabla` con fallback estático pre-scp (misma tabla que TRONCAL_CONTENT) + live tras `scp`. Web-only, sin tocar data/, DUEÑO gate SUBSET respetado (cero toques en `state/`).
- **Ownership declarado y respetado.** Plan 12/09 dijo «ALLOWLIST OWNER: NADIE» y «DUEÑO gate: Seath» y los 3 lo respetaron: ningún PR tocó allowlists ni el guard SUBSET del otro. Tres semanas después del patrón «parcheo el fichero del otro», por fin 0 cruces indebidos.

**Lo que no me gusta / fricción técnica (menor, no bloqueante):**
- **Bundle con doble regen (O1 394.0 KiB + S2 394.0 KiB) — unión trivial pero fragilizable.** Cada uno regeneró bundle core.json desde su rama; el ensayo unió sin conflicto pero ambos tocaron el mismo artefacto generado. Largo plazo: o solo una rama regenera, o Gwyn regen canónico post-merge (ya lo hace). Hoy no rompe.
- **O1 `_extract_join_args` detecta `v` en cualquier flag (`-av`) — generoso.** Cubre anti-join real pero aceptaría `-av` aunque GNU join no lo use; no es bug (el texto es estático, no ejecuta join), solo amplitud. Si algún día se quiere estricto, acotar a `-v`/`-vN`.
- **T1 duplica constantes de la tabla (TRONCAL_STATIC hardcodeada) — espejo del bundle.** Es fallback pre-scp, intencional y byte-idéntico a TRONCAL_CONTENT; si cambia el volcado habrá que sincronizar 2 sitios (web/app.js + generator). Documentado como estático, no como fuente de verdad.
- **🧭27 `grep -v` sigue sin soporte — pero hoy ningún PR lo necesita.** Sigue en recámara P3; la FICHA positiva ya enseña sin él. No es fricción de hoy.

**Ideas para mañana (van a `abierto.md` si no existen — no duplicar si ya están):**
- **Dato6 «La segunda purga» PR-0092 coma-trampa** — la purga que «no pesa» vs la que sí; `join` con coma dentro como lección de separador (Havel 12/09, persigue).
- **`sort -k4 -n` sobre volcado** — ordenar el volcado por bytes para cazar EN_COLA (Havel idea volcado→sort).
- **TR-003 EN_COLA como bifurcación karma** — rescatar vs quemar el volcado (Havel, P2).
- **Si el troncal ya tiene tabla viva, el siguiente hueco dulce es `ps aux | grep` en web** — espejo de la tabla Faro pero para `ps` (reusa patrón T1).

**Relevo a Gwyn:** ensayé **47→48→49 y 698 es tu número** (691+3+4+0, gate 24/28). Los 3 están ✅ y se mergean en ese orden (engine→sandbox→meta-ui). Si tu `generate(42,6)` tras merge sigue dando `join -v 1` + `ps aux|grep 11:04` y `generate(42,4, contract_id='story.ch4.e2')` da `TR-001/TR-002/TR-003` sin `id` y `DEFAULT_CH4_COMMANDS` 13 con `join`→127 en ch4, y `load_curriculum()` 24/28, aplica `python tools/web/build_bundle.py` y mergea **47 → 48 → 49**. Nada queda 💥. Bundle regen canónico 47 ficheros. Jornada redonda — la cuarta huella, el 127 que enseña y la tabla del troncal entran juntos sin pisarse.

### 🎯 Gwyn — cierre de diseño 23:00 (11/09)

**Estado de los merges:** PRs #45 (sandbox S2 `story.ch4.e2`) y #46 (meta-ui
T1 circuito ch4+guard SUBSET) mergeados en el orden ensayado por Artorias
(sandbox→meta-ui). Suite **691 passed** exactos (680+4+7), gate **24/28**,
bundle **47 ficheros (393.3 KiB)** regenerado canónicamente (guardián verde).
Goldens re-verificados en el mundo real post-merge: golden e2
`TR-001/TR-002/TR-003` sin header, allowlist 13, `tail`→127, `generate(42,6)`
intacto. **O1 `auditor_join` NO.mergeado: 💥 NO ENTREGADO** (0 commits, sin
PR; rama mantenida). Repón con la MISMA spec — nobody la cambió, es buena.
Las 2 ramas mergeadas borradas tras confirmar MERGED; la 3ª no se toca.
Resoluciones de huellas: los scripts añaden una assertion "ganó HEAD y
quedó cronológico" — esta noche el resolutor del 2º merge detectó que la
rama traía una sección NUEVA (Seath 19:00) que ni HEAD ni la heurística
"branch es vieja" contemplaba; la aserción de contenido la pescó antes de
comitear (se insertó cronológicamente). El enésimo salvavidas del patrón.

**Validación del 🧭 de Oscar (11/09):** las 🧭20/21/22/23/24 cerradas con
re-verificación quedan ARCHIVADAS — no abro discusión. **🧭27 (`grep -v`
no soportado): mi decisión es MANTENER el filtro positivo como lección y NO
implementar `-v` como deuda técnica.** Razón de diseño: el patrón
«filtra por lo que SÍ quieres» (`grep TR-`, `grep 000`, `grep PR-0091`)
enseñado tres veces en dos capítulos es una idea con más alma que un flag
menos conocido; y el handler sin flags obliga a componer (pipe) — la
fricción ES la lección. Si un día una quest exige filtrar por lo que NO es,
lo reconsidero (boon de hallazgo como propone Artorias, P3). 🧭25 (pipes)
y 🧭26 (`cut` ya en ch4) quedan en recámara como estaban, sin cambio.

**⭐ Lo que me ha gustado (capa diseño, del 11/09):**
- **«El volcado que no pesa» es un buen título que enseña lección.** La
  pista de lo que pesa no es lo que se roba sino lo que EN_COLA espera —
  `TR-003` es el dato narrativo ESCONDIDO en la sala de datos. El cap. 4
  (que era puro servicio) ya tiene un misterio propio sin salir de su
  troncal. ⭐⭐⭐
- **El cap. 4 ya tiene DOS misiones con tint distinto** y la lección del
  filtro positivo EVOLUCIONA: en dato4 del Faro se filtra "por el código
  de purga correcto"; en ch4.e2 se filtra "por el prefijo de lo que SÍ es
  volcado". Dos usos de la misma idea — no relleno, variación. ⭐⭐
- **Guard SUBSET de T1 institucionalizado (`<= 13`, nunca `==`).** La
  lección del 10/09 (llaves exactas se quiebran al añadir) ya es CONSTANTE
  con nombre propio en el código. El proyecto se hace robusto a sí mismo.
  ⭐⭐⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **S2 tocó `test_ch6_datos_circuit.py` (dueño T1) como hotfix de gate
  flexible** — tercera vez en dos semanas que "un dueño parchea el fichero
  del otro para no bloquear". Ya es patrón, no accidente: le pido a
  Gwyndolin que en el plan de MAÑANA declare QUIÉN es dueño de cada test
  de puerta/gate cuando dos módulos colaboren. Si sale otra vez, quite el
  único-changed-file del dibujo (o pregunto a Juanma por un mini-ADR).
- **O1 `auditor_join` NO ENTREGADO — tercera vez que Ornstein sufre
  replanificación** (1ª sin rama 07/09, 2ª 💥, 3ª 💥). Un turno con tres
  día seguidos sin entrega pide diagnóstico, no empieza de nuevo: pido a
  Gwyndolin que mañana evalúe si es tamaño de tarea, señal del plan
  anterior, o load del turno de 13:00 y lo plantee con datos.

**Dirección para mañana (prioridad de diseño):**
1. **Reposición `auditor_join` (O1, Ornstein 13:00)** — misma spec intacta:
   prefijo `postmortem.auditor.join` (disjunto de `story.ch4.e2`),
   detector `_find_join` con `-v`, 3 tests. Con la PR #46 ya mergeada, el
   Ensayo mañana es de 1 rama (tras 691 base).
2. **Manus: el ALMA de `story.ch4.e2`** — la FICHA de dato4 la cubrió el
   05:00 (gracias). Ahora le falta ALMA a e2 del troncal: la prosa de
   `story.ch4.e2.*` es honesta pero SOBRIA (7 claves, functional). La glosa
   del «que no pesa» y el destino de `TR-003|EN_COLA` en la historia
   siguiente merecen una FICHA de sabor como la del dato4.
3. **`grep -v` NO tocado (decisión arriba)** — prioridad 0 en recámara;
   despedida limpio.
4. **No tocar:** karma 521/522 (sin dueño, Q con Manus), pack
   `POSTMORTEM.md` (séptima noche sin urgencia), 🧭25/26 (recámara).

**Para Juanma (si juega esta noche):** entra al cap. 4 con la llave
prestada (e1) y verás una SALA NUEVA grey «El volcado que no pesa»:
`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` para bajarte el
volcado, y el truco que aprendiste en el Faro invertido —
`cut -d'|' -f1 /tmp/volcado.csv | grep TR-` para quedarte solo con los
registros (sin el header del servidor). El truco del día: la tercera línea
del volcado dice `TR-003|EN_COLA` y esa es la que pesa.

### 🎯 Gwyn — cierre 10/09 (histórico; ver entrada del 11/09 arriba)
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
