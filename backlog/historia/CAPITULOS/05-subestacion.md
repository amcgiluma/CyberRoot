# CAPÍTULO 5 — Subestación

> Acto 2, beat 9 (DESIGN §2.5). Tras el troncal del cap. 4, la presión de la
> Oficina deja de ser tráfico y se vuelve cuerpo. La Subestación, que era el
> único lugar de la ciudad sin factura, es localizada por Vela: no por un
> guion, sino por la suma de las alertas reales que el jugador acumuló
> llegando hasta aquí (§2.5, beat 9). Es la ÚNICA incursión invertida del
> juego (§6.1, cap. 5): no entras; defiendes. La regla de la luz se da la
> vuelta — en los Muelles la luz escasa era refugio, y cuando Lumen entra en
> ella, entra con hombres, no con sensores (ESCENARIOS: Muelles).
>
> Familia técnica: **auditoría y defensa** (§6.2, cap. 5) — leer logs ajenos,
> cerrar permisos, hardening mínimo, detectar movimientos. Aquí las lentes
> azules se vuelven nivel obligatorio (§3.1): un perfil rojo juega
> EXACTAMENTE lo mismo, porque defender es defender. Cada encargo =
> técnico + beat + karma + gancho (§2.6.1); 5 encargos `story.ch5.e1`–`e5`:
> 2 azules, 1 gris, 1 rojo, 1 de cierre.
>
> **Fragmento 5 disponible como botín en este capítulo** (expediente médico
> del Muelle — ver `FRAGMENTOS.md`): cae en E4/E5. El nº que cuelga al lado
> del de Vela encuentra aquí su momento.
>
> Estado: `[LISTA]` para integración → `src/data/story/`.

---

## ESCENA DE APERTURA — La luz que viene a por ti

La Subestación no huele a soldado hasta el tercer día. Antes, huele a lo que
fue siempre: aceite vacío, dos transformadores de 20 kV que no enfriaron a
nadie en diecinueve años, la luz verde de «CORTE MANUAL» desde el mes 18 de
los Apagones. Gris mantiene la tira de LED con las 08:00 justas de
encendido, y detrás de ella todo sigue tan muerto como para que Lumen lo
siguiera contando como desafectado.

Luego, un martes, el repeater de la grúa nueve deja de parpadear. No caído:
atento, en silencio. Ceniza lo lee en la mesa de encargos sin levantarse.

> — Un repeater no se apaga solo y no se silencia solo. Alguien lo ha puesto
> en escucha. La Oficina no usa sensores aquí porque aquí no llega su luz; usa
> manos, y las manos empiezan por dejar de hacer ruido.
>
> (Hace una pausa que no es de duda, es de coste.)
>
> — Se acabó la cobertura gratis. Y se acabó contar con que el censo no nos
> supiera. No ha sido un azar: han sumado nuestras alertas, y la suma da
> aquí. Todo lo que hiciste desde que entraste por esa puerta tiene precio, y
> hoy empieza a cobrarse. Sales cuando esto termine, o no sales.

La primera vez en toda la casa que te recoge un hombre, no un análisis. La
luz de la Subestación se vuelve un detalle de cuánto ruido estás dispuesto a
hacer dentro de tu propia casa.

---

## ENCARGOS — Defender el refugio

*Formato por encargo: objetivo técnico + beat + decisión de karma + gancho
(§2.6.1). Capítulo invertido: no subes de anillo, te quedas donde vives y la
dificultad es el volumen. Aquí el ruido no lo mira un sensor que factura: lo
escucha gente que va de puerta en puerta. Todo lo ruidoso atraes; todo lo
silencioso es distancia. La familia es auditoría/defensa (§6.2) — leer logs,
cerrar permisos, detectar movimiento — y un perfil rojo lo juega igual, porque
defender es defender (§3.1).*

### E1 — «La puerta que dejaste» (azul, `story.ch5.e1`)

El primer invitado no vino por la puerta principal: vino por la que dejaste
tú. En el archivo de sesiones de la Subestación hay una conexión registrada
a tu nombre, desde un host del Alto, en la hora muerta del dia anterior a la
escucha del repeater. No es una intrusión ajena: es la sesión que usaste en
algún encargo y no cerraste del todo. Lumen la está leyendo para saber
cuánta casa hay detrás de tu perfil.

- Técnico: leer las sesiones propias del host (`last`, `who`, lectura de
  `auth.log` simulado) para identificar qué puerta sigue abierta a tu nombre,
  y cerrarla: permiso de fichero, `kill` de la sesión colgada o `chmod` sobre
  el recurso que la mantiene.
- Beat: la sesión que se lee es la del primer trabajo, la de la firma. La
  puerta que usaron para vestirte un crimen no es la única que dejaste
  tocada: la costumbre de no cerrar lo que abres es el mismo hoyo de siempre.
- Karma: cerrarla entera y registrar el cierre (azul: dejas constancia de
  qué se cerró y por qué, la casa mide su propio tamaño) o cerrar solo el
  tramo que Lumen ya ha leído (rojo: suficiente para hoy, barato, y dejas una
  salida tuya escrita para cuando la necesites).
- Gancho: al cerrarla, el `auth.log` del host anota qué o quién la abrió la
  última vez: no consta tu nombre. Consta una reactivación de perfil que la
  Oficina no hizo. La puerta de la firma la reabrieron dentro; lo que Lumen
  lee ahora es el eco.

### E2 — «Los permisos de la casa» (gris, `story.ch5.e2`)

La casa se sostiene sobre cuentas prestadas que Gris cosió con favores, y
ahora que hay manos en los Muelles cada cuenta es una llave. Gris, que nunca
da nada gratis y menos seguridad, te pone sobre la mesa la lista de lo que
la casa comparte con fuera: tres recursos con modo demasiado abierto, dos
que la propia casa ni sabía que existían. Te pide que hagas lo de siempre
con lo de siempre: que nadie de fuera los toque, y que él siga pudiendo
entrar cuando quiera.

- Técnico: auditar permisos de la casa (`ls -l`, `chmod`/`chown` sobre los
  tres recursos señalados) y dejarlo todo con la mínima apertura que la
  Subestación necesita para sobrevivir, sin cortar la vida de dentro.
- Beat: uno de los recursos es un fichero de anotaciones de Ceniza sobre el
  primer encargo, de antes de conocerte. Anotado a mano vuelto digital: «no
  avisarle. Necesitamos que llegue. Fecha anterior a la firma.» La grieta
  del beat 6 escrita en la propia casa (coherente con `PERSONAJES.md` —
  Ceniza justifica, no consuela).
- Karma: gris. Cerrar los permisos y dejar la nota donde estaba (gris: la
  casa se blinda y tú sigues sin leer lo que no te corresponde) o copiar la
  anotación antes de cerrar (gris más oscuro: te la llevas, y Gris lo presume
  porque «un secreto ajeno es un favor que se cobra»).
- Gancho: al cerrar, la Subestación despide dos servicios que Gris pagaba en
  silencio desde el Umbral. El repeater de la grúa nueve llega a leerlos como
  señal de que la red del Muelle se está cerrando sobre ellos, y Zeta, que
  lleva horas en su silla, dice: «seis años para cortar el cable de uno
  mismo».

### E3 — «La visita» (rojo, `story.ch5.e3`)

La Oficina no ha entrado aún, pero su gente ha dejado algo dentro: un
proceso vivo en el rack de informes, escondido entre los que la casa corre
de verdad. No es el demonio de continuidad del capítulo 3; es otro: obra de
alguien que pasó cuando el repeater calló. Si Lumen está midiendo la casa
desde dentro, ese proceso es su termómetro.

- Técnico: detectar el proceso ajeno leyendo qué corre y de quién (`ps`,
  `ps aux`, la columna USER que delata §4.6/S1 PR #14) entre los legítimos de
  la casa, y decidir qué hacer con él.
- Beat: el proceso cuelga de un no-tuvo-tiempo de terminar algo: escribe en
  un log de la Oficina que la Subestación creía borrado, el de los informes
  del Auditor. Quien lo dejó no solo mide al jugador: lee a su cazador. El
  daemon que te archiva ha empezado a su vez a ser observado.
- Karma: rojo. Matarlo y dejarlo limpio (rojo: lo quemas, borras el log que
  escribió, y la Oficina pierde el termómetro sin saber qué pasó) o dejarlo
  vivo pero apuntando a otra parte (azul: más caro — reescribes qué lee para
  que la Oficina vea lo que tú decides que vea).
- Gancho: al intervenir, una línea nueva cae en el archivo del Auditor: un
  informe que no está firmado por la hora de la expulsión. La pregunta
  adicional del capítulo 4 (la reactivación sin registro) tiene ahora una
  sombra en el otro lado: el formulario ya no solo pregunta por ti. Pregunta
  por quién preguntaba por él.

### E4 — «El que se queda» (cierre de doble salida, `story.ch5.e4`)

El asalto llega a la puerta de la Subestación por la única vía que Lumen
tiene para entrar en los Muelles: la carretera del dique, que en diecinueve
años solo vieron las grúas paradas. Ceniza te da el último rodeo: lo que la
casa tiene dentro que no puede caer en manos de la Oficina, y lo que la casa
está dispuesta a perder. Defiendes, no robas; pero decides qué entra en la
sombra antes de que entren ellos.

- Técnico: cerrar el perímetro con lo aprendido de defensa — `chmod` sobre
  los accesos, `kill`/`chown` donde la casa se queda a medias, leer los logs
  de entrada (`cat`/`tail` del acceso) para saber por dónde vienen — en un
  solo recorrido apretado por el ruido.
- Beat: en el archivo de fragmentos, los cajones 27 a 31 siguen vacíos (la
  numeración que nadie ha abierto, §ESCENARIOS: Subestación). Uno de ellos,
  el 29, tiene recién una mancha de polvo movida y una sola hoja: el
  expediente. Cae aquí como botín (fragmento 5 — ver `FRAGMENTOS.md`). El
  historial del Muelle que cuelga al lado del de Vela encontrado en el lugar
  que no debería tener nada.
- Karma: doble salida de cierre. Dejar el expediente donde estaba y exponerlo
  a lo que pase en el dique (rojo: lo que la Oficina encuentre en la casa es
  problema de quien lo guardó) o llevarlo contigo lejos del fuego (azul: una
  prueba del tamaño que la casa ya no puede sostener, y que empequeñece al
  resto de lo que defiendes).
- Gancho: el cierre del capítulo. Se sobrevive al asalto, pero el coste queda
  escrito en la casa: un transformador que esta vez sí se enfría, la tira de
  LED a 04:40, el repeater de la grúa nueve muerto del todo. Zeta cuenta lo
  suyo en voz baja y Gris dice la primera cifra que ha dicho sin la segunda.
  Y el Auditor, al registrar la defensa, cierra con una línea que no pide
  nadie: `SUJETO 000 — DEFENSA DE ACTIVO NO REGISTRADO. PROGRAMA: EN CURSO.`

---

## ESCENA DE HUB — El formulario y su sombra — `story.ch5.auditor`

*La única expulsión (o cierre) del capítulo donde el Auditor no registra una
intrusión ajena, sino la defensa de un activo que no figura en el censo. El
giro del cap. 4 (la pregunta adicional) recibe aquí su segunda sombra: ya no
duda de sus datos sobre ti, duda del lugar donde ocurre la defensa.*
*Formato: informe del daemon tras el episodio del dique.*

El rack de informes suena con la cadencia de siempre. Expediente 000, hora,
comando, presupuesto. Pero esta vez el objetivo no es un nodo del Grid: es
la línea del dique, y el activo que se defendió no está en ningún formulario.
El Auditor lo registra con la precisión quirúrgica de quien archiva algo que
no debería archivar, y la línea final no cierra igual.

> — Expediente 000: actividad defensiva en sector no censado del Muelle.
> Continuidad del ensayo: estable.
>
> — Nota de archivo fuera de registro: el recurso defendido no consta en el
> censo de activos de la ciudad. No consta dirección, no consta medidor, no
> consta expediente. Un activo que el censo no registra no debería producir
> defensa registrada.
>
> — Dos anomalías de archivo coincidentes en el mismo ciclo: un perfil dado
> de baja reactivado sin registro (anterior) y un activo no censado con
> actividad defensiva (actual). Recomendación fuera de registro: revisar si
> la Oficina mantiene expedientes de activos que nadie dio de alta.
>
> — Fin de la nota. Continuidad del ensayo: estable.

Segunda vez que el formulario hace una pregunta. La primera fue por un perfil
que no debería existir; esta es por un lugar que no debería defenderse. Nadie
le ha pedido nunca al Auditor que revise los expedientes de su propia
Oficina. Empieza a pedírselo él.

---

## COLA DE POST-MORTEM — Ceniza y defensa (cap. 5)

*Extracto integrable: líneas por clase de evento (§2.6.2/§2.6.3), nunca
repetición literal. Aquí el que muere no es intruso: es defensor, y el
post-mortem de Ceniza habla de lo que se perdió en casa, no de lo que se
encontró fuera.*

Primera expulsión del capítulo (defensa ruidosa / se pidió al dique sin
medir):

> — Te fuiste al dique a defender una puerta que llevas meses sin cerrar en
> casa. Una casa que se abre por dentro no se defiende hacia fuera: se blinda
> hacia dentro. `chmod` sobre lo que vives es más barato que un cuerpo en la
> carretera. Sales cuando esto termine, o no sales. Hoy no has salido.

Repetición ante el mismo obstáculo (sube el tono, añade un dato):

> — Segunda vez con la puerta de atrás. Lumen no está leyendo tus comandos:
> está leyendo el tamaño de tu casa por lo que dejas fuera. Cada permiso
> abierto que no cierras es un hombre que no teme entrar. La entrada del
> dique no era tuya: era de los que vinieron a mirar. Ahora queda la factura
> y la costumbre.

Y la de la cuenta prestada que se quedó abierta:

> — Dejaste una cuenta de Gris con la puerta abierta al salir al dique. Una
> llave prestada no es tuya: es un favor que te delata. Gris te cobrará dos
> veces la misma cifra `kill`; la Oficina, con una visita más precisa. Cierra
> lo que la casa comparte antes de defender lo que la casa no suelta.

Líneas del Auditor (canal kármico §3.3, canal 2). Perfil azul:

> Expediente 000: defensa de activo no censado con contención de acceso y
> conservación del perímetro. Clasificación: supervisión no autorizada, sin
> expulsión técnica. Continuidad del ensayo: estable. Nota adicional
> pendiente de revisión en la Oficina.

Perfil rojo:

> Expediente 000: defensa de activo no censado con destrucción de proceso de
> registro ajeno. Clasificación: interferencia en la continuidad del
> servicio. Continuidad del ensayo: estable, bajo observación de
> expediente. Nota adicional pendiente de revisión en la Oficina.

---

## GANCHO DE CIERRE — El coste escrito en la casa

Cuando el dique queda vacío y la tira de LED vuelve a las 08:00, la
Subestación existe todavía. No igual: existe con la cuenta pagada. Un
transformador de 20 kV entrega por fin algo de frío; el repeater de la grúa
nueve ya no está; el archivo de fragmentos tiene el cajón 29 vacío de su
mancha de polvo, con o sin la hoja según lo que decidieras. Zeta, desde su
rincón, no dice lo amable que no sabe decir; dice:

> — Seis años para cortar el cable de uno mismo. Y al final el que corta el
> de los demás cobra por el tuyo.

Gris dice la primera cifra que ha dicho sin la segunda. Ceniza, por una vez,
no corrige a nadie; corrige el informe del asalto y lo deja sobre la mesa,
abierto: la casa sabe ya cuánto cuesta vivir fuera de la factura. Y en el
boletín de las 07:00, la voz calmada de siempre, la de Vela:

> ...los Muelles permanecen bajo supervisión ordinaria. Se ha registrado
> actividad no atribuida en el sector del dique; el censo no identifica
> titular de esa actividad, que se considera tráfico residual de las grúas
> fuera de servicio. La continuidad del servicio permanece garantizada.
> Gracias por su confianza.

La primera vez que Vela miente sobre lo que sabe, y no por culpa del
jugador: lo sabe porque la Subestación se defendió, y el censo que presenta
no le tiene registrada ni la casa. La puerta del capítulo 6 ya no está detrás
del troncal: censo, confrontación y un formulario que ha aprendido a
preguntar por su propia Oficina.

*Fin del capítulo 5. Sigue el capítulo 6: la casa ya no es refugio, el censo
es el siguiente objetivo, y el formulario del Auditor tiene pendiente una
revisión que va a abrir la puerta del Faro.*

---

### Notas para el integrador

- Claves sugeridas: `story.ch5.apertura`, `story.ch5.e1`–`story.ch5.e4`,
  `story.ch5.auditor` (la segunda sombra del giro, beat 9), `story.ch5.postmortem_ceniza`,
  `story.ch5.auditor_azul`, `story.ch5.auditor_rojo`, `story.ch5.dique`.
- ⚠️ Capítulo INVERTIDO: no hay salida por distrito ni subida de anillo. El
  presupuesto de ruido se entiende como VOLUMEN (todo lo ruidoso atrae gente
  en los Muelles, donde Lumen entra con hombres — ESCENARIOS). El contrato de
  generador para el cap. 5 NO usa la plantilla de muestreo normal de sala;
  §6.4.5 lo marca como única excepción estructural, guionizada como campaña,
  no dejada al muestreo. Smough: verificar que el flujo de encargo permita
  esta variante antes de integrar `story.ch5.*`.
- Voz verificada contra `PERSONAJES.md` (test del nombre tapado): Ceniza en
  apertura y post-mortem (cadencia de informe, dato antes que ánimo, la
  condición de salida «sales cuando esto termine, o no sales», no promete
  salida segura); Gris en E2 (precio dos veces — aunque en el cierre, por una
  vez, dice UNA cifra, y eso es intencional: el asalto le quita el tic);
  Zeta en E2/E4/al cierre (cortante, comparativa, «seis años para cortar el
  cable de uno mismo», nada amable); el Auditor en su escena de Hub (frase
  formulario + nota fuera de registro + remata «continuidad del ensayo:
  estable» — su sello; la recomendación a revisar la Oficina es la segunda
  pregunta del arco §9, sin resolver).
- Continuidad con el cap. 4: la pregunta adicional por la reactivación del
  perfil (cap. 4, beat 8) recibe su eco — E1 la responde sin resolverla (el
  `auth.log` no consta tu nombre), y el Hub del Auditor la suma a la segunda
  anomalía. Arc §9 en curso: la burocracia acumula casos; aún NO resuelto.
- Beat 9 cumplido: Vela localiza la Subestación COMO CONSECUENCIA de las
  alertas acumuladas del jugador (lo dice Ceniza en la apertura: «han sumado
  nuestras alertas»), no por guion (DESIGN §2.5, beat 9). La grieta de
  Ceniza (beat 6) aparece como anotación escrita en la casa (E2) sin
  resolver.
- Fragmento 5 cae aquí (E4, cajón 29): el expediente médico del Muelle que
  cuelga al lado del de Vela. Coherencia con fragmentos 2 y 4 (NHC
  HOSP-47-C, VESPER DE GESTIÓN S.L.) y con la cronología de Vela intacta.
- Regla §2.6.7: el tema (identidad como dato, vivir fuera de la factura,
  luz como vigilancia) jamás lo enuncia el narrador; lo cargan el archivo
  de fragmentos vacío, el acto del censor, la cifra de Gris y la costumbre
  de no cerrar.
- `story.ch5.*` aún NO están en `curriculum.json` (dueño Smough cuando el
  cap. 5 integre datos). El capítulo reutiliza conceptos ya en currículo
  (`ps`, `chmod`/permisos, logs/grep de cap. 2, `kill` de cap. 3) como
  MANTENIMIENTO bajo nueva presión — no exige conceptos nuevos obligatorios
  salvo la operativa de defensa (leer log ajeno + cerrar permiso), que nace
  de la combinación, no de un comando inédito.