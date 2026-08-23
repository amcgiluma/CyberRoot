# AGENTES — Roles del Concilio (CyberRoot)

> ⚠️ **LEE ESTE FICHERO.** Aquí se explica QUÉ hace cada agente del Concilio.
> Saber qué hacen los demás te permite: no pisar a nadie, delegar bien, y
> proponer mejoras de forma informada. Es la parte "transparencia entre agentes".

## El Concilio (8 agentes, horario Madrid)
| Hora | Agente | Modelo | Función | Dónde entrega |
|---|---|---|---|---|
| 03:00 | **Manus** (historiador) | flash | Escribe la HISTORIA del día desde el plot. Prosa humanizada. | `backlog/historia/<fecha>.md` |
| 07:00 | **Havel** (vidente-creativo) | flash | JUEGA el juego + GENERA ideas nuevas (capítulos/mecánicas/comandos) + anota bugs. NO lleva la crítica de diseño (eso es de Artorias/Gwyn). | `backlog/TODO.md` |
| 11:00 | **Gwyndolin** (planificador) | pro | Convierte TODO/log-ideas en `backlog/planes/YYYY/MM/DD.md` (HOY) con tareas por módulo. Reparte trabajo. | `backlog/planes/YYYY/MM/DD.md` |
| 13:00 | **Ornstein** (ejecutor 1) | flash | Implementa SU módulo. Construye/mantiene el **harness de playtest**. | `src/<modulo>` |
| 16:00 | **Smough** (ejecutor 2) | flash | Implementa SU módulo. | `src/<modulo>` |
| 19:00 | **Seath** (ejecutor 3) | flash | Implementa SU módulo. | `src/<modulo>` |
| 21:00 | **Artorias** (revisor filtro) | flash | Revisa técnicamente (tests/lint/juego), marca 💥/✅, y DEJA NOTAS DE GUSTO + "qué no mergear" para mañana. | `backlog/TODO.md` |
| 23:00 | **Gwyn** (revisor diseño+merge) | luna | Validación de diseño, MERGE final, DEJA SUS NOTAS DE GUSTO/ideas, y reporta a Juanma. | `backlog/TODO.md` + Telegram |

## Cómo te ayudan a TI (cualquier agente)
- **Antes de actuar, mira qué toca cada uno** → no hagas el trabajo de otro.
- **Si crees que un rol podría hacer algo mejor**, NO lo implementes tú: proponlo en `backlog/MEJORAS.md` (ver sección Auto-mejora abajo).
- **Si tu turno depende de otro** (p.ej. ejecutor de una tarea que puso el planificador), léelo bien en el `backlog/planes/YYYY/MM/DD.md` de HOY.

## Cómo coordinarse (resumen del protocolo, AGENTS-PLAN §2.5)
- Paso 0: lee PROJECT-MAP, TODO, DESIGN, PLAN. Paso 3: deja tu huella SIEMPRE (estado+worklog). Paso 4: deja el relevo para el siguiente.

## AUTO-MEJORA del comité (cómo los agentes pueden mejorarse a sí mismos)
- Cualquier agente que detecte que **su rol, su prompt o el flujo no funcionan** (tarea imposible, cuello de botella, paso confuso, solapamiento) puede proponer una mejora.
- **DÓNDE:** escribe en `backlog/MEJORAS.md` una entrada: `[LÍNEA] Proponer + fecha + quién + problema + propuesta + impacto esperado`.
- **CÓMO SE APLICA:** Gwyndolin o un humano (Raiden/Juanma) revisa las propuestas y actualiza el rol/prompt/flujo correspondiente. No te cambies el rol a ti mismo unilateralmente si afecta a la coordinación con otros.
- **Regla:** mejorar el sistema es tan válido como mejorar el juego. Un agente que propone una buena mejora al flujo está haciendo su trabajo.

## Límites del auto-mejora (para no romper el sistema)
- Los horarios y la cadena de PRs/merge NO se deben alterar sin aprobación (son el esqueleto). Se pueden PROPONER cambios, no auto-aplicarlos si afectan a otros.
- Un agente puede optimizar SU propio trabajo (cómo hace su tarea) pero no cambiar la misión de otro.
- Todo cambio real queda documentado en `backlog/MEJORAS.md` + WORKLOG (trazabilidad pública).