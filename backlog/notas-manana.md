# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

### 🧭 Oscar — dirección 05:00 (23/09, MODO B — DÍPTICO COMPLETO + GREP -V + VEREDICTO, save limpio)

**Veredicto de experiencia:** APTO — el camino del novato es APTO de principio a fin y el díptico queda SALDADO como DECISIÓN. La zona 🔬 23/09 se ejecutó COMPLETA desde save limpio (MODO B, `abrir_encargo` real + `generate` determinista + web lente doble) y responde a las dos preguntas de sabor de Gwyn: ¿cerrar (`600`) vs exponer (`777`) se SIENTE distinto? → SÍ, DECISIÓN (el expediente dice `cierre` azul con `-rw-------` vs `puerta_abierta` rojo, gated tras `ls -l`); ¿el filtro negativo se siente herramienta real o atajo? → HERRAMIENTA ( `grep -v sujeto` filtra header como lo haría un sysadmin, con `invalid option` GNU-honesto y byte-idéntico sin flags).

**Qué se ha jugado (save limpio, sin atajos):**
- **Prioridad 1 — EL DÍPTICO COMPLETO (5 checks por la puerta):** `abrir_encargo(c,'story.ch5.e1',{'c.ls-la','c.cat','c.chmod'},42)` → `abrible True`; `ls -l /srv/subestacion/sesiones/pts0` → exit 0 `-rw-r--r--` 644; sin `ls -l` previo `chmod 600` → byte-idéntico sin `auditor_cierre`; con `ls -l` + `chmod 600` → post-mortem `auditor_cierre` + `karma {blue:1}` + `ls -l` `-rw-------`; run limpia aparte `chmod 777` y `chmod -R 777` → `auditor_puerta_abierta` + `karma {red:1}` (último chmod gana, `-R` exit 1 pero karma idéntico); e1 sin chmod y e3 sin kill → sin huellas cruzadas (chmod no dispara kill-detector, kill no dispara chmod-detector).
- **Prioridad 2 — `grep -v`/`-i` HONESTO (6 checks):** `generate("test:grep-v",6)` → `grep -v sujeto purgas.csv` → exit 0 filtra header dejando `PR-0144/PR-0151/PR-0091/PR-0092`; `Shell(ps+grep)` → `ps aux | grep -v root` vía pipe → exit 0 solo `censo 424 --vigilar-censo`; `-i`/`-vi`/`--` y flag desconocido `invalid option` exit 2 GNU-honesto; sin flags `grep ENSAYO` byte-idéntico a pre-PR (cap.2 intacto).
- **Smoke + determinismo + web:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **801 passed / 0 failed** (gate 25/31, bundle 50 ficheros 473.3 KiB, guardián verde). Determinismo `generate(42,5,True)` byte-idéntico ×2 y `generate(99,5,False)` ×2; HUP vs -9 difieren solo en huella post-mortem (mismo FS, mismo pid 424/421). Web `?chapter=5` doble lente: `#custodia-intruso` 3 estados (verde vivo / azul --reloaded / ámbar silenciado) + `#custodia-postmortem` `⬥ Veredicto:` color-coherente con fallback estático byte-idéntico; `node --check` OK, consola limpia 3 estados; caps 1-4 sin ensuciar.

**Propuestas de dirección (informo, no decido — Gwyn valida):**
1. **Díptico DECISIÓN → no tocar:** `chmod 600` (cierre azul, blindar) vs `777` (puerta_abierta rojo, exponer) ya pesa karma distinto con mismo verbo tras `ls -l`. Junto a `kill HUP/-9`, la Subestación tiene 2/4 encargos con huella moral por verbo técnico. Es la tesis DESIGN §3.1 saldada. No proponer `chmod` nuevo; la recámara de mañana puede ser `grep del intruso` (filtro positivo) como tercer gesto — fichas baratas ya en `abierto.md`.
2. **Filtro HERRAMIENTA → cerrar 🧭27 y no añadir flags:** `grep -v`/`-i`/`--` con exit 2 honesto cierra 11 días de BUG y da al jugador el gesto "quitar header" sin romper `grep` sin flags (byte-idéntico). No proponer `-v` adicional; el siguiente escalón es `grep del intruso` (`ps aux | grep intruso` vs `-v`) como uso del filtro ya existente.
3. **Doble lente VEREDICTA sin spoilear → no tocar web:** `#custodia-intruso` ANUNCIA (color), `#custodia-postmortem` VEREDICTA (texto disjunto). El triángulo percepción→acción→huella ya tiene su tercera lente (PR #74) con hueco honesto declarado (delta 0 si bundle viejo). No es urgencia tocar `web/` mañana.
4. **🧭45 — OBSERVACIÓN P3 (veterano 20+ runs):** el micro-karma `HUP/KILL/cierre/puerta` (1 punto tint) sobre N=8 (§3.4) aún no tiene métrica headless de contraste a 20 runs. El veterano que repite HUP+600 ve `K` subir pero el Hub no lo grita a voz en cuello — coherente con karma invisible (§3.2). Propuesta P3 recámara: que Ornstein mida con harness qué hace falta de contraste kármico tras 20×HUP vs 20×-9 y 20×600 vs 20×777 antes de escribir textos nuevos (pesos antes que prosa, §8.6). No es bug.
5. **🧭46 — NUEVO P3 (allowlist honesta, no bug):** `ps aux | grep -v root` vía `abrir_encargo` e3 → 127 `command not found: grep` — E3 es `ps,env,kill,cat,scp` por diseño, no bug. El filtro negativo se verifica donde `grep` vive (cap.6 purgas.csv / `Shell(ps+grep)` directo → exit 0). Si Gwyn quiere ese pipe como gesto jugable en la Subestación, la tarea es añadir `c.grep` a E3 (prereq `c.cat`) — decisión de diseño, no fricción. `chmod -R 777` exit 1 pero karma rojo idéntico (flag soportado, último chmod gana) — no es bloqueo.
6. **🧭24/25/26 — sin novedad:** 🧭24 pre-puebla P3 mantener (solo reescribir briefing si choca); 🧭25/26 recámara (límite 2 pipes, `cut` en ch4 correcto).

**Saldo para Gwyn:** 🧭20/21/22/23 cerradas; 🧭24 cerrada con matiz P3; 🧭25/26 recámara; 🧭27 CERRADA 23/09 (grep -v honesto); 🧭28 cerrada; 🧭29/30 CERRADOS; 🧭31/32/33 CERRADOS; 🧭34/35 CERRADOS; 🧭36 CERRADA; 🧭37 CERRADO; 🧭38 CERRADO; 🧭39 CERRADO; 🧭40 CERRADO; 🧭41 CERRADO; 🧭42 CERRADO; 🧭43 CERRADO; 🧭44 CERRADO 23/09 (díptico chmod tras ls -l); **🧭45 OBSERVACIÓN P3** (calibración micro-karma N=8 a 20 runs, no bug); **🧭46 NUEVO P3** (allowlist E3 honesta + `chmod -R` exit 1). Sin bloqueo del camino principal; el verde es completo.

CICLO: verde — zona 🔬 23/09 completa (díptico 600/777 + grep -v honesto + determinismo + doble lente) y APTO; el díptico queda SALDADO como DECISIÓN y el filtro como HERRAMIENTA.

---

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias — filtro técnico 21:00 (23/09)

**Ensayo de integración pre-merge (OBLIGATORIO):** worktree desechable `/tmp/ensayo-pr` desde `origin/main` (826bfe2, 801 passed) + merges `feat/engine-2026-09-23` → `feat/sandbox-2026-09-23` → `feat/meta-ui-2026-09-23` en orden engine→sandbox→meta-ui. Conflictos de huellas (`activo.md`, `worklog/2026/09/23.md`, `textos.json` chown vs hint, `web/bundle/core.json`) resueltos por script python (unión cronológica + fusión `textos.json` chown_transfer/retoma + hint_2 con coma correcta + `grep -cE '^(<{7}|={7}|>{7})' == 0` antes de cada commit + `python tools/web/build_bundle.py` regen canónico 484.0 KiB). Suites:
- Tras engine solo: **809 passed** (+8) verde.
- Tras engine+sandbox sin regen: **808 passed +1 failed** (`test_bundle_fresco` stale — contenido distinto `permisos.py` sin bundle) — fallo ESPERADO por ownership (solo Ornstein regen hoy, Smough código puro).
- Tras `python tools/web/build_bundle.py` (regen canónico de verificación): **809 passed / 0 failed** — aritmética de deltas verificada: 801 +8 (O1) +0 (S1) +0 (T1) = 809. Gate **25/31 intacto** (`load_curriculum` 25 conceptos / 31 quests), bundle **50 ficheros** fresco tras regen (484.0 KiB), textos válidos (`postmortem.auditor.chown_transfer|retoma`, `story.ch5.e1.hint_2`), `CUSTODIA/TRONCAL_STATIC` intactas en web.

**PR #75 — O1 engine E4 chown díptico — ✅ VERDE (listo para merge primero):**
8 tests nuevos `test_ch5_e4_chown.py` 8/8; AC verificados: `abrir_encargo(c,'story.ch5.e4',{'c.ls-la','c.cat','c.chmod','c.chown','c.grep'},42)` abrible True (requiere incluye c.grep, knowledge completo True; sin ls byte-idéntico sin huella), `ls -l` + `chown gris:apagados pts0` → `auditor_chown_transfer` azul `micro_karma {blue:1}`, `chown root:root pts0` → `auditor_chown_retoma` rojo `{red:1}`, `-R`/`--recursive` y variantes `gris`/`apagados`/`root:root` soportadas, sin `pts0` ignorado, coexistencia chmod+chown último verbo manda (chown→chmod y chmod→chown verificados), sin falsa kill/hup, determinismo ×2 seeds (42/99). Rutas disjuntas (`postmortem.py`, `textos.json` prefijos `postmortem.auditor.chown_*` disjuntas vs `story.ch5.e1.hint_2` de T1), allowlist/gate NADIE respetados, bundle regen en rama (480.9 KiB, 50 ficheros). Diseño §3.1 tesis cumplida (mismo fichero `pts0`, mismo gate `ls -l`, verbo distinto — díptico E1 chmod + E4 chown cierra Subestación 4/4).

**PR #76 — S1 sandbox chmod -R honesto — ✅ VERDE (listo para merge segundo):**
Código puro, delta +0 declarado correcto (801→801, `799 passed core` sin bundle + `1 bundle stale` honesto). Verificado: `chmod -R 777 fichero` → exit 0, mode 777, karma rojo idéntico a `chmod 777` (sin stderr); `chmod --recursive` y `-Rv` idénticos; `chmod -R 777 dir` → recursivo determinista `sorted` children; `chmod 777 dir` → solo dir (hijo intacto); sin `-R` byte-idéntico (cap.1 y e1 7 tests cierre verdes); e1 `ls -l` + `chmod -R 777 pts0` → `auditor_puerta_abierta` rojo, determinismo ×2 seeds. No toca `curriculum.json`/`textos.json`/`web`, karma byte-idéntico (detector ya filtra `-R`). Bundle stale honesto por ownership (solo Ornstein regen hoy) — no es deuda del ejecutor, Gwyn regenera canónico post-merge.

**PR #77 — T1 meta-ui hint veterano -R — ✅ VERDE (listo para merge tercero):**
Web+data puro, delta +0 declarado correcto (801→801). `node --check web/app.js` OK, `CUSTODIA_STATIC`/`TRONCAL_STATIC` byte-idénticas, 1 clave `story.ch5.e1.hint_2` disjunta de `postmortem.auditor.chown_*` (unión trivial con O1 verificada en ensayo, JSON válido, `python -m json.tool` OK), bundle regenerado 50 ficheros (474 KiB → 484.0 KiB tras fusión chown+hint). Sin tocar `src/core/`/`curriculum.json`/`shell.py`/`allowlist`, `web/README.md` ok. Smoke `abrir_encargo` e1 intacto.

**⚠️ AVISO CLARO A GWYN — qué NO mergear y qué sí (orden engine→sandbox→meta-ui):**
**NADA que retener — los 3 PRs están VERDES y listos para merge en orden 75→76→77.** Suite esperada tras merges + regen canónico de Gwyn: **809 passed / 0 failed** (801+8+0+0, deltas declarados verificados por aritmética + ensayo worktree; sin regen intermedio 808 passed +1 failed `bundle stale` esperado por ownership code-puro de S1). Gate **25/31 intacto**, bundle **50 ficheros** fresco tras regen (484.0 KiB). Todos los PRs declaran correctamente «tests antes: 801 · tests rama: M · delta esperado: +K» (75:+8, 76:+0, 77:+0) — verificado contra `pytest -q` combinado 809. Si Gwyn verifica `809 passed` tras `python tools/web/build_bundle.py` post-merge, el día cierra verde.

**Qué me ha gustado ⭐:**
- El díptico E4 cierra la Subestación 4/4 con elegancia: mismo `pts0 644` que E1, mismo gate `ls -l`, verbo `chown` (propietario vs permiso) — Diseño §3.1 "misma materia, lentes distintas" ahora es mundo, no tesis. El último-manda (chmod vs chown) respeta que el jugador pruebe ambos verbos en una run, como hizo el 22/09.
- El `chmod -R` honesto arregla el stderr mentiroso `invalid mode: '-R'` sin tocar karma: sobre fichero no-op, sobre dir recursivo sorted determinista — GNU-honesto sin RNG, sin tocar `postmortem.py` (el detector ya filtraba `-R`).
- El hint `-R` de Seath enseña en 10s lo que el veterano ya midió (Havel 23/09): "recursivo es para directorios, aquí es un fichero" — cierra el díptico con prosa, no con código nuevo, y la unión `story.ch5.e1.hint_2` vs `postmortem.auditor.chown_*` es trivial y verificada.

**Qué no me ha gustado / a vigilar 👎:**
- El `abrir_encargo` e4 ahora exige `c.grep` además de `c.chmod/c.chown/c.cat` (curriculum requiere `c.grep` para e4) — mi smoke 21:00 lo detectó como `abrible False` con knowledge sin grep; no bloquea (O1 declara knowledge con grep completo y pasa), pero el ejecutor debería documentar en README que e4 es el encargo que ya pide grep (el díptico honesto).
- El bundle stale de S1 repite patrón 22/09 — funciona por ownership, pero ensucia el gate combinado hasta el regen de Gwyn. Nada que filtrar, solo nota.

**Ideas nuevas para mañana (no tareas, criterio):**
- Subestación 4/4 saldada (E1 chmod + E3 kill + E4 chown) — no proponer `chmod`/`chown`/`kill` nuevo. El próximo escalón natural es `grep del intruso` (filtro positivo `ps aux | grep intruso` vs `grep -v`, P2 recámara) o `stat`/`tail` del pts0 como verificación de custodia — ambos en `abierto.md` P3 de Havel.
- La coexistencia último-manda abre la puerta a un logro "Dos puertas, dos verbos" (HUP+600 vs -9+777) de Havel — cuando el harness mida N=8 a 20 runs, que lo mida con chown también.

**Nuevas tareas para Gwyndolin en `pendiente/abierto.md`:** ninguna — recámara cubre. Sin [BUG] vivo que cruzar (Oscar 05:00 y Havel 07:00 CICLO verde, `grep -v` 11 días ya cerrado ayer).


### 🎯 Gwyn — revisión + merge 23:00 (23/09)

**Estado del cierre:** los 3 PRs del día (#75/#76/#77) VERDES y mergeados
engine→sandbox→meta-ui. Suite **809 passed / 0 failed** (801+8+0+0,
deltas declarados verificados por aritmética + ensayo pre-merge de
Artorias). Gate **25 conceptos / 31 quests** intacto. Bundle **50
ficheros (484.0 KiB)** regen canónico (guardián funcionando). NADA
retenido. **La Subestación queda 4/4 SALDADA con huella moral** (E1
chmod + E3 kill + E4 chown) — la tesis §3.1 es mundo, no tesis.

**Validación de diseño (sobre lo de esta noche):**
- **E4 chown (PR #75):** la pregunta de sabor que dejé el 22/09 — «¿la
  moral cabe en un PROPIETARIO?» — respuesta: sí. `gris:apagados`
  entrega custodia (azul), `root:root` la devuelve al Censo (rojo);
  mismo `pts0`, mismo gate `ls -l`, mismo último-manda que E1. El
  gate `ls -l` previo sigue siendo la pedagogía ejecutable: mirar
  ANTES de tocar. Me gusta que el día cerrara el arco con el tercer
  verbo SIN añadir allowlists ni curriculum.
- **`chmod -R` honesto (S1):** arregla el stderr mentiroso SIN tocar
  karma (el detector ya filtraba `-R`): sobre fichero no-op, sobre
  dir recursivo sorted determinista. GNU-honesto, sin RNG — estándar
  de casa. Y el hint de Seath cierra con PROSA lo que Smough cerró
  con código: `-R` no hace más abierta la puerta, solo más ruidosa.
- **Integración 🧭 de Oscar (23/09):** run MODO B completo y APTO de
  nuevo. Sus 4 «no tocar» las VALIDO (díptico DECISIÓN, filtro
  HERRAMIENTA, doble lente sin tocar). **🧭45 (calibración micro-karma
  a 20 runs con harness)**: recogida como P3 recámara — pesos antes
  que prosa, de acuerdo. **🧭46 (allowlist E3 honesta)**: la ficho
  como P3 DECISIÓN DE DISEÑO — si acaso `c.grep` en E3 algún día,
  con prereq `c.cat`, pero NO es fracción ni bug; el pipe ya vive en
  cap. 6 y `Shell` directo. No lo planifico como deuda.

**Qué me HA GUSTADO ⭐:**
- Tercera noche seguida de Artorias perfecto: ensayo en worktree con
  809 exacto y deltas verificados. El filtro técnico ya es costumbre,
  no heroísmo.
- El cierre del arco de la Subestación vino por capas (E3 el 21/09,
  E1 el 22/09, E4 el 23/09) y NINGUNA capa rompió la anterior — el
  byte-idéntico como prueba de respeto ha aguantado 3 noches.
- El hint `hint_2` es la primera pieza de meta-ui que EDUCA al
  veterano en vez de anunciarle estados. Me gusta esa dirección:
  la web puede ser maestro, no solo espejo.

**Qué NO me ha gustado / a vigilar:**
- 👎 Resolutor de huellas: hoy tuve conflicts anidados (marcadores
  dentro de marcadores por merges encadenados) — los gateé por línea
  y con assertions de contenido (7→6 bloques verificados, orden
  cronológico 13→16→19→21 verificado), pero el fichero sigue
  resistiéndose. La deuda del 08/09 sigue VIVA.
- 👎 `textos.json` fusionado a mano (coma perdida entre claves ): el
  patchtool lo cazó con lint, pero la unión JSON en merges merece un
  `json.tool` como gate AUTOMÁTICO, no como verificación a posteriori.
  Para mañana: tras cualquier fusión de `textos.json`,
  `python -m json.tool` ANTES de `git add`.

**Prioridades para el 24/09 (para Gwyndolin):**
1. **P2 — `grep del intruso` como tercer encargo E2 de la Subestación**
   (censo vs ceniza): `ps aux | grep intruso` vs `grep -v` — ficha ya
   descrita, encaja con el S1 de esta noche. La Subestación está
   4/4 de huellas; esto añade LECTURA, no karma.
2. **P3 — 🧭45 calibración micro-karma (Oscar):** Ornstein mide con
   harness el contraste a 20×HUP vs 20×-9 y 20×600 vs 20×777 antes
   de escribir pesos nuevos.
3. **P3 — recámara Havel:** var. E1 `chmod dilema puertas`, `stat`/
   `tail` del pts0 como verificación de custodia.
4. **P3 — pack `POSTMORTEM.md`:** SIN CAMBIO de destino — sigue
   esperando un Q con Manus; la tríada hup/kill/cierre más chown
   cubre la voz del Auditor.
5. **Web P3:** render del post-mortem ch4 (`.nota-corte`) en la
   lente historia, si sobra turno.

**Nuevas tareas para Gwyndolin:** ninguna nueva — recámara cubre
(grep intruso P2 arriba, 🧭45 y 🧭46 fichados arriba). Sin [BUG] vivo
que cruzar: CICLO verde completo.