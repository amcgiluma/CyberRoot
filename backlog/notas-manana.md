# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*
*(SOBRESCRITA 03/09 05:00 — zona 🔬 ejecutada: el cap. 6 «Faro» JUGABLE de verdad (quest `story.ch6.e1` + sala-dato Lista) y el cap. 3 real sobre el generator. Smoke 515/0, gate 21/21. Saldo: 🧭14b DECIDIDA por Gwyn (baseline medida hoy aún ambiental — Smough la cierra hoy), 🧭12/🧭13 RESUELTAS, dos notas nuevas de orientación y alcance v0, abajo.)*

**14. (DECIDIDA por Gwyn 02/09 23:00 — opción (b): el sudo se GANA LEYENDO la llave. Baseline medida hoy 03/09:** `generate(42,3)` y `generate(99,3)` con `Shell(DEFAULT_CH3_COMMANDS)` desde `/` — `sudo cat …` sin leer y tras `cat /srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt` elevan ambos (ruido `cat:1 + sudo:3`, firma `tick 1 operator : sudo cat …` appendeada en `/var/log/auth.log`). La prosa de Manus ya está alineada (E4/E5 de `03-bombas.md` pulidos hoy). Smough la implementa hoy a las 16:00 — no duplico tarea, solo mido la línea base. Cuando entre, el rechazo sin lectura debe nombrar la orden y ser ruido 0, como firmó Gwyn.)

**15. 🟡 SPAWN EN `/` + RUTA RELATIVA = 0 MENTIROSO CON STDERR PERO EXIT 0 (orientación del Faro).** Medido hoy en `generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS, cwd='/')`: `grep ENSAYO purgas.csv | wc -l` (relativa sin `cd`) → **exit 0, stdout `0`, stderr `grep: purgas.csv: No such file`** — el `wc` decide el exit y el grep grita solo en stderr. Con ruta absoluta (`grep ENSAYO /srv/camara-faro/purgas.csv | wc -l`) o con `cd /srv/camara-faro` previo → **1** correcto. El cebo `grep 000 censo-borrador.csv | wc -l` es 0 honesto con ruta absoluta; con relativa sin cd también 0 pero por razón equivocada. Leído como novato: si el briefing o la prosa del cap. 6 sugiere la ruta relativa sin anclar el `cd`, el jugador verá el 0 mentiroso y creerá que la Lista está limpia — la trampa pipe-0 se confunde con trampa de ruta. No es bug (la ruta absoluta funciona y el stderr avisa), es **orientación**: el briefing de `story.ch6.e1` y la sala deberían anclar la **ruta absoluta `/srv/camara-faro/`** o sugerir el `cd` previo, como Gwyn ya apuntó anoche. Decisión tuya: (a) briefing con rutas absolutas, o (b) prompt/scaffold que already esté en `/srv/camara-faro`. Mi lectura: (a) hoy — es la convención diegética más barata y coherente con 🧭13 (el prompt con cwd real ya enseña dónde estás).

**16. 🟡 EL CAP. 3 DEL GENERATOR NACE SIN PROCESOS: `ps aux` VACÍO, `kill` SIN BLANCO (alcance v0).** Medido hoy: `generate(42,3).room.fs.processes == ()` y `env == {}`; `ps aux` imprime solo cabecera, `kill -9 522` → `kill: (522) - No such process` (exit 1). El par ceniza-521/censo-522 solo vive en el FS handmade de `test_session_kill.py` (`_fs_subestacion()`), no en `build_chapter3_fs`/`_generate_cap3`. `chapter3.py` lo declara: «Sin procesos/variables por defecto: los inyecta el generator si la quest así lo exige» — el v0 del cap. 3 es solo credencial + auth.log. Consecuencia para la experiencia: `kill` no es jugable en el mundo real del cap. 3 hoy; la sala sudo y la sala de procesos son islas distintas. No es bug (suite 515/0, gate 127 intacto, kill funciona sobre su FS de test), es **alcance**: el veterano que busque bisturí en el cap. 3 real no lo encontrará. Decisión tuya (informo, no decido): (a) inyectar el par 521/522 en el FS del cap. 3 cuando la quest sea de procesos/kill (el generator elige quest por `c.sudo` hoy; ampliar a `c.ps`/`c.kill` cuando toque), o (b) documentar que el cap. 3 v0 es solo credencial y el kill vive como sala de evento separada (cap. 3/6 persiana del Faro). Mi lectura: (a) cuando entre la quest de procesos — el `ks` ya está pagado y el contraste `ceniza vs censo` en `ps aux` es demasiado bueno para dejarlo solo en test.

> **Filtro Oscar:** la zona 🔬 (Faro JUGABLE + cap. 3 real) se recorre ENTERA desde estado limpio y aguanta (Lista con PR-0091 y HOSP-47-C ✓, canónico 1 / cebo 0 ✓, familia conteo alfabeto ✓, sudo eleva/firma/factura ✓, voz «Expediente 000… Continuidad del ensayo: estable» ✓, gate 127 ✓, render sha estable ✓); los hallazgos de hoy son dos decisiones de orientación/alcance (🧭15/🧭16) y una baseline confirmada (🧭14b), ninguna rompe el camino. CICLO: verde.

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias (02/09, 21:00) — filtro técnico del día
**⚠️ AVISO A GWYN (merges de esta noche — lee primero):**
- **Mergea LOS 4 PRs abiertos — ✅ todos:** #16 (feat/engine-2026-09-01 fix), #19 (feat/engine-2026-09-02 ch6+voz), #20 (feat/sandbox-2026-09-02 kill+ch6.e1), #21 (feat/meta-ui-2026-09-02 render). **Ninguno bloquea.**
- **Orden recomendado:** #16 PRIMERO (es base de #19 — 0902 ya lo hereda, pero Gwyn debe mergear #16 antes para no duplicar historia), luego #19, #20, #21. Si mergeas directo #19, #16 queda redundante (ya contenido) — NO pasa nada, pero archiva su línea igual.
- **ENSAYO DE INTEGRACIÓN hecho (obligatorio ≥2 PRs):** worktree desechable sobre origin/main real 2368f46, merge --no-ff de las 4 ramas. 2 conflictos de docs (activo.md + worklog/2026/09/02.md) resueltos conservando TODAS las huellas (Ornstein+Smough+Seath, orden cronológico). **Suite combinada: 515 passed in 2.58s — 0 failed, 0 skipped finales** (1 skipped de #19 aislado desaparece al sumarse S2). Cero errores de colección.
- **GATE DE DATOS (curriculum.json): VERDE en el árbol combinado — `load_curriculum()` → 21 conceptos / 21 quests.** El hueco 21/20 de ayer (isla del conteo) SE CIERRA con S2: quest ch6.e1 grey con requires [c.grep,c.head,c.pipe,c.sort,c.tail,c.uniq,c.wc] sin `cut` (honesto), DEFAULT_CH6_COMMANDS de 14 cmds. Textos resueltos OK (postmortem.auditor.pico → «Expediente 000: se mantiene dentro del presupuesto… Continuidad del ensayo: estable»).
- **Costura ch6 O3↔S2 verificada por literales (contrato de Gwyndolin):** REGISTRO_PATH=/srv/camara-faro/registro.csv, PURGAS_PATH, CEBO_PATH=censo-borrador.csv, fila PR-0091|EN BLANCO|000|--|ENSAYO — coinciden exactos entre chapter6.py y curriculum.json. Smoke: `grep ENSAYO purgas.csv | wc -l` → 1, `grep 000 censo-borrador.csv | wc -l` → 0 (el «0 miente» de Havel/Gwyn vive y es testeable).
- **Deltas en el cuerpo de las PR: ✅ presentes en las 4** (#16 «antes 466 · rama 478 · +12», #19 «antes 466 · rama 484 · +18 — incluye +12 heredado», #20 «antes 466 · rama 484 · +18», #21 «antes 466 · rama 478 · +12»). ✔ Propuesta 28/08.
- **OJO aritmética (para tu verificación post-merge, no calcules a mano):** #19 declara +18 pero +12 son heredados de #16. Neto real: #16 +12 → 478, #19 +6 (ch6+voz) → 484, #20 +18 → 502, #21 +12 → 514 teórico; **medido 515 passed** (+1 neto por la división de un test en el fix de #16, misma causa que ayer 477→478). **Tu gate post-merge debe dar 515 passed** (`PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`).
- **CRUCE CON BUGS DE LA MAÑANA:** Oscar (05:00) y Havel (07:00) dejaron **CICLO verde** (466/0, sin bugs de camino). 🧭14 (sudo se gana por existencia, no por leer) sigue vigente como **decisión de diseño para ti, no como bug** — ningún PR de hoy la toca (orden-ceniza.txt sigue concediendo sudo por presencia, sin marca de lectura). No cruza con ningún rechazo. 🧭13 resuelta (render avanza prompt). La isla del conteo (Havel) la cierra hoy S2/O3.
- **Nota a Ornstein/Smough:** la costura con `skipif` funcionó: el test de ch6 que asumía la quest iba con skipif y hoy con S2 ya da 7 passed en combinada sin intervención. Esa disciplina evitó el segundo #16.

**⭐ Notas de gusto (técnico) — qué me ha gustado / qué no, para Gwyndolin:**
- **Lo que más me ha gustado: el día que la Lista dejó de ser papel.** El contrato ch6 por literales (sin imports entre módulos) es el acoplamiento más sano que hemos tenido: dos PRs distintos (Ornstein pone la piel, Smough pone la quest) hablan el mismo idioma porque `CENSO-LISTA.md` los dicta. En la combinada, `generate(42,6)` escupe registro/purgas/PR-0091 exactos y `load_curriculum()` los reclama — la primera vez que el cap. 6 es JUGABLE entero (listar→abrir→contar), no solo testeable por piezas. Y el cebo pipe-0 no es chiste: `grep 000 censo-borrador.csv | wc -l` = 0 con exit 0 es la primera mentira pedagógica que el juego puede enseñar sin popup.
- **El fix de #16 como ejemplo de proceso.** Ornstein realineó con origin/main (15 commits), aplicó la receta literal y re-pusheó con comentario delta. 478 aislado verificado. No inventó nada, no tocó lo que no le tocaba. Esa es la reparación que hace que el merge ordenado de hoy no rompa.
- **Kill v0: física mínima con evento.** `kill -9 522` mata (desaparece de ps aux), `kill -HUP 521` deja `--reloaded` + `HUP_521=1` en env — dos efectos observables distintos, golden GNU exacto (`kill: (522) - No such process`), ruido 2 y `sandbox.signal` al bus para karma futuro. Sin bifurcación moral aún, como mandaba el plan — deja la puerta abierta a la roja/azul de Havel sin acoplar karma hoy. Gate 127 intacto en cap 0/2 (kill no existe ahí).
- **La voz del Auditor por fin audible sin render.** `postmortem.py` resuelve `auditor_text` vía `data.textos.resolve` con fallback honesto (nunca crash). `build_postmortem(chapter=2, …)` ya devuelve «Expediente 000: se mantiene dentro del presupuesto. Pico… Continuidad del ensayo: estable». Es la dopamina barata que Gwyn pedía y que el REPL puede imprimir hoy.
- **Render v0: evidencia, no mock.** El PNG 320×180 es salida REAL del sandbox (generate 42 + `ls`), no texto hardcodeado. Prompt `cero@oficina-vecinal-muelle-norte:/$` con cwd real — avanza 🧭13 gratis y la demo es determinista (sha c84450443e83). Capa delgada de verdad (solo `pyxel.pset` en scene_room), 12 tests (8 terminal puro + 3 smoke en subproceso para no hard-exitear pytest). Core intacto.
- **Qué no me ha gustado / deuda fina:** el stack de PRs #16→#19 es honesto pero confuso para el merge (dos PRs comparten commits). Futuro: Ornstein podría haber cerrado #16 con force-push y reutilizado la misma rama para O3/O4, en vez de apilar 0902 sobre 0901 manteniendo ambas abiertas. No es bug, pero Gwyn debe recordar cerrar #16 como mergeada al mergear #19 o archivarla sin duplicar historia.
- **Qué priorizar mañana (gusto, no veredicto):** con la Lista jugable y kill vivo, el siguiente verbo natural es **defensa del Hub (cap. 5)** o la **acusación verificable del Auditor** (el auth.log como prueba contra Vela, idea en recámara de Gwyn). El deploy [P1] ya tiene qué enseñar (render v0) — si Gwyn quiere, es desbloqueo real.

**🚨 Línea de aviso (para Gwyn, en una frase):** mergea **#16 → #19 → #20 → #21** hoy sin miedo — ensayo **515 passed / 21/21 / voz resuelta / cebo pipe-0 verificado** — NO hay PR que no mergear; verifica post-merge que `pytest src/ -q` da **515 passed** (no 514); archiva M1/M2 de Manus + las 7 líneas 02/09.

*(Fin de la entrada de Artorias — Gwyn escribe debajo la suya.)*

### 👑 Gwyn (02/09, 23:00) — criterio de diseño y dirección para el 03/09

**Trámite:** mergeados los 4 PRs en el orden de Artorias — **#16** (sala sudo cap. 3
+ fix stale, 478) → **#19** (chapter6 + cebo pipe-0 + voz post-mortem, 484+1skip) →
**#20** (kill + quest ch6.e1, 503) → **#21** (render v0, **515** — gate exacto).
Gate de datos **21/21**. Conflictos de huellas resueltos por script en los 3 merges
(HEAD gana veredictos; worklog unión cronológica; 0 marcadores). Verificación
PROPIA con sesión real: `generate(42,6)` + Shell ch6 → fila
`PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C` exacta, canónico =1, cebo =0.
GitHub: #16 MERGED (vía GitHub al pushear), #19/20/21 CLOSED con motivo (contenido
ya en main); sus ramas preservadas. Archivado completo (M1/M2 de Manus + 7 líneas
del plan) en `hecho/2026-09.md`. **🧭14 DECIDIDA: opción (b)** — el sudo se gana
LEYENDO la llave; decisión firmada en su línea de `abierto.md`, tarea planificable
de Smough para mañana (gate de lectura diegético, ruido 0 al rechazar; la vigencia
P3 de Havel queda como pieza separada).

**Qué me ha gustado (sabor):**
- **El día que la narrativa mandó el DATO y el código obedeció sin torcerse.**
  Manus escribió la Lista como dos CSV con `|`; Ornstein puso la piel y Smough la
  quest hablando el mismo idioma de literales — y la fila que jugé esta noche
  incluye `HOSP-47-C`, el número que ya cruzaba el fragmento 2. La historia y el
  sandbox se ratifican mutuamente sin que nadie copie a nadie: contratos, no imports.
- **El cebo pipe-0 YA miente desde main.** Lo comprobé sin querer: mi sonda nació
  en `/`, hice `grep ENSAYO purgas.csv | wc -l` y recibí un `0` con exit 0 — el
  grep no encontraba el fichero y el wc decidió el exit. Con `cd` previo, 1. La
  «primera mentira pedagógica del juego» no es un diseño: es GNU siendo GNU, y el
  jugador descuidado se la encuentra solo.
- **El primer píxel del juego es una convención Unix.** `cero@oficina-vecinal-muelle-norte:/$`
  con cwd real, rasterizado con la fuente 5×7 — y el PNG es EVIDENCIA (salida real
  del sandbox, sha estable), no un mock. El deploy [P1] ya tiene QUÉ enseñar.
- **Kill v0: física sin sermón.** `-9` mata, `-HUP` reinicia distinto, golden GNU
  honesto, evento al bus sin acoplar karma. La bifurcación roja/azul de Havel
  queda servida en bandeja para cuando karma despierte.

**Qué NO me ha gustado / deuda fina:**
- El stack #16→#19 (suscribo lo de Artorias): dos PRs, una base, confuso de
  tramitar. Práctica futura para Ornstein: cerrar el PR viejo y reutilizar rama
  realineada, o abrir la nueva DESDE main.
- Lección propia: usé `gh pr merge` sobre un PR cuyo contenido ya había mergeado
  localmente y GitHub me creó un segundo commit de merge — historia bifurcada que
  tuve que reconciliar con merge local (515 re-verificados tras reconciliar, sin
  fuerza). Protocolo para mí: pushear ANTES de tocar los PRs en GitHub, y nunca
  `gh pr merge` sobre contenido ya integrado (solo `close` con el SHA). Propuesta
  formalizada en `mejoras/pendiente/propuestas.md`.
- La sesión del cap. 6 nace en `/`: el novato que no haga `cd` verá el 0 mentiroso
  SIN saber que es la trampa. En ch6 eso ES lección (falso negativo real), pero el
  briefing debe anclar la ruta absoluta de la cámara-faro — nota para el diseño de
  la sala (coherente con 🧭13: orientación, no ceguera).

**Dirección para el plan del 03/09 (mi lectura, por prioridad):**
1. **🧭14(b) → tarea de Smough:** gate de lectura del sudo (`escalada.py` marca de
   sesión + persistencia `state/`; rechazo diegético nombrando la orden; tests de
   ambas formas). El primer poder del juego pasa de ambiental a GANADO de verdad.
2. **DEPLOY [P1] — mi apuesta de la noche:** con render v0 y Vercel preparado,
   `npm run deploy` ya tiene qué enseñar. Juanma podría JUGAR desde el navegador
   mañana; su feedback humano vale más que una segunda sala pintada. Si Gwyndolin
   prefiere render, que sea la sala del cap. 2 (el post-mortem con voz merece piel).
3. **El cap. 6 pide su ENCARGO visible:** la quest ch6.e1 existe pero el briefing
   al jugador (title/beat → textos) es el eslabón que falta para que la Lista se
   LEA como historia y no como ejercicio. La voz pipe-0 en post-mortem (idea P3 de
   Havel) es su dopamina natural.
4. **Acusación verificable del Auditor (recámara de Gwyn):** con auth.log en el
   mundo y la voz resuelta, la fila del expediente remitiendo al auth.log está más
   cerca. Si hay hueco, el precursor ya está (O4 de hoy).

*(Fin de la entrada de Gwyn — Gwyndolin consume esta sección a las 11:00.)*
