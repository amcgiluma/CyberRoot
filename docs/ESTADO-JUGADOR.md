# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (02/09 — MODO B: ya hay build jugable y CRUCE de capítulos)

**¿Hay algo que jugar de principio a fin?** Sí, y hoy el viaje del novato ya
engloba **tres capítulos** de superficie jugable real: el cap. 0 («Trabajo en
frío») se completa desde cero, se puede **cruzar al cap. 2** («Facturas») con el
flujo de encargo jugando la golden, y el **cap. 3 («Bombas») ya tiene en main el
`sudo` GANADO** (la credencial narrativa del mundo) con la **primera VOZ del
juego**: el Auditor resuelve a texto formulario en `data/`. Esta es la zona 🔬 de
Gwyn que mando hoy y que Havel continuará a las 07:00 con ojos de novedad.

**En main (todo mergeado hasta anoche, PRs #17/#18; #16 retenido por Ornstein):**
- **Sudo GANADO (S1, cap. 3, DESIGN §6.1):** `sudo` es una **credencial narrativa
  como FICHERO del mundo** (`/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt`,
  marcador `AUTORIZACION: CENIZA`), nunca una contraseña tecleada. Sin credencial
  → rechazo diegético accionable (nombra qué falta y dónde), exit 1, **ruido 0**
  (intentar no es delinquir). Con credencial → `sudo <cmd>` ejecuta el comando
  envuelto, factura **ruido PREMIUM** (base + premium) y **deja FIRMA en
  `/var/log/auth.log`** (usuario, comando, tick): el poder deja factura, y la
  columna que delata es la de `ps aux`. Gate por capítulo: cap. 0/2 no exponen
  `sudo`/`ps` → exit 127 (la puerta sigue cerrada donde debe).
- **Primera VOZ del juego (T1, textos 🧭12):** `src/data/textos.json` +
  `textos.py` (resolvedor) dan prosa a `postmortem.auditor.cruce|pico` con la voz
  formulario del Auditor (§2.4: «Expediente 000: … Continuidad del ensayo:
  estable») y a los `title_key`/`beat_key` del cap. 1; cobertura que falla si
  falta una clave.
- **Familia conteo (S2, cap. 6):** `head`/`tail`/`sort`/`uniq` GNU-honestos
  (lectura frugal) — la barrera técnica hacia el cap. 6 «Faro».
- **Cap. 5 en datos (T2):** `story.ch5.e1–e4` al currículo (tints de Manus).
- **Cap. 2 cruce + post-mortem (días previos):** `listar_encargos`/`abrir_encargo`/
  `cerrar_encargo`; el cierre adjunta `build_postmortem` y **resuelve a texto**.
- Gate de datos: **21 conceptos / 20 quests**.

**Para «jugable de principio a fin» sigue faltando:** el **engine/game.py**
orquestador que encadene runs de capítulos consecutivos en un entrypoint único
(se sigue ejercitando vía API/flujo), el **render**, y que la **sala del cap. 3
sea generable por el generator real** (PR #16 retenido: fix de 2 tests stale de
Ornstein; hoy la ejercité montando el FS como `_fs_sala_sudo()`).

**CICLO (línea de Oscar):** verde — la zona 🔬 (sudo GANADO + primera voz del
Auditor) se ejecutó COMPLETA desde estado limpio y el camino aguanta: el sudo
eleva/firma/factura como diseñó Gwyn, la voz resuelve con la forma exacta, el
gate 127 del cap. 0/2 sigue cerrado, y el post-mortem del cierre del cap. 2 pinta
texto. **Tomé además UNA decisión pendiente de dirección para Gwyn** (🧭14: si el
sudo debe exigir LEER la llave, no solo que exista), no una rotura — el viaje
sigue verde.

## 🏃 Run de referencia (estado limpio) — 02/09

*Nueva "partida", sala sudo del cap. 3 montada como `_fs_sala_sudo()` (la que
deja el PR #16 retenido; mientras lo arregla Ornstein la ejercito con el FS de
su test), a la que añadí la primera VOZ del Auditor con `data.textos`. Como manda
la zona 🔬 de Gwyn, pegué el recorrido que haría un jugador real: primero INTENTO
`sudo` sin la llave, luego la encuentro/leo y la uso, y compruebo que el juego me
dice la verdad en todas las esquinas.*

**Veredicto: APTO (con un matiz de dirección que dejo para Gwyn, no bloqueante).**
Fase a fase:

1. **La primera VOZ resuelve con la forma exacta (§2.4):**
   `resolve('postmortem.auditor.pico', {command:'sort turnos.log', amount:'9'})`
   → *«Expediente 000: se mantiene dentro del presupuesto. Pico de la sesión:
   sort turnos.log (9 puntos). Continuidad del ensayo: estable.»* Tanto el `pico`
   como el `cruce` cargan el dato sobre emoción (`{command}`/`{amount}`), el sello
   «continuidad del ensayo: estable» remata cada uno. El sistema que te lee,
   habla. ✔
2. **El post-mortem del cierre del cap. 2 pinta TEXTO, no `line_key` crudo:** en
   una sesión cap. 2 (`grep 11:04 … | wc -l`, noise 3/12), `build_postmortem`
   emite `{line_key: postmortem.auditor.pico, args:{command:grep, amount:3, …}}` y
   `resolve(...)` lo convierte en la línea del expediente. La cadena
   motor(→clave+args)→datos(→texto) cierra el eco 🧭12: el jugador LEERÁ al
   Auditor HOY, no cuando haya UI. ✔
3. **El sudo con la llave funciona como diseñó Gwyn:** `cat` de la orden (ruido
   1, leo alcance/firma) → `sudo cat` eleva, factura **base+premium (1+3=4)** y
   deja firma `tick 0 operator : sudo cat …` **appendeando** al auth.log (no lo
   sobrescribe). Un segundo `sudo` deja una segunda firma (reutilizar la llave no
   borra la factura). El roundtrip del save conserva credencial y firma. El
   contrato «el poder deja factura» ES cierto en el árbol. ✔
4. **El gate 127 sigue cerrado donde debe:** `sudo` y `ps` en una sesión del
   cap. 0 y `sudo` en el cap. 2 → `exit 127: sh: command not found` — la puerta
   del cap. 3 no se abre antes de tiempo. ✔

## 🟡 Hallazgo de la run (matiz de dirección para Gwyn — no rompe el camino)

**El `sudo` no exige GANAR/LEER la llave: exige que el fichero-credencial EXISTA
en el mundo.** El gate del sandbox es `check_credential(fs, cwd)` (`shell.py`
L216): comprueba la ruta convencional (`SUDO_CREDENTIAL_PATH`) **y el marcador de
contenido**, pero **no rastrea que el jugador la haya leído** (`cat` no queda
marcado en la sesión como «credencial obtenida»). Consecuencia, medida ejecutando
HOY: en la sala sudo donde el fichero está presente, ejecutar `sudo cat …` **sin
haberlo leído antes** eleva, firma y factura igualmente (exit 0, ruido 4). La
premisa de la zona «(a) `sudo` SIN leer la credencial → rechazo» **solo se
reproduce en un FS sin credencial** (el caso `test_sin_leer_llave...`), no en la
sala con la llave presente. Leído con la silla del novato: si el generator
coloca la credencial en el mundo (y la expone `sudo` en el cap. 3), el momento de
**«ganarse» la llave leyéndola se vuelve cosmético** — el jugador puede `sudo` en
cuanto el fichero está, sin leer la orden (y sin aprender su alcance). Detalle y
decisión a Gwyn en `notas-manana.md` (🧭14). **No es un bug que rompa nada** — la
suite está en 466/0 y el circuito verificado funciona; es una decisión de
**fidelidad pedagógica** («leer para ganar» vs «la llave vive en el mundo»).

## 👴 Progreso de veterano (20+ h → la run 30)

La zona de hoy mandaba el circuito del cap. 3; mi capa larga sigue siendo el
largo plazo. Revalido HOY con las piezas nuevas:

- **La primera voz aguanta la repetición (vista como veterano):** la plantilla
  del Auditor (`line_key`+`args`) quiere decir que la VOZ se reutiliza con datos
  distintos por run; un veterano en la run 30 verá la forma «Expediente 000» una
  y otra vez pero con el comando/amount de SU sesión concreta. Eso es exactamente
  el efecto §5.3 (textos por clase de evento, no por run única): la variedad vive
  en los datos. Correcto, no repetitivo.
- **El sudo como verbo del veterano:** a largo plazo el gate por EXISTENCIA (mi
  hallazgo 🧭14) es bueno para el veterano (cero fricción para reutilizar la
  llave) y matiz para el novato (se pierde el beat de «ganar» la llave). Si Gwyn
  exige la lectura, el veterano la tiene trivial; si no, el novato pierde una
  lección de alcance. La decisión de dirección debería pesar más la PROGRESIÓN
  inicial (cap. 3 es el primer contacto real con el poder) que la comodidad del
  veterano.
- **La familia conteo es el alfabeto del cap. 6 (se mantiene):** los `sort/uniq/
  head/tail` recién mergeados son la barrera técnica hacia el Faro; con la
  worldbuilding del censo de Manus (M1, esta madrugada) las salas-dato tienen
  DATO real que contar. La progresión cap. 3→6 por competencia acumulada sigue
  coherente.
- **Sigue faltando el inventario AGREGADO multi-run** (mi 🧭3 del 30/08): no hay
  sistema de partidas que «sepa qué dominas» cruzando runs. Sigue siendo la llave
  del Hub.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: sudo GANADO + primera VOZ)

- **Smoke del conjunto:** suite desde raíz → **466 passed / 0 xfailed** exactos
  (lo que dejó Gwyn: 455 + 11 = 466). ✓
- **Primera VOZ verificada en vivo** (`resolve` con los args reales del
  post-mortem): forma formulario exacta, sello «continuidad» presente. ✓
- **Circuito sudo recorrido ENTERO desde estado limpio:** rechazo (solo-intento)
  → leer llave → sudo eleva + premium + firma en auth.log (append) → segundo uso
  re-firma → roundtrip conserva. ✓ (Con su matiz 🧭14, abajo.)
- **Post-mortem del cierre del cap. 2 resuelve a TEXTO** (no `line_key` crudo):
  claves `postmortem.auditor.pico` con `{command, amount}` pueblan la forma. ✓
- **Gate 127 cap. 0/2:** `sudo`/`ps` fuera del set → exit 127 (puerta cerrada). ✓

## Hallazgos de la run (dónde aprieta el viaje)

1. **🟡🧭14 — El `sudo` se gana por EXISTENCIA de la llave, no por LEERLA.**
   Con la credencial presente, `sudo cat …` ejecutado sin haberla leído eleva y
   firma (medido HOY: exit 0, ruido 4). El beat de «ganarse» la llave (§6.1:
   «credencial robada u objeto de estado… se lee con cat») no está ENFORZADO en
   el sandbox. Decisión de dirección para Gwyn (informo, no decido): (a) aceptar
   v0 («la llave vive en el mundo; leerla es sabor»), o (b) exigir la lectura
   (marcar la credencial como obtenida en la sesión antes de permitir `sudo`).
2. **🟡 Sigue sin entrypoint de run ÚNICO que encadene capítulos** (el cruce se
   ejercita vía API/flujo, no por un launcher): `engine/game.py` sigue siendo la
   pieza que convierte «puedo recorrer cada capítulo» en «partida completa».
   Seguimiento, no bug.
3. **🟡 La sala del cap. 3 no es aún generable desde main** (PR #16 retenido): la
   ejercité con el FS de `_fs_sala_sudo()`. Cuando Ornstein fusione el fix, la
   zona deberá re-jugarse sobre el generator real (relevo para Havel/días
   siguientes). Seguimiento, no bug.

*(Detalle y propuestas de dirección: `backlog/notas-manana.md` 🧭, sobrescritas
hoy. La pieza más útil para Gwyn es el hallazgo 1 — una decisión de gate del
primer «poder» real del juego.)*

## 🧭 Notas de dirección (resumen — texto completo en `notas-manana.md`)

Saldo: **🧭12 RESUELTA esta noche** (T1: claves `postmortem.auditor.*` en `data/`
con resolvedor, verificada HOY resolviendo); **🧭13 RESUELTA** (Gwyn la validó
anoche con decisión: cwd en la oficina + prompt con ruta al meter render);
**🧭9 con tubo** (eco en bus, idempotente). NUEVA para HOY: **🧭14** (decisión de
gate del sudo: ¿exigir LEER la llave, o basta con que exista? — medido que hoy el
`sudo` eleva sin leerla). Filtro: apto — el circuito sudo y la primera voz se
recorren desde estado limpio y aguantan; el hallazgo es una decisión de
fidelidad pedagógica, no una rotura.

CICLO: verde — la zona 🔬 (sudo GANADO + primera VOZ) se ejecutó completa y el
viaje del novato suma el cap. 3 con su primer «poder» de verdad; la voz resuelve
con la forma exacta; el gate 127 aguanta; los hallazgos son una decisión de gate
(🧭14) y packaging/entrypoint (seguimiento), ninguno rompe el camino.

---
*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*