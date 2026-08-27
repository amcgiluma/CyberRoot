# CyberRoot

> **Un juego de hacking construido por un Concilio de IAs autónomas.**
> RPG de terminal cyberpunk que enseña Linux y seguridad (Blue/Red Team)
> de forma orgánica y divertida — sin que se sienta como deberes.

Desarrollado de forma 100% autónoma por un comité de agentes de inteligencia
artificial que se organiza, se planifica, se critica, se corrige y mejora él
mismo día a día. El humano decide el "qué" (dirección y gusto); el Concilio
ejecuta el "cómo".

---

## 🧙 EL CONCILIO

Nueve agentes inspirados en Dark Souls coordinan el desarrollo del juego.
Cada uno firma su trabajo con su nombre.

| Avatar | Agente | Hora | Rol | Modelo |
|--------|--------|------|-----|--------|
| 🖤 | **Manus, Padre del Abismo** | 03:00 | Historiador — escribe la historia del día | glm-5.3-flash |
| ⭐ | **Oscar de Astora** | 05:00 | Guardián de la experiencia — juega como jugador (run desde cero + veterano), vigila el `ESTADO-JUGADOR.md` y propone dirección a Gwyn | glm-5.3-flash |
| ☀️ | **Havel la Roca** | 07:00 | Vidente-creativo — juega e idea | glm-5.3-flash |
| 🌙 | **Gwyndolin, Dark Sun** | 11:00 | Planificador — organiza el día | glm-5.3-flash |
| ⚔️ | **Ornstein** | 13:00 | Ejecutor 1 — implementa su módulo | glm-5.3-flash |
| 🔨 | **Smough** | 16:00 | Ejecutor 2 — implementa su módulo | glm-5.3-flash |
| 💛 | **Seath el Descamado** | 19:00 | Ejecutor 3 — implementa su módulo | glm-5.3-flash |
| 🐺 | **Artorias del Abismo** | 21:00 | Revisor filtro — valida e idea | glm-5.3-flash |
| 👑 | **Gwyn, Señor de la Ceniza** | 23:00 | Revisor de diseño + **MERGE final** | glm-5.3-flash |

> 🔥 **Mapa visual interactivo del Concilio**: retratos, flujo del día y mapa del
> reino en 3 niveles de detalle →
> **[amcgiluma.github.io/CyberRoot/mapa](https://amcgiluma.github.io/CyberRoot/mapa/)**
> (fuente: [`docs/mapa/`](docs/mapa/))

---

## 🔄 EL FLUJO DIARIO

```
Oscar de Astora (05:00) juega la EXPERIENCIA (run desde cero + veterano)
   │  estado global → docs/ESTADO-JUGADOR.md + dirección → backlog/notas-manana.md (🧭, para Gwyn)
Havel (07:00) juega e idea
   │  ideas + bugs → backlog/tareas/pendiente/abierto.md
Gwyndolin (11:00) planifica (autónomo, sin aprobación humana)
   │  plan → backlog/planes/YYYY/MM/DD.md (por fecha)
Ornstein / Smough / Seath implementan (13/16/19h)
   │  cada uno en su RAMA feat/<módulo> → abre PR a main
Artorias (21:00) revisa técnicamente y deja notas de gusto
   │  💥/✅ + qué no mergear + ideas
Gwyn (23:00) revisa diseño, hace el MERGE final y decide la zona 🔬 de mañana
   │  si NO mergea: deja por qué + cómo arreglarlo
   │  relevo del testeo: Gwyn → Oscar (05:00) → Havel (07:00)
Manus (03:00) escribe la historia mientras el ciclo se repite
```

- **Flujo 100% autónomo**: las ideas fluyen de Havel a Gwyndolin sin aprobación
  humana. Juanma interviene solo de forma excepcional.
- **Solo Gwyn mergea** a `main`. Las ramas rechazadas se mantienen vivas y Gwyn
  deja documentado `por qué` no se mergeó y `cómo` arreglarla.
- **Notas de gusto para mañana**: Artorias y Gwyn dejan el criterio de juego
  (qué mola, qué no) que Gwyndolin usa para planificar el día siguiente.

---

## 🗂 LA LIBRETA (cómo se comunica el Concilio)

Cada agente arranca sin memoria; la **libreta en el repo es la fuente de verdad**:

```
docs/PROJECT-MAP.md    → índice maestro y mapa de módulos
docs/AGENTES.md        → roles del Concilio (todos saben qué hace cada uno)
docs/DESIGN.md         → el diseño del juego (vivo)
docs/ADR/              → decisiones de arquitectura (públicas)
docs/TESTEO-DIARIO.md  → protocolo de testeo: 4 capas (Oscar/Havel/Artorias/Gwyn) que no se pisan
docs/ESTADO-JUGADOR.md → qué es jugable HOY de principio a fin + run de referencia (lo mantiene Oscar)
backlog/INDICE.md      → mapa del backlog: qué fichero lee/escribe cada agente
backlog/tareas/        → tareas por estado: pendiente/abierto (con prioridad [P0]-[P3]) · en-curso/activo · hecho/<AAAA-MM> (archivo mensual) · descartado
backlog/zona-testeo.md → la zona 🔬 de testeo del día (la decide Gwyn al cierre)
backlog/notas-manana.md→ notas rodantes para mañana (dirección de Oscar + revisores)
backlog/mejoras/       → auto-mejora: pendiente/propuestas · aplicadas/historico
backlog/planes/YYYY/MM/DD.md → el plan de cada día (histórico por fecha)
backlog/historia/      → la narrativa de Manus (índice, personajes, escenarios, fragmentos, capítulos)
docs/worklog/YYYY/MM/DD.md → registro diario por fechas
src/core/ARCHITECTURE.md   → normativa de la frontera core/render (leer ANTES de programar)
```

Regla de oro: *ningún agente termina su turno sin haber escrito dónde ha dejado
su trabajo.* Y **nadie relee el proyecto entero**: cada uno lee la libreta y la
guía de su módulo.

## ♻️ AUTO-MEJORA

El Concilio puede mejorarse a sí mismo: si un agente ve que su tarea no se puede
hacer bien o que el flujo no funciona, propone un cambio en
`backlog/mejoras/pendiente/propuestas.md`.
Lo revisa y **aplica Gwyn** (el revisor final, 23:00), con el humano supervisando.
Los horarios y la cadena de merge no se alteran sin permiso.

---

## 📐 FASE 0 — Investigación y diseño (primera semana)

La Fase 0 es la construcción del plano antes de escribir código del juego:

| Día | Trabajo |
|-----|---------|
| Día 1 | Research: stack técnico, mecánicas/dopamina, skills anti-slop |
| Día 2-3 | Diseño en **5 pasadas** (concepto/historia → roguelite → capítulos → dopamina → revisión) |
| Día 4 | Arquitectura de módulos + coordinador de cierre + **gate de Juanma** |

La Fase 0 usa el modelo **`opencode-go/ox-alpha-free`** (potente y gratis ~1 semana).

---

## Estado actual
- **Fase:** 0 **finalizada** ✅ → **Fase 1 (el Concilio) ACTIVADA el 26/08 23:25**.
- **Gate:** aprobado por Juanma ("OK ACTIVA EL CONCILIO").
- **El Concilio (9 agentes) corre solo desde el 27/08** (Manus 03:00 → ... → Gwyn 23:00),
  construyendo el juego día a día.
- **Última actualización:** 26/08/2026

## Cómo se construye
1. **Fase 0** (✅ breve): los agentes investigan y diseñan el juego → `docs/DESIGN.md`.
2. **Gate de Juanma**: revisa el diseño y da el visto bueno.
3. **Fase 1+ (el Concilio)**: los 9 agentes construyen el juego día a día hasta que esté terminado.

## 🎮 Jugar en web (próximamente)
El objetivo es que el juego esté **jugable siempre en el navegador**, no solo con
pull + local. Cuando exista el primer build (Fase 1), se desplegará a **Vercel**
(tarea P1 de máx. prioridad, acceso ya verificado; fallback: GitHub Pages), y el
enlace se añadirá aquí.

> ⚠️ **Regla para el agente/Concilio que haga el deploy:** en cuanto haya un enlace
> de juego en web publicado, **ACTUALIZA ESTA SECCIÓN** con el enlace y la fecha.
> Hasta entonces, mantenla como "próximamente".

---
*Desarrollado por un comité de IAs autónomo y transparente. El proceso es la feature.*
