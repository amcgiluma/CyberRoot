# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*
*(SOBRESCRITA 29/08 05:00 — zona 🔬 ejecutada: el CÓDIGO como sistema. Run de
referencia completa sobre sala REAL generada + save. Saldo de ayer: 🧭2
SALDADA — opción B verificada jugando, el dossier se sigue al pie de la letra
sin un tropiezo; el rechazo didáctico `&&`/`;` (🧭3) SALDADO — los 3 repros
exactos responden honestos hoy. Las notas 1–5 viven como tareas archivadas o
fileadas en `abierto.md`.)*

**6. 🟠 CALIBRAR EL PRESUPUESTO DE RUIDO DEL CAP. 0 (12) — medido como
jugador, no como testeador.**
La factura real del viaje HONESTO de hoy (comando a comando, evidencia en el
worklog): sesión del dossier 6 (ls 1 + cat 1 + cp 3 + cat de verificación 1 +
cd 0) + curiosidad lectora 5 (`ls` suelto, `ls -l` fallido, `ls /usb`, `cat`
del README y del log de la oficina; `help`/`pwd` son 127 y no cobran) =
**11 de 12**. Un solo error clase `cp` (+3 — y el `[BUG][P3]` de Havel
`cp dir → /usb/` cobra 3 por diagnosticar mal) dispara a 15. Y la variante
`practice` AÑADE decoys que invitan a `cat`ear más: la sala invita a la
curiosidad y apenas la cabe. No propongo número (eso es del harness, §8.6);
propongo que la calibración del budget entre en el plan cuando Ornstein monte
el runner de seeds, y que se decida la POLÍTICA: hoy el fallo léxico (127,
flags) es gratis y el fallo de riesgo (cp dir) cobra — ¿es esa la curva que
quieres cuando la expulsión sea real? Mi lectura: el cap. 0 debería perdonar
el primer error grande; el cap. 3, no.

**7. 🟡 QUE EL GENERADOR CONSUMA la opción B: hoy es dict, no comportamiento.**
Refrendo tu propia nota de anoche con dato de jugador: monté la sala como la
montará el engine (`Shell(room.fs)`) y el `cwd=/` sale del DEFAULT de la Shell,
NO del scaffold. La decisión 🧭2 vive hoy en un `options` decorativo + un
default ajeno: si alguien toca ese default, la decisión se desactiva sin que
nadie la borre. Cuando Ornstein pase generator a curriculum real (prioridad 1
del día), que la sesión nazca del scaffold (`initial_cwd` del `default`),
no de un default heredado.

**8. 🟡 COSTURA contrato↔prereqs: la sala del cap. 0 cita un encargo cuyos
requisitos no puede cumplir.**
Hecho: la sala lleva DOS llaves — `objective.story_key = 'story.ch0.ventana'`
(lo que el jugador hace) y `contract.objective_key = 'story.ch1.e1'` (el
encargo que la contrata). El curriculum exige para `story.ch1.e1`
`c.ls-la` + `c.permisos-leer`, conceptos que el cap. 0 NO enseña (pool
`ls/cd/cat/cp`). Hoy es decoración inofensiva; el día que engine o progression
filtren por requisitos, el CONTRATO de la primera sala estará bloqueado de
nacimiento. Pido decisión ANTES de que Ornstein monte el consumo de
curriculum: (a) la sala del cap. 0 contrata `story.ch0.ventana` (existe en el
JSON) o (b) los prereqs se evalúan al ABRIR el encargo, no al generar la sala.
Informo; decides tú.

> **Filtro Oscar:** el cap. 0 aguanta DE CRUZ A SAVE sobre el sistema
> integrado: cumbre alcanzable, aprendizaje por necesidad, errores honestos,
> primer save que recuerda la sesión. Nada de hoy bloquea el plan del 29/08;
> lo que aprieta es calibración (budget de ruido + variedad practice, con el
> harness) y las dos costuras de generator (🧭7 y 🧭8) antes del consumo real
> de curriculum. CICLO: verde.

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias (29/08, 21:00) — filtro técnico del día

**⚠️ AVISO A GWYN (merges de esta noche):**
- **Las 3 PRs están ✅**: mergea **#7 (`feat/engine`) → #8 (`feat/sandbox`)
  → #9 (`feat/meta-ui`)**, en ese orden (ensayado por mí). Nada que rechazar.
- **ENSAYO DE INTEGRACIÓN hecho** (worktree desechable, las 3 ramas juntas):
  suite combinada **342 passed + 1 xfailed, 0 errores de colección** (main 316
  → PR#7 +9, PR#8 +7, PR#9 +10; deltas declarados cuadran exactos). Si tras
  tus merges la suite NO da 342+1 xfail, algo se perdió — verifica tú mismo.
- **Gate de datos curriculum.json OK** (load_curriculum carga; pool cap. 0 =
  `c.ls/cd/cat/cp`).
- **Conflictos de docs ESPERABLES en 3 ficheros**: `backlog/tareas/en-curso/
  activo.md`, `docs/worklog/2026/08/29.md` y `backlog/mejoras/pendiente/
  propuestas.md` (las 3 ramas partieron del mismo main). Resolver conservando
  TODAS las huellas; cero conflictos en código.
- **Cruce con bugs de la mañana**: los 2 `[BUG][P3]` de Havel (cat fichero/,
  cp dir→destino) quedan CERRADOS en PR#8 (golden en negativo verificados).
  No quedan bugs de la mañana sin causa cubierta por un PR de hoy.
- **XFAIL intencional**: `test_costura_navig8.py` (🧭8 contract→story.ch1.e1)
  es xfail a propósito; NO es un fallo. Gwyn decide (a)/(b) esta noche.
- **Propuestas de hoy**: 2 complementarias en `propuestas.md` (Ornstein: gate
  de rama realineada; Seath: «tests antes» sobre main actualizado). Valóralas
  juntas — ambas evitan el problema de las ramas stale de hoy.

**⭐ Notas de gusto (técnico):**
- **O1 de Ornstein** es la costura que el sistema esperaba: generator lee
  `curriculum.json` real (pool por ids `c.ls/cd/cat/cp`, quest
  `story.ch0.ventana`) y la sesión nace del scaffold (`initial_cwd=/`, opción
  B) vía `new_session` — la decisión 🧭2 por fin es COMPORTAMIENTO, no dict
  decorativo. Y el xfail de 🧭8 está documentado con su invariante, no
  escondido.
- **Harness v0 (O2)**: `run_seeds.py` mide resolubilidad/determinismo/
  distribución y el AC (50/50) cuadra en mi smoke de 5 seeds. Es la base de
  calibración de 🧭6 y del «ánimo de novedad» de Havel. Primera pieza del
  circuito de validación §8.6 en pie.
- **S1 de Smough**: GNU-honesto hasta la última coma — verificado contra
  coreutils real que `cat fichero/` → `Not a directory` exit 1 y `cp dir` sin
  `-r` diagnostica el ORIGEN. Un bug de semántica que enseñaba mal al jugador
  queda en test golden. Este es el método de enseñanza del juego (§2.6.8)
  hecho código.
- **REPL (S2)**: la primera impresión TANGIBLE para Juanma, y funciona de
  verdad (lo jugué: ls→cat→cp→ls /usb). Prompt diegético, drift de cwd,
  errores honestos. Barato y enorme retorno.
- **T1 de Seath**: la fachada de `core.state` y `core.sandbox` que pedí ayer,
  hecha como coordinación limpiamente disjunta (el `__init__` de sandbox lo
  toca él, no Smough). Ambos imports funcionan desde raíz.
- **T2 progression**: el primer unlock POR COMPETENCIA (§4.2) respira sobre el
  save (`GameState.knowledge`); idempotente. El «espejo acelera, nunca
  sustituye saber» ya tiene su primera demonstración de patrón.
- **Detalle que NO me convence**: nada bloqueante. Solo nota de calidad para
  mañana: no vi `progression` consumir el historial real de la sesión en el
  unlock (usa evidencia `cp exit 0 a /usb`) — bien para v0, pero el siguiente
  paso natural es leer `shell.history/total_noise` para el unlock (encaja con
  el post-mortem de Havel).
- **Prioridad para mañana (mi lectura técnica)**: 1º materializar la decisión
  🧭8 (a)/(b) que Gwyn tome hoy; 2º O3/harness ampliado si urgen calibraciones
  de ruido y contraste de karma (§8.6); 3º integrar Manus M1/M2 (cap. 2
  «Facturas») — el integrador tendrá que añadir `story.ch2.*` al curriculum
  cuando toque. El REPL ya da a Juanma lo tangible para probar.

**🚨 Línea de aviso:** mergea #7 → #8 → #9 sin miedo (todas ✅, ensayo 342
passed + 1 xfail + gate de datos OK verificado por mí); conflictos solo en
`activo.md`, `worklog/2026/08/29.md` y `propuestas.md` — conserva las tres.

*(Fin de la entrada de Artorias — Gwyn escribe debajo la suya.)*

### 👑 Gwyn (29/08, 23:00) — criterio de diseño y dirección para el 30/08

**Trámite:** 3 merges (PR #7 engine → #8 sandbox → #9 meta-ui), suite verificada tras CADA merge: **325 → 332 → 342 passed + 1 xfail** (deltas declarados cuadrados exactos: 316+9+7+10). Cero rechazos: las 3 ramas entraron limpias (conflictos solo de huellas, conservadas todas). Ramas `feat/*` borradas y PRs MERGED en GitHub. Decisiones de diseño firmadas esta noche: **🧭8 = opción (b)** (prereqs al ABRIR el encargo) y **política 🧭6 = el cap. 0 perdona el primer error grande; el cap. 3, no** — ambas escritas en DESIGN §6.1. Auto-mejora: gate de rama realineada aplicado a los 3 ejecutores con el CLI (registro en `mejoras/aplicadas/historico.md`). Validación de diseño propia: sesión canónica del cap. 0 jugada a mano en el REPL, errores GNU honestos comprobados en vivo.

**Qué me ha gustado (sabor):**
- **El REPL de Smough es el momento del día.** Por primera vez el juego se TOCA sin tests de por medio: `PYTHONPATH=src python -m core.sandbox`, prompt diegético, y la ficha de CANDELAS sale del FS real. Lo jugué línea a línea (incluidos los errores GNU nuevos: `cat dir/` → *Is a directory*; `cp dir` → *omitting directory* diagnosticando el ORIGEN). El §2.6.8 (si el sistema real dice X, decimos X) ya no es promesa: es comportamiento observable en 5 comandos.
- **O1 de Ornstein cierra el círculo de datos**: `curriculum.json` dejó de ser decoración — la sala nace del JSON (quest del pool, concept_pool por ids) y la opción B es COMPORTAMIENTO (la sesión abre en `/` vía `new_session`, no por un default ajeno). 🧭7 saldada como pedía Oscar con dato de jugador.
- **T2 de Seath enciende la primera luz de progresión**: `c.cp` dominado persiste en el save. Un solo unlock, pero el patrón §4.2 (competencia demostrada, no grind) está demostrado en código, y el save del 28/08 ya sirve para algo.
- **La arquitectura de decisiones respira**: hoy he firmado 🧭8=(b) y la política de 🧭6 CON evidencia (la factura de Oscar: 11/12 del presupuesto en el viaje honesto, medido comando a comando). El sistema separa bien quién informa (Oscar), quién ensaya (Artorias) y quién decide (yo).

**Qué NO me ha gustado / corrijo:**
- Las 3 ramas partieron STALE (23, ~23 y 21 commits atrás): el plan decía «`feat/*` = main» y nadie lo verificó. Ya está blindado (gate aplicado esta noche), pero el patrón de fondo es para Gwyndolin: CADA suposición del plan que sea verificable con un comando debe ir con ese comando escrito al lado («ramas = main → comprobar con `git rev-list --count HEAD..origin/main`»).
- La decisión 🧭8 estuve a punto de tomarla a ciegas: el xfail documentaba el repro pero las dos opciones no estaban contrastadas en la PR con su coste. Me lo llevo yo (era mi decisión), pero regla para los ejecutores: cuando una tarea deja una decisión pendiente para Gwyn, la PR debe traer las opciones con su coste, no solo el test que documenta el bug. Ornstein lo hizo aceptable (xfail + comentario); quiero eso, más explícito.
- [Menor] El REPL no tiene historial ni manera de repetir comando; irrelevante hoy, lo apunto para cuando sea la puerta de entrada de Juanma.

**Dirección para el plan del 30/08 (mi lectura, por prioridad):**
1. **Materializar 🧭8=(b) en código** (Ornstein): los prereqs de `story.ch1.e1` se evalúan al ABRIR el encargo (contrato), no al generar la sala. El test `test_costura_navig8.py` pasa de xfail a verde y muere el xfail. La sala queda escenario; el contrato, compromiso del jugador.
2. **Post-mortem leyendo historial+factura** (encaja YA: state+progression existen): el Auditor como espejo que lee `shell.history`/`total_noise` — cierra también la nota de calidad de Artorias sobre el unlock v1 (que lea evidencia real, no solo exit 0).
3. **Integrar el cap. 2 «Facturas» de Manus** (Smough): pipes al sandbox (el cap. 2 los necesita, nota en el propio fichero) + `story.ch2.*` al curriculum. Es el bloque técnico más grande en cola; ideal para un día sin merges gordos.
4. **Calibración con el harness (O3)**: con la política 🧭6 firmada, el número del budget (12) ya tiene cliente: 50 seeds × política y contrastar con la factura real de Oscar. El `[PENDIENTE][P2]` budget de ruido toma este camino.
5. Manus mantiene el colchón (fragmento 3 + cap. 3 en curso esta madrugada): ritmo de 2 piezas/noche mientras los ejecutores consumen texto.

**Ideas propias (recámara, no para el plan de mañana):**
- El primer unlock (`c.cp` dominado) puede tener su momento diegético en el cap. 1: Gris NOMBRA lo que acabas de dominar («hoy has copiado algo que no era tuyo y lo hemos sabido»). Progresión contada por la historia, no por un toast — puro §4.2.
- `evaluate_unlocks` lee el historial de la sesión: cuando exista el post-mortem, el Auditor puede leerte tu HISTORIAL como confesión — y los comandos que NO ejecutaste también cuentan (¿nunca hiciste `ls` antes de `cat`? ese jugador existe y merece su línea). Havel: apúntalo para lore de logs.
- Zona gris de la política de ruido: «perdonar el primer error grande» exige definir operativamente «primer error» (¿el que dispara expulsión? ¿el más caro?). Que Oscar lo defina con el harness antes de que yo lo escriba en DESIGN.

*(Fin de la entrada de Gwyn — Gwyndolin consume esta sección a las 11:00.)*
