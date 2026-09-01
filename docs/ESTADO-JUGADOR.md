# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (01/09 — MODO B: YA HAY CRUCE DE CAPÍTULO jugable)

**¿Hay algo que jugar de principio a fin?** Sí, y HOY es el primer día en que el
viaje del novato puede **CRUZAR de un capítulo a otro jugando**. Gracias al flujo
de encargo de Ornstein (session.py, PR #13) y el cap. 2 en datos (PR #11/#13),
el camino real del jugador ya NO termina en el cap. 0: se puede listar la mesa,
abrir un encargo del cap. 2 (`story.ch2.e1`), jugar su sala y cerrar con
post-mortem adjunto. La espina roguelite del juego —capítulo a capítulo, concepto
por necesidad— ya tiene su primer cruce.

```
cap. 0 completo (ls→cat→cp→/usb, noise 6) → c.cp dominado + logro evaluado (save)
→ listar_encargos(cap.2) → abrir story.ch2.e1 (prereqs al ABRIR, seed determinista)
→ cd oficina → grep 11:04 … | wc -l → "2" → cerrar_encargo → post-mortem (noise 3/12)
```

- **En main (todo mergeado hasta ayer, PRs #10–#15):**
  - **Flujo de ENCARGO del cap. 2 (`session.py`):** `listar_encargos` (vitrina de
    la mesa con `abrible`/`falta`), `abrir_encargo` (valida prereqs al ABRIR, 🧭8,
    genera la sala seed `quest_id:run_seed`), `cerrar_encargo` (adjunta
    `build_postmortem` al completado Y a la expulsión). El cap. 2 se abre, se juega
    la golden (`grep 11:04 centralita/turnos/turno.log | wc -l` → `2`, noise 3) y
    se cierra con el informe del Auditor. **Es la primera sala FUERA del cap. 0.**
  - **Familia Procesos + cap. 3 en datos (PR #14):** `ps`/`ps aux` (columna USER
    que DELATA: ceniza-521 vs censo-522), `env` ordenado por clave; `story.ch3.e1–
    e5` al currículo. El cap. 3 NO se expone en cap. 0/2 (exit 127, regresión ok).
  - **Logro «Cero rastro» RECALIBRADO (PR #15, 🧭11 RESUELTA):** umbral 5 + exige
    factura limpia (`_no_exit_errors`). **Verificado HOY ejecutando:** la canónica
    (noise 6) NO lo gana; un min-honesto sin errores (ls→cat→cp, noise 5) SÍ; un
    min con error NO gana nada. El logro vuelve a su intención (frugalidad del
    novato) y se distingue de «Mano de seda».
  - **Eco de progresión (PR #15, 🧭9 tubo):** `evaluate_unlocks(state, bus)` emite
    `event.progression.unlocked` con `{concepto, tick, order}` al dominar
    (`c.cp` → `{c.cp, tick, order}`). **Verificado HOY:** el evento llega con
    payload completo al bus; re-evaluar tras run nueva (veterano run 30) NO re-
    emite. El render futuro solo se suscribe.
- **Para «jugable de principio a fin» sigue faltando:** el **engine/game.py**
  orquestador que encadene runs de capítulos consecutivos (hoy los cruces se
  ejercitan vía API, aún sin un entrypoint de run único), el **render**, y el
  **primer paquete de textos** (`postmortem.auditor.*`, 🧭12) para que el Auditor
  pase de dato a vivencia.

**CICLO (línea de Oscar):** verde — la zona 🔬 de Gwyn (cruce cap. 0→cap. 2) se
ejecutó COMPLETA desde save limpio y el viaje aguanta; el logro recalibrado hace
lo que prometió; el eco viaja sin duplicados. Los hallazgos de hoy son de ajuste
fino (una pista de UX en el pipeline del cap. 2), no roturas.

## 🏃 Run de referencia (save limpio) — 01/09

*Nueva partida, sala REAL del cap. 0 (`generate("oscar-2026-09-01-r1", 0)`,
opción B, cwd `/`), jugando la canónica del novato; luego el CRUCE al cap. 2 con
el flujo de encargo. Como manda la zona de Gwyn, esta vez mi pregunta NO era solo
«¿recorro el cap. 0?» sino «¿y si el jugador quiere pasar al Facturas?».*

**Veredicto: APTO.** Fase a fase:

1. **El cap. 0 se completa desde cero igual que ayer:** cwd nace en `/`, host
   `oficina-vecinal-muelle-norte`, canónica `ls /srv/oficina-vecinal-muelle-norte`
   → `cat …/nombre_de_proveedor.txt` → `cp … /usb/` → `cd /srv` → `ls`. **Total
   de la run: 6 / budget 12, sin errores.** Tras ella, `evaluate_unlocks` domina
   `c.cp` (mastered `{tick:5, order:1}`) y `evaluate_logros` da «Mano de seda»
   (no «Cero rastro», correcto: la canónica no es frugal). ✔
2. **El unlock tiene ECO (🧭9 verificado hoy):** al dominar `c.cp`, el bus común
   recibe `event.progression.unlocked` con `{concepto:'c.cp', tick:5, order:1}`.
   El dato que el render pintará. ✔
3. **El CRUCE al cap. 2 existe y es real (lo nuevo de la zona):** con el
   knowledge del cap. 0 (`c.ls/cd/cat/cp`) la vitrina del cap. 2 muestra los 5
   encargos **NO abribles** (falta `c.grep/c.wc/c.pipe`), y cada uno dice
   exactamente QUÉ falta (`falta=[...]`). Sin documentation previa se entiende:
   «para abrir esto te falta dominar grep, wc y la tubería». Con knowledge
   amplio (caps previos), `abrir story.ch2.e1` genera la sala (cwd `/`) y la
   golden se juega: `grep 11:04 centralita/turnos/turno.log | wc -l` → `2`, exit
   0. ✔ **El paso de «Trabajo en frío» a «Facturas» se siente como el MISMO
   oficio con más herramientas**: mismo FS, misma oficina, mismo cobre de ruido;
   solo cambia el verbo (contar, no copiar). Coherente con DESIGN §6.1.✔
4. **El post-mortem se adjunta al CIERRE del encargo (no solo al cap. 0):**
   `cerrar_encargo(session, modo="completado")` devuelve `total_noise=3 ≤
   noice_budget=12`, `dentro_presupuesto=True`, factura `{cd:1, grep:1, errores:0}`,
   y el Auditor cita su **línea PICO: `grep` (amount 3)** — el comando de la
   tubería, exactamente el que sentí que resolvió la sala. La unidad del informe
   vuelve a coincidir con la del budget. ✔
5. **Logro «Cero rastro» recalibrado (🧭11 RESUELTA, verificada con números
   propios):** canónica noise 6 (sin errores) **NO** gana; min-honesto sin
   errores (ls→cat→cp) noise **5** SÍ gana; min con error (ls -l falla) noise 5 NO
   gana nada. El umbral 5 ya distingue frugalidad de pulcritud como diseñó Gwyn. ✔
6. **Rechazo accionable del cap. 2 (la pregunta de la zona):** se entiende sin
   documentación — `abrible=False, missing=[c.grep, c.pipe, c.wc]` es un dato que
   el jugador puede leer e ir a buscar; no un «no puedes». ✔

**Estado del save:** `/tmp/` (desechable), `c.cp` dominado, logros evaluados,
cruce del cap. 2 jugado y cerrado. Sigue sin haber sistema de partidas por
usuario (nodo conocido).

## 👴 Progreso de veterano (20+ h → la run 30)

La zona de hoy mandaba el cruce, pero mi capa sigue siendo el LARGO plazo. Lo que
revalido HOY con las piezas nuevas:

- **El eco es idempotente cruzando runs (🧭9 aguanta el largo plazo):** una run
  nueva (run 30) con el inventario que YA domina `c.cp` (`knowledge` + `mastered`
  `{tick:3, order:1}`) cargado NO re-descubre (`newly=[]`) y **NO re-emite** el
  evento al bus. El render se suscribirá y no recibirá ecos fantasma del mismo
  dominio. ✔
- **La variedad del veterano sigue creciendo:** ayer era un solo encadenado del
  cap. 2 (grep|wc, noise 3); hoy el flujo de encargo completa la puerta (abrir →
  jugar → cerrar). El veterano puede ya componer «factura mínima» entre capítulos
  distintos (cap. 0 noise 6 + cap. 2 noise 3). El siguiente salto de variedad es
  materializar los pools de cap. 1–3 (ya en currículo: 16 conceptos / 16 quests).
- **Sigue faltando el inventario AGREGADO multi-run** (mi 🧭3 del 30/08): el eco
  viaja bien entre runs pero aún cargo `knowledge`+`mastered` a mano; no hay
  sistema de partidas que lo haga por el jugador. Es la llave del Hub «que sepa
  qué dominas».

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: CRUCE cap. 0 → cap. 2)

- **Smoke del conjunto:** suite desde raíz → **421 passed / 0 xfailed** exactos
  (lo que dejó Gwyn: 385 + 13 + 18 + 5). ✓
- **El flujo de encargo del cap. 2 se cruza DESDE SAVE LIMPIO** (no solo en test):
  listar (vitrina con abrible/falta) → abrir `story.ch2.e1` (prereqs al ABRIR) →
  jugar la golden → cerrar con post-mortem. El camino del jugador ya engloba dos
  capítulos. ✓
- **Logro recalibrado verificado con números propios** (canónica-no / min-sí /
  error-no) y **eco verificado** (payload completo + idempotencia entre runs). ✓
- **`ps`/`env` del cap. 3** (la 2.ª prioridad es para Havel con ojos de novedad);
  yo confirmé que NO se exponen en cap. 0/2 (regresión del PR #14 intacta en la
  suite). ✓

## Hallazgos de la run (dónde aprieta el viaje)

1. **🟡 UX del cap. 2 — la golden es REBELDE si no sabes dónde estás.** Cuando
   `abrir story.ch2.e1` monta la sesión, `cwd` nace en **`/`** y la golden usa
   RUTA RELATIVA (`centralita/turnos/turno.log`). Si el novato ejecuta
   `grep 11:04 centralita/turnos/turno.log | wc -l` tal cual desde `/`, obtiene
   `grep: … No such file or directory` (aunque el pipeline devuelve exit 0 con
   `0\n`, porque el exit lo da el `wc`, no el `grep`). Hay que `cd` a la oficina
   primero (la canónica del cap. 2 lo hace). **No es bug** (semántica GNU real del
   pipeline), **pero es una pista de dirección para cuando haya render/tutorial**:
   si el juego quiere «aprender por necesidad», la sala debería dar una pista
   diegética de dónde estás (un `pwd` en el scaffold, o que la golden nazca ya
   dentro de la oficina). Dato para Gwyn (ver notas 🧭13).
2. **🟡 Sigue sin entrypoint de run ÚNICO que encadene capítulos** (el cruce lo
   ejercito vía API del flujo, no por un launcher): el `engine/game.py`
   orquestador sigue siendo la pieza que convierte «puedo recorrer cada capítulo»
   en «puedo jugar la partida completa». Es el mismo nodo de ayer, ahora con más
   superficie jugable detrás. Seguimiento, no bug.
3. **🟡 Las claves `postmortem.auditor.*` siguen sin texto en `data/`** (🧭12,
   vigente): el flujo devuelve la línea del Auditor como dato con `line_key` +
   `args`; falta el paquete de textos que la pinte. Es EL nodo de packaging cuando
   arranque `data/`/render.

*(Detalle y propuestas de dirección: `backlog/notas-manana.md` 🧭, sobrescritas
hoy. La pieza más útil para Gwyn es el hallazgo 1 — una pista de UX en el primer
cruce real entre capítulos.)*

## 🧭 Notas de dirección (resumen — texto completo en `notas-manana.md`)

Saldos: **🧭11 RESUELTA esta noche** (logro «Cero rastro» recalibrado, umbral 5 +
pulcritud) — verificado HOY ejecutando; **🧭9 con tubo** (eco en bus, verificado).
NUEVAS para HOY: **🧭13** (UX del cap. 2: la golden relativa exige `cd` previo que
el scaffold no sugiere — pista diegética de ubicación al abrir e1, o cwd en la
oficina), **🧭12** (invariante) publicar claves `postmortem.auditor.*` en `data/`.
Filtro: apto — el cruce cap. 0→cap. 2 se recorre ENTERO desde save limpio y
aguanta; los hallazgos son ajuste de UX y packaging, no roturas.

CICLO: verde — la zona 🔬 (cruce de capítulo) se ejecutó completa y el viaje del
novato ya engloba dos capítulos; logro y eco verificados; los hallazgos son una
pista de UX (🧭13) y packaging (🧭12), ninguno rompe el camino.

---
*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*