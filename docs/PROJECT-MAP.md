# PROJECT-MAP — Índice maestro / mapa de módulos (CyberRoot)

> ⚠️ **LEE ESTE FICHERO PRIMERO SIEMPRE.** Es la puerta de entrada del sistema.
> Aquí se dice QUÉ existe, DÓNDE está, y qué agente toca qué. Una IA NUNCA
> lee el proyecto entero: lee este mapa + la guía del módulo de su tarea.
> Después de cada tarea, actualiza lo que toque tocar (obligatorio).

---

## 0. Cómo se navega este proyecto (para agentes)
1. **Lee este `PROJECT-MAP.md`** → sabrás qué módulos existen y qué hace cada uno.
2. **Lee `docs/AGENTES.md`** → sabrás QUÉ hace cada agente del concilio (coordinación).
3. **Lee `backlog/TODO.md`** → sabrás qué hay pendiente, en curso y hecho.
4. **Lee `docs/DESIGN.md`** → la visión/reglas del juego que nunca debes romper.
5. Localiza tu tarea → **lee SOLO la guía del módulo** (`src/<modulo>/README.md`)
   antes de tocar nada.
6. **NO leas el código entero del repo.** Solo lo necesario para tu tarea.
7. **Revisa `backlog/MEJORAS.md`** → propuestas de auto-mejora que te afecten.
8. **Al terminar**: documenta (README/WORKLOG/TODO) — "tarea terminada" = hecho + documentado. (WORKLOG vive en `docs/worklog/`, por fechas.)
9. **Puedes delegar**: tienes `delegate_task` (sub-agentes baratos, flash). Ver `docs/AGENTES.md` (sección DELEGACIÓN). Usa sub-agentes para tareas extensas y verifica el resultado real.

## 1. Top-level (estado vivo, se actualiza cada día)
```
backlog/            → LA COLA DE TRABAJO. Lo que hay que hacer, lo que se hace.
  TODO.md           → tareas con estado (pendiente/curso/hecho/descartado) ← LEER
  planes/           → HISTÓRICO de planes diarios: planes/YYYY/MM/DD.md (hoy = fecha actual)
  historia/         → la narrativa de Manus (INDICE, PERSONAJES, ESCENARIOS, CAPITULOS/...)
docs/               → el conocimiento permanente.
  PROJECT-MAP.md    → ESTE fichero (índice maestro).
  AGENTES.md        → roles del concilio: qué hace cada agente (coordinación).
  DESIGN.md         → diseño del juego (historia, capítulos, niveles, stack).
  TESTEO-DIARIO.md  → protocolo de testeo del Concilio: capa de Havel/Artorias/Gwyn + zona 🔬.
  worklog/           → registro diario por fechas: index.md + YYYY/MM/DD.md
  ADR/              → decisiones de arquitectura (fecha + motivo) — públicas.
  USAGE.md          → panel de uso/coste de IA diario.
  AGENTS-PLAN.md    → este mismo sistema, documentado públicamente.
src/                → el código del juego (módulos).
  <modulo>/         → cada módulo con su README.md (qué hace) + ARCHITECTURE.md
```

## 2. Cómo se atribuye trabajo (quién escribe DÓNDE)
| Agente (hora) | Modelo | Escritura/Entregas DÓNDE (obligatorio) |
|---|---|---|
| **Manus** (03:00) | deepseek-v4-flash | `backlog/historia/<fecha>.md` (story, humanizer). Marca en TODO las piezas narrativas listas. |
| **Oscar de Astora** (05:00) | deepseek-v4-flash | `docs/ESTADO-JUGADOR.md` (estado global jugable / run de referencia desde save limpio / progreso de veterano) + NOTAS DE DIRECCIÓN en `backlog/TODO.md` para Gwyn (no decide, informa). |
| **Havel** (07:00) | deepseek-v4-flash | `backlog/TODO.md` (bugs + ideas NUEVAS de capítulos/mecánicas/comandos, `[PENDIENTE]`). Notas en `docs/worklog/` (día actual). |
| **Gwyndolin** (11:00) | deepseek-v4-pro | `backlog/planes/YYYY/MM/DD.md` (HOY) + reparte tareas en `backlog/TODO.md`. Propone mejoras en MEJORAS (las aplica Gwyn). |
| **Ornstein/Smough/Seath** (13/16/19) | deepseek-v4-flash | Código en su RAMA `feat/<modulo>` + PR a main. Marca `[HECHO]` en `backlog/TODO.md`. README del módulo. Ornstein: + harness de playtest. |
| **Artorias** (21:00) | deepseek-v4-flash | 💥/✅ de las ramas/PRs + NOTAS DE GUSTO + "qué no mergear" + ideas, en `backlog/TODO.md`. |
| **Gwyn** (23:00) | gpt-5.6-luna | VALIDA diseño + MERGE final (solo él). Si no mergea: por qué + cómo arreglar en `backlog/TODO.md`. + sus notas de gusto + reporte a Juanma. APLICA la auto-mejora (via `hermes cron edit`, registra `[APLICADA]` en MEJORAS). |
| **Juanma** (feedback) | — | Escribe en la libreta (TODO/DESIGN) o me dice a mí. ← EL CONTROL |

## 3. Tabla de módulos
*(Rellena en la Fase 0, cuando la arquitectura se cierre)*
| Módulo | Qué hace | Dónde vive | README/Auth | Quién lo toca |
|---|---|---|---|---|
| *(pendiente de Fase 0)* | | `src/...` | | ejecutor A/B/C |

## 4. Cómo se entera un agente de "qué se ha hecho y qué toca"
1. Lee `backlog/TODO.md` → ve estados `pendiente/curso/hecho/descartado`.
2. Si es el planificador, lee `backlog/historia/` (para nutrir el plan con la
   historia) y el `WORKLOG` de ayer (saber qué se hizo) → redacta
   `backlog/planes/YYYY/MM/DD.md` (HOY).
3. Si es un ejecutor, lee `backlog/planes/YYYY/MM/DD.md` (HOY) → coge SU tarea.
4. Al terminar su tarea, SIEMPRE escribe su resultado y marca el estado.
Ese ciclo de "leer algo → hacer → escribir dónde lo he dejado" es lo que
mantiene a todo el sistema sincronizado SIN memoria compartida.

---
*Este índice se mantiene actualizado como parte de "documentar al terminar".*