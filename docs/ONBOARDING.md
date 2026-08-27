# 🎮 ONBOARDING — Retomar CyberRoot en una sesión nueva

> Léeme SIEMPRE al empezar una sesión de trabajo en este repo. En ~3 minutos te
> pongo al día de QUÉ es este proyecto, DÓNDE está cada cosa y QUÉ está pasando
> HOY. No asumas nada: con esto + los ficheros que te refiero ya puedes actuar.
> (*Última actualización 27/08/2026.*)

## 1. Qué es esto (30 segundos)
**CyberRoot** es un **juego roguelite educativo de hacking/Linux** (inspirado en
Hades + dopamina tipo Balatro + sinergias tipo Isaac) que está siendo **escrito
100% por un comité de 9 agentes IA autónomos** ("el Concilio") que se ejecutan
cada día vía cron y despliegan a este repo público.

El juego es el **pretexto**. El **logro real** es el sistema de agentes que se
planifican, se ejecutan, se revisan, se corrigen y se mejoran a sí mismos — el
usuario lo vive como el objetivo en sí.

**Estado actual (27/08):** Fase 0 (diseño) cerrada con **gate aprobado** el 26/08
23:25. **Fase 1 ACTIVA**: el Concilio construye el juego desde el 27/08. Todo en
`main`. El Concilio corre solo; tú (agente humano/interface) supervisas, verificas
y das el gusto final.

## 2. Dónde está CADA cosa → y en qué orden leerla

| Archivo | Qué es |
|---|---|
| **`docs/worklog/`** | El registro diario (`2026/08/27.md` = HOY). PRIMERA lectura: lo que pasó. |
| **`docs/AGENTS-PLAN.md`** | El plano completo del Concilio (roles, horarios, protocolo, modelo). |
| **`docs/PROJECT-MAP.md`** | Quién escribe dónde + los módulos del core. |
| **`backlog/INDICE.md`** | Mapa del backlog: qué está pendiente, en curso, hecho. |
| **`backlog/planes/YYYY/MM/DD.md`** | El plan de HOY (qué toca ejecutar). |
| **`src/core/ARCHITECTURE.md`** | Normativa técnica (frontiera core/render, contratos). |
| **`docs/DESIGN.md`** | La visión del juego (1.159 líneas, crece). |

**Orden de lectura recomendado** (si vienes de cero):
`docs/worklog/<hoy>` → `docs/AGENTS-PLAN.md` → `backlog/planes/<hoy>` → las demás
bajo demanda.

## 3. El Concilio (9 agentes IA vía cron en Hermes)

| Hora | Agente | Rol | Modelo | Job id |
|---|---|---|---|---|
| 03:00 | Manus | historia | glm-5.3-flash | `f6bef0f8e3d8` |
| 05:00 | Oscar | experiencia del jugador | glm-5.3-flash | `ee900afb19da` |
| 07:00 | Havel | ideas + testeo | glm-5.3-flash | `e3c150781f9d` |
| 11:00 | Gwyndolin | planifica | glm-5.3-flash | `d5c8def555cd` |
| 13:00 | Ornstein | ejecutor 1 | glm-5.3-flash | `1ebe58fd86a3` |
| 16:00 | Smough | ejecutor 2 | glm-5.3-flash | `55bb406c6e4c` |
| 19:00 | Seath | ejecutor 3 | glm-5.3-flash | `65ccfc807dd6` |
| 21:00 | Artorias | revisor filtro | glm-5.3-flash | `c4c98c5d8950` |
| 23:00 | Gwyn | validación + MERGE | glm-5.3-flash | `d972fdc912b7` |

**Vigilante** (`7dec77a6d301`, deepseek-v4-flash): red de seguridad, cada 60 min,
comprueba que cada agente corrió ~1h tras su turno y **reporta** (no reprograma).

Fuente de verdad de los crons: `hermes cron list` (o `~/.hermes/cron/jobs.json`).
NO edites jobs.json a mano — usa `hermes cron edit/update`.

## 4. Reglas CRÍTICAS que debes respetar

1. **Modelos:** TODO el Concilio usa `glm-5.3-flash`. El Vigilante usa
   `deepseek-v4-flash` (independiente a propósito). **NO** usar `gpt-5.6-luna`
   (roto, HTTP 500), `ox-alpha-free` (caducó), `deepseek-v4-flash/pro` para
   ejecutores. La prueba FIABLE de un modelo = cron one-shot que entregue;
   `opencode run -m X` por shell da **falsos** UnknownError.
2. **Ejecutores:** antes de codear, **PLAN DE IMPLEMENTACIÓN propio en hitos**
   (~1h cada uno, con criterio de "hecho") + **delegar cada hito en sub-agentes**
   y verificar el resultado real. No importa que el plan de Gwyndolin sea de alto
   nivel: el detalle lo ponen los ejecutores.
3. **Firma git por agente**: cada agente hace `git config user.name "X"` antes de
   commit. Gwyn es el ÚNICO que mergea a main.
4. **AUTO-MEJORA**: un agente puede proponer cambios a los prompts vía
   `backlog/mejoras/pendiente/propuestas.md`; Gwyn los valida y aplica
   (`hermes cron edit`), registrando en `mejoras/aplicadas/historico.md`.
5. **Anti-slop**: la prosa del juego pasa `humanizer` + `docs/SKILLS-ANTISLOP.md`.
6. **No usar codex** como fallback de modelos.

## 5. LO QUE TOCA HOY — mira el plan del día
`backlog/planes/2026/08/27.md` (o el de la fecha actual si estás otro día).
Típico del ciclo diario:
- Los **ejecutores** implementan su módulo (código en ramas `feat/<módulo>`, PR a
  main), con su plan de hitos documentado.
- **Artorias** revisa los PR, **Gwyn** valida contra el DESIGN y mergea cada noche,
  y deja **`backlog/zona-testeo.md`** (zona 🔬) para el testeo de mañana.
- **Oscar** (05:00) juega/revisa lo nuevo desde save limpio; **Havel** (07:00) ideas.

## 6. Si llegas y NO sabes qué se ha hecho hoy
1. `git log --oneline -15` → commits recientes (quién hizo qué).
2. `git log --since="24h" --author="<agente>"` → por agente.
3. `cat docs/worklog/hoy` → el relato del día.
4. `hermes cron list` → estado de los crons.

## 7. Deploy web (P1) — cuándo lo toca
Cuando exista un build jugable, montar **Vercel** (CLI autenticado como
`hanjitrunks-3934`) o **fallback GitHub Pages**. SOLO cuando haya build (no crear
proyecto vacío). Actualizar el enlace en el `README.md` al publicar.