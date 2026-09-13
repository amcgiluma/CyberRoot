# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (13/09 — MODO B: tríada Auditor completa + 127 que enseña + tabla viva del troncal)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya tiene troncal con alma y Faro con cruce: **cap. 4 `story.ch4.e2` «El volcado que no pesa» grey (`cat /etc/hosts` → `faro`+`troncal-01`/`02`, `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `TR-003|EN_COLA` 512 bytes `03:14`, `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id`, FICHA con alma 6 claves) + Faro `dato4` «El cruce» (`join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → 2 huérfanas `PR-0091`/`PR-0092` con header `sujeto`, dato5 «La persiana» `ps aux | grep 11:04` → 1 línea) + Faro E2/E3/dato2/dato3/e1 + cap. 4 e1 «La llave prestada» intacta + web con tabla viva del troncal hermana del Faro.** `join` sigue 127 fuera de ch6 con glosa didáctica `Try 'join --help' — tables cross there (chapter 6).` (solo `join`, el resto 127 seco); `tail`/`sort`/`uniq` siguen 127 en ch4; `auditor_join` cita el anti-join sin filtrar datos de fila.

**En main (698 passed / 0 xfailed, gate 24 conceptos / 28 quests, bundle 47 ficheros 396.7 KiB — merges #47/#48/#49 del 12/09 verificados):**
- **Auditor con 4ª huella (O1 PR #47):** `postmortem.auditor.join` — `build_postmortem` detecta `join` con `-v`/`-v1`/`-v 1`/`-av`/tras pipe (`_find_join` shlex pipe-aware) y añade `auditor_join`+`auditor_join_text` «Expediente 000: cruce registrado — join anti-join (-v): huérfanas de la primera tabla. Continuidad del ensayo: estable.» + segunda línea en `lines_resolved`; sin `join` byte-idéntico a antes; `join` sin `-v` NO dispara; no filtra datos de fila (texto formulario, no contador `PR-0091`).
- **127 que enseña (S2 PR #48):** `join` fuera de ch6 → exit 127 `sh: command not found: join` + `Try 'join --help' — tables cross there (chapter 6).`; resto de comandos inexistentes → 127 seco sin glosa; en ch6 `join a b` funciona y NO da 127.
- **Tabla viva del troncal en web (T1 PR #49):** `?chapter=4&seed=42` preview estático `TR-001/002/003` ( `TRONCAL_STATIC` byte-idéntico a `chapter4.py` `TRONCAL_CONTENT`) ANTES de `scp`, y tabla viva-live DESPUÉS de `scp /tmp/` con reflejo de `cut -d'|' -f1`; cap. 4 only, restart limpia ambos paneles (Faro intacto).
- **Cap. 4 e2 jugable con alma (S2+T1+FICHA Manus 12/09):** `generate(42,4, contract_id='story.ch4.e2')` determinista byte-idéntico 42×2; `new_session().execute("cat /etc/hosts")` exit 0 `10.6.0.5 faro`+`10.6.1.10 troncal-01` (seed 1 → +`10.6.1.11 troncal-02` 3 hosts); `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` exit 0 deja `id|origen|destino|bytes|estado` + `TR-001|OK 1024` + `TR-002|OK 2048` + `TR-003|EN_COLA 512`; `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` 3 líneas sin `id`; `GameState(shell).to_dict/from_dict` roundtrip idéntico preservando `hosts` multi-host y `/tmp/volcado.csv`.
- **Faro dato4+dato5 intactos:** `generate(42,6)` → `join -t'|' -1 3 -2 1 -v 1` exit 0 `sujeto|…` + `000|PR-0091|EN BLANCO|--|ENSAYO|--|0|1|HOSP-47-C` + `000483|PR-0092|…|EN BLANCO, revisado` (coma-trampa); `ps aux | grep 11:04` → 1 línea `PR-0091` sin señuelo; determinismo 42×2 stable seeds 7/99.
- **Gate curricular:** 24/28 (`c.cut` 4 + `c.scp` 4 → `story.ch4.e2` grey DAG válido, `c.join` ch6 prereqs `c.cut`(4)+`c.sort`(6) DAG válido).
- **Bandit + Shell límites:** `ls`5 vs `ls -a`6, `tail -n +2 | cut | sort` 2 pipes OK, `tail|cut|sort|uniq -c` 3 pipes → `multiple pipelines not supported` exit 2; `grep -v` vía pipe → exit 2 (filtro positivo como lección, decisión Gwyn 11/09).

**Para «jugable de principio a fin» sigue faltando:** **engine/game.py** orquestador, **inventario agregado multi-run**, **salas narrativas Faro e3+** y **eco diegético del espejo** (🧭9). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (auditor_join + glosa 127 + tabla viva troncal) se ejecutó COMPLETA desde save limpio; el camino del novato sigue apto y la tríada Auditor ya tiene su cuarta huella con voz.

## 🏃 Run de referencia (save limpio) — 13/09

*Nueva partida sobre generator real + Shell por capítulo (`new_session` + `DEFAULT_CH4_COMMANDS` / `DEFAULT_CH6_COMMANDS`). Zona 🔬 de Gwyn 13/09 ejecutada como primera prioridad desde save limpio.*

**Veredicto: APTO — el Auditor ya cita tu cruce, el 127 enseña el Faro y el troncal se ve como tabla.**

1. **`auditor_join` — 4ª huella post-mortem (cap. 6, dato4, mundo real):** `generate(42,6, contract_id='story.ch6.dato4')` + `new_session` `cd /srv/camara-faro` + `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` exit 0 `sujeto|…`+`000|PR-0091|EN BLANCO|--|ENSAYO`+`000483|PR-0092|…|EN BLANCO, revisado` (header + 2 huérfanas). `build_postmortem(shell.to_dict())` → `lines_resolved` 2 líneas: `auditor_text` pico `join (2)` + `auditor_join_text` «cruce registrado — join anti-join (-v): huérfanas de la primera tabla. Continuidad del ensayo: estable.»; variantes `join -v1`/`-v 1`/`-av`/`cat purgas.csv | join -t'|' … -v 1 - registro.csv` también disparan; `join` sin `-v` → 1 línea sin `auditor_join`; sin `join` (`cat purgas.csv`) → 1 línea byte-idéntica a antes (sin `auditor_join` key). Texto no filtra fila (`PR-0091` ausente, solo formulario). ✔
2. **Glosa 127 que nombra el Faro (cap. 0/4, frontera):** `generate(42,0)` + `new_session` `join` → exit 127 `sh: command not found: join` + `Try 'join --help' — tables cross there (chapter 6).`; `generate(42,4)` + `join` → idéntica glosa; `foobar`/`tail` en ch4 → exit 127 seco sin glosa; `generate(42,6)` + `join -t'|' -1 3 -2 1 purgas.csv registro.csv` → exit 0 sin glosa (funciona). `generate(42,6)` intacto determinista. ✔
3. **`story.ch4.e2` «El volcado que no pesa» — `cat`→`scp`→`cut|grep` (cap. 4, mundo real):** `generate(42,4, contract_id='story.ch4.e2')` + `new_session` `cat /etc/hosts` → exit 0 `10.6.0.5 faro`+`10.6.1.10 troncal-01` (seed 1 → +`troncal-02` 3 hosts); `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → exit 0 deja `/tmp/volcado.csv` con `TR-003|EN_COLA 512`; `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → exit 0 `TR-001/TR-002/TR-003` sin `id`; `cut -d'|' -f1` sola → `id`+3 (equivocar enseñando). `GameState(shell).to_dict/from_dict` idéntico preservando `hosts` y `/tmp/volcado.csv`. ✔
4. **Regresión cap. 4 + Faro intacto:** `generate(42,4)` sin contract → `story.ch4.e1` (sigue prefiriendo `e1`); `generate(42,6)` intacto → `join | grep PR-0091` →1 línea; `ps aux | grep 11:04` →1 línea `PR-0091` sin señuelo; determinismo 42×2 y seed 7/99 stable. ✔
5. **Fronteras allowlist + pipes:** `DEFAULT_CH4_COMMANDS` 13 exactos (`join` no en ch4, `cut` sí); `tail` en ch4 →127, 1 pipe OK / 3 pipes KO, `grep -v` → exit 2 (filtro positivo documentado). ✔
6. **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **698 passed / 0 xfailed**, `generate(42,4/6)` deterministas, bundle 47 fresco 396.7 KiB, gate 24/28. ✔
   *(Nota técnica auditada 13/09: `web/bundle/core.json` contiene `TRONCAL_STATIC` byte-idéntico a `src/core/generator/chapter4.py` `TRONCAL_CONTENT` en `web/app.js` — duplicación intencional verificada por Artorias 12/09, guardián verde. Si Manus toca el volcado, hay 2 sitios que actualizar — deuda señalada por Gwyn.)*

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 del Faro con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA con matiz (doc drift menor, decisión Gwyn 12/09: MANTENER pre-puebla):** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127. `new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` (O1 09/09) — `scp` sin `cat` ya no rechaza. El briefing aún documenta el rechazo «léelo en /etc/hosts» como didáctico, pero la pre-puebla lo hace redundante. No es bug (698/0, `scp` copia, `GameState` roundtrip preserva hosts), solo P3 si algún día confunde.
**5. 🧭25 — PERSISTE (observación documentada): límite 2 pipes (3 cmds) + redirección no soportada.** `cut|grep TR-` 1 pipe OK, `cut|grep|sort` con `sort`→127 en ch4 (frontera), `cat|cut|grep|wc` 3 pipes (4 cmds) → exit 2 honesto. Redirección `>` → `syntax not supported`. No bloquea (ninguna quest pide 3 pipes); `ch4.e2` se diseñó en 1 pipe evitando el límite.
**6. 🧭26 — PERSISTE (dirección pedagógica menor, no bug): `c.cut` ya vive en cap. 4, Faro e1 no es primer `cut`.** e1 solo pide `grep|wc`, dato2/e2 sí exigen `cut` por necesidad. Ningún camino rompe; Gwyn mantiene e1 sin `cut`.
**7. 🧭27 — PERSISTE (fricción menor, no bloqueante, decisión Gwyn 11/09: filtro positivo): `grep -v` vía pipe NO soportado.** `join|grep -v sujeto` → exit 2, `ps aux|grep -v root` → exit 2. Causa: `_run_grep` sin flags. FICHA dato4 y ch4.e2 ya usan filtro positivo (`grep TR-`/`grep 000`/`grep PR-0091`) y Gwyn decidió NO implementar `-v`. No rompe.
**8. 🧭28 — CERRADO (verificación positiva): FICHA ch4.e2 con alma pulida — el troncal ya tiene alma.** `story.ch4.e2.beat` con `03:14`+`512 bytes`+`TR-003|EN_COLA` sin AI-slop, `brief/briefing` con `cat /etc/hosts`→`scp`→`cut|grep TR-` 1 pipe y límite 2 pipes documentado.
**9. 🧭29 — NUEVO, CERRADO (verificación positiva 13/09): tríada Auditor completa `corte→orden→join` se siente como testigo, no como checklist.** Medido: `join -v` dispara `auditor_join` solo con anti-join (`-v`/`-v1`/`-v 1`/`-av`/pipe+join), sin `-v` NO dispara (el `join` normal ya lo cubre el pico), sin `join` byte-idéntico (sin key `auditor_join`, `lines_resolved` 1 vs 2). Texto formulario sin datos de fila (`PR-0091` ausente, `Expediente 000` sí). La retícula corte→orden→join se reconoce como la misma voz en 3 huellas — pregunta de sabor «¿feels like the Auditor saw your cross?» → sí.
**10. 🧭30 — NUEVO, CERRADO (verificación positiva 13/09): glosa 127 enseña sin marear y tabla viva del troncal da que hacer.** Medido: glosa SOLO con `join` fuera de ch6 (`Try 'join --help' — tables cross there (chapter 6).`), resto de 127 secos; en ch6 `join` funciona sin glosa. Web: `?chapter=4&seed=42` preview estático `TR-001/002/003` sin `id` antes de `scp`, tabla viva-live `TR-001/TR-002/TR-003` con columna 1 | resaltada después de `cut -d'|' -f1 /tmp/volcado.csv | grep TR-`; cambia de capítulo (`?chapter=6`) el panel desaparece; restart limpia ambos paneles (Faro+Troncal). Pregunta sabor «¿la glosa del 127 enseña o marea? ¿la tabla da que hacer o solo muestra?» → enseña (nombra el Faro, no regala la query) y da que hacer (el `cut|grep TR-` deja de ser texto para ser columna que ves).

## 👴 Progreso de veterano (20+ h → la run 30)

- **La tríada ya es ritual del veterano:** tras 20h el veterano reconoce el post-mortem por su segunda línea — `corte` (si cortaste), `orden` (si ordenaste `sort -k12`), `join` (si cruzaste con `-v`). En la run 30 sin `join` el informe es byte-idéntico a antes (1 línea); con `join` aparece la segunda sin tocar el pico. El veterano que vuelve a dato4 para cazar la coma-trampa `PR-0092` redescubre que `cut -d'|' -f3 purgas.csv` y `join -v` son hermanas (cortar vs cruzar).
- **El 127 como mapa mental:** el veterano ya no teclea `join` en cap. 0/4 — la glosa `tables cross there (chapter 6).` es el cartel que recuerda dónde vive cada verbo. Como `scp` que nombra `/etc/hosts`, el 127 ya no es muro sino brújula. El veterano que prueba `sort` en ch4 y recibe 127 seco sabe que no todo lo que existe en ch6 vive fuera.
- **Troncal como mini-Faro:** el veterano que dominó `cut -d'|' -f1` en ch4.e2 lo reusa en ch6 dato2/e2 (`cut -d'|' -f4 | sort | uniq -c`) y en dato4 (`join` es `cut` de tablas cruzadas). En la run 30 alterna `generate(42,4)`/`generate(1,4)` y deja `TR-003|EN_COLA` siempre la pista que pesa (512 bytes, 03:14, `faro`+`troncal-01` siempre, a veces `troncal-02` variable por seed) — el header `id` siempre fantasma que el veterano filtra sin pensar, ahora con la tabla viva que también resalta la columna 1.
- **El límite 2 pipes y `>` como techo creativo:** el veterano ya encadena `cut|grep TR-` (1 pipe) y `cut|sort|uniq -c` en dos líneas para contar sin header; el que intente `tail|cut|sort|uniq -c` recibe mensaje exacto y aprende el límite. Con `>` no disponible, «encadenar con `> /tmp`» no es alternativa — la FICHA ch4.e2 ya evita el problema diseñando en 1 pipe.
- **Hub/eco aún pendiente:** `c.cut`/`c.scp`/`c.join`/`c.ps-forense` dominados sin eco diegético (🧭9), inventario agregado multi-run sin cruzar runs (🧭17). Con `cut|grep TR-` dejando `TR-003|EN_COLA` y `join -v 1` dejando `PR-0091` y `ps aux` dejando `START 11:04`, el eco del espejo de Gris («copiaste el volcado / cruzaste tablas / leíste el reloj») es la pieza que daría cuerpo a ch4.e2+dato4/5.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: auditor_join + 127 + tabla viva troncal)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **698 passed / 0 xfailed** (gate `load_curriculum()` 24/28, `DEFAULT_CH4_COMMANDS` 13 cmds con `cut/scp` sin `join`, `DEFAULT_CH6_COMMANDS` 16 cmds con `join`+`cut`, bundle 47 ficheros 396.7 KiB). ✓
- **Prioridad 1 — `auditor_join` anti-join (cap. 6, dato4, mundo real):** `generate(42,6, contract_id='story.ch6.dato4')` + `new_session` `cd /srv/camara-faro` + `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` exit 0 `sujeto|…`+`000|PR-0091|EN BLANCO|--|ENSAYO`+`000483|PR-0092|…|EN BLANCO, revisado`; `build_postmortem` con `-v` → `auditor_join_text` presente + `lines_resolved` 2, sin `-v` → 1 línea sin `auditor_join`, sin `join` → byte-idéntico a antes (solo pico); variantes `-v1`/`-v 1`/`-av`/pipe+join deterministas, sin filtrar `PR-0091`. ✓
- **Prioridad 2 — 127 que enseña + tabla viva del troncal (cap. 0/4 + web):** `join` en cap. 0→127 con glosa `Try 'join --help' — tables cross there (chapter 6).`, en ch4 idéntica glosa, `foobar`→127 seco, `tail` en ch4→127 seco, `join` en ch6→exit 0 sin glosa; web `?chapter=4&seed=42` preview estático `TR-001/002/003` con columna 1 | antes de `scp`, `cut -d'|' -f1 /tmp/volcado.csv` refleja tabla viva-live con columna 1 resaltada y sin `id`; cambia a `?chapter=6` el panel troncal desaparece (cap. 4 only); restart limpia ambos paneles (Faro+Troncal intactos). `scp`/`cut|grep TR-` 1 pipe OK, `grep -v`→exit 2 (filtro positivo). ✓
- **Smoke Havel (07:00) — lo que debe seguir funcionando sí o sí:** suite 698/0, gate 24/28, bundle 47 fresco 396.7 KiB, frontera allowlist 127, pipes 2 OK / 4 KO honesto, `GameState` roundtrip multi-host, `generate` determinista 42×2 intactos. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23 cerradas**, **🧭24 cerrada con matiz pre-puebla P3**, **🧭25/26/27 PERSISTEN** (límite 2 pipes + `cut` en ch4 + `grep -v` filtro positivo), **🧭28 cerrada** (FICHA ch4.e2 con alma), **🧭29/30 NUEVOS CERRADOS** (tríada `corte→orden→join` con voz + 127 que enseña + tabla viva). Ninguna rompe el camino. Preguntas de sabor de la zona — «¿feels like the Auditor saw your cross? ¿la glosa del 127 enseña o marea? ¿la tabla del troncal da que hacer o solo muestra?» — se responden: **sí — el Auditor cita el cruce sin filtrar fila con la misma retícula que corte/orden, la glosa del 127 nombra el Faro sin marear (solo `join`, resto seco, en ch6 no hay glosa) y la tabla del troncal hermana del Faro da que hacer (preview estático antes de `scp`, tabla viva-live tras `cut|grep TR-`, columna 1 resaltada, cap. 4 only, restart limpio).**

CICLO: verde — la zona 🔬 se ejecutó completa (auditor_join 4 variantes + 127 4 casos + troncal shell+web) y el viaje del novato sigue apto; la tríada ya tiene su cuarta huella sin cicatriz.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*

## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
