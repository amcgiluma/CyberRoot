# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (17/09 — MODO B: cadena troncal→Faro cerrada, e3 simétrico + dato7 condicional)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya tiene **cadena cruzada**: **cap. 4 `story.ch4.e3` «Lo que no avanza»** grey `c.scp` (`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `TR-003|EN_COLA` 512 bytes `03:14` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id` + **bifurcación simétrica** `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → post-mortem `volcado rescatado` vs `rm /tmp/volcado.csv` → `caducado` vs `tick ≥30` → `caducado`, prioridad rescate>caducado — **ambas por verbo via `abrir_encargo`** + **cap. 6 `story.ch6.dato7` «El fantasma que pesa»** grey `c.join` (`volcado-rescate.csv` SOLO si rescataste → `join -t'|' -1 1 -2 1 volcado-rescate.csv purgas.csv | grep TR-003` → 1 línea; si caducado → `No such file` y el join nombra la ausencia) + **Faro dato4 «El cruce»** (`join -t'|' -1 3 -2 1 -v 1` → 2 huérfanas) + **dato6 doble ruta** (`| grep 000483` vs `cut -f3 | grep 000483`) + **toggle EN_COLA** + **eco espejo+Gris** (3 firmas). `join` 127 fuera de ch6; `tail/sort/uniq` 127 en ch4.

**En main (738 passed +1 failed `test_bundle_fresco` stale por `session.py` → 739 tras regen canónico, gate 24 conceptos / 31 quests, bundle 47 ficheros — merges #59/#60 del 16/09 parciales, T1 Seath 16/09 aún EN CURSO):**
- **E3 simétrico (O1 PR #59, 🧭36 CERRADA):** `_commands_for(4,'story.ch4.e3')` 14 con `rm` (ruido 2 GNU-honesto) vs base 13 en e1/e2 (`rm`→127 intacto); `abrir_encargo(c,'story.ch4.e3',knowledge)` expone `rm` y pre-puebla `hosts` remotos (`cat /etc/hosts` ya no es requisito para `scp`), `scp rescate`→exit 0 + `build_postmortem`→`volcado: rescatado`, `rm`→`caducado`, `tick 30`→`caducado`, prioridad rescate>caducado.
- **Dato7 condicional (S1 PR #60):** `chapter6.py` `VOLCADO_RESCATE_*` + `build_chapter6_fs(fs_rng, volcado_rescatado)` condicional; `generate(..., volcado_rescatado=True/False)` determinista por seed+flag; `curriculum.json` `story.ch6.dato7` grey requires `c.join` (gate 24/30→31, DAG `c.scp 4→c.cut 4→c.join 6` válido); textos `story.ch6.dato7.*` (golden `join -t'|' -1 1 -2 1 volcado-rescate.csv purgas.csv | grep TR-003`); 8 tests nuevos; bundle 426.2 KiB regenerado por Smough (regla 12/09).
- **Toggle + Gris + espejo (heredados T1 #55 / O1 #53):** `TRONCAL_STATIC` byte-idéntica, badge `EN_COLA · 512` toggle 1→3, `hideTroncalTabla` resetea, `gris_eco` + `auditor_espejo` 3 firmas deterministas.
- **Dato6 doble ruta (S2 #54):** `join|grep 000483` y `cut|grep 000483` ambas requirement; `grep 000`→2 vs `grep 000483`→1.
- **ADR TR-003 cerrado:** e3 + dato7 jugables en main (ver run 17/09).
- **Web pendiente:** T1 Seath 16/09 (tooltip `N/30` + lente Faro) sigue EN CURSO — `web/app.js` sin cambios en main, bundle stale 1 fichero (`session.py`) pendiente regen canónico de Gwyn.

**Para «jugable de principio a fin» sigue faltando:** **engine/game.py** orquestador, **inventario agregado multi-run** (🧭17), **salas narrativas Faro E4+** y **cap. 5 asalto Hub** (con `START 03:14` como firma). **🧭36 ya no falta** (cableada). Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (cadena e3→dato7) se ejecutó COMPLETA desde save limpio con simetría `scp` vs `rm` verificada y Faro condicional byte-determinista; el camino del novato sigue apto y la consecuencia cruza capítulos sin fricción.

## 🏃 Run de referencia (save limpio) — 17/09

*Nueva partida sobre generator real + `abrir_encargo` por capítulo (knowledge con `c.scp`/`c.join`). Zona 🔬 prevista stale (15/09) → se juega prioridad real 16/09 (cadena TR-003) como primera prioridad desde save limpio; MODO B headless.*

**Veredicto: APTO — la cadena ya pesa en el mundo, no solo en el post-mortem.**

1. **E3 simétrico «Lo que no avanza» (cap. 4, mundo real, 🧭36 CERRADA):** `abrir_encargo(cur,'story.ch4.e3',['c.scp'])` → `abrible True`; `sess.shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/")` → exit 0 + `/tmp/volcado.csv` `TR-003|faro|troncal-01|512|EN_COLA`; `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id`. **Rescate** `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → exit 0 → `build_postmortem` → `volcado: rescatado` `postmortem.volcado.rescate` «Expediente 000: volcado EN_COLA entregado al Faro.» **Disolución por verbo** `rm /tmp/volcado.csv` → exit 0 → `volcado: caducado` «sin entrega — caducado.» **Caducado por tiempo** `scp` + 30×`ls` → `tick 31` → `caducado` (prioridad rescate>caducado verificada). `e1/e2` `rm`→127 intacto (frontera 13 vs 14). ✔
2. **Dato7 condicional «El fantasma que pesa» (cap. 6, NUEVO S1):** `generate(42,6, volcado_rescatado=True)` → `/srv/camara-faro/volcado-rescate.csv` `id|origen|destino|bytes|estado` + `TR-003|faro|troncal-01|512|EN_COLA`; `Shell(DEFAULT_CH6_COMMANDS, cwd="/srv/camara-faro")` `join -t'|' -1 1 -2 1 volcado-rescate.csv purgas.csv | grep TR-003` → exit 0 1 línea; `generate(42,6, volcado_rescatado=False)` → fichero NO existe → `join` → `join: volcado-rescate.csv: No such file or directory` exit 1 + `cat volcado-rescate.csv` → mismo; `generate(42,6)` por defecto sin volcado (no rompe dato4/dato6/e1, `ps aux | grep 11:04` → 1 línea). `load_curriculum()` 24/31 con `story.ch6.dato7` grey `c.join`. ✔
3. **Dato6 doble ruta (Faro, cap. 6):** `generate(42,6)` `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep 000483` → 1 línea `000483|PR-0092|...|EN BLANCO, revisado`; `cut -d'|' -f3 purgas.csv | grep 000483` → `000483` requirement; `join|grep 000` → 2 líneas. ✔
4. **Dato4 + Faro E2/E3 (cap. 6):** `generate(42,6)` `join -v` 2 huérfanas `PR-0091`/`PR-0092`; `tail -n +2 | cut -d'|' -f4 | sort | uniq -c` sin header, 2× `UMBRAL-BAJO` con `head -n 3` orden `-k12`. ✔
5. **Fronteras allowlist + pipes + determinismo:** `DEFAULT_CH4_COMMANDS` 13 (`rm`→127 fuera e3), `DEFAULT_CH4E3_COMMANDS` 14 (`rm`→0 solo e3), `tail` en ch4 →127, `c.cut` 4/6, `c.scp` 4, `c.join` 6, 1-2 pipes OK / 3 KO honesto, `grep -v`→exit 2 filtro positivo, `generate(42,4/6)` determinista. ✔
6. **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **738 passed +1 failed `test_bundle_fresco` (bundle stale `session.py`, esperado — 739 tras `python tools/web/build_bundle.py`)**, `load_curriculum()` 24/31, bundle 47 ficheros. Bundle stale no rompe camino (el `core` es correcto, solo falta regen canónico de Gwyn). ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 del Faro con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA con matiz (doc drift menor, decisión Gwyn 12/09: MANTENER pre-puebla):** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127. `abrir_encargo`/`new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo «léelo en /etc/hosts» como didáctico, pre-puebla lo hace redundante. No es bug (738+1 stale), solo P3.
**5. 🧭25 — PERSISTE (observación): límite 2 pipes (3 cmds) + redirección no soportada.** `cut|grep TR-` 1 pipe OK, `cut|grep|sort` con `sort`→127 en ch4 no bloquea; ch4.e2/e3 diseñan en 1 pipe evitando límite.
**6. 🧭26 — PERSISTE (dirección menor): `c.cut` vive en cap. 4, Faro e1 no es primer `cut`.** e1 `grep|wc`, dato2/e2 exigen `cut` por necesidad. Correcto.
**7. 🧭27 — PERSISTE (fricción menor, decisión Gwyn 11/09: filtro positivo): `grep -v` vía pipe NO soportado.** `join|grep -v sujeto` → exit 2. FICHA dato4/dato6 y ch4.e2/e3 usan filtro positivo — Gwyn decidió NO implementar `-v`.
**8. 🧭28 — CERRADO (verificación positiva): FICHA ch4.e2 con alma pulida.** `story.ch4.e2.beat` con `03:14`+`512 bytes`+`TR-003|EN_COLA`.
**9. 🧭29 — CERRADO (tríada Auditor `corte→orden→join` con voz):** retícula determinista, prefijos disjuntos.
**10. 🧭30 — CERRADO (glosa 127 + tabla troncal hermana):** glosa solo `join` fuera de ch6, tabla viva con columna 1 | resaltada.
**11. 🧭31 — CERRADO (dato6 coma-trampa):** `join -v | grep 000483` devuelve coma en campo 5 — `cut -d','` parte.
**12. 🧭32 — CERRADO (eco del espejo testigo):** ①+②+③ → `copiaste el volcado, cruzaste dos testigos y leíste el reloj` byte-idéntico sin firma.
**13. 🧭33 — CERRADO (badge `EN_COLA · 512` con presión diegética):** badge ámbar con 512/03:14, preview limpio, header `id` tachado.
**14. 🧭34 — CERRADO (toggle lente):** badge clicable → solo `TR-003` (como `grep EN_COLA` con ojos), restart limpia.
**15. 🧭35 — CERRADO (dato6 doble ruta honesta):** `join` y `cut` pesan lo mismo, sin callejón.
**16. 🧭36 — CERRADA (verificación positiva 17/09): allowlist e3 simétrica en session.** `abrir_encargo(c,'story.ch4.e3',knowledge)` → `scp`→`rescatado`, `rm`→`caducado`, `tick 31`→`caducado` prioridad rescate; `e1/e2` `rm`→127 intacto; `DEFAULT_CH4E3_COMMANDS` 14 disjunta de base 13. La simetría `scp` vs `rm` ya es jugable en el flujo que el jugador usa (session), no solo en Shell directo. CERRADA por PR #59 (Ornstein).

## 👴 Progreso de veterano (20+ h → la run 30)

- **La cadena como ritual del veterano:** el veterano de 20h ya gira `scp troncal-01:.../volcado.csv /tmp/` + `cut|grep TR-` sin mirar; en e3 elige flanco por identidad, no por validez. En la run 30 alterna `generate(42,4, e3)`/`generate(99,4, e3)` y el `TR-003|EN_COLA` (512, 03:14) siempre es la pista que pesa. Si rescata (`scp ...volcado-rescate.csv` → `volcado: rescatado`) el Faro guarda `volcado-rescate.csv` y `join … volcado purgas | grep TR-003` le devuelve su testigo; si disuelve (`rm`) o deja caducar (30 ticks) el Faro amanece sin fichero y el `join` le responde `No such file` — misma hora, dos mundos. La web le muestra `ticks del volcado: N/30` mientras decide (tooltip pendiente T1 Seath).
- **El Faro como espejo reversible:** `join -v | grep 000483` vs `cut -f3 | grep 000483` — mismo dato, dos altitudes. `grep 000` (2) vs `grep 000483` (1) sigue prueba de precisión; `cut -d','` coma-trampa intacta. Dato7 añade `volcado-rescate.csv` como tercera tabla del Faro, solo visible si trajiste el testigo.
- **El espejo + Gris como cierre:** `scp→cut|grep` + `join -v` + `ps aux|grep` → `repertorio — copiaste el volcado, cruzaste dos testigos y leíste el reloj` + Gris `Copiaste el volcado que no pesa...` — dos voces, mismo gesto. Sin firma → byte-idéntico. Con `dato7` el repertorio suma `volcado: rescatado|caducado` como cuarta firma.
- **Hub/eco vivo:** `c.cut`/`c.scp`/`c.join`/`c.ps-forense` dominados con eco (`auditor_corte`/`auditor_join`/`auditor_orden` + `auditor_espejo` + `auditor_volcado` + `gris_eco`) — el eco ya no es pendiente (🧭9 cerrada en sus dos mitades). Inventario agregado multi-run sigue pendiente (🧭17) pero el espejo+Gris+volcado+cadena dan cuerpo a ch4.e2/e3+dato4/5/6/7.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: cadena e3→dato7 COMPLETA)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **738 passed +1 failed `test_bundle_fresco` (stale `session.py`, esperado → 739 tras regen)** (gate `load_curriculum()` 24/31, `DEFAULT_CH4_COMMANDS` 13 + `DEFAULT_CH4E3_COMMANDS` 14 disjunta, `DEFAULT_CH6_COMMANDS` 16 con `join`+`cut`, bundle 47 ficheros). ✓
- **Prioridad 1 — e3 simétrico «Lo que no avanza» (O1 #59, 🧭36 CERRADA):** `abrir_encargo` ch4 e3 + `scp`+`cut|grep TR-` → 3 filas; `scp ...volcado-rescate.csv` → `rescatado` + `rm`→`caducado` + `tick 31`→`caducado` prioridad rescate>caducado; `TRONCAL_STATIC` byte-idéntica; `listar_encargos(4)` → e1/e2/e3 determinista; `e1/e2` `rm`→127 intacto. ✓
- **Prioridad 2 — dato7 condicional (S1 #60, NUEVO):** `generate(42,6, volcado_rescatado=True)` → `volcado-rescate.csv` existe + `join -t'|' -1 1 -2 1 volcado purgas | grep TR-003` → 1 línea; `generate(42,6, volcado_rescatado=False)` → NO existe → `join` `No such file`; `generate(42,6)` por defecto sin volcado; 8 tests, gate 24/31. ✓
- **Prioridad 3 — dato6 doble ruta (Faro):** `generate(42,6, dato6)` `join|grep 000483` → 1 línea + `cut|grep 000483` → `000483` requirement; `join|grep 000` → 2 líneas; briefing nombra ambas válidas. ✓
- **Smoke Havel (07:00) — lo que debe seguir funcionando sí o sí:** suite 738+1 stale→739, gate 24/31, bundle fresco tras regen, frontera allowlist 127, pipes 2 OK / 4 KO honesto, `GameState` roundtrip, `generate` deterministas. ✓ (bundle stale no rompe camino, solo falta `python tools/web/build_bundle.py` de Gwyn)

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23 cerradas**, **🧭24 cerrada con matiz pre-puebla P3**, **🧭25/26/27 PERSISTEN** (límite 2 pipes + `cut` en ch4 + `grep -v` filtro positivo), **🧭28 cerrada** (FICHA alma), **🧭29/30 CERRADAS** (tríada + glosa + tabla), **🧭31/32/33 CERRADOS** (coma-trampa + espejo + badge), **🧭34/35 CERRADOS** (toggle + doble ruta), **🧭36 CERRADA** (allowlist e3 simétrica). Nueva: **dato7 condicional verde sin deuda**. Ninguna rompe el camino. La cadena troncal→Faro ya es mundo (fichero), no solo post-mortem; bundle stale 1 fichero pendiente regen canónico.

CICLO: verde — la zona 🔬 se ejecutó completa (e3 simétrico + dato7 + toggle + dato6) y el viaje del novato sigue apto; la cadena cruza capítulos y el Faro responde con presencia/ausencia.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*
## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
