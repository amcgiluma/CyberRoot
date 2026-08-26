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
1. Los perfiles de testeo matinales AÑADEN aquí sus hallazgos: **Oscar (05:00)**
   deja `[BUG]` de su run desde save limpio, NOTAS DE DIRECCIÓN para Gwyn e
   ideas de contenido como `[PENDIENTE]`; **Havel (07:00)** añade ideas/bugs
   (como `[PENDIENTE]`) — sin filtro humano.
2. El planificador (11:00) coge lo `[PENDIENTE]` (ideas de Havel y de Oscar,
   más las notas de dirección que Gwyn haya validado),
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
- `[HECHO]` (24/08) **Research Mecánicas + Dopamina completado** — agente Research
  Mecánicas: `docs/RESEARCH-MECANICAS.md` definitivo con fuentes verificadas.
  Cubre: aprender-sin-deberes (Bandit/Terminus/Root-Me/Hacknet + meta-análisis
  Clark 2016/Wouters 2013; vetado el antipatrón quiz-con-skin), dopamina Balatro
  descompuesta en 5 palancas (puntuación compuesta datos×combo, ciclos cortos,
  juice proporcional a magnitud, riesgo/recompensa, cascadas de unlocks) con
  traducción directa a mecánicas CyberRoot, loop Hades (muerte=lección,
  post-mortem automático, metaprogresión dual donde el Linux real del jugador ES
  la progresión), procedural enseñante (piel aleatoria / médula curricular, RNG
  jamás decide semántica de comandos) y UX dual (eventos compartidos core→HUD/
  terminal, mapa diegético estilo Slay the Spire, legibilidad>espectáculo).
  Incluye checklist de 8 directrices para el Diseñador Jefe (P1–P5).
- `[HECHO]` (24/08) **Skills anti-slop documentados** — Manus: `docs/SKILLS-ANTISLOP.md`
  definitivo (relanzado tras 2 fallos 503 del proveedor). 3 capas: filtro humanizer
  (34 patrones + equivalencias españolas + grep de palabras trampa), craft por
  superficie (narrativa ambiental Souls para niveles, diálogo reactivo Hades/GDC
  2021, barks ≤12 palabras, ficha de voz obligatoria por NPC con fila "nunca
  diría", item descriptions dato técnico + grieta humana) e integración en el
  concilio (auto-pass anti-slop documentado en cada commit, checklist de 10
  puntos, revisión Ornstein/Smough cita patrón+línea al rechazar).
- `[PENDIENTE]` (24/08) Validar fuente bitmap legible para la terminal in-game
  (5×7 aprox., paleta CRT) con capturas reales en Pyxel — Research Stack:
  es EL riesgo visual detectado; resolverlo ANTES del Diseñador P4 (dopamina/UX
  del 26/08) para que el diseño de HUD parta de un texto que se lee bien.
- `[PENDIENTE]` (24/08) **Definir el protocolo de TESTEO DIARIO del Concilio** en
  la Fase 0 (→ `docs/TESTEO-DIARIO.md`, lo plantea el Diseñador P5). Tres tester
  con CAPA distinta: Havel 07:00 (lo nuevo por git diff + smoke del conjunto +
  ideas, "¿mola?"), Artorias 21:00 (PRs/ramas técnicamente: tests/lint/juego,
  "¿está bien hecho?"), Gwyn 23:00 (diseño y sabor en conjunto + coherencia,
  "¿es buen juego?"). La ZONA de testeo del día la deja Gwyn al cierre (23:00)
  → Havel la lee a las 07:00. Evitar pisarse entre los 3.
  ↩ (26/08 07:00) `[HECHO]` — Diseñador P5 crea `docs/TESTEO-DIARIO.md`: capa
  por perfil, zona 🔬 Gwyn→Havel con formato fijo, fallback si falta zona,
  prioridades para Gwyndolin, línea CICLO verde/ámbar/rojo en worklog.
- `[PENDIENTE]` (25/08) **Tercer pilar de mecánicas: SINERGIAS, VARIEDAD y
  REJUGABILIDAD tipo Isaac** (pero de conocimiento). Juanma: además de progreso-
  Hades y dopamina-Balatro (ya en research), que los boons/objetos/perks sinergien
  de forma chula y den variedad de runs, sin multiplicar contenido. Lo investiga
  el **Diseñador P2** (11:00 del 25/08) en su sección de sinergias/rejugabilidad.
  ↩ (25/08 09:00) `[HECHO]` — Diseñado en `DESIGN.md` §5 (principio «sinergia
  nace de Unix», 6 tipos, presupuesto ~60 boons + 25–35 sinergias manuales,
  rejugabilidad por fases). Balance numérico → P4; reparto por capítulos → P3.
- `[PENDIENTE]` (23/08) Gate de Juanma sobre `docs/DESIGN.md` al cerrar la Fase 0.
  ↩ (24/08) El gate debe incluir también ratificar Pyxel como stack definitivo
  (recomendación del research: SÍ).
- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** creados y PAUSADOS (Manus/Havel/Gwyndolin/Ornstein/Smough/Seath/Artorias/Gwyn). Se activan tras el gate.

### Backlog de ejecución
*(se llena en Fase 0 / al aprobar ideas)*

---
*Regla: al terminar SIEMPRE actualiza el estado aquí. Es tu huella en el sistema.*