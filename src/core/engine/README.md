# engine/ — El motor roguelite

> **Qué hace:** dirige el ciclo completo de una incursión y su vuelta al Hub:
> mapa de nodos → salas → extracción/detección → liquidación → post-mortem.
> Orquesta `sandbox/` (ejecuta comandos) y `generator/` (crea la incursión);
> aplica las reglas de números del diseño.
>
> Normativa: `docs/DESIGN.md` §4.1 (loop), §7 (dopamina/números), §4.7 (Hub) ·
> arquitectura: `../ARCHITECTURE.md` §2.5.

## Responsabilidades
- **Run**: estado de la incursión, sala actual, rutas, entradas/salidas de
  sala; modos mapa↔terminal como ESTADOS del core (el render solo los pinta).
- **Vigilancia/detección**: % sube por ruido de acciones (regla de luz §6.0.2:
  más luz = más vigilancia base por anillo). NUNCA sube por reloj artificial
  (§7.9). Al llegar al umbral → expulsión.
- **Economía DATOS×COMBO** (§7.1): base por tipo de dato; combo por escalones
  (+0,1 por cadena limpia, baja UN escalón por fallo, DOS por tramo de
  detección); liquidación total al extraer, parcial (50 % ⚠️ v1 de lo ya
  extraído, sin combo) al ser expulsado + bonus de profundidad (§7.7).
- **Apuestas de run** (§7.3): deep scan, ruta ruidosa, «una sala más».
- **Sinergias** (§5.2, catálogo v1 en §7.8): detección de disparadores
  pipeline/recon→ejecución/estado persistente/etc., leyendo el historial de
  comandos de la run. Los efectos son numéricos/eventos — el juice lo añade el
  render con los mismos eventos.
- **Cierre de run**: informe post-mortem (siempre, §4.7) + cola de eventos
  hacia el Hub (historia avance SIEMPRE — el contenido vive en `data/story/`).
- Números calibrables: constantes documentadas en un solo sitio para que el
  harness las ajuste sin reescribir lógica.

## Entradas / salidas
- ENTRADA: comandos de jugador (`exec`, `ui.*`) + `IncursionInstance` del
  generador + perfil del jugador (boons, karma).
- SALIDA: mutaciones de estado de run + `Event`s (combo, alerta, hallazgo,
  expulsión, liquidación…).

## Cómo se testea
- Run completa headless: resolver una incursión sembrada ejecutando su
  secuencia canónica → éxito esperado, métricas exactas.
- Expulsión forzada (ruido máximo) → parcial cobrado correcto, lección en cola,
  avance narrativo presente.
- Combo: cadenas limpias/fallidas/tramos de alerta → escalones exactos.
- Determinismo: misma seed + mismos comandos → misma partida entera.

## Dueño
Ornstein (`feat/engine`). También construye `tools/harness/` sobre esta API.

---

## v0 (O2, 30/08) — post-mortem del Auditor leyendo el historial real

Primer fichero del módulo: `postmortem.py` (la pieza que el Hub muestra
SIEMPRE primero, §4.7). `build_postmortem(shell_dict, state)` es una función
PURA, testeable headless (sin I/O, sin RNG, sin estado global).

- **EN**: `Shell.to_dict()` (historial de la sesión real) + `state` con
  `noise_budget` (la MISMA unidad que `total_noise`, 🧭10; default 12 ⚠️ v1).
- **SALIDA**: dict plano con `factura` (cuentas por comando + `errores`),
  `total_noise` vs `noise_budget`, `dentro_presupuesto`, y una línea del
  Auditor (`line_key` + `args`) que cita el comando CONCRETO que disparó la
  detección — el que hace CRUZAR el presupuesto acumulado si lo hay, o el
  pico (más ruido individual) si no. Voz: formulario seco (PERSONAJES.md).
  El texto va como CLAVE + args; el render resuelve la prosa contra `data/`
  (convención §3: core no hardcodea textos).
- **Tests**: `src/tests/core/engine/test_postmortem.py` (8 tests) — factura
  de la sesión canónica (ls 2 · cat 1 · cp 1 · cd 1 · errores 0), total 6/12,
  pico sin cruce, cruce con presupuesto 5, errores contados, default de
  presupuesto, helpers deterministas, informe JSON-plano.

```bash
./.venv/bin/python -m pytest src/tests/core/engine -o addopts= -q
```

---

## v0.2 (O1+O2, 31/08) — flujo de ENCARGO del cap. 2 + post-mortem conectado

Segundo fichero del módulo: `session.py` — el flujo completo de un encargo del
currículo REAL: **listar → abrir (validando prereqs) → generar la sala del
contrato → jugar → cerrar.** Un `postmortem.py` lo consume al CERRAR (O2).

- `listar_encargos(curriculum, chapter, knowledge=None)` → vitrina de la mesa
  del Hub: los encargos del capítulo ordenados por id, con `abrible`/`falta`
  si se pasa `knowledge`. NO genera nada (🧭8=(b)).
- `rechazo_accionable(...)` → qué conceptos faltan (el «no puedes» es un dato,
  no una negativa).
- `abrir_encargo(curriculum, quest_id, knowledge, run_seed=0)` → valida
  `Contract.prereqs_met` al ABRIR (nunca en `generate()`); si procede, genera
  la sala (seed determinista `quest_id:run_seed`) y devuelve un
  `EncargoSession` (Incursion + Shell viva). `session.ejecutar(line)` juega.
- `cerrar_encargo(session, modo="completado"|"expulsión")` → adjunta
  `build_postmortem(shell_dict, state)` como dato estructurado del cierre.

Para que la golden del cap. 2 (`grep 11:04 centralita/turnos/turno.log |
wc -l` → `2`) fuera JUGABLE dentro del flujo, el generador ganó soporte del
cap. 2: `generate(seed, chapter=2, contract_id="story.ch2.e1")` construye la
sala de la centralita (nueva hoja `src/core/generator/chapter2.py`, canon con
la golden) y `generate(seed,0)` queda byte-a-byte idéntico (regresión).

El módulo consume `build_postmortem` como función PURA e intacta: el post-
mortem del cap. 2 factura la línea del pipe (grep/wc) bajo su comando primario
y `total_noise` con el ruido real (grep 2 + wc 1 + cd 0).

---

## v0.3 (O4, 02/09) — el post-mortem entrega la VOZ resuelta

`build_postmortem` construye la línea del Auditor como `line_key` + `args`
(convención §3: core no hardcodea prosa) y desde esta entrega RESUELVE la
prosa contra `data/textos` antes de devolverla, sin romper la API pura. El
dict de cierre gana dos campos legibles sin render:

- `auditor_text`: la cadena final (`resolve(line_key, args)`), p. ej.
  `Expediente 000 …` para la factura del cap. 2 (`grep 11:04 …`).
- `lines_resolved`: lista con las líneas de auditoría formatadas.

El import `core/data/textos → resolve/load_textos` está permitido por
ADR-0001 (`data` no trae deps de core). `_resolve_auditor_text` es honesto:
si `data.textos` falla o devuelve vacío, devuelve la CLAVE cruda en lugar de
crash o de un hueco `{...}` — nunca rompe el cierre de la run. El REPL puede
imprimir la voz del Auditor HOY, sin esperar al render.

---

## v0.4 (O1, 04/09) — el Auditor cita lo que LEÍSTE (`read_marks`)

Idea P2 de Havel + dirección #3 de Gwyn: el post-mortem consume `read_marks`
(ya en `Shell.to_dict()` desde S1, 03/09) como segunda fuente de verdad tras
el historial. Regla v0 sin imports de sandbox:

- `history` contiene `sudo` y `read_marks` no vacío → segunda línea
  `postmortem.auditor.lectura` con `args {path}` citando la ruta leída
  (forma formulario §2.4 — dato, nunca moralina).
- `history` contiene `sudo` y `read_marks` vacío → variante
  `postmortem.auditor.ciega` («elevó sin leer ninguna orden»).
- Sin `sudo` → sin segunda línea, informe byte-idéntico (cap. 0/2 intactos).

`build_postmortem` añade `auditor_lectura` + `auditor_lectura_text` y
extiende `lines_resolved` a 2 entradas cuando toca. Determinista por
codepoint y roundtrip intacto. Tests en `test_postmortem_lectura.py` (7).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine -o addopts= -q
```
---

## v0.5 (O1+O3, 05/09) — el Auditor cita TU columna + cebo del 0 por ruta

**O1 — `postmortem.auditor.corte` (Ornstein, idea P3 Havel 05/09):** el informe añade tercera fuente de verdad si el `history` contiene `cut` con flags (`-d`/`-f`). Helpers `_extract_cut_args` + `_find_cut` escanean el historial (solo shlex sobre la línea, sin imports sandbox): extraen `column`/`pattern` y resuelven `postmortem.auditor.corte` → `auditor_corte` + `auditor_corte_text` y tercera entrada en `lines_resolved` (segunda si no hubo `sudo`). Sin `cut` con flags → informe byte-idéntico (no rompe tríada lector ni caps 0/2/3). Determinista por orden de history. Texto en `data/textos.json`: `Expediente 000: corte registrado — columna {column} ({pattern}). Continuidad del ensayo: estable.` Tests en `test_postmortem_corte.py` (4).

**O3 — Cebo del Faro: el 0 que miente por ruta (generator/chapter6.py):** añade fichero `LEEME.txt` en `/srv/camara-faro/` que invita a usar ruta relativa (`purgas.csv` sin `cd`). Piel pura: `grep ENSAYO purgas.csv | wc -l` desde `/` → `stdout 0` + `stderr grep: purgas.csv: No such file…` + `exit 0` del `wc` (pipe honesto GNU); con absoluta o tras `cd /srv/camara-faro` → `1` (canónico E1 intacto). Tests en `test_chapter6_cebo.py` (2).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q  # 573 passed
python tools/web/build_bundle.py  # regenera core.json (44 ficheros)
```

---

## v0.6 (O1, 12/09) — el Auditor cita TU cruce de tablas (join -v)

**O1 — `postmortem.auditor.join` (Ornstein, reposición 12/09):** cuarta huella hermana de corte/orden — si el history contiene `join` con `-v` (anti-join), añade 1 línea formulario. Helpers `_extract_join_args` + `_find_join` (solo shlex sobre la línea, sin imports sandbox): detectan `-v`/`-v1`/`-v 1` en cualquier posición (tras pipe también), retornan {} (texto estático, nunca datos de fila). `build_postmortem` añade `auditor_join` + `auditor_join_text` y extiende `lines_resolved` (antes de sudo, orden corte→orden→join→lectura). Sin `join` con `-v` → informe byte-idéntico (no rompe tríada lector ni caps 0/2/6). Texto en `data/textos.json`: `Expediente 000: cruce registrado — join anti-join (-v): huérfanas de la primera tabla. Continuidad del ensayo: estable.` Tests en `test_auditor_join.py` (3: con -v dispara / sin -v no dispara documentado / sin join byte-idéntico, determinismo).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_auditor_join.py -o addopts= -q  # 3 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 694 passed
python tools/web/build_bundle.py  # regenera core.json (47 ficheros)
```

---

## v0.7 (O1, 13/09) — Eco del espejo v0: el Auditor nombra tu repertorio

**O1 — `postmortem.espejo.repertorio` (Ornstein, P1 13/09):** quinta huella, eco diegético que nombra el repertorio ya dominado sin enseñar comando nuevo. Si el history contiene alguna de las 3 firmas (① `scp` a `/tmp/volcado.csv` seguido de `cut|grep` — ch4.e2; ② `join` con `-v` — dato4; ③ `ps aux|grep` con hora — dato5), añade **1 sola línea** `postmortem.espejo.repertorio` con `args {huellas}` enumerándolas en orden ①→②→③ ("copiaste el volcado", "cruzaste dos testigos", "leíste el reloj" → "A, B y C"). Helpers `_has_espejo_volcado`/`_has_espejo_reloj` (solo substring+regex, sin sandbox) y reutiliza `_find_join` para ②. Sin firma → byte-idéntico (no key, no línea). Texto en `data/textos.json`: `Expediente 000: repertorio — {huellas}. Continuidad del ensayo: estable.` — sin datos de fila, sin popup, formulario. `test_auditor_join.py` actualizado para coexistencia (join dispara `auditor_join`+`auditor_espejo`, len 2→in 2,3). Tests en `test_postmortem_espejo.py` (5: ①/②/③ cada uno dispara + byte-idéntico sin firma + ①+②+③ en una línea orden determinista).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_postmortem_espejo.py -o addopts= -q  # 5 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 703 passed
python tools/web/build_bundle.py  # regenera core.json (47 ficheros, 400.2 KiB)
```
---

## v0.9 (S1, 15/09) — bifurcación TR-003: volcado rescate vs caducado (Smough)

**S1 — `postmortem.volcado.*` (Smough, ADR TR-003, P1 15/09):** sexta huella, bifurcación del volcado EN_COLA. Si el history contiene `scp ... volcado-rescate.csv` con exit 0 → `postmortem.volcado.rescate` (voz: «volcado EN_COLA entregado al Faro»); si contiene `rm /tmp/volcado.csv` exit 0 o tick>=30 sin rescate → `postmortem.volcado.caducado` («volcado EN_COLA sin entrega — caducado»). Rescate tiene prioridad. Helpers `_has_volcado_rescate`/`_has_volcado_rm` (solo shlex/substring, sin sandbox), `volcado` campo resume estado. Textos en `data/textos.json`, `story.ch4.e3.*` desde prosa de Manus (04-troncales.md). Tests en `test_volcado_rescate.py` (3: rescate/caducado por rm y tick/byte-idéntico). Suite 714→723 (+9, +6 rm y 3 volcado), bundle 418.2 KiB.

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_volcado_rescate.py -o addopts= -q  # 3 passed
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/sandbox/test_rm.py -o addopts= -q  # 6 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 723 passed
python tools/web/build_bundle.py  # regenera core.json (47 ficheros, 418.2 KiB)
```

---

## v0.8 (O1, 15/09) — session.py ch4 jugable como encargo

**O1 — `session.py` cap. 4 (Ornstein, 15/09, ADR TR-003):** el flujo de encargo materializa el capítulo 4 «Troncales» — `SUPPORTED_CHAPTERS` {0,2}→{0,2,4}, `_commands_for(4)` devuelve `DEFAULT_CH4_COMMANDS` base (13, sin `rm` — el `rm` de e3 lo aporta Smough con `DEFAULT_CH4E3_COMMANDS` (14) en su allowlist e3). `abrir_encargo` genera sala ch4 con `contract_id` determinista `quest:seed` (cap. !=0 → con contrato; 0 sin), compatible con e1/e2 actuales y con e3 cuando Smough la suba al `curriculum.json` (el engine lee del curriculum, no hardcodea e3). `listar_encargos(4)` ordena por id, `abrir` rechaza accionable con `falta` honesto si faltan prereqs, `cerrar_encargo` adjunta `postmortem` intacto (firma no cambia). Tests flexibles en `test_session_ch4.py` (4: SUPPORTED+commands + listar honesto e1+e2⊆ids e3 opcional + abrir e2 con cut+scp y shell activa + cerrar e2→postmortem completado/expulsión).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_session_ch4.py -o addopts= -q  # 4 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 718 passed (717 +1 bundle stale → 718 tras regen Gwyn)
python tools/web/build_bundle.py  # regen canónico al cierre de Gwyn (regla 12/09)
```

---

## v0.9 (O1, 16/09) — session.py e3 cablea `rm` (simetría scp/rm, 🧭36)

**O1 — `session.py` e3 (Ornstein, 16/09, 🧭36):** `_commands_for(4, quest_id)` devuelve `DEFAULT_CH4E3_COMMANDS` (14, con `rm`) SOLO cuando `quest_id == 'story.ch4.e3'`; base 13 INTACTA en e1/e2 (llamada legacy sin quest_id → base). `abrir_encargo` crea el `Shell` con la allowlist correcta y pre-puebla `hosts` remotos (como `generator.new_session`) para que `scp`/`rm` funcionen sin `cat` previo. `rm /tmp/volcado.csv` exit 0 → `build_postmortem` marca `volcado: caducado` (detector ya existente de S1 15/09); e1/e2 `rm→127` frontera intacta. Tests en `test_session_ch4_e3.py` (4: base vs e3 / e3 scp+rm→caducado / e1/e2 rm 127 / determinismo+listar). Suite 727→731 (+4, bundle stale honesto pendiente regen canónico Gwyn).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_session_ch4_e3.py -o addopts= -q  # 4 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 731 (730 +1 bundle stale → 731 tras regen Gwyn)
```


---

## v0.10 (O1, 18/09) — session.py ch5: la puerta normal del Asalto — PR #64

**O1 — `session.py` cap. 5 (Ornstein, 18/09, 🧭37/38):** `SUPPORTED_CHAPTERS` {0,2,4}→{0,2,4,5}, `_commands_for(5)` → `("cat","scp")` con fallback local idéntico (costura O↔S: Ornstein consume con try/except, Smough crea `DEFAULT_CH5_COMMANDS` nova en `shell.py` a las 16:00 — unión por terminal si choca). Mensaje de `listar_encargos` actualizado a "0, 2, 4 y 5". Solo `story.ch5.e2` abre hoy (e1/e3/e4 → `{"abrible": False, "missing": ["encargo sin flujo materializado en cap. 5 (hoy solo e2)"]}` sin generar sala). Kwarg `volcado_rescatado: bool=False` en `abrir_encargo` propagado a `generate(seed,5, volcado_rescatado)` — geografía condicional: rescatado → `/tmp/volcado-custodia.csv` exit 0 `TR-003|faro|troncal-01|512|EN_COLA`; caducado → exit 1 `No such file`. Helper `volcado_del_save(pm)->bool` lee `pm.get("volcado")=="rescatado"` del post-mortem del Hub. Shell montada con snapshot FS del asalto y allowlist ch5. Generador `chapter 5` wired (allow 5 + dispatch `_generate_cap5` + `_session_commands` cat/ps/scp para validación canónica intruso 03:14). Tests `test_session_ch5.py` 7 tests + flexibilización de asserts ch4/errores para superset 5.

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_session_ch5.py -o addopts= -q  # 7 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 755 passed +1 bundle stale → 756 tras regen Gwyn
```

---

## v0.11 (O1, 20/09) — session.py ch5: puerta COMPLETA — PR #68

**O1 — `session.py` cap. 5 puerta completa (Ornstein, 20/09, reposición 19/09):** borrado guard `chapter==5 and quest_id!="story.ch5.e2"` — los 4 encargos e1/e2/e3/e4 abren por la MISMA puerta (prereqs → `abrible False missing [...]` / OK → `EncargoSession` seed `quest:run_seed`). `volcado_rescatado` propaga a los 4 (True → `/tmp/volcado-custodia.csv` exit 0 `TR-003|EN_COLA` 66 bytes; False → `No such file` exit 1 — misma semántica e2). `SUPPORTED_CHAPTERS` {0,2,4,5} y `_commands_for(5)` intactos (\"cat\",\"scp\"); `shell.py`/`web/`/`src/data/` intocados. Tests `test_session_ch5.py` reescrito (12 tests: requires correctos e1[c.ls-la,cat,chmod]/e3[ps,env]/e4[chmod,chown,cat,grep], volcado condicional e1/e3/e4, determinismo ×2 seeds `generate(42,5)/(99,5)` byte-idéntico, `volcado_del_save` helper). Suite 769→773 passed (+4 net, +5 tests — bundle stale honesto pendiente regen canónico Gwyn).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_session_ch5.py -o addopts= -q  # 12 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 773 passed +1 bundle stale → 774 tras regen Gwyn
```

---

## v0.12 (O1, 21/09) — session.py ch5 per-encargo + postmortem HUP/KILL — PR #69

**T1 (P2, 🧭44) — `_commands_for(5, quest_id)` per-encargo (Ornstein, patrón CH4E3 14/09):** `_commands_for(5)` base `(cat,scp)` intacta (legacy sin quest_id → base); `quest_id=='story.ch5.e1'` → `DEFAULT_CH5E1_COMMANDS` (cat,chmod,kill,ls,ps,scp), `e3` → `DEFAULT_CH5E3_COMMANDS` (cat,env,kill,ps,scp), `e4` → `DEFAULT_CH5E4_COMMANDS` (cat,chmod,chown,ls,scp,tail). `abrir_encargo` monta `Shell` con la allowlist correcta; `ps aux` vía puerta → 0 con `censo <pid> intruso --vigilar-censo START 03:14` (seed 42→424, 99→421, forma `<=` en tests, `03:14` invariante; `kill -HUP`/`-9` jugable por la puerta, `ls`/`chmod` e1 y `chmod/chown/tail` e4 → 0, e2 127 honesto). `session.py` importa las 3 allowlists novas con try/except fallback idéntico (costura O↔S). Tests `test_ch5_per_encargo.py` (5: commands_for ramifica / e3 ps jugable / e1 ls/chmod / e4 tail / e2 intacta). Suite 774→784 (+10 con T2).

**T2 (P1, karma del volcado) — `postmortem.py` huella kármica vigilante (Ornstein, propuesta Havel 20/09):** detector `_detect_vigilante` lee `fs.environment[HUP_*]` + ausencia `--vigilar-censo` en `fs.processes` + `history` con `kill` (solo shlex/substring, sin sandbox). `kill -HUP <pid>` sobre intruso → `postmortem.auditor.hup` («señal de reconfiguración registrada…») + `karma_delta 1` azul (`karma_tint blue`, `karma {delta:1,tint:blue}`, `micro_karma {blue:1}`); `kill -9` (o TERM/-KILL/-15) → `postmortem.auditor.kill` («proceso de vigilancia eliminado…») +1 rojo. Sin kill → informe byte-idéntico (no key, no karma, no línea); e1/e4 sin falsa detección (misma FS, sin HUP). Textos nuevos `postmortem.auditor.hup/kill` en `data/textos.json` (prefijo disjunto, sin tocar `postmortem.auditor.corte/orden/join` etc.). Tests `test_postmortem_hup_kill.py` (5: HUP azul / KILL rojo / sin kill byte-idéntico / e1/e4 sin falsa / prefijo disjunto). Bundle 49 (459.2 KiB) regen en rama (toca `textos.json`).

```bash
PYTHONPATH=src .venv/bin/python -m pytest src/tests/core/engine/test_ch5_per_encargo.py src/tests/core/engine/test_postmortem_hup_kill.py -o addopts= -q  # 10 passed
PYTHONPATH=src .venv/bin/python -m pytest -o addopts= -q  # 784 passed
python tools/web/build_bundle.py  # 49 ficheros → 459.2 KiB
```
