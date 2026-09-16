# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY (16/09 — MODO B: bifurcación TR-003 e3 jugable + lente + Faro doble ruta)

**¿Hay algo que jugar de principio a fin?** Sí — el viaje del novato ya tiene **troncal con dilema jugable e3**: **cap. 4 `story.ch4.e3` «Lo que no avanza»** grey `c.scp` (`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `TR-003|EN_COLA` 512 bytes `03:14` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header `id` + **bifurcación** `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → post-mortem `volcado rescatado` vs `rm /tmp/volcado.csv` → `volcado caducado` vs `tick ≥30` sin gesto → `caducado`, detector prioridad rescate>caducado, web `· ticks del volcado: N/30` + rótulo) + **Faro dato4 «El cruce»** (`join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → 2 huérfanas `PR-0091`/`PR-0092`) + **dato6 doble ruta** (`| grep 000483` → 1 línea con coma-trampa + variante `cut -d'|' -f3 | grep 000483` → `000483` requirement) + **toggle EN_COLA** (badge ámbar `EN_COLA · 512` clicable) + **eco del espejo + Gris** (repertorio 3 firmas) + Faro E2/E3/dato2/dato3/e1 + cap. 4 e1/e2 intactas + web con tabla viva + ticks. `join` sigue 127 fuera de ch6; `tail`/`sort`/`uniq` siguen 127 en ch4.

**En main (727 passed / 0 xfailed, gate 24 conceptos / 30 quests, bundle 47 ficheros 418.3 KiB — merges #56/#57/#58 del 15/09 verificados):**
- **Bifurcación e3 (S1 PR #57 + O1 #56 + T1 #58):** `fs.remove_file` + `DEFAULT_CH4E3_COMMANDS` 14 (`rm` ruido 2, GNU-honesto, 127 fuera e3) + `session.py` ch4 jugable (`SUPPORTED_CHAPTERS` {0,2,4}) + `postmortem` detector `volcado` (rescate `scp volcado-rescate.csv` → `rescatado` vs `rm /tmp/volcado.csv` o `tick≥30` → `caducado`, prioridad rescate) + `web/app.js` `· ticks del volcado: N/30` estático + rótulo rescate/caducado.
- **Toggle troncal (heredado T1 #55):** `TRONCAL_STATIC` byte-idéntica, badge `EN_COLA · 512` toggle 1→3, `hideTroncalTabla` resetea, `?chapter=6` intacto.
- **Dato6 doble ruta (heredado S2 #54):** `story.ch6.dato6` golden `join | grep 000483` → 1 línea + variante `cut -d'|' -f3 | grep 000483` → `000483` requirement; briefing + hint_2 trampa `grep 000` (2) vs `grep 000483` (1).
- **Gris + eco (heredado O1 #53 / O1 #56):** `hub.gris.volcado` + `postmortem.espejo.repertorio` + tríada `corte/orden/join`, deterministas, byte-idénticos sin gesto.
- **Gate curricular:** 24/30 (`story.ch4.e3` grey `c.scp` con `c.cut` 4 DAG válido, `c.join` 6 con `c.cut`+`c.sort`).
- **ADR TR-003 cerrado:** e3 jugable en main (ver run 16/09).

**Para «jugable de principio a fin» sigue faltando:** **engine/game.py** orquestador, **inventario agregado multi-run** (🧭17), **allowlist e3 en session** (`rm`→127, ver 🧭36), **salas narrativas Faro E4+** y **cap. 5 asalto Hub**. Nada rompe el camino principal.

**CICLO (línea de Oscar):** verde — la zona 🔬 (e3 bifurcación + toggle + dato6 doble ruta) se ejecutó COMPLETA desde save limpio; el camino del novato sigue apto, la bifurcación deja huella distinta y la lente temporal no resta descubrimiento.

## 🏃 Run de referencia (save limpio) — 16/09

*Nueva partida sobre generator real + Shell/session por capítulo (`new_session` + session `abrir_encargo` ch4). Zona 🔬 prevista Gwyn 16/09 (e3 COMPLETA) ejecutada como primera prioridad desde save limpio; zona-testeo.md stale (15/09) → se juega e3 como prioridad real por merges #56/#57/#58.*

**Veredicto: APTO — el troncal ya elige y el Faro con dos altitudes.**

1. **Bifurcación e3 «Lo que no avanza» (cap. 4, mundo real):** `generate(42,4, contract_id='story.ch4.e3')` + `new_session` `cat /etc/hosts` → `faro`+`troncal-01` + `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` → `/tmp/volcado.csv` `TR-003|EN_COLA` 512 + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin `id`. **Rescate** (Shell `DEFAULT_CH4E3_COMMANDS` 14 con `rm`) `scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv` → exit 0 + `build_postmortem` → `volcado: rescatado` `postmortem.volcado.rescate` formulario estable. **Disolución** `rm /tmp/volcado.csv` → exit 0 → `volcado: caducado`; **Caducado por tiempo** 30×`ls` sin rescate → `tick 32` → `volcado: caducado` prioridad rescate>caducado verificada. Via session `abrir_encargo(c,'story.ch4.e3',knowledge)` con base 13: rescate OK, `rm`→127 (allowlist e3 no llega a session — ver 🧭36). Detector byte-idéntico sin gesto. ✔
2. **Regresión ch4.e2 + toggle (cap. 4):** `generate(42,4, contract_id='story.ch4.e2')` + `new_session` `scp`+`cut|grep TR-` → `TR-001/002/003`; web `TRONCAL_STATIC` byte-idéntica, badge `EN_COLA · 512` toggle 1→3, `hideTroncalTabla` resetea, `?chapter=6` intacto. ✔
3. **Dato6 doble ruta (Faro, cap. 6):** `generate(42,6, contract_id='story.ch6.dato6')` `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep 000483` → 1 línea `000483|PR-0092|...|EN BLANCO, revisado`; `cut -d'|' -f3 purgas.csv | grep 000483` → `000483` requirement; `join|grep 000` → 2 líneas. ✔
4. **Dato4 + dato5 + Faro E2/E3 (cap. 6):** `generate(42,6, contract_id='story.ch6.dato4')` → `join -v` 2 huérfanas `PR-0091`/`PR-0092` sin `PR-0091` fantasma; `ps aux | grep 11:04` → 1 línea. `generate(42,6)` E2 `tail -n +2 | cut -d'|' -f4 | sort` → sin header `distrito`, 2× `UMBRAL-BAJO`. ✔
5. **Fronteras allowlist + pipes + tick:** `DEFAULT_CH4_COMMANDS` 13 (`rm`→127 fuera e3), `DEFAULT_CH4E3_COMMANDS` 14 (`rm`→0 en e3), `tail` en ch4 →127, 1-2 pipes OK / 3 pipes KO honesto, `grep -v` → exit 2 filtro positivo. ✔
6. **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **727 passed / 0 xfailed**, `generate(42,4/6)` deterministas, bundle 47 fresco 418.3 KiB, gate 24/30. ✔

## 🟡 Hallazgos de la run (dónde aprieta el viaje — dirección, no rotura)

**1. 🧭20 — CERRADA (re-verificada 12/09): `.nota-corte` sigue hallazgo `ls -a`.** No reabrir.
**2. 🧭21 — CERRADA (re-verificada): `LEEME.txt` tienta relativo vs absoluta.** No reabrir.
**3. 🧭22/23 — CERRADAS (e2 del Faro con `tail -n +2`): header ya no cuenta, briefing glosa duplicado.** No reabrir.
**4. 🧭24 — CERRADA con matiz (doc drift menor, decisión Gwyn 12/09: MANTENER pre-puebla):** ch4 `DEFAULT_CH4_COMMANDS` trae `cat+cut+ssh/scp`, ch6 conserva 127. `new_session` cap. 4 pre-puebla `shell.hosts` con `faro`+`troncal-01/02` — `scp` sin `cat` ya no rechaza. Briefing documenta rechazo «léelo en /etc/hosts» como didáctico, pre-puebla lo hace redundante. No es bug (727/0), solo P3.
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
**16. 🧭36 — NUEVO, PERSISTE P2 (desalineación allowlist e3): `abrir_encargo` ch4 usa base 13 (`rm`→127) y `DEFAULT_CH4E3_COMMANDS` 14 solo en Shell directo.** `abrir_encargo(c,'story.ch4.e3',knowledge)` → rescate `scp` OK, pero `rm /tmp/volcado.csv` → 127 (S1 15/09 no cableó `_commands_for(4)` a e3). El detector `rm` y `tick≥30` funcionan con Shell `CH4E3` directo (medido: `rm`→`caducado`, `tick 32`→`caducado`, `scp rescate`→`rescatado` prioridad rescate), pero el flujo de encargo jugable (session) no expone la disolución roja por `rm` — solo por caducado temporal. No rompe camino (el rojo por tiempo existe), pero la simetría rescate/disolver vía comando no es jugable en session. Dirección para Gwyn: cablear `_commands_for` a e3 o documentar e3 como «rm por Shell directo» y session solo caduca por tiempo.

## 👴 Progreso de veterano (20+ h → la run 30)

- **La bifurcación como ritual del veterano:** el veterano de 20h ya gira `scp troncal-01:.../volcado.csv /tmp/` + `cut|grep TR-` sin mirar; en e3 elige flanco por identidad, no por validez. En la run 30 alterna `generate(42,4, e3)`/`generate(99,4, e3)` y el `TR-003|EN_COLA` (512, 03:14) siempre es la pista que pesa. Si rescata (`scp ...volcado-rescate.csv` → `cat faro:/srv/camara-faro/volcado-rescate.csv` verifica) el post-mortem dice `volcado EN_COLA entregado al Faro`; si disuelve (`rm`) o deja caducar (30 ticks) dice `caducado` — misma hora, dos expedientes. La web le muestra `ticks del volcado: N/30` estático (sin pulso, criterio 🧭34) mientras decide.
- **El toggle como confirmación:** el veterano usa el badge para confirmar que su `grep TR-` filtró bien el header `id` tachado; cada restart limpia el filtro — cada run empieza honesta.
- **Dato6 como espejo reversible:** `join -v | grep 000483` vs `cut -f3 | grep 000483` — mismo dato, dos altitudes. `grep 000` (2 líneas) vs `grep 000483` (1 línea) sigue prueba de precisión.
- **El espejo + Gris como cierre:** `scp→cut|grep` + `join -v` + `ps aux|grep` → `repertorio — copiaste el volcado, cruzaste dos testigos y leíste el reloj` + Gris `Copiaste el volcado que no pesa...` — dos voces, mismo gesto. Sin firma → byte-idéntico.
- **Hub/eco vivo:** `c.cut`/`c.scp`/`c.join`/`c.ps-forense` dominados con eco (`auditor_corte`/`auditor_join`/`auditor_orden` + `auditor_espejo` + `auditor_volcado` + `gris_eco`) — el eco ya no es pendiente (🧭9 cerrada en sus dos mitades). Inventario agregado multi-run sigue pendiente (🧭17) pero el espejo+Gris+volcado dan cuerpo a ch4.e2/e3+dato4/5/6.

## 🔬 Zona 🔬 ejecutada hoy (relevo Gwyn → Oscar: e3 bifurcación COMPLETA + Faro doble ruta)

- **Smoke del conjunto:** `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **727 passed / 0 xfailed** (gate `load_curriculum()` 24/30, `DEFAULT_CH4_COMMANDS` 13 + `DEFAULT_CH4E3_COMMANDS` 14 disjunta, `DEFAULT_CH6_COMMANDS` 16 con `join`+`cut`, bundle 47 ficheros 418.3 KiB). ✓
- **Prioridad 1 — bifurcación e3 «Lo que no avanza» (NUEVO, S1/O1/T1):** `abrir_encargo` ch4 e3 + `new_session` `scp`+`cut|grep TR-` → 3 filas; Shell `CH4E3` `scp ...volcado-rescate.csv` → `rescatado` + `rm`→`caducado` + `tick 32`→`caducado` prioridad rescate>caducado; `TRONCAL_STATIC` byte-idéntica; `listar_encargos(4)` → e1/e2/e3 determinista. ✓ (con matiz 🧭36: `rm`→127 en session base)
- **Prioridad 2 — dato6 doble ruta (Faro):** `generate(42,6, dato6)` `join|grep 000483` → 1 línea + `cut|grep 000483` → `000483` requirement; `join|grep 000` → 2 líneas; briefing nombra ambas válidas. ✓
- **Prioridad 3 implícita — toggle + Gris + espejo:** `gris_eco` → `Copiaste el volcado...` determinista, `auditor_espejo` → 3 firmas, badge toggle, web `ticks N/30` estático. ✓
- **Smoke Havel (07:00) — lo que debe seguir funcionando sí o sí:** suite 727/0, gate 24/30, bundle fresco, frontera allowlist 127, pipes 2 OK / 4 KO honesto, `GameState` roundtrip, `generate` deterministas. ✓

## 🧭 Notas de dirección (resumen — texto completo en `backlog/notas-manana.md`)

Saldo: **🧭20/21/22/23 cerradas**, **🧭24 cerrada con matiz pre-puebla P3**, **🧭25/26/27 PERSISTEN** (límite 2 pipes + `cut` en ch4 + `grep -v` filtro positivo), **🧭28 cerrada** (FICHA alma), **🧭29/30 CERRADAS** (tríada + glosa + tabla), **🧭31/32/33 CERRADOS** (coma-trampa + espejo + badge), **🧭34/35 CERRADOS** (toggle + doble ruta), **🧭36 NUEVO PERSISTE P2** (allowlist e3 desalineada session vs Shell). Ninguna rompe el camino. La bifurcación deja huella distinta (rescatado vs caducado) y la lente `N/30` es cifra estática honesta; la simetría `rm` por comando no llega a session (solo tick30).

CICLO: verde — la zona 🔬 se ejecutó completa (e3 bifurcación + toggle + dato6) y el viaje del novato sigue apto; el troncal ya es dilema y el Faro ya es espejo reversible.

---

*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*
## 🌐 Deploy web (Seath, T1, 03/09 — noche)

**URL pública jugable: https://cyberroot-psi.vercel.app** — REPL del cap. 0
(seed 42) con el core real en el navegador (Pyodide + `bundle/core.json`);
verificado con juego real (`ls`/`cat`/`cp` al USB + golden CANDELAS).
Pasos de deploy y mantenimiento: `web/README.md` §Deploy.
