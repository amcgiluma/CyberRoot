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

### Propuesta: nuevo agente para el testeo de la experiencia del jugador
`[PROPUESTA] (24/08, por la noche) — Juanma — Havel / testeo`
- Problema: Havel (07:00) puede estar SOBRECARGADO: juega lo nuevo (git diff) + smoke
  del conjunto + genera ideas + ve el estado global. Y quedaría sin resolver del
  todo la "run de referencia": ver el juego como un jugador que EMPIEZA DE CERO y
  avanza (save limpio → capítulo 1 en adelante), que es distinto de probar módulos.
- Propuesta: valorar crear UN NUEVO AGENTE dedicado al testeo de la EXPERIENCIA del
  jugador (estado global de qué está jugable + run de referencia desde save limpio),
  descargando a Havel para que siga en ideas + lo nuevo. Enlazado con el protocolo
  de testeo diario (TESTEO-DIARIO.md, lo hace P5) y el doc ESTADO-JUGADOR.md.
- Impacto: testeo de experiencia más profundo sin sobrecargar a Havel.
- Estado: ↩ (26/08) `[APROBADA y aplicada]` — existe desde el 25/08: es
  **Oscar de Astora** (05:00), integrado en `docs/TESTEO-DIARIO.md` §1. Esta
  propuesta puede archivarse; Gwyn la cierra en su próxima pasada de curación.

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
