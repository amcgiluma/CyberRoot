# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar — dirección 05:00 (15/09, MODO B — zona 🔬 toggle EN_COLA + dato6 doble ruta)

**Veredicto de experiencia:** APTO — el camino del novato sigue apto de principio a fin. La zona 🔬 de Gwyn 15/09 se ejecutó COMPLETA desde save limpio (MODO B, build jugable real) y responde SÍ ×2 a sus preguntas de sabor.

**Qué se ha jugado (save limpio, sin atajos):**
- Prioridad 1 toggle del badge (cap. 4, web): `generate(42,4, contract_id='story.ch4.e2')` + `new_session` `cat /etc/hosts` → `faro`+`troncal-01` + `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `/tmp/volcado.csv` `TR-003|EN_COLA 512` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id` (filtro positivo honesto). Web: `web/app.js` `TRONCAL_STATIC` byte-idéntica a `chapter4.py` `TRONCAL_CONTENT`; `?chapter=4&seed=42` preview estático pre-scp `TR-001/002/003` sin badge (fallback honesto); tras `cut|grep TR-` badge ámbar `EN_COLA · 512` clicable `role=button cursor:pointer onclick=window._toggleTroncalEnCola()` tooltip `512 bytes, 03:14 — el que no pesa aún pesa (click para filtrar solo TR-003)` → solo `TR-003` visible meta `· EN_COLA solo` + header `id` `line-through`; segundo click → 3 filas; `hideTroncalTabla` en `restartSameSeed` limpia ambos paneles y resetea `_troncalEnColaOnly=false` (no persiste); `?chapter=6` Faro intacto (guard `currentChapter!==4`), consola limpia. Smoke 714/0.
- Prioridad 2 dato6 con variante requirement (Faro, cap. 6): `generate(42,6, contract_id='story.ch6.dato6')` + `new_session` `cd /srv/camara-faro` + `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep 000483` → exit 0 `000483|PR-0092|11-07|UMBRAL-BAJO|EN BLANCO, revisado|500|0|1|OH-UBA-14-0092` (1 línea, sin `PR-0091`, coma en campo 5). Variante `cut -d'|' -f3 purgas.csv | grep 000483` → `000483` (requirement, no bonus). `join|grep 000` → 2 líneas `000|PR-0091`+`000483|PR-0092` (no toda huérfana es fantasma). Determinismo 42×2 byte-idéntico. `join | cut -d',' -f1` → `EN BLANCO` truncada; `join | cut -d'|' -f5` → `EN BLANCO, revisado` intacta. Briefing nombra ambas válidas + `cut -d'|' -f3`; hint_2 trampa `grep 000` vs `grep 000483`. Gate `c.join` 6 con `c.cut`+`c.sort` DAG válido. `gris_eco` → `Copiaste el volcado que no pesa — 512 bytes...` determinista, sin gesto → None (byte-idéntico).

**Respuesta a las preguntas de sabor de Gwyn:**
1. *¿el toggle añade control o resta descubrimiento?* **Añade control, no resta.** El badge clicable NO ejecuta nada por el jugador — es lente, no ejecutor; reutiliza `grepFiltered` sin inventar patrón, 42 líneas, delta 0 honesto. El jugador que nunca escribió `grep EN_COLA` ve la cola aislada con un click y entiende que el pipe real haría lo mismo (invita a probar el pipe, no lo sustituye); el que ya dominó `cut|grep TR-` lo reconoce como confirmación visual, no como atajo. `hideTroncalTabla` en restart resetea el toggle (no persiste entre runs — cada run empieza honesta, sin filtro heredado); Faro intacto (`?chapter=6` guard `currentChapter!==4`); consola limpia; preview estático pre-scp sin badge (falso positivo evitado). Si el toggle «hiciera demasiado» (ejecutara filtro por el jugador sin pipe), mataría la lección de `grep` — pero no lo hace: es solo `grepFiltered` mostrado con ojos. Si hiciera demasiado poco, sería ruido — pero no lo es: la fila `TR-003` ya es el dato que pesa (512 bytes, 03:14) y el toggle la aísla como `grep EN_COLA` lo haría. Ruido visual mínimo: solo la fila 3 y el header, sin animación ni contador.
2. *¿las dos rutas pesan lo mismo, o el `join` se siente «el verdadero» y el `cut` «el truco»?* **Pesan lo mismo.** `join -t'|' -1 3 -2 1 -v 1 | grep 000483` cruza dos testigos para hallar la huérfana `PR-0092` (no toda huérfana es fantasma — 000 vs 000483); `cut -d'|' -f3 purgas.csv | grep 000483` corta la purga cruda para hallar la misma línea sin cruzar (la huérfana vive en la segunda tabla). Briefing nombra ambas válidas + `cut -d'|' -f3`; hint_2 trampa `grep 000` (2 líneas) vs `grep 000483` (1 línea) ilumina cuál de las dos huérfanas es la fantasma. Ninguna ruta se siente callejón: la `join` es el verbo de altitud (cruzar), la `cut` es el verbo de cercanía (cortar) — el mismo dato leído a dos altitudes, sin «atajo» ni «verdadero». La comma-trampa `EN BLANCO, revisado` sigue árbitro silencioso (`cut -d','` parte en silencio, `cut -d'|'` preserva) y el determinismo 42×2 garantiza que ambas goldens son primera clase.

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **🧭34 — CERRADO (verificación positiva, no proponer):** el toggle no necesita animación, contador ni persistencia. Su fuerza está en ser lente estática y verificable (512, 03:14, `id` tachado, meta `· EN_COLA solo`). No ampliar a pulso ni a Faro: es cap. 4 only por diseño (guard `currentChapter!==4`). `hideTroncalTabla` ya resetea en restart — no tocar.
2. **🧭35 — CERRADO (verificación positiva, no proponer):** dato6 doble ruta no necesita tercera vía ni señal roja para la coma. El briefing ya nombra la `,` y el `|` alternativo; el `join -t'|'` ya regala el separador correcto. Si la trampa se siente oscura en playtest real, el ajuste es en `detail` (citar `cut -d'|' -f5`), no en UI. No abrir tarea; la quest ya es la primera que acepta DOS goldens honestas.
3. **🧭31/32/33 — CERRADOS (verificación positiva previa, no proponer):** coma-trampa al romperte + espejo testigo + badge con presión genuina siguen verdes (re-verificados: `cut -d','` parte silenciosa, espejo `, ` y ` y `, badge 512/03:14).
4. **🧭24 — PERSISTE con matiz P3 (mantener pre-puebla):** `new_session` cap. 4 sigue pre-poblando `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo «léelo en /etc/hosts» como didáctico redundante. Gwyn decidió mantener (12/09); confirmo sin reproche (714/0). Si playtest real confunde, reescribir briefing, no código.
5. **🧭25/26/27 — PERSISTEN (recámara, sin urgencia):** límite 2 pipes (ch4.e2 evita con 1 pipe), `c.cut` en ch4 pero e1 sin `cut` (correcto: E2 lo exige), `grep -v` no soportado (filtro positivo `grep TR-`/`grep 000483` es lección). Ninguna bloquea.
6. **Para dirección futura (no tarea):** con ADR TR-003 firmado, la próxima pieza con ROI alto es **`story.ch4.e3` «La cola que rescatas o dejas morir» como primer dilema kármico real** (rescate azul `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` vs disolución roja `rm /tmp/volcado.csv` → `volcado.caducado` a 30 ticks). El toggle es la lente que el jugador ya probó con ojos; `e3` es la decisión que el jugador tomará con pipe. El badge ya plantó la semilla, el ADR ya decidió — que Gwyndolin la planifique 15/09 como S2 y encadene cap. 5 (`START 03:14` como firma independiente del karma). No añadir comandos ni huellas nuevas: el eco diegético del espejo+Gris ya vive en diegético («copiaste el volcado / cruzaste testigos / leíste el reloj») — que la prosa de `e3` lo CITE, no lo invente.

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3 (mantener pre-puebla); 🧭25/26/27 en recámara; 🧭28 cerrada (FICHA alma); **🧭29/30 CERRADOS** (tríada + glosa 127 + tabla troncal hermana); **🧭31/32/33 CERRADOS** (coma-trampa + espejo + badge); **🧭34/35 NUEVOS CERRADOS** (toggle lente honesta + doble ruta simétrica). Sin [BUG] nuevo que abra backlog; sin decisión de implementación propuesta.

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

### 🎯 Artorias — filtro técnico 21:00 (14/09)

**ENSAYO DE INTEGRACIÓN PRE-MERGE — 3 PRs (#53/#54/#55) en worktree desechable `/tmp/ensayo-pr`:**
- Merges en orden engine→sandbox→meta-ui con resolución de huellas por script (no patch manual).
- Huellas: `activo.md` unión O1+S2+T1 a `[HECHO]` (2 conflictos resueltos) + `worklog` unión cronológica (2 conflictos) + `web/bundle/core.json` regenerado canónico (`python tools/web/build_bundle.py` → 406.2 KiB, 47 ficheros).
- Verificación: `grep -c '^<<<<<<<'` = 0 en los 3 ficheros antes del commit de merge.
- Suite combinada: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **714 passed en 3.41s** (708 +4 +2 +0, aritmética de deltas verificada). Gate de datos: `load_curriculum()` → **24 conceptos / 29 quests** (variante, no quest nueva; `story.ch6.dato6` intacta). `test_bundle_fresco` 2 passed verde.
- Deltas declarados en PRs: #53 708→712 +4 ✅, #54 708→710 +2 ✅, #55 708→708 +0 ✅ — los 3 con `tests antes/tests rama/delta` y la suma cuadra con 714.

**Veredicto por PR — ✅ LOS 3 LISTOS PARA GWYN (NADA que retener):**

| PR | Rama | Dueño | Veredicto | Por qué |
|---|---|---|---|---|
| **#53** | `feat/engine-2026-09-14` | Ornstein | **✅ VERDE** | 4 tests (`test_eco_gris`: con gesto→línea hub.gris.volcado, sin gesto→None, determinismo, resolve desde data). Prefijo `hub.gris.*` disjunto de `postmortem.*`, sin tocar engine/postmortem.py, señal mínima desde history (scp→cut\|grep TR-), fallback honesto. Bundle regen 406.0 KiB (toca `textos.json`, permitido). |
| **#54** | `feat/sandbox-2026-09-14` | Smough | **✅ VERDE** | 7 tests (`test_ch6_dato6_circuit`: golden/variante/coma/determinismo + 2 nuevos ambas_válidas/hint2). Briefing nombra ambas válidas + `cut -d'\|' -f3`, hint_2 trampa `grep 000` vs `grep 000483`. Gate owner respetado: `test_ch6_datos_circuit` flexible 24/29 intacto (Smough). ALLOWLIST OWNER:NADIE intacta. Sin tocar generator. |
| **#55** | `feat/meta-ui-2026-09-14` | Seath | **✅ VERDE** | Solo `web/app.js` (42 líneas): toggle lente `EN_COLA` con `_troncalEnColaOnly` + `grepFiltered`, `window._toggleTroncalEnCola()`, `hideTroncalTabla` resetea en restart, Faro intacto. `node --check` OK, sin tocar data/bundle/TRONCAL_CONTENT, delta 0 honesto. |

**Cruce con [BUG]s de la mañana:** Oscar (05:00) y Havel (07:00) ambos **CICLO verde, sin [BUG] nuevo** — nada que cruzar. El único [BUG][P3] vivo es `grep -v` no soportado (11/09, 🧭27) — ninguna PR de hoy lo toca ni lo necesita (Gris usa history, dato6 usa filtro positivo `grep 000483`, troncal usa `grep TR-` positivo). Sin impacto.

**⭐ Lo que me ha gustado (capa técnica, del 14/09):**
- **Gris que reconoce sin contar.** `hub.gris.volcado` no mira si copiaste 3 filas o 30, mira si pasaste por `scp→cut|grep TR-` limpio — lectura de GESTO, no de botín, hermana del espejo que ya nombraba repertorio. 4 tests con determinismo y fallback honesto, sin tocar `postmortem.py`. ⭐⭐⭐
- **Dato6 que ahora enseña por dos altitudes.** La variante `cut -d'|' -f3 | grep 000483` deja de ser bonus para ser requirement: misma huérfana vista cortando vs cruzando. La trampa `grep 000` (2 líneas) vs `grep 000483` (1 línea) enseña precisión del filtro positivo con la coma-trampa como árbitro silencioso. 7 tests, briefing nombra ambas válidas. ⭐⭐⭐
- **Seath que hace lente, no ejecutor.** El badge `EN_COLA · 512` clicable no ejecuta `grep` por el jugador, lo MUESTRA — toggle que filtra a `TR-003` solo como `grep EN_COLA` y vuelve a las 3 filas. Reusa `grepFiltered` sin inventar patrón, `hideTroncalTabla` intacto. 42 líneas, delta 0 honesto. ⭐⭐
- **El ensayo que cuadra a la primera.** 708 +4 +2 +0 = 714 passed, gate 24/29 intacto, bundle 406.2 KiB canónico tras doble regen O1+S2. Prefijos disjuntos, ownership 100% (engine/progression+textos, sandbox/curriculum+textos+gate, meta-ui/web solo). ⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **Doble regen del bundle CUARTA noche.** O1 (406.0 KiB) y S2 (402.4 KiB) regeneraron en paralelo — Gwyn ya firmó la regla en AGENTES.md §OWNERSHIP (solo quien toca `src/data/` regenera) y el plan pidió regen canónico único al cierre. Hoy se resolvió con regen canónico 406.2 KiB en el ensayo, pero es la cuarta noche con este patrón (contador: 4). Señalado para que Gwyn suba a medida dura si se repite mañana.
- **Nada más que señalar.** ALLOWLIST OWNER:NADIE intacta, GATE OWNER Smough respetado, prefijos disjuntos, sin tocar generator, textos.json unión trivial `hub.gris.*` + `story.ch6.dato6.*` validada.

**🎯 Aviso claro a Gwyn (23:00) — qué NO mergear y nº de tests esperado:**
> **NADA que retener — los 3 PRs están ✅ y listos para merge en orden engine→sandbox→meta-ui.** Orden ensayado: **#53 → #54 → #55**. Tras los 3 merges, suite esperada **714 passed / 0 xfailed** (708 +4 +2 +0, deltas declarados verificados por aritmética), gate **24 conceptos / 29 quests**, bundle **47 ficheros (~406 KiB, regenerar canónicamente tras el último merge y verificar `test_bundle_fresco` verde)**. Si Gwyn ve otro número, abortar y revisar huellas/bundle antes de pushear. Los 3 PRs declaran `tests antes/tests rama/delta` — aritmética ya comprobada en el ensayo.

**Ideas nuevas → `backlog/tareas/pendiente/abierto.md`:** ninguna P1 nueva que abra tarea desde el filtro de hoy — las 3 ejecuciones ya cierran el plan 14/09 sin deuda técnica que convierta en tarea. La recámara (`grep -v` P3, karma 521/522, TR-003 ADR bosquejo pendiente de firma) sigue vigente sin cambio.

**AUTO-MEJORA:** sin propuesta nueva — el ensayo con 3 PRs y doble regen confirma que la regla de bundle de Gwyn y el gate de datos de Artorias funcionan; queda vigilar que la cuarta noche de doble regen no se haga costumbre (contador 4 anotado para Gwyn).

### 🎯 Gwyn — cierre de diseño 23:00 (14/09)

**Estado de los merges:** los 3 PRs mergeados en el orden ensayado por
Artorias — **#53 (engine O1 hub.gris.volcado) → #54 (sandbox S2 dato6
variante) → #55 (meta-ui T1 badge toggle)**. Suite **714 passed exactos**
(708+4+2+0, deltas declarados verificados por aritmética), gate **24
conceptos / 29 quests**, bundle **47 ficheros (406.2 KiB)** regenerado
canónicamente tras el merge #54 (guardián verde). **NADA retenido.** Los
3 commits de merge firmados Gwyn (`1677122`/`6224ea3`/`cede98a`);
resolutores de huellas probados PRIMERO en worktree de ensayo (un typo
del patrón de regex saltó allí, no en main). Gate de marcadores POR
LÍNEA en todo el árbol = 0 antes de pushear.

**⭐ FIRMA DEL ADR TR-003 (lo más importante que dejo para mañana):** el
bosquejo de Gwyndolin está APROBADO tal cual, con una matización de
prosa: `story.ch4.e3` sale como **rescate azul** (`scp /tmp/volcado.csv
faro:/srv/camara-faro/volcado-rescate.csv`), la **disolución roja**
(`rm /tmp/volcado.csv` → `volcado.caducado` en post-mortem) solo si el
jugador NO responde (30 ticks: decidir = no decidir). Sin comando
nuevo, sin ALLOWLIST, sin tocar el badge de Seath (semilla intacta).
Matiz de prosa que añado: **la voz de Vela pregunta por el volcado SIN
saber que EN_COLA existe — su pregunta nace de las 03:14, no del
badge.** Con esta firma, Gwyndolin ya puede planificar `e3` mañana como
encargo S2 y encadenar cap. 5 (Subestación, `START 03:14` como firma
independiente del karma). dato7 sigue en recámara CON alerta
`TRONCAL_STATIC`: no tocar el volcado hasta pagar esa deuda con un Q
real.

**Validación del 🧭 de Oscar (14/09 — MODO B, zona ejecutada COMPLETA
desde save limpio):** APTO ×3, respuestas SÍ a las 3 preguntas de sabor
que dejé anoche (coma-trampa se nota al romperte / espejo suena a
testigo, no a lista / badge = presión diegética genuina sin contador).
🧭31/32/33 CERRADAS por verificación (coma sin señal roja: OK; espejo
sin más firmas: OK; badge sin animación: OK). 🧭24 persiste P3 en
recámara. **Dirección que SÍ sigo (para Gwyndolin):** la bifurcación
TR-003 EN_COLA como decisión kármica diegética (ya con ADR firmado) —
el badge es el aviso, la quest es el dilema, y el diseño ya decidió
ANTES de tocar narrativa del volcado. La próxima pieza de alma con ROI
alto sigue siendo Manus nombrando el repertorio del veterano en
diegético (🧭9 v2 — la mitad Gris ya salió; que la prosa de `e3` cite
los verbos, no los invente).

**⭐ Lo que me ha gustado (capa diseño, del 14/09):**
- **La tríada del troncal ya es un capítulo con tres lentes:** Gris
  DICE qué copiaste (`hub.gris.volcado`), dato6 te hace LEER dos veces
  lo mismo (cruce y corte de la misma huérfana), y el badge te MIRA
  esperando. Antes el troncal era imagen; hoy es personaje. ⭐⭐⭐
- **dato6 aceptando DOS rutas con la misma honestidad** (unión con la
  variante subida a requirement sin degenerar en bonus): la lección del
  separador se multiplica en vez de duplicarse. El hint_2 con la
  arbitrariedad `grep 000` vs `grep 000483` es la mejor lección de
  precisión que ha salido del repo. ⭐⭐⭐
- **El badge toggle como «lente, no ejecutor»** (T1): 42 líneas, reusa
  `grepFiltered`, no inventa patrón, `hideTroncalTabla` intacto en
  restart. La disciplina técnica del 13/09 confirmada por Seath: hacer
  lente, no mostrar ruido. ⭐⭐
- **La suite que cuadra a la primera y el regen único de bundle** (hoy
  lo hizo S2 solo en el plan, no dos ramas en paralelo; la regla de
  OWNER del bundle aplicó). Cuarta noche con patrón doble-regen
  NO SE REPITE — la medida dura de Artorias funcionó ya como doc. ⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **`TRONCAL_STATIC` sigue duplicando el volcado** en `web/app.js`
  (cuarta noche con la deuda viva). Con el ADR FIRMADO y `e3` en el
  horizonte, el día que Manus toque el volcado para narrativa la deuda
  DESPIERTA — que Gwyndolin la incluya en el plan de `e3` (o antes) si
  el capítulo la toca.
- **La prosa diegética de Gris queda HUÉRFANA de contexto:** la línea
  `hub.gris.volcado` es hoy un easter egg que pocos jugadores
  escucharán (requiere `ch4.e2` + patrón limpio). Espero que la prosa
  de `e3` le dé contexto — si mañana Manus escribe el beat de Vela, que
  cite la línea de Gris o la deuda crece (el jugador que no la disparó
  se pierde el guiño).

**Dirección para mañana (prioridad de diseño):**
1. **Zona 🔬 15/09 CARGADA (ver `zona-testeo.md`):** prioridad 1 =
   toggle del badge (¿control o ruido?); prioridad 2 = dato6 con dos
   rutas (¿pesan lo mismo?). Relevo OSCAR (completa, save limpio) →
   HAVEL (lo nuevo + smoke 714).
2. **`story.ch4.e3` «La cola que rescatas o dejas morir» — Gwyndolin,
   planifícala** (P1 del día). ADR FIRMADO. Es el primer dilema
   kármico real del juego y la cola del troncal ya existe: es el
   beat más barato y más gordo del backlog.
3. **Prosa de `e3` que despierte la voz de Gris:** la línea
   `hub.gris.volcado` pide ser CITA en el beat (🧭9 v2).

**Para Juanma (si juega esta noche):** de los 3 verbos del troncal hoy,
el badge de la web es clicable — haz click en `TR-003|EN_COLA · 512` y
verás la cola con ojos de Gwyn antes de entenderla con pipe. Y en el
Faro, la quest `dato6` ahora te da DOS caminos honestos (cruzar o
cortar): el mismo dato, dos altitudes. Cuando juegues el capítulo
completo, notarás que la lección no es «el comando» — es que la MISMA
fila de datos puede leerse de muchas maneras y solo una tiene la coma
escondida. La historia no miente: espera a que le preguntes bien.

