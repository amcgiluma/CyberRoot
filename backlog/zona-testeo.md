# 🔬 Testeo de mañana

> La escribe **GWYN al cierre (23:00)** SOBRESCRIBIENDO este fichero, con el
> formato exacto de `docs/TESTEO-DIARIO.md` §4 (máx. 2 prioridades + smoke).
> La lee **OSCAR (05:00)** primero —recorrido completo— y la continúa
> **HAVEL (07:00)** con ojos de novedad. Relevo: Gwyn → Oscar → Havel.
> Si algún día no hay zona, fallback: Oscar usa su run de referencia habitual
> y Havel su `git log --since` + smoke del camino real (TESTEO-DIARIO §4).

## 🔬 Testeo de mañana (2026-08-26)

Zona prioritaria: coherencia de la reestructuración del backlog (26/08)
- Recorrer `backlog/INDICE.md` y verificar que las rutas nuevas (`tareas/`, `mejoras/`, `zona-testeo.md`, `notas-manana.md`) están reflejadas igual en `docs/PROJECT-MAP.md`, `docs/AGENTES.md` y los prompts de los crons (sin menciones huérfanas a los antiguos `TODO.md`/`MEJORAS.md` fuera de worklogs históricos).
- Segunda prioridad: simular el flujo de una tarea (pendiente → en-curso → hecho del mes) con una tarea real de ejemplo y comprobar que cada rol sabe dónde escribir.
- Smoke: la GitHub Page (`docs/mapa/index.html`) sigue mostrando el flujo del día y las zonas del repo sin referencias rotas.

Contexto: división de `backlog/TODO.md` y `backlog/MEJORAS.md` en carpetas por estado + índice (reestructurador one-shot, 26/08); el primer uso real del relevo con código llegará en Fase 1.
