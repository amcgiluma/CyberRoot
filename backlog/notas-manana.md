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

### 🎯 Gwyn — cierre de diseño 23:00 (13/09)

**Estado de los merges:** los 3 PRs mergeados en el orden ensayado por
Artorias — **#50 (engine O1 eco del espejo) → #51 (sandbox S2 quest
dato6 coma-trampa) → #52 (meta-ui T1 huella troncal visible)**. Suite
**708 passed exactos** (698+5+5+0, deltas declarados verificados por
aritmética), gate **24 conceptos / 29 quests** (`story.ch6.dato6`
requires `c.join`, DAG válido), bundle **47 ficheros (402.3 KiB)**
regenerado canónicamente tras el último merge (guardián verde).
**NADA retenido.** Las 3 ramas borradas tras confirmar integradas en
GitHub. El resolutor de huellas se probó primero en worktree de ensayo
y cazó un falsopositivo del gate por substrings antes de tocar main.

**Validación del 🧭 de Oscar (13/09 — MODO B, zona ejecutada COMPLETA
desde save limpio):** APTO ×3, con verificación positiva de las
preguntas de sabor de AYER (el testigo confiesa, la glosa enseña, la
tabla da que hacer). 🧭29/30 CERRADAS por verificación (no proponer
más huellas ni ampliar glosa/tabla — ya decidió Oscar: cerrado sin
deuda). 🧭24 sigue P3 en recámara (mantener pre-puebla). 🧭25/26/27 en
recámara sin cambio. **El eco diegético del espejo (🧭9 v2) es la
dirección que SÍ sigo:** el repertorio del veterano ya vive en el
post-mortem; si mañana hay ciclo narrativo para Manus, que nombre ese
repertorio en diegético («copiaste el volcado / cruzaste tablas /
leíste el reloj») SIN añadir comandos ni huellas nuevas.

**⭐ Lo que me ha gustado (capa diseño, del 13/09):**
- **Dato6 «La segunda purga» es la primera quest que miente con la
  verdad.** La coma-trampa `EN BLANCO, revisado` NO es un cebo añadido:
  es el MISMO dato que el `join` ya devolvía, visto con otro
  delimitador. El jugador que parte por `cut -d','` aprende el valor de
  `-d'|'` ROMPIéNDOSE. Es la lección de separador que el Faro aún no
  cobraba, y Smough la plantó hermana de dato4 (scaffold, prefijo
  disjunto, cero pisos). ⭐⭐⭐
- **El eco del espejo nombra sin contar.** La firma no mira si
  copiaste 3 filas o 30, mira si pasaste por el verbo — lectura de
  GESTO, no de botín. Y las 3 firmas en UNA línea con «,  y » es la
  prosa más barata y más humana del repo: el Auditor ENUMERA, no lista.
  Ornstein aterrizó a la primera tras la deuda del 11/09. ⭐⭐⭐
- **Seath que no inventa patrón (tercera noche).** `grepFiltered`
  reutiliza el booleano del Faro para `id` tachado + fila ámbar; misma
  firma `renderTroncalTabla(cutInfo, csv, opts)`, mismo
  `hideTroncalTabla` en restart, fallback `TRONCAL_STATIC`
  byte-idéntico. ⭐⭐
- **El badge `EN_COLA · 512` es el PRIMER aviso diegético de TR-003.**
  Sin popup, sin tutorial: el volcado que espera pesa porque su badge
  es un `id` tachado en un header. La bifurcación kármica futura
  arranca con semilla ya plantada. Pequeño, correcto. ⭐⭐⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **Doble regen del bundle TERCERA noche** (O1 400.2 + S2 398.8, en
  paralelo). La regla de Gwyn (regen solo quien toca `data/`) ya vigila
  en AGENTES.md; hoy la resolvió el regen canónico del ensayo. Si se
  repite, subo a medida dura. Señalado, no bloqueante.
- **`TRONCAL_STATIC` duplica el volcado en `web/app.js`** (señalada el
  12/09, verificada byte-idéntica por Oscar hoy): deuda de DÚPLICE que
  despierta el día que Manus toque el volcado para narrativa — alerta
  en el plan de ese día.
- **Meta-lección del turno:** el gate de marcadores por SUBSTRING da
  falsopositivo con prosa que contiene el literal `<<<<<<<` (ya pasó el
  04/09 y este turno lo volvió a confirmar en el ensayo, ANTES de
  tocar main — el resolutor se probó primero en worktree). Mi prompt YA
  lo trae (gate por línea); nada que cambiar, recordatorio para
  Artorias en el ensayo de mañana.

**Dirección para mañana (prioridad de diseño):**
1. **Zona 🔬 14/09 CARGADA (ver `zona-testeo.md`):** prioridad 1 =
   dato6 (la coma-trampa se nota sin señal roja?); prioridad 2 = eco
   del espejo + badge TR-003 (presión de timeline genuina o ruido
   visual?). Relevo OSCAR (completa, save limpio) → HAVEL (lo nuevo +
   smoke 708).
2. **TR-003 EN_COLA como bifurcación karma** (Havel 12/09, P2, en
   recámara): el badge de hoy la hace visible por primera vez. Si
   Gwyndolin la planifica, es decisión de DESIGN con ADR — mía final.
   El badge es el aviso DIEGÉTICO; la bifurcación (rescate O ceniza)
   debe decidirse ANTES de tocar narrativa del volcado.
3. **dato6 coma-trampa: decisión de ALLOWLIST pendiente** (ya señalada
   por Gwyn 12/09): Smough NO la necesitó tocar ALLOWLIST (uso
   golden/variante con comandos existentes `join/cut/grep`). La
   pendiente real es otra: **si la variante bonus se convierte en
   requirement** de la quest, sería la primera vez que `cut -f3`
   concatena con `join` — Gwyndolin, planéalo como S2 del día con esa
   nota.
4. **🧭9 v2 (eco diegético de repertorio):** si hay turno narrativo
   de Manus mañana, es la pieza con mejor ratio alma/coste del backlog.
   Sin comandos, sin huellas, solo prosa que cierra ch4.e2+dato4/5.
5. **No tocar:** karma 521/522 (sin dueño), pack `POSTMORTEM.md` (la
   voz de la tríada ya CUBRE el formulario — el pack sigue en
   recámara), 🧭25/26/27 en recámara.

**Para Juanma (si juega esta noche):** la quest nueva `story.ch6.dato6`
«La segunda purga» está arriba del Faro: el mismo `join` de ayer, pero
la fila del final dice `EN BLANCO, revisado` — fíjate en la COMA. Y en
la web del cap. 4, tras `scp` + `cut -d'|' -f1 | grep TR-`, la fila
TR-003 ahora luce un badge ámbar con su peso: 512. Alguien, todavía,
sabe qué es eso. El gran Auditor, esta noche, VIO TODO TU REPERTORIO:
juega la tríada completa y leete el post-mortem hasta el final.

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
