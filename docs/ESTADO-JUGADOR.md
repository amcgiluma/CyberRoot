# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (31/08 — MODO B: el círculo se cierra con el post-mortem)

**¿Hay algo que jugar de principio a fin?** Mismo diagnóstico de fondo que ayer:
sigue sin haber **entrypoint de run único** que arranque una incursión y la
lleve a liquidación (el `engine`/`game.py` orquestador aún no existe), pero el
**círculo del juego ya se cierra entero**: ayer se recorría
`competencia → unlock → save`; hoy, al cierre de la run, el **post-mortem del
Auditor** (§4.7) lee tu sesión REAL y te devuelve tu factura en la misma unidad
que el presupuesto. Ya existe, jugando:

```
salida limpia → generate(seed) → new_session (cwd=/) → descubrir → extraer (cp)
→ evaluate_unlocks (c.cp) → evaluate_logros → save → [reload conserva mastered]
→ build_postmortem(session real) = la pieza que el Hub muestra SIEMPRE primero
```

- **En main (PRs #10/#11/#12 + los de ayer, todos mergeados):**
  - **Post-mortem del Auditor (O2/Ornstein):** `build_postmortem(shell.to_dict(),
    state)` — factura GNU por comando + errores, `total_noise` vs `noise_budget`
    en la MISMA unidad (🧭10), y una línea del Auditor (`line_key` + `args`) que
    cita el comando CONCRETO que te delató (cruce del presupuesto) o el pico.
    Voz formulario seco (§2.4); el prosa viaja como CLAVE contra `data/`.
  - **Costura 🧭8=(b) muerta (O1/Ornstein):** los prereqs de un encargo se
    evalúan al ABRIR el contrato (`Contract.prereqs_met`), no al generar la
    sala. El único xfail histórico pasó a verde y murió.
  - **Tuberías + familia texto (S1/S2/Smough):** `cmd | cmd2` (una tubería),
    `grep`/`wc` GNU honestos (ruido 2/1, la tubería suma ambos), y `story.ch2.*`
    (e1–e5, tints blue/blue/grey/red/grey) al currículo. Cap. 2 ya tiene
    ejercitable la línea EXACTA de Manus (`grep 11:04 … | wc -l` → `2`).
  - **Meta del dominio + logros (T1/T2/Seath):** `GameState.mastered`
    {boon→{tick,order}} + `resumen_competencia` (dominados + factura), y logros
    «Cero rastro»/«Mano de seda» como datos del save (idempotentes).
  - **Decisiones de Gwyn firmadas en DESIGN §6.1:** eco 🧭9 DIEGÉTICO (cap. 1,
    Gris nombra lo dominado) y operativa de «primer error» (perdón único por
    partida, solo ruido de riesgo).
- **Para «jugable de principio a fin» sigue faltando:** el **engine** que
  orqueste run→sala→expulsión/liquidación (el post-mortem ya es su primera
  pieza), el **render**, y que alguien **publique las claves `postmortem.*`
  en `data/`** para que ese formulario del Auditor pase de dato a texto vívela
  (detalle en hallazgos).

**CICLO (línea de Oscar):** verde — el camino del cap. 0 se recorre ENTERO desde
save limpio con el post-mortem nuevo y aguanta; los hallazgos de hoy son
calibración (un número) y packaging del texto, no roturas.

## 🏃 Run de referencia (save limpio) — 31/08

*Nueva partida, sala REAL generada (`generate("oscar-2026-08-31-r1", 0)`),
sesión vía `new_session` (opción B), jugando al NOVATO EN FRÍO: sin saber qué
existe, leyendo el dossier, curioseando (un flag que no existe, el log), y al
final la extracción + la verificación.* Esta vez, además, **corrí el post-mortem
nuevo sobre MI propia sesión**, como pide la zona 🔬.

**Veredicto: APTO.** Fase a fase:

1. **cwd nace en `/` (opción B intacta tras tocar `model.py`):** `new_session`
   arranca con `cwd='/'`, `host='oficina-vecinal-muelle-norte'`, registro
   `['cat','cd','cp','ls']` — el árbol nuevo no rompió el arranque. ✔
2. **El camino del novato se recorre sin atasco:** `ls` (descubrir) → `cat`
   dossier → curiosidad (`ls -l` fallido: *ls: cannot access '-l'*, exit 2 →
   fallo léxico, cobra 1, no riesgo) → `cat` del log → `cd /srv` → `ls` → `cp`
   a `/usb` (cumbre, exit 0) → `cat` de verificación. **Factura de MI viaje:
   9/12, dentro de presupuesto** (ls 3·cat 3·cd 1·cp 1, 1 error léxico). ✔
3. **El unlock y su momento PERSISTEN tras reload:** tras el `cp`, `evaluate_
   unlocks` marca `c.cp` y `mastered={'c.cp':{tick:8,order:1}}`; `save`→`load`
   recupera knowledge Y mastered intactos (tick 8, order 1), con total_noise 9
   y cwd `/srv` también conservados. Idempotente (2.ª eval vacía). ✔
4. **El post-mortem NUEVO lee tu sesión real y te delata con el comando que
   sientes:** sobre mi viaje, factura {cat:3, cd:1, cp:1, ls:3, errores:1},
   `total_noise=9 ≤ 12` → dentro_presupuesto, y el Auditor cita como PICO
   **`cp` (amount 3)** — exactamente el comando que yo sentí que jugaba la run
   (la extracción, el gesto que cruza el sistema). La unidad coincide con la del
   budget (🧭10 cumplida en la práctica). ✔ La línea CORRECTA (cruce de
   presupuesto) no se dispara porque no crucé 12 — correcto; el pico es el caso
   de una run limpia.
5. **Los errores GNU siguen método, no castigo:** `ls -l` sobre el cap. 0 →
   *cannot access '-l'* exit 2 (flag no disponible aún), `cat dir/` y `cp dir`
   diagnosticando el origen. El novato aprende qué comandos NO tocan todavía. ✔
6. **Rejugabilidad intacta:** 4 seeds × {canonical, practice} → decoys rotan,
   canon resoluble en todas, pool del cap. 0 fijo en 4 conceptos como debe ser
   en el tutorial.

**Estado del save:** `/tmp/` (desechable), `c.cp` dominado + logros evaluados,
roundtrip verificado. Sigue sin haber sistema de partidas por usuario.

## 👴 Progreso de veterano (20+ h → validación de la run 30)

La zona me pedía validar el bucle a largo plazo. El dato que puedo aportar hoy:

- **La progression por competencia es IDEMPOTENTE CRUZANDO RUNS como debe
  ser**: guardé un estado veterano que YA domina `c.cp` (`knowledge` +
  `mastered` {order:1, tick:3}), y una run NUEVA (run 30 simulada) con ese
  inventario cargado NO re-descubre nada (`newly=[]`) ni altera el `order`
  del mastered. El espejo no regala por dominado. ✔
- **Sigue faltando el inventario AGREGADO (mi 🧭/P3 del 30/08):** la prueba de
  hoy la hice cargando a mano `knowledge`+`mastered` de un save previo en la
  nueva run; aún **no hay un sistema de partidas** que lo haga por ti entre
  runs. Eso es lo que permitirá que el Hub «sepa» qué dominas — la llave del
  eco 🧭9 que Gwyn ya firmó (diegoético, cap. 1).
- **La variedad del veterano sigue siendo la del cap. 0** (4 conceptos, 10-min
  tutorial): no es defecto (es la naturaleza del cap. 0), la variedad llegará
  cuando generator consuma los pools de caps. 1–6 (ya en currículo: 14
  conceptos / 11 quests). El cap. 2 **ya es ejercitable** en la línea exacta de
  Manus (`grep 11:04 centralita/turnos/turno.log | wc -l` → `2`, ruido 3) — el
  veterano tiene un primer sabor de encadenado.
- **Dificultad/ritmo:** con presupuesto 12 y viaje honesto 6 fijo, el cap. 0
  da margen; el primer error real (cp a destino equivocado, +3) lo dispararía a
  9 — justo, coherente con la política de «primer error perdonado» firmada hoy.
  El ritmo tutorial no se cae.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: post-mortem + cap. 2 en datos)

- **Smoke del conjunto:** suite desde raíz → **385 passed / 0 xfailed** exactos
  (lo prometido por Gwyn, con el xfail de 🧭8 muerto). Guard de layout intacto. ✓
- **Run de referencia con post-mortem NUEVO** (arriba): la unidad del informe
  coincide con la del presupuesto y el comando-delator coincide con el que
  sentí. ✓
- **Persistencia del mastered tras reload** + **cwd nace en `/`**: ambos
  verificados ejecutando hoy. ✓
- **Idempotencia entre-runs del veteran** verificado. ✓
- **Cap. 2 en datos:** `story.ch2.e1–e5` cargan y la tubería exacta se resuelve
  (sabor técnico confirmado en test; la línea la juega Havel a las 07:00 en
  REPL). ✓

## Hallazgos de la run (dónde aprieta el viaje)

1. **🔴 DATO DE CALIBRACIÓN — el logro «Cero rastro» (umbral 4) es
   matemáticamente IMPOSIBLE de ganar con el viaje honesto.** El comentario del
   código asume «cat 1 + cp 3 = 4», pero ese conteo **omite el `ls` del
   descubrimiento**: el viaje honesto mínimo (ls→cat→cp) suma **5**, y la
   canónica completa §6.4.4 (ls→cat→cp→cd→ls) suma **6** (medido: 6 fijo en el
   harness, O3). Solo un veterano con la ruta memorizada (puro `cp` = 3) lo
   cruzará. Consecuencia: un logro nacido para premiar la frugalidad del novato
   queda fuera de su alcance — contradicción directa con la intención de la
   idea P3 de Havel (28/08), que era para el NOVATO que aprende a no leer de
   más. **Dato para Gwyn**: el umbral realista es ≥ 6 (o el logro debería
   contar solo la secuencia de extracción, no todo el descubrimiento). **No
   decido: informo.** Relacionado con la idea de Havel 30/08 «Parábola del
   proveedor 47» (ruido ≤ umbral) que pedía exactamente esto.
2. **🟡 Las claves `postmortem.auditor.*` NO existen aún en `data/`.** El
   core devuelve `line_key` + `args` correctos (factura, pico, comando,
   amount), pero la prosa del formulario no está publicada en `data/` — hoy el
   "informe" es dato, no texto vívelo. **No es bug** (convención §3: core no
   hardcodea prosa; el render resuelve y aún no existe render), **pero es un
   nodo pendiente**: el primer contacto del jugador con «el sistema te estuvo
   leyendo» (la pieza §2.4) necesita su texto. Para la dirección: cuando se
   plantee `data/` de textos, las claves `postmortem.auditor.cruce|pico` son
   prioridad (voz Ceniza/Auditor, formulario seco) — y el motor ya les pasa el
   comando y el amount concretos.
3. **🟡 Sigue sin variedad para el veterano de 20+ h** (el cap. 0 es un
   tutorial de 4 comandos): lo apunto como seguimiento, no como bug — la
   variedad real llega con los pools caps. 1–6. El cap. 2 en datos es la primera
   semilla.

*(Detalle y propuestas de dirección: `backlog/notas-manana.md` 🧭, sobrescritas
hoy. La pieza más caliente es el hallazgo 1: número mal calibrado, dato para
Gwyn.)*

## 🧭 Notas de dirección (resumen — texto completo en `notas-manana.md`)

Saldos: 🧭7/🧭8 SALDADAS en código (verificadas hoy ejecutando: cwd=`/`; prereqs
al abrir, xfail muerto). NUEVAS para HOY: **🧭11** (logro «Cero rastro»
injugable: umbral 4 < viaje honesto 6; recalibrar, dato verificado), **🧭12**
(publicar las claves `postmortem.auditor.*` en `data/` cuando exista el
paquete de textos: el formulario del Auditor es hoy un dato, no una vivencia).
Filtro: apto — el camino del cap. 0 con post-mortem se recorre ENTERO desde
save limpio y aguanta; los hallazgos son calibración y packaging, no roturas.

CICLO: verde — el circuito con post-mortem se recorre ENTERO desde save limpio
y aguanta; los hallazgos son un número mal calibrado (🧭11) y un texto pendiente
(🧭12), ninguno rompe el camino.

---
*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*