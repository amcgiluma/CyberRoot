# AGENTS-PLAN — Estructura del sistema de agentes (CyberRoot)

> Fecha: 23/08/2026 · Estado: **definitivo v1.0 (decisiones de Juanma cerradas).**
> Pendiente solo: verificar identificadores de modelo en config y maquetar crons.
> Este documento y todo el sistema fueron diseñados para ser **públicos**: esta
> estructura es de la que "fardamos" en GitHub. Somos lo más transparentes posible.

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

## 4. CRONS DE AGENTES (horario Madrid)

### 07:00 — Cron tester de ideas · DeepSeek V4 Flash (barato)
- Revisa el código, ve lo que hay, **prueba el juego como jugador**.
- Busca qué está mal en lo nuevo del día anterior; toma capturas/progresos.
- Anota ideas generales que NO estén ya apuntadas (en la libreta, sin ejecutar).
- Debe trabajar **arduamente y durante un buen rato de testing**.
- Rol: "¿qué tal lo que se hizo ayer y qué se nos ocurre?"

### 11:00 — Cron planificador · DeepSeek V4 Pro (caro) ⚠️
- **Explicito: NO gastar demasiados tokens.** Es el modelo caro del comité.
- Las ideas le llegan "mascadas": él NO explora; **estructura**.
- Monta un plan ordenado con **código claro y guías explícitas** para que los
  ejecutores no se pierdan. Decide qué hace cada uno y en qué módulo.
- Si necesita tomar una decisión importante, envía a Juanma un **mensaje
  urgente a Telegram** para ejecutarla **al día siguiente**. Solo casos muy
  excepcionales. La idea es que el bucle fluya cuasi-autónomo.

### 13:00 / 16:00 / 19:00 — Cron ejecutores · DeepSeek V4 Flash ×3
- Rápidos, baratos, buenos. Implementan tareas del plan en su módulo.
- **Conscientes de que hay otros ejecutores trabajando**: solo tocan su zona
  (definida por el planificador), para no colisionar en git.
- Verifican su pieza con tests reales (resolver el nivel / test unitario),
  no "compila y ya". Documentan sus cambios al terminar.

### 21:00 — Cron revisor FILTRA · DeepSeek V4 Flash
- Se **toma su tiempo probando cosas** (juego + tests + lint + smoke).
- Rechaza lo roto con comentario accionable. Filtro para no meter mierda.

### 23:00 — Cron revisor de DISEÑO · GPT 5.6 Luna (caro) ⚠️
- Revisión profunda que **el plan sigue la visión** (no solo que "compila").
- Modelo distinto al constructor → no se auto-aprueba.
- **Cuidado con el uso de tokens; no excedernos.**
- **NO hay gate de humanización obligatorio** (rompe el ciclo). En su lugar,
  al terminar envía a Juanma un **reporte**. Si Juanma ve algo mal, le avisa.

### Nota de PRs
Los PR los revisan los agentes 21:00 (filtro) y 23:00 (diseño), en cadena.

### 03:00 — 🔥 6º agente HISTORIADORA · DeepSeek V4 Flash [CONFIRMADO]
- Escribe la HISTORIA del día en base al **plot general definido en la Fase 0**.
- Produce texto narrativo (diálogos, sabor, descripciones) antes de que los
  ejecutores codifiquen, para que tengan materia que integrar.
- Modelo barato; su prosa pasa criterio `humanizer` (regla de ejecutores).

---

## 5. Humanizer (regla + 6º agente de historia)
- **Regla en todos los ejecutores** (ya asentada): la prosa del juego pasar
  criterio del skill `humanizer` para que no suene a AI-slop.
- **[PROPUESTA] 6º agente — historiadora**: un agente que escribe la HISTORIA a
  diario en base al **plot general definido durante los primeros 3-4 días**
  (Fase 0). Así la narrativa florece sin saturar a los ejecutores de código.
  ⚡ Pendiente: Juanma confirma si lo activamos y con qué modelo/hora.

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
| (07:00) | **Research mecánicas** | deepseek-v4-flash | `docs/RESEARCH-MECANICAS.md` (aprender sin deberes, referencias) |
| (11:00) | **Diseñador jefe** (caro) | deepseek-v4-pro | `docs/DESIGN.md` (historia, plot, capítulos, niveles, stack, mapa) |
| (16:00) | **Arquitectura** | deepseek-v4-pro | `src/<modulo>/README.md` + `ARCHITECTURE.md` + rellenar tabla del PROJECT-MAP |

- El **gate de Juanma** ocurre al final de la Fase 0: él revisa `DESIGN.md`
  y el mapa de módulos, da el visto bueno (o pide cambios).
- Con el OK, se ELIMINAN estos crons provisionales y se instalan los del
  comité diario (sección 4).

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
- [ ] Verificar identificadores de modelo (deepseek v4 pro, deepseek v4 flash,
      gpt 5.6 luna) en config OpenCode.
- [ ] Decidir el 6º agente historiadora (Sí/No, modelo, hora).
- [ ] Definir fuente de métricas del panel de uso y su cron.
- [ ] Autenticar `gh` con la cuenta de Juanma (única acción manual suya).
- [ ] Crear repo público + estructura git + PROJECT-MAP.
- [ ] Configurar crons (7/11/13/16/19/21/23) + PRs.
- [ ] Fase 0: lanzar research dirigido por agentes → DESIGN.md + plot.

---
*Este documento pasará por humanizer en su versión final dentro del repo.*