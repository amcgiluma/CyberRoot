# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (10/09 — MODO B: cap. 4 JUGABLE por primera vez con viaje completo)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato es **la cadena Faro (6 ficheros, `.nota-corte` oculta, LEEME relativo, coma-trampa, tríada Auditor) + quest `story.ch6.e2` «La que no pesa» (`tail -n +2 | cut -d'|' -f4 | sort`, 2 pipes) + cap. 4 COMPLETO (`cat /etc/hosts` descubre `faro`+`troncal-01`/`02`, `scp` copia `volcado.csv` TR-001 con metadatos, `GameState` roundtrip) + `c.cut` ya viviendo en cap. 4 (prereq `wc`) y `c.scp` en cap. 4 (prereq `cut`).** `scp` sigue 127 en cap. 6 por allowlist (frontera deliberada — cap. 4 nace CON red, cap. 6 sin red).

**En main (648 passed / 0 xfailed, gate 23 conceptos / 25 quests, bundle 46 ficheros 370.4 KiB — merges #39/#40/#41 del 09/09 verificados por Manus 10/09 03:00):**
- **Cap. 4 jugable (O1+S1+T1 merges):** `generate(42,4)` → `/etc/hosts` (`127.0.0.1 localhost` + `# Troncal — red cap.4 (faro + troncal)` + `10.6.0.5 faro` + `10.6.1.10 troncal-01`, y `troncal-02` 10.6.1.11 en seed 1/7/13 vía `fork("ch4-hosts").below(2)`) → `Shell(DEFAULT_CH4_COMMANDS).execute("cat /etc/hosts")` exit 0 descubre ambos (y 3 en seed 1), `ls /etc` exit 0 con `hosts` pero `hosts=={}` intacto (solo lectura descubre), re-leer no duplica, `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` exit 0 deja `/tmp/volcado.csv` `id|origen|destino|bytes|estado` + `TR-001|faro|troncal-01|1024|OK` con owner/mode/mtime copiados, `scp faro:/srv/camara-faro/purgas.csv` OK igual, `GameState(shell).to_dict/from_dict` idéntico multi-host. `generate(42,4)` determinista byte-idéntico (2 llamadas iguales).
- **Gate curricular:** 23 conceptos / 25 quests (`c.scp` nuevo cap. 4 prereq `c.cut`; `c.cut` movido 6→4 prereq `c.wc` 2, DAG válido `wc(2) ≤ cut(4) ≤ scp(4) → ch4.e1(4)` y `cut(4) ≤ dato2/dato3(6)` intacto). Quests: `story.ch4.e1` «La llave prestada» (blue, `requires c.scp`, briefing con rutas absolutas `/etc/hosts` + `troncal-01:/srv/archivo-troncal/volcado.csv` + aviso 2 pipes), `story.ch6.e1`/`e2`/`dato2`/`dato3` intactas, `ch5` 4 quests cap. 5.
- **Faro intacto + pipe-limit:** `tail -n +2 | cut -d'|' -f4 | sort` (2 pipes) exit 0 `--/MUEL-01/UMBRAL-BAJO×2` sin `distrito`, `cut|sort|uniq -c` exit 0 con header, `tail|cut|sort|uniq -c` (3 pipes, 4 eslabones) → `sh: multiple pipelines not supported in this session: chain them one at a time` exit 2 (límite documentado T1, no bug). Redirección `>` → `sh: syntax not supported` (shell `|`-only hoy) — encadenar con `> /tmp/x` no viable hasta que llegue redirección.
- **Faro Bandit re-verificado:** `ls`5 vs `ls -a`6 (`.nota-corte` oculta con `cut -d'|' -f4 | sort | uniq -c`), LEEME relativo `0`+stderr vs absoluta `1`, coma-trampa `cut -d','` basura, goldens dato2/dato3/e2 exit 0, tríada Auditor intacta.
- **Puerta web / smoke:** `generate(42,6)` byte-idéntico salvo hosts Faro, `scp`/`ssh` 127 en cap. 6 por frontera, bundle 46 fresco, suite 648.

**Para «jugable de principio a fin» sigue faltando:** **engine/game.py** orquestador, **inventario agregado multi-run**, **salas narrativas Faro e3+** y **quests `story.ch4.e2+` + `dato4/dato5`** (suelo completo — hosts+scp+cut ya están). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 se ejecutó COMPLETA desde save limpio: viaje cap. 4 `cat→scp→cat→GameState` determinista, Faro antes/después del troncal comparado, pipe-limit medido con dato exacto; el camino del novato sigue apto y la progresión ch4→Faro no rompe.

## 🏃 Run de referencia (save limpio) — 10/09

*Nueva partida sobre generator real + Shell por capítulo (`new_session` + `DEFAULT_CH4_COMMANDS` / `DEFAULT_CH6_COMMANDS`). Zona 🔬 de Gwyn 10/09 ejecutada como primera prioridad.*

**Veredicto: APTO — el cap. 4 es jugable por primera vez y no rompe el Faro.**

1. **`cat /etc/hosts` descubre donde `ls` no (ch4 + Faro, mundo real):** `generate(42,4)` + `new_session().execute("cat /etc/hosts")` → exit 0 `127.0.0.1 localhost` + `# Troncal...` + `10.6.0.5 faro` + `10.6.1.10 troncal-01` + `hosts=={faro,troncal-01}`; `new_session(g42).execute("ls /etc")` → exit 0 `hosts` + `hosts=={}` (solo lectura descubre); seed 1 → `10.6.1.11 troncal-02` + 3 hosts, seed 42→2 hosts determinista; `generate(42,6)` → `10.6.0.5 faro` solo, `ls /etc` no descubre igual. Re-leer `cat` no duplica. `GameState(shell).to_dict/from_dict` idéntico con 2 y 3 hosts. ✔
2. **`scp` copia con metadatos (ch4) y 127 en ch6 por frontera:** `sh42.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/")` → exit 0 deja `TR-001|faro|troncal-01|1024|OK` con owner `lumen`/`troncal` mode `644`; `scp faro:/srv/camara-faro/purgas.csv /tmp/` OK igual dejando `purgas.csv`; `sh42.execute("scp notroncal:/x /tmp/")` → exit 1 `no descubierto — léelo en /etc/hosts` ruido 0 (didáctico); seed 1 → `scp troncal-02:/srv/archivo-troncal/volcado.csv /tmp/b.csv` → `TR-101|faro|troncal-02|4096|OK`. En ch6 `Shell(DEFAULT_CH6_COMMANDS).execute("scp faro:...")` → 127 `command not found` (frontera deliberada, no bug). ✔
3. **Quest `story.ch4.e1` «La llave prestada» (blue, `requires c.scp`):** curriculum 23/25, `c.cut(4←wc)` → `c.scp(4←cut)` → `story.ch4.e1(4←scp)` DAG válido; textos `story.ch4.e1.title/beat/brief/briefing/hint_1/hint_2` con `/etc/hosts`, `troncal-01`, `/srv/archivo-troncal/volcado.csv`, `faro 10.6.0.5`, aviso `Respeta el límite de 2 pipes`; golden `cat /etc/hosts` + `scp troncal-01:volcado.csv /tmp/` exit 0 verificado vía `new_session` determinista. ✔
4. **Faro ANTES vs DESPUÉS del troncal — `c.cut` ya vive en ch4:** `c.cut` chapter 4 prereq `c.wc`(2) — `story.ch6.e1` NO requiere `cut` (solo grep/head/pipe/sort/tail/uniq/wc), `dato2/dato3/e2` SÍ requieren `cut` (y siguen verdes con `cut` en 4 ≤ 6). Jugando Faro PRIMERO (sin pasar por ch4) el jugador resuelve `story.ch6.e1` con `grep|wc` sin tocar la tabla — `cut` no se enseña por necesidad en e1, pero sí en `dato2` (`cut -d'|' -f4 | sort | uniq -c` → `1 -- / 1 MUEL-01 / 2 UMBRAL-BAJO / 1 distrito` con header) y `e2` (`tail -n +2 | cut -d'|' -f4 | sort` → `--/MUEL-01/UMBRAL-BAJO×2` sin `distrito`). Jugando troncal PRIMERO, `cut` ya se domina sobre `volcado.csv` (`cut -d'|' -f1 /tmp/volcado.csv` → `id/TR-001/TR-002/TR-003`) y el Faro lo REUSA — no duplica la lección, la mantén. Ningún camino rompe; el Faro no pierde su necesidad de `cut` (dato2/e2 la garantizan), solo e1 sigue sin exigirla. ✔
5. **Límite 2 pipes medido (🧭25):** `tail -n +2 | cut -d'|' -f4 | sort` (2 pipes) exit 0 sin fantasma; `cut|sort|uniq -c` (2 pipes) exit 0; `tail|cut|sort|uniq -c` (3 pipes, 4 cmds) → exit 2 `sh: multiple pipelines not supported in this session: chain them one at a time`; `echo >`, `tail >`, `pipe | ... > /tmp/x` → exit 2 `sh: syntax not supported in this session: it runs one pipeline at a time (chaining, redirection and globbing arrive later)` — redirección aún no existe, así que "encadenar con > /tmp" no es alternativa viable hoy. Ninguna quest activa pide 3 pipes (`dato4` sería la primera candidata). ✔
6. **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **648 passed / 0 xfailed**, `generate(42,4)` determinista, `generate(42,6)` intacto, bundle 46, gate 23/25. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 10/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA (10/09): `cat /etc/hosts` descubre + `scp` copia + `ls` no descubre — hygiene allowlist resuelta.** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp` de fábrica, ch6 conserva 127 deliberada. No reabrir.
**5. 🧭25 — PERSISTE (observación documentada): límite 2 pipes (3 cmds) + redirección no soportada.** `tail|cut|sort` y `cut|sort|uniq -c` verdes separados; `tail|cut|sort|uniq -c` (3 pipes) → exit 2 honesto. Redirección `> /tmp/x` → `syntax not supported` — el consejo "encadenar con >" del briefing ch4.e1 no es ejecutable hasta que el shell soporte `>`. No bloquea hoy (ninguna quest pide 4 eslabones); `dato4` debe diseñarse cabiendo en 2 pipes o esperar ampliación a 3 pipes con ADR.
**6. 🧭26 — NUEVO (dirección pedagógica menor, no bug): `c.cut` ya vive en cap. 4, el Faro e1 deja de ser primer sitio donde se enseña `cut`.** e1 solo pide `grep|wc`, dato2/e2 sí exigen `cut` por necesidad. Si el jugador hace Faro ANTES del troncal, aprende `cut` en `dato2` (no en e1); si hace troncal primero, lo aprende sobre `volcado.csv` y lo reusa en Faro. La progresión sigue enseñando `cut` con necesidad real (dato2/e2), pero e1 ya no es su puerta — decisión validada por DAG (`cut` 4 ≤ 6). Informo, no decido: Gwyn decide si e1 debe exigir `cut` en el futuro o si e1 queda como conteo y dato2/e2 como tabla.

## 👴 Progreso de veterano (20+ h → la run 30)

- **El cap. 4 ya es el segundo alfabeto jugable:** tras 20h el veterano domina `grep|wc`+`cut|sort|uniq` del Faro; ahora el troncal añade `cat /etc/hosts → scp host:ruta` como segundo eje "leer dónde → copiar desde dónde". En la run 30, el jugador que alterna semillas (42→99→1) ve `faro`+`troncal-01` siempre y `troncal-02` solo en 1/7/13 — el determinismo por seed es trofeo coleccionable, no azar. `TR-001|faro|troncal-01|1024|OK` vs `TR-101|faro|troncal-02|4096|OK` son firmas por host que el veterano reconoce sin abrir el briefing.
- **Faro + troncal como par que enseña `cut` dos veces con dos tablas distintas:** `purgas.csv` (`|` con header+dup PR-0092, `f4=distrito`) y `volcado.csv` (`|` con header simple, `f1=id`). El veterano que domina `cut -d'|' -f4` en el Faro hace `cut -d'|' -f1 /tmp/volcado.csv | sort | uniq -c` en el troncal sin aprender nada nuevo — MISMO verbo, otra tabla. La sinergia `cut`→`scp` (Havel 05/09 "el : es un | que ya sabes cortar", ahora en `c.cut→c.scp`) es el primer ejemplo jugable de "lo que cortaste en la tabla lo cortas en la dirección `host:ruta`".
- **El límite 2 pipes como techo creativo, no muro:** el veterano ya encadena `tail|cut|sort` + `cut|sort|uniq -c` en dos líneas para contar sin header; el que intente `tail|cut|sort|uniq -c` recibe el mensaje exacto y aprende el límite. Con `>` no disponible, la "segunda pasada" es re-leer el fichero con otro pipeline sobre el mismo FS — la didáctica "encadenar" hoy es "re-leer con otro tubo", no "volcar a /tmp". La decisión de ampliar a 3 pipes (toca `shell.py:_PIPE_MSG` `>3`→`>4`, 1 línea + tests) solo compensa si `dato4` demuestra que 4 eslabones son lección mejor que 2+2.
- **Hub/eco aún pendiente:** `c.cut`/`c.scp` dominados sin eco diegético (🧭9), inventario agregado multi-run sin cruzar runs (🧭17). Con `scp` copiando entre FS y `GameState` guardando `hosts`+`known_hosts`+`host_stack`, el veterano ya mueve ficheros entre hosts y su save lo recuerda — el eco del espejo de Gris ("hoy copiaste entre máquinas") es la pieza que daría cuerpo al momento ch4.e1, igual que `cut` lo dio en el Faro.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: cap. 4 despierta con red completa)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **648 passed / 0 xfailed** (gate `load_curriculum()` 23/25, `DEFAULT_CH4_COMMANDS` 13 cmds con `ssh/scp`+`cut`, bundle 46 ficheros 370.4 KiB). ✓
- **`?chapter=4&seed=42` → `cat /etc/hosts` descubre `faro`+`troncal-01` (seed 1 → `troncal-02`) + `ls /etc` NO descubre + re-leer no duplica:** `Shell(new_session(generate(42,4))).execute("cat /etc/hosts")` → exit 0 con `10.6.0.5 faro` + `10.6.1.10 troncal-01`, `hosts=={faro,troncal-01}` (seed 1 → 3 incl. `10.6.1.11 troncal-02`), `Shell(generate(42,4)).execute("ls /etc")` → exit 0 `hosts` + `hosts=={}` (solo lectura descubre). ✓
- **`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` copia con metadatos (TR-001) + `GameState` roundtrip:** `new_session(g42).execute("scp troncal-01:.../volcado.csv /tmp/")` → exit 0 deja `TR-001|faro|troncal-01|1024|OK` con owner/mode/mtime, `scp faro:/srv/camara-faro/purgas.csv /tmp/` OK, `cat /tmp/volcado.csv` + `cut -d'|' -f1` verde, `GameState(shell).to_dict/from_dict` idéntico 2 y 3 hosts, `generate(42,4)` determinista byte-idéntico, `generate(42,6)` intacto (Faro `10.6.0.5 faro` solo). ✓
- **Quest `story.ch4.e1` completa:** curriculum `c.scp(4←c.cut)` + `c.cut(4←wc)`, gate 23/25, textos `story.ch4.e1.*` con rutas absolutas y aviso 2 pipes, `scp` no-descubierto → exit 1 ruido 0 `no descubierto — léelo en /etc/hosts` (didáctico). ✓
- **Faro ANTES del troncal vs DESPUÉS:** `story.ch6.e1` no exige `cut`, `dato2/dato3/e2` sí — Faro sigue enseñando `cut` por necesidad (dato2/e2) aunque e1 no; troncal enseña `cut` sobre `volcado.csv` y Faro lo reusa. Ningún camino rompe. ✓
- **Límite 2 pipes + redirección no soportada:** `tail|cut|sort` (2 pipes) y `cut|sort|uniq -c` (2 pipes) verdes; `tail|cut|sort|uniq -c` (3 pipes) → `multiple pipelines not supported: chain them one at a time` exit 2; `> /tmp/x` → `syntax not supported in this session` — dato para decisión [P1] mañana. ✓
- **Faro re-verificado:** `ls`5 vs `ls -a`6, LEEME relativo, coma-trampa, goldens dato2/dato3/e2, Auditor tríada, GNU `sort -k0` con `Try --help`. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23/24 CERRADAS** (re-verificadas 10/09; 24 resuelta por `DEFAULT_CH4_COMMANDS`), **🧭25 PERSISTE** (límite 2 pipes + redirección no viable), **🧭26 NUEVO** (cut ya vive en ch4 — Faro e1 no es primer sitio). Ninguna rompe el camino. La pregunta de la zona «¿viaje completo hasta cap. 4 + Faro antes/después + límite 2 pipes?» se responde: **sí — `cat /etc/hosts` descubre 2-3 hosts donde `ls` no, `scp` copia TR-001 con metadatos y el save lo guarda, Faro sigue enseñando `cut` por necesidad en dato2/e2 aunque e1 no lo pida, y el límite 2 pipes aguanta sin romper ninguna quest activa; la redirección `>` aún no existe.**

CICLO: verde — la zona 🔬 se ejecutó completa (mundo real ch4 + ch6 + `c.cut` 6→4 comparado) y el viaje del novato sigue apto; la red dejó de ser stub para ser camino y `cut` viajó del Faro al troncal sin perder su necesidad.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
