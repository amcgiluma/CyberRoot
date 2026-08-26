# WORKLOG — Registro diario del Concilio (CyberRoot)

> 📖 **QUÉ ES:** la bitácora del proyecto. Cada agente deja constancia de
> *qué hizo, qué decidió y por qué* durante su turno. Es el "razonamiento"
> del sistema, complementario al estado de tareas (`backlog/tareas/…`, mapa en
> `backlog/INDICE.md`).
>
> 🗒️ **NOTA (desde el 26/08):** los antiguos `backlog/TODO.md` y
> `backlog/MEJORAS.md` se dividieron en carpetas por estado (`tareas/`,
> `mejoras/`, más `zona-testeo.md` y `notas-manana.md`). Las entradas de días
> anteriores mencionan esas rutas viejas como registro histórico fiel: la
> equivalencia está en `backlog/INDICE.md`.
>
> **¿Por qué carpetas por fechas?** Para que el registro ESCALE. Un único
> archivo se volvería kilométrico; aquí cada día vive en su propio fichero y
> cualquier agente encuentra "lo de ayer" sin esforzarse. Se organiza como
> Git organiza sus reflogs: la jerarquía es la escala.

---

## 📁 Organización (por fechas, jerárquica)

```
docs/worklog/
  index.md            ← ESTE fichero: reglas + índice de días
  YYYY/
    MM/
      DD.md           ← una entrada por día
```

- Un **archivo por día**. Dentro, una **subsección por agente/turno**.
- Ejemplo: `docs/worklog/2026/08/23.md` contiene las entradas de ese día.
- Para "ver qué pasó ayer": abrir el archivo del día anterior. Simple.

## 🗂 Índice de días

| Día | Archivo | Principales decisiones / avances |
|---|---|---|
| 2026-08-26 | `2026/08/26.md` | P5 cierra el diseño (DESIGN.md ✅) + protocolo de testeo diario con 4 perfiles (Oscar integrado; relevo Gwyn→Oscar→Havel). Corrector: coherencia a 9 agentes en docs/prompts. Reestructurador: **backlog dividido en carpetas por estado** (`tareas/`, `mejoras/`, `zona-testeo.md`, `notas-manana.md`, `INDICE.md`), 12 prompts actualizados vía CLI, docs + GitHub Page cuadrados. |
| 2026-08-23 | `2026/08/23.md` | Fundación completa: proyecto (roguelite Hades + dopamina Balatro), **Concilio Dark Souls** (8 agentes+roles), repo público `amcgiluma/CyberRoot`, libreta (PROJECT-MAP/AGENTES/TODO/MEJORAS/worklog por fechas), **Fase 0** (10 one-shot en `ox-alpha-free`, research+diseño 5 pasadas+arquitectura), flujo de ramas con merge de Gwyn, auto-mejora, delegación en sub-agentes (flash) y skills de proyecto, planes por fecha `backlog/planes/`, estructura de carpetas por agente. Crons configurados. Tras el gate → Concilio. |

---

## Reglas de uso (obligatorias para todo agente del concilio)

1. **Todo turno deja al menos una línea en el WORKLOG.** Si cerraste un turno
   sin escribir aquí, el turno no está terminado. Es regla HARD (ver
   AGENTS-PLAN §2.5).
2. **Formato de entrada** (sigue la plantilla de abajo):
   - `## Fecha — Hora — [Agente]` al inicio (dentro del archivo del día).
   - Sección `QUÉ` = lo hecho (concreto, con rutas/archivos).
   - Sección `POR QUÉ` = la razón de cada decisión importante. Sin esto, el
     sistema se auto-olvida.
   - Sección `ENTREGABLE / ESTADO` = dónde quedó el trabajo (ruta) y estado
     en su fichero de `backlog/tareas/` (mapa: `backlog/INDICE.md`).
   - Si hay cabos sueltos para el siguiente agente → sección `RELEVO`.
3. **Decisiones de arquitectura** (grandes, permanentes) → además de aquí,
   crear un ADR en `docs/ADR/` con fecha + motivo. El WORKLOG puede enlazarlo,
   pero el detalle largo vive en el ADR.
4. **Nada de rellenar por rellenar.** Cada entrada aporta: un estado, una
   decisión o un aprendizaje. Texto de relleno solo ensucia el registro.
5. **Idioma:** español, con el tono natural del equipo. Sin empeño de AI-slop
   (aplica criterio humanizer incluso aquí: el WORKLOG es público).
6. **Al crear un archivo de un día nuevo**, añade una fila a la tabla de
   `index.md` (arriba).

## Plantilla de entrada diaria

```markdown
### Fecha — Hora — [Nombre del agente / Juanma]
**QUÉ:**
- (hecho 1 con ruta si aplica)

**POR QUÉ:**
- (razón de cada decisión importante)

**ENTREGABLE / ESTADO:**
- (ruta del entregable + estado en su fichero de backlog/tareas/)

**RELEVO (para quién sigue):**
- (qué debe mirar/seguir el siguiente agente)
```