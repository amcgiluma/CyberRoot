# MEJORAS — Auto-mejora del comité (CyberRoot)

> 📌 **DÓNDE los agentes proponen mejoras a su propio rol/prompt/flujo.**
> Cualquier agente que detecte que algo no funciona (tarea imposible, cuello de
> botella, paso confuso, solapamiento, prompt ineficiente) puede proponer aquí
> una mejora para que Gwyndolin o un humano (Raiden/Juanma) la aplique.
> Ver roles y límites en `docs/AGENTES.md` (sección AUTO-MEJORA).

## Formato de propuesta
```
[PROPUESTA] (fecha) — quién — a quién/afecta a qué
- Problema: (qué no funciona y por qué)
- Propuesta: (qué cambiar, con concreto)
- Impacto esperado: (qué mejora)
- Estado: [NUEVA] / [EN REVISIÓN] / [APROBADA] / [DESCARTADA]
```

## Reglas
1. Proponer en `backlog/MEJORAS.md` y marcar el estado. No auto-cambiarse el rol
   si afecta a otros.
2. Los horarios del concilio y la cadena de PRs/merge son el esqueleto: NO se
   cambian sin aprobación (se puede PROPONER el cambio).
3. Todo cambio aplicado queda registrado aquí + en el WORKLOG (trazabilidad).

## Propuestas

### Primera propuesta (siembra)
`[PROPUESTA] (23/08) — Raiden — todos los agentes`
- Problema: los agentes del concilio podían no saber qué hacía el resto.
- Propuesta: crear `docs/AGENTES.md` (roles del concilio) para que todo agente
  sepa quién hace qué al arrancar, y este `backlog/MEJORAS.md` para auto-mejora.
- Impacto: coordinación y capacidad de self-improvement del comité.
- Estado: [APROBADA] (aplicada por Raiden).