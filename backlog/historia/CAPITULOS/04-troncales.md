# CAPÍTULO 4 — Troncales

> Acto 2, beats 7–8 (DESIGN §2.5). Tras la ventana abierta del cap. 3, el
> troncal que cruza al Faro por fin se deja caminar. Aquí el juego enseña a
> moverse entre máquinas que no se tocan (`ssh`, claves, `scp`, túneles — §6.2)
> y a leer quién se conecta de verdad: a quién le abres la sesión es la misma
> pregunta que desde la firma. La regla de la luz en su máximo (§6.0): en el
> Faro entrar es fácil de intentar y caro de pagar. Y el giro del Auditor
> (beat 8) se planta sin resolverse (§9): se queda preguntando cosas que el
> formulario no prevé.
>
> 5 encargos sobre la frontera Umbral/Faro (§6.3); aquí solo el material
> narrativo: escenas, diálogos, karma, ganchos. Fragmento 4 (la cuenta)
> disponible como botín (ver `FRAGMENTOS.md`) — puede caer en E4/E5.
> Estado: `[LISTA]` para integración → `src/data/story/`.

---

## ESCENA DE APERTURA — Cruce

El troncal no se ve. Es una línea que los operadores miden por latencia y por
silencio: veinte milisegundos hasta el Faro cuando no hay nada que lo mire, y
una hora interminable si algo en la frontera decide preguntar qué llevas.
Ceniza te lo monta como quien tiende un cable por un edificio vacío.

> — Un nodo troncal es una puerta con cola. Todo el tráfico del anillo pasa
> por ahí, y la puerta anota quién entra, cuándo y con qué llave. No hay
> forma de cruzar en silencio una puerta que escribe. Lo que se puede hacer
> es cruzar con la llave correcta y que la anotación no sea tuya. Vas a
> necesitar acceso remoto limpio, y eso se construye: se obtiene una
> credencial, se guarda protegida, se usa lo
> mínimo para lo que vaya a servir, y se cierra al salir. Una sesión abierta
> no es una puerta que dejas: es un testigo que te acompaña.

Primera vez que te conectas a una máquina que no está en la misma habitación
que tu cuerpo. El prompt aparece con un nombre de host que no has tecleado
nunca, y por un segundo el reflejo de quien eres le cuesta al terminal lo
mismo que a ti: ningún usuario, ninguna casa. Escribes, y la máquina del otro
lado no pregunta quién eres. Pregunta qué llave traes.

---

## ENCARGOS — La mesa de la frontera

*Formato por encargo: objetivo técnico + beat + decisión de karma + gancho
post-mortem (§2.6.1). Los textos entran como claves; el generador pone la piel
procedural encima (hosts, llaves, IPs). Capítulo con la luz en su pico: cada
salida sube por distrito hacia la nuca del Faro y el presupuesto de ruido se
siente al cruzar cada umbral.*

### E1 — «La llave prestada» (azul, `story.ch4.e1`)

Una sesión abierta en un salto del Umbral alto, a nombre de un técnico que
lleva dos turnos sin entrar. Nadie la cerró al dejar el puesto; nadie corrió
esa noche. Para llegar al troncal hace falta subirse a esa sesión, pero antes
hay que saber de quién es y no entrar adormilado por la puerta que otro dejó.

- Técnico: `ssh` al host de salto con la credencial que el capítulo te va
  ganando (del `sudo` del cap. 3 pasas a llaves), y `who`/lectura de sesión
  para saber quién está al otro lado antes de usarla.
- Beat: la sesión abandonada de ese técnico es la misma que aparece en la
  lista del cap. 2 como «ventana abierta». No la dejó él abierta: la abrió
  alguien con su perfil, y el técnico nunca se enteró porque nadie le contó
  que su turno se alargaba sin él.
- Karma: entrar con la llave del técnico y registrar el uso (azul: la usas
  sabiendo de quién es, la anotas, la cierras al salir) o reutilizarla sin
  dejar constancia (rojo: la puerta del técnico queda como si él la hubiera
  abierto otra vez).
- Gancho: al subir al troncal, el `last` de la frontera no tiene tu sesión.
  Tiene la de él. Algo en la puerta ya te atribuye una puerta que no es tuya,
  como la primera vez.

### E2 — «El peso que cabe» (gris, `story.ch4.e2`)

El troncal acumula un volcado de conexiones de la última semana que Lumen
archiva y no mira, porque el fichero «no pesa lo que debería». Un operador de
mantenimiento del Faro, que solo quiere que le den la razón, te pide que
saques ese volcado y le digas cuánto pesa de verdad. No quiere que lo leas.

- Técnico: `scp` para traerte el fichero del troncal a tu terreno (o leerlo
  remoto sin copiarlo entero), y `wc`/`du` para decir el peso exacto en la
  misma unidad que el presupuesto.
- Beat: el volcado tiene un peso que no cuadra con su fecha de creación: se
  registró como de la semana pasada pero su marca de contenido dice que se
  escribió hoy a las 11:04. La última hora del cap. 2, reescrita en el Faro.
- Karma: gris. Decirle al operador que el peso es correcto y devolver el
  volcado sin leerlo (gris: le das la razón, avanzas la relación) o quedarte
  una copia para quien sea que te la pida después, sin que él se entere
  (gris más oscuro: un peso que no cuadra vale más que una respuesta).
- Gancho: el operador se contenta. Lo que no vio es que la fecha del volcado
  no era su problema: era la única prueba de que el troncal se reescribe solo
  los días de la firma.

### E3 — «El túnel» (rojo, `story.ch4.e3`)

Detrás del salto hay un servicio del Faro que no se anuncia en ninguna lista:
se llega a él por un túnel cifrado que alguien tendió hace años y nunca cerró.
Gris ha oído hablar de lo que hay al final y lo quiere antes de que la Oficina
se entere de que el túnel existe. Te apunta el puerto y te dice el «por qué»,
que es lo único que nunca da gratis.

- Técnico: abrir un túnel cifrado (encuadre `ssh -L` o el equivalente del
  sandbox) para alcanzar el servicio que el salto no expone, y apuntar bien
  lo que ves al otro lado.
- Beat: al final del túnel hay una terminal de Continuidad que lleva años
  abierta y silenciosa. No pide contraseña: le basta con que la llave del
  salto siga viva. El túnel es la primera pisada del «giro»: algo en el Faro
  está esperando una llave concreta y no pregunta quién la trae.
- Karma: rojo. Llegar al final y contar a Gris qué hay (rojo: la palabra vale,
  y el túnel sigue abierto para quien la compre) o llegar, mirar, y cerrar el
  túnel por dentro (azul: más caro, dejas el servicio como si nadie hubiera
  entrado, y la llave de acceso muere contigo).
- Gancho: al cerrar (o no) el túnel, la terminal de Continuidad envía una
  línea que no pidió nadie: `EXPEDIENTE 000 — SIN ARCHIVO ADJUNTO — CONFIRME
  RECEPCIÓN`. La primera pieza del informe que el Auditor te diría solo si le
  preguntaras algo que no está en el formulario.

### E4 — «La cuenta que no existe» (rojo, `story.ch4.e4`)

El Faro factura por una sesión corporativa que no figura en el censo de
personal. Gris quiere el número de cuenta de esa nómina antes de que Lumen
mire dos veces el troncal que le dio sombra al Alto. Lo pide como quien pide
una dirección: sin mirar qué hay dentro.

- Técnico: seguir la sesión fantasma hasta su origen (leer quién la inició,
  con qué llave, de qué host), `scp` o lectura de los datos de la cuenta, y
  cruzar los campos con lo que el troncal sabe de Continuidad cuando haga
  falta.
- Beat: la cuenta está a nombre de una sociedad instrumental llamada como la
  propia ciudad. Lleva sin moverse desde que se truncó la que la pagaba. El
  fragmento 4 puede caer aquí, como pieza de la misma carpeta.
- Karma: rojo. Llevarse el número de la cuenta a Gris (rojo: la nómina de un
  fantasma a nombre de una empresa fachada vale para quien sabe cobrarla) o
  borrar el rastro de que la sesión existió y dejar la cuenta quieta (azul:
  cuesta más y deja al Fantasma una nómina que nadie reclama, que es casi lo
  mismo).
- Gancho: la cuenta, una vez vista, deja de ser un número. Es el hilo que
  une la pulsera del hospital y el troncal: el mismo nombre en dos archivos
  que nadie ha abierto juntos salvo quien los busca.

### E5 — «El expediente» (cierre de capítulo, `story.ch4.e5` — beat 7)

Llegar al final del troncal, al nodo donde la frontera se convierte en Faro,
y encontrar la cámara de Continuidad. No hay que robar nada: hay que confirmar
qué expide, y a nombre de qué. Ceniza lo pide como quien pide una llave para
mirar las dos veces seguidas.

- Técnico: lo aprendido en el capítulo en una sola secuencia: `ssh` con la
  llave ganada, cruzar la frontera con el túnel disponible, leer el expediente
  (`cat`/`less` del registro de la cámara) y decidir qué se queda.
- Beat: el registro del Programa de Continuidad. Sujetos 001 a 012, todos
  cerrados: «ensayo fallido», «sujeto inestable», «cerrado por fecha». En la
  fila 000, el campo de estado está vacío. No dice «en curso» y no dice
  «cerrado»: la fecha de cierre está en blanco, como la fecha de alta de la
  pulsera. Dos lecturas posibles y el juego no elige (§2.5, beat 7): el único
  que sobrevivió por azar, o el único que sigue corriendo porque lo dejan.
- Karma: leer el expediente y no tocar nada (azul: la prueba queda intacta
  para quien la necesite después) o marcar la fila 000 como «cerrado» antes de
  salir (rojo: le cierras un misterio a Lumen y de paso le cierras la puerta a
  quien lo buscaba desde dentro).
- Cierre de capítulo: el fragmento 4 puede caer aquí (ver `FRAGMENTOS.md`,
  fragmento 4 — la cuenta).

---

## ESCENA DE HUB — El giro del Auditor (beat 8 §2.5) — `story.ch4.auditor`

*El borde del arco del Auditor, sin resolverlo. Empieza a preguntar cosas que
no constan en el formulario. No lo hemos escrito como traición ni como
aliado: le falta un dato suyo y la burocracia acumula casos.*
*Formato: primera vez que el Auditor, tras una expulsión en la frontera, no
cierra con su frase-neutra-de-costumbre.*

El rack de informes suena con la cadencia de siempre. Expediente 000, hora,
comando, presupuesto. El Auditor repasa la sesión del Faro con la frialdad de
quien archiva, y al final, en lugar de la frase que cierra todos los informes,
se queda una línea de más. No consta en el formulario.

> — Expediente 000: inicio de sesión en la frontera del Faro con la llave de
> un operador ausente. Continuidad del ensayo: estable.
>
> — Pregunta adicional fuera de registro: el operador cuyo perfil se utilizó
> fue dado de baja hace dos turnos. La Oficina no reactiva perfiles dados de
> baja. No consta registro de reactivación para la fecha de tu acceso.
>
> — Fin de la pregunta adicional. Continuidad del ensayo: estable.

Ceniza, que escucha detrás de ti, no lo comenta en el momento. Es la primera
vez que el formulario hace una pregunta. Nadie había visto al Auditor dudar
de sus propios datos, y dudar en voz alta necesita un dato que él no tiene.

---

## COLA DE POST-MORTEM — Ceniza y el Auditor (cap. 4)

*Extracto integrable: líneas por clase de evento (§2.6.2/§2.6.3), nunca
repetición literal. Capítulo donde las sesiones se abren y se cierran, y la
llave importa más que el comando.*

Primera expulsión del capítulo (sesión sin llave propia):

> — Entraste al salto con una sesión que no era tuya y sin saber de quién
> era. El troncal no pregunta quién eres: pregunta qué llave traes, y la
> anota. Si entras con la puerta de otro, la anotación no es tuya, es suya, y
> la factura te la cobran a ti dos veces: una en ruido y otra en testigos.
> `ssh` no es un atajo: es declarar de quién entras.

Repetición ante el mismo obstáculo (sube el tono, añade un dato):

> — Segunda expulsión con el mismo problema. No es el comando: es de quién
> vas. El troncal conserva el historial de quien entró, y ese historial ya
> tiene tu huella por el técnico ausente. Lee lo que hay sobre la sesión
> antes de abrirla. Una llave prestada te saca una vez; te delata la
> segunda, cuando el dueño ya sabe que no fue él.

Y la del túnel abierto sin control:

> — Abriste un túnel cifrado y lo dejaste respirando al salir. Un túnel no
> es una puerta que se cierra sola: es un pasillo que sigue siendo tuyo
> hasta que lo cierras. Si te expulsan con la sesión viva, el pasillo queda
> con tu nombre en la entrada y el faro del otro lado encendido. Ciérralo al
> salir, o vive con la cuenta de haber dejado la puerta del Faro entregada.

Líneas del Auditor (canal kármico §3.3, canal 2). Perfil azul:

> Expediente 000: acceso a la frontera del Faro con credencial obtenida y
> conservación del registro. Clasificación: supervisión no autorizada.
> Continuidad del ensayo: estable. Pregunta adicional pendiente de
> respuesta.

Perfil rojo:

> Expediente 000: acceso a la frontera del Faro con apropiación de sesión y
> destrucción selectiva de registro. Clasificación: intrusión en la
> continuidad del servicio. Continuidad del ensayo: estable, bajo
> observación de expediente.

---

## GANCHO DE CIERRE — La puerta que pregunta

Cuando la cámara de Continuidad queda leída (o marcada, según lo que
hicieras), el troncal no se cierra del todo. Ceniza te lo dice sin floritura,
y el espacio entre sus dos frases es la grieta que ya no te esconden:

> — Has visto el programa, y has visto que el Auditor lo sabe todo menos una
> cosa: que la fila 000 está vacía y que algún sistema cree que sigue en
> curso. No te he contado esta parte antes porque no sabía si existía para
> usarte o para delatarme. Ahora los dos hemos visto la cámara.
>
> — Hay un nombre en dos archivos: la sociedad de la cuenta y el expediente
> del troncal. Nadie ha leído los dos juntos salvo nosotros, y el Auditor
> está preguntando por algo que no le consta. Eso no es un error de
> Continuidad: es la primera vez que el formulario tiene una pregunta propia.
> No la pierdas.

El boletín de las 07:00, la voz calmada de siempre:

> ...los sistemas de la frontera Norte han completado su rutina de
> supervisión. No se han detectado incidencias. El censo se mantiene íntegro
> y la continuidad del servicio, garantizada. En el troncal, el archivo de
> conexiones se ha reescrito esta mañana y archiva su propio historial, como
> es habitual. Gracias por su confianza.

En los días siguientes, la fila 000 no se cierra, el túnel muere o no según
lo que decidieras, y el Auditor se queda con una pregunta adicional sin
respuesta. Ya no es solo un daemon que registra: es un formulario que ha
aprendido a dudar de sus propios datos, y no le gusta.

*Fin del capítulo 4. Sigue en el capítulo 5: la presión sube y la Subestación
deja de ser refugio — el asalto llega al Hub.*

---

### Notas para el integrador

- Claves sugeridas: `story.ch4.apertura`, `story.ch4.e1`–`story.ch4.e5`,
  `story.ch4.auditor` (el giro, beat 8), `story.ch4.postmortem_ceniza`,
  `story.ch4.auditor_azul`, `story.ch4.auditor_rojo`, `story.ch4.troncal`.
- Voz verificada contra PERSONAJES.md (Ceniza, Gris, Zeta no aparece en este
  capítulo, Auditor, Vela). Test del nombre tapado: Ceniza en la apertura y
  el gancho (condición de salida, dato antes que ánimo, no promete salida
  segura); Gris en E2/E3 (precio dos veces, el «por qué» como favor que
  nunca da gratis); el Auditor en su giro (frase formulario + pregunta fuera
  de registro + remata «continuidad del ensayo: estable» — es SU sello).
- Karma de cap. 4: E1 azul, E2 gris, E3 rojo, E4 rojo, E5 de cierre con ambas
  salidas. Coherente con el descenso del Acto 2 (§3.3): un perfil que ya
  subió al Alto recibe en la frontera trabajos más sucios, y la frontera
  cobra en testigos lo que el Alto cobraba en alertas.
- ⚠️ Bloques de terminal: el capítulo asume `ssh`, `scp` y un mecanismo de
  túnel (`ssh -L` como referencia conceptual). Esto es CONTRATO PEDAGÓGICO,
  no salida reproducible: hay que verificar contra la implementación real del
  sandbox cuando la familia Red entre en currículo (igual que los pipes del
  cap. 2 se verificaron con `test_session_ch2.py`). La nota para Smough:
  antes de `story.ch4.*` en `curriculum.json`, el sandbox necesita modelar
  credenciales/llaves (`ssh`), copia remota (`scp`) y un túnel — o bien el
  capítulo se ajusta a lo que el sandbox soporte cuando el cap. 4 se
  integre. Hasta entonces, los encargos E1-E5 son espina narrativa.
- El giro del Auditor (beat 8 → `story.ch4.auditor`) se PLANTA aquí, no se
  resuelve. Su arco (§9) es que «la burocracia desarrolla conciencia por
  acumulación de casos»: este capítulo es el primer caso. No adelantar su
  resolución. Regla §2.6.7: el tema (identidad como dato) jamás se enuncia
  por el narrador; los archivos y las preguntas del formulario lo cargan.
- Continuidad de datos: el 47 vuelve como sucursal (Banco del Muelle
  SUCURSAL 47) y como NHC (HOSP-47-C); la cuenta `44-0191-7` de la División
  Estructuras (filial 44) cruza con la pulsera
  (fragmento 2, HOSP-47-C) sin forzar. La fila 000 del Programa se conecta
  con el cap. 6 (hoja de cierre, fragmento 6). La hora 11:04 del cap. 2
  vuelve como marca de reescritura del troncal (E2) — recurrencia intencional,
  no slop.
- El capítulo no introduce personajes nuevos (Zeta no aparece; queda para el
  cap. 5). No hace falta ficha nueva.
- `story.ch4.*` aún NO están en `curriculum.json` (dueño Smough cuando toque
  el cap. 4). El 4 es la familia «Red real» (§6.2): `ssh`, `scp`, túneles,
  lectura de sesiones.