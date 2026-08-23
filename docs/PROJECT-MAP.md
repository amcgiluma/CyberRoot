# PROJECT-MAP — Índice maestro / mapa de módulos (CyberRoot)

> ⚠️ **LEE ESTE FICHERO PRIMERO SIEMPRE.** Es la puerta de entrada del sistema.
> Aquí se dice QUÉ existe, DÓNDE está, y qué agente toca qué. Una IA NUNCA
> lee el proyecto entero: lee este mapa + la guía del módulo de su tarea.
> Después de cada tarea, actualiza lo que toque tocar (obligatorio).

---

## 0. Cómo se navega este proyecto (para agentes)
1. **Lee este `PROJECT-MAP.md`** → sabrás qué módulos existen y qué hace cada uno.
2. **Lee `backlog/TODO.md`** → sabrás qué hay pendiente, en curso y hecho.
3. **Lee `docs/DESIGN.md`** → la visión/reglas del juego que nunca debes romper.
4. Localiza tu tarea → **lee SOLO la guía del módulo** (`src/<modulo>/README.md`)
   antes de tocar nada.
5. **NO leas el código entero del repo.** Solo lo necesario para tu tarea.
6. **Al terminar**: documenta (README/WORKLOG/TODO) — "tarea terminada" = hecho + documentado. (WORKLOG vive en `docs/worklog/`, por fechas.)

## 1. Top-level (estado vivo, se actualiza cada día)
```
backlog/            → LA COLA DE TRABAJO. Lo que hay que hacer, lo que se hace.
  TODO.md           → tareas con estado (pendiente/curso/hecho/descartado) ← LEER
  PLAN-del-dia.md   → plan del día redactado por el planificador (11:00)
  historia/         → borradores de la historiadora (03:00) = materia narrativa
docs/               → el conocimiento permanente.
  PROJECT-MAP.md    → ESTE fichero (índice maestro).
  DESIGN.md         → diseño del juego (historia, capítulos, niveles, stack).
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
| **Historiadora** (03:00) | deepseek-v4-flash | `backlog/historia/<fecha>.md` (story). Marca en TODO las piezas narrativas listas. |
| **Tester ideas** (07:00) | deepseek-v4-flash | `backlog/TODO.md` (nuevas ideas, bugs encontrados). Notas en `docs/worklog/` (día actual). |
| **Planificador** (11:00) | deepseek-v4-pro | `backlog/PLAN-del-dia.md` + reparte tareas en `backlog/TODO.md`. |
| **Ejecutores ×3** (13/16/19) | deepseek-v4-flash | Código en `src/<su modulo>/`. Marca hecho en `backlog/TODO.md`. README del módulo. |
| **Revisor filtro** (21:00) | deepseek-v4-flash | Resultado en `backlog/TODO.md` (💥 rechazado / ✅ pasa) + comentario. |
| **Revisor diseño** (23:00) | gpt-5.6-luna | Reporte final en `docs/worklog/` (día actual) / `backlog/TODO.md` + aviso a Juanma. |
| **Juanma** (feedback) | — | Escribe en la libreta (TODO/DESIGN) o me dice a mí. ← EL CONTROL |

## 3. Tabla de módulos
*(Rellena en la Fase 0, cuando la arquitectura se cierre)*
| Módulo | Qué hace | Dónde vive | README/Auth | Quién lo toca |
|---|---|---|---|---|
| *(pendiente de Fase 0)* | | `src/...` | | ejecutor A/B/C |

## 4. Cómo se entera un agente de "qué se ha hecho y qué toca"
1. Lee `backlog/TODO.md` → ve estados `pendiente/curso/hecho/descartado`.
2. Si es el planificador, lee `backlog/historia/` (para nutrir el plan) y el
   `WORKLOG` de ayer (saber qué se hizo) → redacta `PLAN-del-dia.md`.
3. Si es un ejecutor, lee `PLAN-del-dia.md` → coge SU tarea asignada.
4. Al terminar su tarea, SIEMPRE escribe su resultado y marca el estado.
Ese ciclo de "leer algó → hacer → escribir dónde lo he dejado" es lo que
mantiene a todo el sistema sincronizado SIN memoria compartida.

---
*Este índice se mantiene actualizado como parte de "documentar al terminar".*