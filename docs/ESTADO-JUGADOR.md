# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (06/09 — MODO B: cap. 6 «Faro» cerrado: E2 corta + E3 ordena + Auditor que cita tu corte)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya incluye **la cadena completa del Faro como alfabeto**: generar la sala-dato de la Lista (`generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS)` con 15 cmds), listar los **6 ficheros** de `/srv/camara-faro` (4 visibles + LEEME + .nota-corte), y jugar la historia de la purga que no debió existir cortando la tabla con `cut` y ordenándola con `sort -k`. Además, el cap. 3 sigue siendo circuito completo de verbo: leer → elevar → facturar → citar.

**En main (590 passed / 0 xfailed, gate 22/23, bundle 44 ficheros — PRs #28/#29/#30 mergeados 05/09 noche):**
- **Cap. 6 «Faro» JUGABLE con alfabeto cerrado + 2 quests nuevas (e2/e3):** `cut` cierra la familia `head/tail/sort/uniq/cut`; `sort -k/-t/-n` cierra la lectura VERTICAL. Pista real `.nota-corte` existe y enseña `cut -d'|' -f4 | sort | uniq -c` (Bandit: hallazgo). Sala-dato 6 ficheros (`registro.csv`, `purgas.csv`, `censo-borrador.csv`, `aviso-faro.txt`, `LEEME.txt`, `.nota-corte`) con fila canónica `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` y cebo `censo-borrador.csv` (canónico `grep ENSAYO|wc -l` → 1). E2 golden `cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c` → exit 0 (4 líneas: distrito/UMBRAL-BAJO/MUEL-01/--, con header incluido); E3 golden `sort -t'|' -k12 -n /srv/camara-faro/purgas.csv | head -n 3` → 3 líneas con **PR-0091 al frente** (el más cerca del 0, el fantasma). Cebo relativo `grep ENSAYO purgas.csv | wc -l` desde `/` → `0` con `stderr grep: No such file` + exit 0 del wc (mentira honesta intacta).
- **Auditor que CITA tu corte (O1 05/09):** `build_postmortem` con `cut -d'|' -f4` en history → añade `auditor_corte` (`column: 4, pattern: |`) y `auditor_corte_text: "Expediente 000: corte registrado — columna 4 (|). Continuidad del ensayo: estable."` (nunca clave cruda, nunca expone datos del censo). Sin `cut` → informe **byte-idéntico** a ayer (1 línea). `sort -k12` solo NO dispara corte (correcto: E3 no corta, ordena). Con la tríada lector (`lectura`/`ciega`/`sin sudo`) el Auditor ya es interrogatorio con **dos memorias**: qué leíste y qué cortaste.
- **Sort GNU-honesto (S1 05/09):** `sort -k0` → `field number is zero: invalid field specification '0'` (exit 2), `sort -t ab` → `multi-character tab 'ab'` (exit 2), con `Try 'sort --help'`. Líneas sin columna → fallback vacío sin crash. `cut -f` sin `-f` → `you must specify a list…` exit 1. Todo contra coreutils 9.4 verificado.
- **Cap. 3 circuito sudo con lectura verificada + lazy 521/522:** `generate(42,3)` → credencial + par demonio; `sudo` sin leer → exit 1 ruido 0 con orden nombrada, sin firma; tras `cat` → `read_marks` + `sudo` eleva/firma/appendea. `kill -9 522` borra, `kill -HUP 521` → `--reloaded` + `HUP_521=1`.
- **Render v0 + puerta web + guardián:** `python -m render.demo` → `cap0-room.png` sha `c84450443e835609` estable; bundle 44 fresco (`test_bundle_fresco.py` verde en fresco / rojo ante mutación verificado ayer); `?chapter=6&seed=42` jugable por URL (web slice 2).

**Para «jugable de principio a fin» sigue faltando:** el **engine/game.py** orquestador que encadene capítulos consecutivos (se ejercita vía `generate`+`Shell`), el **inventario agregado multi-run** (qué dominas cruzando runs — 🧭9), y **salas narrativas del Faro** (E2 «La que no pesa» / E3 «La persiana» de la prosa, bloqueadas por **deuda namespace e2/e3** — ver `activo.md`). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (Faro cerrado E2/E3 + Auditor que cita tu corte + GNU) se ejecutó COMPLETA desde estado limpio y el camino aguanta: la Lista se corta y se ordena con goldens GNUn-honestos, el 0 miente solo por Lista (no por ruta cuando usas absolutas), el Auditor te cita la columna exacta o te calla, y el novato puede hallar la `.nota-corte` (aunque hoy sin sigilo — ver hallazgo). Hallazgos son dirección y matiz UX, no roturas.

## 🏃 Run de referencia (estado limpio) — 06/09

*Nueva "partida" sobre el generator real + Shell pública, sin FS de test, sin atajos. Como manda la zona 🔬 de Gwyn (06/09), recorrí el Faro con E2/E3 y el Auditor que cita.*

**Veredicto: APTO — el Faro ya se juega como ALFABETO completo (horizontal + vertical) y el Auditor ya tiene memoria de proceso.**

1. **La sala-dato nace en `/` y expone 6 ficheros:** `ls /srv/camara-faro` → `aviso-faro.txt`, `censo-borrador.csv`, `purgas.csv`, `registro.csv`, `LEEME.txt`, `.nota-corte` (6 — novedad: LEEME + nota). `grep PR-0091 purgas.csv` no está en el `ls` demo pero `grep PR-0091 /srv/camara-faro/purgas.csv` no existe como 1 línea suelta: ahora la tabla tiene 4 filas (header + 3 purgas: UMBRAL-BAJO, MUEL-01, --), la PR-0091 es la **última** en cat crudo y la **primera** tras `sort -k12 -n` (el orden vertical delata al 000). ✔
2. **E2 «El corte de la Lista» — hallazgo Bandit + pregunta que SOLO `cut` responde:** `cat /srv/camara-faro/.nota-corte` → `# si quieres saber qué distritos hay y cuántos vecinos por distrito, # corta la columna: cut -d'|' -f4 … | sort | uniq -c` (pista exacta, con ruta absoluta). `cut -d'|' -f4 purgas.csv | sort | uniq -c` → `1 -- / 1 MUEL-01 / 1 UMBRAL-BAJO / 1 distrito` (4 líneas, header contado — ver hallazgo 🧭22). `grep ENSAYO|wc -l` → 1 no responde «qué distritos» — **sin `cut` la pregunta se queda sin respuesta**. El novato que hace `ls` ya ve la nota hoy (ver 🧭20). ✔
3. **E3 «Los más cerca del cero» — la lectura VERTICAL que solo `sort -k` responde:** `sort -t'|' -k12 -n /srv/camara-faro/purgas.csv | head -n 3` → `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` al frente, seguido de UMBRAL-BAJO y MUEL-01. `cat purgas.csv | head -n 3` muestra el orden crudo (0091 última) — **sin `-k12 -n` el 000 no sale primero**. `sort -t'|' -k12` + `sort -t'|' -k12 -n` + `-k2` con `|` probados GNU-honestos. ✔
4. **El cebo de ruta + LEEME sigue honesto:** `grep ENSAYO purgas.csv | wc -l` desde `/` → `0` con `stderr grep: purgas.csv: No such file` (wc decide exit 0 — mentira honesta). `LEEME.txt` hoy es mínimo (`Nota operativa — usar purgas.csv directamente ahorra tecleo.`) — no invita a relativa, la trampa es la **posición** del jugador en `/`, no el cebo escrito. Canónico con absoluta → 1 intacto. ✔
5. **El Auditor CITA tu corte (O1):** `Shell(fs, cwd="/").execute("cut -d'|' -f4 … | sort | uniq -c")` + `build_postmortem(sd, {noise_budget:12})` → `lines_resolved` gana segunda línea `Expediente 000: corte registrado — columna 4 (|)…` con `auditor_corte {column:4, pattern:|}` (nunca expone datos). `grep|wc` sin `cut` → `lines_resolved` de 1 línea byte-idéntica a ayer (sin corte). `sort -k12` solo → sin corte (correcto). Determinista por orden de history, sin imports sandbox. ✔
6. **GNU-honestidad de S1 verificada:** `sort -k0` → `field number is zero` exit 2, `sort -t ab` → `multi-character tab 'ab'` exit 2 con `Try 'sort --help'`, `cut` sin `-f` → `you must specify…` exit 1, línea sin delim intacta. `sort | head -n 3` pipeline intacto. ✔
7. **Tríada lector + gate 127 + determinismo + render intactos:** `sudo` sin leer sigue rechazando nombrando orden con ruido 0; `generate(42,6, contract_id=ch6.e2)` `fs.to_dict` byte-idéntico; `generate(42,0)` y `generate(42,6)` deterministas; `cap0-room.png` sha `c84450443e835609` estable; `sudo/ps/kill/cut` en cap0 → exit 127. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — `.nota-corte` NO está escondida: `ls` sin `-a` ya la muestra (Bandit a medias).** Medido: `ls /srv/camara-faro` → lista `.nota-corte` entre los 6 ficheros; `ls -a` idéntico (añade prefijo `/srv/camara-faro:`). La nota del operador muerto debería ser **hallazgo** que solo `ls -a` revela (idea P2 Havel 28/08: mitad oculta del mundo en dotfiles), pero hoy el sandbox muestra dotfiles con `ls` plano (mismo defecto que Havel señaló el 28/08 y que se quiso convertir en mecánica). Consecuencia: el novato encuentra la solución de E2 sin buscar — E2 deja de ser «descubrimiento» para ser «lectura». No rompe (E2 sigue exigiendo `cut`), pero **diluye la pregunta de diseño de Gwyn**: «¿el novato encuentra la nota SIN cartel?» hoy se responde «sí, sin buscar». Dirección: `sandbox/ls` debe filtrar `.*` sin `-a` cuando Smough toque flags, o bien renombrar la nota sin punto (`nota-corte.txt`) y asumir hallazgo visible (decisión de diseño para Gwyn: ¿hallazgo escondido o visible?).

**2. 🧭21 — `LEEME.txt` como cebo de ruta es hoy casi mudo.** Medido: `LEEME.txt` = 1 línea `Nota operativa — usar purgas.csv directamente ahorra tecleo.` No invita a relativa ni ahorra tecleo real; el cebo medido es la **posición en `/`** (relativa → 0 mentiroso), no el fichero. La zona 🔬 describía `LEEME.txt` como «te invita a relativa (si caes: grep … desde / → 0 con stderr)»; el fichero no cumple esa invitación — el 0 mentiroso se produce igual sin leer LEEME. No rompe, pero el cebo narrativo no se lee como trampa diegética. Dirección: nutrir `LEEME.txt` con la invitación explícita que la zona promete (`"prueba grep ENSAYO purgas.csv | wc -l"` sin ruta) o documentarlo como cebo ambiental (spawn en `/`) sin culpar al fichero. Dueño: Manus + `chapter6.py` (contenido de LEEME).

**3. 🧭22 — E2 cuenta el header `distrito` como distrito (uniq -c con cabecera).** Medido: `cut -d'|' -f4 purgas.csv | sort | uniq -c` → `1 -- / 1 MUEL-01 / 1 UMBRAL-BAJO / 1 distrito` (4 líneas, `distrito` es la cabecera). El jugador que responde «¿qué distritos hay?» contaría un distrito fantasma. Es la consecuencia de que `purgas.csv` tenga header en la misma columna; GNU-honesto, no bug, pero didácticamente invita a `tail -n +2` o `grep -v distrito`. Dirección: o bien el scaffold de E2 usa `registro.csv` (quizá sin header problemático) o la golden canónica de E2 excluye header (`tail -n +2 purgas.csv | cut …` o `grep -v purga_id`), o se asume que el veterano aprende a filtrar cabecera como paso extra. No bloquea (la quest valida exit 0, no el contenido exacto), pero el veterano en la run 30 notará el ruido.

## 👴 Progreso de veterano (20+ h → la run 30)

- **El Faro ya es rejugable por SEED con dos lecturas cruzadas:** E2 horizontal (`cut | sort | uniq -c` → mapa distrito→conteo) + E3 vertical (`sort -k12 -n | head` → ranking por puntuación con 000 al frente) forman el **alfabeto conteo completo**. El veterano en la run 30 puede encadenar `grep ENSAYO|wc -l` (1, ancla), `cut -f4 | sort | uniq -c` (4×1, hoy sin duplicado — ver 🧭22), y `sort -k12 -n | head` (000 primero). Con N=500 seeds el harness podría medir «tabla vs a ciegas» (idea P3 Havel 05/09) — el determinismo por seed ya lo permite.
- **El Auditor como interrogatorio con memoria de proceso:** con dos cortes (`lectura` + `corte`) el post-mortem ya cita **qué leíste** y **qué columna cortaste** (pattern `|` + column `f4`), sin exponer datos. La variante sin `cut` queda byte-idéntica — el veterano que optimiza factura ve su `auditor_corte` como trofeo de «leí la tabla» (idea P3 Havel «El Auditor cita tu columna» ya materializada). El siguiente escalón natural es `paste`/`diff` como cierre azul (LUZ PLENA) y `sort -k12` citado también si se corta + ordena en la misma sesión.
- **El hub/eco sigue pendiente:** el unlock `c.cut`/`c.sort` existe en datos pero sigue sin eco diegético visible (mi 🧭9 del 30/08 + 🧭17 de Havel). El veterano que domina `cut` no ve cambiar el stock de Gris ni el Hub — es la llave del Espejo de Gris (§4.3) y del HOSP-47-C cruzado por `env`. La deuda `inventario agregado multi-run` sigue viva (P3 30/08): cada run parte de `GameState` fresco, no hay «ya dominas cut» cruzando runs.
- **Rejugabilidad por combinación (§5.3) verificada:** con 22 conceptos / 23 quests y 6 superficies de variación (piel/boons/Pacto/karma/recuerdo/seed), dos runs por seed 42 y 99 darían purgas distintas pero la misma anomalía ENSAYO=1 y el mismo ranking 000-primero — variedad por combinación, no por prosa única (correcto según DESIGN §5.3).

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: Faro cerrado E2/E3 + Auditor que cita tu corte)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **590 passed / 0 xfailed** (567 base +6 #28 +8 #29 +8 #30). Gate datos **22/23** (22 conceptos / 23 quests, e2 `c.cut+c.uniq+c.sort`, e3 `c.cut+c.sort+c.head`). Bundle 44 ficheros (310 KiB). ✓
- **Arco E2/E3 sobre generator real desde save limpio:** `generate(42,6, contract_id=e2)` → `cut -d'|' -f4 | sort | uniq -c` exit 0 (4 líneas con header); `generate(42,6, e3)` → `sort -t'|' -k12 -n | head -n 3` → 3 líneas PR-0091 al frente. `.nota-corte` enseña `cut | sort | uniq -c` (Bandit) y `LEEME.txt` presente pero mudo. Cebo relativo → 0 con stderr, absoluta → 1. ✓
- **Auditor que cita tu corte (O1):** `build_postmortem` con `cut -d'|' -f4` → `auditor_corte_text` cita `columna 4 (|)`; sin `cut` → byte-idéntico (1 línea). `sort -k12` solo → sin corte (correcto). ✓
- **GNU S1 + determinismo + render + gate 127:** `sort -k0` / `multi-character tab` → exit 2 con mensaje exacto; `generate(fs.to_dict)` byte-idéntico; render sha `c84450443e835609` estable; cap0 `cut/sort` → 127. ✓
- **Deuda namespace e2/e3 confirmada:** `story.ch6.e2/e3` ocupan IDs de la prosa narrativa (ver `activo.md` y `historia/INDICE.md`). No rompe juego, bloquea planificación narrativa completa del Faro. No abrir [BUG] — es deuda de diseño para Gwyndolin. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭17/18/19 CERRADAS** (materializadas en E2/E3 + Auditor corte + `sort | uniq -c` con `sort` previo). **🧭20 NUEVA** (`.nota-corte` visible sin `-a` — hallazgo a medias, necesita filtro `ls` o renombrado), **🧭21 NUEVA** (LEEME mudo como cebo), **🧭22 NUEVA** (header contado como distrito en E2). Ninguna rompe el camino. La pregunta de Gwyn «¿el novato encuentra la nota SIN cartel?» se responde: **sí, incluso sin buscar** — calibrar si se quiere hallazgo escondido (filtrar dotfiles) o visible (asumir y pulir LEEME).

CICLO: verde — la zona 🔬 se ejecutó completa sobre el generator real y el viaje del novato suma el Faro cerrado (cortar + ordenar) + el Auditor con memoria de corte; el veterano ya puede leer la Lista en dos ejes y el informe lo cita; los hallazgos son pulido de hallazgo y didáctica, ninguno bloquea la run.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
