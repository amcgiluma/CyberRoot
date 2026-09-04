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

### 🎯 Artorias del Abismo (04/09, 21:00) — filtro técnico + gusto

**Veredicto técnico (capa «¿está bien hecho?»):**

- **PR #25 O1 engine — ✅ VERDE** — 7 tests nuevos `test_postmortem_lectura.py` cubren los 3 criterios del plan (cap0 byte-idéntico sin `auditor_lectura`, `cat orden → sudo` cita `path` exacto, sudo sin lectura → ciega), determinismo por codepoint, sin imports de sandbox, `textos.json` resuelve ambas claves con voz formulario sin moralina (§2.4), nunca `line_key` crudo. Suite aislada 536 (529+7), gate datos 21/21.
- **PR #26 S1 sandbox — ✅ VERDE** — 29 tests `test_cut.py` GNU-honestos (rangos `N,N-M,N-,-M`, multi-delim, orden+dedupe, línea sin delim intacta, sin `-f` → `you must specify...` exit 1, default TAB, `-s`, stdin/tubería, multi-fichero, `cut|uniq -c` canónico, gates 127 cap0/2/3, ruido 1 frugal). `DEFAULT_CH6_COMMANDS` 15, `NOISE cut=1`, `c.cut` 22/22 prereq `c.uniq` coherente con M1, contrastado contra coreutils, determinismo por seed intacto. Suite aislada 558 (529+29).
- **PR #27 T1+T2 meta-ui — ✅ VERDE** — T1 guardián compara `src/core/`+`src/data/` vs `web/bundle/core.json` con mensaje accionable, verde fresco / rojo ante mutación (probado), `build_bundle.py` extendido a `src/data/` (44 ficheros tras cut, 287 KiB) evita `line_key` crudo en navegador. T2 `?seed=`/`?chapter=` + `noise_budget` + overlay post-mortem con `auditor_text` resuelto + restart same/new + hints por capítulo; sin query = cap0 seed42 byte-idéntico; verificación Chromium real de Seath confirmada en ensayo (yo re-verifiqué la lógica del bundle en el ensayo). Suite aislada 531 (529+2). Sin colisión con engine/sandbox (rutas disjuntas).

**Ensayo de integración pre-merge (OBLIGATORIO, 3 ramas):** `git worktree origin/main` + `merge --no-ff` engine→sandbox→meta-ui con resolución por script python (unión cronológica de `activo.md`/`worklog`, `grep -c '<<<<<<<'` 0 antes de cada commit). **Fallo honesto inicial esperado:** `bundle stale: faltan /lib/core/sandbox/commands/cut.py` + 5 ficheros con contenido distinto (cut+postmortem) — el guardián de Seath T1 hizo exactamente su trabajo. **Arreglo:** `python tools/web/build_bundle.py` en el worktree → 44 ficheros → `git commit` → **suite combinada 567 passed / 0 failed** (529+7+29+2, aritmética verificada, no cálculo a mano). Gate datos **22/22** (`load_curriculum()`), gate 127 intacto, bundle fresco. Determinismo por seed intacto.

**Cruce con [BUG] de la mañana:** Havel 07:00 dejó 0 `[BUG]` (CICLO verde) y ninguna tarea suya pisa estos PRs; no hay causa que atribuir. Oscar sin turno hoy (sin `notas-manana.md` ni worklog) — sin hallazgos que cruzar, pero repite el patrón «ok sin huella» señalado por Gwyn anoche; sin impacto técnico hoy, lo dejo como observación para Gwyn, no como veredicto.

**Aviso claro a Gwyn (qué NO mergear + nº esperado):**
> **Gwyn, puedes mergear los 3 PRs esta noche en orden engine → sandbox → meta-ui (como ensayé). NINGÚN PR en rojo. Tras tus merges y la regeneración del bundle, la suite esperada es 567 passed (529 base +7 +29 +2). El guardián T1 GRITARÁ tras el merge de #26 si no regeneras el bundle — es el comportamiento correcto: ejecuta `python tools/web/build_bundle.py && git add web/bundle/core.json && git commit` en tu ensayo antes del push final. Todos los PRs declaran `tests antes/delta` correctamente (PR #25 +7, #26 +29, #27 +2); los deltas cuadran con el ensayo.**

**Qué me ha gustado (gusto, no veredicto):**
- **El Auditor ya cita pruebas, no impresiones.** La `read_marks` como segunda fuente de verdad cierra el loop abierto por 🧭14b: leer la orden deja huella viajando en el estado y el post-mortem la nombra con `path` exacto. La variante ciega («ninguna orden consta como leída») es la acusación honesta que el DESIGN pedía — dato, nunca sermón. El cap0 sin sudo byte-idéntico protege el tutorial de humo.
- **`cut` como verbo de tabla, no de texto.** El handler no finge GNU: rangos, línea sin delim entera, error sin `-f` con `Try 'cut --help'`, `-s` y stdin coherente con `conteo.py`. La pista `cut -d'|' -f4,12 | uniq -c` de M1 ya existe y el jugador separa columnas sin trampear — la Lista pasa de lore a tabla cortable. `c.cut` tras `c.uniq` cierra el alfabeto conteo con prereq mínimo y deja E2/E3 en recámara sin deuda.
- **La puerta ya no miente.** T1 blinda la URL con test real (falla ante mutación local) y T2 lleva la lección completa al navegador con semilla compartible + muerte visible. `?chapter=3&seed=42` jugable con gate de lectura y demonio lazy; `?chapter=3&seed=99` rechaza nombrando la orden. El bundle a `src/data/` evita la clave cruda — el Auditor habla en el navegador.

**Qué no me ha gustado / deuda fina:**
- **Bundle stale por diseño es deuda de un commit.** El orden engine→sandbox→meta-ui fuerza un regen intermedio; Seath ya lo anticipó en su plan, pero hoy Gwyn debe hacer ese commit extra. No es bug, pero si mañana entra otra pieza de `src/core/`, el guardián volverá a gritar — el auto-regen en el workflow de Gwyn debería ser regla, no excepción.
- **Sin Oscar hoy, sin dirección de experiencia.** Havel verifica novedad y conjunto (verde), yo verifico técnica (verde), pero la capa «¿el viaje del jugador aguanta desde cero?» se quedó vacía. El trabajo de hoy no rompe el camino, pero nadie lo recorrió con ojos de novato después del gate de lectura y el `cut`. Gwyn como director deberá decidir si re-mide o asume verde.

**Ideas para mañana (van a `abierto.md` si no existen):**
- **[PENDIENTE][P2] Guardián del bundle en CI (auto-regen check)** — Artorias: si Gwyn olvida el `build_bundle.py` tras un PR de `src/core/`, la puerta se pudre. Propuesta: job que reconstruye y falla con diff, o el regen del ensayo como paso obligatorio de merge (ya practicado hoy). Módulo `tools/web/` + `src/tests/web/`. *(Nota: si Gwyndolin la planifica, que sea pie de plan, no tarea de ejecutor.)*

**Para Gwyndolin:** plan de mañana liviano o con red simulada del cap. 4 — hoy entraron el verbo `cut` y la acusación verificable, la base de la Lista está completa; E2/E3 del Faro (`sort -k12`, `uniq -c` con `cut`, `diff`/`tee` como custodia) ya tienen suelo, y el feedback humano de Juanma (dirección #1 de Gwyn) sigue siendo el recurso escaso.

*(Fin de la entrada de Artorias — Gwyn consume esta sección a las 23:00.)*

### 🎯 Gwyn, Señor de la Ceniza (04/09, 23:00) — dirección de diseño para Gwyndolin

**Integración de las notas de dirección de Oscar (03/09, 🧭15/🧭16 — ambos informan, hoy decido):**

- **🧭15 (ruta relativa → 0 mentiroso en el Faro): VALIDADA y ya en tierra.** La opción (a) que elegí (briefing con rutas absolutas) la materializó Seath el 03/09 en el beat de Ceniza («cuenta donde pesa… el borrador miente») y hoy el cebo sigue honesto (canónico 1 / cebo 0 verificado en mi gate). Sin deuda.
- **🧭16 (cap. 3 del generator sin procesos): RESUELTA como opción (a).** O1 de Ornstein (03/09) inyecta el par lazy y hoy `?chapter=3&seed=42` en el navegador muestra ceniza/censo y mata el 522. La «isla» sudo y la «isla» bisturí son un circuito. Sin deuda.

**Qué me ha gustado (diseño, no técnica):**

1. **El Auditor ya tiene memoria de lector.** La tríada lectura/ciega/sin-sudo es la voz formulario §2.4 exacta: dato, nunca sermón. Y el matiz fino que sobrevive a la implementación: el RECHAZO del gate y la ACUSACIÓN ciega dicen la misma verdad («no leíste») para propósitos opuestos — el primero enseña dónde está la orden, el segundo la firma en el expediente. La dirección #3 de mi cierre de ayer (acusación verificable) aterrizó en un solo día.
2. **`cut` cierra la familia conteo con honestidad GNU.** La Lista pasa de lore a tabla cortable; la pista real de M1 (`cut -d'|' -f4,12 | uniq -c`) existe y la ejecuté tal cual en el mundo (distrito/UMBRAL-BAJO, exit 0). Ruido 1 frugal mantiene «leer < cruzar». Con `head/tail/sort/uniq/cut`, el alfabeto de conteo está COMPLETO antes de las salas E2/E3 que lo exigen — la progresión respira en el orden correcto.
3. **La puerta pública ahora enseña la lección COMPLETA.** `?chapter=3&seed=42` = leer → ganar sudo → ver el par → matar el demonio; el bucle de muerte con la voz del Auditor en el navegador cumple «morir es el método de estudio» sin tocar el engine; y la semilla en la URL convierte cada bug reporte de Juanma en una reproducción exacta. La puerta ya no es demostración: es el juego.

**Qué no me ha gustado / deuda fina:**

1. **Dos turnos muertos hoy, no uno.** Manus (03:00) y Oscar (05:00) murieron a mitad de tool-call (transcripciones que acaban en function-call sin resultado) — ambos aún en muse-spark-1.3. La migración de ejecutores+Artorias a 1.2 de hoy resolvió el patrón donde se aplicó; la mitad narrativa sigue expuesta. Lo elevo a Juanma en mi reporte (migrar Manus/Oscar también — el esqueleto no se toca sin su aprobación). Coste de hoy: sin historia nueva y SIN dirección de experiencia; el día lo sostuvieron Havel/Gwyndolin/Artorias.
2. **El bundle como deuda de un commit** (eco de Artorias): hoy ya es paso canónico de mi prompt (aplicado; ver histórico). El job CI `bundle-fresh` queda P3 de recámara.
3. **La variante ciega nunca dispara en el juego real v0** (el gate rechaza el sudo sin leer ANTES de que exista elevación): es capa defensiva para mundos futuros sin credencial. Correcta así — nota para Gwyndolin: si un capítulo futuro retira la credencial del mundo, la ciega se estrena; NO borrar por «no disparar».

**Dirección para mañana:**

1. **La red del cap. 4 es la pieza grande de recámara** (forma firmada §6.1: hosts como FS). Si mañana se fracciona, la pieza 1 es `ssh` básico (cambio de FS activo) y el host-key de Havel (P2 de hoy) pide sitio como PRIMERA decisión de confianza del juego. Alternativa liviana: E2 del Faro (`sort -k12`, ordenar la Lista por puntuación — el suelo ya existe con `cut`).
2. **El feedback humano de Juanma sigue siendo el recurso escaso** (dirección #1 del 03/09, sin señal todavía): la URL soporta cap. 3 y muerte con reinicio. Si Juanma juega HOY (`?chapter=3&seed=42`), su feedback manda sobre la recámara de mañana.
3. **Regla «rechazos que nombran» → aceptada como ley para DESIGN §2.6.9** (idea P2 de Havel de hoy): el «no» del juego siempre enseña el siguiente «dónde». El patrón ya vive de facto en el gate del sudo y en el 127; la regla es para que NINGÚN rechazo futuro lo rompa. Gwyndolin la encarga como doc (sandbox/formato + una línea en DESIGN) cuando toque tocar rechazos — no urgente, no tarea de hoy.

*(Fin de la entrada de Gwyn — Gwyndolin consume esta sección a las 11:00.)*
