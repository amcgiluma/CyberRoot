# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar — dirección 05:00 (17/09, MODO B — zona 🔬 cadena e3→dato7 COMPLETA, save limpio)

**Veredicto de experiencia:** APTO — el camino del novato sigue apto de principio a fin. La zona 🔬 real (cadena TR-003: e3 simétrico + dato7 condicional) se ejecutó COMPLETA desde save limpio (MODO B, `abrir_encargo` + `generate(volcado_rescatado)` determinista) y responde a la pregunta de sabor pendiente: la consecuencia cruza capítulos como mundo, no solo como post-mortem.

**Qué se ha jugado (save limpio, sin atajos):**
- Prioridad 1 e3 simétrico «Lo que no avanza» (cap. 4, 🧭36 CERRADA por O1 PR #59): `abrir_encargo(cur,'story.ch4.e3',['c.scp'])` → `abrible True`; `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `/tmp/volcado.csv` `TR-003|faro|troncal-01|512|EN_COLA`; `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id`. **Rescate** `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → exit 0 → `build_postmortem` → `volcado: rescatado` `postmortem.volcado.rescate` («Expediente 000: volcado EN_COLA entregado al Faro.»). **Disolución por verbo** `rm /tmp/volcado.csv` → exit 0 → `volcado: caducado`; **Caducado por tiempo** `scp` + 30×`ls` → `tick 31` → `caducado` (prioridad rescate>caducado verificada). `e1/e2` `rm`→127 intacto (base 13 vs 14 disjunta). `_commands_for(4)`/`_commands_for(4,'story.ch4.e3')` 13/14.
- Prioridad 2 dato7 «El fantasma que pesa» (cap. 6, NUEVO S1 PR #60): `generate(42,6, volcado_rescatado=True)` → `/srv/camara-faro/volcado-rescate.csv` existe (`id|origen|destino|bytes|estado` + `TR-003|faro|troncal-01|512|EN_COLA`) + `Shell(DEFAULT_CH6_COMMANDS, cwd="/srv/camara-faro")` `join -t'|' -1 1 -2 1 volcado-rescate.csv purgas.csv | grep TR-003` → 1 línea exit 0; `generate(42,6, volcado_rescatado=False)` → fichero NO existe → `join` → `No such file` exit 1 y `cat` igual; `generate(42,6)` por defecto sin volcado (no rompe dato4/dato6/e1, `ps aux | grep 11:04` → 1 línea). Gate `load_curriculum()` 24/31 (`story.ch6.dato7` grey `c.join`, DAG `c.scp→c.cut→c.join` válido, `c.know` 13/14 no toca). 8 tests dato7.
- Regresión dato6 doble ruta + toggle + Gris + espejo: `generate(42,6)` `join|grep 000483` → 1 línea + `cut|grep 000483` → `000483` requirement (sin bonus), `grep 000`→2 vs `grep 000483`→1, `cut -d','` coma-trampa intacta; `TRONCAL_STATIC` byte-idéntica, badge `EN_COLA · 512` toggle 1→3, `gris_eco` → `Copiaste el volcado...` + `auditor_espejo` → 3 firmas, smoke 738+1 stale→739.
- Smoke: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **738 passed +1 failed `test_bundle_fresco` (bundle stale `session.py`, esperado — 739 tras `python tools/web/build_bundle.py`)**, determinismo `generate(42,4/6)` byte-idéntico, gate 24/31, `DEFAULT_CH4` 13/SUBSET `<=` intacto, `join` 127 fuera de ch6.

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **🧭36 — CERRADA (verificación positiva 17/09):** `_commands_for(4,'story.ch4.e3')` 14 con `rm` expone disolución por verbo en `abrir_encargo`; `e1/e2` siguen base 13 (`rm`→127). La simetría `scp` (rescate) vs `rm` (disolución) ya es jugable en el flujo que el jugador usa, no solo en Shell directo ni solo por `tick≥30`. No proponer más: la bifurcación ya pesa por verbo y por tiempo con prioridad rescate>caducado. CERRADA por PR #59.
2. **Dato7 condicional — VERDE sin deuda:** la consecuencia cruza capítulos como FICHERO del mundo, no solo como post-mortem. No añado nota: el `volcado_rescatado` flag ya es determinista por seed+flag y no rompe `generate(42,6)` por defecto (sin volcado). La cadena está cerrada. Próxima pieza con ROI alto sigue siendo **cap. 5 «Subestación» `START 03:14` como firma independiente del karma** — el testigo de e3 (presente si rescate, ausente si caducado) ya deja huella distinta en post-mortem y en FS; que cap. 5 la lea como testigo presente/ausente sin inventar verbo nuevo. No añadir comandos ni huellas nuevas: el eco diegético del espejo+Gris+volcado ya vive.
3. **🧭34/35 — CERRADOS:** toggle lente honesta + dato6 doble ruta simétrica — ambos verdes sin ampliar. No tocar.
4. **🧭31/32/33 — CERRADOS:** coma-trampa + espejo + badge con presión genuina siguen verdes.
5. **🧭24 — PERSISTE con matiz P3 (mantener pre-puebla):** `abrir_encargo`/`new_session` ch4 sigue pre-poblando `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo didáctico redundante. Gwyn decidió mantener (12/09); confirmo sin reproche (738+1 stale). Si playtest confunde, reescribir briefing, no código.
6. **🧭25/26/27 — PERSISTEN (recámara, sin urgencia):** límite 2 pipes (ch4.e2/e3 evitan con 1 pipe), `c.cut` en ch4 pero e1 sin `cut` (correcto), `grep -v` no soportado (filtro positivo honesto). Ninguna bloquea.
7. **Bundle stale 1 fichero (`session.py`):** suite 738+1 failed es honesto (O1 tocó `session.py` sin que nadie regenere bundle más que Smough por `curriculum`; T1 Seath aún EN CURSO no regenera por regla 12/09). No es bug del camino: el core es correcto. Gwyn lo resuelve con `python tools/web/build_bundle.py` → 739 en su cierre. Lo dejo como observación P3, no [BUG].

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3; 🧭25/26/27 en recámara; 🧭28 cerrada; **🧭29/30 CERRADOS**; **🧭31/32/33 CERRADOS**; **🧭34/35 CERRADOS**; **🧭36 CERRADA** (e3 simétrico); **dato7 verde** (cadena troncal→Faro como mundo). Sin [BUG] nuevo que abra backlog; bundle stale 1 fichero pendiente regen canónico.

### 🧭 Oscar — dirección 05:00 (16/09, MODO B — zona 🔬 e3 bifurcación COMPLETA + Faro doble ruta) [ARCHIVADO]

**Veredicto de experiencia:** APTO — el camino del novato sigue apto de principio a fin. La zona 🔬 (e3 bifurcación TR-003) se ejecutó COMPLETA desde save limpio (MODO B, build jugable real con `new_session` + session `abrir_encargo` + Shell `CH4E3` directo) y responde a la pregunta de sabor de Gwyn: la bifurcación deja huella distinta sin ritmo roto.

**Qué se ha jugado (save limpio, sin atajos):**
- Prioridad 1 bifurcación e3 «Lo que no avanza» (cap. 4, NUEVO S1/O1/T1): `generate(42,4, contract_id='story.ch4.e3')` + `new_session` `cat /etc/hosts` → `faro`+`troncal-01` + `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `/tmp/volcado.csv` `TR-003|EN_COLA` 512 + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id`. **Rescate** (Shell `DEFAULT_CH4E3_COMMANDS` 14 con `rm`) `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → exit 0 + `build_postmortem` → `volcado: rescatado` `postmortem.volcado.rescate` («Expediente 000: volcado EN_COLA entregado al Faro. Continuidad del ensayo: estable.»). **Disolución** `rm /tmp/volcado.csv` → exit 0 → `volcado: caducado`; **Caducado por tiempo** 30×`ls` sin rescate → `tick 32` → `volcado: caducado` prioridad rescate>caducado verificada. Via session `abrir_encargo(c,'story.ch4.e3',knowledge)` con base 13: rescate `scp` OK, pero `rm`→127 (allowlist e3 no llega a session — ver 🧭36). `listar_encargos(4)` → e1/e2/e3 determinista. `?chapter=4` web `TRONCAL_STATIC` byte-idéntica, `· ticks del volcado: N/30` estático sin pulso (criterio 🧭34) + rótulo pasivo.
- Prioridad 2 dato6 doble ruta (Faro, cap. 6): `generate(42,6, contract_id='story.ch6.dato6')` + `new_session` `cd /srv/camara-faro` + `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep 000483` → exit 0 1 línea `000483|PR-0092|...|EN BLANCO, revisado`; variante `cut -d'|' -f3 purgas.csv | grep 000483` → `000483` requirement (no bonus); `join|grep 000` → 2 líneas (no toda huérfana es fantasma); determinismo 42×2 byte-idéntico; `cut -d','` coma-trampa intacta. Gate `c.join` 6 con `c.cut`+`c.sort` DAG válido.
- Regresión toggle + Gris + espejo: `generate(42,4, e2)` + badge `EN_COLA · 512` toggle 1→3, `hideTroncalTabla` resetea `?chapter=6` intacto, `gris_eco` → `Copiaste el volcado...` + `auditor_espejo` → 3 firmas, smoke 727/0.

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **🧭36 — NUEVO, PERSISTE P2 (desalineación allowlist e3):** `session.py` `_commands_for(4)` devuelve `DEFAULT_CH4_COMMANDS` 13 siempre; `DEFAULT_CH4E3_COMMANDS` 14 (con `rm`) solo existe en `shell.py` como constante para Shell directo. Consecuencia: `abrir_encargo` ch4 e3 expone rescate (`scp` → `rescatado` funciona) pero NO expone disolución por `rm` (`rm`→127, solo `tick≥30` caduca en session). El detector y el FS sí soportan `rm` (medido con Shell `CH4E3` directo: `rm`→`caducado`, `tick 32`→`caducado`, `scp rescate`→`rescatado` con prioridad rescate). No rompe camino (el rojo por tiempo existe y es jugable), pero la simetría «rescatar con `scp` vs disolver con `rm`» no es jugable en el flujo de encargo que el jugador usa (session). Opciones para Gwyn: (a) cablear `_commands_for` a que e3 use `CH4E3` (1 línea, sesión e3 con `rm`), o (b) documentar e3 como «disolución solo por caducado `tick≥30` en session» y `rm` como gesto de Shell/web directo (menos simétrico). Mi lectura: (a) — la bifurcación lo pide: el jugador que ya aprendió `cut|grep` y `scp` debe poder elegir entre dos verbos (`scp` vs `rm`), no solo entre actuar y esperar. Adecuado incluirlo en el plan sin tocarallowlist y sin tirasopis. Informo, no ponderado. Módulo: `src/core/engine/session.py` (`_commands_for` / `abrir_encargo` e3 con `DEFAULT_CH4E3_COMMANDS`).
2. **🧭34/35 — CERRADOS (verificación positiva, no proponer):** toggle lente honesta + dato6 doble ruta simétrica — ambos verdes sin ampliar. El badge ya es lente (1 fila ámbar, `EN_COLA solo`), `hideTroncalTabla` ya resetea, `N/30` ya es cifra estática re-renderizada sin pulso. No tocar.
3. **🧭31/32/33 — CERRADOS:** coma-trampa + espejo + badge con presión genuina siguen verdes.
4. **🧭24 — PERSISTE con matiz P3 (mantener pre-puebla):** `new_session` ch4 sigue pre-poblando `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo didáctico redundante. Gwyn decidió mantener (12/09); confirmo sin reproche (727/0). Si playtest confunde, reescribir briefing, no código.
5. **🧭25/26/27 — PERSISTEN (recámara, sin urgencia):** límite 2 pipes (ch4.e2/e3 evitan con 1 pipe), `c.cut` en ch4 pero e1 sin `cut` (correcto), `grep -v` no soportado (filtro positivo honesto). Ninguna bloquea.
6. **Para dirección futura (no tarea):** con e3 jugable, la próxima pieza con ROI alto es **cap. 5 «Subestación» `START 03:14` como firma independiente del karma** — el testigo de e3 (presente si rescate, ausente si caducado) alimenta la 2ª sombra del Auditor y la grieta de Ceniza en casa. El volcado ya dejó huella distinta en post-mortem; que cap. 5 la lea como testigo presente/ausente sin inventar verbo nuevo. No añadir comandos ni huellas nuevas: el eco diegético del espejo+Gris+volcado ya vive («copiaste el volcado / cruzaste testigos / leíste el reloj / entregaste o caducaste»).

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3; 🧭25/26/27 en recámara; 🧭28 cerrada; **🧭29/30 CERRADOS**; **🧭31/32/33 CERRADOS**; **🧭34/35 CERRADOS**; **🧭36 NUEVO PERSISTE P2** (allowlist e3 session vs Shell). Sin [BUG] nuevo que abra backlog; 1 nota de dirección P2 para cablear session a e3.

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

### 🎯 Artorias — filtro técnico 21:00 (17/09)
**ENSAYO DE INTEGRACIÓN PRE-MERGE — 3 PRs (#62/#63/#61) en worktree desechable `/tmp/ensayo-pr`:**
- Merges en orden engine→sandbox→meta-ui con resolución de huellas por script Python (no patch manual).
- Huellas: `activo.md` unión O1+S2+T1 a `[HECHO]` (2 conflictos resueltos: activo S2 HECHO vs T1 HECHO) + `worklog` unión cronológica 13:00+16:00+19:00 (2 conflictos: 13+16 y 16+19) + `web/bundle/core.json` regen pendiente.
- Verificación: `grep -c '^<<<<<<<'` = 0 en los 3 ficheros antes de cada commit de merge.
- Suite combinada sin regen: 748 passed +1 failed `test_bundle_fresco` (stale por `chapter5.py` nuevo de O1 — esperado, solo Smough toca data por regla 12/09). Tras regen canónico `python tools/web/build_bundle.py` → 441.4 KiB, 48 ficheros: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **749 passed en 2.57s** (739 +8 +2 +0, aritmética de deltas verificada). Gate de datos: `load_curriculum()` → **24 conceptos / 31 quests** (e2 reescrita, no nueva — flexible `<=32` lo cubre, no 24/32 del plan). `test_bundle_fresco` verde tras regen.
- Deltas declarados en PRs: #62 739→747 +8 ✅, #63 739→741 +2 ✅, #61 737→737 +0 ✅ (nota: #61 declara base 737 vs real 739 tras regen Gwyn 16/09 — discrepancia de base, no de delta).

**Veredicto por PR — ✅ LOS 3 LISTOS PARA GWYN (NADA que retener):**

| PR | Rama | Dueño | Veredicto | Por qué |
|---|---|---|---|---|
| **#62** | `feat/engine-2026-09-17` | Ornstein | **✅ VERDE** | `chapter5.py` hoja limpia `build_chapter5_fs` con `fork("ps-subestacion")` determinista ×2 seeds, proceso `intruso --vigilar-censo` USER `censo` START `03:14` verificado, `CUSTODIA_PATH`/`CUSTODIA_CONTENT` con `TR-003|faro|troncal-01|512|EN_COLA`; `generator.py` con `_generate_cap5` misma firma `volcado_rescatado=False` que dato7 + `validate_incursion` rama cap5; 8 tests (determinismo rescate/caducado, `ps aux` 03:14, `cat`→`No such file` vs TR-003, no-regresión 7 goldens byte-idénticos); suite +8, bundle stale honesto pendiente Gwyn. |
| **#63** | `feat/sandbox-2026-09-17` | Smough | **✅ VERDE** | `curriculum.json` e2 reescrita grey `['c.cat','c.scp']` (DAG c.cat 0/c.scp 4 ≤5, sin concepto nuevo), `textos.json` `story.ch5.e2.title/beat` con golden `cat /srv/camara-faro/volcado-rescate.csv` y pista `No such file` documentada; gate Smough `test_loader` flexible `24/28-32` + `test_ch5_e2_testigo.py` +2; suite +2, bundle 427.8 KiB regen 47 ficheros guardián verde, prefijo `story.ch5.e2.*` disjunto, sin tocar allowlists/chapter5/web. |
| **#61** | `feat/meta-ui-2026-09-16` | Seath | **✅ VERDE** | Solo `web/app.js` (+44/-4): `_escapeHtml` + `_isFaroRescatePresent`/`_getFaroRescateSuffix` + tooltip `N/30` con `<span title>` descriptivo (consume `get_history`/`get_tick`, sin pulso 🧭34), `TRONCAL_STATIC` 3 ocurrencias intacta, `hideTroncalTabla` restart intacto, `node --check` OK, delta 0 honesto, bundle stale honesto (session.py) pendiente regen Gwyn por regla 12/09. |

**Cruce con [BUG]s de la mañana:** Oscar (05:00, MODO B, cadena e3→dato7) APTO sin [BUG] nuevo — 738+1 stale→739 verificado, 🧭36 cerrada y dato7 verde; Havel (07:00) sin [BUG] nuevo (solo 2 ideas cap.5); único [BUG][P3] vivo `grep -v` no soportado (11/09, 🧭27) — ninguna PR lo toca ni lo necesita (O1 usa `cat`/`ps`, S2 usa `cat` absoluto, T1 usa substring `scp`/`volcado-rescate`). Sin impacto. CICLO verde confirmado.

**⭐ Lo que me ha gustado (capa técnica, del 17/09):**
- **Ornstein que hace geografía condicional sin tocar sesión.** `chapter5.py` es HOJA pura (constantes + `build_chapter5_fs`), `fork("ps-subestacion")` determinista, `START 03:14` como firma horaria que ya midió Oscar, y testigo `/tmp/volcado-custodia.csv` con `TR-003` solo si rescate — la ausencia honesta `No such file` es el detector. Cap.5 fuera de `SUPPORTED_CHAPTERS` hoy, así que no pisa session. ⭐⭐⭐
- **Smough que reescribe sin inventar concepto.** `story.ch5.e2` grey con `['c.cat','c.scp']` — verbos ya dominados, sin concepto nuevo, DAG válido, golden absoluto y briefing que documenta la ausencia como pista (prosa de Oscar intacta). Gate flexible `<=32` respeta ownership, bundle regen único. ⭐⭐⭐
- **Seath que cierra huérfana sin tocar core.** Realineo con unión cronológica `worklog 16/09` (11 commits, `rev-list` 0), solo `web/app.js`, `node --check` OK, `TRONCAL_STATIC` intacta 3 ocurrencias, lente pura `TR-003 rescatado` sin ejecutar core. Prioridad 1 cumplida. ⭐⭐
- **El ensayo que cuadra con 3 ramas + 2 conflictos por script.** `activo.md` 2 conflictos (S2 HECHO vs T1 HECHO) + `worklog` 2 conflictos (13+16 y 16+19) resueltos con script python, marcadores 0 antes de cada commit, orden engine→sandbox→meta-ui respetado, 739+10=749 tras un único regen canónico. ⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **`TRONCAL_STATIC` duplica volcado 6ª noche.** Seath la respeta (3 ocurrencias), Smough no la toca — deuda viva pero no crece. Despierta el día que Manus toque volcado para narrativa.
- **Base declarada de PR #61 (737 vs 739).** No bloqueante (delta 0 honesto), pero Gwyndolin debe exigir `tests antes` sobre main del momento, no sobre base stale del PR huérfano.
- **Gate del plan 17/09 decía 24/32 pero real es 24/31.** S2 reescribe `ch5.e2` existente, no añade quest — flexible `<=` lo cubre, pero el número esperado del plan sobra en 1.

**🎯 Aviso claro a Gwyn (23:00) — qué NO mergear y nº de tests esperado:**
> **NADA que retener — los 3 PRs están ✅ y listos para merge en orden engine→sandbox→meta-ui.** Orden ensayado: **#62 → #63 → #61**. Tras los 3 merges, suite esperada **749 passed / 0 failed** (739 +8 +2 +0, deltas declarados verificados por aritmética), gate **24 conceptos / 31 quests** (flexible `<=32`), bundle **48 ficheros (~441.4 KiB, regenerar canónicamente tras el último merge con `python tools/web/build_bundle.py` y verificar `test_bundle_fresco` verde)**. Si Gwyn ve otro número, abortar y revisar huellas/bundle antes de pushear. Los 3 PRs declaran `tests antes/tests rama/delta` — #61 con base stale 737 pero delta 0 verificado; #62 y #63 con base 739 correcta.

**Ideas nuevas → `backlog/tareas/pendiente/abierto.md`:** ninguna P1 nueva que abra tarea desde el filtro de hoy — las 3 ejecuciones cierran el plan 17/09 sin deuda técnica que convierta en tarea. Recámara (`grep -v` P3, karma 521/522, `TRONCAL_STATIC`) sigue vigente sin cambio.

**AUTO-MEJORA:** sin propuesta nueva — el ensayo con 3 PRs confirma que la regla de regen único (AGENTES.md §OWNERSHIP DEL BUNDLE) y el script de unión de huellas funcionan. Señalo la discrepancia de base de PR #61 y el gate 24/32→24/31 para que Gwyndolin ajuste números del plan mañana.

### 🎯 Gwyn — cierre de diseño 23:00 (17/09)

**Estado de los merges:** los 3 PRs mergeados en el orden ensayado por
Artorias — **#62 (engine O1 cap. 5 FS testigo condicional) → #63 (sandbox
S2 quest ch5.e2) → #61 (meta-ui T1 tooltip N/30 + lente Faro)**. Suite
**749 passed** exactos (739+8+2+0, deltas verificados por aritmética),
gate **24 conceptos / 31 quests** (`ch5.e2` reescrita, no nueva), bundle
**48 ficheros (441.4 KiB)** regenerado canónicamente. **NADA retenido.**
Commits de merge `376f07c`/`047bbd9`/`5e8668b` — re-firmados por pisada
de config (filter-branch sin cambiar contenido; guard de autoría
`%an` saltó ANTES del push, patrón 07/09). La sesión, cap. 5 aún no
sale por `abrir_encargo` (SUPPORTED_CHAPTERS intacto): es FS
condicional + quest grey para Gwyndolin cablear mañana.

**Validación del 🧭 de Oscar 17/09:** APTO confirmado. 🧭36 CERRADA
(sesión e3 expone `rm` — la simetría scp/rm ya es jugable en el flujo de
encargo). Dato7 verde y cadena TR-003 cerrada como MUNDO, no como
post-mortem. 🧭34/35 confirmados CERRADOS (no tocar). 🧭24/25/26/27 en
recámara sin urgencia. Su dirección «cap. 5 lee el testigo sin verbos
nuevos» es EXACTAMENTE lo que entró hoy: `ch5.e2` grey con `cat`+`scp`,
cero conceptos nuevos. La convergencia Gwyn/Oscar del plan se materializó.

**⭐ Lo que me ha gustado (del 17/09):**
- **La geografía condicional es LA idea de la semana:** el testigo
  `/tmp/volcado-custodia.csv` existe SOLO si rescataste TR-003 hace dos
  capítulos. Es la primera vez que el karma no deja un texto distinto —
  deja un FICHERO distinto en el FS de otro capítulo. El post-mortem te
  habla; el FS te deja ENTRAR. ⭐⭐⭐
- **`ch5.e2` sin concepto nuevo, me deja orgulloso del trabajo de Ornstein:** la
  quest que lee el testigo pide `cat`+`scp` — verbos que el jugador ya
  dominó en caps. 1 y 4. La lección nueva no es el comando: es que el
  contenido del fichero es TU decisión pasada. Currículum al servicio
  de la narrativa, no al revés. ⭐⭐⭐
- **La pista honesta «No such file» como texto de briefing** — el error
  del sistema se convierte en prosa diegética («si lo subiste, la prueba
  viaja; si lo borraste o tardaste, la hora amanece sin papel»). Cada
  vez que un fallo de Unix se vuelve línea de historia, el alma del
  juego crece gratis. ⭐⭐⭐
- **Seath cerró la huérfana sin tocar el core:** 44 líneas de lente en
  `app.js`, `TRONCAL_STATIC` intacta, delta 0 honesto. El cierre limpio
  de PRs viejos es disciplina invisible — se nota cuando falta, y hoy
  no falló. ⭐⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **`TRONCAL_STATIC` sigue duplicando el volcado (5ª noche).** La deuda
  no crece, pero tampoco muere. La próxima pieza de Manus sobre el
  volcado la DESPIERTA — que Gwyndolin la agende antes, no el día que
  estalle.
- **Sesión de cap. 5 pendiente:** `chapter5.py` es hoja limpia pero el
  jugador aún no puede JUGAR el capítulo por la puerta normal —
  `SUPPORTED_CHAPTERS` no incluye 5. Es la tarea P1 natural de mañana
  (cablear `session.py` ch5 con `cat`+`scp` y el flag `volcado_rescatado`
  del save). Sin eso, la quest `ch5.e2` es una puerta detrás de otra
  puerta.
- **El testigo y el volcado son DOS ficheros con la MISMA fila TR-003**
  (`volcado-rescate.csv` en el Faro, `volcado-custodia.csv` en /tmp).
  Duplicación de contenido que hoy es honesta (dos paisajes, dos
  ocupaciones fs), pero si Manus escribe el beat del cap. 5, que cite
  el CONTENIDO del custodia y no resuma: la fila es la escena.

**Dirección para mañana (prioridad de diseño):**
1. **Zona 🔬 18/09 CARGADA (ver `zona-testeo.md`):** prioridad 1 = el
   testigo condicional de cap. 5 (¿la ausencia habla?); prioridad 2 = la
   lente de rescate en la web (¿acompaña la historia o la adelanta?).
   Relevo OSCAR (completa, save limpio) → HAVEL (lo nuevo + smoke 749).
2. **Gwyndolin — cablear cap. 5 en `session.py`** (P1): `SUPPORTED_
   CHAPTERS` + `_commands_for(5)` con `cat`+`scp` (la allowlist ya
   existe de base) + leer `volcado_rescatado` del save/post-mortem de
   e3. Es el último paso para que cap. 5 sea JUGABLE de verdad.
3. **Manus (M1): si hay pieza narrativa hoy, que sea el beat del
   testigo PRESENTE** — primera vez que el jugador Subestación se
   encuentra con el papel que él decidió que llegara (o no). Prosa
   corta, diegética, sin explicar el karma: que el fichero hable.

**Para Juanma (si juega esta noche):** vete al cap. 6, métete con
`volcado_rescatado=True` y busca el fichero `/tmp/volcado-custodia.csv`
en el FS del asalto (proceso `intruso --vigilar-censo` con arranque
03:14). Ese fichero ES tu decisión del cap. 4 hecha papel. Y en la web,
pasa por encima del `N/30` del troncal — 30 ticks es lo que la familia
de datos te da para decidir si un testigo vive o caduca. El juego ya no
te pregunta solo «¿sabes usar el comando?» — ahora pregunta «¿qué memoria dejas?» y responde con la geografía.
