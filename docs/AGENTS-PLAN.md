# AGENTS-PLAN — Estructura del sistema de agentes (CyberRoot)

> Fecha: 23/08/2026 · Estado: **definitivo v1.0 (decisiones de Juanma cerradas).**
> Repo: `amcgiluma/CyberRoot` (público) — creado y conectado (commit `9d4c0f9`).
> Este documento y todo el sistema fueron diseñados para ser **públicos**: esta
> estructura es de la que "fardamos" en GitHub. Somos lo más transparentes posible.

## 🧙 NOMBRES DE LOS AGENTES (lore Dark Souls — decisión de Juanma)
El comité es un "concilio" inspirado en Dark Souls. Cada rol tiene nombre:
- 🖤 **Manus, Padre del Abismo** · 03:00 · Historiador (narrativa) — deepseek-v4-flash
- ⭐ **Oscar de Astora** · 05:00 · Guardián de la experiencia del jugador (run de referencia + estado global jugable + notas de dirección) — deepseek-v4-flash
- ☀️ **Havel la Roca** · 07:00 · Vidente-creativo (ideas + testeo) — deepseek-v4-flash
- 🌙 **Gwyndolin** · 11:00 · Planificador — deepseek-v4-pro
- ⚔️ **Ornstein** · 13:00 · Ejecutor 1 — deepseek-v4-flash
- 🔨 **Smough** · 16:00 · Ejecutor 2 — deepseek-v4-flash
- 💛 **Seath el Descamado** · 19:00 · Ejecutor 3 — deepseek-v4-flash
- 🐺 **Artorias del Abismo** · 21:00 · Revisor filtro — deepseek-v4-flash
- 👑 **Gwyn, Señor de la Ceniza** · 23:00 · Revisor de diseño + MERGE FINAL — deepseek-v4-pro

---

## 0. El mensaje público (por qué existe esto)
Un "comité de IA diario" te hace un juego: planificador, ejecutores, revisores,
testers e historiador (el Concilio), coordinados por una libreta que es la fuente.
No hay nada que ocultar: se explica, se documenta y se presume. El proceso
es la feature además del producto.

## 1. Principio rector
Juanma decide el **qué** (dirección, gusto, feedback). El sistema ejecuta el
**cómo** en bucle diario cuasi-autónomo. Toda decisión queda en la libreta
con fecha y motivo. El bucle fluye solo; Juanma solo interviene cuando el
sistema se lo pide explícitamente (casos excepcionales) o para criterio.

## 2. Fuente de verdad única: la LIBRETA
Cada cron arranca sin memoria conversacional. Todo se persiste en el repo:
```
docs/PROJECT-MAP.md      → mapa de módulos (qué es cada cosa, dónde) ← GUÍA CLAVE
docs/DESIGN.md           → el diseño del juego (vivo, se actualiza)
docs/ADR/                → decisiones de arquitectura (incl. las de IA/eficiencia)
backlog/INDICE.md        → mapa del backlog: qué fichero lee/escribe cada rol ← GUÍA CLAVE DEL BACKLOG
backlog/tareas/          → tareas por estado: pendiente/abierto.md · en-curso/activo.md · hecho/<AAAA-MM>.md (archivo POR MES) · descartado/historico.md
backlog/mejoras/         → auto-mejora: pendiente/propuestas.md (los agentes proponen) · aplicadas/historico.md (registro de Gwyn)
backlog/zona-testeo.md   → la ZONA 🔬 del día (Gwyn escribe al cierre; Oscar/Havel leen)
backlog/notas-manana.md  → notas rodantes para mañana (🧭 Oscar → Gwyn · 🎯 revisores → planificador)
backlog/planes/          → HISTÓRICO de planes diarios: planes/YYYY/MM/DD.md (hoy = fecha actual)
backlog/historia/        → la narrativa de Manus (con índice, personajes, capítulos)
docs/worklog/            → registro diario por fechas: worklog/YYYY/MM/DD.md
docs/AGENTES.md          → roles del concilio: qué hace cada agente (supervisión mutua)
backlog/mejoras/         → auto-mejora del comité: pendiente/propuestas.md + aplicadas/historico.md
```
**Regla de oro:** ninguna IA vuelve a leer todo el proyecto. Leen el
`PROJECT-MAP.md` + la guía del módulo relevante + las tareas que les tocan.
**Planes por fecha:** en vez de un único `PLAN-del-dia.md`, cada día guarda su
plan en `backlog/planes/YYYY/MM/DD.md`. El planificador escribe el de hoy; los
ejecutores leen "el plan de hoy" (fecha actual). Se conserva el histórico completo.

## 2.5 PROTOCOLO DE COMUNICACIÓN — CÓMO SE SABE QUÉ HACER Y QUÉ SE HIZO ⭐

> **Este es el corazón del sistema.** Cada cron arranca SIN memoria. La ÚNICA
> forma de que el comité se coordine solo es que TODO el trabajo quede escrito
> en sitios conocidos, y que cada agente siga estos 4 pasos en orden.

### Paso 0 de TODO agente: "¿DÓNDE ESTÁN LAS COSAS?"
Lee SIEMPRE, en este orden, al arrancar:
1. `docs/PROJECT-MAP.md` → mapa de módulos y quién escribe dónde.
2. `docs/AGENTES.md` → QUÉ hace cada agente del concilio (sabes con quién coordinas).
3. `backlog/INDICE.md` → mapa del backlog, y SOLO los ficheros de tu fila (qué hay pendiente/en curso/hecho sin leerlo entero).
4. `docs/DESIGN.md` → la visión que NO puedes romper.
5. (Si eres planificador) `backlog/historia/` (para saber la historia) + el día de ayer de `docs/worklog/`.
6. (Si eres ejecutor) `backlog/planes/YYYY/MM/DD.md` (HOY) → tu tarea asignada.
7. `backlog/mejoras/pendiente/propuestas.md` → revisa si hay propuestas de auto-mejora pendientes que te afecten.
Después, SOLO tocas el módulo de tu tarea, nunca el código entero.

### Paso 1: "¿QUÉ TENGO QUE HACER HOY?"
- Manus/Oscar/Havel: leen lo de ayer y generan (Manus = historia, Oscar =
  run de referencia + notas de dirección, Havel = ideas frescas + jugar).
- Planificador: coge lo `[PENDIENTE]` de `backlog/tareas/pendiente/abierto.md` (incluidas las ideas de Havel)
  → redacta `backlog/planes/YYYY/MM/DD.md` (hoy) sin esperar aprobación humana.
- Ejecutores: cogen SU tarea del plan (la que les asignó el planificador).
- Revisores: revisan los PR/diff de hoy.

### Paso 2: HACER el trabajo (en tu zona, sin pisar a otros)

### Paso 3: "¿DÓNDE DEJO LO QUE HE HECHO?" — SIEMPRE ESCRÍBIRLO (obligatorio)
Cada agente, al terminar, DEJA SU HUELLA en ubicaciones fijas (ver tabla
en PROJECT-MAP). Las reglas de oro de la escritura:

1. **Marca el estado en el fichero del backlog que corresponda** (`backlog/tareas/…`, ver INDICE) SIEMPRE → `[HECHO]` | `[EN CURSO]`
   | `[DESCARTADO]`. Nunca dejes una tarea "en el aire" sin estado.
2. **Actualiza el WORKLOG** (append en `docs/worklog/YYYY/MM/DD.md` del día): qué
   hice, decidí, y POR QUÉ.
   El "porqué" es tan importante como el "qué" (es el razonamiento del comité).
3. **Actualiza el README del módulo** que tocaste (si cambió su comportamiento).
4. **Deja el entregable en su sitio:** historia → `backlog/historia/...`; plan → `backlog/planes/YYYY/MM/DD.md`; ADR → `docs/ADR/<fecha>-<tema>.md`.
5. **Commit + push.** El repo es la memoria física del comité.

### Paso 4: el RELEVO (cómo sigue el sistema)
Al terminar tu turno dejas "la pelota" en un sitio concreto para el siguiente:
- **Manus →** deja historia en `backlog/historia/` para planificador/ejecutores.
- **Oscar →** actualiza `docs/ESTADO-JUGADOR.md` (estado jugable + run de
  referencia) y deja NOTAS DE DIRECCIÓN para Gwyn en `notas-manana.md` (🧭); ejecuta primero la
  zona 🔬 del relevo Gwyn → Oscar → Havel (`docs/TESTEO-DIARIO.md`).
- **Havel →** deja ideas frescas y bugs en `tareas/pendiente/abierto.md`; Gwyndolin las planifica directamente (fuente creativa autónoma).
- **Planificador →** deja el plan en `backlog/planes/YYYY/MM/DD.md` (fecha de hoy) para que los ejecutores lo lean.
- **Ejecutores →** marcan `[HECHO]` para que los revisores validen ese PR.
- **Artorias →** marca 💥/✅ y deja NOTAS DE GUSTO + "qué no mergear" para mañana.
- **Gwyn →** escribe el reporte final, deja SUS notas de gusto/ideas, y avisa a Juanma en Telegram.

### La regla que NUNCA se rompe
> **"Ningún agente termina su turno sin haber escrito dónde ha dejado su
> trabajo."** Si un turno no deja huella (estado, entregable o registro),
> el sistema se rompe al día siguiente. Documentar NO es opcional: es parte
> de "tarea terminada". Esto es una regla HARD en cada prompt de cron.

## 2.6 AUTO-MEJORA del comité (los agentes pueden mejorarse a sí mismos) ⭐
El comité no es estático: puede mejorar su propio funcionamiento.

- **Visión:** si un agente detecta que su tarea no se puede hacer bien, que el
  flujo tiene un cuello de botella, que su prompt es ineficiente o que otro rol
  podría hacer algo mejor, puede proponer un cambio.
- **DÓNDE:** `backlog/mejoras/pendiente/propuestas.md` — formato `[PROPUESTA]` (problema/propuesta/
  impacto/estado). Ver `docs/AGENTES.md` (sección AUTO-MEJORA) para las reglas.
- **QUIÉN APLICA: Gwyn (revisor final, 23:00) decide y APLICA** las mejoras
  aprobadas usando el CLI OFICIAL (`hermes cron edit --prompt ... <job_id>`),
  que es válido y con respaldo — NO edita `jobs.json` a mano. Cualquier agente
  propone en `mejoras/pendiente/propuestas.md`; Gwyn decide el contenido Y lo aplica; Juanma supervisa.
- **Esqueleto protegido:** horarios del concilio y cadena de PRs/merge NO se
  cambian sin aprobación de Juanma (se pueden PROPONER en `mejoras/pendiente/`, no auto-aplicar).
- **Cada agente sabe qué hace el resto** (lee `docs/AGENTES.md` arriba), lo que
  le da contexto para proponer mejoras con criterio.

## 2.7 DELEGACIÓN — los agentes pueden invocar sub-agentes (coordinadores) ⭐
Los 9 agentes del Concilio tienen la herramienta `delegate_task`: pueden invocar
**sub-agentes** para ejecutar tareas y así NO llenar su ventana de contexto,
coordinando trabajo de forma más eficiente. Detalle completo en `AGENTES.md`
(sección "DELEGACIÓN").

**Resumen del patrón (plan → delega → verifica → reinvoque):**
1. **Evalúa si conviene delegar** (tarea extensa/independiente → delega; corta → hazla tú).
2. **Invoca sub-agentes enfocados** (1 pieza acotada cada uno, con todo el contexto).
3. **VERIFICA el resultado real** (git log, tests, ficheros) — no te fíes del resumen.
4. **Si falla la verificación**, reinvoca el ciclo con el fallo como entrada.

**Config:**
- Modelo de sub-agentes = `deepseek-v4-flash` (barato) fijado en `delegation.model` — incluso
  si el coordinador es Gwyn (caro), los sub-agentes son baratos.
- Límites: 3 sub-agentes simultáneos; anidamiento de 1 nivel (sub-agentes son hojas,
  no pueden volver a delegar). Para tareas grandes, repetir el ciclo, no anidar.
- Coste: cada sub-agente es una ejecución más → usar con criterio.

## 2.8 SKILLS DE PROYECTO — los agentes pueden crear skills locales ⭐
Los agentes del proyecto tienen el toolset `skills` (pueden usar `skill_manage` para
cerrar/actualizar skills). Esto les permite crear **skills locales a nivel de proyecto**
que estandarizan tareas repetitivas y codifican el conocimiento propio del proyecto.

- **Qué es una skill aquí:** un documento markdown reutilizable que cualquier agente
  carga antes de una tarea para hacerla bien y consistente (p.ej. "cómo escribir
  niveles de CyberRoot", "cómo limpiar AI-slop en la historia", "cómo revisar un PR
  del Concilio", "cómo generar una run del harness").
- **Por qué importa:** el HERMES crea skills automáticamente cuando lo necesita, pero
  podemos adelantarnos: la Fase 0 debe planear las skills iniciales que estandaricen
  el trabajo, y el proyecto las va MEJORANDO conforme avanza (mismo mecanismo que la
  auto-mejora: si una skill queda obsoleta o floja, se actualiza).
- **Dónde viven:** en la carpeta de skills de la sesión del proyecto. NO se suben al repo
  sin revisión (o si se suben, como referencia). Lo importante es que el agente las
  carga y las mejora.
- **Regla de mejora:** igual que los agentes se mejoran a sí mismos, las skills se
  mejoran: si una skill no sirve o falta una, proponer/crear una (skill_manage).

**Nota (decisión de Juanma):** NO hace falta un `AGENTS.md` de proyecto porque el
índice (PROJECT-MAP + libreta) ya cubre la navegación; las skills complementan eso
con procedimientos estandarizados reutilizables.

---

## 3.1 Modelos VERIFICADOS (proveedor opencode-go, 100% confirmados)
Listados con `opencode models opencode-go`:
- `opencode-go/deepseek-v4-flash` — Manus, **Oscar**, Havel, ejecutores, revisor filtro
- `opencode-go/deepseek-v4-pro` — planificador (Gwyndolin) y revisor de diseño (Gwyn)
- `opencode-go/ox-alpha-free` — **Fase 0 (research + diseño + arquitectura + coordinador)**: modelo potente, GRATIS durante ~1 semana (decisión de Juanma). Los 10 jobs de Fase 0 usan este modelo. Cuando caduque la gratuidad, volver a los modelos estándar.
(Disponibles además: grok-4.5, glm-5.2, kimi-k2.7-code, qwen3.8-max… si algún día se decide un cambio de modelo.)

## 3.2 Panel de uso — fuente de verdad REAL (verificado)
`opencode stats` es la fuente oficial de uso/coste. Soporta:
- `--days N` → estadísticas de los últimos N días (para el volcado diario).
- `--models` → desglose de coste/tokens POR modelo (clave: ver cuánto gasta
  el planificador caro vs los flash baratos).
- `--tools` y `--project` para filtrar.
Suscripción OpenCode Go = $10/mes fijo → el panel monitoriza que el comité
diario se mantenga dentro de esa cuota. El volcado a `docs/USAGE.md` se
automatizará con este comando (pendiente: cron de uso + formato del doc).

## 3.3 Estructura de documentación por MÓDULOS (decisión clave)
Para que las IAs no lean TODO el proyecto, cada módulo tiene:
```
src/<modulo>/
  README.md      → qué hace este módulo, sus entradas/salidas, cómo se testea
  ARCHITECTURE.md→ decisiones internas del módulo (si hace falta)
```
- El `docs/PROJECT-MAP.md` es el **índice maestro**: lista cada módulo, su
  README, dependencias y quién lo toca. Un agente lee SOLO el map + el módulo
  de su tarea, nunca el código entero.
- **Tras cada tarea, el agente documenta**: actualiza el README del módulo,
  su fichero en `backlog/tareas/` (marca hecho/descartado) y el WORKLOG (qué y por qué, en la ruta del día). Documentar es
  obligatorio y forma parte de "tarea terminada".
- La guía de navegación para agentes también se documenta en el
  `PROJECT-MAP.md` y en el README público del repo (autoexplicativo para el
  que lo vea en GitHub).

---

## 4. CRONS DE AGENTES (horario Madrid) — el CONCILIO

### 03:00 — 🖤 MANUS, Padre del Abismo · Historiador · deepseek-v4-flash
- Escribe la HISTORIA del día desde el **plot general** (Fase 0).
- Entrega narrativa en `backlog/historia/<fecha>.md` para planificador/ejecutores.
- Su prosa pasa criterio `humanizer`. En Fase 0 además investiga skills anti-slop.

### 05:00 — ⭐ OSCAR DE ASTORA · Guardián de la experiencia · deepseek-v4-flash
- **Capa EXPERIENCIA/PROGRESIÓN del testeo diario** (`docs/TESTEO-DIARIO.md` §1):
  ejecuta PRIMERO la zona 🔬 que dejó Gwyn la noche anterior (relevo
  Gwyn → Oscar → Havel).
- Run de referencia desde SAVE LIMPIO (el dueño del save limpio es él) +
  perspectiva de VETERANO (20+ h). Mantiene vivo `docs/ESTADO-JUGADOR.md`
  (qué es jugable HOY de principio a fin).
- Deja NOTAS DE DIRECCIÓN para Gwyn en `backlog/notas-manana.md` (🧭; informa, NO decide)
  y su línea CICLO en el worklog. NO genera ideas de contenido ni valida código.

### 07:00 — ☀️ HAVEL la Roca · Vidente-creativo (jugar + idear) · deepseek-v4-flash
- **Rol enfocado y ligero (2 cosas, no más):**
  1. **JUEGA** lo nuevo del día anterior por `git log` + **smoke del CONJUNTO**
     (¿el juego entero sigue arrancando/avanzando?). **SIN save limpio**: la
     run de referencia desde cero es capa de Oscar (05:00, TESTEO-DIARIO.md).
  2. **GENERA ideas nuevas** constantemente (capítulos, mecánicas, objetos, boons,
     comandos Linux, bifurcaciones, enemigos, logros) para que el juego crezca solo.
- Anota bugs y las nuevas ideas en `backlog/tareas/pendiente/abierto.md` como `[PENDIENTE]` (sin implementar:
  eso lo hacen los ejecutores tras el planificador). Es la **chispa creativa**.
- **NO** lleva la crítica de diseño ni las notas de gusto para mañana: eso es de los
  revisores (Artorias y Gwyn) para no sobrecargarlo. Él siembra, ellos deciden.
- Distingue hechos (lo que prueba) de opiniones.

### 11:00 — 🌙 GWYNDOLIN, Dark Sun · Planificador · deepseek-v4-pro (caro) ⚠️
- **NO gastar demasiados tokens.** Las ideas le llegan mascadas; él estructura.
- Redacta `backlog/planes/YYYY/MM/DD.md` (HOY): tareas concretas {módulo, descripción, aceptación}.
- **REGLA DE TAMAÑO:** cada tarea debe ser una pieza pequeña y AUTÓNOMA que un
  ejecutor (o sus sub-agentes) complete en un turno, sin llenar su contexto.
  Si una idea es grande, la FRACCIONA en varias tareas con orden. Criterio:
  "un ejecutor la entiende sin releer todo y la acaba en su franja".
- **INICIATIVA DE CURACIÓN:** decide TÚ qué toca hoy de las tareas abiertas completas (`pendiente/abierto.md`; da igual
  la antigüedad de la tarea). Elige lo más valioso/interesante/urgente; no
  repitas mecánicamente lo pendiente. Si algo antiguo sigue siendo importante,
  tráelo; si no aporta, propón descartarlo.
- **RAMAS HUÉRFANAS (regla explícita):** comprueba `git branch -a` y `gh pr list`.
  Si hay una rama/PR de días atrás que quedó SIN cerrar (sin merge de Gwyn Y sin
  rechazo), inclúyela en el plan de HOY: dale a su ejecutor un mini-plan para
  terminarla y cerrarla. Ninguna rama muere en el limbo. Las correcciones de
  ramas rechazadas por Gwyn también (el ejecutor las arregla primero).
- Reparte trabajo entre Ornstein/Smough/Seath en módulos que NO colisionen.
- Si requiere decisión importante: mensaje urgente a Juanma (Telegram) → ejecutarla
  al día siguiente. Solo casos excepcionales.

### 13:00 — ⚔️ ORNSTEIN · Ejecutor 1 · deepseek-v4-flash
### 16:00 — 🔨 SMOUGH · Ejecutor 2 · deepseek-v4-flash
### 19:00 — 💛 SEATH el Descamado · Ejecutor 3 · deepseek-v4-flash
- Implementan tareas en SU módulo; **conscientes de los otros 2** → no colisionar.
- **Si una tarea es demasiado grande → la PARTEN y DELEGAN** en sub-agentes
  (`delegate_task`, baratos flash) para las piezas independientes; coordinan y
  **verifican el resultado real** de cada sub-agente. No lo hacen todo en su contexto.
- Verifican su pieza con tests reales. Documentan y marcan `[HECHO]` al terminar.

### 21:00 — 🐺 ARTORIAS del Abismo · Revisor filtro · deepseek-v4-flash
- Se toma su tiempo probando (juego + tests + lint + smoke).
- Marca 💥 / ✅ en `backlog/tareas/en-curso/activo.md`. Rechaza lo roto con comentario accionable.

### 23:00 — 👑 GWYN, Señor de la Ceniza · Revisor de diseño + MERGE · deepseek-v4-pro
- Revisión profunda: ¿el PR sigue la visión del `DESIGN.md`? (no solo que "compila").
- Integra las NOTAS DE DIRECCIÓN de Oscar (05:00) en su validación.
- **Decide LA ZONA 🔬 de testeo de mañana** (`docs/TESTEO-DIARIO.md` §4): la
  SOBRESCRIBE al cierre `backlog/zona-testeo.md`; el relevo de la zona es
  **Gwyn → Oscar (05:00) → Havel (07:00)**.
- Modelo distinto al constructor → no se auto-aprueba.
- **Cuidado con tokens; no excedernos.**
- **Es el encargado del MERGE FINAL:** tras ver la revisión de Artorias (21:00),
  da el visto bueno y **mergea** el PR. Luego envía a Juanma un **reporte**.
- Sin gate de humanización obligatorio (rompe ciclo) — reporta y Juanma avisa si ve algo.

### 🔄 Cadena de PRs y ramas (decisión confirmada) ★
1. **Ejecutor** (Ornstein/Smough/Seath) crea su RAMA (`feat/<modulo>`), trabaja ahí,
   abre P.R. a `main`. Nunca toca `main` directamente.
2. **Artorias** (21:00) revisa las ramas/PRs, prueba técnicamente, marca 💥/✅
   y avisa a Gwyn qué NO mergear (+ notas de gusto para mañana).
3. **Gwyn** (23:00) — el ÚNICO que mergea — revisa en profundidad y:
   - Si está bien y sigue el diseño y Artorias lo aprobó → **mergea** a `main`.
   - Si NO se debe mergear → NO la mergea, NO borra la rama, y deja documentado:
     **POR QUÉ no se ha mergeado** y **CÓMO arreglarlo** (para que el ejecutor lo coja).
     Registrado junto a la línea en `backlog/tareas/en-curso/activo.md` (+ comentario del PR). La tarea sigue `[EN CURSO]`.
4. Gwyn reporta a Juanma (qué se mergeó, qué no y por qué, cómo arreglarlo).
5. Al día siguiente, el ejecutor cuya rama fue rechazada la arregla PRIMERO (lo dejo
   marcado como máxima prioridad en su prompt).

---

## 5. Humanizer (regla + Manus) ✅ confirmado
- **Regla en todos los agentes** (decisión cerrada): la prosa del juego pasa
  criterio del skill `humanizer` (34 patrones anti-AI-slop de Wikipedia) para
  que no suene a AI-slop.
- **Manus** (historiador) es quien produce la narrativa, con humanizer aplicado.
- **En la Fase 0, Manus investiga skills anti-slop** que sirvan de verdad para
  escribir la narrativa y los niveles del juego (no solo el humanizer base);
  los hallazgos se documentan como skill/guía para el comité.

---

## 6. Fase 0 — Arranque (primeros 4 días) — CRONS DISTINTOS ⚡⚠️
> **IMPORTANTE: la Fase 0 NO usa los crons del Concilio (sección 4).** Son
> crons one-shot/temporales solo para diseñar. El objetivo: producir el
> `DESIGN.md` + plot + mapa de módulos. NO escribir código del juego.
> **Modelo de Fase 0: `opencode-go/ox-alpha-free`** (potente, gratis ~1 semana).

### Pipeline de Fase 0 (10 one-shot, tareas largas descompuestas en pasadas)
| Día | Hora | Job one-shot | Producción |
|-----|------|--------------|------------|
| 1 (24/08) | 03:00 | Research Stack | `docs/INVESTIGACION-STACK.md` |
| 1 (24/08) | 05:00 | Research anti-slop (Manus) | `docs/SKILLS-ANTISLOP.md` |
| 1 (24/08) | 07:00 | Research mecánicas + dopamina | `docs/RESEARCH-MECANICAS.md` |
| 2 (25/08) | 11:00 | Diseñador P1 | `docs/DESIGN.md` (concepto+historia/plot) |
| 2 (25/08) | 16:00 | Diseñador P2 | `docs/DESIGN.md` (revisión + roguelite) |
| 3 (26/08) | 09:00 | Diseñador P3 | `docs/DESIGN.md` (capítulos/niveles) |
| 3 (26/08) | 14:00 | Diseñador P4 | `docs/DESIGN.md` (dopamina/UX) |
| 3 (26/08) | 18:00 | Diseñador P5 | `docs/DESIGN.md` (revisión final) |
| 4 (27/08) | 11:00 | Arquitecto | módulos `src/<mod>/README.md` + tabla PROJECT-MAP |
| 4 (27/08) | 18:00 | Coordinador de cierre | resumen + pide el gate a Juanma |

- **Gate de Juanma** al final de la Fase 0: revisa `DESIGN.md` + mapa de módulos,
  da el visto bueno (o pide cambios).
- Con el OK, los one-shot de Fase 0 ya habrán corrido; se activa el **Concilio**.

> Nota: los jobs de diseño se nombran como "Diseñador Jefe" en varios prompts;
> todos usan `ox-alpha-free`. El "Diseñador Jefe" = el rol que produce DESIGN.md.

### 6.1 Estructura de CARPETAS por agente (a decidir en Fase 0) ⭐
Durante la Fase 0, el Diseñador/Arquitecto debe definir la estructura de CARPETAS
DE TRABAJO de cada agente del Concilio (dónde guarda cada uno sus entregas
internas), no solo los módulos de código. Ejemplo orientativo para Manus:
```
backlog/historia/
  INDICE.md               → índice del arco narrativo
  PERSONAJES.md           → descripciones de cada personaje, motivaciones, arcos
  ESCENARIOS.md           → descripciones de cada escenario/lugar (la Base, las redes...)
  CAPITULOS/
    00-piloto.md          → resumen/esquema del capítulo 0 por hacer
    01-<nombre>.md        → lo escrito del capítulo 1...
  (por capítulo: esquema primero, texto después)
```
Otros agentes, si necesitan su carpeta de trabajo (Havel ideas, Manus historia,
Gwyndolin planes fundiendo el histórico, etc.), también se definen aquí.
Regla: cada agente sabe su carpeta como parte de `PROJECT-MAP.md`. Esto se
concreta en la Fase 0 y se registra en `docs/PROJECT-MAP.md`.

## 6.5 DISEÑO DEL JUEGO — dos norteas confirmadas (decisión de Juanma)

### 🎰 Dopamina ("estilo Balatro")
El juego debe ser **super dopaminérgico**: muchísimos números, estadísticas,
combinaciones, decisiones rápidas adictivas y feedback numérico constante.
Cada acción debe "cosquillear" el cerebro del jugador (puntos que suben,
combos, desbloqueos, contadores). Esto es un objetivo de diseño EXPLÍCITO que
el DISEÑADOR JEFE (Fase 0) debe convertir en mecánicas concretas. No un
"nice-to-have": es una decisión de diseño cerrada.

### ☠️ ROGUELITE HÍBRIDO "estilo Hades" ★ (decisión de Juanma — confirmada)
Juanma ha decidido el modelo de referencia: **Hades**. No es un roguelite puro
ni una historia lineal: es exactamente la fórmula de Hades, vuelta a un
contexto de hacking + aprendizaje de Linux. La clave de Hades que lo hace útil
aquí: **la muerte no corta el avance, lo alimenta.** Eso resuelve la trampa
educativa (que fallar no sea frustrante, sino parte de aprender).

**Cómo se traduce "Hades" a este juego:**
- **La Run = infiltrar una red/servidor** generada proceduralmente (permisos,
  puertos, servicios, trampas varían en cada Run). Objetivo: robar/defender el
  objetivo (dato, flag, root…).
- **La Muerte = te detectan / el sistema te echa.** No es game-over: vuelves
  a la base y la historia AVANZA. Cada muerte trae diálogo/consecuencia nueva.
- **La Base (equivalente a la casa de Zagreus)** = el Hub donde vives entre
  Runs: hablas con aliados (avanza la narrativa), mejoras tu equipo, gastas
  recursos, ves tu progresión permanente. El corazón del avance narrativo.
- **Boons/Mejoras** = boons de CONOCIMIENTO: cada Run (o muerte) te deja
  aprender/desbloquear comandos, exploits, perks. "Descubrir comandos y
  poderes nuevos" al estilo del NPC que te regala un boon.
- **Karma Blue/Red = los caminos**: decisiones DENTRO y ENTRE Runs inclinan
  tu karma y abren finales distintos. Muchos finales según lo que elijas hacer.
- **Metaprogresión (toque de Hades)**: mejoras permanentes entre Runs que se
  conservan al morir (el "espejo" de Zagreus). El aprendizaje DE VERDAD es la
  metaprogresión: cada comando aprendido te hace más fuerte para la siguiente.
- **Visual/UX**: aquí ABANDONAMOS el "todo en terminal". Necesita un MAPA DE
  NODOS (a qué sala/Run ir), HUD de estado, selector de equipo/objetivos y
  feedback numérico chillón. La interacción de RESOLVER cada sala puede ser
  terminal (escribes comandos reales), pero el mapa/HUD/equip son visuales
  (pixel-art). Lo mejor de ambos mundos: parece un hacker, se siente un juego.

**Marcos cerrados para el Diseñador Jefe (Fase 0):**
1. Loop maestra: Run → (muerte/éxito) → Base (historia + mejoras + metaprogresión) → Run.
2. Historia artificial ramificada por karma (caminos/finales) + roguelite como vehículo.
3. Generación procedural de redes ENSEÑANTE (no sacrifica el aprendizaje por variedad).
4. Muerte = herramienta pedagógica (cada fallo deja lección), no castigo.
5. Dopamina constante (números, combos, unlocks) en cada sistema.

**Por qué esto NO es "demasiado":** porque la historia (heart), el learning
(heart) y el roguelite (vehículo/adrenalina) comparten el MISMO loop y se
reparten el mismo motor. Hades demostró que se puede tener trama profunda +
roguelite adictivo sin que uno mate al otro. Escoge: lo dejamos como "la
referencia de diseño oficial del juego" en el DESIGN.md de la Fase 0.

## 7. Panel de uso / coste de IA (DIARIO) ⚡
- **Objetivo:** monitorizar que la suscripción mensual cubre el gasto del
  comité. OpenCode es transparente con su uso; Hermes también.
- Se registra a diario en `docs/USAGE.md`: tokens/modelo, coste, cuota
  consumida vs mensual. ⚡ Pendiente: definir fuente exacta de métricas y
  automatizar el volcado (cron de uso).
- Toda decisión de eficiencia y arquitectura IA → `docs/ADR/`, público.

---

## 8. Repositorio
- **Público** en GitHub (portfolio + transparencia + "fardar" del comité).
- Sin secretos ni credenciales (ver `.gitignore`).
- README público explica la estructura de agentes, el map de módulos y la
  libreta → self-documenting para el que llegue desde GitHub.
- Mantener MUY friki/organizado: la documentación ES parte del producto.

## 9. Pendiente para arrancar
- [x] Verificar identificadores de modelo (deepseek-v4-pro, deepseek-v4-flash, gpt-5.6-luna, ox-alpha-free — ✅ confirmados via `opencode models`).
- [x] Autenticar `gh` con la cuenta de Juanma (✅ amcgiluma, lista).
- [x] Crear repo público + estructura git + PROJECT-MAP (✅ `amcgiluma/CyberRoot`).
- [x] Concilio nombrado y definido → Manus, Oscar (añadido el 24/08), Havel, Gwyndolin, Ornstein, Smough, Seath, Artorias, Gwyn (9 en total).
- [x] Crear base del registro diario → `docs/worklog/` (por fechas: index + 2026/08/23).
- [x] Modelo `ox-alpha-free` para Fase 0 (gratis ~1 semana, decisión Juanma) — aplicado a los 10 jobs.
- [x] Flujo 100% autónomo: ideas de Havel → Gwyndolin directamente, sin aprobación humana.
- [x] Notas de gusto para mañana → las dejan LOS REVISORES (Artorias + Gwyn), no Havel.
- [x] Flujo de ramas: ejecutores en rama, solo Gwyn mergea, ramas rechazadas con por qué + cómo arreglar.
- [x] Auto-mejora del comité (`docs/AGENTES.md` + `backlog/mejoras/pendiente/propuestas.md`).
- [x] Visto bueno final del Concilio + firma por agente en git + README documentado.
- [ ] Definir cron de uso del panel de métricas (`opencode stats --days N --models`) — ya existe el panel (00:00), falta el formato del doc.
- [ ] **Fase 0** (arranca 24/08 03:00): los 10 one-shot producen DESIGN.md + plot + mapa de módulos.
- [ ] En Fase 0: definir la estructura de CARPETAS por agente (ej. historia/ con INDICE, PERSONAJES, ESCENARIOS, CAPITULOS/ por capítulo) → se registra en PROJECT-MAP.
- [ ] En Fase 0: PLANEAR las skills de proyecto iniciales (skills con `skill_manage` que estandaricen tareas: escribir niveles, limpiar AI-slop, revisar PRs, harness). Se mejoran conforme avanza el proyecto (mismo mecanismo que la auto-mejora).
- [ ] Gate de Juanma al final de Fase 0.
- [ ] Tras el gate → `resume` de los 9 agentes del Concilio; planes diarios en `backlog/planes/YYYY/MM/DD.md`.
- [ ] Harness de playtest automático: Ornstein lo construye para que Oscar y
  Havel (y el comité) jueguen runs headless y midan balance. Debe soportar
  reset a SAVE LIMPIO (lo necesita la run de referencia diaria de Oscar).
- [ ] Fijar nombre definitivo del juego (candidatos en BRAINSTORM).

---
*Este documento pasará por humanizer en su versión final dentro del repo.*