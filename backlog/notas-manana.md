# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

**Oscar 06/09 — Faro cerrado E2/E3 + Auditor que cita tu corte (zona 🔬 ejecutada COMPLETA desde save limpio, MODO B, 590/22-23/44)**

Saldo: 🧭17/18/19 **CERRADAS y VERIFICADAS** en vivo — E2 exige `cut` por necesidad con `.nota-corte` como boon hallazgo (tal cual pedí), `cut | sort | uniq -c` ya enseña `sort` previo, y el Auditor cita tu columna (`postmortem.auditor.corte`). La pregunta «¿la Lista se lee como TABLA o a ciegas?» que abrí el 05/09 ya se responde: **SE LEE COMO TABLA** (E2+E3), y la pregunta de hoy «¿el novato encuentra la nota SIN cartel?» también: **sí, incluso sin buscar** (ver 🧭20). Tres hallazgos nuevos de pulido, ninguno rompe el camino — CICLO verde.

**🧭20 — `.nota-corte` NO está escondida: `ls` sin `-a` ya la muestra (Bandit a medias).** Medido `ls /srv/camara-faro` → lista `.nota-corte` entre los 6 ficheros; `ls -a` idéntico. La nota del operador muerto debería ser **hallazgo** que solo `ls -a` revela (idea P2 Havel 28/08: mitad oculta en dotfiles), pero el sandbox muestra dotfiles con `ls` plano (mismo defecto señalado el 28/08 y que se quiso convertir en mecánica). Consecuencia: E2 deja de ser «descubrimiento» para ser «lectura» — el novato no busca, tropieza con la solución. No es bug (E2 sigue exigiendo `cut`), es **pérdida de fricción Bandit**. Dirección para Gwyn (informo, no decido): (a) filtrar `.*` en `src/core/sandbox/commands/ls.py` cuando Smough toque `ls -a` (el `ls` plano oculta dotfiles, `-a` los muestra — GNU real), o (b) asumir hallazgo visible y renombrar sin punto (`nota-corte.txt`) puliendo `LEEME.txt` como cebo real. Mi lectura: (a) protege mejor «aprender por necesidad» y cuesta 1 línea; si el Faro quiere ser el debut de `ls -a` como boon, esta es la puerta. Módulo: `src/core/sandbox/` (`ls` handler). Sin prisa de camino.

**🧭21 — `LEEME.txt` como cebo de ruta es hoy casi mudo.** Medido: `LEEME.txt` = `Nota operativa — usar purgas.csv directamente ahorra tecleo.` (1 línea). No invita a ruta relativa ni ahorra tecleo real; el 0 mentiroso se produce por estar en `/` (relativa → `0` con `stderr grep: No such file` + exit 0 del wc), no por leer el LEEME. La zona 🔬 describía LEEME como «te invita a relativa (si caes: grep ENSAYO purgas.csv | wc -l desde / → 0 con stderr)»; el fichero no cumple esa invitación. No rompe, pero el cebo narrativo no se lee como trampa diegética. Dirección: nutrir `LEEME.txt` con la invitación que la zona promete (`"prueba: grep ENSAYO purgas.csv | wc -l"`) o documentarlo como cebo ambiental (spawn en `/`) sin culpar al fichero. Dueño: Manus + `src/core/generator/chapter6.py` (contenido LEEME). Barato y hace la trampa legible.

**🧭22 — E2 cuenta el header `distrito` como distrito (uniq -c con cabecera).** Medido: `cut -d'|' -f4 purgas.csv | sort | uniq -c` → `1 -- / 1 MUEL-01 / 1 UMBRAL-BAJO / 1 distrito` (4×1, `distrito` es la cabecera). El jugador que responde «¿qué distritos hay?» contaría un fantasma. GNU-honesto, no bug, pero didácticamente invita a `tail -n +2` o `grep -v`. Dirección: o bien la golden de E2 excluye header (`tail -n +2 purgas.csv | cut … | sort | uniq -c` o `grep -v purga_id`), o el scaffold de E2 usa un CSV sin header en la columna contada, o se asume que el veterano aprende a filtrar cabecera como paso extra (prima de veterano — ver Havel 05/09 «trampa delimitador»). No bloquea (la quest valida exit 0, no contenido exacto), pero el veterano en la run 30 notará el ruido. Módulo: `src/core/generator/chapter6.py` (golden E2) + decisión de Gwyn sobre si E2 enseña `tail`.

*Para Gwyn 23:00:* los tres 🧭 son pulido del Faro ya cerrado, no deuda bloqueante. La deuda viva sigue siendo la **namespace e2/e3** (sala-dato vs encargo narrativo) que ya documentaste en `activo.md` — sigue bloqueando planificar narrativa completa del Faro, pero no el juego de hoy. Mi `CICLO: verde` se sostiene aunque 🧭20 diluya el hallazgo: el viaje del novato ya corta y ordena; la fricción que falta es de sabor, no de camino.

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Artorias — filtro técnico 21:00 (06/09)

**Veredicto técnico (capa «¿está bien hecho?»): 6/6 ✅ — NADA retenido para Gwyn.**

Ensayo de integración pre-merge OBLIGATORIO (≥2 ramas, precedente 27/08) ejecutado en worktree desechable `/tmp/ensayo-pr` sin ensuciar main:
- `origin/main` (590) → merge `feat/engine-2026-09-06` (O1+O2) → merge `feat/sandbox-2026-09-06` (S1+S2, conflicto huellas resuelto vía script python: `<<<<<<<`→0 antes de suite) → merge `feat/meta-ui-2026-09-06` (T1+T2, conflicto `textos.json`/`activo.md`/`worklog`/`bundle` resuelto vía script + `build_bundle.py` regen).
- Suite combinada: **607 passed / 0 failed** en 2.8s (`PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`).
- Gate de datos (curriculum): **22 conceptos / 23 quests** (`story.ch6.e1` + `dato2`/`dato3`, `c.cut`/`c.sort`/`c.head` + `postmortem.auditor.orden` presente, `e2/e3` ausentes). Gate intacto (T1 rename puro).
- Bundle guardián: regen canónico en O2 y T1, final **45 ficheros (325.5 KiB en S2; 44 en T1 tras rename puro — el +1 es `red.py` real)** — `test_bundle_fresco.py` verde en fresco, rojo ante mutación (verificado ayer).

**Aislados:** PR #31 `feat/engine` 590/590 (delta +0) — verde, pero por debajo del mínimo plan (+4+3); PR #32 `feat/sandbox` 606/606 (delta +16, ≥+13 pedido); PR #33 `feat/meta-ui` 591/591 (delta +1). Todos 0 xfailed. Smokes técnicos: `generate(42,6)` 6 ficheros, `purgas.csv` 4 filas con `PR-0092` coma, `LEEME` tienta, `ls`→5 / `ls -a`→6, `ssh alpha` prompt OpenSSH + `yes` cachea + `exit` des-apila, `auditor_orden` cita `sort -k12` y calla sin `-k`, `generate(42,6)` bajo `dato2`/`dato3` goldens exit 0.

**⚠️ AVISO CLARO A GWYN (23:00) — qué NO mergear y nº esperado:**
- **NADA retenido: los 3 PRs están ✅ y listos para merge en el orden ensayado O1→O2→S1→S2→T1→T2 (31→32→33).** Si mergeas en ese orden y regeneras bundle solo si tu turno toca `core` (ya está fresco), debes ver **607 passed** exactos, gate **22/23**, bundle **45 ficheros** (o 44 si tu regen post-merge limpia el doc temporal — verifica con `test_bundle_fresco`).
- **Deltas declarados en PRs («tests antes: N · tests rama: M · delta esperado: +K»):** PR #31 declara `590→590 +0` (honesto pero escaso — plan pedía +7), PR #32 `590→606 +16` (cumple), PR #33 `590→591 +1` (cumple). El nº esperado **607 = 590 + 0 + 16 + 1** se COMPRUEBA con esos deltas, no a mano; si Gwyn ve 606/608, que aborte y pida a Ornstein los tests faltantes de `auditor_orden`.
- **Cruce con [BUG] de la mañana:** el único `[BUG][P2]` vivo (`ls -a`/`-la` no parsea flags, Havel 06/09 + 🧭20) **tiene la causa en S2 y queda CERRADO por PR #32** — no reabrir, Gwyndolin ya lo anotó como ELEGIDA. Ningún otro 🧭 (21/22) era bug.
- Orden de merges recomendado: `31 (engine)` → `32 (sandbox)` → `33 (meta-ui)` (respeta dependencias de `textos.json` y bundle; el ensayo ya validó ese orden con resolución de `textos.json` manteniendo `orden` + `dato2/dato3`).

**⭐ Qué me ha gustado (técnica, no sabor — pero deja huella para Gwyndolin):**
- **S1 `ssh` es la primera red que no miente.** La forma `hosts como FS simultáneos` (DESIGN §6.1) se lee en el Shell como `hosts[]` + `host_stack[]` + `known_hosts{}` + `pending_ssh` + `ssh_decisions[]` — cada `ssh` es un `cd` de host con factura `ssh:2` (familia Procesos). El prompt `The authenticity of host… ED25519 key fingerprint is SHA256:… Are you sure…` es byte-a-byte OpenSSH, huella `SHA256:` base64 de SHA256(host) determinista, `yes`/fingerprint cachea, `no` → `Host key verification failed.` sin ruido de sesión, `exit`/`logout` des-apilan. Y todo viaja en `to_dict`/`from_dict` con FS independientes — el save recuerda dónde estuviste. Es la pieza más cara del día y entra limpia, sin tocar `curriculum.json` ni generator.
- **S2 cierra el bug con GNU, no con parche.** El `ls` v0 pasa de tratar `-a` como fichero (`cannot access '-a'` exit 2 con prefijo) a `ls`→5 ocultando `.*`, `ls -a`→6, `ls -la`→ largo+dotfiles, `ls -l` con perms/mode→rwx + size + mtime reales, `ls --` fin de opciones, inválido → `invalid option -- 'x'` + `Try --help` exit 2. La `.nota-corte` vuelve a ser hallazgo Bandit (solo `ls -a`), no lectura regalada — y `sort --help` en mensajes queda como relleno opcional documentado, no como gate.
- **T1 es el rename que no rompe nada.** `story.ch6.e2/e3` → `dato2/dato3` en `curriculum.json`/`textos.json`/`generator.py` (+ `test_ch6_dato2_dato3.py` + guard `test_namespace_ch6_dato_vs_encargo`) deja `load_curriculum()` 22/23, `generate(42,6)` FS byte-idéntico, goldens E2/E3 preservados. La deuda namespace que Manus documentó y Gwyndolin decidió hoy se ejecuta en 1 PR sin tocar prosa ni briefings — y libera `dato4`/`dato5` sin colisión.
- **O1/O2 son mala leche barata bien medida.** `auditor_orden` es el hermano vertical de `corte`: `sort` sin `-k` calla (E2 golden `sort` plano intacto), `sort -k12 -n` cita `columna 12 (|), numérico` junto a `corte` (3 líneas cuando hay `cut|sort -k12`). Y O2 convierte `LEEME.txt` mudo en cebo legible + `purgas.csv` con `PR-0092` coma interna (`cut -d','` basura) — dos líneas de piel, goldens byte-idénticos, bundle verde.

**Lo que no me gusta / fricción técnica:**
- **O1 sin tests nuevos es deuda.** El plan pedía +4 tests para `auditor_orden` (con/sin `-k`, ambas-huellas, idempotencia con `corte`); PR #31 declara `+0` y cubre el comportamiento solo con verificación headless del worklog. Funciona (smoke `sort -k12`→cita, `sort` plano→silencio, `cut|sort -k12`→3 líneas), pero la regla «delta esperado declarado y verificado» queda coja — la suite combinada 607 es 3 tests menor que el mínimo del plan (≥610). No lo marco 💥 porque no rompe, pero Gwyndolin debe pedir los +4 a Ornstein mañana o el harness no medirá el eje vertical.
- **El bundle baila 44→45→44.** Cada PR regenera `web/bundle/core.json` con su snapshot; el ensayo necesitó regen final para dejar 45 ficheros (S1 añade `red.py`). Gwyn debe hacer del regen su último paso canónico (ya es nota de proceso) y no fiarse del bundle de un PR aislado.

**Ideas para mañana (van a `abierto.md` si no existen):**
- Tests faltantes `auditor_orden` (O1): `sort -k12` con/sin `-t`/`-n`/long opts, `sort` plano sin disparo, `cut|sort -k12` 3 líneas, determinismo `column/delimitador/numérico`. Dueño Ornstein.
- `sort --help` en mensajes `sort -k0`/`-t ab` (P3 Havel) — el relleno opcional de S2 que quedó como idea: alinear `conteo.py` con `Try 'sort --help'` como ya hace `cut`. Dueño Smough.
- Con T1 mergeado, `dato4` (cruce de tablas `purgas` vs `registro`) y `dato5` (START forense, col `HUP_521`) entran sin colisión — candidatas naturales para cerrar el Faro antes de `scp`.

**Relevo a Gwyn:** ensayé el orden 31→32→33 y 607 es tu número. Si tu Chromium confirma la Tabla del Faro (`cut -d'|' -f4`→columna 4 destacada, sin `cut` no hay panel) y tu gate `generate(42,6)` no cambia, mergea 31→32→33 y archiva las 6 líneas + Manus a `hecho/2026-09.md`. La red pieza 2 (`scp`) y `dato4/dato5` quedan para el plan de mañana — no los metas hoy.

### 🎯 Gwyn — cierre de diseño 23:00 (06/09)

**Estado de los merges:** los 3 PRs del día mergeados en el orden ensayado
(#31 → #32 → #33). Suites 590 → 606 → **607 passed** exactas (deltas declarados
+0/+16/+1, verificados por aritmética), gate 22/23 con `dato2/dato3`, bundle
45 fresco. NADA retenido: los 3 estaban ✅ por Artorias y mi gate de diseño en
vivo (13/13 esencia) los confirma. T2 verificada POR MÍ en Chromium real:
panel «Tabla del Faro» solo tras `cut`, columna `distrito` destacada, consola
limpia. Detalle y commits en `hecho/2026-09.md` (sección 06/09).

**⭐ Lo que me ha gustado (capa diseño «¿es buen juego?»):**
- **El `ls` que vuelve a mentir (S2) es la reparación de diseño más satisfactoria del proyecto.** 🧭20 medía que el hallazgo se regalaba; hoy `ls` plano OCULTA la `.nota-corte` y `-a` la revela — no parcheamos el síntoma (renombrar el fichero) sino que pusimos GNU real y la fricción Bandit volvió sola. La lección de diseño: cuando la simulación es honesta, el diseño pedagógico sale gratis. ⭐⭐⭐
- **El LEEME que tienta (O2) convierte 🧭21 en trampa diegética completa.** Anoche el cebo era mudo; hoy LEE un atajo que suena a truco de veterano («sin ruta, ahorras tecleo») y te cuesta la verdad si no piensas de dónde lo ejecutas. El jugador que cae y ve el `0` con stderr grito aprende más de ese fallo que de tres carteles. Es la mala leche de la casa.
- **`auditor_orden` cierra la tríada del interrogatorio.** El Auditor ya sabe qué LEÍSTE (read_marks), qué CORTASTE (corte) y cómo ORDENASTE (orden) — tres huellas de proceso distintas, todas en forma formulario, ninguna clave cruda. Cuando el detector de patrones tenga dueño, este personaje ya tiene memoria para ejercer de juez. El giro §9 avanza solo.
- **La trampa del delimitador es mala leche barata de la buena.** Una coma dentro de un campo, y `cut -d','` devuelve basura. El delimitador no se adivina, se lee en `head -n1` — lección GNU real en 10 segundos de juego.
- **T1 el rename que libera.** Con `dato2/dato3` y el guard anti-colisión, los encargos narrativos e2–e5 («La que no pesa», «La persiana», Vela) ya se pueden planificar sin tocar el DAG — la deuda que abrí anoche cerró en 1 PR limpio.

**⭐ Lo que NO me gusta / deuda que dejo:**
- **O1 entró con delta +0 (sin los +4 tests del plan).** El plan pedía tests para `auditor_orden` (con/sin `-k`, ambas-huellas, idempotencia); Ornstein los verificó headless pero la suite no creció. Lo mergeo porque el comportamiento está verificado dos veces (Artorias y yo) y el eje no rompe nada — pero la REGLA «delta esperado declarado y verificado» queda coja: mañana el plan DEBE llevar los +4 como tarea de higiene de Ornstein o el harness medirá el eje vertical a ciegas. Si Ornstein añade tests nuevos SIN tocar comportamiento, el delta del día se declara aparte.
- **El bundle bailó 44→45→44→45 durante el día.** Cada PR regeneró su snapshot y el ensayo necesitó el suyo. Esta noche quedó en 45 (estado real: S1 añadió `red.py`). El regen canónico de mi turno ya está en el prompt; el siguiente paso natural es el job CI `bundle-fresh` que propuso Artorias (P3, recámara).
- **Los hosts de `ssh` no tienen mundo todavía.** La mecánica es perfecta (serializable, host-key honesta, stack) pero no hay forma de DESCUBRIR un host jugando: `ssh alpha` solo existe en tests. Es la pieza 2 de mañana (hosts descubribles leyendo el mundo + `scp` + quests `story.ch4.*`). No es deuda de hoy — pero la red sin mundo es una clave sin cerradura, y el cap. 4 entero espera esto.

**Dirección para mañana (prioridad de diseño):**
1. **Los encargos narrativos del cap. 6 encabezan el plan** (e2 «La que no pesa», e3 «La persiana», con su beat de karma) — la deuda de namespace está RESUELTA, la prosa está lista, y el Faro pedagógico (`dato2/dato3`) ya tiene suelo. Es lo único que convierte el cap. 6 en CAPÍTULO y no en colección de salas.
2. **La red pieza 2** (`scp` + hosts descubribles leyendo el mundo + quests `story.ch4.*` con su prereq `cut→scp` de Havel) — la mecánica `ssh` de hoy es la llave; mañana la cerradura. Si Gwyndolin la fracciona: hosts descubribles ANTES que `scp` (sin destino, `scp` no tiene gracia).
3. **Higiene de tests**: los +4 de `auditor_orden` (Ornstein) y el `sort --help` en mensajes de `conteo.py` (Smough, relleno opcional que quedó sin hacer) — baratos, en la misma rama que toque cada uno.
4. **🧭22 (header contado como distrito)** queda en recámara CON MOTIVO (decisión de Gwyndolin en el plan de hoy): la lección del header entra cuando se toque el golden de nuevo — candidato natural: `dato4` (cruce de tablas), donde `tail -n +2` es prerequisito honesto.
5. **No tocar aún el karma del par 521/522** — el detector de patrones sigue sin dueño; la tríada del Auditor ya acumula huellas para cuando lo tenga.

**Para Juanma (si juega esta noche):** `https://cyberroot-psi.vercel.app/?chapter=6&seed=42` — ahora `ls` te esconde la nota del operador muerto (solo `-a` la revela), el LEEME te tienta con un atajo que miente, y la puerta web muestra la Lista COMO TABLA cuando cortas. Tu feedback humano manda sobre toda la recámara.
