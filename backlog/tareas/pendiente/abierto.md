# TAREAS ABIERTAS — pendiente (CyberRoot)

> Tareas `[PENDIENTE]`, `[BUG]` e ideas abiertas. Añade quien detecta o
> imagina; consume **Gwyndolin (11:00)** al planificar. Formato:
> `- [ESTADO][PRIORIDAD] (fecha) Título — quién: detalle.` · Estados y mapa: `../INDICE.md`.
> Al elegir una tarea, Gwyndolin MUEVE la línea a `../en-curso/activo.md`.
> Lo completado se archiva en `../hecho/<AAAA-MM>.md`.
> *(Contenido migrado del antiguo `backlog/TODO.md` el 26/08, estados intactos; prioridades asignadas 26/08.)*

## Prioridades

- `[P0]` — máxima/urgente: desbloquea lo crítico o lo que Juanma marca como máxima. Gwyndolin la respeta SIEMPRE por encima de su criterio.
- `[P1]` — alta: importante, entra antes que lo interesante.
- `[P2]` — media: vale pero puede esperar; Gwyndolin usa su juicio de valor.
- `[P3]` — baja/incubando: idea interesante que no compromete nada corto-plazo.

> Orden en el fichero: P0 arriba → P3 abajo no es obligatorio, pero la señal de
> prioridad está en el prefijo. La prioridad no anula la curación de Gwyndolin:
> la guía. Mantener prioridades al día = parte de su HIGIENE GENERAL del backlog.

## Abiertas

- `[PENDIENTE][P1]` (26/08) **Preparar el DEPLOY de Vercel / GitHub Pages para jugar en web** — Juanma: el juego debe estar disponible siempre para testear en navegador (no solo pull+local). Empaquetar el build web (wasm/Pyodide, Pyxel ya lo soporta), subir `index.html`+`.wasm`+assets y publicarlo. Esta tarea es de máx. prioridad: se ejecuta en cuanto exista el build, desde el día 1 de la Fase 1. Nota: los agentes testean headless local (core sin interfaz); la web es para Juanma/público del repo. **DECISIÓN FIJADA (26/08): vía VERCEL con prioridad** — acceso confirmado (Vercel CLI 59.5.0 autenticado como `hanjitrunks-3934`, cuenta con 8 proyectos; `vercel project ls` OK, repo `amcgiluma/CyberRoot` enlazable). El deploy real lo hace el Concilio cuando exista build (no crear proyecto vacío aún). Fallback si algo fallara con Vercel: GitHub Pages (ya en uso para el mapa, sin token).
- `[PENDIENTE][P1]` (23/08) Gate de Juanma sobre `docs/DESIGN.md` al cerrar la Fase 0. ↩ (24/08) El gate debe incluir también ratificar Pyxel como stack definitivo (recomendación del research: SÍ). *(Actual: el gate está en el Coordinador de cierre del 26/08 21:00.)*
- `[PENDIENTE][P1]` (24/08) Validar fuente bitmap legible para la terminal in-game (5×7 aprox., paleta CRT) con capturas reales en Pyxel — Research Stack: es EL riesgo visual detectado; resolverlo antes de cerrar el diseño del HUD. *(Nota: la fecha límite original —P4 del 26/08— pasó; revalorar en curación.)*
- `[PENDIENTE][P2]` (23/08) Estructurar el comité de IA diario — la base de todo. Decisión tomada; documentada en AGENTS-PLAN.md. *(migrado tal cual del TODO.md: cerrado de facto — la curación de Gwyndolin/Gwyn debe confirmarlo y archivarlo o descartarlo)*