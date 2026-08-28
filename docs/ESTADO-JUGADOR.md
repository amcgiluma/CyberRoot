# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (28/08 — MODO B parcial: primer código, proxy headless)

**¿Hay algo que jugar de principio a fin?** AÚN NO — pero por primera vez hay un
trozo de juego REAL que se puede ejercitar:

- **MERGEADO en main:** sandbox del cap. 0 (PR #2): FS virtual + shell con
  `ls`/`cd`/`cat`/`cp` (set por defecto, 🧭1 aplicada), semántica GNU verificada
  contra coreutils reales, ruido por comando (cd 0 / ls 1 / cat 1 / cp 3),
  sesión serializable ida-y-vuelta, determinismo entre procesos
  (PYTHONHASHSEED distinto → salida byte a byte idéntica).
- **NO hay build jugable** en sentido estricto: ni `python -m core` ni REPL
  interactivo ni harness (`tools/harness/` no existe). Hoy el «jugable» se
  ejercita vía pytest o construyendo la sesión en Python (así hice la run de
  referencia de abajo).
- **Primera pieza visual commitada:** fuente bitmap 5×7 CP437 + 3 capturas
  golden (las regeneré hoy: byte a byte estables, sha256 sin cambios ✓). El
  juicio de SABOR CRT es capa de Havel (07:00).
- **Para «jugable de principio a fin» falta:** engine (runs/salas/detección),
  generator, curriculum.json, state/saves, progression/karma, render. Hoy el
  juego es UNA sesión de terminal sin objetivo mecánico todavía.

## 🏃 Run de referencia (save limpio) — 28/08

*(No existe save: la run de hoy es una SIMULACIÓN del novato de cero sobre la
piel exacta de la escena técnica de `CAPITULOS/00-la-firma.md` — 29 líneas
tecleadas en 4 fases. La secuencia canónica ya la cubren los tests; yo jugué el
viaje completo: desorientación, extracción, curiosidad y errores.)*

**Veredicto: el viaje aguanta de `ls` a `cp`.** Fase a fase:

1. **Desorientación → lectura (NOVATO OK):** la raíz muestra `srv` y `usb`
   (el destino del botín se ve antes de saber qué buscar); `cd` + `ls` navegan
   sin fricción; `cat` devuelve el contenido tal cual. Los tres comandos
   aparecen por necesidad real, no por cuestionario.
2. **Extracción (OK con matiz):** `cp nombre_de_proveedor.txt /usb` funciona
   (con o sin barra final) y `cat /usb/...` confirma el botín: el momento
   cumbre del cap. 0 SE PUEDE COMPLETAR. Matiz: si el jugador sigue la secuencia
   canónica (que acaba en `cd /srv`), el nombre relativo del dossier YA NO
   resuelve desde ahí (verificado: «cp: cannot stat 'nombre_de_proveedor.txt'»).
   Primera rozadura de andamiaje → 🧭2 para Gwyn (cwd inicial / qué significa
   mecánicamente «run guiada»).
3. **Curiosidad (rozaduras menores):** `help` y `pwd` no existen (127 sin
   pista; el `pwd` ya está propuesto por Havel como idea P3); `ls -l` trata el
   flag como fichero («cannot access '-l'») — GNU-honesto pero sin insinuar que
   los flags llegan después. `cd` sin args vuelve a la raíz (home=/): bien.
4. **Errores (lo mejor y lo peor del sandbox):** los mensajes de `cp`/`cat` son
   GNU reales y honestos (missing operand, same file, Is a directory) —
   excelente para enseñar Linux de verdad. Lo peor: `&&` y `;` producen errores
   que culpan al comando equivocado («cd: too many arguments») en vez del
   rechazo didáctico que el shell YA aplica a pipes/globs → `[BUG][P2]` filed.

**Estado del save al terminar: no existe sistema de saves** (es el módulo
`state` de Seath, pendiente).

## 👴 Progreso de veterano (save 20+ horas)

Sin cambios respecto al 27/08: no hay progresión, karma, unlocks ni economía en
código. La evaluación en papel (3 fases de rejugabilidad §5.4, Pactos de Vela
§4.6, techo post-finales) sigue como referencia; la validación real llegará con
el harness de Ornstein (§8.6). Lo único de largo plazo ya medible en código: el
ruido por comando está contabilizado (cd 0/ls 1/cat 1/cp 3) y es la base
numérica de la tensión velocidad-vs-cuidado del late game.

## 📝 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: tutorial cap. 0 con `cp`)

- **Sesión canónica end-to-end:** `test_session_cap0.py` 3/3 passed (escena
  byte a byte + gancho `cp` + reproducibilidad entre procesos). ✓
- **Smoke del conjunto:** «225 passed sí o sí» → **225 passed** ✓ (cuadra con
  lo prometido por Gwyn: 105 common + 91 sandbox + 29 assets).
- **Capturas golden regeneradas:** estables byte a byte (árbol limpio tras
  regenerar). ✓ El sabor CRT lo juzga Havel.
- **Cruce sesión ↔ prosa retocada por Manus:** dossier con `destino: /usb` y
  «no salgas sin la copia» ✓; los 4 comandos (`ls`/`cat`/`cp`/`cd`) aparecen en
  la escena técnica por necesidad ✓; run 0 PUEDE fallar con línea de expulsión
  y post-mortem vivo (🧭2 materializada) ✓. UNA divergencia hallada: el listado
  tras `cd /srv` en la prosa muestra `usb`, que en el FS real cuelga de la raíz
  → `[PENDIENTE][P2]` filed (barato de arreglar ahora en la prosa).
- **¿Enseña por necesidad?** SÍ a nivel de comando (leer para saber QUÉ copiar,
  copiar para cumplir el encargo, navegar para orientarse). A nivel de RUTA hay
  un hueco de andamiaje (dossier con nombre relativo vs cwd tras la secuencia
  canónica): 🧭2 para Gwyn.

## 🧭 Notas de dirección

*(Detalle en `backlog/notas-manana.md` 🧭 — sobrescritas hoy.)* Resumen: (1)
encadenado `&&`/`;` → rechazo didáctico ([BUG][P2] filed); (2) definir cwd
inicial y significado mecánico de «run guiada» en el cap. 0; (3) divergencia
prosa ↔ FS en el listado de la escena ([P2] filed); (4) REPL
`python -m core.sandbox` ([P3] filed). Las 🧭1–7 de la revisión de papel del
27/08 quedan saldadas (1–2 materializadas y verificadas hoy; 3–7 como tareas en
`abierto.md`). Nada bloquea el plan del 29/08.

CICLO: verde — el camino del cap. 0 aguanta de principio a fin en proxy
headless; los 4 hallazgos de hoy son rozaduras, no roturas.

---
*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*
