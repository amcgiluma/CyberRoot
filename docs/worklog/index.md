# WORKLOG — Registro diario del Concilio (CyberRoot)

> 📖 **QUÉ ES:** la bitácora del proyecto. Cada agente deja constancia de
> *qué hizo, qué decidió y por qué* durante su turno. Es el "razonamiento"
> del sistema, complementario al `backlog/TODO.md` (que solo lleva el estado
> de las tareas).
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
| 2026-08-23 | `2026/08/23.md` | Fundación del proyecto: comité de IAs, concilio Dark Souls, roguelite Hades, infra del repo. |

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
     en el TODO.
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
- (ruta del entregable + estado en backlog/TODO.md)

**RELEVO (para quién sigue):**
- (qué debe mirar/seguir el siguiente agente)
```