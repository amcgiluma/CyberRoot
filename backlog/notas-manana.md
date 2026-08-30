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

### 👑 Gwyn (30/08, 23:00) — criterio de diseño y dirección para el 31/08

**Trámite:** 3 merges (PR #10 engine → #11 sandbox → #12 meta-ui), suite verificada tras CADA merge: **356 → 374 → 385 passed, 0 xfailed** (deltas declarados cuadrados exactos; el ensayo de Artorias predijo 385/0 y el árbol real lo clavó). Conflictos solo en las 2 huellas previstas, resueltas conservando TODAS las huellas en orden cronológico. Ramas `feat/*` borradas, PRs MERGED en GitHub. Validación de diseño propia: smoke del conjunto (14 conceptos / 11 quests, ch2 tints correctos, `prereqs_met` viva, post-mortem y resumen importables). Sin rechazos.

**Notas de dirección de Oscar (🧭) — resuelta esta noche:**
- **🧭9 (progresión invisible) → VALIDADA y CONVERTIDA EN DECISIÓN.** Oscar tenía razón: el unlock era data muda. Firmado en DESIGN §6.1: el eco será DIEGÉTICO (cap. 1: Gris nombra lo que dominas) con los datos que T1 trajo (`mastered` + momento + `resumen_competencia`). Prohibido el toast de sistema; si algún día hace falta aviso mecánico, será voz del Auditor. Gwyndolin: esta decisión es la PUERTA del cap. 1 — cuando Seath haga render/Hub, el eco ya tiene forma y datos.
- **🧭10 (post-mortem en la misma unidad) → SALDADA.** O2 de Ornstein trae `factura` + `total_noise` vs `noise_budget` en la MISMA unidad; la línea del Auditor va como clave+args (el texto lo resuelve data/). Zona 🔬 de mañana la hace jugar desde save limpio.

**Qué me ha gustado (sabor):**
- **El día que el sistema dejó de prometer y empezó a cumplir.** La costura 🧭8 más vieja del plan murió con un test verde; las tuberías del cap. 2 ejecutan la línea EXACTA de Manus (`grep 11:04 … | wc -l` → `2`) con semántica GNU real; el Auditor puede leerte el HISTORIAL (factura y comando que delata). Diseño §5.2, §2.4 y §6.1 ya son comportamiento.
- **O3 le da a la política 🧭6 su primer dato duro**: viaje honesto = 6 fijo sobre budget 12. Con eso firmé la operativa de «primer error» (perdón único por partida, solo ruido de riesgo cuenta; el 127 léxico nunca activa ni consume el perdón). Escrita en DESIGN §6.1 — ejecutores: se escribe en el motor cuando el cobro de ruido llegue al flujo de sala.
- **Manus sostiene el colchón como el mejor de sus turnos**: fragmento 3 (el contrato a nombre de nadie) y cap. 3 «Bombas» (escalada Umbral→Faro, grieta de Ceniza plantada) — coherentes con H1/H2 y la Lista. El motor narrativo va DOS capítulos por delante del motor de juego: es exactamente el colchón que queríamos.

**Qué NO me ha gustado / corrijo:**
- `UMBRAL_CERO_RASTRO=4` nació descalibrado: está POR DEBAJO del coste honesto (6) — un logro de excelencia que el jugador honesto no puede alcanzar es un logro de consuelo mal diseñado. No lo recalibro a ciegas: la zona 🔬 de mañana pide a Havel la factura mínima alcanzable; con ese dato se re-fija (probablemente 4→5 con «sin errores» como condición extra, o sube a 6). Seath/Ornstein: no lo toquéis sin el dato.
- Las tres ramas tocaron las mismas huellas y los tres merges conflictuaron igual (patrón HEAD `[HECHO]` vs rama `[EN CURSO]`). Ya está fijado en MI prompt (auto-mejora de esta noche: lado HEAD gana, worklog nunca pierde entradas, resolución por script). Coste de la noche: ~3 resoluciones manuales que mañana serán mecánicas.
- [Menor] El bloque de terminal del cap. 2 menciona `sort`/`uniq`/`>` que el sandbox aún no soporta — Manus lo dejó anotado en el propio fichero. Cola natural del cap. 2, no urgente hasta que los encargos ch2 lo pidan.

**Dirección para el plan del 31/08 (mi lectura, por prioridad):**
1. **Puerta del cap. 2 en juego real (Smough)**: los encargos `story.ch2.e1–e5` ya existen en datos — que una sesión pueda ABRIR uno y validarlo (aunque la sala del cap. 2 no se genere aún: contrato→apertura→validación con `prereqs_met`, el flujo que O1 dejó como API). Es el primer encargo FUERA del cap. 0.
2. **Cap. 3 «Bombas» hacia datos (Smough o Seath, según holgura)**: `story.ch3.*` al currículo + `ps`/`env` y el sudo GANADO (nota de Artorias: es un salto de diseño — el sudo se otorga por narrativa, no por contraseña; decidir forma conmigo antes de codearlo).
3. **Eco 🧭9 pre-render (Ornstein)**: nada de UI — un EVENTO de bus `progression.unlocked` (concepto, momento) que el futuro render pinte y que HOY ya permita al REPL anunciarlo como línea del Auditor. Barato, y el cap. 1 de Manus lo conecta.
4. **Recalibrado del umbral «Cero rastro»** cuando Havel traiga la factura mínima (mañana).
5. **Manus mantiene el colchón**: cap. 4 «Troncales» + fragmento 4 ya en su plan de madrugada. El ssh/scp de «Troncales» avisa: el sandbox necesitará red simulada — que Gwyndolin lo planifique como tarea propia, no como apunte.

**Ideas propias (recámara, no para el plan de mañana):**
- La factura del post-mortem puede volverse OBJETO de historia: que Gris te la pida («enséñame cómo entraste») y el juego valide que tu propio informe coincide con el save — el jugador que mintió en su factura se delata solo. H1/H2 lo sostienen.
- Los logros como líneas que el Auditor TE ESCRIBE en el Hub cuando exista: «Mano de seda» no es una medalla, es una anotación fría en tu expediente. §7.6 sin traicionar el formulario §2.4.
- El `resumen_competencia` con factura es la SEMILLA del ranking interno de runs (ruido más bajo con más encargos) — solo si algún día Juanma pide puntuación; la REGLA DURA §4.2 prohíbe que el grind compita con la competencia.

*(Fin de la entrada de Gwyn — Gwyndolin consume esta sección a las 11:00.)*
