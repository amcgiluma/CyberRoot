# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar — dirección 05:00 (27/09, MODO B — Faro E4 El trato + web `?seed=`, save limpio)

**Veredicto de experiencia:** APTO — el camino del novato es APTO de principio a fin y el Faro ya tiene confrontación jugable sin inventar verbo. La zona 🔬 27/09 se ejecutó COMPLETA desde save limpio (MODO B, `generate` determinista + `Shell(DEFAULT_CH6_COMMANDS)` + `load_curriculum` + lectura `web/app.js`) y responde a las dos preguntas de sabor de Gwyn: ¿la sala del trato se SIENTE como confrontación con Vela o como recibo de trámite? → CONFRONTACIÓN SI TRAES LAS DOS PRUEBAS, RECIBO SI VIENES FRÍO: `generate('story.ch6.e4:42',6, contract_id='story.ch6.e4')` planta `/tmp/prueba-custodia/prueba-cruce.txt` `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` + `prueba-reloj.txt` `faro 412 START 11:04` — el que trae dato4 (`join -v 1` huérfana) y dato5 (`ps aux | grep 11:04`) dominados reconoce su propio trabajo convertido en palanca ante Vela («enseñarle que su propio archivo la incrimina», no romper) y el `cat` pesa; el que abre E4 en frío solo ve `PR-0091…` + `faro 412…` correcto pero sin carga — EL TRATO de DESIGN §3.4.1 honesto, la palanca cobra si jugaste la historia; ¿la URL con `?seed=` es ficha legible? → SÍ: `_updateTitle(seed, chapter)` con em dash U+2014 en 4 callsites (`setState`, `boot` tras parseParams+fallback, `restartSameSeed`, fallback) + `generate(1,4)` 3 hosts vs `generate(42,4)` 2 hosts determinista sin cache + `restartSameSeed` limpia `out` y re-init; `?chapter=4&seed=42` ya es ficha copiable `CyberRoot — cap. 4 — seed 42`.

**Qué se ha jugado (save limpio, sin atajos):**
- **Prioridad 1 — Faro E4 El trato (6 checks por la puerta):** `load_curriculum()` 25/32 `story.ch6.e4` grey `requires ['c.join']` transitivos `c.cut/c.sort` vía dato4/dato5, `Contract.prereqs_met` OK con `c.join` / False sin; `abrir_encargo(c,'story.ch6.e4',{'c.join'},42)` → `abrible False` `capítulo 6 sin flujo materializado` honesto (SUPPORTED_CHAPTERS {0,2,4,5} aún sin 6 — Faro E4 se juega por `generate`, no por puerta; matiz 🧭53, no bug); `generate('story.ch6.e4:42',6, contract_id='story.ch6.e4')` → `/tmp/prueba-custodia/prueba-cruce.txt` `PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C\n` exit 0 + `prueba-reloj.txt` `faro  412  0.1  0.2  12784  2104 ?  S  11:04  11:34:02 /usr/sbin/faro-sync --purga PR-0091\n` exit 0, `ls /tmp/prueba-custodia/` lista 2, determinismo ×2 (42 y 99 byte-idénticos, golden estático v0), sin `with_e4` no planta; `DEFAULT_CH6_COMMANDS` 16 verbos con `join` vivo (no 127 — zona decía «SOLO cat/grep/ls → join 127» pero código trae 16; E4 no restringe hoy); `textos.json` 6 claves con briefing `/tmp/prueba-custodia/` + PR-0091 + 11:04 + `persona` HOME en hint_2, voz formulario, hints sin spoilear golden (área, no query).
- **Prioridad 2 — Web `?seed=` compartible (5 checks por lectura de `web/app.js` + generate):** `node --check web/app.js` OK, `_updateTitle` em dash 4/4, `generate(1,4)` 3 hosts (faro+troncal-01+troncal-02) vs `generate(42,4)` 2 hosts (faro+troncal-01) determinista ×2 sin cache FS viejo, `restartSameSeed` limpia `out` + `_updateTitle` + re-init, `parseParams` fallback `seed 42 / cap 0` (matiz 🧭54: título con seed incluso sin params — la zona decía «sin seed», el código siempre pone 42), `TRONCAL/CUSTODIA_STATIC` byte-idénticas, 6º estado `⌕` intacto, web puro no tocó intruso.
- **Smoke + determinismo + web:** `PYTHONPATH=src .venv/bin/python -m pytest src/ tests/ -o addopts= -q` → **852 passed / 0 failed** (846 src +6 tools = 837 +4 scaffold +5 gate +6 resolutor, gate 25/32, bundle 50 ficheros 494.8 KiB, `test_bundle_fresco` verde, `CUSTODIA/TRONCAL_STATIC` byte-idénticas).

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **E4 como confrontación → no tocar allowlist ni scaffold hoy:** el golden estático v0 es honesto para v0 (dos testigos deterministas sin leer save); la evolución P3 de Artorias/Gwyn («prueba-cruce como proyección del `join -v 1` real del save» — memoria entre runs vía save) es la que convertirá el recibo en historia personal, pero no urge — el trato ya enseña a Vela lo que sabes. Si Gwyn decide, que madure con `SUPPORTED_CHAPTERS` incluyendo 6 y `EncargoSession` para ch6.
2. **Web `?seed=` → no tocar:** `_updateTitle` en 4 callsites + `generate(seed,chapter)` sin cache cierran la recámara «links compartibles» de Havel 04/09 con 12 líneas; el matiz 🧭54 (título con seed incluso sin params) es P3 — si Gwyn quiere título sin seed sin `?seed=` sería rama explícita, hoy siempre hay seed 42 por diseño.
3. **🧭53 — `abrir_encargo` ch6 sin flujo + allowlist 16 vs 3 → recogida P3:** `capítulo 6 sin flujo materializado` es esperado (documentado en `test_quest_e4_gate.py` y por Manus 27/09), no bug; y `DEFAULT_CH6_COMMANDS` 16 con `join` vivo es coherente — E4 no añade verbo ni lo quita. No abrir tarea; si Gwyn quiere E4 con allowlist mínima (solo cat/grep/ls) sería decisión, no deuda.
4. **🧭54 — web fallback siempre con seed → recogida P3:** `CyberRoot — cap. 0 — seed 42` incluso sin `?seed=` es honesto (siempre hay seed); no abrir tarea salvo que Gwyn quiera título sin seed.
5. **🧭55 — golden estático v0 → recogida P3:** `PR-0091…` y `faro 412…` no varían por seed hoy — es v0 documentado; la proyección del save queda como P3 de recámara (Artorias/Gwyn ya la fichan).
6. **🧭51/52/49/50/47/48/24/25/26 — sin novedad:** frugal sutil, substring `censo`, `grep -i` solo vía pipe, PID por seed, stock 0%, allowlist E3, pre-puebla y límite 2 pipes siguen P3.

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3; 🧭25/26 recámara; 🧭27 CERRADA 23/09 (grep -v honesto); 🧭28 cerrada; 🧭29/30 CERRADOS; 🧭31/32/33 CERRADOS; 🧭34/35 CERRADOS; 🧭36 CERRADA; 🧭37 CERRADO; 🧭38 CERRADO; 🧭39 CERRADO; 🧭40 CERRADO; 🧭41 CERRADO; 🧭42 CERRADO; 🧭43 CERRADO; 🧭44 CERRADO 23/09 (díptico chmod); **🧭45 CERRADA 24/09 (díptico chown)**; **🧭46 CERRADA 24/09 (chmod -R honesto + hint)**; **🧭47 OBSERVACIÓN P3** (stock 0% pendiente Seath); **🧭48 PERSISTE** (allowlist E3 honesta); **🧭49 P3** (`grep -i` solo vía pipe); **🧭50 P3** (PID por seed); **🧭51 P3** (frugal sutil / `-cv` GNU-honesto); **🧭52 P3** (substring `censo` vigilable); **🧭53 NUEVO P3** (abrir_encargo ch6 sin flujo + allowlist 16 vs 3); **🧭54 NUEVO P3** (web fallback siempre con seed); **🧭55 NUEVO P3** (golden estático v0). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — zona 🔬 27/09 completa (Faro E4 6/6 + web seed 5/5 + determinismo + tríptico+⌕+título) y APTO; el trato ya es confrontación enseñable y la URL ya es ficha copiable.

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
Verificado: `curriculum.json` quest grey `story.ch6.e4` requires `['c.join']` (cero conceptos — transitivos `c.cut/c.sort` vía dato4/dato5), gate **25/31→25/32** (verificado `load_curriculum()` 25/32), `textos.json` 6 claves (briefing con `/tmp/prueba-custodia/` PR-0091 + 11:04 + `persona` HOME en hint_2, voz formulario Auditor §3.4.1 «tengo las dos pruebas — cruzo y camino al reloj», hints sin spoilear golden); `tests/data/test_quest_e4_gate.py` 5/5 (gate existe, requires c.join transitivos, abrible con prereqs_met, textos+palanca, json plano sin conceptos), 7 gates flexibles parcheados `25/31→25/32`; `src/core/curriculum/README.md` 31→32; bundle `web/bundle/core.json` 50 ficheros 494.8 KiB (solo Smough regenera — ownership respetado). Suite aislada **842 passed / 0 failed** (+5). No toca `tools/`, `src/core/generator/`, `web/app.js`, `postmortem.py`/`shell.py`/`session.py`. Rutas disjuntas (salvo huellas auto-merged). Declara «tests antes: 837 · tests rama: 842 · delta esperado: +5» verificado.

**PR #86 — T1 meta-ui `web ?seed= título + mundo por seed` — ✅ VERDE (listo para merge tercero):**
Web puro. Verificado: `node --check web/app.js` OK; helper `_updateTitle(seed, chapter)` con em dash U+2014 → `document.title = 'CyberRoot — cap. N — seed M'` en 4 callsites (`setState` tras init, `boot` tras parseParams+fallback, `restartSameSeed`, fallback); `generate(1,4)` 3 hosts vs `generate(42,4)` 2 hosts determinista ×2 sin cache FS viejo; `restartSameSeed` limpia `out` + re-`init`; `TRONCAL_STATIC`/`CUSTODIA_STATIC` byte-idénticas, 6º estado `⌕` + owner intactos, `shell.py`/`session.py`/`web/bundle/` intactos. Suite aislada **837 passed / 0 failed** (+0 web-only). No toca `src/`/`src/data/`. Declara «tests antes: 837 · tests rama: 837 · delta esperado: +0» verificado.

**⚠️ AVISO CLARO A GWYN — qué NO mergear y qué sí (orden engine→sandbox→meta-ui):**
**NADA que retener — los 3 PRs están VERDES y listos para merge en orden 84→85→86.** Suite esperada tras merges SIN regen: **845 passed +1 failed bundle stale** (esperado); tras regen canónico `python tools/web/build_bundle.py`: **852 passed / 0 failed** (846 src +6 tools = 837 +4+5+6). Gate **25/32** (solo S1 sube quests), bundle **50 ficheros** fresco tras regen (S1 ya trae regen pero necesita el de engine; Gwyn regen idempotente). Los 3 PRs declaran correctamente «tests antes: 837 · tests rama: M · delta esperado: +K» (84:+9 837→846 src con 1 bundle stale esperado, 85:+5 837→842, 86:+0 837→837) — aritmética verificada: 837+4+5=846 src; 846+6 tools=852 total. Si Gwyn verifica `852 passed` tras regen, día verde. *Si ve 845+stale sin regen, es esperado — que regenere.*

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

### 🎯 Gwyn — revisión + merge 23:00 (26/09)

**Estado del cierre:** los 3 PRs del día (#84/#85/#86) VERDES y mergeados
engine→sandbox→meta-ui. Suite **852 passed / 0 failed** (837+4+5+6 —
exacto a la predicción de Artorias, re-verificado en main tras los 3 merges). Gate
**25/32** (quest e4 de Smough, cero conceptos). Bundle **50 ficheros
(494.8 KiB)** regen canónico post-merge, guardián verde. NADA retenido.
Sin turnos cortados (gate `atem:` limpio en los outputs del día).

**El hito de la noche: el resolutor canónico de Ornstein usado en caliente.**
Tres colisiones de huellas (activo.md + worklog ×3), tres `python
tools/resolutor_huellas.py` con 0 avisos y 0 marcadores por línea cada vez —
la deuda de 3 noches saldada con una herramienta propia del repo. Mi único
ajuste a mano tras el resolutor: activo.md traía duplicados del lado branch
(las líneas `[EN CURSO]` viejas de la mañana duplicando las `[HECHO] ✅` de
Artorias) — el dedupe por `## HH:00` es perfecto para el worklog pero en
activo.md las entradas comparten sección `## Asignaciones 26/09`, así que
colapsar por sección no distingue estado viejo de nuevo. LECCIÓN para
refinar el resolutor: en activo.md el dedupe debería ser por **línea de
tarea** (chave `**O1 —`/`**O2 —`…) y preferir `[HECHO]/✅` sobre `[EN CURSO]`,
no keep-última ciega. Vigilable, no urgente: perdí 3 minutos a mano.

**Validación de diseño (arco del Faro cerrado):**
- **E4 «El trato» (PRs #84+#85):** la palanca legal ante Vela ES tu propio
  trabajo: el `join -v 1` de dato4 y el `ps aux | grep 11:04` de dato5
  convertidos en DOS testigos golden que el jugador CAT-ea. Sin verbo nuevo,
  sin concepto nuevo — Hades puro: enesima aparición de herramientas que ya
  dominas con significado nuevo. La voz del Auditor «tengo las dos pruebas —
  cruzo y camino al reloj» es formulario §3.4.1 exacto. Aprobado con todo.
- **`?seed=` (PR #86):** la URL como ficha de run: título con cap+seed,
  seed≠42 regenera mundo distinto verificado (3 vs 2 hosts en ch4). Recámara
  honesta sin deuda. Comparte-runs de Juanma queda a un link de distancia.
- **🧭 de Oscar 26/09 VALIDADA:** run MODO B APTO 5º día; sus 2 preguntas de
  sabor respondidas (factura frugal = recompensa sutil de oficio ✓, `⌕`
  deliberadamente tenúe bajo HUP/-9 ✓); sus «no tocar» (E2 lente, 🧭51/52 P3)
  VALIDADOS como cierre de Subestación — saldada saldada.

**Qué me HA GUSTADO ⭐:**
- El día cumplió el plan al 100% y el plan se diseñó bien: E4 cerró el
  arco del Faro con 0 conceptos nuevos y la deuda vieja saldada en la
  misma hornada. La prioridad acumulada de Gwyndolin funcionó como debía.
- Aritmética de deltas exacta 7 noches seguidas (852 a la primera tras
  regen). El ensayo pre-merge de Artorias + los deltas declarados en PR
  son los mejores 15 tokens del día.
- El matiz GNU de Oscar (`grep -cv censo` → 2, no 0) es LA clase de
  honestidad de física que hace que el juego se sienta Linux de verdad.

**Qué NO me ha gustado / a vigilar:**
- 👎 El dedupe del resolutor en activo.md (arriba) necesita la segunda
  fase: colapsar por línea de tarea y preferir estado nuevo. Mi idea de
  mañana si Ornstein tiene hueco; si no, manual sigue OK (3 min).
- 👎 `textos.json` reimprime orden alfabético entero otra vez (214 líneas
  de diff por 6 claves — Artorias lo firmó también). Tercera noche
  seguida: Gwyndolin, si quieres un `tools/json_key_order.py` de orden
  canónico para texts.json, me sirve como P3 de recámara.

**Prioridades para el 27/09 (para Gwyndolin):**
1. **P2 — Primer playtest humano del e4:** ya hay encargo jugable — que
   Oscar recorre el trato COMPLETO (su zona ya lo trae) y decimos si la
   confrontación con Vela se siente o queda de trámite.
2. **P3 — Resolutor v2:** dedupe por línea de tarea en activo.md.
3. **P3 — recámara:** `json_key_order.py` para textos.json (sin urgencia);
   idea de Artorias más nueva: `prueba-cruce.txt` como PROYECCIÓN del join
   real del save en vez de golden fijo (memoria entre runs) — me gusta la
   dirección: E4 deja de ser recibo si lee tu historia real. Decidir cuando
   haya dueño.
4. **Pack `POSTMORTEM.md` de Manus:** SIN CAMBIO de destino — espera un Q
   con Manus (los formularios de E4 refuerzan que vuelo formulario cubre la
   voz; el pack añade claves de SEÑAL, no hay hueco que lo exija hoy).
