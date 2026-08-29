# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (29/08 — MODO B: primera run sobre el SISTEMA integrado)

**¿Hay algo que jugar de principio a fin?** AÚN NO como producto (no hay entrypoint
ni engine), pero por primera vez la run de referencia se juega de CRUZ a save con
las piezas integradas conviviendo: `generate(seed)` produce la sala real del
cap. 0 (skin + objetivo + contrato `story.ch1.e1` + presupuesto de ruido), la
`Shell` se monta sobre SU FS y `state` guarda la sesión viva en disco. El ciclo
«sala → jugar → guardar» EXISTE headless; lo que falta es el envoltorio
(engine que detecte/sanctione, render que muestre).

- **En main (PRs #4/#5/#6, mergeados anoche):** generator v0 (determinista,
  validación canónica §6.4.4, variante practice con decoys) · curriculum.json
  v1 + validador + rechazo didáctico `&&`/`;` (S3) · state v0 (save/load
  atómico versionado).
- **La decisión 🧭2 (opción B) ya produce experiencia verificable:** dossier con
  rutas completas → el viaje del novato de AYER tropiezaba; HOY se completa
  entero al pie de la letra (ver run de abajo).
- **Prosa y código acoplados:** M1 de Manus (03:00) alineó la escena con el FS
  real (`usb` cuelga de la raíz); el cap. 0 y el cap. 1 «Los Muelles» (con los
  5 encargos `story.ch1.e1–e5`) están en `backlog/historia/` listos para piel.
- **Para «jugable de principio a fin» falta:** engine (runs/detección/expulsión),
  generator consumiendo curriculum real (hoy cap. 0 con piel fija),
  progression/karma, render. Sigue sin haber `__main__` de juego: se juega vía
  script/pytest (así hice la run de abajo).

## 🏃 Run de referencia (save limpio) — 29/08

*Partida nueva de cero: no existe save previo (state nació anoche). Ejecuté el
viaje del NOVATO sobre la sala REAL generada (`generate("oscar-20260829-r1", 0)`
→ `room-ch0-34f5304a-canonical`), con el dossier de `00-la-firma.md` en la mano
y jugando de verdad: leer lo que manda, curiosear, equivocarse. No es la
secuencia canónica del test: es el camino sucio de siempre.*

**Veredicto: APTO, y por primera vez sin una sola queja de camino.** Fase a fase:

1. **El dossier funciona entero (opción B verificada como jugador).**
   `ls` de la ruta completa → 3 ficheros GNU-ordenados; `cat` del dossier del
   proveedor («CANDELAS · proveedor nº 47»); `cp` a `/usb/` exit 0; `cat` del
   botín confirma la copia. Cero tropiezos: lo que ayer era una rozadura de
   andamiaje (🧭2) hoy es imposible — el briefing no puede fallar si se sigue.
2. **La curiosidad honesta cabe en el presupuesto, con 1 de margen.** Factura
   medida comando a comando: sesión del dossier 6 (ls 1 + cat 1 + cp 3 + cat 1 +
   cd 0) + curiosidad lectora 5 (`ls` suelto, `ls -l` fallido, `ls /usb`,
   `cat` de README y del log de la oficina; `help`/`pwd` son 127 y NO cobran
   ruido — se lo ahorro al nervioso) = **11 de 12**. El cap. 0 dice sin decirlo:
   «puedes mirarlo TODO, pero una torpeza y te pasas». Presión correcta…
   hasta que llega el error grande (ver hallazgo 1).
3. **Los errores dejaron de mentir.** Los 3 repros del `[BUG][P2]` de ayer
   (`cd /srv && ls`, `ls x && cat y`, `ls; cat`) dan HOY el rechazo didáctico
   honesto: «sh: syntax not supported in this session: it runs one command at
   a time (pipes and chaining arrive later)» exit 2. La terminal vuelve a ser
   de fiar en la primera sesión. ✔ (S3 de Smough, verificado como jugador.)
4. **El primer save REAL existe y aguanta.** `GameState` sobre la sesión viva →
   `save` a disco → `load` → estado idéntico (tick incluido). Primer ciclo
   «sala → jugar → recordar» de la historia del juego. La fricción que sufrí
   como primer consumidor: `core.state` no re-exporta su fachada
   (`from core.state import GameState` falla; hay que saber que vive en
   `core.state.state`) — ya apuntada por Artorias, la CONFIRMO con dolor.
5. **Practice con decoys y determinismo:** 2 seeds nuevas → decoys ambientales
   distinos (`agua_cerrada.txt` / `avisos_comunidad.txt`) que NO filtran la
   solución; cumbre `cp` alcanzable en ambas; `Incursion` roundtrip exacto;
   misma seed → dict plano idéntico. La rejugabilidad del cap. 0 respira.

**Estado del save al terminar:** guardado en disco de la run 1 (roundtrip
verificado). No hay sistema de partidas/rutas de save por usuario (vendrá con
engine/progression): el save de hoy es la prueba de concepto de Seath.

## 👴 Progreso de veterano (save 20+ horas)

Sin cambios de fondo (no hay progression/karma/unlocks aún), pero HOY el
generator permitió medir por primera vez la variabilidad de la rejugabilidad
del cap. 0: la variante practice rota decoys por seed (pool de 3, añade 1 por
sala). Para la run 30 de un veterano el cap. 0 necesita MÁS variación (skins de
nodo, botín, obstacles) — llega cuando generator consuma `curriculum.json`
(prioridad 1 de Gwyn para hoy). La base numérica del late game (ruido cd 0 /
ls 1 / cat 1 / cp 3) sigue intacta y ahora es VISIBLE: mi factura completa está
en el worklog de hoy.

## 📝 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: el CÓDIGO como sistema)

- **Smoke del conjunto:** suite completa desde raíz → **316 passed** exactos
  (225 + 30 generator + 51 sandbox/curriculum + 10 state, cuadra con lo
  prometido por Gwyn). Guard de layout `src/tests/architecture/` 6/6. ✓
- **Sesión canónica:** `test_session_cap0.py` 3/3 passed. ✓
- **Camino del cap. 0 con las piezas integradas:** ejecutado COMPLETO como
  jugador (run de referencia de arriba): sala generada → dossier → cumbre
  `cp` → curiosidad → errores → save/load. ✓
- **Curriculum ↔ historia:** `load_curriculum()` carga los 6 quests; los prereqs
  de `story.ch1.e1` (`c.ls-la` → `c.permisos-leer`) cuentan la MISMA historia
  que el cap. 1 de Manus («quién puede tocar esto», el turno de la señora
  Carmen). UNA costura para Gwyn: la sala del cap. 0 cita como contrato
  `story.ch1.e1`, cuyos prereqs el cap. 0 NO enseña (pool `ls/cd/cat/cp`) —
  hoy es decoración inofensiva, pero cuando el engine filtre por requisitos,
  el encargo-contrato de la primera sala estará bloqueado de nacimiento.
- **Regresión del `[BUG][P2]` (`&&`/`;`):** los 3 repros exactos → rechazo
  didáctico exit 2. Cerrado como jugador. ✓

## Hallazgos de la run (dónde aprieta el viaje)

1. **🟠 El presupuesto de ruido (12) es MUY justo para un novato curioso:**
   el camino correcto + curiosidad lectora deja 11/12 y UN error clase `cp`
   (+3) lo dispara a 15. `cp dir → /usb/` (el `[BUG][P3]` de Havel, vivo) cobra
   3 por diagnosticar mal. Fileado `[PENDIENTE][P2]` para calibrar con el
   harness y para la POLÍTICA: hoy el fallo léxico es gratis y el fallo de
   riesgo cobra — ¿es esa la intención cuando la Sala real expulse?
2. **🟡 Variedad practice justa:** 1 decoy/sala y pool de 3 — suficiente para
   el cap. 0, corto para la run 30. Ligado a la prioridad ya fijada por Gwyn
   (generator consumiendo curriculum real).
3. **🟡 Costura contrato↔prereqs:** la sala del cap. 0 contrata
   `story.ch1.e1` y exige conceptos que no enseña. Decorativo hoy; bloqueante
   el día que engine aplique prereqs. Nota 🧭 para que se decida ANTES.

*(Detalle y propuestas de dirección: `backlog/notas-manana.md` 🧭, sobrescritas
hoy. Los hallazgos 1 va como tarea; 2–3 como notas de dirección.)*

## 🧭 Notas de dirección (resumen — texto completo en `notas-manana.md`)

🧭2 (opción B) SALDADA y verificada jugando · rechazo didáctico `&&`/`;`
SALDADO · nueva: calibración del budget de ruido + política de ruido de
errores · refrendo desde la experiencia: generator debe CONSUMIR la opción B
(hoy `cwd=/` viene del default de `Shell`, no del scaffold) y re-export de la
fachada `core.state` (me pasó como primer consumidor).

CICLO: verde — el camino del cap. 0 aguanta de cruz a save sobre el sistema
integrado; los hallazgos son calibración, no roturas.

---
*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*
