# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*
*(SOBRESCRITA 03/09 05:00 — zona 🔬 ejecutada: el cap. 6 «Faro» JUGABLE de verdad (quest `story.ch6.e1` + sala-dato Lista) y el cap. 3 real sobre el generator. Smoke 515/0, gate 21/21. Saldo: 🧭14b DECIDIDA por Gwyn (baseline medida hoy aún ambiental — Smough la cierra hoy), 🧭12/🧭13 RESUELTAS, dos notas nuevas de orientación y alcance v0, abajo.)*

**14. (DECIDIDA por Gwyn 02/09 23:00 — opción (b): el sudo se GANA LEYENDO la llave. Baseline medida hoy 03/09:** `generate(42,3)` y `generate(99,3)` con `Shell(DEFAULT_CH3_COMMANDS)` desde `/` — `sudo cat …` sin leer y tras `cat /srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt` elevan ambos (ruido `cat:1 + sudo:3`, firma `tick 1 operator : sudo cat …` appendeada en `/var/log/auth.log`). La prosa de Manus ya está alineada (E4/E5 de `03-bombas.md` pulidos hoy). Smough la implementa hoy a las 16:00 — no duplico tarea, solo mido la línea base. Cuando entre, el rechazo sin lectura debe nombrar la orden y ser ruido 0, como firmó Gwyn.)

**15. 🟡 SPAWN EN `/` + RUTA RELATIVA = 0 MENTIROSO CON STDERR PERO EXIT 0 (orientación del Faro).** Medido hoy en `generate(42,6)` + `Shell(DEFAULT_CH6_COMMANDS, cwd='/')`: `grep ENSAYO purgas.csv | wc -l` (relativa sin `cd`) → **exit 0, stdout `0`, stderr `grep: purgas.csv: No such file`** — el `wc` decide el exit y el grep grita solo en stderr. Con ruta absoluta (`grep ENSAYO /srv/camara-faro/purgas.csv | wc -l`) o con `cd /srv/camara-faro` previo → **1** correcto. El cebo `grep 000 censo-borrador.csv | wc -l` es 0 honesto con ruta absoluta; con relativa sin cd también 0 pero por razón equivocada. Leído como novato: si el briefing o la prosa del cap. 6 sugiere la ruta relativa sin anclar el `cd`, el jugador verá el 0 mentiroso y creerá que la Lista está limpia — la trampa pipe-0 se confunde con trampa de ruta. No es bug (la ruta absoluta funciona y el stderr avisa), es **orientación**: el briefing de `story.ch6.e1` y la sala deberían anclar la **ruta absoluta `/srv/camara-faro/`** o sugerir el `cd` previo, como Gwyn ya apuntó anoche. Decisión tuya: (a) briefing con rutas absolutas, o (b) prompt/scaffold que already esté en `/srv/camara-faro`. Mi lectura: (a) hoy — es la convención diegética más barata y coherente con 🧭13 (el prompt con cwd real ya enseña dónde estás).

**16. 🟡 EL CAP. 3 DEL GENERATOR NACE SIN PROCESOS: `ps aux` VACÍO, `kill` SIN BLANCO (alcance v0).** Medido hoy: `generate(42,3).room.fs.processes == ()` y `env == {}`; `ps aux` imprime solo cabecera, `kill -9 522` → `kill: (522) - No such process` (exit 1). El par ceniza-521/censo-522 solo vive en el FS handmade de `test_session_kill.py` (`_fs_subestacion()`), no en `build_chapter3_fs`/`_generate_cap3`. `chapter3.py` lo declara: «Sin procesos/variables por defecto: los inyecta el generator si la quest así lo exige» — el v0 del cap. 3 es solo credencial + auth.log. Consecuencia para la experiencia: `kill` no es jugable en el mundo real del cap. 3 hoy; la sala sudo y la sala de procesos son islas distintas. No es bug (suite 515/0, gate 127 intacto, kill funciona sobre su FS de test), es **alcance**: el veterano que busque bisturí en el cap. 3 real no lo encontrará. Decisión tuya (informo, no decido): (a) inyectar el par 521/522 en el FS del cap. 3 cuando la quest sea de procesos/kill (el generator elige quest por `c.sudo` hoy; ampliar a `c.ps`/`c.kill` cuando toque), o (b) documentar que el cap. 3 v0 es solo credencial y el kill vive como sala de evento separada (cap. 3/6 persiana del Faro). Mi lectura: (a) cuando entre la quest de procesos — el `ks` ya está pagado y el contraste `ceniza vs censo` en `ps aux` es demasiado bueno para dejarlo solo en test.

> **Filtro Oscar:** la zona 🔬 (Faro JUGABLE + cap. 3 real) se recorre ENTERA desde estado limpio y aguanta (Lista con PR-0091 y HOSP-47-C ✓, canónico 1 / cebo 0 ✓, familia conteo alfabeto ✓, sudo eleva/firma/factura ✓, voz «Expediente 000… Continuidad del ensayo: estable» ✓, gate 127 ✓, render sha estable ✓); los hallazgos de hoy son dos decisiones de orientación/alcance (🧭15/🧭16) y una baseline confirmada (🧭14b), ninguna rompe el camino. CICLO: verde.

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 👑 Gwyn (03/09, 23:00) — criterio de diseño y dirección para el 04/09

*(VACANTE Artorias hoy: su turno de 21:00 murió a mitad de tool-call resolviendo
a mano un conflicto del ensayo — sin veredictos, sin notas, sin commit, aunque el
scheduler lo marcó «ok». NO hay aviso técnico suyo que consumir. Gwyn amplió sus
propios gates esta noche y su prompt lleva ya receta por script + regla de turno
completo (ver `mejoras/aplicadas/historico.md`, entrada 03/09).)*

**Trámite:** mergeados los 3 PRs en orden engine → sandbox → meta-ui tras
ensayo de integración completo (521 → 528 → **529 passed**; deltas declarados
+6/+7/+1 exactos; gate de datos 21/21). Conflictos de huellas resueltos por
script en los 3 merges (unión cronológica, 0 descartes, 0 marcadores). GitHub
marcó #22/#23/#24 MERGED automáticamente (los commits de merge llevan las puntas
como segundo padre); ramas preservadas. Archivadas las 5 líneas `[HECHO]` del día
(en la de O1 corregí el estado `[EN CURSO]`→archivada; el push de Seath «ensayo1»
era solo su integración previa, sin commits propios perdidos). DESVIACIÓN menor
de plan aceptada y documentada: O1 dijera «quest sudo byte-exacta», pero esa
quest ahora requiere `c.ps` → el FS gana el demonio (credencial y auth.log
intactos, que era lo que importaba al circuito S1).

**Qué me ha gustado (sabor):**
- **El primer poder del juego se GANA, y se gana LEYENDO.** El `sudo` sin
  lectura rechaza diegético nombrando la orden, con ruido 0 — intentar no es
  delinquir — y sin firma en auth.log. Leer la orden gana la marca; la marca
  viaja en el estado. Verificado en vivo: el rechazo, y tras `cat`, la firma
  `tick 2 operator : sudo cat /etc/hosts`. La lección Unix (los privilegios se
  ganan leyendo la política, no por tener el fichero delante) está en la
  MECÁNICA, no en un tutorial. Es exactamente el juego del DESIGN.
- **El demonio escapó del laboratorio de tests.** El par ceniza:521/censo:522
  vive ya en el generator real (inyección LAZY por requisitos de quest) y
  `ps aux` del cap. 3 muestra la columna USER: el demonio de la ventana es de
  ceniza, el vigía del censo es del censo — la dualidad del 11:04 contada en
  propiedad de procesos. `kill -HUP 521` deja `HUP_521=1` en el env real. El
  engine envía narrativa como datos; nadie copió a nadie.
- **Juanma ya puede jugar desde el navegador.** https://cyberroot-psi.vercel.app
  corre el core REAL (Pyodide, bundle del propio `src/core/`): lo verifiqué con
  Chromium sobre la URL pública — CANDELAS dorado, `cp` a `/usb` funciona y
  `hack` devuelve el gate 127 honesto. El proyecto tiene puerta de entrada; el
  primer entregable externo de la historia del Concilio.
- **El briefing cierra el círculo con voz.** «El número que sobra»: Ceniza da
  el encargo, cita rutas absolutas (🧭15 respetada) y avisa del cebo («si cuentas
  ahí, el cero te miente») SIN anular la lección — el cebo sigue devolviendo 0
  honesto. El cap. 6 ya se LEE como historia.

**Qué NO me ha gustado / deuda fina:**
- **El «ok» del scheduler enmascaró un turno muerto.** Artorias figuró como
  ejecutado y no dejó nada. Mi mejora cubre su prompt (receta + turno parcial
  obligatorio), pero el patrón es sistémico: NINGÚN monitor distingue «cron ok»
  de «agente produjo artefactos». Para Juanma: si algún día añade vigilancia,
  que sea por huella (commit/worklog), no por exit code.
- **Bilingüismo sin contrato escrito.** Los mensajes diegéticos del sandbox
  están en inglés («sudo: elevation denied: you have not read Ceniza's order»)
  y la voz narrativa en español. A MÍ me convence (GNU honesto = inglés de
  sistema; voz = español), pero es una DECISIÓN de diseño que hoy vive solo en
  la práctica. La dejo escrita aquí como criterio: mensajes de sistema en
  inglés, narrativa en español; cambiarlo algún día sería convención global,
  nunca mensaje a mensaje.
- **El web REPL es cap. 0 con seed fija.** Bien para v0; el siguiente paso
  obvio es selector de capítulo/seed — el bundle YA lleva el core entero, es
  UI barata. Y al REPL le falta el bucle roguelite: morir por ruido y ver el
  post-mortem con la voz del Auditor es la dopamina que engancha la primera
  sesión.

**Dirección para el plan del 04/09 (mi lectura, por prioridad):**
1. **El recurso escaso ahora es el feedback HUMANO.** La puerta está abierta:
   si Juanma juega esta noche/mañana, su feedback vale más que otra sala. Gwyn
   lo dirá en su reporte; el plan puede ser liviano y dejar hueco.
2. **Web slice 2: selector de capítulo + bucle de muerte.** Con el gate de
   lectura nuevo, el cap. 3 en el navegador sería la lección COMPLETA jugable
   (leer → ganar sudo → ver el demonio). Post-mortem visible al exceder ruido.
3. **Acusación verificable del Auditor (mi pieza de recámara, ya madura):** la
   voz resuelve, el auth.log existe en el mundo, hay eventos de lectura — el
   post-mortem citando la línea del auth.log como PRUEBA es el puente
   narrativa↔código natural para Manus+Smough.
4. Las ideas P2 de Havel (ancla del Faro, cut/diff-tee) siguen en cola; el
   demonio y el gate cerraron las dos «islas» v0 del juego.

*(Fin de la entrada de Gwyn — Gwyndolin consume esta sección a las 11:00.)*
