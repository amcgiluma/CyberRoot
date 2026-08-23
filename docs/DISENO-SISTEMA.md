# Diseño del sistema de agentes autónomos — CyberRoot

> Fecha: 23/08/2026 · Estado: propuesta (pendiente de aprobación de Juanma)

Sistema por el que varios agentes desarrollan el juego de forma autónoma,
documentando todo, con revisión en dos capas y eficiencia de tokens.

## Filosofía
Juanma decide el "qué" (criterio, gustos, dirección global). El sistema
ejecuta el "cómo" en bucle diario autónomo. La documentación del proceso
vive en el propio repo (público) como valor añadido.

## Roles de los agentes

### 1. Planificador — llama a un modelo fuerte (ej. Grok 4.6)
- Leen el diseño, el backlog, el estado del juego y los mensajes de Juanma.
- Convierten ideas/feedback en **planes accionables y ordenados**.
- Reparten el trabajo en piezas que NO colisionan entre ejecutores.
- Pocas llamadas, razonamiento caro, ejecución barata posterior.

### 2. Ejecutores — modelos básicos/baratos (ej. DeepSeek V4 Flash)
- Implementan las tareas ordenadas del plan de forma mecánica.
- Cada uno con su **zona del repo** para evitar conflictos de git.
- Muchas llamadas, modelo barato → eficiencia de tokens.
- Deben jugar/testear su parte de forma real antes de dar por hecha la tarea.

### 3. Revisor filtra — modelo barato (ej. DeepSeek)
- Compila, corre lint y smoke tests del diff reciente.
- Rechaza lo que esté roto con comentario accionable.

### 4. Revisor de diseño — modelo más fuerte
- Comprueba que el PR sigue el plan y la visión del diseño (no solo que "compite").
- Da el visto bueno de criterio.
- Modelo distinto al constructor → no se auto-aprueba.

## Scheduling (crons diarios)
- **1 cron de ideas:** recoge reflexiones/dirección (para alimentar al planificador).
- **2–3 crons de trabajo:** ejecutores en franjas horarias separadas, cada uno
  en su módulo (evita conflicto de colisiones).
- **1 cron de revisión de PRs:** el filtro + el de diseño, en cadena.

## El puente entre días: la "libreta"
Cada cron arranca en sesión limpia SIN memoria conversacional. El puente es
un fichero de estado que se lee y se escribe:
- `TODO.md` — backlog con estados (pendiente / en curso / hecho / descartado).
- `WORKLOG.md` — registro diario: qué se hizo, qué queda, decisiones y razón.
- ADR en `docs/` — decisiones de arquitectura con fecha y motivo.
La libreta es la fuente de verdad única entre sesiones.

## Eficiencia de tokens (a documentar en el repo)
- Modelo caro solo para planificar/diseñar/criterio; modelo barato para ejecutar.
- `context_from` para encadenar salidas entre crons sin releer todo el repo.
- Ejecutores con alcance acotado a su módulo (no releen el repo entero).
- Decisiones de asignación de modelos quedan en ADR.

## Repositorio
- **Público** en GitHub (decisión de Juanma: portfolio + transparencia).
- Sin secretos ni credenciales dentro (ver `.gitignore`).
- README explicando el sistema de agentes como diferenciador, no como algo que ocultar.

## Pendiente para arrancar
- [ ] Autenticar `gh` con la cuenta de Juanma (una vez, una sola acción suya).
- [ ] Aprobar diseño del juego y reparto de agentes.
- [ ] Crear repo público y estructura git.
- [ ] Configurar los crons.