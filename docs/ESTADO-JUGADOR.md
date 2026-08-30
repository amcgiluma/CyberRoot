# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (30/08 — MODO B: el circuito competencia→unlock→save existe y aguanta)

**¿Hay algo que jugar de principio a fin?** AÚN NO como producto (sigue sin
haber entrypoint de juego ni engine), pero el SISTEMA integrado del 29/08 dio
un salto cualitativo: hoy el ciclo **competencia → unlock → save** se recorre
ENTERO y es verificable como jugador. Lo que falta para producto es el
envoltorio (engine que detecte/sancione + render que muestre), no ninguna
pieza necesaria del camino conceptual.

- **En main (PRs #7/#8/#9, mergeados anoche):**
  - **Generator consume curriculum real (O1/Ornstein):** `generate(seed,0)`
    saca el `concept_pool` de `curriculum.json` por ids (`c.ls/cd/cat/cp`),
    la quest del pool del capítulo (`story.ch0.ventana`), exige `requires ⊆
    pool` (§6.4.1) y monta la sesión con `new_session(incursion)` cuyo `cwd`
    nace del **scaffold** (`initial_cwd=/`, opción B) — la 🧭7 de ayer es
    COMPORTAMIENTO, no dict decorativo. 🧭7 SALDADA.
  - **Sandbox GNU honesto (S1/S2/Smough):** `cat fichero/` → *Not a directory*
    exit 1 y `cp dir` → *omitting directory* diagnosticando el ORIGEN (los
    errores GNU son método de enseñanza, §2.6.8). REPL real
    `python -m core.sandbox`: prompt diegético, se juega la secuencia del
    dossier. Primer punto de entrada TOCABLE para Juanma.
  - **Fachadas uniformes (T1/Seath):** `from core.state import GameState,
    save_game, load_game` y `from core.sandbox import Shell` FUNCIONAN desde
    raíz. La fricción de fachada del `core.state` que sufrí como primer
    consumidor el día 29 está CERRADA.
  - **Progression v0 (T2/Seath):** `evaluate_unlocks(state)` marca `c.cp`
    dominado por COMPETENCIA demostrada (lee evidencia real del historial de
    la sesión: un `cp …/usb` con exit 0), idempotente, guardado en
    `GameState.knowledge`. PRIMER unlock de la historia del juego.
- **La plataforma del unlock hoy:** `GameState` sabe recoger el conocimiento
  dominado y persistirlo (`knowledge` en el save v1, opcional, backward-compat
  con saves previos → `{}`). No hay aún sistema de partidas por usuario
  (vendrá con engine/progression), pero el PATRÓN §4.2 está demostrado en
  código y verificado jugando (run de referencia abajo).
- **Decisión de Gwyn firmada en DESIGN §6.1:** costura contrato↔prereqs 🧭8 =
  **opción (b)** — los prereqs de un encargo se evalúan al ABRIR el contrato,
  no al generar la sala. Y política de ruido 🧭6: el cap. 0 perdona el primer
  error grande; el cap. 3, no.
- **Para «jugable de principio a fin» falta:** engine (runs/detección/
  expulsión), materializar 🧭8=(b) en código (Ornstein hoy: el xfail
  `test_costura_navig8` pasa a verde), progression leyendo la factura real y
  algoritmos text, render.

## 🏃 Run de referencia (save limpio) — 30/08

*Partida nueva de cero, misma técnica de siempre: sala REAL generada
(`generate("oscar-20260830-r1",0)` → `room-ch0-4f60cd0a-canonical`), sesión
montada como la montará el engine (ahora vía `new_session`, no a mano),
jugando al NOVATO con el dossier en la mano y curioseando.*

**Veredicto: APTO. El circuito competencia→unlock→save se recorre entero y el
save «recuerda» tu competencia.** Fase a fase:

1. **El camino del cap. 0 sigue intacto con el árbol nuevo.** `cwd` nace en
   `/` (de `scaffold.initial_cwd()` — la opción B YA es comportamiento, 🧭7
   verificada ejecutando), mismo dossier con rutas absolutas, cumbre `cp`
   alcanzable al pie de la letra: ls→cat→cp→cd→ls, todo exit 0. Factura 11/12
   (ls 1 + cat 1 + cp 3 + cd 0 + ls 1 + curiosidad/error lector 5) — dentro
   del presupuesto, igual de justo que ayer, ahora sobre un pool que nace del
   curriculum real.
2. **§4.2 respetado como jugador, no solo en test:** una sesión con ls/cat/
   curiosidad pero SIN el `cp` de la extracción NO marca `c.cp`
   (`knowledge={}`, `newly=[]`). El unlock exige la evidencia — competencia,
   no grind. ✔
3. **Con la evidencia, el unlock PERSISTE en el save:** tras el `cp …/usb`
   exit 0, `evaluate_unlocks` marca `{'c.cp': True}`, `save_game` → disco →
   `load_game` recupera `knowledge={'c.cp': True}` con tick=8 y total_noise=11
   intactos. **Idempotente**: una segunda evaluación no re-marca (vacía). El
   primer unlock de la historia del juego sobrevive a reiniciar. ✔
4. **Errores honestos, método no castigo:** `ls -l` (flag no disponible en el
   cap. 0) → `ls: cannot access '-l'` exit 2 cobrando ruido 1 (fallo léxico,
   no de riesgo — coherente con la política de Gwyn). `cat fichero/` y `cp dir`
   responden como coreutils real. El REPL reproduce la secuencia con prompt
   diegético (`operator@oficina-vecinal…`, banner de conexión).
5. **Determinismo/variedad del cap. 0 intocados:** practice rota decoys por
   seed (1–2/sala: turnos_recepcion, avisos_comunidad, agua_cerrada) sobre
   pool fijo — la rejugabilidad del tutorial respira.

**Estado del save al terminar:** `/tmp/oscar_cap0_save.json` con `c.cp`
dominado, roundtrip verificado. No hay sistema de partidas por usuario aún.

## 👴 Progreso de veterano (save 20+ horas)

El patrón de progresión de fondo YA existe y es el correcto: `knowledge`
persiste y se alimenta SOLO por competencia (§4.2 / DESIGN §4.2 y §7.5.3). Con
el pool del cap. 0 fijo en 4 conceptos, la run 30 de un veterano sigue sin
tener variedad real (sigue siendo un tutorial de 10 min) — eso NO es un defecto
de hoy: es la naturaleza del cap. 0 (aprender por necesidad, 4 comandos), y la
variedad llega cuando generator consuma los pools de los caps. 1–6. **Lo que el
veterano de hoy SÍ puede validar es el patrón del unlock repetido:** un save que
ya domina `c.cp` rejuega el cap. 0 sin que el espejo le regale nada (no hay
atributos «por compra»), y el unlock es idempotente cruzando runs (una sesión
nueva no vuelve a «descubrir» lo ya dominado… a costa de UNA arruga nueva, ver
hallazgo 2 🧭9).

## 📝 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: el CÓDIGO como sistema)

- **Smoke del conjunto:** suite desde raíz → **342 passed + 1 xfailed** exactos
  (cuadra con lo prometido por Gwyn + 1 xfail = `test_costura_navig8`, el de
  🧭8, intencional). Guard de layout `src/tests/architecture/` intacto. ✓
- **Circuito competencia→unlock→save recorrido COMPLETO como jugador** (run de
  referencia de arriba): sala generada → sesión vía `new_session` → dossier →
  cumbre `cp` → curiosidad+errores → `evaluate_unlocks` marca `c.cp` →
  `save_game`/`load_game` lo recupera → idempotencia. ✓
- **§4.2 contra-evidencia verificado:** sin `cp …/usb` no hay unlock. ✓
- **Fachadas:** `core.state` y `core.sandbox` re-exportan (saldo de la
  fricción/nota de calidad de Artorias). 🧭7 materializada. REPL smoke OK.
- **Rejugabilidad:** 4 seeds × {canonical, practice} → decoys rotan
  (1–2/sala), canon resoluble en todas, pool fijo como debe ser en el tuto.

## Hallazgos de la run (dónde aprieta el viaje)

1. **🟠 La progresión por competencia es INVISIBLE para el jugador de hoy.**
   El unlock existe en datos (`c.cp` en `knowledge`) y persiste, pero NO hay
   ningún punto donde el jugador lo VEA: ni annuncio al dominarlo, ni listado
   en el Hub, ni eco en el mundo. Yo solo lo «veo» porque el script lo imprime.
   El Espejo de Gris (§4.3) y el momento diegético de nombrar «qué acabas de
   dominar» aún no existen. Informo para dirección 🧭9; decide Gwyn cuándo.
2. **🟡 Arruga de veterano (asociada):** `evaluate_unlocks` es idempotente por
   unidad de GameState, pero cada run nueva arranca un `GameState` fresco —
   no hay aún un inventario AGREGADO entre runs que diga «el veterano ya
   domina cp». Es la misma incompletitud de «no hay sistema de partidas» (nodo
   6 del mes); lo apunto para que Gwyndolin lo tenga en el plan del engine,
   no como bug.
3. **🟡 Costura contrato↔prereqs, estado:** 🧭8 = opción (b) firmada en DESIGN
   §6.1 y a materializar hoy (Ornstein): el xfail pasa a verde y muere. Ya NO
   es bloqueante; queda como seguimiento del día.

*(Detalle y propuestas de dirección: `backlog/notas-manana.md` 🧭, sobrescritas
hoy. El hallazgo 1 va como nota de dirección 🧭9 para Gwyn; no es tarea.)*

## 🧭 Notas de dirección (resumen — texto completo en `notas-manana.md`)

🧭7 SALDADA (generator consume opción B vía `new_session`: cwd=`/` nace del
scaffold) · 🧭8 SALDADA como decisión (Gwyn firmó opción (b) en DESIGN §6.1;
Ornstein la materializa hoy) · saldo de la fricción de fachada `core.state`
CERRADA. NUEVAS para HOY: 🧭9 (la progresión por competencia necesita su eco
visible: hoy el unlock es data invisible), 🧭10 (recomendación de feedback del
resumen de ruido cuando haya post-mortem). Filtro: apto, camino completo hasta
save funciona, hallazgos son de feedback/calibración, no roturas.

CICLO: verde — el circuito competencia→unlock→save se recorre ENTERO desde
save limpio y aguanta; los hallazgos son feedback y calibración, no roturas.

---
*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*