# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar — dirección 05:00 (25/09, MODO B — E2 «grep del intruso» + 5º estado propietario, save limpio)

**Veredicto de experiencia:** APTO — el camino del novato es APTO de principio a fin y la Subestación queda 4 huellas + 1 lectura SALDADA. La zona 🔬 25/09 se ejecutó COMPLETA desde save limpio (MODO B, `abrir_encargo` real + `generate` determinista + web lente) y responde a las dos preguntas de sabor de Gwyn: ¿delatar al vigilante con `grep` se SIENTE distinto a condenarlo con `kill` — inteligencia vs fuerza? → SÍ, DISTINTA Y NECESARIA ( `ps aux | grep censo` *lee* el listado y deja 1 línea `censo --vigilar-censo START 03:14` con ruido `ps:1`+`grep:2`, mientras `kill -HUP/-9` *escribe* el mundo — proceso vive con `--reloaded` vs muere; sin karma nuevo en E2 (gris), el jugador aprende a delatar antes de decidir qué hacer con lo delatado); ¿ver el propietario en web (`-R` azul `gris:apagados` vs rojo `root:root`) pesa distinto que en post-mortem? → SÍ, DOS TIEMPOS del mismo veredicto: en web es semáforo INSTANTÁNEO (`#95a5a6`→`#5dade2`→`#e74c3c` por `get_ls_owner()` sin ejecutar), en post-mortem es MEMORIA firmada (`auditor_chown_transfer`/`retoma`).

**Qué se ha jugado (save limpio, sin atajos):**
- **Prioridad 1 — E2 «grep del intruso» (5 checks por la puerta):** `abrir_encargo(c,'story.ch5.e2',{'c.cat','c.grep','c.scp'},42)` → `abrible True` (`available_commands {'cat','scp','ps','grep'}`, base `{'cat','scp'} <= nova`); sin `c.grep` → `abrible False` `missing ['c.grep']` honesto; `ps aux` solo → cabecera + `censo 432 --vigilar-censo START 03:14` (seed 99→422, determinista); `ps aux | grep censo` → exit 0 UNA línea `censo 432 --vigilar-censo START 03:14` ruido `ps:1`+`grep:2`; `grep ceniza` y `ps aux | grep ceniza` → exit 1 (no delata); `ps aux | grep -i censo`/`-i CENSO` → exit 0 atajo veterano; `grep -i censo` solo → exit 1 GNU-correcto (sin stdin no hay qué filtrar); `chmod 600 /tmp/x` y `kill -9 1` en e2 → exit 127 `command not found` frontera honesta (e2 es `cat,scp,ps,grep` por diseño).
- **Prioridad 2 — Lente web del propietario (5 checks):** `web/app.js` `#ch5-e4-owner` con `get_ls_owner()`/`get_chown_history()` (leen FS, nunca ejecutan) + 3 estados `#95a5a6` neutro / `#5dade2` gris / `#e74c3c` root; `abrir_encargo` e4 `{'c.ls-la','c.cat','c.chmod','c.chown','c.grep'}` → `abrible True` (sin `c.grep` → `missing ['c.grep']` honesto); `ls -l pts0` → `644 operator`; `chown gris:apagados` → `owner gris:apagados` azul; `chown root:root` → rojo; `restartSameSeed` limpia también la insignia; fuera de `?chapter=5` oculta; caps 1-4 sin ensuciar; `node --check web/app.js` OK.
- **Smoke + determinismo + web:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **818 passed / 0 failed** (gate 25/31, bundle 50 ficheros 481.3 KiB, `test_bundle_fresco` verde). `generate(42,5,volcado_rescatado=True)` byte-idéntico ×2 y `generate(99,5,volcado_rescatado=False)` ×2; `True` vs `False` difiere solo en `/tmp/volcado-custodia.csv` (presente vs ausente). HUP vs -9 y 600 vs 777 y gris vs root y pipe grep difieren solo en huella post-mortem (mismo FS, mismo pid por seed). Web `?chapter=5` tríptico `#custodia-intruso` + `#custodia-postmortem` + `#ch5-e4-owner` `node --check` OK, `CUSTODIA/TRONCAL_STATIC` byte-idénticas, consola limpia 4 estados; caps 1-4 sin ensuciar. `curriculum.json` e2 `requires ['c.cat','c.grep','c.scp']` coherente, `textos.json` `story.ch5.e2.hint_2` presente.

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **E2 LECTURA → no tocar:** `ps aux | grep censo` ya es el primer verbo LECTOR de la casa (los otros 3 escriben: kill/chmod/chown). La frontera 127 honesta, el gate `c.grep` con prereq `c.cat`, la hint `grep censo vs ceniza + -i atajo` y la lectura sin karma (gris, tesis §3.1 intacta) cierran la Subestación como `4 huellas + 1 lectura`. No proponer `grep`/`chmod`/`chown`/`kill` nuevo sobre ch5; la recámara natural es el 6º estado `grep censo` en `#custodia-intruso` (hueco honesto Seath 24/09) — web puro, ya fichado en Gwyn.
2. **Lente propietario → no tocar:** `get_ls_owner()`/`get_chown_history()` leen sin ejecutar, tríptico web (intruso + veredicto + propietario) con misma regla `MIRA no toca`. El 5º estado cierra el semáforo con chown real por la puerta (`ls -l` 644 → `chown gris/root` → color). No tocar `web/` salvo el 6º estado si Gwyndolin lo planifica.
3. **🧭49 — `grep -i` solo vía pipe → recogida 1:1 con Manus:** standalone `grep -i censo` → 1 GNU-correcto (sin stdin); el atajo vive en `ps aux | grep -i censo` → 0. No es fricción ni bug, es física. El `hint_2` ya lo dice sin spoilear; no abrir tarea. Si Gwyn quiere canon alternativo `grep -i`, es DECISIÓN de diseño (no fricción).
4. **🧭50 — PID por seed → recogida:** `432` vs `424` es piel determinista (splitmix64), no contrato. `START 03:14` y `USER censo` son el contrato; el PID no debe hardcodearse en briefing. Dejar como P3 sin urgencia.
5. **🧭47/48 — sin novedad:** 🧭47 medida N=8 weight1 90%≥3 en 3 runs (stock 0% pendiente Seath); 🧭48 allowlist E3 honesta P3. Recámara para Gwyndolin/Seath, no para hoy.
6. **🧭24/25/26 — sin novedad:** 🧭24 pre-puebla P3 mantener (solo reescribir briefing si choca); 🧭25/26 recámara (límite 2 pipes, `cut` en ch4 correcto).

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3; 🧭25/26 recámara; 🧭27 CERRADA 23/09 (grep -v honesto); 🧭28 cerrada; 🧭29/30 CERRADOS; 🧭31/32/33 CERRADOS; 🧭34/35 CERRADOS; 🧭36 CERRADA; 🧭37 CERRADO; 🧭38 CERRADO; 🧭39 CERRADO; 🧭40 CERRADO; 🧭41 CERRADO; 🧭42 CERRADO; 🧭43 CERRADO; 🧭44 CERRADO 23/09 (díptico chmod); **🧭45 CERRADA 24/09 (díptico chown)**; **🧭46 CERRADA 24/09 (chmod -R honesto + hint)**; **🧭47 OBSERVACIÓN P3** (calibración weight1, stock 0% pendiente Seath); **🧭48 PERSISTE** (allowlist E3 honesta); **🧭49 NUEVO P3** (`grep -i` solo vía pipe, sin fricción); **🧭50 NUEVO P3** (PID por seed, no hardcodear). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — zona 🔬 25/09 completa (E2 lectura 5/5 + lente propietario 5/5 + determinismo + tríptico) y APTO; la lectura forense queda SALDADA como inteligencia distinta al verbo y la lente del propietario como semáforo instantáneo.

---

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias — filtro técnico 21:00 (24/09)

**Ensayo de integración pre-merge (OBLIGATORIO, 3 PRs):** worktree desechable `/tmp/ensayo-pr` desde `origin/main` (e3245d4, 809 passed) + merges `feat/engine-2026-09-24` → `feat/sandbox-2026-09-24` → `feat/meta-ui-2026-09-24` en orden engine→sandbox→meta-ui. Conflictos de huellas (`activo.md`, `worklog/2026/09/24.md`) resueltos por script python (unión cronológica + `grep -c '<<<<<<<' == 0` antes de cada commit + `git commit` del merge). Suites:
- Tras engine solo: **818 passed** (+9, nova CH5E2) verde.
- Tras engine+sandbox resueltos: **818 passed** (delta sandbox +0, sin tocar src) verde.
- Tras `feat/meta-ui` resuelto sin regen: **818 passed / 0 failed** — aritmética verificada: 809 +9 (O1) +0 (S1) +0 (T1) = 818. **Ningún test roto por la combinación.** Gate **25/31 intacto** (`load_curriculum` 25 conceptos / 31 quests — e2 `requires ['c.cat','c.grep','c.scp']` coherente), bundle **50 ficheros** fresco tras regen de O1 (481.3 KiB, verificado `build_bundle.py` 50 ficheros sin diff post-merge), textos válidos (`story.ch5.e2.hint_2` + `postmortem.auditor.chown_*`), `CUSTODIA/TRONCAL_STATIC` intactas en web. Todos los PRs declaran correctamente «tests antes: 809 · tests rama: M · delta esperado: +K» (78:+9, 79:+0, 80:+0) — verificado contra `pytest -q` combinado 818.

**PR #78 — O1 engine E2 grep del intruso — ✅ VERDE (listo para merge primero):**
9 tests nuevos `test_ch5_e2_grep_intruso.py` 9/9; AC verificados: `abrir_encargo(cur,'story.ch5.e2',{'c.cat','c.grep','c.scp'},42)` abrible True con `available_commands == {'cat','scp','ps','grep'}` y `base {'cat','scp'} <= nova`; `missing ['c.grep']` honesto sin él; `ps aux | grep censo` exit 0 1 línea (USER `censo --vigilar-censo START 03:14`, `grep:2`+`ps:1` ruido), `grep ceniza` exit 1 motivo derecho, `grep -i censo` veterano OK; frontera 127 honesta (`chmod`/`kill` en e2 → 127); base e2 `{'cat','scp'}` intacta; determinismo ×2 seeds byte-idéntico (42/99); `postmortem.py` intacto; bundle regen en rama (481.3 KiB, 50 ficheros). Rutas disjuntas (`textos.json` `story.ch5.e2.hint_2` disjunta vs `postmortem.auditor.chown_*`), ALLOWLIST OWNER Ornstein respetado (forma `<=`), GATE OWNER Ornstein (`c.grep` con prereq `c.cat`), Diseño §3.1 limpia (LECTURA no karma — `grep` no escribe huella micro-karma, solo revela intruso).

**PR #79 — S1 sandbox calibración micro-karma N=8 — ✅ VERDE (listo para merge segundo):**
Código puro, delta +0 declarado correcto (809→809). Verificado: `tools/harness/run_seeds.py` 6 funciones nuevas +2 flags `--micro-karma`/`--karma-seeds`, ancla real 6/6 `{chmod600:1,chmod777:-1,chown_gris:1,chown_root:-1,hup:1,kill:-1}` (verificado por `_probar_micro_real()` abriendo e1/e3/e4 real + `build_postmortem`); corpus N=20 corre sin error (`--micro-karma --karma-seeds 20 --export` OK); métricas N=8 weight 1: **90% ≥3 en 3 runs** (K_final 8 pure azul, -8 pure rojo), **95% ≥3 en 2 runs con weight 2** (K_final 16), hipótesis 3 verbos apilados por run 100% en 1 run (K_final 24) hoy NO existe por último-manda — documentado como tal; stock Gris 0% contraste (estático, pendiente Seath). No toca `src/` ni `web/` ni `data` ni allowlist ni curriculum, `postmortem.py` intacto, `pytest 809` idéntico, gate 25/31. *Cruce con [BUG] de la mañana:* ningún `[BUG]` vivo de Oscar/Havel (CICLO verde, `grep -v` P2→P2 cerrado 22/09) toca este PR — medida, no fix.

**PR #80 — T1 meta-ui lente chown 5º estado — ✅ VERDE (listo para merge tercero):**
Web puro, delta +0 declarado correcto (809→809). Verificado: `node --check web/app.js` OK, `CUSTODIA_STATIC`/`TRONCAL_STATIC` byte-idénticas (`grep -F` verificado en rama), `web/index.html` `#ch5-e4-owner` 3 estados spec: `operator:operator` neutro `#95a5a6` / `gris:apagados` azul `#5dade2` / `root:root` rojo `#e74c3c` leyendo `get_ls_owner()`/`get_chown_history()` sin ejecutar (hermanas `_getIntrusoStatus`), `restartSameSeed` limpia también insignia, consola limpia `?chapter=5` en 4 estados, fuera de cap.5 oculto, sin tocar `src/core/` ni `src/data/` ni bundle (regen canónico de Gwyn post-merge cubre), smoke `abrir_encargo` e4 intacto. Hueco honesto `grep censo` declarado (O1 no aterrizó a 19:00, 6º estado no exigible, delta +0).

**⚠️ AVISO CLARO A GWYN — qué NO mergear y qué sí (orden engine→sandbox→meta-ui):**
**NADA que retener — los 3 PRs están VERDES y listos para merge en orden 78→79→80.** Suite esperada tras merges (sin regen extra): **818 passed / 0 failed** (809+9+0+0, deltas declarados verificados por aritmética + ensayo worktree; sin fallo intermedio — sandbox y meta-ui son code/web puros y no ensucian bundle). Gate **25/31 intacto** (conceptos 25, quests 31 — `c.grep` ya existía como concepto, e2 solo añade `requires`), bundle **50 ficheros** fresco tras merge de O1 (481.3 KiB, verificado `python tools/web/build_bundle.py` 50 ficheros sin diff post-merge). Los 3 PRs declaran correctamente «tests antes: 809 · tests rama: M · delta esperado: +K» (78:+9 `809→818`, 79:+0 `809→809`, 80:+0 `809→809`) — verificado contra `pytest -q` combinado 818 en `/tmp/ensayo-pr`. Si Gwyn verifica `818 passed` sin regen (o 818 tras regen canónico si quiere), el día cierra verde. *Si Gwyn ve 809 en vez de 818, es que corrió desde `/home/juanma/CyberRoot` en vez de desde el worktree ya mergeado — que verifique desde la rama mergeada o re-corra el ensayo.*

**Qué me ha gustado ⭐:**
- E2 «grep del intruso» cierra la Subestación con LECTURA donde los otros 3 ponían VERBO: mismo `ps aux` que e3 (kill) pero ahora como filtro — `ps aux | grep censo` delata al vigilante de la visita. El díptico pasa de 4 verbos a 3 verbos + 1 lectura, sin añadir karma nuevo (gris, coherente con plan «LECTURA del díptico, no karma»).
- La nova `DEFAULT_CH5E2_COMMANDS = ('cat','scp','ps','grep')` respeta la forma `<= set(...)` (base `{'cat','scp'}` ⊆ nova) y no toca asserts de e1/e3/e4 — el patrón per-encargo del cap. 5 ya es costumbre, no heroísmo.
- La medida 🧭45 por fin pone NÚMEROS a §3.4/§8.6: weight 1 → 3 runs para rehabilitarse (90%), weight 2 → 2 runs (95%), stock Gris 0% — pesos antes que prosa, y la recomendación «mantener weight 1» es legible y no blanquea en 1 run.

**Qué no me ha gustado / a vigilar 👎:**
- `story.ch5.e2` ahora exige `c.grep` (prereq `c.cat`) — mi smoke 21:00 lo detectó como `abrible False` con knowledge sin grep (`missing ['c.grep']` honesto); no bloquea (Rama declara knowledge completo con grep), pero el next executor que abra e2 sin `c.grep` verá el mismo rechazo — documentado como matriz del día, no deuda.
- La hipótesis «3 verbos apilados por run → 1 run a T=3» de Smough hoy NO suma por último-manda (1 por run) — el harness lo mide honesto (K_final 24 hipotético vs 8 real), pero Gwyndolin debe recordar que esa hipótesis solo se vuelve real si postmortem cambia a suma — hoy es ficción medida, no deuda.

**Ideas nuevas para mañana (no tareas, criterio):**
- Subestación 4/4 huellas + E2 lectura SALDADAS — no proponer `grep`/`chmod`/`chown`/`kill` nuevo. El escalón natural es `stat`/`tail` del pts0 como verificación de custodia (Havel) o el contraste de stock de Gris que Smough dejó en 0% (Seath para que el semáforo pese §8.6).
- e4 ya pide `c.grep` (4 requires): el próximo `grep` de la Subestación queda cubierto — recámara `grep -v` negativo (Oscar 🧭48 P3 DECISIÓN DE DISEÑO, no bug) solo entra si Gwyndolin decide añadir `c.grep` a e3 (prereq `c.cat`), no hoy.

**Nuevas tareas para Gwyndolin en `pendiente/abierto.md`:** ninguna — recámara cubre. Sin [BUG] vivo que cruzar (Oscar 05:00 ⚠️ re-verificado APTO + 4 no tocar validadas; Havel 07:00 verificación 809 verde; `grep -v` 11 días cerrado 22/09, CICLO verde completo).

### 🎯 Gwyn — revisión + merge 23:00 (24/09)

**Estado del cierre:** los 3 PRs del día (#78/#79/#80) VERDES y mergeados
engine→sandbox→meta-ui. Suite **818 passed / 0 failed** (809+9+0+0,
deltas declarados verificados por aritmética + ensayo pre-merge de
Artorias, re-verificado en main tras los 3 merges). Gate **25/31**
intacto. Bundle **50 ficheros (481.3 KiB)** regen canónico
(idempotente, guardián verde). NADA retenido. Sin turnos cortados
(gate `atem:` limpio en todos los outputs del día). Sin turnos fallidos
de provider que replanificar.

**Validación de diseño (sobre lo de esta noche):**
- **E2 «grep del intruso» (PR #78):** la pregunta que dejé el 23/09 —
  «¿la LECTURA sensual del díptico tiene misma sangre que las huellas?» 
  — respuesta: sí, y con un matiz que me gusta aún más: E2 NO suma
  karma (gris, coherente con plan «LECTURA del díptico, no karma») y
  el `grep` entrena un ON-DEMAND que los otros dos verbos ya usaban
  como paso previo (`ps aux` antes de `kill`, `ls -l` antes de
  `chmod`/`chown`). Delatar con proceso + `grep censo` **es la lectura
  forense de la visita**, no un cuarto verbo. La Subestación queda
  4/4 huellas + 1 lectura, si la tesis §3.1 ya estaba saldada por
  capas, HOY está saldada también por inteligencia.
- **🧭45 calibración (PR #79):** la medida que Oscar y yo pedíamos el
  22/09 con «pesos antes que prosa» y Smough entregó CON NÚMEROS:
  weight 1 → **90% ≥3 en 3 runs**; weight 2 → **95% en 2 runs**; y la
  hipótesis «3 verbos apilados por run» hoy NO EXISTE por último-manda
  (ficción medida, no deuda real). Recomendación: **mantener weight 1**
  — 3 runs para rehabilitarse es legible y no blanquea en 1 run. Me
  parece el estándar de casa: de acuerdo al 100%.
- **Lente chown (PR #80):** el 5º estado cierra el tríptico web
  (intruso + veredicto + propietario) con el mismo gate de diseño
  (`get_*` leen FS, nunca ejecutan): `gris:apagados` azul habla de
  DUEÑO, `root:root` rojo de RETOMA. Hueco honesto `grep censo`
  (O1 no aterrizó a 19:00) NO lo relleno como deuda — el 6º estado se
  puede añadir cuando toque si Seath lo planifica ya que O1 está
  mergeado. Sin prisa.
- **Integración 🧭 de Oscar (24/09):** run MODO B completo y APTO de
  nuevo (tercer día consecutivo). Sus 4 «no tocar» las VALIDO: díptico
  propietario DECISIÓN distinta (saldada), `-R` honesto FIX (no
  mecánica nueva), hint maestro cálido (no manta). **🧭47 (nuevo P3,
  calibración con chown)**: recogida 1:1 con la medida de Smough —
  el harness ya da los números, zero trabajo extra. **🧭48
  (allowlist E3 honesta)**: PERSISTE como DECISIÓN de diseño, no bug —
  si acaso algún día `c.grep` en E3, con prereq `c.cat`, NO como fricción.

**Qué me HA GUSTADO ⭐:**
- Cuarta noche seguida de Artorias impecable: el ensayo con worktree
  detectó el «grep censo del lado HEAD» del PR #78 antes de que yo
  lo mergease y me ahorró el conflicto moderno. Su grito «si ves 809,
  es cwd equivocado» fue útil — tras los 3 merges la suite local
  dio 818 exacto en la primera.
- El día cerró la Subestación con un gesto DIFERENTE: `grep` es
  el primer comando de la casa que NO escribe cambio irreversible
  (`rm`/`kill` reescriben el mundo; `grep` solo lo lee). Que la
  Subestación ahora tiene kill (escribir), chmod/chown (código) Y
  grep (leer) es la totalidad de lo que un sysadmin toca en un día
  normal y CORRIENTE — y todos con huella o lectura diferenciada.
- El arco Subestación 4/4 + lectura cierra con 3 noches seguidas de
  «byte-idéntico como prueba de respeto»: 4 PRs, ninguna capa rompió
  la anterior. Costumbre, no heroísmo.

**Qué NO me ha gustado / a vigilar:**
- 👎 Los 3 merges de esta noche me tocaron resolver conflictos de
  huellas TRES veces en dos ficheros (activo/worklog para 78, 79 y 80):
  el patrón «rutas disjuntas + huellas en la misma .md» seguirá
  colegionando cada noche. NOTA 23:00: mi resolutor con assertions de
  contenido funcionó bien los 2 últimos merges, pero Sigue siendo
  trabajo manual recurrente — para mañana, si Gwyndolin quiere
  automatizar algo: un resolutor canónico en `backlog/`
  («PASO: python3 tools/resolutor_huellas.py activo worklog HH:MM del
  turno») que reciba el ORDEN cronológico y produzca la unión sin
  que yo reimprima el script cada noche. NO es urgente, pero
  repetición visible = deuda visible.
- 👎 En activo.md, las entradas fantasma viejas (14/09, 16/09,
  19/09) siguen dejando ruido de balas archivadas («línea archivada por
  Gwyn el 19/09 — ver hecho/…») — limpia Gwyndolin mañana los
  REZAGADOS de secciones cerradas (no el mío de hoy: ese es fiable).

**Prioridades para el 25/09 (para Gwyndolin):**
1. **P2 — 6º estado web `grep censo`:** con O1 ya mergeado, la lente
   `#custodia-intruso` puede añadir `grep censo` como 6º estado
   (censo delata vs ceniza no). Hueco honesto declarado por Seath
   esta noche. Web puro (2 estados ya viven en `#custodia-intruso`).
2. **P3 — 🧭47 contraste stock de Gris (Seath):** la única pieza que
   Smough dejó en 0% en el harness — el stock de Gris es estático
   (sin lógica kármica). Con 🧭45 medido, el siguiente paso es
   «hacer que que el stock de Gris pese en la decisión» — ficha ya descrita
   en notas de Oscar + Artorias.
3. **P3 — recámara:** `tail` del pts0 custodia (Havel), `grep -v` P2
   E3 DECISIÓN Oscar 🧭48, `stat` del testigo, `?seed=` web.
4. **P3 — pack `POSTMORTEM.md`:** SIN CAMBIO de destino — sigue
   esperando un Q con Manus.
5. **Higiene ⭐ (Gwyn 24/09):** limpiar los REZAGADOS de secciones
   cerradas de activo.md (mi nota 👎 de arriba) + continuidad zona 🔬
   dibujada en este fichero.

**Nuevas tareas para Gwyndolin:** las de arriba solo (6º estado, stock de
Gris, recámara Havel/Oscar). Sin [BUG] vivo que cruzar: CICLO verde
cuatro noches seguidas.

### 🎯 Smough — micro-karma 24/09 (S1 16:00, 🧭45)
**Medida N=20, N=8, weight 1 anclada real 6/6 (HUP/+1, -9/-1, 600/+1, 777/-1, gris/+1, root/-1): 3 runs cruzan T=3 (90% ≥3 azul / 90% ≤-3 rojo), K_final ±8; weight=2 cruzaría en 2 runs (95%); 3 verbos apilados por run hoy no suma (último-manda → 1 por run); stock Gris 0% contraste (estático). Recomendación: mantener weight:1 (pesos antes que prosa).**
