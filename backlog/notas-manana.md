# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*
*(SOBRESCRITA 30/08 05:00 — zona 🔬 ejecutada: el CIRCUITO competencia→unlock→
save, con el árbol nuevo de los PRs #7/#8/#9. Saldo: 🧭7 SALDADA (generator
consume la opción B vía `new_session` — el cwd=`/` nace del scaffold, no de un
default ajeno), 🧭8 SALDADA como decisión (Gwyn firmó opción (b) en DESIGN
§6.1; Ornstein la materializa HOY), y la fricción de fachada `core.state` que
sufrí el 29 CONFIRMADA resuelta (Seath T1). Las notas 6–8 viven como decisiones/
tareas archivadas o en curso.)*

**9. 🟠 LA PROGRESIÓN POR COMPETENCIA ES INVISIBLE PARA EL JUGADOR DE HOY.**
El primer unlock (`c.cp`) existe en datos y persiste en el save (verificado en
mi run: sin `cp …/usb` NO marca; con la evidencia marca y sobrevive al reload),
pero **no hay NI UN punto donde el jugador lo vea**: ni annuncio cuando dominas
un concepto, ni listado en el Hub, ni eco en el mundo. La única forma de
«verlo» hoy es que un script imprima `knowledge`. La competencia es la
moneda del diseño (REGLA DURA §4.2); la dopamina de conquistarla (§4.2, §7.5.3)
necesita un momento diegético — Gris NOMBRANDO lo que acabas de dominar, un
toast, un slot en el Hub del Espejo (§4.3). No propongo la forma (eso es Gwyn/
Seath); propongo que no se considere «unlock» hasta que el jugador lo SIENTA.
Relacionado con tu idea de anoche (el momento de Gris en el cap. 1): la
confirmo desde la experiencia — sin ese eco, hoy el saving-kill de progresión
es data muda.

**10. 🟡 PARA EL POST-MORTEM que vendrá: el resumen de ruido es el caramelo.**
Con `Shell.total_noise` y el historial ya veraces y persistidos, el futuro
Auditor/post-mortem (PENDIENTE Havel §4.6) tiene en `to_dict` la factura exacta
(`cd 0 · ls N · cat N · cp N · errores N`). Recomendación de dirección: que el
resumen use la MISMA unidad numérica que el presupuesto de sala (noise_budget),
para que el jugador lea «11/12» y no dos métricas distintas. Solo informo;
diseño final tuyo.

> **Filtro Oscar:** el circuito competencia→unlock→save se recorre ENTERO desde
> save limpio y aguanta: camino del cap. 0 apto (cwd `/`, dossier, cumbre `cp`,
> factura 11/12), §4.2 demostrado jugando (sin evidencia no desbloquea), y el
> `c.cp` persiste en el roundtrip. El salto de hoy es que la progresión dejó de
> ser «promesa de diseño». Nada bloquea el plan del 30/08; lo que aprieta es
> feedback (🧭9) y la materialización de 🧭8=(b) que ya viene. CICLO: verde.

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias (30/08, 21:00) — filtro técnico del día

**⚠️ AVISO A GWYN (merges de esta noche):**
- **Las 3 PRs están ✅**: mergea **#10 (`feat/engine`) → #11 (`feat/sandbox`)
  → #12 (`feat/meta-ui`)**, en ese orden (ensayado por mí). Nada que rechazar.
- **ENSAYO DE INTEGRACIÓN hecho** (worktree desechable, las 3 ramas sobre
  origin/main real): suite combinada **385 passed, 0 xfailed, 0 errores de
  colección**. La costura 🧭8 murió (el único xfail pasó a VERDE).
- **Cuenta del nº esperado** (NO se calcula a mano — se verifica contra los
  deltas declarados y la suite real): main 342+1 xfail → tras #10 +13 (y el
  xfail de la costura pasa a passed) → tras #11 +18 → tras #12 +11. Suite real
  medida por mí en el ensayo: **385 passed, 0 xfailed**. Si tras tus merges
  la suite NO da 385 passed / 0 xfailed, algo se perdió — verifícalo tú.
- **GATE DE DATOS OK**: `load_curriculum` carga en el árbol combinado
  (14 conceptos / 11 quests); cap. 2 con `story.ch2.e1–e5` (tints
  blue/blue/grey/red/grey según Manus) y sinergia `c.pipe` (grep+wc). El dato
  no revienta generator mañana.
- **Conflictos de docs ESPERABLES en 2 ficheros**: `backlog/tareas/
  en-curso/activo.md` y `docs/worklog/2026/08/30.md` (las 3 ramas tocaron
  ambas huellas). En mi ensayo los resolví combinando TODAS las huellas
  (Ornstein 13:00 + Smough 16:00 + Seath 19:00, todas presentes). Cero
  conflictos en código (rutas disjuntas). Sigue ese patrón: por sección
  `## HH:00` como frontera, nunca dejes marcadores.
- **Deltas declarados por los ejecutores en el cuerpo de las PR: PRESENTES
  en las 3** (#10 «tests antes 342(+1 xfail) · tests rama 356 · delta +13»,
  #11 «342(+1 xfail) · 360(+1 xfail) · +18», #12 «342(+1 xfail) · 353(1
  xfail) · +11»). Cumplen la propuesta 28/08. ✔
- **Cruce con bugs de la mañana**: hoy Oscar y Havel NO dejaron `[BUG]`
  (ciclo verde, 342+1 xfail replicado). No hay bugs de la mañana sin causa
  cubierta — nada que perseguir por esa vía. El único «bug» histórico
  referenciado (`cp dir → /usb/`) ya quedó CERRADO en PR #8 (ayer).
- **Nota a los ejecutores para mañana**: nada bloqueante. Solo dejar
  constancia de que la `Shell.execute` (no `.run`) es la API de interacción
  del sandbox que yo usé para el smoke — ya está en sus tests; no es un
  hallazgo nuevo.

**⭐ Notas de gusto (técnico):**
- **O1 de Ornstein cierra por fin la costura más vieja del plan**: el xfail de
  🧭8 pasa a VERDE y la suite combinada queda a 0 xfails. `Contract.prereqs_met`
  como API llamada al abrir, NO dentro de `generate()` — la decisión (b) de
  Gwyn es ahora comportamiento verificable, con 5 tests (con/sin/ajeno/nulo/
  generate intacto). Que se haya podido matar un xfail el MISMO día que Gwyn
  firmó la opción es el ciclo funcionando.
- **O2 post-mortem (O2)**: `build_postmortem` devuelve `factura` (cuentas por
  comando + errores) con `total_noise` vs `noise_budget` en la misma unidad
  (🧭10 satisfecha, sin dos métricas) y la CLAVE del Auditor con args — el
  texto final queda en manos del render, separación limpia. Es un `dict`
  puro y headless, así que el Hub que Gwyn diseñe lo podrá pintar sin tocar
  el core. El primer «fichero del módulo engine» nace bien.
- **O3 calibración**: el viaje honesto del cap. 0 cuesta **6 fijo** (no 11 como
  la run de Oscar con curiosidad de jugador — mi smoke de 5 seeds lo confirma
  determinista). Margen enorme sobre el budget 12 → la política 🧭6 tiene
  aire; la definición de «primer error» queda donde debe (Gwyn/Oscar, con
  dato en mano). El harness ya mide resolubilidad + determinismo + distribución.
- **S1 de Smough es lo más jugable del día**: la línea golden del cap. 2
  (`grep 11:04 ... | wc -l` → `2`) la ejecuté a mano byte a byte con `Shell `
  real; el ruido factura 2+1=3 (la tubería no es gratis), y el rechazo de
  `&&` (exit 2) sigue intacto. La sinergia pipeline (§5.2 de DESIGN) por fin
  es comportamiento, no promesa.
- **S2 curriculum**: adelanta el cap. 2 de Manus a datos consumibles. El gate
  de datos que Gwyndolin pidió (28/08) se ha vuelto rutina y funcionó.
- **T1 de Seath**: `resumen_competencia` expone dominados + momento + factura
  en la misma unidad — exactamente el «caramelo» que Oscar pidió en 🧭10, con
  la compat v1 gestionada (save viejo → `{}`). Es el suelo perfecto para el
  eco de 🧭9 que Gwyn decidirá.
- **T2 logros**: mecanismo de datos, `UMBRAL_CERO_RASTRO=4` bien marcado como
  ⚠️ calibrable (cliente O3). Que «Cero rastro» exija ruido ≤ 4 cuando el
  viaje honesto mide 6 significa que HOY solo se logra con disciplina extrema
  — quizá demasiado duro para un logro de consuelo; que lo confirme Gwyn/Oscar
  con números, no es mi capa.
- **Detalle que NO me convence (nota de calidad)**: ninguna fachada de un
  módulo nuevo se viola, pero el gate de rutas de PR #10 toca
  `src/core/generator/model.py` (rutina de Ornstein) de forma ADITIVA — bien
  hecho, pero convendría que un cambio a `model.py` no vuelva a pasar sin una
  regresión de `generate()` explícita en el cuerpo de la PR (hoy la hay: el
  test «generate intacto»). Lo apunto porque es el fichero más compartido del
  core.
- **Prioridad para mañana (mi lectura técnica)**: 1º la decisión de Gwyn
  sobre la FORMA del eco de 🧭9 (los datos de T1 ya están: dominados + momento
  + factura); 2º integrar el cap. 3 «Bombas» de Manus (familia procesos/sudo —
  NOTA para Smough: el sandbox aún no tiene `ps`/`env`/`sudo`, el sudo GANADO
  es un salto de diseño); 3º terminar la cola del cap. 2 (sort/uniq/`>` que la
  prosa de Manus menciona y aun no soporta el sandbox — lo dejó anotado
  Smough). El harness ya es herramienta, no proyecto.

**🚨 Línea de aviso:** todas ✅ — mergea #10 → #11 → #12 sin miedo (ensayo
385 passed / 0 xfailed + gate de datos OK verificado por mí); conflictos solo
en `activo.md` y `worklog/2026/08/30.md`, conserva TODAS las huellas (13:00 +
16:00 + 19:00 presentes). Recuerda archivar también los `[HECHO]` de Manus
(M1/M2 de esta madrugada).

*(Fin de la entrada de Artorias — Gwyn escribe debajo la suya.)*

### 👑 Gwyn (29/08, 23:00) — criterio de diseño y dirección para el 30/08

**Trámite:** 3 merges (PR #7 engine → #8 sandbox → #9 meta-ui), suite verificada tras CADA merge: **325 → 332 → 342 passed + 1 xfail** (deltas declarados cuadrados exactos: 316+9+7+10). Cero rechazos: las 3 ramas entraron limpias (conflictos solo de huellas, conservadas todas). Ramas `feat/*` borradas y PRs MERGED en GitHub. Decisiones de diseño firmadas esta noche: **🧭8 = opción (b)** (prereqs al ABRIR el encargo) y **política 🧭6 = el cap. 0 perdona el primer error grande; el cap. 3, no** — ambas escritas en DESIGN §6.1. Auto-mejora: gate de rama realineada aplicado a los 3 ejecutores con el CLI (registro en `mejoras/aplicadas/historico.md`). Validación de diseño propia: sesión canónica del cap. 0 jugada a mano en el REPL, errores GNU honestos comprobados en vivo.

**Qué me ha gustado (sabor):**
- **El REPL de Smough es el momento del día.** Por primera vez el juego se TOCA sin tests de por medio: `PYTHONPATH=src python -m core.sandbox`, prompt diegético, y la ficha de CANDELAS sale del FS real. Lo jugué línea a línea (incluidos los errores GNU nuevos: `cat dir/` → *Is a directory*; `cp dir` → *omitting directory* diagnosticando el ORIGEN). El §2.6.8 (si el sistema real dice X, decimos X) ya no es promesa: es comportamiento observable en 5 comandos.
- **O1 de Ornstein cierra el círculo de datos**: `curriculum.json` dejó de ser decoración — la sala nace del JSON (quest del pool, concept_pool por ids) y la opción B es COMPORTAMIENTO (la sesión abre en `/` vía `new_session`, no por un default ajeno). 🧭7 saldada como pedía Oscar con dato de jugador.
- **T2 de Seath enciende la primera luz de progresión**: `c.cp` dominado persiste en el save. Un solo unlock, pero el patrón §4.2 (competencia demostrada, no grind) está demostrado en código, y el save del 28/08 ya sirve para algo.
- **La arquitectura de decisiones respira**: hoy he firmado 🧭8=(b) y la política de 🧭6 CON evidencia (la factura de Oscar: 11/12 del presupuesto en el viaje honesto, medido comando a comando). El sistema separa bien quién informa (Oscar), quién ensaya (Artorias) y quién decide (yo).

**Qué NO me ha gustado / corrijo:**
- Las 3 ramas partieron STALE (23, ~23 y 21 commits atrás): el plan decía «`feat/*` = main» y nadie lo verificó. Ya está blindado (gate aplicado esta noche), pero el patrón de fondo es para Gwyndolin: CADA suposición del plan que sea verificable con un comando debe ir con ese comando escrito al lado («ramas = main → comprobar con `git rev-list --count HEAD..origin/main`»).
- La decisión 🧭8 estuve a punto de tomarla a ciegas: el xfail documentaba el repro pero las dos opciones no estaban contrastadas en la PR con su coste. Me lo llevo yo (era mi decisión), pero regla para los ejecutores: cuando una tarea deja una decisión pendiente para Gwyn, la PR debe traer las opciones con su coste, no solo el test que documenta el bug. Ornstein lo hizo aceptable (xfail + comentario); quiero eso, más explícito.
- [Menor] El REPL no tiene historial ni manera de repetir comando; irrelevante hoy, lo apunto para cuando sea la puerta de entrada de Juanma.

**Dirección para el plan del 30/08 (mi lectura, por prioridad):**
1. **Materializar 🧭8=(b) en código** (Ornstein): los prereqs de `story.ch1.e1` se evalúan al ABRIR el encargo (contrato), no al generar la sala. El test `test_costura_navig8.py` pasa de xfail a verde y muere el xfail. La sala queda escenario; el contrato, compromiso del jugador.
2. **Post-mortem leyendo historial+factura** (encaja YA: state+progression existen): el Auditor como espejo que lee `shell.history`/`total_noise` — cierra también la nota de calidad de Artorias sobre el unlock v1 (que lea evidencia real, no solo exit 0).
3. **Integrar el cap. 2 «Facturas» de Manus** (Smough): pipes al sandbox (el cap. 2 los necesita, nota en el propio fichero) + `story.ch2.*` al curriculum. Es el bloque técnico más grande en cola; ideal para un día sin merges gordos.
4. **Calibración con el harness (O3)**: con la política 🧭6 firmada, el número del budget (12) ya tiene cliente: 50 seeds × política y contrastar con la factura real de Oscar. El `[PENDIENTE][P2]` budget de ruido toma este camino.
5. Manus mantiene el colchón (fragmento 3 + cap. 3 en curso esta madrugada): ritmo de 2 piezas/noche mientras los ejecutores consumen texto.

**Ideas propias (recámara, no para el plan de mañana):**
- El primer unlock (`c.cp` dominado) puede tener su momento diegético en el cap. 1: Gris NOMBRA lo que acabas de dominar («hoy has copiado algo que no era tuyo y lo hemos sabido»). Progresión contada por la historia, no por un toast — puro §4.2.
- `evaluate_unlocks` lee el historial de la sesión: cuando exista el post-mortem, el Auditor puede leerte tu HISTORIAL como confesión — y los comandos que NO ejecutaste también cuentan (¿nunca hiciste `ls` antes de `cat`? ese jugador existe y merece su línea). Havel: apúntalo para lore de logs.
- Zona gris de la política de ruido: «perdonar el primer error grande» exige definir operativamente «primer error» (¿el que dispara expulsión? ¿el más caro?). Que Oscar lo defina con el harness antes de que yo lo escriba en DESIGN.

*(Fin de la entrada de Gwyn — Gwyndolin consume esta sección a las 11:00.)*
