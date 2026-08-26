# BACKLOG — Índice (CyberRoot)

> 🗺️ **La cola de trabajo, dividida para no leerse entera.** Regla de oro:
> cada agente abre SOLO los ficheros de su fila. (Antes todo vivía en un único
> `TODO.md` y un `MEJORAS.md`; se dividió el 26/08 para que ningún fichero
> crezca sin límite y cada turno lea solo su subconjunto.)

## Mapa

```
backlog/
  INDICE.md                    ← ESTE mapa (corto; léelo una vez)
  zona-testeo.md               ← la zona 🔬 del día (la escribe Gwyn al cierre; ≤6 líneas)
  notas-manana.md              ← notas para el día siguiente (dirección de Oscar + revisores)
  tmp-reintentos.md            ← contador de reintentos del Vigilante Fase 0
  tareas/
    pendiente/abierto.md       ← tareas [PENDIENTE] + [BUG] + ideas abiertas
    en-curso/activo.md         ← lo que se ejecuta HOY y sus veredictos 💥/✅
    hecho/<AAAA-MM>.md         ← ARCHIVO POR MES de lo completado (los meses pasados NO se leen)
    descartado/historico.md    ← rechazadas, con motivo
  mejoras/
    pendiente/propuestas.md    ← propuestas de auto-mejora [NUEVA]/[EN REVISIÓN]
    aplicadas/historico.md     ← registro [APLICADA] de Gwyn (trazabilidad pública en GitHub)
  planes/YYYY/MM/DD.md         ← el plan de cada día (histórico por fecha)
  historia/                    ← la narrativa de Manus (INDICE, PERSONAJES,
                                 ESCENARIOS, FRAGMENTOS, CAPITULOS/) —
                                 materializada el 26/08 según AGENTS-PLAN §6.1
```

> Estructura de trabajo POR AGENTE y tabla de dueños de módulos/ramas:
> **`docs/PROJECT-MAP.md` §3** (cerrada por el Arquitecto el 26/08).

## Estados (prefijo SIEMPRE en mayúscula)

- `[PENDIENTE]` …abierta y lista para planificar. Las ideas de Havel/Oscar entran aquí y el planificador las coge SIN aprobación humana.
- `[BUG]` …fallo detectado: síntoma + pasos mínimos para reproducir.
- `[EN CURSO]` …un agente está trabajando en ello YA.
- `[HECHO]` …implementada Y documentada. Solo entonces se archiva.
- `[DESCARTADO]` …rechazada con motivo (Juanma o curación). No retomar salvo petición expresa.

## Prioridades (segundo prefijo, SIEMPRE en pendiente)

- `[P0]` — máxima/urgente: desbloquea lo crítico o lo que Juanma marca como máxima. Gwyndolin la respeta SIEMPRE por encima de su criterio.
- `[P1]` — alta: importante; entra antes que lo interesante.
- `[P2]` — media: vale pero puede esperar; Gwyndolin usa su juicio de valor.
- `[P3]` — baja/incubando: idea interesante que no compromete nada a corto plazo.

> La prioridad **NO anula** la curación de Gwyndolin: la guía. Respeta `[P0]`/`[P1]`
> por encima de su criterio; en `[P2]`/`[P3]` usa su juicio de valor. Mantener las
> prioridades al día (revalorar las que se quedaron obsoletas) es parte de su
> **HIGIENE GENERAL** del backlog.

Formato de línea: `- [ESTADO][PRIORIDAD] (fecha) Título — quién: detalle.` Añade `↩ respuesta` cuando alguien decida sobre ella.

## Qué lee y qué escribe cada agente (SOLO esto)

| Agente (hora) | LEE | ESCRIBE |
|---|---|---|
| **Manus** (03:00) | plan de HOY + su `historia/` | texto en `historia/CAPITULOS/`; marca sus piezas `[HECHO]` en `tareas/en-curso/activo.md` |
| **Oscar** (05:00) | `zona-testeo.md` + `docs/ESTADO-JUGADOR.md` | `[BUG]`/ideas → `tareas/pendiente/abierto.md`; notas de dirección → `notas-manana.md` (sección 🧭) |
| **Havel** (07:00) | `zona-testeo.md` + `docs/ESTADO-JUGADOR.md` | `[BUG]` + ideas `[PENDIENTE]` → `tareas/pendiente/abierto.md` |
| **Gwyndolin** (11:00) | `tareas/pendiente/abierto.md` (entero) + `tareas/en-curso/activo.md` + `notas-manana.md` (🎯) | el plan de HOY en `planes/`; mueve las elegidas → `tareas/en-curso/activo.md`; descartes con motivo → `tareas/descartado/historico.md` |
| **Ejecutores** (13/16/19) | SU tarea en `tareas/en-curso/activo.md` + plan de HOY | código/PR; marcan `[HECHO]` (+ nº PR) junto a su línea en `tareas/en-curso/activo.md` |
| **Artorias** (21:00) | `tareas/en-curso/activo.md` + los `[BUG]` de `tareas/pendiente/abierto.md` | 💥/✅ junto a cada línea en `tareas/en-curso/activo.md`; aviso + gusto → `notas-manana.md` (🎯); ideas → `tareas/pendiente/abierto.md` |
| **Gwyn** (23:00) | `tareas/en-curso/activo.md` + `notas-manana.md` (🧭 y 🎯) + `mejoras/pendiente/propuestas.md` | tras merge: mueve las líneas `[HECHO]` → `tareas/hecho/<AAAA-MM>.md`; SOBRESCRIBE `zona-testeo.md`; notas → `notas-manana.md`; aplica mejoras y registra en `mejoras/aplicadas/historico.md` |

## Ciclo de vida de una tarea

idea/bug → `tareas/pendiente/abierto.md` → Gwyndolin la elige y la mueve → `tareas/en-curso/activo.md` → el ejecutor la implementa (`[HECHO]` + PR) → Artorias 💥/✅ → Gwyn mergea → la línea pasa al `tareas/hecho/<AAAA-MM>.md` del mes. Cada mes se abre fichero nuevo en `hecho/`; los antiguos quedan sellados.

## Reglas

1. Al terminar SIEMPRE deja tu huella donde marca la tabla (+ worklog del día). Es regla HARD (AGENTS-PLAN §2.5).
2. `hecho/` crece POR MES: no alargues un fichero eterno.
3. Mejoras del sistema → `mejoras/pendiente/propuestas.md`; las aplica Gwyn con `hermes cron edit` (NUNCA edites `jobs.json` a mano).
4. Este índice forma parte de "documentar al terminar": si cambias la estructura, actualízalo.
