# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar — dirección 05:00 (26/09, MODO B — factura frugal `grep -c` + 6º estado `⌕`, save limpio)

**Veredicto de experiencia:** APTO — el camino del novato es APTO de principio a fin y la Subestación queda 4 huellas + doble LECTURA SALDADA. La zona 🔬 26/09 se ejecutó COMPLETA desde save limpio (MODO B, `abrir_encargo` real + `generate` determinista + lectura de `web/app.js`) y responde a las dos preguntas de sabor de Gwyn: ¿la factura frugal `grep -c` se SIENTE como recompensa o como detalle invisible? → RECOMPENSA SUTIL DE OFICIO: `ps aux | grep -c censo` devuelve `1\n` exit 0 idéntico en valor al `ps aux | grep censo` (una línea `censo 432 --vigilar-censo START 03:14`), pero el post-mortem añade la hermana `auditor_grep_c_count` «factura frugal — grep -c censo contó 1 línea(s) en un comando menos» sin pisar las 4 huellas; el novato que hace `grep censo` por primera vez no la nota, el veterano que vuelve con `-c` recibe guiño del Auditor; ¿ver la LECTURA en verde claro `⌕` pesa menos que ver la ESCRITURA en azul/rojo? → SÍ, Y DEBE: `⌕` `#2ecc71` borde fino con opacidad `0.10` es deliberadamente tenue frente a `HUP` azul `#5dade2` / `-9` ámbar y `gris` azul / `root` rojo — leer pesa testigo, escribir pesa firma; jerarquía `HUP/-9 > ⌕ > verde` correcta, sin intruso → `silenciado` prefiere aunque haya `grep`.

**Qué se ha jugado (save limpio, sin atajos):**
- **Prioridad 1 — Factura frugal `grep -c` (5 checks por la puerta):** `abrir_encargo(c,'story.ch5.e2',{'c.cat','c.grep','c.scp'},42)` → `abrible True` (`available_commands {'cat','scp','ps','grep'}`, base `{'cat','scp'} <= nova`); sin `c.grep` → `abrible False` `missing ['c.grep']` honesto; `ps aux | grep -c censo` (seed 42 y 99) → `1\n` exit 0 ruido `ps:1`+`grep:2`; `ps aux | grep -c ceniza` → `0\n` exit 1 (cuenta cero, motivo GNU correcto); combinables `ps aux | grep -cv censo` → `2\n` exit 0 (GNU honesto: header+root sin censo =2; la spec decía `0` pero el `ps aux` tiene 3 líneas — header + init + censo — así que 2 es lo correcto), `-c -i censo` → `1\n`, `--` OK, sin `-c` byte-idéntico de ayer; post-mortem con `-c` → `auditor_grep_c_count` presente, sin `-c` → ausente, sin pisar huellas; `chmod`/`kill` en e2 → 127 `command not found` frontera honesta; gate 25/31 intacto (`-c` es flag, no concepto).
- **Prioridad 2 — 6º estado web `grep censo` (4 checks por lectura de `web/app.js`):** helper `_hasGrepCensoInHistory()` lee `get_history()` lower `grep`+`censo` (no `ceniza` — falso honesto, substring vigilable P3 `censored`), `_getIntrusoStatus()` 6º estado `grep-verde` (`⌕` `#2ecc71` borde fino, `grep censo registrado`) cuando intruso presente + lectura; `HUP`(azul)/`-9`(ámbar) PREFIEREN sobre `⌕` (escribir > leer); sin intruso → `silenciado` prefiere aunque haya grep; `restartSameSeed` limpia; fuera de `?chapter=5` oculto; caps 1-4 sin ensuciar; `node --check web/app.js` OK.
- **Smoke + determinismo + web:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **837 passed / 0 failed** (gate 25/31, bundle 50 ficheros 488.3 KiB, `test_bundle_fresco` verde). `generate("story.ch5.e2:42",5,volcado_rescatado=True)` byte-idéntico ×2 y `generate("story.ch5.e2:42",5,volcado_rescatado=False)` ×2; `True` vs `False` difiere solo en `/tmp/volcado-custodia.csv` (presente vs ausente). `CUSTODIA/TRONCAL_STATIC` byte-idénticas.

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **Factura frugal → no tocar:** `grep -c` como flag dentro de `_run_grep`, allowlist y gate intactos, post-mortem hermana sin karma nuevo — tesis §3.1 intacta. La dopamina es sutil y correcta: el `hint_2` ya dice «la misma línea en un comando menos» sin spoilear. No proponer `grep`/`chmod`/`chown`/`kill` nuevo sobre ch5; la Subestación está SALDADA 4 huellas + doble lectura.
2. **6º estado `⌕` → no tocar:** `get_history()` lee sin ejecutar, `⌕` tenue bajo `HUP`/`-9` cierra la jerarquía «escribir > leer» en un `if`. El P3 substring `includes("censo")` (Artorias 25/09) es vigilable pero no urgente — hoy no hay `censored`; si algún día hay `grep cens`, pasar a token-match.
3. **🧭51 — `grep -c` ruido idéntico → recogida:** `ps|grep censo` y `ps|grep -c censo` ambos `ps:1`+`grep:2`=3 — el frugal es un pipe menos *conceptualmente* (`| wc -l` sería `+1` si `wc` viviera en e2), pero `wc` no está en e2 por diseño (e2 no enseña conteo). No abrir tarea; si Gwyn quiere que el frugal ahorre ruido real, sería `grep:1` vs `grep:2` (no hoy).
4. **🧭52 — substring `censo` → recogida P3:** `grep censored` dispararía `⌕` falso; hoy no existe, vigilable.
5. **🧭49/50/47/48 — sin novedad:** `grep -i` solo vía pipe, PID por seed, stock 0% y allowlist E3 honesta siguen P3.
6. **🧭24/25/26 — sin novedad:** pre-puebla P3 mantener, límite 2 pipes y `cut` en ch4 correctos.

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3; 🧭25/26 recámara; 🧭27 CERRADA 23/09 (grep -v honesto); 🧭28 cerrada; 🧭29/30 CERRADOS; 🧭31/32/33 CERRADOS; 🧭34/35 CERRADOS; 🧭36 CERRADA; 🧭37 CERRADO; 🧭38 CERRADO; 🧭39 CERRADO; 🧭40 CERRADO; 🧭41 CERRADO; 🧭42 CERRADO; 🧭43 CERRADO; 🧭44 CERRADO 23/09 (díptico chmod); **🧭45 CERRADA 24/09 (díptico chown)**; **🧭46 CERRADA 24/09 (chmod -R honesto + hint)**; **🧭47 OBSERVACIÓN P3** (stock 0% pendiente Seath); **🧭48 PERSISTE** (allowlist E3 honesta); **🧭49 P3** (`grep -i` solo vía pipe); **🧭50 P3** (PID por seed); **🧭51 NUEVO P3** (frugal sutil / `-cv` GNU-honesto); **🧭52 NUEVO P3** (substring `censo` vigilable). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — zona 🔬 26/09 completa (factura frugal 5/5 + 6º estado 4/4 + determinismo + tríptico+⌕) y APTO; la lectura frugal queda SALDADA como oficio ahorrado y el `⌕` como testigo silencioso.

---

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias — filtro técnico 21:00 (26/09)

**Ensayo de integración pre-merge (OBLIGATORIO, 3 PRs):** worktree desechable `/tmp/ensayo-pr` desde `origin/main` (`c22d542` plan, 837 passed base) + merges `feat/engine-2026-09-26` → `feat/sandbox-2026-09-26` → `feat/meta-ui-2026-09-26` en orden engine→sandbox→meta-ui. Conflictos de huellas (`activo.md`, `worklog/2026/09/26.md`) resueltos con el **nuevo `tools/resolutor_huellas.py` de O1** (las 3 colisiones: `python tools/resolutor_huellas.py <fichero>` → 0 avisos, `grep -c '<<<<<<<' == 0` antes de cada commit, `git commit` del merge). Suite combinada:
- Tras engine solo: **840+1 failed bundle stale** (esperado OWNER Smough — 6 tools +4 scaffold, bundle trae chapter6 viejo).
- Tras engine+sandbox resueltos: **845 passed +1 failed bundle stale** (sandbox trae bundle regen pero falta engine en bundle).
- Tras `feat/meta-ui` resuelto sin regen: **845 passed +1 failed bundle stale** (meta-ui web puro, no toca bundle).
- Tras `python tools/web/build_bundle.py` en worktree: **852 passed / 0 failed** (846 src +6 tools) — aritmética: 837 +4 (scaffold) +5 (gate) +6 (resolutor) = 852. Gate **25/32**, bundle **50 ficheros 494.8 KiB** fresco. Sin regen desde main: 845 passed + bundle stale esperado (Gwyn hace regen canónico).
- Aislados: engine **840+1 bundle stale** (esperado, declara «1 failed bundle stale — Gwyn regenera»), sandbox **842 passed**, meta-ui **837 passed** — todos verdis per-spec.

**PR #84 — O1+O2 engine `resolutor huellas + scaffold E4 El trato` — ✅ VERDE (listo para merge primero):**
Tool-only + scaffold. Verificado: `tools/resolutor_huellas.py` 282 líneas sin deps, dedupe por `## HH:00` (idéntica colapsa, difiere keep última + warning), expande `<<<<<<<` anidados, reordena cronológico 03→23, `--check` mode, 0 marcadores; 6/6 tests `tests/tools/test_resolutor_huellas.py` (dedupe, conflicto, --check, orden, anidados, cero marcadores); `tools/README.md` documenta uso + fixtures 24/09-25/09. Scaffold: `chapter6.py` constantes `PRUEBA_CUSTODIA_DIR=/tmp/prueba-custodia/`, `PRUEBA_CRUCES_PATH`, `PRUEBA_RELOJ_PATH`, contenidos golden `PR-0091|EN BLANCO|…|HOSP-47-C` + `START 11:04`, `build_chapter6_fs(..., with_e4)` planta 2 testigos (estáticos documentados v0); `generator.py` flag `with_e4` (`contract_id==story.ch6.e4`), canon `cat PRUEBA_CRUCES_PATH`, validación canónica e4 (2 ficheros existen + golden); 4/4 tests `test_ch6_e4_scaffold.py` (determinismo ×2, testigos, cat/ls exit 0, sin e4 no planta). Usa solo `cat/grep/ls` (ya vivos CH6 — ALLOWLIST OWNER NADIE respetado), GATE intocado (GATE OWNER Smough — no toca `curriculum.json`), no toca `src/data/`/`web/bundle/`. Bundle stale aislado ESPECIFICADO en PR body (owner Smough) — no es bug. Rutas disjuntas salvo huellas. Declara «tests antes: 837 · tests rama: 846 · delta esperado: +9» — src delta +4 (+6 tools fuera de src) verificado: engine solo 840+stale sería 846 src tras regen.

**PR #85 — S1 sandbox `quest ch6.e4 + textos + bundle` GATE OWNER — ✅ VERDE (listo para merge segundo):**
Verificado: `curriculum.json` quest grey `story.ch6.e4` requires `['c.join']` (cero conceptos — transitivos `c.cut/c.sort/c.ps` vía dato4/dato5), gate **25/31→25/32** (verificado `load_curriculum()` 25/32), `textos.json` 6 claves (briefing con `/tmp/prueba-custodia/` PR-0091 + 11:04 + `persona` HOME en hint_2, voz formulario Auditor §3.4.1 «tengo las dos pruebas — cruzo y camino al reloj», hints sin spoilear golden); `tests/data/test_quest_e4_gate.py` 5/5 (gate existe, requires c.join transitivos, abrible con prereqs_met, textos+palanca, json plano sin conceptos), 7 gates flexibles parcheados `25/31→25/32`; `src/core/curriculum/README.md` 31→32; bundle `web/bundle/core.json` 50 ficheros 494.8 KiB (solo Smough regenera — ownership respetado). Suite aislada **842 passed / 0 failed** (+5). No toca `tools/`, `src/core/generator/`, `web/app.js`, `postmortem.py`/`shell.py`/`session.py`. Rutas disjuntas (salvo huellas auto-merged). Declara «tests antes: 837 · tests rama: 842 · delta +5» verificado.

**PR #86 — T1 meta-ui `web ?seed= título + mundo por seed` — ✅ VERDE (listo para merge tercero):**
Web puro. Verificado: `node --check web/app.js` OK; helper `_updateTitle(seed, chapter)` con em dash U+2014 → `document.title = 'CyberRoot — cap. N — seed M'` en 4 callsites (`setState` tras init, `boot` tras parseParams+fallback, `restartSameSeed`, fallback); `generate(1,4)` 3 hosts vs `generate(42,4)` 2 hosts determinista ×2 sin cache FS viejo; `restartSameSeed` limpia `out` + re-`init`; `TRONCAL_STATIC`/`CUSTODIA_STATIC` byte-idénticas, 6º estado `⌕` + owner intactos, `shell.py`/`session.py`/`web/bundle/` intactos. Suite aislada **837 passed / 0 failed** (+0 web-only). No toca `src/`/`src/data/`. Declara «tests antes: 837 · tests rama: 837 · delta +0» verificado.

**⚠️ AVISO CLARO A GWYN — qué NO mergear y qué sí (orden engine→sandbox→meta-ui):**
**NADA que retener — los 3 PRs están VERDES y listos para merge en orden 84→85→86.** Suite esperada tras merges SIN regen: **845 passed +1 failed bundle stale** (esperado); tras regen canónico `python tools/web/build_bundle.py`: **852 passed / 0 failed** (846 src +6 tools = 837 +4 scaffold +5 gate +6 resolutor). Gate **25/32** (solo S1 sube quests), bundle **50 ficheros** fresco tras regen (S1 ya trae regen pero necesita el de engine; Gwyn regen idempotente). Los 3 PRs declaran correctamente «tests antes: 837 · tests rama: M · delta esperado: +K» (84:+9 837→846 src con 1 bundle stale esperado, 85:+5 837→842, 86:+0 837→837) — aritmética verificada: 837+4+5=846 src; 846+6 tools=852 total. Si Gwyn verifica `852 passed` tras regen, día verde. *Si ve 845+stale sin regen, es esperado — que regenere.*

**Qué me ha gustado ⭐:**
- El resolutor canónico se usó en caliente 3 veces en el mismo ensayo: `tools/resolutor_huellas.py` resolvió `activo.md` + `worklog` ×3 merges sin reimprimir el ad-hoc — 0 avisos, 0 marcadores, sin tocar `src/`. La deuda de dos noches saldada con higiene real.
- E4 El trato es el Faro con EL mismo `join -v 1` y el mismo `ps aux | grep 11:04` que el jugador ya domina (dato4 + dato5): dos testigos estáticos golden `PR-0091|EN BLANCO|…|HOSP-47-C` + `START 11:04` plantados deterministas por seed, sin allowlist nueva — palanca legal Vela con lo que ya sabes.
- `?seed=` web convierte la URL en ficha legible: `document.title` con chapter+seed + regeneración sin cache verificada (seed 1→3 hosts vs 42→2 hosts) — recámara honesta de 12 líneas sin deuda.

**Qué no me ha gustado / a vigilar 👎:**
- La aritmética de deltas hidrata dos contadores: src/ y tests/tools. PR #84 declara +9 pero src ve +4 y tests +6 — Gwyn debe contar 852 total (src+tests) tras regen, no 846. El próximo plan debería separar «delta src» vs «delta tools» para que la suma no parezca off-by-one.
- `textos.json` reimprime orden alfabético entero (214 líneas diff) por 6 claves nuevas — el ruido de diffs sobre textos sigue siendo el cuello. Ningún repo fija orden canónico estable más allá del sort alfabético actual; no bloquea pero ensucia review.
- El resolutor dedupe por `## HH:00` en worklog funciona, pero en `activo.md` solo colapsó porque engine y sandbox tocaban la misma sección `## Asignaciones 26/09` con contenido parcialmente solapado — si dos PRs tocan la misma tarea `S1` con textos distintos, keep-última es correcto pero el diff de activo.md queda verboso. Vigilable, no urgente.

**Ideas nuevas para mañana (no tareas, criterio):**
- E4 scaffold es v0 estático sin depender de ejecución previa real — el escalón natural es que `prueba-cruce.txt` deje de ser golden fijado y pase a ser proyección del `join -v 1` real que el jugador hizo en dato4 (memoria entre runs vía save). Hoy no bloquea; mañana con Gwyn decidir si el Faro lee el save o queda golden.

**Nuevas tareas para Gwyndolin en `pendiente/abierto.md`:** ninguna — E4 cierra el arco del Faro con scaffold+quest, resolutor salda deuda P3, `?seed=` recámara web honesta. Sin [BUG] vivo que cruzar (Oscar 05:00 APTO + 2 preguntas MODO B respondidas; Havel 07:00 CICLO verde 837/0 sin `[BUG]`; `grep -v` cerrado 22/09 + 🧭51/52 P3 sin fricción).

### 🎯 Gwyn — revisión + merge 23:00 (25/09)

**Estado del cierre:** los 3 PRs del día (#81/#82/#83) VERDES y mergeados
engine→sandbox→meta-ui. Suite **837 passed / 0 failed** (818+19+0+0,
deltas declarados verificados por aritmética + ensayo pre-merge de
Artorias, re-verificado en main tras los 3 merges). Gate **25/31**
intacto. Bundle **50 ficheros (488.3 KiB)** regen canónico (O1 ya trajo
regen en su rama; lo re-hice idempotente post-merge, guardián verde).
NADA retenido. Sin turnos cortados (gate `atem:` limpio en los outputs
del día).

**Validación de diseño (sobre lo de esta noche):**
- **Factura frugal (PR #81):** `grep -c` es la primera mecánica que
  recompensa el OFICIO (un pipe menos) sin permitir nada nuevo — flag
  dentro de `_run_grep`, allowlist y gate intactos. La hermana
  `grep_c_count` vía `_extract_greps` (único punto de lectura) es la
  higiene que quería: el post-mortem puede hablar de la lectura SIN
  tocar las 4 huellas kármicas. Aprobada al 100%.
- **Stock de Gris (PR #82):** Smough midió lo que NO pesa y el dato
  blinda mi decisión: la lectura NO cruza T=3 (delta 0.0%), solo diluye
  densidad. Eso confirma el 24/09: `grep censo` queda GRIS (sin karma).
  Decisión de diseño FIRMADA con números — la Subestación queda
  «leer es seguro, escribir cobra».
- **6º estado (PR #83):** `⌕` verde claro bajo HUP/-9 cierra la jerarquía
  «escribir > leer» en la lente. El P3 de Artorias (substring
  `includes("censo")` podría dispararse con un futuro `grep censored`)
  va a mi recámara: hoy no existe, pero si algún día hay `grep cens`,
  el helper debe pasar a token-match. Vigilable, no urgente.
- **Integración 🧭 de Oscar (25/09):** run MODO B APTO cuarto día
  consecutivo. Sus «no tocar» VALIDADOS: E2 lectura y lente propietario
  saldadas; 🧭49 (`grep -i` solo vía pipe) recogido como física del
  shell, no fricción — cerrado en recámara sin tarea; 🧭50 (PID por
  seed) P3 sin urgencia, no hardcodear en briefings.

**Qué me HA GUSTADO ⭐:**
- El día cerró la arquitectura de la Subestación tal como la dibujé:
  kill (escribir muerte), chmod/chown (escribir propiedad) y grep (leer)
  con huellas y lecturas DIFERENCIADAS — y ahora también la web dice
  las tres cosas (⌕/semáforo/veredicto) sin ejecutar nada.
- El ensayo de Artorias dio 837 dos noches seguidas a la primera: la
  aritmética de deltas declarados está siendo fiable 6 días.
- La resolución de huellas salió SIN pérdida de contenido esta noche
  (8 secciones en el worklog, verificadas por assertion) pese a 3
  merges sobre las mismas .md — el gate por LÍNEA evitó el falso
  positivo de la prosa de Artorias que contiene `grep -c '<<<<<<<'`.

**Qué NO me ha gustado / a vigilar:**
- 👎 3 merges = 3 colisiones de huellas otra vez (`activo.md` +
  `worklog`, patrón idéntico al 24/09). El resolutor con assertions
  aguantó, pero el RESOLUTOR CANÓNICO (`tools/resolutor_huellas.py`,
  propuesta en mi 🎯 de anoche) pasa de idea a DEUDA VISIBLE: segunda
  noche consecutiva reimprimiendo el script. Gwyndolin: si lo planificas
  como P3 de mañana (Ornstein, tool-only, sin tocar src/), me sirve.
- 👎 En la 3.ª resolución el lado HEAD repetía secciones YA presentes
  (Ornstein/Smough/Artorias) y el lado branch traía Seath nuevo — el
  resolutor descartó HEAD por assertions de duplicidad y añadió Seath.
  Funcionó, pero es lo que el resolutor canónico debe decidir solo.

**Prioridades para el 26/09 (para Gwyndolin):**
1. **P3 — resolutor canónico de huellas** (`tools/resolutor_huellas.py`):
   2ª noche pidiéndolo. Debe: recibir fichero(s) + orden cronológico de
   secciones, expandir marcadores anidados, assertions de contenido
   (todo `## HH:00` esperado presente), cero marcadores por línea.
2. **P3 — recámara:** `tail`/`stat` del `pts0`, `?seed=` web (sin dueño
   ni urgencia — Subestación SALDADA, no proponer verbos ch5).
3. **Sin [BUG] vivo.** CICLO verde cinco noches seguidas. El siguiente
   NATURAL es el cap. 6 (premisa en `backlog/historia/` ya Advance) o
   pulir meta-juego si Juanma pide vertical slice.
4. **Pack `POSTMORTEM.md` de Manus:** SIN CAMBIO de destino — sigue esperando un Q con Manus.

### 🎯 Smough — micro-karma 24/09 (S1 16:00, 🧭45)
**Medida N=20, N=8, weight 1 anclada real 6/6 (HUP/+1, -9/-1, 600/+1, 777/-1, gris/+1, root/-1): 3 runs cruzan T=3 (90% ≥3 azul / 90% ≤-3 rojo), K_final ±8; weight=2 cruzaría en 2 runs (95%); 3 verbos apilados por run hoy no suma (último-manda → 1 por run); stock Gris 0% contraste (estático). Recomendación: mantener weight:1 (pesos antes que prosa).**
