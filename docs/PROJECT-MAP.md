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
src/                → el código del juego (módulos). Mapa completo: §3 abajo.
  core/             → lógica pura headless: common, sandbox, curriculum,
                      generator, engine, state, progression, karma
                      (detalle: src/core/ARCHITECTURE.md)
  render/           → capa delgada de Pyxel (dibuja estado, traduce input)
  assets/ data/ tests/ → arte binario · contenido JSON · pytest headless
tools/              → utilidades raíz: cyberroot_usage.py · harness/ (Ornstein)
```

## 2. Cómo se atribuye trabajo (quién escribe DÓNDE)
| Agente (hora) | Modelo | Lee (SOLO esto del backlog) | Escritura/Entregas DÓNDE |
|---|---|---|---|
| **Manus** (03:00) | deepseek-v4-flash | plan de HOY + `en-curso/activo.md` | `backlog/historia/<...>.md` (story, humanizer). Marca sus piezas `[HECHO]` en `en-curso/activo.md`. |
| **Oscar de Astora** (05:00) | deepseek-v4-flash | `zona-testeo.md` + su `ESTADO-JUGADOR.md` | `docs/ESTADO-JUGADOR.md` (run de referencia/veterano) + `[BUG]`/ideas en `tareas/pendiente/abierto.md` + notas de dirección en `notas-manana.md` (🧭). |
| **Havel** (07:00) | deepseek-v4-flash | `zona-testeo.md` + `ESTADO-JUGADOR.md` | bugs `[BUG]` + ideas `[PENDIENTE]` en `tareas/pendiente/abierto.md`. Smoke del conjunto SIN save limpio (esa capa es de Oscar). Worklog del día. |
| **Gwyndolin** (11:00) | glm-5.3-flash | `pendiente/abierto.md` (entero) + `en-curso/activo.md` + `notas-manana.md` (🎯/🧭 validadas) | plan de HOY en `planes/YYYY/MM/DD.md`; mueve elegidas → `en-curso/activo.md`; descartes con motivo → `descartado/historico.md`. Propone mejoras en `mejoras/pendiente/propuestas.md` (las aplica Gwyn). |
| **Ornstein/Smough/Seath** (13/16/19) | deepseek-v4-flash | SU línea en `en-curso/activo.md` + plan de HOY | Código en su RAMA `feat/<modulo>` + PR a main. Marcan `[HECHO]` (+PR) junto a su línea en `en-curso/activo.md`. README del módulo. Ornstein: + harness. |
| **Artorias** (21:00) | deepseek-v4-flash | `en-curso/activo.md` + `[BUG]` de `pendiente/abierto.md` | 💥/✅ junto a cada línea en `en-curso/activo.md`; aviso + gusto en `notas-manana.md` (🎯); ideas nuevas → `pendiente/abierto.md`. |
| **Gwyn** (23:00) | glm-5.3-flash | `en-curso/activo.md` + `notas-manana.md` (🧭/🎯) + `mejoras/pendiente/propuestas.md` | MERGE final (solo él); tras merge MUEVE las líneas `[HECHO]` → `hecho/<AAAA-MM>.md`; rechazos documentados junto a la línea; SOBRESCRIBE `zona-testeo.md`; notas en `notas-manana.md` (🎯); aplica auto-mejora (`hermes cron edit`) y registra `[APLICADA]` en `mejoras/aplicadas/historico.md`. |
| **Juanma** (feedback) | — | — | Escribe en la libreta (INDICE/DESIGN) o me dice a mí. ← EL CONTROL |

## 3. Tabla de módulos
*(Cerrada por el Arquitecto el 26/08 — Fase 0. Detalle operativo por paquete:
`src/core/ARCHITECTURE.md` + `README.md` de cada módulo. ADR:
`docs/ADR/ADR-0001-arquitectura-core-render.md`.)*

### 3.1 Código (`src/` — una rama = un dueño = rutas disjuntas)

| Módulo | Qué hace | Dónde vive | README/Auth | Quién lo toca (rama) |
|---|---|---|---|---|
| **common** | RNG seedeada, bus de eventos, tipos base | `src/core/common/` | `src/core/ARCHITECTURE.md` §2.1 | Ornstein (`feat/engine`) |
| **sandbox** | FS virtual + shell: semántica real de comandos Linux, ruido por acción | `src/core/sandbox/` | su `README.md` | Smough (`feat/sandbox`) |
| **curriculum** | DAG único de conceptos (~60 boons/8 familias); pools y prerrequisitos | `src/core/curriculum/` + `src/data/curriculum.json` | su `README.md` | Smough (`feat/sandbox`) |
| **generator** | Generación procedural ENSEÑANTE determinista por seed; validación canónica §6.4.4 | `src/core/generator/` | su `README.md` | Ornstein (`feat/engine`) |
| **engine** | Motor roguelite: run, salas, detección, DATOS×COMBO, post-mortem | `src/core/engine/` | su `README.md` | Ornstein (`feat/engine`) |
| **state** | GameState serializable JSON ida-y-vuelta + saves versionados | `src/core/state/` | su `README.md` | Seath (`feat/meta-ui`) |
| **progression** | Espejo de Gris, unlocks POR COMPETENCIA, economía, récords | `src/core/progression/` | su `README.md` | Seath (`feat/meta-ui`) |
| **karma** | Contabilidad Blue/Red: N=8, bandas, condiciones de finales | `src/core/karma/` | su `README.md` | Seath (`feat/meta-ui`) |
| **render** | Capa delgada Pyxel: dibuja estado, traduce input→comandos. Cero lógica. ÚNICO importador de pyxel | `src/render/` | su `README.md` | Seath (`feat/meta-ui`) |
| **assets** | Fuente bitmap 5×7 (riesgo nº 1 del stack), paleta CRT, sprites, sfx | `src/assets/` | su `README.md` | Seath (`feat/meta-ui`) |
| **data** | Contenido JSON: currículo, campañas, catálogos, textos ⚠️ v1 calibrables | `src/data/` (reparto por fichero en su README) | su `README.md` | dueño por fila; textos los integra el ejecutor desde `backlog/historia/` |
| **tests** | pytest headless + frontera arquitectónica (`tests/architecture/` no se toca sin propuesta) | `src/tests/` | su `README.md` | cada dueño en SU carpeta |
| **harness** | Playtest autónomo: miles de seeds, métricas de balance/contraste kármico §8.6 | `tools/harness/` (fuera de src — `run_seeds.py` v0 creado el 29/08 por O2) | v0 runner de seeds (Ornstein) | Ornstein (`feat/engine`) |

**Orden de arranque sugerido para Fase 1** (respeta el grafo de dependencias
de `core/ARCHITECTURE.md`): common → sandbox+curriculum (Smough) ∥ generator+
engine (Ornstein, contra stubs de sandbox) ∥ state+progression+karma (Seath,
contra contratos). Render al final de la primera semana: primero fuente bitmap
validada.

### 3.2 Trabajo por agente (`backlog/` — estructura vigente, NO reinventar)

| Agente | Su espacio de trabajo | Escribe también en |
|---|---|---|
| Manus (03:00) | `backlog/historia/` (INDICE, PERSONAJES, ESCENARIOS, FRAGMENTOS, CAPITULOS/) — materializado hoy según AGENTS-PLAN §6.1 | `[HECHO]` en `tareas/en-curso/activo.md`; sus textos entran al juego vía ejecutor integrador → `src/data/story/` |
| Oscar (05:00) | `docs/ESTADO-JUGADOR.md` (su doc vivo) | `tareas/pendiente/abierto.md` [BUG]/ideas · `notas-manana.md` 🧭 |
| Havel (07:00) | — (lee zona-testeo + ESTADO-JUGADOR; no tiene carpeta propia: sus entregas son tareas e ideas) | `tareas/pendiente/abierto.md` |
| Gwyndolin (11:00) | `backlog/planes/YYYY/MM/DD.md` | mueve tareas → `tareas/en-curso/activo.md`; descartes → `tareas/descartado/historico.md`; propone mejoras → `mejoras/pendiente/propuestas.md` |
| Ornstein (13:00) | `feat/engine`: `src/core/{generator,engine,common}/`, `tools/harness/` | código+PR · `[HECHO]` en activo.md · READMEs que toque |
| Smough (16:00) | `feat/sandbox`: `src/core/{sandbox,curriculum}/` (+ retos de `data/chapters/`) | ídem |
| Seath (19:00) | `feat/meta-ui`: `src/core/{state,progression,karma}/`, `src/render/`, `src/assets/` | ídem |
| Artorias (21:00) | — (veredictos 💥/✅ sobre el trabajo de otros) | `activo.md` + `notas-manana.md` 🎯 |
| Gwyn (23:00) | `zona-testeo.md` (sobrescribe), merges, archivo mensual | `tareas/hecho/<mes>.md` · `mejoras/aplicadas/historico.md` |

Regla anti-colisión transversal: **una tarea = un dueño = una rama = rutas
disjuntas.** Si tu tarea exige tocar rutas de otro, se abre en
`tareas/pendiente/abierto.md` y la ejecuta el dueño.

## 4. Cómo se entera un agente de "qué se ha hecho y qué toca"
1. Abre SU fila de la tabla §2 (o `backlog/INDICE.md` si duda) → lee SOLO esos ficheros.
2. Si es el planificador, además `backlog/historia/` (para nutrir el plan con la historia) y el WORKLOG de ayer → redacta `backlog/planes/YYYY/MM/DD.md` (HOY).
3. Si es un ejecutor, lee el plan de HOY + SU línea en `en-curso/activo.md`.
4. Al terminar, SIEMPRE escribe su resultado y deja el estado donde marca la tabla.
Ese ciclo de "leer algo → hacer → escribir dónde lo he dejado" es lo que mantiene a todo el sistema sincronizado SIN memoria compartida.

---
*Este índice se mantiene actualizado como parte de "documentar al terminar".*
