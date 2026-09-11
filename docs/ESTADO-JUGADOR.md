# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (11/09 — MODO B: Faro dato4 + dato5 JUGABLES, cap. 4 y Faro completos)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya cruza tablas y lee el reloj: **Faro `dato4` «El cruce» (`join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → `PR-0091|EN BLANCO|000|--|ENSAYO`, anti-join 0 pipes, header `sujeto` + fantasma-2 `PR-0092` documentados) + `dato5` «La persiana» (`ps aux` 3 procesos deterministas, `ps aux | grep 11:04` → 1 línea `PR-0091` sin señuelo, mismo binario `faro-sync`) + Faro E2/E3/dato2/dato3/e1 intactos + cap. 4 COMPLETO (`cat /etc/hosts` descubre `faro`+`troncal-01`/`02`, `scp` copia `volcado.csv` TR-001/TR-101, `GameState` roundtrip) + `c.join` (ch6 prereq `cut`+`sort`) y `c.cut` en ch4.** `scp`/`join` siguen 127 fuera de su capítulo por allowlist (frontera deliberada).

**En main (680 passed / 0 xfailed, gate 24 conceptos / 27 quests, bundle 47 ficheros 390.5 KiB — merges #42/#43/#44 del 10/09 + FICHA dato4 de Manus 11/09 verificados):**
- **Faro dato4+dato5 jugables (O1+S1+T1+FICHA):** `generate(42,6)` → 3 procesos (`init Aug25` + `faro-sync --purga PR-0091 START 11:04` culpable + `faro-sync --purga PR-0092` señuelo `09:33` variable) → `Shell(DEFAULT_CH6_COMMANDS).execute("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv")` exit 0 `sujeto|…` + `000|PR-0091|EN BLANCO|--|ENSAYO|--|0|1|HOSP-47-C` + `000483|PR-0092|…|EN BLANCO, revisado` (coma-trampa genera 2º huérfano real); `join ... | grep PR-0091` exit 0 1 línea; `ps aux | grep 11:04` exit 0 1 línea `PR-0091` sin `PR-0092`/`Aug25`; determinismo byte-idéntico 42×2 y estable en seed 7/99; `ps` 127 fuera de cap. 3/6 por allowlist; `c.join` ch6 prereqs `c.cut`(4)+`c.sort`(6) DAG válido `cut(4) ≤ join(6)`.
- **Gate curricular:** 24 conceptos / 27 quests (`c.join` nuevo + `story.ch6.dato4`/`dato5` grey; `c.join` prereqs `c.cut`+`c.sort` DAG válido, `dato4` requires `c.join`, `dato5` requires `c.ps`). Quests: `story.ch6.dato4` «El cruce» + `dato5` «La persiana» + `story.ch6.e1/e2`+`dato2/dato3`+`story.ch4.e1` intactas.
- **Textos FICHA dato4 (Manus 11/09):** `story.ch6.dato4.beat/briefing/hint_1/hint_2/detail` con «La purga nombra; el registro calla», rutas absolutas, `-v 1` huérfanas, 3 líneas (cabecera+2 huérfanas), filtra con `| grep 000` → 2 huérfanas / `| grep PR-0091` → 1 fantasma, PR-0092 documentado como coma-trampa. Sin AI-slop.
- **Cap. 4 jugable + smoke:** `generate(42,4)` + `cat /etc/hosts` descubre 2 hosts (seed 1→3), `scp` copia TR-001/TR-101 con metadatos, `GameState` roundtrip, `generate` determinista, bundle fresco.
- **Faro Bandit re-verificado:** `ls`5 vs `ls -a`6 (`.nota-corte` oculta), LEEME relativo `0`+stderr vs absoluta `1`, coma-trampa `cut -d','` basura, goldens dato2/dato3/e2 exit 0, tríada Auditor `cut→corte`/`sort -k12→orden`, GNU `sort -k0` con `Try --help`.
- **Shell límites:** `tail -n +2 | cut -d'|' -f4 | sort` (2 pipes) exit 0, `cut|sort|uniq -c` exit 0, `tail|cut|sort|uniq -c` (3 pipes) → `multiple pipelines not supported` exit 2 honesto. `grep -v` vía pipe NO soportado (ver 🧭27).

**Para «jugable de principio a fin» sigue faltando:** **engine/game.py** orquestador, **inventario agregado multi-run**, **salas narrativas Faro e3+** y **quest `story.ch4.e2`** (suelo completo — hosts+scp+cut+join+ps ya están). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (dato4 join + dato5 ps + cap4 regresión + c.join frontera + pipe-limit) se ejecutó COMPLETA desde save limpio; el camino del novato sigue apto y la progresión ch4→Faro no rompe; `grep -v` es fricción menor documentada, no bloqueo.

## 🏃 Run de referencia (save limpio) — 11/09

*Nueva partida sobre generator real + Shell por capítulo (`new_session` + `DEFAULT_CH6_COMMANDS` / `DEFAULT_CH4_COMMANDS`). Zona 🔬 de Gwyn 11/09 ejecutada como primera prioridad.*

**Veredicto: APTO — el Faro ahora cruza tablas sin SQL y lee el reloj forense.**

1. **`dato4` «El cruce» — `join -v 1` cruza `purgas.csv`×`registro.csv` (cap. 6, mundo real):** `generate(42,6)` + `new_session().execute("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv")` → exit 0 `sujeto|purga_id|fecha|…` (header 1ª no-pareja) + `000|PR-0091|EN BLANCO|--|ENSAYO|--|0|1|HOSP-47-C` (fantasma que el registro esconde) + `000483|PR-0092|11-07|UMBRAL-BAJO|EN BLANCO, revisado|500|0|1|OH-UBA-14-0092` (2º huérfano real por coma-trampa `EN BLANCO, revisado`). `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep PR-0091` → exit 0 1 línea con `PR-0091` sin `PR-0092`; `generate(42,6)` byte-idéntico 2 llamadas; seed 7/99 mismo fantasma `PR-0091` estable. ✔
2. **Errores GNU `join` didácticos:** `join` sin operandos → exit 1 `join: missing operand` + `Try 'join --help'`; `join -t xx …` multi-char → exit 1; `join /nope.csv registro.csv` → exit 1 `No such file`. No muerden. ✔
3. **`dato5` «La persiana» — `ps aux` como RELOJ forense (cap. 6, mundo real):** `generate(42,6).room.fs.processes` → `init Aug25` (pid 1) + `faro-sync --purga PR-0091 START 11:04` (pid ~419) + `faro-sync --purga PR-0092 START 09:33` (pid ~434, señuelo variable por seed); mismo binario `/usr/sbin/faro-sync`, solo `START` delata la noche de `PR-0091`. `Shell.execute("ps aux")` → 4 líneas (cabecera+3), `ps aux | grep 11:04` → exit 0 1 línea `PR-0091` sin señuelo ni `Aug25`; `ps aux | grep PR-0091` → 1 línea; `ps aux | grep 09:33` → señuelo solo; rejugar 2× determinismo byte-idéntico (seed 42 y seed 7 idénticos salvo PID/START señuelo). ✔
4. **`c.join` frontera (allowlist):** `load_curriculum()` 24/27, `c.join` ch6 prereqs `c.cut`(4)+`c.sort`(6) DAG válido (2 ≤4 ≤6); `Shell(DEFAULT_CAP0_COMMANDS).execute("join")` → 127 `command not found`, `Shell(DEFAULT_CH4_COMMANDS).execute("join")` → 127, `Shell(DEFAULT_CH6_COMMANDS).execute("join --help")` → 0. Frontera 127 fuera de ch6 es deliberada (NO bug). ✔
5. **Faro + cap. 4 regresión:** `generate(42,4)` + `new_session().execute("cat /etc/hosts")` → exit 0 `10.6.0.5 faro` + `10.6.1.10 troncal-01` + `hosts=={faro,troncal-01}`; seed 1 → `troncal-02` + 3 hosts; `ls /etc` no descubre; `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → exit 0 `TR-001|faro|troncal-01|1024|OK` con metadatos; `GameState` roundtrip idéntico multi-host. ✔
6. **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **680 passed / 0 xfailed**, `generate(42,4/6)` deterministas, bundle 47 fresco, gate 24/27. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 11/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA (11/09): `cat /etc/hosts` descubre + `scp` copia + `ls` no descubre — hygiene allowlist resuelta.** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127 deliberada. No reabrir.
**5. 🧭25 — PERSISTE (observación documentada): límite 2 pipes (3 cmds) + redirección no soportada.** `tail|cut|sort` y `cut|sort|uniq -c` verdes separados; `tail|cut|sort|uniq -c` (3 pipes, 4 cmds) → exit 2 honesto. Redirección `>` → `syntax not supported`. No bloquea hoy (ninguna quest pide 3 pipes); `dato4` se diseñó en 0 pipes (`join -v 1`) evitando el límite.
**6. 🧭26 — PERSISTE (dirección pedagógica menor, no bug): `c.cut` ya vive en cap. 4, Faro e1 no es primer `cut`.** e1 solo pide `grep|wc`, dato2/e2 sí exigen `cut` por necesidad. Ningún camino rompe; Gwyn mantiene e1 sin `cut`.
**7. 🧭27 — NUEVO (fricción menor, no bloqueante): `grep -v` vía pipe NO soportado — `join | grep -v sujeto` falla.** Medido 11/09: `join -v 1 … | grep PR-0091` exit 0 1 línea (verde), `ps aux | grep 11:04` exit 0 1 línea (verde), pero `join … | grep -v sujeto` → exit 2 `grep: sujeto: No such file` y `grep -v sujeto /srv/…/purgas.csv` → mismo exit 2, y `ps aux | grep -v root` → exit 2. Causa: `texto.py:_run_grep` solo maneja `grep PATRON [FICHERO]` sin flags — `-v` se lee como patrón y `sujeto` como fichero. La FICHA de Manus ya lo sorteó (`| grep 000` / `| grep PR-0091` en briefing/hints, sin `-v`). No rompe el camino (dato4 se resuelve sin `-v`, filtrando positivo), pero la sugerencia clásica `grep -v` de Gwyn 10/09 no es ejecutable hoy. Informo, no decido: Gwyn decide si implementar `grep -v` o mantener el filtro positivo como lección.

## 👴 Progreso de veterano (20+ h → la run 30)

- **El Faro ya es crimen con DOS pruebas cruzables:** tras 20h el veterano domina `cut|sort|uniq` y `tail|cut|sort` del Faro; ahora el troncal añade `cat /etc/hosts→scp` y el Faro añade `join -v 1` (cruzar) + `ps aux|grep` (reloj). En la run 30, alternar `generate(42,6)`/`7`/`99` deja `PR-0091` siempre huérfano y `PR-0092` siempre 2º huérfano — el fantasma es estable, la coma-trampa es firma. `START 11:04` siempre delata al culpable; el señuelo `09:33`/`08:17` variable por seed es ruido que el veterano descarta en 1 pipe.
- **`join` y `ps` como verbos que cambian de pregunta sin cambiar sintaxis:** el veterano que aprendió `ps` en cap. 3 (quién corre) lo reusa en cap. 6 (cuándo empezó) con el mismo `ps aux | grep 11:04` — 1 pipe, 1 línea, 1 deducción. `join -v 1` con 0 pipes es el verbo de tablas que el veterano usa luego para sospechar que `purgas.csv` y `volcado.csv` también se pueden cruzar por `faro` (idea Havel 10/09 dato4 `purgas`×`volcado`).
- **El límite 2 pipes y `> ` como techo creativo, no muro:** el veterano ya encadena `tail|cut|sort` + `cut|sort|uniq -c` en dos líneas para contar sin header; el que intente `tail|cut|sort|uniq -c` recibe mensaje exacto y aprende el límite. Con `>` no disponible, «encadenar con `> /tmp`» no es alternativa hasta que llegue redirección — la FICHA dato4 ya evita el problema diseñando en 0 pipes. El `grep -v` no disponible enseña filtro positivo (`grep PR-0091`) en vez de negativo.
- **Hub/eco aún pendiente:** `c.join`/`c.ps-forense` dominados sin eco diegético (🧭9), inventario agregado multi-run sin cruzar runs (🧭17). Con `join -v 1` dejando `PR-0091` y `ps aux` dejando `START 11:04`, el eco del espejo de Gris («cruzaste tablas / leíste el reloj») es la pieza que daría cuerpo a dato4/5.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: dato4 JOIN + dato5 PERSIANA)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **680 passed / 0 xfailed** (gate `load_curriculum()` 24/27, `DEFAULT_CH6_COMMANDS` 16 cmds con `join`, bundle 47 ficheros 390.5 KiB). ✓
- **`dato4` «El cruce» — `join -t'|' -1 3 -2 1 -v 1` anti-join (ch6, mundo real):** `Shell(new_session(generate(42,6))).execute("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv")` → exit 0 `sujeto|…` + `000|PR-0091|EN BLANCO|--|ENSAYO` + `000483|PR-0092|…|EN BLANCO, revisado` (2 huérfanas reales, header como 1ª); `join … | grep PR-0091` → 1 línea `PR-0091`; `join` sin operandos / multi-char `-t` / inexistente → exit 1 GNU honesto (`Try --help` / `No such file`); determinismo byte-idéntico 42×2; `c.join` ch6 prereqs `c.cut`(4)+`c.sort`(6) DAG válido; `join` 127 en cap. 0/4 frontera. ✓
- **`dato5` «La persiana» — `ps aux` forense (ch6, mundo real):** `generate(42,6).room.fs.processes` → 3 (`init Aug25` + `faro-sync --purga PR-0091 START 11:04` + `faro-sync --purga PR-0092 START 09:33`); `Shell.execute("ps aux | grep 11:04")` → exit 0 1 línea `PR-0091` sin señuelo; `ps aux` 4 líneas; determinismo 2× idéntico (seed 42 y 7/99 mismo `PR-0091` 11:04, señuelo variable); `ps` 127 fuera de ch6 frontera. ✓
- **Pipe-limit + `grep -v`:** `tail|cut|sort` (2 pipes) y `cut|sort|uniq -c` (2 pipes) verdes; `tail|cut|sort|uniq -c` (3 pipes) → `multiple pipelines not supported` exit 2; `grep -v` vía pipe/file → exit 2 `grep: sujeto: No such file` (flag no soportado — briefing FICHA ya usa `grep 000`/`grep PR-0091` positivo). ✓
- **Regresión cap. 4 + Faro Bandit:** `cat /etc/hosts` descubre 2-3 hosts donde `ls` no, `scp` copia TR-001 con metadatos, `GameState` roundtrip idéntico; `ls`5 vs `ls -a`6, LEEME relativo, coma-trampa, goldens dato2/dato3/e2, Auditor tríada intactos. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23/24 CERRADAS** (re-verificadas 11/09), **🧭25/26 PERSISTEN** (límite 2 pipes + cut en ch4), **🧭27 NUEVO** (`grep -v` vía pipe no soportado, FICHA ya lo sortea con filtro positivo). Ninguna rompe el camino. La pregunta de la zona «¿dato4/dato5 enseñan con necesidad real? ¿ps commuting dice o chirría?» se responde: **sí — `join -v 1` es el verbo que faltaba para el cruce (1 comando, 0 pipes, sin SQL, 2 testigos que se contradicen) y `ps aux|grep 11:04` hace del `ps` del cap. 3 un reloj forense (quién→cuándo) con 1 pipe legible; el límite 2 pipes y `grep -v` no empañan la lección.**

CICLO: verde — la zona 🔬 se ejecutó completa (mundo real ch6 dato4+5 + cap4 + fronteras) y el viaje del novato sigue apto; el Faro cruza tablas y lee el reloj sin perder su necesidad pedagógica.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
