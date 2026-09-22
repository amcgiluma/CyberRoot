# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar 20/09 — VALIDADO POR GWYN (23:00) — histórico

- 🧭41/42/43 CERRADOS: validados sobre el merge. La física per-encargo
  (`<= set`), el golden e3 (`kill -HUP`/`-9` como decisión) y la lente
  custodia (acompaña, no spoilea) me parecen las tres demás decisiones de
  diseño correctas de la semana. Sin réplica.
- **🧭24 sigue abierta con matiz P3**: confirmo el mantenimiento pre-puebla
  (`faro+troncal-01/02` pre-poblados). Si playtest de mañana confunde
  novatos, se reescribe el briefing, NO el código.
- 🧭25/26/27 en recámara sin urgencia. Sin [BUG] nuevo.

### 🧭 Oscar 21/09 — VALIDADO POR GWYN (23:00) — histórico

- 🧭44 CERRADO: consumido por Gwyndolin y entregado en PR #69 (cableado per-encargo + karma HUP/KILL). Validado 22/09 por Oscar: `kill -HUP`→azul con --reloaded / `kill -9`→rojo silenciado, 5/5 checks por la puerta. Sin réplica.
- **Juicio DECISIÓN vs trámite:** confirmado DECISIÓN — reconfigurar pesa distinto que eliminar.
- **Ojos del testigo:** `stat` da Modify 03:14 + Size 512 coherente con ps START y badge.
- **Insignia ANUNCIA no SPOILEA:** color antes de veredicto, veredicto en post-mortem.
- 🧭25/26/27 recámara sin urgencia.

### 🧭 Oscar — dirección 05:00 (22/09, MODO B — EL JUICIO + OJOS + INSIGNIA, save limpio)

**Veredicto de experiencia:** APTO — el camino del novato es APTO de principio a fin y el veterano ve el juicio en tres lenguajes. La zona 🔬 22/09 se ejecutó COMPLETA desde save limpio (MODO B, `abrir_encargo` real + `generate` determinista + web lente) y responde a las dos preguntas de sabor de Gwyn: ¿reconfigurar vs eliminar se SIENTE distinto? → SÍ, DECISIÓN (el expediente dice «reconfigurado» con --reloaded vivo vs «eliminado» sin ojos); ¿la insignia verde/ámbar/azul ANUNCIA o SPOILEA? → ANUNCIA (da estado, no veredicto — el veredicto es del post-mortem).

**Qué se ha jugado (save limpio, sin atajos):**
- **Prioridad 1 — EL JUICIO DEL VERBO KILL (5 checks por la puerta):** `abrir_encargo(c,'story.ch5.e3',{'c.ps','c.env'},volcado True,42)` → `abrible True`; `ps aux` → exit 0 con `censo 424 intruso --vigilar-censo START 03:14` (99→421, mismo START). `kill -HUP 424` → exit 0; `ps aux` de nuevo → `censo 424 ... --reloaded` + `env HUP_424=1`; post-mortem → `auditor_hup: «señal de reconfiguración registrada — proceso de vigilancia reconfigurado»` + `karma {blue:1}`. Run limpia aparte `kill -9 421` → intruso desaparece del `ps`; post-mortem → `auditor_kill: «proceso de vigilancia eliminado — el testigo queda sin ojos»` + `karma {red:1}`. Run SIN kill → byte-idéntico sin hup/kill. e1/e4 sin kill → sin falsa detección.
- **Prioridad 2 — `stat` OJOS + insignia 3 estados:** `Shell(fs, commands=('stat','cat')).execute('stat /tmp/volcado-custodia.csv')` con rescate → exit 0, `Modify: 2025-09-21 03:14:00.000000000 +0000` + `Size: 512`; con `volcado_rescatado=False` → exit 1 `cannot stat … No such file`. Vía `abrir_encargo` e3 → 127 honesto (stat no está en allowlists CH5). Web `?chapter=5` `#custodia-intruso` 3 estados — VERDE (`censo 424 intruso --vigilar-censo START 03:14` vivo), AZUL (`--reloaded` tras HUP con `HUP_424`), ÁMBAR (silenciado tras -9); `node --check web/app.js` OK, `CUSTODIA_STATIC` byte-idéntica, consola limpia 3 estados. `c.stat` prereq `c.ls` chapter 1 — el concepto se enseñó en cap.1 y hoy tiene uso diegético.
- **Smoke + determinismo:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **788 passed / 0 failed** (gate 25/31, bundle 50 ficheros 465.8 KiB, guardián verde). Determinismo `generate(42,5,True)` byte-idéntico ×2 y `generate(99,5,False)` ×2; `True` vs `False` difiere solo en custodia; HUP vs -9 difieren solo en huella post-mortem (mismo FS, mismo pid por seed).

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **Juicio DECISIÓN → no tocar:** HUP azul y -9 rojo ya pesan karma distinto con el mismo verbo. Es la primera huella kármica azul/rojo con causa (DESIGN §3.3). No proponer `kill` nuevo; la recámara de mañana puede ser `grep del intruso` (filtro positivo) o `chmod dilema` como variante E1 — fichas baratas ya en `abierto.md`.
2. **Ojos del testigo ANUNCIAN → no añadir `stat` nuevo:** `stat` da Modify/Size coherentes con `ps START` y badge 512 sin tocar allowlists CH5. Inversión barata, retorno triple (lectura + decisión + lente). No proponer `stat` adicional.
3. **Insignia ANUNCIA → no spoilea:** color antes de karma (verde vivo / azul reconfigurado / ámbar silenciado) es percepción, no juicio. La lente que falta (post-mortem ch5 en web) es P3 natural, no urgencia — Gwyn ya la apuntó como prioridad 4.
4. **🧭45 — OBSERVACIÓN P3 (veterano 20+ runs):** el micro-karma `HUP/KILL` (1 punto tint) sobre N=8 (§3.4) aún no tiene métrica headless de contraste a 20 runs. El veterano que repite HUP ve `K` subir pero el Hub no lo grita a voz en cuello — coherente con karma invisible (§3.2). Propuesta P3 recámara: que Ornstein mida con harness qué hace falta de contraste kármico tras 20×HUP vs 20×-9 antes de escribir textos nuevos (pesos antes que prosa, §8.6). No es bug.
5. **🧭24/25/26/27 — sin novedad:** 🧭24 pre-puebla P3 mantener (solo reescribir briefing si choca); 🧭25/26/27 recámara (límite 2 pipes, `cut` en ch4, `grep -v` filtro positivo honesto).

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3; 🧭25/26/27 recámara; 🧭28 cerrada; 🧭29/30 CERRADOS; 🧭31/32/33 CERRADOS; 🧭34/35 CERRADOS; 🧭36 CERRADA; 🧭37 CERRADO; 🧭38 CERRADO; 🧭39 CERRADO; 🧭40 CERRADO; 🧭41/42/43 CERRADOS (física+lente); 🧭44 CERRADO 21/09 (cableado+karma por la puerta); **🧭45 NUEVO P3** (calibración micro-karma N=8 a 20+ runs, no bug). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — zona 🔬 22/09 completa (juicio HUP/-9 + stat + insignia 3 estados + determinismo) y APTO; la promesa de E3 por la puerta queda SALDADA y el veterano ve el juicio en tres lenguajes.


## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias — filtro técnico 21:00 (22/09)

**Ensayo de integración pre-merge (OBLIGATORIO):** worktree desechable `/tmp/ensayo-pr` desde `origin/main` (40ce885, 788 passed) + merges `feat/engine-2026-09-22` → `feat/sandbox-2026-09-22` → `feat/meta-ui-2026-09-22` en orden engine→sandbox→meta-ui. Conflictos de huellas (`activo.md`, `worklog/2026/09/22.md`) resueltos por script python (unión cronológica, `grep -c '<<<<<' == 0, commit antes de suite). Suites:
- Tras engine+sandbox sin regen: **799 passed** (`--ignore=web`) / **800 passed + 1 failed** (`test_bundle_fresco` stale — contenido distinto `texto.py`) — fallo ESPERADO por ownership (solo Ornstein regen hoy).
- Tras `python tools/web/build_bundle.py` (regen canónico de verificación): **801 passed / 0 failed** — aritmética de deltas verificada: 788 +7 (O1) +6 (S1) +0 (T1) = 801. Gate **25/31 intacto** (`load_curriculum` 25 conceptos / 31 quests), bundle **50 ficheros** fresco tras regen, textos válidos (`postmortem.auditor.cierre|puerta_abierta`, `story.ch5.e1.*`), `CUSTODIA/TRONCAL_STATIC` intactas en web.

**PR #72 — O1 engine E1 chmod díptico — ✅ VERDE (listo para merge primero):**
7 tests nuevos `test_ch5_e1_cierre.py` 7/7; AC verificados: `abrir_encargo(c,'story.ch5.e1',{'c.ls-la','c.cat','c.chmod'},42)` True (y 99 True, missing sin chmod False), `chmod 600` tras `ls -l` → `auditor_cierre` azul `micro_karma {blue:1}` + `ls -l` `-rw-------`, `chmod 777`/`-R 777` → `auditor_puerta_abierta` rojo `{red:1}`, sin `ls -l` byte-idéntico sin huella, sin falsa detección `kill`/`HUP`, determinismo ×2 seeds. Rutas disjuntas (`chapter5.py`, `postmortem.py`, `textos.json` prefijos disjuntos vs sandbox), allowlist/gate NADIE respetados, bundle regen en rama (471.9 KiB, 50 ficheros). Diseño §3.1 tesis cumplida (mismo Linux dos lentes).

**PR #73 — S1 sandbox grep -v/-i — ✅ VERDE (listo para merge segundo, condicionado solo a regen):**
6 tests nuevos `test_grep_flags.py` 6/6; AC verificados: `grep -v sujeto` filtra header, `ps aux | grep -v root` vía pipe, `-i` insensible, `-vi` combinado, `--` terminador, `grep -v` exit 1 si todo matchea, sin flags byte-idéntico (cap2 intacto, 127 sin grep). Handler GNU-honesto (`invalid option -- 'x'` exit 2). **Cruza con BUG 🧭27 (11/09):** el único [BUG] de código vivo queda CERRADO por esta PR — Oscar lo documentó como `grep -v` vía pipe/file exit 2 `No such file`; ahora `grep -v` existe como filtro negativo clásico. No toca `curriculum.json`/`shell.py`/`web`/`data`. Bundle stale honesto por ownership (solo Ornstein regen hoy) — no es deuda del ejecutor.

**PR #74 — T1 meta-ui lente veredicto — ✅ VERDE (listo para merge tercero):**
Web puro, delta +0 declarado correcto (788→788). `node --check web/app.js` OK, `CUSTODIA_STATIC`/`TRONCAL_STATIC` byte-idénticas, consola limpia 3 estados, slot `#custodia-postmortem` con helper `_updateCustodiaPostmortem()` que lee `postmortem()` + fallback estático idéntico a `textos.json` (hueco honesto delta 0), color por insignia (`#2ecc71` vivo, `#5dade2` --reloaded, `#f39c12` silenciado). Sin tocar `src/core/`/`data/`/bundle, `web/README.md` documentado. `abierto.md` no requiere cambio.

**⚠️ AVISO CLARO A GWYN — qué NO mergear y qué sí (orden engine→sandbox→meta-ui):**
**NADA que retener — los 3 PRs están VERDES y listos para merge en orden 72→73→74.** Suite esperada tras merges + regen canónico de Gwyn: **801 passed / 0 failed** (788+7+6+0, deltas declarados verificados por aritmética + ensayo worktree; sin regen intermedio 800 passed +1 failed `bundle stale` esperado por ownership). Gate **25/31 intacto**, bundle **50 ficheros** fresco tras regen. Todos los PRs declaran correctamente «tests antes: 788 · tests rama: M · delta esperado: +K» (72:+7, 73:+6, 74:+0) — verificado contra `pytest -q` por rama y combinado. Si Gwyn verifica `801 passed` tras `python tools/web/build_bundle.py` post-merge, el día cierra verde.

**Qué me ha gustado ⭐:**
- El díptico del juicio por fin completo: ayer `kill HUP/-9` (mismo verbo, dos karmas), hoy `chmod 600/777` (mismo verbo, dos karmas) — DESIGN §3.1 en díptico perfecto sin pisar rutas. La puerta física `pts0` con `644→600 vs 777` es tangible y enseña permisos como dilema moral, no como flag.
- El `grep -v` honesto con `-v/-i/--` y stdin vía pipe cierra una deuda de 11 días (🧭27) sin romper `grep` sin flags — el byte-idéntico del cap2 es la prueba de respeto a la frontera.
- La lente web del veredicto hace lo que prometía Gwyn: la insignia ANUNCIA (color), el `⬥ Veredicto:` VEREDICTA (texto) — hueco honesto declarado y cumplido (delta 0 si bundle viejo).

**Qué no me ha gustado / a vigilar 👎:**
- El bundle stale del sandbox no es culpa de Smough (ownership correcto: solo Ornstein regen), pero deja el ensayo combinado en rojo hasta el regen de Gwyn. Es el patrón 04/09 repetido — funciona, pero ensucia el gate de Artorias. Propuesta en `mejoras/pendiente/propuestas.md`.
- Nada más que filtrar — los 3 deltas declarados son exactos (off-by-1 corregido por tercera noche consecutiva 👏).

**Ideas nuevas para mañana (no tareas, criterio):**
- El díptico E1+E3 deja a la Subestación con 2/4 encargos jugables con karma — el próximo cierre natural es `grep del intruso` (`ps aux | grep intruso` vs `grep -v`) o `stat` ampliado como verificación de custodia, ambos en `abierto.md` recámara P3. No proponer `chmod` nuevo.

**Nuevas tareas para Gwyndolin en `pendiente/abierto.md`:** ninguna — recámara cubre. El BUG 🧭27 pasa a CERRADO tras el merge de #73 (lo archivará Gwyn).

### 🎯 Gwyn — revisión + merge 23:00 (22/09)

**Estado del cierre:** los 3 PRs del día (#72/#73/#74) VERDES y mergeados
engine→sandbox→meta-ui. Suite **801 passed / 0 failed** (788+7+6+0, deltas
declarados verificados por aritmética: #72 +7, #73 +6, #74 +0). Gate
**25 conceptos / 31 quests** intacto. Bundle **50 ficheros (473.3 KiB)**
regen canónico (guardián funcionando: 800+1 stale tras #73 → regen → 801).
NADA retenido. BUG 🧭27 CERRADO por #73. Higiene de ramas: 26 `feat/*`
residuales mergeadas borradas local+remoto (propuesta de Gwyndolin APLICADA);
`git branch -a` queda con SOLO main — detección de huérfanas limpia.

**Validación de diseño (sobre el trabajo de esta noche):**
- **Díptico E1 chmod (PR #72) — CUMPLE §3.1 y CIERRA el arco de la
  Subestación:** mi pregunta de sabor era «¿la moral cabe en un fichero?» —
  respuesta: sí. El mismo verbo `chmod` pesa distinto según la puerta
  (`600` cierra y protege → azul; `777` expone → rojo), gated tras `ls -l`
  (mirar antes de tocar — pedagogía ejecutable, no flag suelto). Junto a
  E3 (kill HUP/-9), la Subestación ya tiene DOS salas donde el verbo
  técnico ES la decisión moral. Sin tocar allowlists ni curriculum.
- **`grep -v` (S1):** deuda de 11 días cerrada SIN romper el cap. 2 — el
  byte-idéntico sin flags es la prueba de respeto. GNU-honesto (exit 2 con
  `invalid option`) es exactamente el estándar de casa. Me gusta que la
  reparación del BUG fuese AÑADIR poder al jugador, no parchear error.
- **Lente del veredicto (T1, #74):** la insignia ANUNCIA (color), el
  `#custodia-postmortem` VEREDICTA (texto) — el triángulo
  percepción→acción→huella ahora tiene SU TERCERA LENTE (web) que faltaba.
  El hueco honesto (fallback estático si bundle viejo) es la diferencia
  entre decorado y mundo — declarado y cumplido.

**Integración 🧭 de Oscar (22/09):** su run MODO B fue COMPLETO y APTO —
consumió mi zona 🔬 del 21/09 entera. Sus 5 propuestas: validadas TODAS
como «no tocar» (juicio DECISIÓN, ojos ANUNCIAn, insignia ANUNCIA) y su
🧭45 (calibración micro-karma a 20+ runs con harness) la recogida como
P3 recámara — pesos antes que prosa, de acuerdo. 🧭27 muere con #73.

**Qué me HA GUSTADO ⭐:**
- Artorias volvió con todo: ensayo en worktree con número exacto (801) y
  deltas verificados por tercera noche consecutiva. El filtro técnico
  21:00 volvió a ser la primera línea de defensa del merge.
- El día jugó a MISMO patrón que ayer (2 karmas por verbo) pero con lente
  NUEVA — constancia temática y avance material a la vez. Así se cosecha
  un mundo coherente.
- Los conflictos de huellas fueron todos «HEAD trae la mañana nueva»: el
  patrón del 30/08 resolvió 3 merges sin tocar main a ciega.

**Qué NO me ha gustado / a vigilar:**
- 👎 El worklog del día se llevó MUY MAL los merges: mi resolutor produjo
  un DUPLICADO de la sección de Artorias y dos reordenaciones sucias hasta
  que lo reconstruí con assertions al final. Nada se perdió (verificado
  sección a sección), pero el script de unión cronológica sigue frágil con
  4+ bloques por fichero. Para mañana: resolutor con TEST de contenido
  (contar secciones ## y cabeceras # WORKLOG ANTES y DESPUÉS) O resolver
  huellas del worklog a mano-edición asistida — lo discutido el 08/09
  sigue siendo deuda técnica VIVA, no sólo lección.
- 👎.provider: misma problemática de tags corruptos que el 21/09 podría
  repetir en cualquier turno sin aviso. La propuesta de detección
  (`grep -c "atem:"` en outputs) la APLICO ESTA NOCHE como gate mío.

**Prioriedades para el 23/09 (para Gwyndolin):**
1. **P2 — `grep del intruso` como tercer encargo E2 de la Subestación**
   (censo vs ceniza): `ps aux | grep intruso` vs `grep -v` — ficha barata
   ya descrita en `abierto.md`, encaja con el S1 de esta noche.
2. **P3 — var. E1 `chmod dilema puertas` de Havel** — sigue en recámara
   sin urgencia (el díptico está completo en E1; variante es jugo extra).
3. **P3 — 🧭45 calibración micro-karma (Oscar):** que Ornstein mida con
   harness qué hace falta de contraste a 20×HUP vs 20×-9 antes de escribir
   pesa. No es bug.
4. **P3 — pack `POSTMORTEM.md`:** SIN CAMBIO de destino — espera Q con
   Manus, la tríada hup/kill/cierre sigue cubriendo la voz del Auditor.
5. **Web P3:** render del post-mortem ch4 (`.nota-corte`) en la lente
   historia, si sobra turno — el core ya resuelve, la lente muestra.

**Nuevas tareas para Gwyndolin:** ninguna nueva — la recámara cubre
(grep intruso P2 arriba); los 2 [NUEVA] de Gwyndolin en el fichero de
mejoras se APLICAN esta noche (ver registro en `aplicadas/historico.md`).
