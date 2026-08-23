# TODO — La cola de trabajo (CyberRoot)

> 📌 **DONDE VIVE TODO EL ESTADO DEL SISTEMA.** Cada agente lo lee para saber
> qué hacer y lo escribe al terminar. Sin esto, el sistema no se comunica.
>
> Convención de estados (SIEMPRE con estos prefijos en mayúscula):
> - `[PENDIENTE]`  …aprobado y esperando. Nunca se implementa sin aprobar.
> - `[EN CURSO]`   …un agente está trabajando en ello YA.
> - `[HECHO]`      …implementado Y documentado. Marquese al terminar, siempre.
> - `[DESCARTADO]` …Juanma lo rechazó. No retomarlo salvo petición expresa.
> - `[APROBADO]`   …Juanma dio visto bueno. Listo para que el planificador
>                    lo convierta en tarea.
>
> Formato de cada item (mínimo):
> `- [ESTADO] (fecha) Título — quién: detalle breve.`
> Añade `↩ respuesta de Juanma` cuando él decida sobre algo.

---

## ✅ Ya sabes lo que hay que hacerse — flujo diario
1. El tester (07:00) AÑADE ideas/bugs aquí (como `[PENDIENTE]`).
2. Juanma REVIEWA y marca `[APROBADO]` / `[DESCARTADO]`.
3. El planificador (11:00) coge lo `[APROBADO]` → lo convierte en tareas
   concretas con módulo y lo deja `[EN CURSO]` en `PLAN-del-dia.md`.
4. Los ejecutores (13/16/19) implementan y marcan `[HECHO]` + documentan.
5. Revisores (21/23) validan, marcan `[HECHO]` si pasan o lo devuelven.
6. Fin de día → todo queda escrito para que al día siguiente se lea y siga.

---

## TAREAS

### Ideas (fase de pre-diseño)
- `[PENDIENTE]` (23/08) Estructurar el comité de IA diario — la base de todo.
  Decisión tomada; se está documentando en AGENTS-PLAN.md.

### Fase 0 (research y diseño)
- `[PENDIENTE]` (23/08) Lanzar research dirigido por agentes → validar stack,
  mecánicas, capítulos/niveles y producir `docs/DESIGN.md` + plot general.
  ↩ pendiente de aprobar por Juanma para arrancar.

### Backlog de ejecución
*(se llena en Fase 0 / al aprobar ideas)*

---
*Regla: al terminar SIEMPRE actualiza el estado aquí. Es tu huella en el sistema.*