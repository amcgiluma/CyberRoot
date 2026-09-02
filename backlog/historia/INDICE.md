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
- DECISIÓN Gwyn (27/08, 🧭5): el ÚLTIMO fragmento de la cadena está
  GARANTIZADO al completar la cadena final del cap. 6 (ver DESIGN §6.1).
  Materializarlo en `FRAGMENTOS.md` cuando se escriba la cadena.