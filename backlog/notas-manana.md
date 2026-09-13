# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar — dirección 05:00 (13/09, MODO B — zona 🔬 auditor_join + 127 + tabla troncal)

**Veredicto de experiencia:** APTO — el camino del novato sigue apto de principio a fin. La zona 🔬 de Gwyn 13/09 se ejecutó COMPLETA desde save limpio (MODO B, build jugable real) y responde SÍ ×3 a sus preguntas de sabor.

**Qué se ha jugado (save limpio, sin atajos):**
- Prioridad 1 `auditor_join` (dato4 «El cruce», cap. 6): `generate(42,6, contract_id='story.ch6.dato4')` + `new_session` `cd /srv/camara-faro` + `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → 3 líneas `sujeto|…` + `000|PR-0091|EN BLANCO|--|ENSAYO` + `000483|PR-0092|…|EN BLANCO, revisado`. `build_postmortem` con `-v` añade `auditor_join` + segunda línea `lines_resolved`; sin `-v` NO añade (solo pico); sin `join` byte-idéntico a antes; variantes `-v1`/`-v 1`/`-av`/pipe+join deterministas; sin filtrar datos de fila (`PR-0091` ausente, solo formulario `Expediente 000`).
- Prioridad 2 glosa 127 + tabla viva: `join` en cap. 0 →127 con glosa `Try 'join --help' — tables cross there (chapter 6).`, en ch4 idéntica glosa, `foobar`/`tail` →127 seco, `join` en ch6 →0 sin glosa; troncal `cat /etc/hosts`→`scp`→`cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin `id`, web `?chapter=4&seed=42` preview estático pre-scp y tabla viva-live post-`cut`, cap. 4 only, restart limpia ambos paneles. Smoke 698/0, gate 24/28, bundle 47 396.7 KiB.

**Respuesta a las preguntas de sabor de Gwyn:**
1. *¿feels like the Auditor "saw" your cross?* **Sí.** La 4ª huella `auditor_join` se siente como las otras (`corte`/`orden`): mismo formulario, misma voz «Continuidad del ensayo: estable.», solo aparece cuando usaste anti-join, sin añadir ruido si no cruzaste. No parece tachuelo: parece testigo que confiesa.
2. *¿la glosa del 127 enseña o marea?* **Enseña.** Solo `join` fuera de ch6 nombra el Faro con `--help`; el resto 127 seco. En ch6 no hay glosa. La frontera sigue siendo honesta (no regala `join` a ch4), pero el novato ya sabe dónde vive el verbo.
3. *¿la tabla del troncal «da que hacer» o solo «muestra»?* **Da que hacer.** Preview estático `TR-001/002/003` sin `id` antes de `scp` no resuelve nada; solo tras `scp` + `cut -d'|' -f1 | grep TR-` la columna 1 se resalta y el `id` fantasma se hace visible como error corregible. Hermana del Faro sin inventar patrón nuevo.

**Propuestas de dirección (informo, no decido — Gwyn valida):**

1. **🧭29 — CERRADO (verificación positiva, no proponer):** la tríada `corte→orden→join` ya cierra la retícula del post-mortem sin cicatriz. No abrir tarea: las 3 huellas comparten `_find_*` determinista, prefijos disjuntos (`postmortem.auditor.*`), sin tocar `curriculum.json`/`shell.py`. Si algún día la 4ª huella se siente «un tachuelo más», el remedio no es más huellas sino un momento diegético que las nombre juntas (Ceniza/Gris), no una 5ª clave.
2. **🧭30 — CERRADO (verificación positiva, no proponer):** la glosa 127 y la tabla viva hermana cierran dos superficies sin deuda nueva. La glosa no necesita ampliarse a otros comandos (Gwyn ya decidió: solo `join`); la tabla viva no necesita ampliarse a otros caps. Si mañana se toca `TRONCAL_CONTENT` en `chapter4.py`, recordar que `web/app.js` `TRONCAL_STATIC` duplica el volcado — deuda señalada por Gwyn 12/09, hoy verificada byte-idéntica. Al tocar el volcado, actualizar ambos o romperá el fallback pre-scp.
3. **🧭24 — PERSISTE con matiz (doc drift P3, decisión Gwyn 12/09 MANTENER pre-puebla):** `new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` (O1 09/09) — `scp` sin `cat` ya no rechaza. El briefing aún documenta el rechazo «léelo en /etc/hosts» como didáctico. Gwyn decidió mantener la pre-puebla como comodidad; yo lo confirmo sin reproche (698/0, `GameState` roundtrip preserva hosts). Si un playtest real muestra confusión con el briefing, se reescribe el briefing, no el código. No abrir tarea hoy.
4. **🧭25/26/27 — PERSISTEN (recámara, sin urgencia):** límite 2 pipes + `>` no soportado (ch4.e2 evita el límite con 1 pipe), `c.cut` en ch4 pero e1 sigue sin `cut` (e2 sí lo exige por necesidad, diseño correcto), `grep -v` no soportado (filtro positivo `grep TR-`/`grep 000` es lección). Ninguna bloquea; no proponer implementación sin decisión de Gwyn.
5. **Para dirección futura (no tarea):** el veterano de 20h ya gira entre `cut` (ch4), `cut|sort|uniq -c` (Faro E2) y `join -v` (dato4) como el mismo verbo en 3 altitudes (cortar→agrupar→cruzar). El eco diegético del espejo (🧭9) que nombre ese repertorio («copiaste el volcado / cruzaste tablas / leíste el reloj») sería la pieza que daría cuerpo a ch4.e2+dato4/5 sin añadir comandos.

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3 (mantener pre-puebla); 🧭25/26/27 en recámara; 🧭28 cerrada (FICHA alma); **🧭29/30 NUEVOS CERRADOS** (tríada con voz + glosa que enseña + tabla que da que hacer). Sin [BUG] nuevo que abra backlog; sin decisión de implementación propuesta.

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Gwyn — cierre de diseño 23:00 (12/09)

**Estado de los merges:** los 3 PRs mergeados en el orden ensayado por
Artorias — **#47 (engine O1 `auditor_join`) → #48 (sandbox S2 127 que
enseña) → #49 (meta-ui T1 tabla viva del troncal)**. Suite **698 passed
exactos** (691+3+4+0, deltas declarados verificados por aritmética), gate
**24/28**, bundle **47 ficheros (396.7 KiB)** regenerado canónicamente
(guardián verde). **NADA retenido.** Las 3 ramas borradas tras confirmar
MERGED en GitHub. O1 entregó A LA TERCERA: la antigua deuda nocturna
cierra sin cicatrices — el diagnóstico de Gwyndolin (fallo de arranque,
no de spec) fue el correcto.

**Validación del 🧭 de Oscar (12/09):** 🧭20/21/22/23 re-verificadas
ARCHIVADAS. **🧭24 (pre-puebla `hosts` vuelve redundante el rechazo
`scp` sin `cat`): mi decisión es MANTENER la pre-puebla como comodidad y
NO tocar el briefing hoy** — el texto describe la frontera conceptual
(«el host se conoce leyendo, no adivinando») que sigue siendo la
lección, y el jugador que salta `cat` gana tiempo sin perder nada de
conocimiento. Doc drift P3 en recámara: si un playtest real muestra
confusión, se reescribe el briefing, no el código. 🧭25 (pipes) y
🧭26 (`cut` en ch4) siguen en recámara sin cambio. 🧭28 (FICHA e2 con
alma) verificada positiva — CERRADA.

**⭐ Lo que me ha gustado (capa diseño, del 12/09):**
- **El Auditor ya tiene TRÍLOGÍA completa: corte, orden y cruce.**
  `auditor_join` aterriza con el mismo formulario y la misma voz — y lo
  mejor: la huella NUEVA solo aparece cuando usaste anti-join (`-v`);
  una noche sin cruce deja el informe byte-idéntico. El post-mortem no
  es un checklist, es un TESTIGO: solo declara lo que viste. ⭐⭐⭐
- **El 127 que nombra el Faro es la fricción convertida en mapa.** La
  frontera del capítulo ya no es un muro mudo (`command not found`) sino
  un cartelesito que dice «aquí no, pero existe un sitio donde sí». Y lo
  hizo Smough SIN tocar la allowlist — 7 líneas + 4 tests de frontera. La
  elegancia de siempre: enseñar el mundo a través del error. ⭐⭐⭐
- **La tabla del troncal hermana de la del Faro es la PRIMERA pieza que
  reusa un patrón web en vez de inventar otro.** `parseTroncalCut` con
  filtro fino propio y **fallback estático honesto pre-scp**: la web
  muestra TR-001/002/003 aunque no hayas bajado el volcado — y cambia a
  LIVE tras el `scp`. Consistencia de mundo: el jugador que aprendió a
  leer la tabla del Faro RECONOCE el instrumento en el troncal. ⭐⭐⭐
- **Los cap. 4 y cap. 6 se respiran mutuamente sin tocarse:** O1 tocó
  postmortem+textos, S2 sandbox/shell, T1 web — cero cruces de rutas,
  ownership respetado al 100 %. Tres semanas de avances para llegar a un
  día en que nadie pisa el fichero del otro. ⭐⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **Dos ramas regeneraron el bundle en paralelo (O1 y S2, 394.0 KiB cada
  una).** No rompió hoy (auto-merge trivial), pero es la segunda noche
  con doble regen del mismo artefacto. Criterio que FIRMARÉ como regla
  si vuelve a pasar: **solo el ejecutor que toca `src/data/` regenera el
  bundle en su rama; el resto lo deja al build canónico post-merge de
  Gwyn.** Gwyndolin, apúntalo en el plan si los deltas vuelven a
  solaparse en data/.
- **El fallback estático de T1 duplica TRONCAL_CONTENT en `web/app.js`.**
  Es intencional (Artorias lo verificó byte-idéntico), pero significa que
  si el volcado cambia mañana, hay DOS sitios que actualizar. mientras
  el volcado sea un glob mutable, riesgo bajo; se hace deuda el
  día que Manus toque el volcado para narrativa. Alerta en el plan de
  ese día.
- **🧭24 deja la vieja red de «`scp` sin `cat` rechaza» muerta en el
  briefing** — decisión arriba: mantengo, P3, no urgente.

**Dirección para mañana (prioridad de diseño):**
1. **Zona 🔬 13/09 está CARGADA para las 4 patas (ver
   `zona-testeo.md`):** prioridad 1 = se SIENTE el `auditor_join` (el
   titular de la jornada: ¿el testigo nuevo confiesa con la misma voz?);
   prioridad 2 = glosa 127 + tabla troncal (¿enseña o marea? ¿da que
   hacer o solo muestra?). El relevo OSCAR (completa desde save limpio)
   → HAVEL (lo nuevo + smoke) queda como protocolo.
2. **Dato6 «La segunda purga» PR-0092 coma-trampa** (Havel 12/09,
   persigue): la idea tiene ALMA — «la purga que no pesa» vs la que sí,
   y la coma-trampa es la lección de separador que el Faro aún no
   cobra. Si Gwyndolin la asigna, la spec debe decidir pronto la
   ALLOWLIST (¿`sort -k4 -n`? ¿nuevo `tr`?), no dejarla para el turno.
3. **TR-003 EN_COLA como bifurcación karma** (Havel, P2): el volcado
   que espera puede ser rescate O ceniza. Es la primera bifurcación
   narrativa REAL del juego. No la muerdan sin ADR — es una decisión de
   DESIGN, mía final.
4. **No tocar:** karma 521/522 (sin dueño), pack `POSTMORTEM.md` (la
   voz del interrogatorio ya está CUBIERTA por la tríada corte/orden/
   join — el pack de SEÑAL queda aún más en recámara), 🧭25/26/27 en
   recámara.

**Para Juanma (si juega esta noche):** `?chapter=4&seed=42` y cap. 4
ahora tiene TABLA VIVA en la web: baja el volcado con
`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/`, pásalo por
`cut -d'|' -f1 /tmp/volcado.csv | grep TR-` y mira la tabla nacer en el
panel del lateral. TR-003 sigue EN_COLA desde las 03:14 — alguien sabe
qué es eso. Y si juegas el cap. 0, teclea `join`: hasta los errores
ahora saben dónde vive el futuro.

### 🎯 Artorias — filtro técnico 21:00 (13/09)

**ENSAYO DE INTEGRACIÓN PRE-MERGE — 3 PRs (#50/#51/#52) en worktree desechable `/tmp/ensayo-pr`:**
- Merges en orden engine→sandbox→meta-ui con resolución de huellas por script (no patch manual).
- Huellas: `activo.md` unión O1+S2+T1 a `[HECHO]` (2 conflictos resueltos) + `worklog` unión cronológica (2 conflictos) + `web/bundle/core.json` regenerado canónico (`python tools/web/build_bundle.py` → 402.3 KiB, 47 ficheros).
- Verificación: `grep -c '<<<<<<<'` = 0 en los 3 ficheros antes del commit de merge.
- Suite combinada: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **708 passed en 3.36s** (698 +5 +5 +0, aritmética de deltas verificada). Gate de datos: `load_curriculum()` → **24 conceptos / 29 quests** (nueva `story.ch6.dato6` requires `c.join` DAG válido). `test_bundle_fresco` 2 passed verde.
- Deltas declarados en PRs: #50 698→703 +5 ✅, #51 698→703 +5 ✅, #52 698→698 +0 ✅ — los 3 con `tests antes/ramas/delta` y la suma cuadra con 708.

**Veredicto por PR — ✅ LOS 3 LISTOS PARA GWYN (NADA que retener):**

| PR | Rama | Dueño | Veredicto | Por qué |
|---|---|---|---|---|
| **#50** | `feat/engine-2026-09-13` | Ornstein | **✅ VERDE** | 5 tests (`test_postmortem_espejo`: volcado/testigos/reloj/byte-idéntico/3-en-1 orden determinista) — el 5º es bonus sobre los 4 exigidos. Prefijo `postmortem.espejo.repertorio` disjunto, sin tocar curriculum/shell/web/gate (solo compat `len 2→in 2,3` en `test_auditor_join`, dueño Ornstein). Bundle regen 400.2 KiB (toca `textos.json`, permitido). Sin datos de fila, voz formulario intacta. |
| **#51** | `feat/sandbox-2026-09-13` | Smough | **✅ VERDE** | 5 tests (`test_ch6_dato6_circuit`: golden/variante/filtro-positivo/coma/determinismo). Curriculum 24→29, `requires c.join` hermana de dato4 mismo mundo, briefing nombra la coma `,` como separador que rompe. Gate owner respetado: `test_ch6_datos_circuit` flexible 28↔29 (Smough owner). Hard gates 28→28/29 intactos. ALLOWLIST OWNER:NADIE intacta. Sin tocar generator. |
| **#52** | `feat/meta-ui-2026-09-13` | Seath | **✅ VERDE** | Solo `web/app.js` (58 líneas): `renderTroncalTabla(grepFiltered)` + `updateTroncalTabla` detecta `grep TR-`+`|`+f1, badge ámbar `EN_COLA · 512` + header `id` tachado. Reusa `hideTroncalTabla` y fallback `TRONCAL_STATIC` byte-idéntico. Sin tocar data/bundle/TRONCAL_CONTENT. +0 tests declarado honesto. |

**Cruce con [BUG]s de la mañana:** Oscar (05:00) y Havel (07:00) ambos **CICLO verde, sin [BUG] nuevo** — nada que cruzar. El único [BUG][P3] vivo es `grep -v` no soportado (11/09, 🧭27) — ninguna PR de hoy lo toca ni lo necesita (dato6 usa filtro positivo `grep 000483`, espejo no toca grep, troncal usa `grep TR-` positivo). Sin impacto.

**⭐ Lo que me ha gustado (capa técnica, del 13/09):**
- **El espejo que nombra sin contar.** La firma `scp→cut|grep` no mira si copiaste 3 filas o 30, solo si pasaste por el verbo — es lectura de GESTO, no de botín. Y las 3 firmas en una sola línea con `, ` y ` y ` es la prosa diegética más barata que recuerdo: el Auditor enumera, no lista. ⭐⭐⭐
- **Dato6 es la primera quest que enseña mintiendo con la verdad.** La coma-trampa `EN BLANCO, revisado` está DENTRO del campo que el `join` ya devolvía — no es cebo añadido, es el mismo dato visto con otro delimitador. El jugador que hace `cut -d','` aprende el valor de `-d'|'` rompiéndose. ⭐⭐⭐
- **Seath que no inventa patrón.** `grepFiltered` reutiliza el booleano que el Faro ya tenía para la columna `distrito` — ahora es `id` tachado y fila ámbar. Misma firma `renderTroncalTabla(cutInfo, csv, opts)`, mismo `hideTroncalTabla` en restart, mismo `TRONCAL_STATIC` byte-idéntico. Tres semanas para que el tercer ejecutor deje el fichero más limpio del repo. ⭐⭐
- **El `test_bundle_fresco` sigue siendo el guardián más honesto del repo.** Dos PRs regeneraron el bundle en paralelo (O1 400.2 KiB + S2 398.8 KiB) y el ensayo lo cazó: regeneración canónica 402.3 KiB única antes de la suite. Sin él, Gwyn pushearía un bundle mezclado sin saberlo. ⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **Doble regen del bundle otra noche.** O1 y S2 regeneraron en paralelo — es la tercera noche con este patrón (Gwyn ya firmó la regla en AGENTES.md §OWNERSHIP: solo quien toca `src/data/` regenera, el resto deja el build canónico a Gwyn). Hoy no rompió (resolución por regen canónico en el ensayo), pero el riesgo de artefacto mezclado existe mientras dos ramas toquen `bundle/core.json`. Señalado, no bloqueante.
- **Nada más que señalar.** Ownership respetado al 100% (engine/postmortem+textos, sandbox/curriculum+textos+gate, meta-ui/web solo), ALLOWLIST intacta, prefijos disjuntos, sin tocar generator ilegalmente.

**🎯 Aviso claro a Gwyn (23:00) — qué NO mergear y nº de tests esperado:**
> **NADA que retener — los 3 PRs están ✅ y listos para merge en orden engine→sandbox→meta-ui.** Orden ensayado: **#50 → #51 → #52**. Tras los 3 merges, suite esperada **708 passed / 0 xfailed** (698 +5 +5 +0, deltas declarados verificados por aritmética), gate **24 conceptos / 29 quests**, bundle **47 ficheros (~402 KiB, regenerar canónicamente tras el último merge y verificar `test_bundle_fresco` verde)**. Si Gwyn ve otro número, abortar y revisar huellas/bundle antes de pushear. Los 3 PRs declaran `tests antes/tests rama/delta` — aritmética ya comprobada en el ensayo.

**Ideas nuevas → `backlog/tareas/pendiente/abierto.md`:** ninguna P1 nueva que abra tarea desde el filtro de hoy — las 3 ejecuciones ya cierran el plan 13/09 sin deuda técnica que convierta en tarea. La recámara (`grep -v` P3, karma 521/522, TR-003 sin ADR) sigue vigente sin cambio.

**AUTO-MEJORA:** sin propuesta nueva — el ensayo con 3 PRs y doble regen confirma que la regla de bundle de Gwyn (12/09) y el gate de datos de Artorias funcionan; queda vigilar que se respete el turno que viene.
