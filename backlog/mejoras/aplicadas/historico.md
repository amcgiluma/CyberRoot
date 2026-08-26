# MEJORAS APLICADAS — Historial de implementación (CyberRoot)

> Registro OBLIGATORIO que deja **Gwyn** cada vez que aplica una mejora a un
> prompt de un agente con `hermes cron edit --prompt ... <job_id>` (es lo que
> documenta en GitHub qué se cambió, en qué agente, cuándo y por qué). Va a
> GitHub público. Formato:

```
[APLICADA] (fecha) — por Gwyn
- Agente/job afectado: <nombre del agente> (<job_id>)
- Qué se cambió (del prompt): <resumen del cambio>
- Qué se mejoró / por qué: <motivo>
```

> Regla: cada `[APLICADA]` va acompañada de su commit en el worklog del día y
> de este registro. Sin eso, la mejora no está completa.

## Historial

### [APLICADA] (26/08) — por Raiden (reestructurador one-shot, autorizado por decisión de Juanma)
- Agentes/jobs afectados: los 9 del Concilio (Manus `f6bef0f8e3d8`, Oscar
  `ee900afb19da`, Havel `e3c150781f9d`, Gwyndolin `d5c8def555cd`, Ornstein
  `1ebe58fd86a3`, Smough `55bb406c6e4c`, Seath `65ccfc807dd6`, Artorias
  `c4c98c5d8950`, Gwyn `d972fdc912b7`) + Vigilante `7dec77a6d301` + Arquitecto
  F0 `70997a08ff3a` + Coordinador F0 `c206c75818eb`.
- Qué se cambió (del prompt): todas las referencias al monolítico
  `backlog/TODO.md` / `backlog/MEJORAS.md` pasan a la estructura nueva
  (`backlog/tareas/{pendiente,en-curso,hecho-<mes>,descartado}`,
  `backlog/mejoras/{pendiente,aplicadas}`, `backlog/zona-testeo.md`,
  `backlog/notas-manana.md`, índice en `backlog/INDICE.md`). Cada agente ahora
  Lee SOLO los ficheros de su rol (ver tabla en INDICE.md); los prompts quedan
  más cortos en lectura.
- Qué se mejoró / por qué: dentro de 3 meses TODO.md sería un megafichero que
  todos leerían enteros (violación de la regla de oro). Ahora cada turno lee
  solo su subconjunto y «hecho» se archiva POR MES.
- Detalle completo: `docs/worklog/2026/08/26.md` (entrada del reestructurador).
