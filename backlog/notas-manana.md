# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*
*(SOBRESCRITA 02/09 05:00 — zona 🔬 ejecutada: el `sudo` GANADO del cap. 3 +
la primera VOZ del Auditor, ambos desde estado limpio. Smoke 466/0. Saldo:
🧭12 RESUELTA esta noche (T1 puso las claves en `data/` con resolvedor,
verificada resolviendo); 🧭13 RESUELTA (decisión de Gwyn anoche); 🧭9 con tubo e
idempotente. La nota nueva de hoy es una decisión de gate del primer «poder»
real del juego, abajo.)*

**14. 🟡 EL SUDO SE GANA POR EXISTENCIA DE LA LLAVE, NO POR «LEERLA»: decisión de
gate del primer poder del juego.** Medido hoy ejecutando (sala sudo del cap. 3,
FS de `_fs_sala_sudo()`): con la credencial presente en el mundo (`/srv/…/orden-ceniza.txt`),
ejecutar `sudo cat …` **sin haberla leído antes** eleva, factura premium y firma
en auth.log igualmente (exit 0, ruido 4). El gate del sandbox es
`check_credential(fs, cwd)` (`shell.py` L216): comprueba que el FICHERO existe y
contiene el marcador `AUTORIZACION: CENIZA`, pero **no rastrea que el jugador lo
haya leído** (`cat` no marca la credencial como obtenida en la sesión). Así, el
beat que §6.1 describe —«se GANA: la credencial robada u objeto de estado… se
lee con cat»— no está ENFORZADO: la premisa de la zona «sudo SIN leer la
credencial → rechazo» solo se reproduce en un FS SIN credencial (el
`test_sin_leer_llave`), no en la sala con la llave presente. Leído como novato:
si el generator coloca la credencial en el mundo y expone `sudo` en el cap. 3,
el momento de GANARSE la llave (leer la orden, aprender su alcance) se vuelve
cosmético. **Problema de fidelidad pedagógica, no de robustez** (la suite está
en 466/0 y el circuito verificado funciona; el rechazo-nombra-qué-falta sigue
vivo para el caso «no hay llave»). DECISIÓN TUYA (informo, no decido): **(a)
aceptar v0** — «la llave vive en el mundo; leerla es sabor diegético, la
autorización ES la presencia del fichero»—, o **(b) exigir el GANAR** —marcar en
la sesión que la credencial fue leída antes de permitir `sudo` (el `cat` de la
orden como requisito implícito)—. Mi lectura como guardián de la experiencia: el
punto (b) protege mejor el beat de «aprender por necesidad» del cap. 3 (el
primer contacto real del novato con el poder: primero entiendes QUÉ autorizas,
luego lo usas), y el coste es pequeño (una marca de sesión + el `cat` pasa a ser
el gesto que desbloquea). Pero el (a) es legítimo y barato si prefieres que
sudo sea una llave ambiental. Dato + tienes todo el circuito verificado.

**13. (RESUELTA anoche — Gwyn la validó con decisión al mergear: cwd del scaffold
de e1 dentro de la oficina + prompt con ruta al meter render/tutorial; `pwd` no
se regala. Entra con render. Registrada en `abierto.md`.)**

**12. (RESUELTA esta noche — T1: claves `postmortem.auditor.cruce|pico` en
`data/` con resolvedor `textos.py`; VERIFICADA HOY resolviendo con los args
reales del post-mortem: la forma sale «Expediente 000: … Continuidad del ensayo:
estable». El eco 🧭9 ahora SE OYE.)**

> **Filtro Oscar:** la zona 🔬 (sudo GANADO + primera VOZ) se recorre ENTERA desde
> estado limpio y aguanta (rechazo → leer llave → sudo eleva/firma/factura → voz
> formulario ✓ → gate 127 ✓ → post-mortem a texto ✓); el hallazgo de hoy es una
> decisión de gate (#14) y seguimiento de packaging/entrypoint, ninguno rompe el
> camino. CICLO: verde.

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
