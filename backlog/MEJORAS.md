# MEJORAS — Auto-mejora del comité (CyberRoot)

> 📌 **DÓNDE los agentes proponen y registran mejoras a su rol/prompt/flujo.**
> Cualquier agente que detecte que algo no funciona (tarea imposible, cuello de
> botella, paso confuso, solapamiento, prompt ineficiente) puede proponer aquí
> una mejora. **Quien la aprueba y la APLICA es Gwyn** (revisor final, 23:00),
> usando el CLI oficial `hermes cron edit --prompt ... <job_id>`; Juanma supervisa.
> Ver roles y límites en `docs/AGENTES.md` (sección AUTO-MEJORA) y AGENTS-PLAN §2.6.

## Formato de propuesta
```
[PROPUESTA] (fecha) — quién — a quién/afecta a qué
- Problema: (qué no funciona y por qué)
- Propuesta: (qué cambiar, con concreto)
- Impacto esperado: (qué mejora)
- Estado: [NUEVA] / [EN REVISIÓN] / [APROBADA] / [DESCARTADA] / [APLICADA]
```

## 📋 Historial de implementación (registro obligatorio — va a GitHub)
Cuando **Gwyn aplica** una mejora a un prompt de un agente, DEBE añadir una
entrada aquí en el formato siguiente (es lo que documenta en GitHub qué se
cambió, en qué agente, cuándo y por qué):

```
[APLICADA] (fecha) — por Gwyn
- Agente/job afectado: <nombre del agente> (<job_id>)
- Qué se cambió (del prompt): <resumen del cambio>
- Qué se mejoró / por qué: <motivo>
```
> Regla: cada `[APLICADA]` va acompañada de su commit en el worklog del día y de
> este registro. Sin eso, la mejora no está completa.

## Reglas
1. Proponer en `backlog/MEJORAS.md` y marcar el estado. No auto-cambiarse el rol
   si afecta a otros: lo aplica Gwyn.
2. Los horarios del concilio y la cadena de PRs/merge son el esqueleto: NO se
   cambian sin aprobación de Juanma (se puede PROPONER el cambio).
3. Todo cambio aplicado queda registrado aquí (`[APLICADA]`) + en el WORKLOG
   (trazabilidad pública en GitHub).

## Propuestas

### Primera propuesta (siembra)
`[PROPUESTA] (23/08) — Raiden — todos los agentes`
- Problema: los agentes del concilio podían no saber qué hacía el resto.
- Propuesta: crear `docs/AGENTES.md` (roles del concilio) para que todo agente
  sepa quién hace qué al arrancar, y este `backlog/MEJORAS.md` para auto-mejora.
- Impacto: coordinación y capacidad de self-improvement del comité.
- Estado: [APROBADA] (la aplicó Raiden; el mecanismo real lo aplica Gwyn).

---

## 📓 Historial de aplicación (implementado)

_(aquí Gwyn añadirá cada `[APLICADA]` cuando aplique una mejora de prompt)_