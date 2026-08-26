# MEJORAS PENDIENTES — Propuestas de auto-mejora del comité (CyberRoot)

> 📌 Dónde los agentes proponen mejoras a su rol/prompt/flujo. Cualquier agente
> que detecte que algo no funciona (tarea imposible, cuello de botella, paso
> confuso, solapamiento, prompt ineficiente) propone aquí. **Quien aprueba y
> APLICA es Gwyn** (revisor final, 23:00), con el CLI oficial
> `hermes cron edit --prompt ... <job_id>` (NUNCA edites `jobs.json` a mano);
> Juanma supervisa. Roles y límites: `docs/AGENTES.md` (AUTO-MEJORA) y
> AGENTS-PLAN §2.6. Cada mejora aplicada se registra en
> `../aplicadas/historico.md`.

## Formato de propuesta

```
[PROPUESTA] (fecha) — quién — a quién/afecta a qué
- Problema: (qué no funciona y por qué)
- Propuesta: (qué cambiar, con concreto)
- Impacto esperado: (qué mejora)
- Estado: [NUEVA] / [EN REVISIÓN] / [APROBADA] / [DESCARTADA] / [APLICADA]
```

## Reglas

1. Proponer aquí y marcar el estado. No auto-cambiarse el rol si afecta a otros: lo aplica Gwyn.
2. Los horarios del concilio y la cadena de PRs/merge son el esqueleto: NO se cambian sin aprobación de Juanma (se puede PROPONER el cambio).
3. Todo cambio aplicado queda registrado en `../aplicadas/historico.md` (`[APLICADA]`) + en el WORKLOG (trazabilidad pública en GitHub). Sin eso, la mejora no está completa.

## Propuestas abiertas

### Propuestas del Arquitecto (Fase 0, cierre)
`[PROPUESTA] (26/08) — Arquitecto — Gwyn / Ornstein / todos`
1. **Espacio de trabajo del harness fuera de `src/`**: la estructura de
   `backlog/` cubre a los 9 agentes EXCEPTO un caso — el **harness de
   playtest** que construye Ornstein (`tools/harness/` en la raíz, junto al
   `tools/cyberroot_usage.py` existente). Es herramienta de CI/métricas, no
   código del juego ni entrega narrativa; no cabe en `src/` (rompería la
   frontera core/render) ni en `backlog/`. Propuesta: crearlo en la raíz como
   `tools/harness/`, propiedad de Ornstein (`feat/engine`), con sus métricas
   exportables a `docs/` cuando Gwyn las pida. *(Ya recogido así en
   `docs/PROJECT-MAP.md` §3 — esta entrada es solo para trazabilidad de la
   excepción.)*
2. **`docs/ADR/` se estrena hoy** con `ADR-0001` (frontera core/render).
   Recordatorio operativo: decisiones grandes de arquitectura → ADR numerado +
   fila en el WORKLOG, como ya pedía `docs/worklog/index.md` regla 3.
   *(Creado: `docs/ADR/ADR-0001-arquitectura-core-render.md`.)*

- Estado: [NUEVA] — para decisión/aplicación de Gwyn (23:00).

### Propuestas del corrector one-shot (integración Oscar en TESTEO-DIARIO)
`[PROPUESTA] (26/08) — Corrector one-shot — Gwyn / Ornstein`
1. **Validar visualmente el mapa GitHub** (`docs/mapa/index.html`): ya refleja
   a Oscar y el flujo, pero tras el cambio de protocolo (relevo
   Gwyn→Oscar→Havel) conviene una pasada visual de la página publicada.
   *(Nota del reestructurador 26/08: la página ya está actualizada también a la
   nueva estructura de backlog; queda pendiente la pasada VISUAL de alguien con
   navegador.)*
2. **Unificar AGENTS-PLAN §4 con TESTEO-DIARIO**: hoy quedan coherentes pero
   duplican parte de la descripción de Artorias/Gwyn; un futuro pase podría
   desglosar las preguntas-filtro de cada capa en un solo sitio para evitar
   divergencias futuras.
3. **Harness con reset explícito (Ornstein, Fase 1)**: exponer comando claro
   de reset-a-save-limpio + save-veterano (20+ h); es requisito duro de la
   capa EXPERIENCIA/PROGRESIÓN de Oscar (`docs/TESTEO-DIARIO.md` §1).
- Estado: [NUEVA] — para decisión/aplicación de Gwyn (23:00).
