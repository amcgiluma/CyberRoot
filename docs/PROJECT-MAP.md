# PROJECT-MAP — Índice maestro / mapa de módulos (CyberRoot)

> ⚠️ **LEE ESTE FICHERO PRIMERO SIEMPRE.** Es la puerta de entrada del sistema.
> Aquí se dice QUÉ existe, DÓNDE está, y qué agente toca qué. Una IA NUNCA
> lee el proyecto entero: lee este mapa + la guía del módulo de su tarea.
> Después de cada tarea, actualiza lo que toque tocar (obligatorio).

---

## 0. Cómo se navega este proyecto (para agentes)
1. **Lee este `PROJECT-MAP.md`** → sabrás qué módulos existen y qué hace cada uno.
2. **Lee `docs/AGENTES.md`** → sabrás QUÉ hace cada agente del concilio (coordinación).
3. **Lee `backlog/INDICE.md`** y SOLO los ficheros del backlog de tu fila → sabrás qué hay pendiente/en curso/hecho SIN leer el backlog entero.
4. **Lee `docs/DESIGN.md`** → la visión/reglas del juego que nunca debes romper.
5. Localiza tu tarea → **lee SOLO la guía del módulo** (`src/<modulo>/README.md`) antes de tocar nada.
6. **NO leas el código entero del repo.** Solo lo necesario para tu tarea.
7. **Revisa `backlog/mejoras/pendiente/propuestas.md`** → propuestas de auto-mejora que te afecten.
8. **Al terminar**: documenta (README/WORKLOG/tu fichero del backlog) — "tarea terminada" = hecho + documentado. (WORKLOG vive en `docs/worklog/`, por fechas.)
9. **Puedes delegar**: tienes `delegate_task` (sub-agentes baratos, flash). Ver `docs/AGENTES.md` (sección DELEGACIÓN). Usa sub-agentes para tareas extensas y verifica el resultado real.

## 1. Top-level (estado vivo, se actualiza cada día)
```
backlog/            → LA COLA DE TRABAJO, dividida por estado (ver backlog/INDICE.md)
  INDICE.md         → mapa del backlog: qué hay en cada subcarpeta y qué lee cada agente ← LEER
  zona-testeo.md    → la ZONA 🔬 del día: Gwyn la escribe al cierre; Oscar/Havel la leen por la mañana
  notas-manana.md   → notas rodantes para mañana: 🧭 dirección de Oscar + 🎯 revisores
  tareas/
    pendiente/abierto.md     → tareas [PENDIENTE] / [BUG] / ideas abiertas
    en-curso/activo.md       → lo que se ejecuta HOY + veredictos 💥/✅ de Artorias
    hecho/<AAAA-MM>.md       → ARCHIVO POR MES de lo completado (los meses pasados NO se leen)
    descartado/historico.md  → rechazadas con motivo
  mejoras/
    pendiente/propuestas.md  → propuestas de auto-mejora [NUEVA]/[EN REVISIÓN]
    aplicadas/historico.md   → registro [APLICADA] de Gwyn (trazabilidad pública)
  planes/YYYY/MM/DD.md → HISTÓRICO de planes diarios (hoy = fecha actual)
  historia/          → la narrativa de Manus (INDICE, PERSONAJES, ESCENARIOS, CAPITULOS/...)
docs/               → el conocimiento permanente.
  PROJECT-MAP.md    → ESTE fichero (índice maestro).
  AGENTES.md        → roles del concilio: qué hace cada agente (coordinación).
  DESIGN.md         → diseño del juego (historia, capítulos, niveles, stack).
  TESTEO-DIARIO.md  → protocolo de testeo del Concilio: 4 capas (Oscar/Havel/Artorias/Gwyn) + zona 🔬.
  ESTADO-JUGADOR.md → doc vivo de Oscar: qué es jugable HOY + run de referencia desde save limpio.
  worklog/           → registro diario por fechas: index.md + YYYY/MM/DD.md
  ADR/              → decisiones de arquitectura (fecha + motivo) — públicas.
  USAGE.md          → panel de uso/coste de IA diario.
  AGENTS-PLAN.md    → este mismo sistema, documentado públicamente.
src/                → el código del juego (módulos).
  <modulo>/         → cada módulo con su README.md (qué hace) + ARCHITECTURE.md
```

## 2. Cómo se atribuye trabajo (quién escribe DÓNDE)
| Agente (hora) | Modelo | Lee (SOLO esto del backlog) | Escritura/Entregas DÓNDE |
|---|---|---|---|
| **Manus** (03:00) | deepseek-v4-flash | plan de HOY + `en-curso/activo.md` | `backlog/historia/<...>.md` (story, humanizer). Marca sus piezas `[HECHO]` en `en-curso/activo.md`. |
| **Oscar de Astora** (05:00) | deepseek-v4-flash | `zona-testeo.md` + su `ESTADO-JUGADOR.md` | `docs/ESTADO-JUGADOR.md` (run de referencia/veterano) + `[BUG]`/ideas en `tareas/pendiente/abierto.md` + notas de dirección en `notas-manana.md` (🧭). |
| **Havel** (07:00) | deepseek-v4-flash | `zona-testeo.md` + `ESTADO-JUGADOR.md` | bugs `[BUG]` + ideas `[PENDIENTE]` en `tareas/pendiente/abierto.md`. Smoke del conjunto SIN save limpio (esa capa es de Oscar). Worklog del día. |
| **Gwyndolin** (11:00) | deepseek-v4-pro | `pendiente/abierto.md` (entero) + `en-curso/activo.md` + `notas-manana.md` (🎯/🧭 validadas) | plan de HOY en `planes/YYYY/MM/DD.md`; mueve elegidas → `en-curso/activo.md`; descartes con motivo → `descartado/historico.md`. Propone mejoras en `mejoras/pendiente/propuestas.md` (las aplica Gwyn). |
| **Ornstein/Smough/Seath** (13/16/19) | deepseek-v4-flash | SU línea en `en-curso/activo.md` + plan de HOY | Código en su RAMA `feat/<modulo>` + PR a main. Marcan `[HECHO]` (+PR) junto a su línea en `en-curso/activo.md`. README del módulo. Ornstein: + harness. |
| **Artorias** (21:00) | deepseek-v4-flash | `en-curso/activo.md` + `[BUG]` de `pendiente/abierto.md` | 💥/✅ junto a cada línea en `en-curso/activo.md`; aviso + gusto en `notas-manana.md` (🎯); ideas nuevas → `pendiente/abierto.md`. |
| **Gwyn** (23:00) | gpt-5.6-luna | `en-curso/activo.md` + `notas-manana.md` (🧭/🎯) + `mejoras/pendiente/propuestas.md` | MERGE final (solo él); tras merge MUEVE las líneas `[HECHO]` → `hecho/<AAAA-MM>.md`; rechazos documentados junto a la línea; SOBRESCRIBE `zona-testeo.md`; notas en `notas-manana.md` (🎯); aplica auto-mejora (`hermes cron edit`) y registra `[APLICADA]` en `mejoras/aplicadas/historico.md`. |
| **Juanma** (feedback) | — | — | Escribe en la libreta (INDICE/DESIGN) o me dice a mí. ← EL CONTROL |

## 3. Tabla de módulos
*(Rellena cuando la arquitectura se cierre)*
| Módulo | Qué hace | Dónde vive | README/Auth | Quién lo toca |
|---|---|---|---|---|
| *(pendiente de arquitectura)* | | `src/...` | | ejecutor A/B/C |

## 4. Cómo se entera un agente de "qué se ha hecho y qué toca"
1. Abre SU fila de la tabla §2 (o `backlog/INDICE.md` si duda) → lee SOLO esos ficheros.
2. Si es el planificador, además `backlog/historia/` (para nutrir el plan con la historia) y el WORKLOG de ayer → redacta `backlog/planes/YYYY/MM/DD.md` (HOY).
3. Si es un ejecutor, lee el plan de HOY + SU línea en `en-curso/activo.md`.
4. Al terminar, SIEMPRE escribe su resultado y deja el estado donde marca la tabla.
Ese ciclo de "leer algo → hacer → escribir dónde lo he dejado" es lo que mantiene a todo el sistema sincronizado SIN memoria compartida.

---
*Este índice se mantiene actualizado como parte de "documentar al terminar".*
