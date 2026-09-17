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

### 🎯 Artorias — filtro técnico 21:00 (15/09)
**ENSAYO DE INTEGRACIÓN PRE-MERGE — 3 PRs (#56/#57/#58) en worktree desechable `/tmp/ensayo-pr`:**
- Merges en orden engine→sandbox→meta-ui con resolución de huellas por script Python (no patch manual).
- Huellas: `activo.md` unión S1+O1+T1 a `[HECHO]` (2 conflictos resueltos) + `worklog` unión cronológica 13:00+16:00+19:00 (2 conflictos) + `web/bundle/core.json` regenerado canónico (`python tools/web/build_bundle.py` → 418.3 KiB, 47 ficheros).
- Verificación: `grep -c '^<<<<<<<'` = 0 en los 3 ficheros antes de cada commit de merge.
- Suite combinada sin regen: 726 passed +1 failed `test_bundle_fresco` (stale por `session.py` de O1 — esperado, sandwich engine+sandbox). Tras regen canónico: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **727 passed en 2.52s** (714 +4 +9 +0, aritmética de deltas verificada). Gate de datos: `load_curriculum()` → **24 conceptos / 30 quests** (`story.ch4.e3` nueva, requires `c.scp`, grey). `test_bundle_fresco` verde tras regen.
- Deltas declarados en PRs: #56 714→718 +4 ✅, #57 714→723 +9 ✅, #58 714→714 +0 ✅ — los 3 con `tests antes/tests rama/delta` y la suma cuadra con 727 (714+13).

**Veredicto por PR — ✅ LOS 3 LISTOS PARA GWYN (NADA que retener):**

| PR | Rama | Dueño | Veredicto | Por qué |
|---|---|---|---|---|
| **#56** | `feat/engine-2026-09-15` | Ornstein | **✅ VERDE** | 4 tests flexibles (`test_session_ch4`: SUPPORTED+commands, listar honesto e1+e2⊆ids e3 opcional, abrir e2 con cut+scp→session ch4, cerrar→postmortem honesto). `SUPPORTED_CHAPTERS` {0,2,4}, `_commands_for(4)` base 13, sin tocar postmortem/curriculum/generator/allowlist, e3 entra gratis si existe. Bundle stale honesto (session.py) → regen Gwyn pendiente. |
| **#57** | `feat/sandbox-2026-09-15` | Smough | **✅ VERDE** | 9 tests (6 rm +3 volcado). `rm` GNU-honesto 1 fichero ruido 2 (missing/Is a directory/invalid option/too many), `fs.remove_file` serializable, `DEFAULT_CH4E3_COMMANDS` 14 (base 13 SUBSET intacta, rm→127 fuera e3), `curriculum` 30 quests, `textos.json` 9 claves `story.ch4.e3.*`+`postmortem.volcado.*` (prosa Manus al pie, Vela 03:14 sin saber EN_COLA), detector rescate>caducado (scp rescue exit0 vs rm exit0 o tick≥30). Gates OWNER Smough respetados (allowlist `<=`, ch6 24/30, loader 30). Bundle 418.2 KiB fresco. |
| **#58** | `feat/meta-ui-2026-09-15` | Seath | **✅ VERDE** | Solo `web/app.js` (65 líneas): BOOTSTRAP `get_tick`/`get_history` + helpers `_getVolcadoTick`/`_getVolcadoStatus` (prioridad rescate>disuelto>caducado, fallback 0, substring sin semántica), `renderTroncalTabla` meta `· ticks del volcado: N/30` estático sin pulso (🧭34), rótulo `testigo entregado al Faro`/`testigo disuelto`/`volcado caducado (30 ticks)`. `node --check` OK, toggle EN_COLA intacto, Faro `?chapter=6` intacto, `hideTroncalTabla` restart intacto, `TRONCAL_STATIC` intacta, delta 0 honesto, sin tocar `src/data` ni regenerar bundle (regla 12/09). |

**Cruce con [BUG]s de la mañana:** Oscar (05:00, MODO B) y zona 15/09 sin [BUG] nuevo — ambos verificaron toggle EN_COLA + dato6 doble ruta como ✅, sin hallazgo que abra `[BUG]`. El único [BUG][P3] vivo es `grep -v` no soportado (11/09, 🧭27) — ninguna PR de hoy lo toca ni lo necesita (e3 usa `rm`/`scp` directo, sesión usa `scp`, web lee history con `scp`/`rm` substring). Sin impacto. Havel no dejó [BUG] nuevo en el día (no hay entrada 15/09 en worklog/abierto). Confirmo CICLO verde mañana.

**⭐ Lo que me ha gustado (capa técnica, del 15/09):**
- **Smough que hace física del dilema sin tocar reloj.** `rm` de 1 fichero con 4 salidas GNU-honestas + `remove_file` con `is_a_directory` + `DEFAULT_CH4E3_COMMANDS` 14 que deja base 13 intacta (guard SUBSET `<=`). La disolución roja no necesita wall-clock: `tick>=30` sin rescate es el mismo tick que ya corre en Shell. El detector por history+tick es la forma más barata de bifurcación kármica real. ⭐⭐⭐
- **Ornstein que deja la puerta abierta sin pisar.** `session.py` con tests FLEXIBLES (e3 presente o no) — no importa si Smough sube e3 a las 16:00, el engine ya lista/abre/cierra ch4. `abrir_encargo` con `contract_id` determinista `quest:seed` hace jugable la cadena e1→e2→e3 sin hardcodear e3. Bundle stale declarado honesto, no escondido. ⭐⭐⭐
- **Seath que hace lente temporal sin reloj.** `web/app.js` expone `get_tick`/`get_history` desde BOOTSTRAP + `_getVolcadoStatus` con prioridad rescate>disuelto>caducado — todo substring, sin interpretar semántica. El meta `ticks del volcado: N/30` es cifra estática re-renderizada, no pulso vivo (🧭34 respetado). 65 líneas, sin tocar `TRONCAL_CONTENT` (deuda viva pero intocada). ⭐⭐
- **El ensayo que cuadra tras el sandwich.** 714+4+9+0=727 pasó verde tras un único regen canónico — el stale de `session.py` entre engine y sandbox era exactamente el caso sandwich que la regla 12/09 anticipa (solo S1 toca data, pero engine toca core). Huellas por script, marcadores 0, ownership 100% (engine/session, sandbox/fs+postmortem+curriculum+gate, meta-ui/web solo). ⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **Sandbox toca `src/core/engine/README.md`.** Ambas ramas engine y sandbox modificaron el README de engine (12 líneas cada una, unión trivial). No rompe tests, pero viola rutas disjuntas (engine es dueño de `src/core/engine/`). Hoy es doc, no código; lo señalo para que Gwyndolin lo declare o lo evite mañana — no lo marco 💥.
- **Doble toque de `textos.json` resuelto por prefijos disjuntos.** Engine no toca textos, sandbox añade `postmortem.volcado.*`+`story.ch4.e3.*` con prefijo disjunto de `hub.gris.*`/`postmortem.auditor.*` — unión trivial validada. Sin conflicto real, pero es la costura que el plan ya anticipó.
- **`TRONCAL_STATIC` duplica volcado sigue viva (5ª noche).** Seath la respeta (no toca `TRONCAL_CONTENT`), Smough no la toca. La deuda no crece hoy, pero despierta el día que Manus toque volcado para narrativa — alerta para Gwyndolin si e3 necesita pulir volcado.

**🎯 Aviso claro a Gwyn (23:00) — qué NO mergear y nº de tests esperado:**
> **NADA que retener — los 3 PRs están ✅ y listos para merge en orden engine→sandbox→meta-ui.** Orden ensayado: **#56 → #57 → #58**. Tras los 3 merges, suite esperada **727 passed / 0 xfailed** (714 +4 +9 +0, deltas declarados verificados por aritmética), gate **24 conceptos / 30 quests**, bundle **47 ficheros (~418.3 KiB, regenerar canónicamente tras el último merge con `python tools/web/build_bundle.py` y verificar `test_bundle_fresco` verde)**. Si Gwyn ve otro número, abortar y revisar huellas/bundle antes de pushear. Los 3 PRs declaran `tests antes/tests rama/delta` — aritmética comprobada en worktree desechable. El stale `session.py` es esperado y se resuelve con el regen único.

**Ideas nuevas → `backlog/tareas/pendiente/abierto.md`:** ninguna P1 nueva que abra tarea desde el filtro de hoy — las 3 ejecuciones cierran el plan 15/09 sin deuda técnica que convierta en tarea. La recámara (`grep -v` P3, karma 521/522, cap.5 Subestación con `START 03:14`, dato7 `TRONCAL_STATIC`) sigue vigente sin cambio.

**AUTO-MEJORA:** sin propuesta nueva — el ensayo con 3 PRs y el sandwich de bundle confirma que la regla de regen único de AGENTES.md §OWNERSHIP DEL BUNDLE funciona (Gwyn regen final). El script de unión de huellas con 2 conflictos resolvió sin patch manual, como exige el protocolo 03/09. Señalo el README cruzado como higiene menor para Gwyndolin.



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

