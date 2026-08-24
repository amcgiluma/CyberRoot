# TODO — La cola de trabajo (CyberRoot)

> 📌 **DONDE VIVE TODO EL ESTADO DEL SISTEMA.** Cada agente lo lee para saber
> qué hacer y lo escribe al terminar. Sin esto, el sistema no se comunica.
>
> Convención de estados (SIEMPRE con estos prefijos en mayúscula):
> - `[PENDIENTE]`  …tarea lista y abierta. Las ideas de Havel entran aquí y el
>   planificador las coge para implementarlas SIN esperar aprobación humana
>   (autonomía total del comité).
> - `[EN CURSO]`   …un agente está trabajando en ello YA.
> - `[HECHO]`      …implementado Y documentado. Marquese al terminar, siempre.
> - `[DESCARTADO]` …rechazado (por Juanma o porque no encaja). No retomarlo
>   salvo petición expresa.
> - `[APROBADO]`   …(opcional) Juanma lo marcó explícitamente. Ya no es
>   requisito para planificar: queda solo como registro de visto bueno humano.
>
> Formato de cada item (mínimo):
> `- [ESTADO] (fecha) Título — quién: detalle breve.`
> Añade `↩ respuesta de Juanma` cuando él decida sobre algo.

---

## ✅ Ya sabes lo que hay que hacerse — flujo diario
1. Havel (07:00) AÑADE ideas/bugs aquí (como `[PENDIENTE]`) — sin filtro humano.
2. El planificador (11:00) coge lo `[PENDIENTE]` (incluidas las ideas de Havel),
   las convierte en tareas concretas con módulo y las deja `[EN CURSO]` en
   `backlog/planes/YYYY/MM/DD.md` (plan de hoy). FLUJO 100% AUTÓNOMO: no espera
   aprobación de Juanma.
3. Los ejecutores (13/16/19) implementan y marcan `[HECHO]` + documentan.
4. Revisores (21/23) validan, marcan `[HECHO]` si pasan o lo devuelven.
5. Fin de día → todo queda escrito para que al día siguiente se lea y siga.
6. Juanma solo interviene excepcionalmente (reporte de Gwyn o su feedback),
   no en cada idea.

---

## TAREAS

### Ideas (fase de pre-diseño)
- `[PENDIENTE]` (23/08) Estructurar el comité de IA diario — la base de todo.
  Decisión tomada; se está documentando en AGENTS-PLAN.md.

### Fase 0 (research y diseño)
- `[EN CURSO]` (23/08) Crons de Fase 0 configurados y activos (research stack/anti-slop/mecánicas 03-07h, diseño 11h, arquitectura 16h). →Mañana 24/08 empiezan a producir DESIGN.md + plot.
- `[HECHO]` (24/08) **Research Stack completado** — agente Research Stack:
  `docs/INVESTIGACION-STACK.md` pasado de preliminar a definitivo con fuentes
  primarias verificadas. Pyxel CONFIRMADO (MIT, 17.7k★, v2.9.9, wasm OK,
  `init(headless=True)` oficial = testeo autónomo garantizado). Separación
  core/render CONFIRMADA y reforzada (reglas de frontera + RNG seedeada).
  Riesgos documentados: bus factor=1 de Pyxel (plan B pygame-ce), fuente
  bitmap para terminal in-game. Pendiente de ratificar por Juanma en el gate.
- `[PENDIENTE]` (24/08) Validar fuente bitmap legible para la terminal in-game
  (5×7 aprox., paleta CRT) con capturas reales en Pyxel — Research Stack:
  es EL riesgo visual detectado; resolverlo ANTES del Diseñador P4 (dopamina/UX
  del 26/08) para que el diseño de HUD parta de un texto que se lee bien.
- `[PENDIENTE]` (23/08) Gate de Juanma sobre `docs/DESIGN.md` al cerrar la Fase 0.
  ↩ (24/08) El gate debe incluir también ratificar Pyxel como stack definitivo
  (recomendación del research: SÍ).
- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** creados y PAUSADOS (Manus/Havel/Gwyndolin/Ornstein/Smough/Seath/Artorias/Gwyn). Se activan tras el gate.

### Backlog de ejecución
*(se llena en Fase 0 / al aprobar ideas)*

---
*Regla: al terminar SIEMPRE actualiza el estado aquí. Es tu huella en el sistema.*