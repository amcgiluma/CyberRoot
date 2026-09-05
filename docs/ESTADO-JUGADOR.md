# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (05/09 — MODO B: cap. 6 «Faro» con familia conteo COMPLETA + post-mortem lector)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya incluye **la cadena completa del Faro con la familia conteo cerrada**: generar la sala-dato de la Lista (`generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS)` con 15 cmds), listar los 4 ficheros de `/srv/camara-faro`, y jugar la historia de la purga que no debió existir cortando la tabla con `cut`. Además, **el cap. 3 ya es circuito completo de verbo**: leer → elevar → facturar → citar.

**En main (567 passed / 0 xfailed, gate 22/22, bundle 44 ficheros — PRs #25/#26/#27 mergeados 04/09):**
- **Cap. 6 «Faro» JUGABLE con alfabeto completo (15 cmds):** `cut` cierra la familia `head/tail/sort/uniq/cut` (prereq `c.uniq`, ruido 1 frugal). Pista real de M1 `cut -d'|' -f4,12 /srv/camara-faro/purgas.csv | uniq -c` existe y responde (exit 0, columnas distrito+puntuación; `cut -d'|' -f4` → distrito, `cut` sin `-f` → `you must specify…` exit 1 GNU-honesto, línea sin delim intacta). Sala-dato 4 ficheros (`registro.csv`, `purgas.csv`, `censo-borrador.csv`, `aviso-faro.txt`) con fila canónica `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` y cebo `censo-borrador.csv` (canónico `grep ENSAYO|wc -l` → 1, cebo `grep 000|wc -l` → 0, relativo sin cd → 0 con stderr `No such file`).
- **Cap. 3 circuito sudo con lectura verificada (O1+S1, 03-04/09):** `generate(42,3)` → credencial `/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt` + par lazy 521/522 (`ceniza --ventana` vs `censo --vigilar-censo`). Gate: `sudo` sin leer → **exit 1, ruido 0, stderr nombra la orden exacta** `cat /srv/.../orden-ceniza.txt` y NO firma `auth.log`; tras `cat` → `read_marks` viaja en estado, `sudo` eleva (cat:1 + sudo:3), firma `tick N operator : sudo …` y appendea. Determinismo intacto.
- **Post-mortem tríada (O1 04/09, 7 tests):** `build_postmortem` resuelve `auditor_text` vía `data.textos`: lectura → `lectura verificada — …orden-ceniza.txt consta como leída` (sorted por codepoint, determinista); ciega → `elevación sin lectura previa — ninguna orden consta como leída`; sin sudo (cap. 0) → **1 línea, byte-idéntico, sin `auditor_lectura`** (el tutorial no gana texto nuevo). Nunca `line_key` crudo, fallback honesto.
- **Puerta web (T1+T2, 04/09):** bundle 44 ficheros (`src/core/**/*.py` + `src/data/*.json` → `/lib/...`), guardián `test_bundle_fresco.py` verde en fresco / **rojo ante mutación** (`echo "# x" >> src/core/common/rng.py` → `bundle stale`, revert → verde), URL `https://cyberroot-psi.vercel.app` con `?chapter=3&seed=42` jugable (orden → ps → kill) y bucle muerte con `auditor_text` + reiniciar. Verificado por Gwyn en Chromium real; Havel lo corroboró sin navegador (hueco declarado, no bug).
- **Render v0:** `python -m render.demo` → `cap0-room.png` 320×180 sha `c84450443e835609` estable, prompt `cero@oficina-vecinal-muelle-norte:/$` con cwd real.

**Para «jugable de principio a fin» sigue faltando:** el **engine/game.py** orquestador que encadene capítulos consecutivos en un entrypoint único (se ejercita vía `generate`+`Shell`), el **inventario agregado multi-run** (qué dominas cruzando runs — 🧭9), y **salas E2/E3 del Faro** que exijan `cut` por necesidad (hoy `cut` es verbo disponible pero sin quest que lo pida). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (Faro con alfabeto completo + tríada lector + guardián) se ejecutó COMPLETA desde estado limpio y el camino aguanta: la Lista se corta como tabla, el 0 miente solo por Lista (no por ruta cuando usas absoluta), el sudo se gana leyendo y el Auditor te cita con `path` exacto o te acusa sin invención. Hallazgos son dirección y veterano, no roturas.

## 🏃 Run de referencia (estado limpio) — 05/09

*Nueva "partida" sobre el generator real + Shell pública, sin FS de test, sin atajos. Como manda la zona 🔬 de Gwyn (05/09), recorrí el Faro con `cut` y la tríada lector/ciega/sin-sudo.*

**Veredicto: APTO — el Faro ya se lee como TABLA, no solo como texto filtrado.**

1. **La sala-dato nace en `/` y expone 4 ficheros:** `ls /srv/camara-faro` → `aviso-faro.txt`, `censo-borrador.csv`, `purgas.csv`, `registro.csv`. `grep PR-0091 purgas.csv` → `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` (sujeto 000, cruza `HOSP-47-C` fragmento 2). ✔
2. **La historia se juega contando y cortando:** canónico `grep ENSAYO /srv/camara-faro/purgas.csv | wc -l` → **1**; cebo `grep 000 /srv/camara-faro/censo-borrador.csv | wc -l` → **0**; con ruta relativa sin `cd` → **0 con stderr `grep: purgas.csv: No such file`** (wc decide exit, el cero miente por ruta pero el stderr avisa — briefing ya usa absolutas, validado). ✔
3. **La familia conteo es alfabeto completo con `cut`:** `cut -d'|' -f4 /srv/camara-faro/purgas.csv` → `distrito` (col 4); `cut -d'|' -f4,12 purgas.csv | uniq -c` → distrito+puntuación con `uniq -c` (exit 0, ruido 1+1); `cut -d'|' -f4,12 registro.csv | uniq -c` → cabecera `distrito|puntuacion` + valores; `cut /srv/.../purgas.csv` sin `-f` → **exit 1** `you must specify a list… Try 'cut --help'` (GNU exacto); línea sin delim intacta (mock pendiente de sala, pero handler ya la deja pasar). `head -n 2`/`tail -n 1`/`sort|head -n 3` siguen GNU-honestos. Ya no es catálogo: es verbo. ✔
4. **El Faro se lee como TABLA cuando usas `cut`:** la pista M1 existe y funciona; con `grep` solo ves la fila (1 línea), con `cut` ves la columna. El jugador que conoce `cut` separa campos sin trampear; el que no, sigue ciego con `grep`. Es alfabeto, no isla. ✔
5. **Circuito sudo + tríada lector (cap. 3 sobre generator real):** `generate(42,3)` → `cat orden-ceniza.txt` legible (`AUTORIZACION: CENIZA`, `Vigencia: esta sesion`), `read_marks` nace vacío. `sudo cat /etc/hosts` SIN leer → **exit 1, ruido 0, stderr `elevation denied: you have not read Ceniza's order. Read it first: 'cat /srv/.../orden-ceniza.txt'`**, sin firma en `auth.log`. Tras `cat orden` → `read_marks=['…/orden-ceniza.txt']`, `sudo cat /etc/hosts` → **exit 1 por `cat: No such file` pero con ruido `cat:1 + sudo:3` y firma `tick 1 operator : sudo cat …`**. `build_postmortem` → lectura: `lectura verificada — …orden-ceniza.txt consta como leída…`; ciega: `elevación sin lectura previa — ninguna orden consta como leída`; cap. 0 sin sudo → **1 línea, byte-idéntico**, sin segunda línea. ✔
6. **Puerta web (verificación headless del guardián):** `test_bundle_fresco.py` → verde; mutación → rojo con `bundle stale: faltan /lib/core/sandbox/commands/cut.py`; revert → verde. `build_bundle.py` → 44 ficheros, `curriculum`+`textos` con claves `lectura`/`ciega` dentro. Interactividad `?chapter=3&seed=42` + muerte con `auditor_text` verificada por Gwyn en Chromium; sin navegador local declaro hueco honesto (no bug). ✔
7. **Gate 127 intacto + determinismo + render:** `sudo/ps/kill/cut` en cap. 0/2 → `exit 127: sh: command not found`; `generate(42,0)` y `generate(42,6)` `fs.to_dict` byte-idénticos entre seeds iguales; `python -m render.demo` → `cap0-room.png` sha `c84450443e835609` estable. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭17 — `cut` disponible pero sin BOON ni briefing que lo enseñe (descubrible ≠ enseñado).** Medido: `DEFAULT_CH6_COMMANDS` expone `cut`, `c.cut` existe (prereq `c.uniq`, cap. 6), y la pista M1 funciona, pero `story.ch6.e1` no menciona `cut` ni hay boon que lo regale — el jugador lo encuentra si prueba `cut` o si lee la pista, si no, resuelve la E1 con `grep|wc` y nunca toca la tabla. No rompe (E1 canónica sigue siendo `grep ENSAYO|wc -l` → 1), pero la pregunta de diseño de Gwyn se responde: **hoy la Lista se PUEDE leer como tabla, pero el novato la lee a ciegas salvo que sea curioso por flags**. Dirección: E2 del Faro debe exigir `cut` por necesidad (scaffold sin permisos visibles salvo cortando columnas, o pregunta que solo `cut` responde — ej. “¿qué distritos tienen puntuación 0?” exige `-f4,12`), y el boon `c.cut` debería aparecer como hallazgo en el propio Faro (fichero nota del operador muerto) antes de E2. No es bug — es el siguiente escalón natural que Gwyn ya tenía en recámara (`sort -k12`, `cut` en E2/E3).

**2. 🧭18 — La pista M1 `cut -d'|' -f4,12 | uniq -c` hoy no agrupa (cada línea es “1 distrito”) porque `uniq -c` sin `sort` previo no deduplica.** Medido: `cut -d'|' -f4,12 purgas.csv | uniq -c` → `1 distrito`, `1 UMBRAL-BAJO`, `1 MUEL-01`, `1 --` (4 líneas, cada una 1). Con `sort | uniq -c` sí agruparía si hubiera duplicados. La pista de Manus es correcta GNU-honesta (exit 0), pero el veterano que busque “¿cuántos por distrito?” esperará `sort | uniq -c`. No es bug (GNU así funciona), es **didáctica**: la E2 que use `cut+uniq` debería enseñar `sort` primero (`cut … | sort | uniq -c`) para que `uniq -c` cumpla su promesa de contar. Dejo para Gwyndolin como detalle de quest E2.

**3. 🧭19 — La tríada del post-mortem ya ES memoria de lector, pero la variante ciega NO dispara en el juego real v0 (el gate rechaza antes).** Medido: `sudo` sin leer → rechazo con ruido 0 antes de elevar → `postmortem` ciega solo dispara si inyectas un `event.sudo` defensivo (dict `{"history":[{"argv":["sudo",...]}]}`) — en el mundo real con credencial nunca llega a haber elevación ciega. Es capa defensiva para mundos sin credencial (cap. futuro sin llave), no bug, como Gwyn ya documentó. Para el veterano significa que “elevar sin leer” deja huella en el rechazo, no en el `auth.log` — coherente con “intentar no es delinquir”.

## 👴 Progreso de veterano (20+ h → la run 30)

- **La familia conteo ya es ALFABETO jugable, no lista:** con `cut` la quinteta `sort/head/tail/uniq/cut` + `grep/wc` permite al veterano en la run 30 encadenar `grep ENSAYO|wc -l` (1), `cut -d'|' -f4,12 | sort | uniq -c` (mapa distrito→puntuación), `head/tail` para muestrear crudo. El siguiente escalón —`sort -k12` (ordenar por puntuación, pista de Manus) y `uniq -c` con duplicado fantasma— aún no es quest, pero la base ya permite “leer Vesper contando y cortando”. La dopamina de sinergia pipeline (§5.2) tiene suelo completo.
- **El sudo como verbo del veterano (con gate lector):** el gate “leer antes de elevar” cuesta un `cat` por run (~1 ruido, trivial para el veterano) y protege el primer contacto del novato — pesa más el beat pedagógico que la comodidad, como defendí el 02/09. La marca `read_marks` viaja en el save (roundtrip memoria+disco verificado por Smough), así que el veterano que limpia la run ve su `auditor_text` citar la ruta exacta — memoria, no invención.
- **El Faro como rejugable por seed:** la Lista (4 ficheros) con `PR-0091|EN BLANCO|000|--|ENSAYO` + `HOSP-47-C` cruza el fragmento 2 sin lore nuevo; la piel por seed es determinista (`fs.to_dict` idéntico), la historia no. El veterano en la run 30 verá misma anomalía (ENSAYO=1) con topología distinta — rejugabilidad por combinación (§5.3), bien.
- **Puerta web como espejo real:** `?chapter=3&seed=42` (`orden → sudo → ps aux 521/522 → kill -9 522` + muerte con `auditor_text`) es la lección completa del cap. 3 en el navegador; `?chapter=3&seed=99` rechaza nombrando la orden, `?seed=` convierte cada bug report en reproducción exacta. El veterano ya puede compartir runs por URL — Balatro compartible sin backend.
- **Sigue faltando el inventario AGREGADO multi-run** (mi 🧭3 del 30/08): `GameState` por run persiste `knowledge` + `read_marks`, pero no hay sistema de partidas que sepa “ya dominas cut” cruzando runs. Es la llave del Hub y del Espejo de Gris (§4.3) y del eco visible 🧭9 (hoy el unlock es dato, no momento).

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: Faro con alfabeto completo + tríada lector)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **567 passed / 0 xfailed** (529 base +7 O1 +29 S1 +2 T1/T2). Gate datos **22/22**. ✓
- **Faro con `cut` en vivo sobre generator real:** `generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS)` → `cut -d'|' -f4,12 | uniq -c` (exit 0), `cut -d'|' -f4` (distrito), `cut` sin `-f` (exit 1 `you must specify…`), `grep ENSAYO|wc -l` →1, cebo →0, `grep PR-0091` → `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C`. ✓
- **Tríada lector verficada:** `sudo` sin leer → rechazo nombrando `/srv/.../orden-ceniza.txt` (ruido 0, sin firma); `cat orden` → `read_marks`; `sudo` tras leer → eleva+factura+firma; `build_postmortem` → lectura cita `path` exacto, ciega acusa `ninguna orden consta como leída`, cap0 sin sudo → 1 línea byte-idéntica. ✓
- **Guardián bundle + puerta web (headless):** `test_bundle_fresco` verde / rojo ante mutación / verde tras revert; bundle 44 ficheros con `curriculum`+`textos` (claves lectura/ciega dentro); `?chapter=3` y muerte con `auditor_text` en Chromium verificado por Gwyn (hueco local declarado). ✓
- **Gates + determinismo + render:** `generate(42,0/6)` byte-idénticos, gate 127 intacto cap0/2/3, render sha `c84450443e835609` estable. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭15 VALIDADA** (briefing con rutas absolutas ya en prosa), **🧭16 RESUELTA** (par lazy en cap. 3), **🧭14b CERRADA** (sudo se gana leyendo + tríada que lo cita), **🧭17 NUEVA** (cut disponible pero sin boon/quest que lo enseñe — E2 debe exigirlo por necesidad), **🧭18 NUEVA** (pista M1 `cut|uniq -c` sin `sort` no agrupa — E2 debe ser `cut|sort|uniq -c`), **🧭19 OBSERVACIÓN** (variante ciega defensiva, no dispara en juego real v0 — capa para mundos sin credencial). Ninguna rompe el camino. Filtro: apto — la familia conteo cerró y el Auditor ya tiene memoria de lector.

CICLO: verde — la zona 🔬 se ejecutó completa sobre el generator real y el viaje del novato suma el alfabeto conteo entero (cut como tabla) + el gate lector citado por el Auditor; el veterano ya puede cortar la Lista y compartir runs por URL; los hallazgos son siguiente escalón y matiz didáctico, ninguno bloquea la run.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
