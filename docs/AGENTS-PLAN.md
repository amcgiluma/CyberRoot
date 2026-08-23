# AGENTS-PLAN — Estructura del sistema de agentes (CyberRoot)

> Fecha: 23/08/2026 · Estado: **definitivo v1.0 (decisiones de Juanma cerradas).**
> Repo: `amcgiluma/CyberRoot` (público) — creado y conectado (commit `9d4c0f9`).
> Este documento y todo el sistema fueron diseñados para ser **públicos**: esta
> estructura es de la que "fardamos" en GitHub. Somos lo más transparentes posible.

## 🧙 NOMBRES DE LOS AGENTES (lore Dark Souls — decisión de Juanma)
El comité es un "concilio" inspirado en Dark Souls. Cada rol tiene nombre:
- 🖤 **Manus, Padre del Abismo** · 03:00 · Historiador (narrativa) — deepseek-v4-flash
- ☀️ **Havel la Roca** · 07:00 · Tester de ideas — deepseek-v4-flash
- 🌙 **Gwyndolin** · 11:00 · Planificador — deepseek-v4-pro
- ⚔️ **Ornstein** · 13:00 · Ejecutor 1 — deepseek-v4-flash
- 🔨 **Smough** · 16:00 · Ejecutor 2 — deepseek-v4-flash
- 💛 **Seath el Descamado** · 19:00 · Ejecutor 3 — deepseek-v4-flash
- 🐺 **Artorias del Abismo** · 21:00 · Revisor filtro — deepseek-v4-flash
- 👑 **Gwyn, Señor de la Ceniza** · 23:00 · Revisor de diseño + MERGE FINAL — gpt-5.6-luna

---

## 0. El mensaje público (por qué existe esto)
Un "comité de IA diario" te hace un juego: planificador, ejecutores, revisores,
testers e historiadora, coordinados por una libreta que es la fuente de verdad.
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
backlog/TODO.md          → tareas con estado (pendiente/curso/hecho/descartado)
docs/WORKLOG.md          → registro diario: qué se hizo, qué queda, raciocinio
docs/USAGE.md            → panel de uso/coste de IA (ver sección 7)
```
**Regla de oro:** ninguna IA vuelve a leer todo el proyecto. Leen el
`PROJECT-MAP.md` + la guía del módulo relevante + las tareas que les tocan.

## 2.5 PROTOCOLO DE COMUNICACIÓN — CÓMO SE SABE QUÉ HACER Y QUÉ SE HIZO ⭐

> **Este es el corazón del sistema.** Cada cron arranca SIN memoria. La ÚNICA
> forma de que el comité se coordine solo es que TODO el trabajo quede escrito
> en sitios conocidos, y que cada agente siga estos 4 pasos en orden.

### Paso 0 de TODO agente: "¿DÓNDE ESTÁN LAS COSAS?"
Lee SIEMPRE, en este orden, al arrancar:
1. `docs/PROJECT-MAP.md` → mapa de módulos y quién escribe dónde.
2. `backlog/TODO.md` → qué hay pendiente/en curso/hecho.
3. `docs/DESIGN.md` → la visión que NO puedes romper.
4. (Si eres planificador) `backlog/historia/` + `docs/WORKLOG.md` de ayer.
5. (Si eres ejecutor) `backlog/PLAN-del-dia.md` → tu tarea asignada.
Después, SOLO tocas el módulo de tu tarea, nunca el código entero.

### Paso 1: "¿QUÉ TENGO QUE HACER HOY?"
- Tester/historiadora: leen lo de ayer y generan (ideas / historia).
- Planificador: coge lo `[APROBADO]` del TODO → redacta `PLAN-del-dia.md`
  con tareas concretas, cada una = {módulo, descripción clara, aceptación}.
- Ejecutores: cogen SU tarea del plan (la que les asignó el planificador).
- Revisores: revisan los PR/diff de hoy.

### Paso 2: HACER el trabajo (en tu zona, sin pisar a otros)

### Paso 3: "¿DÓNDE DEJO LO QUE HE HECHO?" — SIEMPRE ESCRÍBIRLO (obligatorio)
Cada agente, al terminar, DEJA SU HUELLA en ubicaciones fijas (ver tabla
en PROJECT-MAP). Las reglas de oro de la escritura:

1. **Marca el estado en `backlog/TODO.md`** SIEMPRE → `[HECHO]` | `[EN CURSO]`
   | `[DESCARTADO]`. Nunca dejes una tarea "en el aire" sin estado.
2. **Actualiza `docs/WORKLOG.md`** (append): qué hice, decidí, y POR QUÉ.
   El "porqué" es tan importante como el "qué" (es el razonamiento del comité).
3. **Actualiza el README del módulo** que tocaste (si cambió su comportamiento).
4. **Deja el entregable en su sitio:** historia → `backlog/historia/<fecha>.md`;
   plan → `backlog/PLAN-del-dia.md`; ADR → `docs/ADR/<fecha>-<tema>.md`.
5. **Commit + push.** El repo es la memoria física del comité.

### Paso 4: el RELEVO (cómo sigue el sistema)
Al terminar tu turno dejas "la pelota" en un sitio concreto para el siguiente:
- **Historiadora →** deja historia en `backlog/historia/` para planificador/ejecutores.
- **Tester →** deja ideas en TODO para que Juanma apruebe y el planificador coja.
- **Planificador →** deja `PLAN-del-dia.md` para que los ejecutores lo lean.
- **Ejecutores →** marcan `[HECHO]` para que los revisores validen ese PR.
- **Revisor filtro →** marca 💥/✅ en el TODO para el revisor de diseño.
- **Revisor diseño →** escribe el reporte final y avisa a Juanma en Telegram.

### La regla que NUNCA se rompe
> **"Ningún agente termina su turno sin haber escrito dónde ha dejado su
> trabajo."** Si un turno no deja huella (estado, entregable o registro),
> el sistema se rompe al día siguiente. Documentar NO es opcional: es parte
> de "tarea terminada". Esto es una regla HARD en cada prompt de cron.

---

## 3.1 Modelos VERIFICADOS (proveedor opencode-go, 100% confirmados)
Listados con `opencode models opencode-go`:
- `opencode-go/deepseek-v4-flash` — tester, ejecutores, revisor filtro, historiadora
- `opencode-go/deepseek-v4-pro` — planificador
- `opencode-go/gpt-5.6-luna` — revisor de diseño
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
  el TODO (marca hecho/descartado) y el WORKLOG (qué y por qué). Documentar es
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

### 07:00 — ☀️ HAVEL la Roca · Tester de ideas · deepseek-v4-flash
- Prueba el juego como jugador: ve qué está mal de lo nuevo de ayer, capturas.
- Anota ideas/bugs en `backlog/TODO.md` como `[PENDIENTE]` (sin ejecutar).
- Trabaja arduamente y un buen rato de testing. "¿Qué tal lo de ayer y qué se nos ocurre?"

### 11:00 — 🌙 GWYNDOLIN, Dark Sun · Planificador · deepseek-v4-pro (caro) ⚠️
- **NO gastar demasiados tokens.** Las ideas le llegan mascadas; él estructura.
- Redacta `backlog/PLAN-del-dia.md`: tareas concretas {módulo, descripción, aceptación}.
- Reparte trabajo entre Ornstein/Smough/Seath para no colisionar.
- Si requiere decisión importante: mensaje urgente a Juanma (Telegram) → ejecutarla
  al día siguiente. Solo casos excepcionales.

### 13:00 — ⚔️ ORNSTEIN · Ejecutor 1 · deepseek-v4-flash
### 16:00 — 🔨 SMOUGH · Ejecutor 2 · deepseek-v4-flash
### 19:00 — 💛 SEATH el Descamado · Ejecutor 3 · deepseek-v4-flash
- Implementan tareas en SU módulo; **conscientes de los otros 2** → no colisionar.
- Verifican su pieza con tests reales. Documentan y marcan `[HECHO]` al terminar.

### 21:00 — 🐺 ARTORIAS del Abismo · Revisor filtro · deepseek-v4-flash
- Se toma su tiempo probando (juego + tests + lint + smoke).
- Marca 💥 / ✅ en `backlog/TODO.md`. Rechaza lo roto con comentario accionable.

### 23:00 — 👑 GWYN, Señor de la Ceniza · Revisor de diseño + MERGE · gpt-5.6-luna
- Revisión profunda: ¿el PR sigue la visión del `DESIGN.md`? (no solo que "compila").
- Modelo distinto al constructor → no se auto-aprueba.
- **Cuidado con tokens; no excedernos.**
- **Es el encargado del MERGE FINAL:** tras ver la revisión de Artorias (21:00),
  da el visto bueno y **mergea** el PR. Luego envía a Juanma un **reporte**.
- Sin gate de humanización obligatorio (rompe ciclo) — reporta y Juanma avisa si ve algo.

### 🔄 Cadena de PRs (decisión confirmada)
1. Ejecutores hacen branch/PR.
2. **Artorias** (21:00) revisa y valida/filtra.
3. **Gwyn** (23:00) revisa en profundidad y, tras ver lo de Artorias, **hace el merge**.
4. Gwyn reporta a Juanma.

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

## 6. Fase 0 — Arranque (primeros 3-4 días) — CRONS DISTINTOS ⚡⚠️
> **IMPORTANTE: la Fase 0 NO usa los crons del bucle diario (sección 4).**
> Son crons temporales/provisionales solo para diseñar. Se eliminan al
> terminar la Fase 0 y se instalan los del bucle diario. El objetivo de la
> Fase 0 es PRODUCIR el `DESIGN.md` + plot, no escribir código del juego.

### Crons de Fase 0 (provisionales)
| Hora | Agente | Modelo | Entrega DÓNDE |
|---|---|---|---|
| (03:00) | **Research stack** | deepseek-v4-flash | `docs/INVESTIGACION-STACK.md` (validar/ampliar Pyxel y arquitectura) |
| (05:00) | **Manus: research skills anti-slop** | deepseek-v4-flash | `docs/SKILLS-ANTISLOP.md` (skills reales para narrativa y niveles del juego) |
| (07:00) | **Research mecánicas + dopamina** | deepseek-v4-flash | `docs/RESEARCH-MECANICAS.md` (aprender sin deberes, bucles dopaminérgicos tipo Balatro) |
| (11:00) | **Diseñador jefe** (caro) | deepseek-v4-pro | `docs/DESIGN.md` (historia, plot, capítulos, niveles, stack, mapa + roguelite) |
| (16:00) | **Arquitectura** | deepseek-v4-pro | `src/<modulo>/README.md` + `ARCHITECTURE.md` + rellenar tabla del PROJECT-MAP |

- El **gate de Juanma** ocurre al final de la Fase 0: él revisa `DESIGN.md`
  y el mapa de módulos, da el visto bueno (o pide cambios).
- Con el OK, se ELIMINAN estos crons provisionales y se instalan los del
  comité diario (sección 4).

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
- [x] Verificar identificadores de modelo (deepseek-v4-pro, deepseek-v4-flash, gpt-5.6-luna — ✅ confirmados via `opencode models`).
- [x] Autenticar `gh` con la cuenta de Juanma (✅ amcgiluma, lista).
- [x] Crear repo público + estructura git + PROJECT-MAP (✅ `amcgiluma/CyberRoot`).
- [x] Decidir el 6º agente historiadora → **Manus**, deepseek-v4-flash, 03:00.
- [ ] Crear `docs/WORKLOG.md` inicial (registro diario del comité).
- [ ] Definir cron de uso del panel de métricas (`opencode stats --days N --models`).
- [ ] Configurar crons de Fase 0 (research/diseño) → DESIGN.md + plot + mapa de módulos.
- [ ] Gate de Juanma al final de Fase 0.
- [ ] Configurar crons del concilio diario (Manus 3, Havel 7, Gwyndolin 11, Ornstein/Smough/Seath 13/16/19, Artorias 21, Gwyn 23+merge) + cadena de PRs.
- [ ] Diseñar roguelite + mecánicas dopaminérgicas en concreto (dentro de Fase 0).

---
*Este documento pasará por humanizer en su versión final dentro del repo.*