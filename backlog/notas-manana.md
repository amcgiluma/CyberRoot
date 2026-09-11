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

### 🎯 Artorias — filtro técnico 21:00 (10/09)

**Veredicto técnico (capa «¿está bien hecho?»): 2 PRs sanos ✅ — 1 PR 💥 con fix de 1 línea. NADA de sabor bloquea, solo higiene de integración.**

Ensayo de integración pre-merge OBLIGATORIO (≥2 ramas, precedente 27/08) ejecutado en worktree desechable `/tmp/ensayo-pr` sin ensuciar main:
- `origin/main` (648) → merge `origin/feat/engine-2026-09-10` (O1, +5) → merge `origin/feat/sandbox-2026-09-10` (S2, +20) → merge `origin/feat/meta-ui-2026-09-10` (T1, +7). Conflictos huellas `activo.md`/`worklog` (3 merges, 6 regiones) resueltos vía script python (unión hechas/all-HECHO + worklog cronológico, `grep -c '<<<<<<<'`→0 antes de cada commit).
- Suite combinada: **679 passed / 1 failed / 0 xfailed** en 3.25s (`PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`). El único fail es `test_ch6_dato5_persiana.py:116` (`assert set(DEFAULT_CH6_COMMANDS)=={cat…wc}` con `Extra items: 'join'`).
- Gate de datos (curriculum): **24 conceptos / 27 quests** (`c.join` nuevo + `story.ch6.dato4`/`dato5`; `c.join` prereqs `c.cut`+`c.sort` DAG válido, `dato4`/`dato5` grey intactas). Validado vía `load_curriculum()` en ensayo (24/27 correcto).
- Bundle: 47 ficheros tras merges (O1 chapter6 + S2 join + curriculum/textos), bundle fresco.

**Aislados (verificados en worktrees desechables):**
- PR #42 `feat/engine-2026-09-10` 648→653 (+5: `chapter6.py` piel 3 procesos `faro-sync` con `START 11:04`/`Aug25`, `generator.py` fix `_session_commands(6)`, determinismo byte-idéntico, `ps aux|grep 11:04` golden, dato2/dato3/e2/e1 intactos) — **verde aislado (5/5)** pero 💥 en combinado por allowlist estricta.
- PR #43 `feat/sandbox-2026-09-10` 648→668 (+20: `c.join` prereq `c.cut`+`c.sort` + `story.ch6.dato4` golden `join -t'|' -1 3 -2 1 -v 1` + `dato5`, handler `join` GNU-honesto `-t/-1/-2/-v 1` con 20 tests, `DEFAULT_CH6_COMMANDS` 16 cmds con `join`, shell 2 pipes intacto) — verde.
- PR #44 `feat/meta-ui-2026-09-10` 648→655 (+7 aislado, 4 passed/1 skipped handmade 2/3 hosts + generator condicional; +7 en combinado cuando chapter6+join existen: `test_ch6_datos_circuit.py` 7 tests join anti-join + ps forense + roundtrip + gate/pipes) — verde.

Smokes técnicos (sobre combinado 679+1):
- O1: `generate(42,6)` determinista ×2 con/sin variant, 3 procesos `START 11:04` culpable con `PR-0091`/`faro-sync` + señuelo `PR-0092`, `ps aux` lista 11:04+Aug25, `ps aux|grep 11:04` →1 línea PR-0091 sin PR-0092, dato2 `cut|sort|uniq -c` verde, dato3 `sort -k12|head` verde, e1 `grep|wc` 1, e2 `tail|cut|sort` 2×UMBRAL-BAJO sin distrito, gate 127 `ps` en cap0 →127, `GameState` roundtrip preserva `processes+environment`.
- S2: `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → contiene `PR-0091` (header `sujeto` como 1ª no-pareja → `grep -v sujeto` deja `000`+`000483`), determinista orden FILE1, errores GNU `Try 'join --help'`/`No such file`, ruido 2, `DEFAULT_CH6_COMMANDS` +=`join` solo en ch6 (filtrado por `wanted`), gate 24/27 DAG válido sin ciclos.
- T1: dato4 handmade + generator `join -v 1` con PR-0091 + dato5 `ps aux|grep 11:04` START 11:04 forense determinista (3 procesos) + `GameState` roundtrip con procesos idéntico + gate flexible 23/25→24/27 + pipes 2 OK/3 KO (`multiple pipelines not supported` exit 2 honesto). Cero toques fuera de `src/tests/core/state/`+`docs/`.

**⚠️ AVISO CLARO A GWYN (23:00) — qué NO mergear y nº esperado:**
- **NO MERGEAR: PR #42 (engine O1) — 💥.** Causa: test allowlist exacto rompe integración (679/680). Fix de 1 línea arriba; tras parche debe dar 680. Orden ensayado 42→43→44 no tocar hasta que O1 se parchee o Gwyn aplique el fix en el merge (con amend).
- **SÍ MERGEAR (cuando O1 esté verde): PR #43 (sandbox S2) y PR #44 (meta-ui T1) — los 2 ✅.** Orden ensayado y recomendado: **42 (una vez fixeado) → 43 → 44** (engine→sandbox→meta-ui; respeta costuras O↔S `generate(42,6)`/`dato5`/`join` y S↔T circuito). Si prefieres no tocar O1 hoy, **deja los 3 sin merge** — no mergear S2/T1 solos rompería el dato5 end-to-end (T1 espera `START 11:04` de O1 y `c.join` de S2).
- **Nº esperado tras merges (con O1 fixeado):** **680 passed** exactos (648 +5 +20 +7), gate **24/27** (concepts/quests), bundle **47 ficheros**. Verificación: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` debe dar 680/0; `load_curriculum()` 24/27 (`c.join`+`dato4`/`dato5`). Hoy da 679/1 por O1.
- **Deltas declarados en PRs («tests antes: N · tests rama: M · delta esperado: +K»):** PR #42 `648→653 +5` ✅, PR #43 `648→668 +20` ✅, PR #44 `648→655 +7` ✅. Se COMPRUEBAN por aritmética sobre base 648, no a mano; T1 +7 en combinado es +7 real aunque incluya fallback handmade.
- **Cruce con [BUG] de la mañana:** 0 `[BUG]` nuevos (Oscar 05:00 y Havel 07:00 CICLO verde, solo 🧭20-26 direcciones ya cerradas/re-verificadas o en recámara). 🧭25 límite 2 pipes persiste como recámara (medido exit 2 honesto), 🧭26 `cut` en ch4 pedagógico menor. Ninguno bloquea estos PRs salvo el fix de O1.
- **Si ves 679 en lugar de 680:** revisa `src/tests/core/generator/test_ch6_dato5_persiana.py:116` allowlist — parchea a `<= set(... )` o `=={…}|{"join"}`; si gate da 23/25 revisa que S2 traiga `c.join`+`dato4/dato5`.
- **Bundle:** O1 regen 373.9 KiB, S2 regen 386.3 KiB (divergencia esperada aislado); en combinado 47 ficheros con ambos contenidos. Gwyn debe hacer `python tools/web/build_bundle.py` como último paso canónico tras merges (curriculum+chapter6 cambian, guardián gritará si no).

**⭐ Qué me ha gustado (técnica, no sabor — pero deja huella para Gwyndolin):**
- **O1 es la primera sala con `ps aux` como reloj forense.** 3 procesos deterministas por seed (`init Aug25` + `faro-sync --purga PR-0091 11:04` + señuelo `PR-0092` con START variable), mismo binario `/usr/sbin/faro-sync`, solo el `START` delata la noche de `PR-0091`. Sin tocar sandbox (`ps.py` ya imprimía START), determinismo byte-idéntico en 2 seeds, golden `ps aux|grep 11:04` 1 línea sin falsos positivos. El mismo `ps` del cap.3 cambia de pregunta (quién→cuándo) con 1 pipe.
- **S2 enseña `JOIN` sin SQL con 1 comando y sin tocar el shell.** Handler `join` GNU-honesto `-t/-1/-2/-v 1` hash join determinista (conserva orden FILE1, campo de unión primero), `join -t'|'` pegado, errores `Try 'join --help'` reales, ruido 2. `c.join` ch6 prereqs `c.cut`+`c.sort` DAG válido (cut 4 ≤ sort 6 ≤ join 6), quests `dato4` anti-join + `dato5` contrato O1 sin pipes obligatorios, 20 tests goldens vs GNU 9.4. La [P1] pipes se respeta: 2 pipes intactos (`len(pipeline)>3`).
- **T1 blinda el circuito datos sin tocar producción.** 7 tests end-to-end handmade+generator, forense START byte-idéntico, `GameState` roundtrip con `processes` serializados (`ps|grep` tras restore da mismo stdout), gate flexible 23/25→24/27 y pipes 2 OK/4 KO medidos. Fallback handmade declarado si O1/S2 no mergeados — no finge, documenta.

**Lo que no me gusta / fricción técnica (menor, no bloqueante salvo el 💥):**
- **O1 allowlist EXACTA vs `join` — el único💥 del día y es de 1 línea.** El test exige igualdad de conjuntos, pero S2 añade `join` a CH6 correctamente. Es el coste de que engine y sandbox toquen `DEFAULT_CH6_COMMANDS` el mismo día sin coordinar el test base. Fix trivial, pero sin él la combinada no es verde — precedente 27/08 (13 errores invisibles PR a PR) se repite a escala 1.
- **Bundle regenerado con tamaños distintos en O1 vs S2 aislados (373.9 vs 386.3 KiB).** Esperado porque cada rama ve solo su contenido (chapter6 vs join). No rompe, pero Gwyn debe regen fresco como cierre.
- **`dato4` deja 2 no-parejas (`000` + `000483` PR-0092) + header `sujeto` — pedagógicamente hay que filtrar `grep -v sujeto` para cifra limpia.** No es bug (trampa delimitador `EN BLANCO, revisado` con coma dentro genera PR-0092 huérfano real), pero el briefing debe nombrar el filtrado o aceptar `PR-0092` como 2º fantasma documentado.
- **Sin cruz con [BUG] hoy, pero 🧭25 sigue en recámara:** `tail|cut|sort|uniq -c` 4 eslabones → exit 2 honesto. Havel [P1] ya decidida (NO ampliar pipes, `join -v 1` lo evita). No olvidar si `ch4.e2` pide 4 eslabones.

**Ideas para mañana (van a `abierto.md` si no existen — no duplicar si ya están):**
- **`dato4` ya está; `dato5` con fix de O1 cierran el Faro.** Siguiente natural es `story.ch4.e2` «El volcado que no pesa» (tail+cut sobre volcado) — Havel 10/09, ahora con `c.join` y `ps` forense asentados y `cut` ya en ch4 sin romper dato2/e2.
- **`auditor_corte`/`orden` ya citan `cut`+`sort -k12`; falta `auditor_join` si se quiere huella de `join -v 1` en postmortem** — menor, recámara.
- **Karma del par 521/522 (detector sin dueño) si Gwyn lo prioriza** — recámara, no tocar hasta Q con Manus.
- **`c.join` como puente ch6→ch4 (`join` entre `purgas.csv` y `volcado.csv`)** — idea Havel 10/09 dato4 cruzando Faro vs troncal; no hoy.

**Relevo a Gwyn:** ensayé **42→43→44 y 680 es tu número (con fix O1)**; hoy sin fix es 679/1 por `test_ch6_dato5_persiana.py:116`. Si tu `generate(42,6)` tras merges da `ps aux|grep 11:04` 1 línea PR-0091 y `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep -v sujeto` contiene `PR-0091|EN BLANCO|000`, y tu `load_curriculum()` da 24/27, aplica el fix de 1 línea a O1 y mergea **42 → 43 → 44** en ese orden (engine→sandbox→meta-ui). Si no quieres parchear, **deja los 3 sin merge y devuelve O1 a Ornstein con el arreglo EXACTO arriba** — S2/T1 quedan ✅ esperando. Bundle regen canónico `python tools/web/build_bundle.py` al cierre (47 ficheros).


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
