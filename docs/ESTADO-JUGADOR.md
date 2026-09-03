# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (03/09 — MODO B: cap. 6 «Faro» JUGABLE + cap. 3 real sobre generator)

**¿Hay algo que jugar de principio a fin?** Sí — y hoy por primera vez el viaje del novato incluye **la cadena narrativa completa del Faro**: generar la sala-dato de la Lista (`generate(42,6)` + `Shell` con `DEFAULT_CH6_COMMANDS`), listar los 4 ficheros de `/srv/camara-faro`, y jugar la historia de la purga que no debió existir. Además, **el cap. 3 ya es generable desde main** (`generate(seed,3)`) — el circuito sudo se recorre sobre el generator real, no sobre el FS de test.

**En main (515 passed / 0 xfailed, gate 21/21 — todo mergeado anoche PRs #16/#19/#20/#21):**
- **Cap. 6 «Faro» JUGABLE (O3+S2, 02/09):** `chapter6.py` + wiring `generator.py` + quest `story.ch6.e1` (grey, requires `c.grep/c.head/c.pipe/c.sort/c.tail/c.uniq/c.wc`). Sala-dato con 4 ficheros (`registro.csv`, `purgas.csv`, `censo-borrador.csv`, `aviso-faro.txt`). Fila canónica `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` presente en `purgas.csv`; cebo `censo-borrador.csv` (cabecera + comentario, `grep 000 | wc -l` → 0 con exit 0 — la primera mentira pedagógica). `DEFAULT_CH6_COMMANDS` (14 cmds: cat/cd/cp/env/grep/head/kill/ls/ps/sort/sudo/tail/uniq/wc) expone la familia conteo.
- **Cap. 3 real sobre generator (O1+fix #16):** `generate(seed,3)` produce la sala sudo con credencial narrativa en `/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt` (`AUTORIZACION: CENIZA`) y `auth.log` en `/var/log/auth.log`. Circuito sudo medido hoy: con credencial presente `sudo` eleva/firma/factura; sin credencial → rechazo diegético. **Baseline 03/09:** el gate sigue siendo por EXISTENCIA (🧭14b decidida anoche por Gwyn como (b) «se gana LEYENDO», aún no implementada — Smough la ejecuta hoy a las 16:00; mido el estado actual como línea base).
- **Kill/señales v0 (S1, 02/09):** `kill -9 522` mata, `kill -HUP 521` → `--reloaded` + `HUP_521=1` en env, golden GNU `kill: (522) - No such process`. Gate 127 intacto en cap. 0/2 (kill no existe ahí). Nota: en el generator real del cap. 3 el FS nace sin procesos inyectados (v0 solo credencial) — kill solo es operable sobre FS de test con procesos; no es bug, es alcance v0.
- **Primera VOZ resuelta (O4+T1):** `build_postmortem` resuelve `auditor_text` vía `data.textos` — «Expediente 000: se mantiene dentro del presupuesto. Pico de la sesión: grep (3 puntos). Continuidad del ensayo: estable.» Nunca `line_key` crudo ni crash.
- **Render v0 (T1):** `python -m render.demo` → `cap0-room.png` 320×180 con sha estable `c84450443e835609`, prompt `cero@oficina-vecinal-muelle-norte:/$` con cwd real.

**Para «jugable de principio a fin» sigue faltando:** el **engine/game.py** orquestador que encadene runs de capítulos consecutivos en un entrypoint único (se sigue ejercitando vía API/`generate`+`Shell`), el **inventario agregado multi-run** (qué dominas cruzando runs — 🧭9), y que el **cap. 3 inyecte procesos en el generator** (hoy solo test FS tiene el par ceniza/censo). Nada de esto rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (cap. 6 JUGABLE + cap. 3 real) se ejecutó COMPLETA desde estado limpio y el camino aguanta: la Lista se lee, el cebo miente, la familia conteo responde, el sudo eleva/firma, la voz pinta texto, el gate 127 aguanta y el render es evidencia. Hallazgos son dirección y alcance v0, no roturas.

## 🏃 Run de referencia (estado limpio) — 03/09

*Nueva "partida" sobre el generator real — sin FS de test, sin atajos. Como manda la zona 🔬 de Gwyn, recorrí el Faro desde `/` (spawn de la sala) y el circuito sudo completo del cap. 3 midiendo la baseline de 🧭14b antes de que Smough la cierre hoy.*

**Veredicto: APTO — el Faro ya es un camino, no una demo.**

1. **La sala-dato nace en `/` y expone 4 ficheros en `/srv/camara-faro`:** `ls /` → `srv`; `ls /srv/camara-faro` → `aviso-faro.txt`, `censo-borrador.csv`, `purgas.csv`, `registro.csv` — los 4 ficheros de Manus/CENSO-LISTA. ✔
2. **La historia de la Lista se juega con grep/wc/pipe:** `grep PR-0091 /srv/camara-faro/purgas.csv` → `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` (el sujeto 000 y la purga de nadie, cruzando `HOSP-47-C` del fragmento 2); canónico `grep ENSAYO purgas.csv | wc -l` con ruta absoluta → **1**; cebo `grep 000 censo-borrador.csv | wc -l` → **0 con exit 0**. Con `cd /srv/camara-faro` previo, mismas cifras con rutas relativas. Sin `cd` y con ruta relativa (`grep ENSAYO purgas.csv | wc -l` desde `/`) → **0 con exit 0 + stderr `grep: purgas.csv: No such file`** — el 0 miente por ruta, y el sistema avisa en stderr sin tumbar el pipe (GNU honesto). Es la trampa pipe-0 jugable: el novato descuidado ve 0 y el veterano lee el stderr. ✔
3. **La familia conteo es alfabeto, no isla:** `head -n 2 purgas.csv` (cabecera + PR-0144), `tail -n 1` (PR-0091), `sort purgas.csv | head -n 3` ordena por bytes — los 4 comandos de la familia responden con semántica GNU y están expuestos por `DEFAULT_CH6_COMMANDS`. Ya no es catálogo en `curriculum.json`: es verbo jugable en la sala-dato. ✔
4. **Circuito sudo del cap. 3 sobre generator real (baseline 🧭14b):** `generate(42,3)` nace en `/`; `cat /srv/.../orden-ceniza.txt` → orden firmada por Ceniza con `AUTORIZACION: CENIZA` y `Vigencia: esta sesion`. `sudo cat /etc/hosts` (o cualquier envuelto) ejecutado SIN leer la orden → **exit 1 por `cat: No such file` pero con ruido `cat:1 + sudo:3` y firma en `/var/log/auth.log` (`tick 1 operator : sudo cat …`)** — es decir, elevó y facturó igualmente. Tras leer la orden, idéntico resultado (misma firma appendeada, misma factura base+premium). Medido en seeds 42 y 99: el gate sigue siendo por EXISTENCIA del fichero, no por haberlo leído. Es la baseline que Gwyn fijó como (b) para Smough hoy — no es regresión, es el estado previo al fix. ✔ (Con su matiz de dirección abajo.)
5. **La primera VOZ resuelve con la forma exacta:** `build_postmortem(shell.to_dict(), {noise_budget:12})` sobre la sesión cap. 6 (`grep ENSAYO | wc -l`) → `auditor_text: «Expediente 000: se mantiene dentro del presupuesto. Pico de la sesión: grep (3 puntos). Continuidad del ensayo: estable.»` — dato sobre emoción, sello de continuidad rematando. Nunca `line_key` crudo. ✔
6. **Gate 127 intacto:** `sudo`/`ps`/`kill` en cap. 0/2 → `exit 127: sh: command not found` — la puerta del cap. 6/3 no se abre antes de tiempo. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭15 — El Faro nace en `/` y el cebo miente por ruta relativa (briefing).** Medido: `grep ENSAYO purgas.csv | wc -l` desde `/` → 0 con stderr `No such file` (el wc decide el exit). Con ruta absoluta o con `cd /srv/camara-faro` previo → 1 correcto. Leído con la silla del novato: el jugador que abre el Faro sin `cd` y usa la ruta relativa del briefing (si lo hubiera) verá el 0 mentiroso SIN saber que es trampa de ruta — el stderr sí avisa, pero el exit 0 no lo delata. No rompe el camino (la ruta absoluta funciona), pero la prosa del cap. 6 y el briefing de `story.ch6.e1` deberían anclar la **ruta absoluta `/srv/camara-faro/`** o sugerir el `cd` previo. Ya lo apuntó Gwyn anoche como «nota para el diseño de la sala (coherente con 🧭13)»; hoy lo confirmo con medición. No es bug — es orientación. Detalle en `notas-manana.md` (🧭15).

**2. 🧭16 — El cap. 3 del generator nace sin procesos: `ps aux` vacío, `kill` sin blanco.** Medido: `generate(42,3)` → `fs.processes=()` y `env={}`; `ps aux` solo imprime cabecera, `kill -9 522` → `kill: (522) - No such process`. El par ceniza-521/censo-522 solo existe en el FS handmade de `test_session_kill.py`, no en el generator. El `chapter3.py` lo declara: «Sin procesos/variables por defecto: los inyecta el generator si la quest así lo exige» — alcance v0 es solo credencial. Consecuencia para el veterano: `kill` no es jugable en el cap. 3 real hoy; la sala sudo y la sala de procesos son islas distintas. No rompe el camino (kill funciona sobre su FS de test y el gate 127 aguanta), pero limita la sinergia cap. 3 → cap. 6 que la zona imaginaba. Propuesta de dirección para Gwyn (informo, no decido): inyectar el par 521/522 en el FS del cap. 3 cuando la quest sea de procesos, o documentar que el cap. 3 v0 es solo credencial. Detalle en `notas-manana.md` (🧭16).

**3. 🧭14b — Baseline confirmada: sudo aún por existencia, no por lectura.** Medido en dos seeds (42, 99): `sudo` sin leer eleva/firma/factura igual que tras leer. Es el estado que Gwyn decidió anoche como (b) «se gana LEYENDO» y que Smough implementa hoy a las 16:00 — no es regresión, es la línea base antes del fix. La prosa de Manus ya está alineada (cap. 3 E4/E5), el gate vendrá después. Sin acción hoy.

## 👴 Progreso de veterano (20+ h → la run 30)

La zona de hoy era el primer Faro jugable; mi capa larga es si el loop aguanta a la run 30.

- **La familia conteo ya es ALFABETO (no isla):** con `sort`/`head`/`tail`/`uniq` jugables en la sala-dato, el veterano puede encadenar `grep ENSAYO purgas.csv | wc -l` (canónico 1) y verificar con `head`/`tail` el contenido crudo. El siguiente escalón —`sort -k12` (columna puntuación) y `uniq -c` como detector de duplicados— aún no está expuesto como objetivo, pero la base ya permite «leer Vesper contando». Correcto como alfabeto; la dopamina de sinergia pipeline (§5.2) tiene dónde nacer.
- **El Faro como lectura, no como ejercicio:** la fila `PR-0091|EN BLANCO|000|--|ENSAYO` con `HOSP-47-C` cruza el fragmento 2 y el registro (Vera Montejo, Roldán, Herrera) sin necesidad de lore nuevo. El veterano en la run 30 verá la misma Lista pero con piel que cambia por seed (determinista) — la historia se mantiene, la topología no. Eso es rejugabilidad por combinación (§5.3), no por prosa única por run. Bien.
- **El sudo como verbo del veterano (pre-fix):** el gate ambiental es cómodo para el veterano (cero fricción para reutilizar la llave) pero pierde el beat pedagógico del novato. Con la (b) de Gwyn, el veterano pagará un `cat` por run (trivial) y el novato aprenderá qué autoriza — pesa más proteger el primer contacto (cap. 3) que la comodidad del veterano, como ya argumenté el 02/09.
- **El kill como isla del veterano:** hoy el veterano que busque `kill -9 522` en el generator real no encontrará blanco — solo en el FS de test. Para la run 30, el cap. 3 debería ofrecer una sala donde el par 521/522 viva en el mundo; si no, la familia procesos queda como lectura (`ps aux` vacío) sin bisturí. Es la deuda fina que dejo como 🧭16.
- **Sigue faltando el inventario AGREGADO multi-run** (mi 🧭3 del 30/08): `GameState` por run persiste su `knowledge`, pero no hay sistema de partidas que sepa «ya dominas grep» cruzando runs. Es la llave del Hub y del Espejo de Gris (§4.3).

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: cap. 6 JUGABLE + cap. 3 real)

- **Smoke del conjunto:** suite desde raíz → **515 passed / 0 xfailed** exactos (gate de datos 21/21). ✓
- **Cap. 6 JUGABLE verificada en vivo sobre generator real:** `generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS)` desde `/` → 4 ficheros en `/srv/camara-faro`; `grep PR-0091` → `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C`; canónico `grep ENSAYO | wc -l` → 1 (abs) / 0 miente (relativa sin cd, con stderr) ; cebo `grep 000 censo-borrador.csv | wc -l` → 0 con exit 0 ; `head`/`tail`/`sort` responden GNU-honestos. ✓
- **Cap. 3 real sobre generator:** `generate(42,3)` y `generate(99,3)` producen la credencial `/srv/.../orden-ceniza.txt` legible; `sudo` sin leer vs tras leer — misma elevación/firma/factura (baseline 🧭14b, Smough la cierra hoy). `auth.log` appendea firma. ✓
- **Kill/señales sobre FS de test (alcance v0):** `kill -9 522` mata (desaparece de `ps aux`), `kill -HUP 521` → `--reloaded` + `HUP_521=1` en env, golden `kill: (522) - No such process` para pid inexistente, gate 127 en cap. 0/2 intacto. Sobre generator real: `ps aux` vacío (alcance v0, no bug). ✓
- **Primera VOZ resuelta:** `build_postmortem(...).auditor_text` → «Expediente 000: se mantiene dentro del presupuesto… Continuidad del ensayo: estable.» ✓
- **Render v0 evidencia:** `python -m render.demo` → `cap0-room.png` sha `c84450443e835609` estable, prompt `cero@oficina-vecinal-muelle-norte:/$` con cwd real. ✓

## Hallazgos de la run (dónde aprieta el viaje)

1. **🧭15 — Spawn en `/` + ruta relativa = 0 mentiroso con stderr pero exit 0.** La sala-dato del Faro nace en `/`; el pipe `grep X purgas.csv | wc -l` con ruta relativa falla silencioso en exit (wc decide) pero grita en stderr. Con ruta absoluta o `cd` previo, correcto. Es la primera mentira pedagógica jugable — pero el briefing debería anclar la ruta absoluta `/srv/camara-faro/` para no confundir orientación con trampa. Dirección para Gwyn, no bug.
2. **🧭16 — Cap. 3 del generator sin procesos: kill no jugable en mundo real.** `generate(...,3)` → `processes=()`; `ps aux` vacío; `kill` solo vive en el FS de test. Alcance v0 documentado, no regresión — pero limita el veterano. Dirección para Gwyn.
3. **🧭14b baseline confirmada** (sudo ambiental hasta el fix de hoy de Smough). Sin acción nueva.

*(Detalle y propuestas de dirección: `backlog/notas-manana.md` 🧭, sobrescritas hoy. El camino principal no está roto.)*

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭14b DECIDIDA por Gwyn (sudo se gana LEYENDO) — baseline medida hoy (aún ambiental, Smough la implementa hoy 16:00);** **🧭12/🧭13 RESUELTAS** (voz y prompt); **🧭15 NUEVA** (spawn `/` + ruta relativa — anclar ruta absoluta en briefing del Faro); **🧭16 NUEVA** (cap. 3 sin procesos en generator — inyectar par 521/522 o documentar alcance). Ninguna rompe el camino. Filtro: apto — el Faro ya es camino jugable y el alfabeto conteo dejó de ser isla.

CICLO: verde — la zona 🔬 (Faro JUGABLE + cap. 3 real) se ejecutó completa sobre el generator real y el viaje del novato suma el capítulo 6 con historia legible; la familia conteo responde; el sudo y la voz aguantan; los hallazgos son orientación y alcance v0, ninguno bloquea la run.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
