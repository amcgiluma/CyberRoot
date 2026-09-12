# historia/ — La narrativa de CyberRoot (carpeta de trabajo de Manus)

> ✍️ **Manus** (03:00) escribe aquí la historia del juego, contra la espina
> fija de `docs/DESIGN.md` §2 (12 beats) y las reglas operativas §2.6.
> Estructura definida en AGENTS-PLAN §6.1 — este índice la materializa.

## Mapa

```
historia/
  INDICE.md        ← ESTE fichero: estado del arco narrativo
  PERSONAJES.md    → fichas de voz ANTES de dar diálogo a nadie (regla §2.6.5)
  ESCENARIOS.md    → lugares: Subestación, tres anillos, nodos tipo del Grid
  CAPITULOS/       → un fichero por capítulo-campaña (0–6), esquema → texto
  FRAGMENTOS.md    → botín narrativo H1/H2 con orden fijo por capítulo (§9 P5)
```

## Flujo de entrega
Manus escribe AQUÍ. Para entrar al juego, sus textos viajan a `src/data/story/`
con claves JSON — lo hace el ejecutor integrador (no Manus), para no romper
formato. Piezas listas para integrar se marcan `[LISTA]` en INDICE.md.

## Reglas de oro (resumen — el detalle manda en DESIGN)
1. Cada encargo = objetivo técnico + beat narrativo + decisión de karma +
   gancho post-mortem (§2.6.1). Sin barrera técnica no hay avance de trama.
2. Morir SIEMPRE avanza: cola de eventos con líneas nuevas por caso (§2.6.2).
3. Ficha de voz obligatoria antes de escribir cualquier personaje (§2.6.5),
   con fila «nunca diría». Test del nombre tapado.
4. Objetos de lore: dato técnico arriba, grieta humana abajo, un número
   concreto por descripción. Cero adjetivos atmosféricos.
5. Todo en español de España; comandos/salidas técnicas en forma real.

## Estado — FUNDACIÓN (27/08, primer turno de Manus)
- Beats 1–12 definidos (DESIGN §2.5). Capítulos 0–6 con necesidad narrativa
  propia (§6.1).
- ✅ Fichas de voz completas (6/6, `PERSONAJES.md`) — desbloquea todo diálogo.
- ✅ Escenarios con datos base (6/6, `ESCENARIOS.md`).
- ✅ Fragmento 1 `[LISTA]` (`FRAGMENTOS.md`). Quedan 3–6 por escribir.
- ✅ Capítulo 0 (`CAPITULOS/00-la-firma.md`, beats 1–3) — prosa RETOCADA el
  28/08 según decisión D1 de Gwyn: `cp` enseñado en la escena técnica (🧭1,
  alineado con la sesión canónica del sandbox) y run 0 falible en prosa (🧭2:
  el bloque del post-mortem de la primera run ya no es rama muerta).
- ✅ Capítulo 1 «Los Muelles» (`CAPITULOS/01-los-muelles.md`, beats 3–4,
  28/08) — pacto, 5 encargos con karma, regla de la luz diegética (🧭3),
  cola de post-mortem de Ceniza, escenas de Zeta, gancho hacia el cap. 2.
- ✅ Capítulo 0 prosa↔FS REALINEADA (29/08, tarea M1): el listado tras
  `cd /srv` muestra UNA entrada (`oficina-vecinal-muelle-norte`); `/usb`
  permanece en la RAÍZ (opción B de Gwyn, 🧭2). Verificado byte a byte contra
  `src/tests/core/sandbox/test_session_cap0.py` (3/3 passed).
- ✅ Fragmento 2 «La pulsera» `[LISTA]` (`FRAGMENTOS.md`, 29/08) — piel
  HOSP-47-C propuesta por Havel; NHC 47-C-0191, fecha de admisión = día de
  la firma; sostiene H1 y H2 a la vez.
- ✅ Capítulo 2 «Facturas» (`CAPITULOS/02-facturas.md`, beats 5,
  29/08) — 5 encargos (`story.ch2.e1`–`e5`: 2 azules, 1 gris, 1 rojo, 1 de
  cierre), pipes como primera sinergia, escenas de Ceniza/Zeta, cola de
  post-mortem con líneas de Auditor por perfil kármico, la Lista nombrada
  por Ceniza y gancho al cap. 3 (el proceso vivo en la subestación
  secundaria). Bloque de terminal con pipes: contrato pedagógico pendiente
  de verificación hasta que el sandbox soporte tuberías (nota del
  integrador).
- ✅ Fragmento 3 «El contrato» `[LISTA]` (`FRAGMENTOS.md`, 30/08) — contrato
  de alquiler del Umbral bajo a nombre de nadie; celda del arrendatario vacía
  de imprenta (no tachada), firma ilegible, «la llave va conmigo», 14 meses
  de pago puntual y luego silencio. Sostiene H1 (se pidió la factura a
  nombre de nadie) y H2 (un contrato sin arrendatario no debería haberse
  firmado jamás) a la vez. Folio OH-UBA-14-0007, candado distinto del 47.
- ✅ Capítulo 3 «Bombas» (`CAPITULOS/03-bombas.md`, beats 5–6,
  30/08) — 5 encargos (`story.ch3.e1`–`e5`: 1 azul, 1 gris, 2 rojos, 1 de
  cierre), deriva del capítulo hacia el descenso del Acto 2. Familia
  Procesos y sistema (`ps`, `env`, `sudo`, `kill`/señales, `tar`), primer
  `sudo` serio con credencial GANADA, y la **grieta de Ceniza PLANTADA**
  (beat 6 §2.5: sabía que el primer trabajo era veneno, no avisó) en su
  propia voz, sin resolver. La regla de la luz (Gris) llega viva al Alto.
  Gancho: la ventana abierta hacia el troncal del Faro (cap. 4).
- ✅ Fragmento 4 «La cuenta» `[LISTA]` (`FRAGMENTOS.md`, 31/08) — estado de
  cuenta impreso del Banco del Muelle (SUCURSAL 47) a nombre de una sociedad
  instrumental llamada como la ciudad, con nómina mensual de `LUMEN DIV.
  ESTRUCTURAS` (filial 44) durante 36 meses y un único recibo HOSP-47-C;
  cerrada por falta de actividad. Sostiene H1 (un estilo de vida pagado con
  un nombre que no existe) y H2 (la nómina de la división de Lumen es la
  factura de mantener a un sujeto sin registro) a la vez. Cruz con la Lista
  (§2.4). Cruza el 47 y el 44 con fragmentos 2-3 sin romper nada.
- ✅ Capítulo 4 «Troncales» (`CAPITULOS/04-troncales.md`, beats 7–8,
  31/08) — 5 encargos (`story.ch4.e1`–`e5`: 1 azul, 1 gris, 2 rojos, 1 de
  cierre), familia Red real (`ssh`, `scp`, túneles) con la regla de la luz
  en su MÁXIMO (Faro: entrar es fácil de intentar, caro de pagar). El
  **giro del Auditor PLANTADO** (beat 8 §2.5: primera pregunta fuera de
  registro, sin resolver — arco §9) y el **expediente** (beat 7) con la
  fila 000 vacía y las dos lecturas sin elegir. El troncal se reescribe los
  días de la firma (11:04 del cap. 2 vuelve como marca). Gancho: la puerta
  que pregunta, presión hacia el cap. 5.
- ✅ Fragmento 5 «El expediente» `[LISTA]` (`FRAGMENTOS.md`, 01/09) —
  expediente médico de salud laboral del hospital del Muelle (HOSP-47-C,
  folio OH-HOSP-47-C-0191, admisión 04:12 del día de la firma), con
  campo «empresa» = VESPER DE GESTIÓN S.L. (cruza con el fragmento 4),
  nombre legible que no es el de los Apagados, tarjeta de cita que repite
  «vuelve el jueves» de la pulsera (2). El que cuelga al lado del de Vela.
  Sostiene H1 (lo pediste tú: un nombre a propósito, una cita reescrita) y
  H2 (el empleador fachada, la revisión muerta «sin emplazar» por un censo
  que no lo tiene) a la vez. Estado 5/6.
- ✅ Capítulo 5 «Subestación» (`CAPITULOS/05-subestacion.md`, beat 9,
  01/09) — 4 encargos (`story.ch5.e1`–`e4`: 2 azules, 1 gris, 1 rojo, cierre
  de doble salida) en la ÚNICA incursión invertida del juego (§6.1):
  defensa del Hub, no intrusión. Regla de la luz invertida (los Muelles:
  Lumen entra con hombres, no sensores; el ruido ES volumen). Familia
  auditoría/defensa (leer logs, cerrar permisos, detectar movimiento).
  Grieta de Ceniza (beat 6) escrita en la casa (E2), el giro del Auditor
  (beat 8) suma su 2.ª sombra, fragmento 5 cae en E4 (cajón 29 del archivo).
  Gancho: el censo, cap. 6.
- ✅ **M1 — Worldbuilding del censo** (`CENSO-LISTA.md`, 02/09): QUÉ se puntúa
  exactamente — campos de `registro.csv` y `purgas.csv`, delimitador `|`,
  ejemplo de fila real, cómo se registra una purga (`ENSAYO`/`CONTINUIDAD`…
  y el hueco que deja un «sin registro» (la purga `PR-0091`, fecha en blanco,
  sujeto sin fila hermana). Doc de CONSULTA para Smough/Ornstein; da DATO a
  las salas-dato del cap. 6 (grep/sort/uniq/cut). Cruza con fragmentos 2–5.
- ✅ **Capítulo 6 «Faro»** (`CAPITULOS/06-faro.md`, beats 10–12, 02/09) — 5
  encargos (`story.ch6.e1`–`e5`: 1 azul, 2 gris, 1 rojo, 1 de cierre) en la
  luz en su MÁXIMO (Anillo Faro, §6.0). Sala-dato sobre la Lista (M1 + familia
  conteo de Havel), escalada al nodo maestro, la **3.ª sombra del Auditor**
  (feed del ensayo callado, palanca de EL TRATO expuesta por el propio
  formulario — arco §9 cerrado sin traición), confrontación con Vela
  (`story.ch6.vela`, cuerpo por primera vez, formato según karma) y los
  finales (§3.4) como DECISIONES de karma en E4/E5, nunca como menú.
  **Fragmento 6 «hoja de cierre» `[LISTA]`** GARANTIZADO al completar la
  cadena final (🧭5): estado 6/6.
- ✅ **Narrativa completa materializada** (02/09): capítulos 0–6 + fragmentos
  1–6, todo `[LISTA]`. El bloqueante de historia (worldbuilding del censo)
  queda resuelto; ya no hay espina narrativa pendiente en `backlog/historia/`.
- ✅ **Mantenimiento 03/09 — coherencia del gate sudo LECTURA (🧭14b)** (`CAPITULOS/03-bombas.md` pulido): E4/E5 hacen explícito que la llave se gana LEYENDO `orden-ceniza.txt` con `cat` antes de `sudo` (Gwyn 02/09 optó por exigir lectura; prosa alineada para el gate que implementa Smough hoy). Verificado contra `SUDO_CREDENTIAL_PATH` real (`/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt`). Sin fichas nuevas. Narrativa sigue `[LISTA]`; cap. 6 jugable verificado anoche (515/21-21, cebo pipe-0, fila PR-0091).
- ✅ **Mantenimiento 05/09 — coherencia post-04/09** (Manus 03:00): auditoría ligera tras los 3 merges (read_marks, `cut` + `c.cut`, guardián bundle, web seed/chapter/muerte). Verificado: cap. 3 E4/E5 siguen alineados con el gate de LECTURA (Gwyn 03/09); cap. 6 E1 ya nombra `cut` para columnas `distrito/puntuacion/motivo_codigo` y la pista M1 `cut -d'|' -f4,12 | uniq -c` ahora EJECUTA (Gwyn live 04/09: exit 0); `CENSO-LISTA.md` y `POSTMORTEM.md` sin contradicción — el pack POSTMORTEM es recámara (prueba/sin_lectura/señal) y O1 solo aterrizó lectura/ciega, resto queda para integrador sin romper prosa. Sin escritura nueva; narrativa sigue `[LISTA]` 6+6, sin deuda. Turno previo muerto a mitad de tool-call (muse-spark-1.3) — migrado a 1.2, huella completa hoy.
- ✅ **Mantenimiento 06/09 — coherencia Faro cerrado + deuda namespace documentada** (Manus 03:00): auditoría post-05/09 tras los 3 merges (O1 corte + O3 LEEME + S1 `sort -k`/`-t`/`-n` + T1/T2 E2/E3 sala-dato). Verificado: `generate(42,6)` expone 6 ficheros (registro/purgas/censo-borrador/aviso/LEEME/.nota-corte), golden E2 `cut -d'|' -f4 | sort | uniq -c` exit 0, golden E3 `sort -t'|' -k12 -n | head -n 3` → 3 líneas con PR-0091 al frente, cebo relativo 0+stderr honesto; `CENSO-LISTA.md` y `06-faro.md` siguen coherentes (delimitador `|`, col 12 = puntuación, PR-0091 ENSAYO). **Deuda confirmada:** las quests sala-dato `story.ch6.e2` («El corte de la Lista») y `e3` («Los más cerca del cero») ocupan los IDs que la prosa reserva para los encargos narrativos E2 «La que no pesa» y E3 «La persiana» (misma colisión para e4/e5 narrativos si avanzan). No rompe juego (suite 590/22-23/44), pero bloquea planificar integración narrativa del cap. 6 sin decidir convención. Recomendación del historiador: renombrar salas-dato a `story.ch6.dato2`/`dato3` (o `e2.sala`) y conservar prosa tal cual — precedente ch1/ch3/ch5 es 1:1, aquí conviene separar «sala-dato» de «encargo» para no reescribir beats. Pack `POSTMORTEM.md` (5 claves: prueba/sin_lectura/señal_muerte/señal_recarga/ceniza.llave) sigue en recámara en «Piezas listas para integrar» — O1 05/09 solo aterrizó `corte`, el resto espera Q con Manus sin bloquear cap. 6. Sin escritura nueva de capítulos; narrativa sigue `[LISTA]` 6+6, deuda documentada para Gwyndolin.
|- ✅ **Mantenimiento 07/09 — coherencia post-06/09: Faro con red pieza 1 y namespace resuelto** (Manus 03:00): auditoría tras los 3 merges del 06/09 (O1 `auditor_orden` + O2 LEEME tienta + trampa `,` + S1 `ssh`+host-key+stack + S2 `ls -a/-l` GNU + T1 rename `dato2/dato3` + T2 tabla viva). Verificado: suite **607 passed / 0 xfailed**, gate **22/23** (`story.ch6.e1` + `dato2`/`dato3`, `e2/e3` fuera salvo guard negativo), bundle **45 ficheros (330.8 KiB)** verde; `generate(42,6)` 6 ficheros con `/srv/camara-faro` (`.nota-corte` oculta sin `-a`, visible con `-a` + `ls -la` long, Bandit restaurado), `purgas.csv` 4 filas con `PR-0092|…|EN BLANCO, revisado` coma-trampa ( `cut -d','` rompe, `cut -d'|'` intacto), goldens `dato2` `cut -d'|' -f4 | sort | uniq -c` y `dato3` `sort -t'|' -k12 -n | head -n 3` exit 0 con PR-0091 al frente, LEEME tienta con atajo relativo explícito, cebo `grep ENSAYO purgas.csv|wc -l` 0+stderr desde `/` vs 1 con absoluta, tríada Auditor `corte`+`orden`+`lectura` ( `cut -f4` cita columna 4, `sort -k12` cita 12/|/numérico, sin `-k` silencio), `ssh` fuera de `DEFAULT_CH*` (gate 127, host-key `SHA256:` determinista, `yes` cachea, `no` no conecta, stack `exit` des-apila — HSD `04-troncales.md` vivo). `CENSO-LISTA.md`/`06-faro.md`/`04-troncales.md`/`03-bombas.md` sin drift; deuda namespace RESUELTA en T1 y documentada aquí como cierre (convención fijada: **E-space 1:1 prosa, sala-dato = `datoN`**). Pack `POSTMORTEM.md` (5 claves) sigue en recámara esperando Q con Manus — `corte`/`orden` ya cubren la voz en formulario, el resto son claves de SEÑAL sin prisa. Sin escritura nueva de capítulos; narrativa sigue `[LISTA]` 6+6, cero deuda narrativa abierta.
|- ✅ **Mantenimiento 08/09 — Faro con red completa + prosa e2 pulida** (Manus 03:00, 09/09): auditoría post-07/09 tras merges #36/#37/#38 (O1 `auditor_orden` + O2 quest `story.ch6.e2` «La que no pesa» + O3 `/etc/hosts` con `faro` + S1 `scp` Fase B + T1 `?seed=`/`?chapter=` + T2 roundtrip scp). Verificado: suite **635 passed / 0 xfailed**, gate **22/24** (`story.ch6.e1` + `dato2`/`dato3` + `e2`, FICHA vacía honesta), bundle **45 ficheros (351.1 KiB)** verde; `cat /etc/hosts` sobre `generate(42,6)` exit 0 descubre `faro` (solo lectura descubre, `ls /etc` no, re-leer no duplica), `scp faro:/srv/camara-faro/purgas.csv` copia real con rechazo didáctico que nombra `/etc/hosts`, golden e2 `tail -n +2 | cut -d'|' -f4 | sort | uniq -c` sin fantasma `distrito` y 2×UMBRAL-BAJO (🧭22/23 cerrados en la quest). **Prosa e2 pulida** en `src/data/textos.json`: beat/briefing/hints/detail reescritos con voz diegética, sin em dashes ni rótulos `concepto:`, preservando goldens y glosas (`tail -n +2`, `/srv/camara-faro/purgas.csv`, `UMBRAL-BAJO`, `PR-0092` `EN BLANCO, revisado`, `un distrito se repite`). `CENSO-LISTA.md`/`06-faro.md`/`04-troncales.md` sin drift. Pack `POSTMORTEM.md` (5 claves) sigue en recámara esperando Q con Manus — `corte`/`orden` ya cubren formulario, resto SEÑAL sin prisa. Narrativa sigue `[LISTA]` 6+6, cero deuda.

|- ✅ **Mantenimiento 09/09 — cap. 4 jugable + coherencia troncal verificada** (Manus 03:00, 10/09): auditoría post-09/09 tras merges #39 (O1 `chapter4.py` + hosts 2–3/seed + `DEFAULT_CH4_COMMANDS` con `ssh`/`scp`) + #40 (O2 quest `story.ch4.e1` «La llave prestada» + `c.scp` prereq `c.cut`; `c.cut` movido 6→4 con prereq `c.wc`, DAG válido) + #41 (T1 circuito ch4 multi-host + dato límite pipes). Verificado: suite **648 passed / 0 xfailed**, gate **23/25** (`c.scp` + `story.ch4.e1` nuevas, `c.cut` 4 ≤ dato2/dato3 6), bundle **46 ficheros (370.4 KiB)** verde; `generate(42,4)` determinista byte-idéntico con `/etc/hosts` `127.0.0.1 localhost` + `# Troncal` + `10.6.0.5 faro` + `10.6.1.10 troncal-01` (+ `troncal-02` si RNG decide 3), `cat /etc/hosts` exit 0 descubre `['faro','troncal-01']` (`ls /etc` no descubre, re-leer no duplica, parser filtra `localhost`/`ip6*`), `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` copia real (TR-001 `id|origen|destino|bytes|estado` con metadatos owner/mode/mtime) y `scp faro:/srv/camara-faro/purgas.csv` también, `GameState.to_dict/from_dict` idéntico multi-host, `generate(42,6)` intacto; `c.scp` chapter 4 prereq `c.cut` chapter 4 prereq `c.wc` (2≤4) — cadena `wc→cut→scp→ch4.e1` válida; briefings `story.ch4.e1.*` con rutas absolutas `/etc/hosts` + `/srv/archivo-troncal/volcado.csv` + `troncal-01` y límite 2 pipes documentado (`tail|cut|sort|uniq -c` 4 eslabones → `multiple pipelines not supported` exit 2 vs `tail|cut|sort` exit 0). `CENSO-LISTA.md`/`06-faro.md`/`04-troncales.md` coherentes: 04-troncales E1 «La llave prestada» como prosa azul de sesión prestada conecta con la piel real (hosts descubribles por lectura) sin drift narrativo — la sesión prestada del beat es ahora el descubrimiento por lectura antes de copiar, misma lección (leer antes de entrar) con verbo `scp` en vez de `ssh who`. Pack `POSTMORTEM.md` (5 claves prueba/sin_lectura/señal_muerte/señal_recarga/ceniza.llave) sigue en recámara esperando Q con Manus — `corte`/`orden` ya cubren interrogatorio, resto SEÑAL sin prisa. Narrativa sigue `[LISTA]` 6+6, cero deuda nueva.

|- ✅ **Mantenimiento 10/09 — Faro dato4 con alma + dato5 forense + coherencia cerrada** (Manus 03:00, 11/09): auditoría post-10/09 tras merges #42 (O1 `dato5` La persiana — 3 procesos `faro-sync` con `START 11:04` culpable + `Aug25` + señuelo variable, `FARO_SYNC_BINARY` compartido, `environment` determinista) + #43 (S2 `dato4` El cruce + handler `join -t'|' -1 3 -2 1 -v 1` GNU-honesto + `c.join` prereq `c.cut`+`c.sort` + quests `dato4`/`dato5` + 12 textos) + #44 (T1 circuito datos ch6 end-to-end + `GameState` roundtrip con procesos). Verificado: suite **680 passed / 0 xfailed** (648+5+20+7, deltas declarados), gate **24/27** (`c.join` + `dato4`/`dato5` nuevas, `c.join` 6 ≥ `c.cut` 4 ≥ `c.wc` 2), bundle **47 ficheros (390.5 KiB)** verde; `generate(42,6)` determinista ×2 con 3 procesos, `ps aux | grep 11:04` → 1 línea `PR-0091` sin `PR-0092`, `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → 3 líneas `sujeto`+`PR-0091|000`+`PR-0092|000483` (cabecera filtra con `| grep 000` → 2 huérfanas, `| grep PR-0091` → 1 fantasma), `cut|sort|uniq -c` sin fantasma intacto, shell 2 pipes intacto (`tail|cut|sort` OK vs `tail|cut|sort|uniq -c` exit 2). **Prosa dato4 pulida** en `src/data/textos.json`: `beat` con alma («Dos libros... La purga nombra; el registro calla. La costura cuenta lo que el censo no»), `briefing` con glosa de header y 2º huérfano `PR-0092` (coma-trampa), `hint_2`/`detail` con `| grep 000` ejecutable (la `grep -v` no existe en sandbox, se sustituye por `grep 000`/`grep PR-0091` verificados exit 0), sin em dashes ni rótulos `concepto:`. `CENSO-LISTA.md`/`06-faro.md`/`04-troncales.md`/`POSTMORTEM.md` sin drift; pack POSTMORTEM (5 claves) sigue en recámara — `corte`/`orden` cubren interrogatorio, resto SEÑAL sin prisa y sin bloqueo. Narrativa sigue `[LISTA]` 6+6, cero deuda nueva. Anti-slop: `grep -nEi` 0 hits sobre `textos.json` dato4 + `06-faro.md`.
|- ✅ **Mantenimiento 11/09 — FICHA ch4.e2 con alma + auditoría 691/24-28** (Manus 03:00, 12/09): auditoría post-11/09 tras merges #45 (S2 quest `story.ch4.e2` «El volcado que no pesa» 24/28 grey `c.cut`+`c.scp`) + #46 (T1 circuito ch4 e1+e2 + guard SUBSET) — suite **691 passed / 0 xfailed** (680+4+7), gate **24/28** (`story.ch4.e2` grey), bundle **47 ficheros (393.8 KiB)** verde; `generate(42,4, contract_id='story.ch4.e2')` golden `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin `id`, `TR-003|EN_COLA` 512 bytes 03:14, `cat /etc/hosts` descubre `faro`+`troncal-01`/`troncal-02`, `GameState` roundtrip intacto, `generate(42,6)` intacto. **Prosa ch4.e2 pulida** en `src/data/textos.json` (6 claves): `beat` con alma («lleva tres noches en el mismo sitio... lo que pesa vs lo que espera») con dato 03:14 y 512 bytes, `brief`/`briefing` con rutas absolutas `/srv/archivo-troncal/volcado.csv` + `/etc/hosts` + `scp troncal-01:.../volcado.csv /tmp/` + `cut -d'|' -f1 | grep TR-` sin header, filtro positivo y 1 pipe, `detail`/`hints` con `id` fantasma y `EN_COLA` como pista, sin em dashes ni rótulos `concepto:`. `CENSO-LISTA.md`/`04-troncales.md`/`06-faro.md`/`POSTMORTEM.md` sin drift; pack POSTMORTEM (5 claves) sigue en recámara — `corte`/`orden` cubren interrogatorio, `auditor_join` queda para reposición O1. Narrativa sigue `[LISTA]` 6+6, cero deuda nueva. Anti-slop: `grep -nEi` 0 hits sobre `textos.json` ch4.e2.

|- DECISIÓN Gwyn (27/08, 🧭5): el ÚLTIMO fragmento de la cadena está
  GARANTIZADO al completar la cadena final del cap. 6 (ver DESIGN §6.1).
  Materializarlo en `FRAGMENTOS.md` cuando se escriba la cadena.