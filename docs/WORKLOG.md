# WORKLOG — Registro diario del Concilio (CyberRoot)

> 📖 **QUÉ ES ESTE FICHERO:** la bitácora del proyecto. Aquí cada agente deja
> constancia de *qué hizo, qué decidió y por qué* durante su turno. Es el
> "razonamiento" del sistema, complementario al `backlog/TODO.md` (que solo
> lleva el estado de las tareas).
>
> - **¿Cómo se escribe?** Añadiendo una entrada nueva bajo `## Entradas`,
>   NUNCA borrando las anteriores (es registro acumulativo de la historia real).
> - **¿Qué debe contener cada entrada?** Fecha, autor (agente o Juanma),
>   QUÉ se hizo, QUÉ se decidió, POR QUÉ, y qué entregable dejó. El "porqué"
>   es lo más valioso: es lo que permite a los demás agentes seguir el hilo
>   sin leer todo el proyecto.
> - **¿Caducan las entradas?** No. Son el relato del desarrollo. Se pueden
>   consultar para entender decisiones antiguas (y para "fardar" públicamente
>   de cómo se construyó el juego desde cero).

---

## Reglas de uso (obligatorias para todo agente del concilio)

1. **Todo turno deja al menos una línea en el WORKLOG.** Si cerraste un turno
   sin escribir aquí, el turno no está terminado. Es regla HARD (ver
   AGENTS-PLAN §2.5).
2. **Formato de entrada** (sigue la plantilla de abajo):
   - `**Fecha — Hora — [Agente]` al inicio.
   - Sección `QUÉ` = lo hecho (concreto, con rutas/archivos).
   - Sección `POR QUÉ` = la razón de cada decisión importante. Sin esto, el
     sistema se auto-olvida.
   - Sección `ENTREGABLE / ESTADO` = dónde quedó el trabajo (ruta) y estado
     en el TODO.
   - Si hay cabos sueltos para el siguiente agente → sección `RELEVO`.
3. **Decisiones de arquitectura** (grandes, permanentes) → además de aquí,
     crear un ADR en `docs/ADR/` con fecha + motivo. El WORKLOG puede
     enlazarlo, pero el detalle largo vive en el ADR.
4. **Nada de rellenar por rellenar.** Cada entrada aporta: un estado, una
   decisión o un aprendizaje. Texto de relleno solo ensucia el registro.
5. **Idioma:** español, con el tono natural del equipo. Sin empeño de AI-slop
   (aplica criterio humanizer incluso aquí: el WORKLOG es público).

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

---

## Entradas

### 23/08/2026 — 13:00 — [Raiden, en sesión de diseño con Juanma]
**QUÉ:**
- Documentamos la Fase de Diseño del proyecto CyberRoot en
  `docs/AGENTS-PLAN.md` y montamos la infraestructura del repo:
  repo público `amcgiluma/CyberRoot` creado y conectado (commit inicial
  `9d4c0f9`, actualizado hasta `4b43300`).
- Creada la estructura de la libreta: `docs/PROJECT-MAP.md` (índice maestro),
  `backlog/TODO.md` (cola de trabajo con estados), `docs/BRAINSTORM.md`
  (ideas), `docs/INVESTIGACION-STACK.md` (research preliminar, marcado como
  NO definitivo — se ha de ampliar en la Fase 0), `docs/AGENTS-PLAN.md`
  (sistema de agentes).

**POR QUÉ:**
- Decidido con Juanma el modelo de desarrollo: un **comité de IAs diario y
  autónomo** que construye el juego poco a poco, documentando todo y siendo
  transparente en GitHub (es la feature y el gancho público).
- Cada cron arranca sin memoria; por eso la **libreta es la fuente de verdad
  única** (PROJECT-MAP + TODO + WORKLOG + ADR). Sin ella el sistema no se
  comunica entre sesiones.

**DECISIONES CLAVE cerradas hoy (para el registro):**
- **Nombres del concilio** (lore Dark Souls): Manus (historiador 3:00),
  Havel la Roca (tester 7:00), Gwyndolin (planificador 11:00), Ornstein
  (13:00), Smough (16:00), Seath (19:00), Artorias (revisor 21:00),
  Gwyn (revisor + merge 23:00).
- **Modelos (verificados con `opencode models opencode-go`):** planificador
  y diseñador jefe = `opencode-go/deepseek-v4-pro` (caro, tokens restringidos);
  el resto del concilio = `opencode-go/deepseek-v4-flash` (barato); revisor de
  diseño + merge = `opencode-go/gpt-5.6-luna`.
- **Diseño del juego:** roguelite HÍBRIDO estilo Hades (muerte alimenta el
  avance, base/Hub entre runs, boons de conocimiento, metaprogresión,
  karma Blue/Red con finales múltiples) + dopamina tipo Balatro (números,
  combos, feedback chillón). Interfaz: mapa de nodos/HUD visual (pixel-art),
  interacción de resolución en terminal real. → referencia oficial del
  `DESIGN.md` de la Fase 0.
- **Cadena de PRs:** ejecutor crea branch/PR → Artorias valida/filtra → Gwyn
  revisa en profundidad y hace el MERGE final → reporta a Juanma.
- **Eficiencia de tokens:** panel de uso a `docs/USAGE.md` vía
  `opencode stats --days N --models` (suscripción OpenCode Go ~ $10/mes).

**ENTREGABLE / ESTADO:**
- `docs/AGENTS-PLAN.md`, `docs/PROJECT-MAP.md`, `backlog/TODO.md`, `docs/BRAINSTORM.md`,
  `docs/INVESTIGACION-STACK.md` → en main (repo público).
- Tareas aceptadas actuales en TODO como `[PENDIENTE]`/`[APROBADO]`.

**RELEVO (próximos pasos):**
- Crear la base del `docs/WORKLOG.md` (esta entrada).
- Definir/programar el cron del panel de uso (métricas diarias → `USAGE.md`).
- Configurar los **crons de Fase 0** (research stack/mecánicas/anti-slop,
  diseñador jefe, arquitectura) → producir `DESIGN.md` + plot + mapa de
  módulos. Gate de Juanma al cierre.
- Aprobado el diseño → instalar los crons del **concilio diario** (7 agentes)
  y eliminar los provisionales.

---
*Sesión liderada por Raiden junto a Juanma. Próxima revisión: al cerrar la Fase 0.*