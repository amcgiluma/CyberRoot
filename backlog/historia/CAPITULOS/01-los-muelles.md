# CAPÍTULO 1 — Los Muelles

> Acto 1, beats 3–4 (DESIGN §2.5). El pacto con los Apagados y la primera
> elección de trabajo. 6–7 encargos sobre el mismo distrito (§6.3); aquí
> solo el material narrativo: escenas, diálogos reactivos, la elección
> azul/rojo y los ganchos post-mortem. Enseñanza técnica del capítulo:
> permisos (`chmod`, `chown`) como «quién puede tocar esto», `man` por
> atasco. Estado: `[LISTA]` para integración → `src/data/story/`.

---

## ESCENA DE APERTURA — Los que no suman

La Subestación de día es otra: se oye el puerto trabajar. Grúas paradas que
nadie desmonta, contenedores con el número repintado encima del número
viejo, y entre medias, gente que camina pegada a las paredes, los que no
suman. Lumen los llama saldos negativos; ellos se llaman Los Apagados, por
los meses en que la ciudad se quedó a oscuras y ellos siguieron ahí cuando
volver la luz significaba volver a deber.

Ceniza reparte el trabajo como quien reparte turnos de guardia. La mesa de
encargos, la tira de LED, los papeles con cinta. Tu nombre no está en
ninguno: te llama «tú» y a veces ni eso.

> — Cobertura, dijo anoche. Significa que cada salida que hagas pasa por
> nodos que mantenemos nosotros. Si Lumen rastrea una de tus sesiones, el
> rastro muere en nuestros nodos, no en tu máquina. A cambio, trabajas.
> Los Muelles tienen facturas pendientes que no son de dinero.

No te pregunta si aceptas. Te enseña el primer nodo: una red vecinal del
Muelle Oeste donde el admin anterior se fue sin dejar permisos sanos.

> — Empieza mirando. `ls -l` no es un capricho: la primera columna es quién
> puede tocar qué. Hasta que no sepas quién puede tocar qué, no toques.

---

## LA REGLA DEL DISTRITO — Gris y la factura de la luz (🧭3)

*Función: el jugador SABE, antes del capítulo 2, que más luz = más vigilancia
(§6.0.2). Diegética: Gris habla de tarifas, nunca enuncia la mecánica. Se
inserta en el primer regreso al Hub con un encargo completo.*

Aquí la vigilancia de Lumen no llega salvo en redadas. Es lo que hace de
los Muelles un refugio y un peligro a la vez: cuando Lumen entra, entra con
hombres, no con sensores. En las noches de redada los bares apagan el
generador y sirven a la luz de velas por ley no escrita: menos luz, menos
lista.

A Gris se lo dices con la mirada, y él responde como responde a todo: con
una tarifa.

> — Lo mío son los Muelles; aquí conozco a todos los que te pueden vender
> algo dos veces. Del Umbral no te quiero hablar de barrio, te quiero
> hablar de factura. El bajo apaga a las 23:20 y por la noche es casi
> amable. El alto mantiene dos avenidas encendidas toda la noche, y esas
> avenidas son de Lumen: veintidós minutos por patrulla, contados a mano
> por una amiga que ya no da las gracias. Cuanta más luz paga un barrio,
> más caro sale mirarlo. Y vas a subir. Cuando subas, te acordarás de
> esta conversación. Mejor: me la acordarás a mí, que es más barato.

Preguntas por el Faro. Gris se encoge de hombros como quien cita la letra
pequeña:

> — El Faro no tiene tarifa. Tiene dueño.

Lo dice mientras te vende la linterna. Cobra dos veces, como siempre. Y
remata, porque cada precio lo suelta dos veces y nunca igual:

> — En zona brillante, la primera mirada te la regala el barrio. La
> segunda ya la factura Lumen.

---

## ENCARGOS — La mesa (muestra integrable)

*Formato por encargo: objetivo técnico + beat + decisión kármica + gancho
post-mortem (§2.6.1). Los textos entran como claves; el generador pone la
piel procedural encima (nombres, rutas, horas).*

### E1 — «El turno de la señora Carmen» (azul, clave `story.ch1.e1`)

El nodo vecinal del Muelle Oeste guarda los partes de asistencia de la
escuela pública 3. Alguien con permisos de administración los consulta por
las noches. La escuela quiere saber quién; nadie quiere un escándalo.

- Técnico: leer `ls -l`, identificar la cuenta con permisos que no toca,
  seguir su rastro en los logs del propio nodo.
- Beat: el parte de asistencia decide si la escuela puede reclamar la
  beca de comedor. Quien mira los partes no mira alumnos: mira a las
  familias con deudas.
- Karma: la cuenta ajena se descubre. La rotas y registras el uso (azul)
  o la conservas para tu colección (rojo).
- Gancho post-mortem (si expulsan): el Auditor anota la cuenta y deja de
  anotarte a ti. Por esta noche.

### E2 — «Cobro por agua» (azul, `story.ch1.e2`)

Un técnico de Lumen con conciencia filtra las tablas de lectura de
contadores del distrito: hay bloques que pagan agua que nunca llega. Quiere
la prueba fuera antes del viernes. No da su nombre; el buzón de salida es
la lavandería Ciclón, en la Calle del Estío.

- Técnico: encontrar el directorio de lecturas entre ruido de backups,
  verificar fechas con `find`, extraer solo los ficheros que valen.
- Beat: el bloque 14 lleva ocho meses pagando un servicio que la empresa
  contabiliza como prestado.
- Karma: los logs que te delatan a ti (y a él) se corrigen con rastro
  mínimo (azul) o se queman enteros (rojo, y el técnico pierde su prueba).
- Gancho: Gris pregunta por el técnico. No por nombre: por buzón.

### E3 — «El censo baja al puerto» (gris, `story.ch1.e3`)

La Oficina instala contadores de presencia en las puertas de los almacenes.
Zeta los ha estado reventando por deporte; a uno le puso una pegatina con
su propio número de operadora. Los Apagados quieren saber qué formato
emiten antes de decidir si se pueden falsificar.

- Técnico: `cat` de configuraciones, entender qué campo es el identificador,
  `man` cuando el formato no se deduzca solo.
- Beat: el contador no cuenta gente: cruza con el censo. No sabe cuántos
  entran; sabe cuántos que DEBEN estar, están.
- Karma: neutral. Aquí el karma lo pone cómo salgas, no qué haces.
- Gancho: si te expulsan, Zeta aparece en la Subestación con los tiempos:
  «cuarenta segundos más tarde que yo. Cero, hay que trabajar eso».

### E4 — «La lista del embargo» (rojo, `story.ch1.e4`)

La inmobiliaria del capítulo 0, la misma del encargo rojo que no cogiste o
sí. Su lista de viviendas embargadas circula ahora entre dos familias del
Muelle que quieren saber si sale su puerta. Cobran por quitarla. El que
te contrata no dice para qué la quiere él.

- Técnico: reconocimiento rápido de la red de la inmobiliaria, copia de la
  lista, salir antes del turno de auditoría.
- Beat: dos familias pagan por borrarse de un papel. Tú decides si el
  papel se borra para ellas o solo para la venta.
- Karma: borras sus dos filas y cualquier copia entera que encuentres
  (azul), o cumples el encargo y conservas tu copia (rojo; Gris la compra
  antes de que llegues a casa).
- Gancho: el Auditor registra «modificación de datos de terceros» sin
  valorar. La palabra «terceros» la eligió él.

### E5 — «El nodo de las francesas» (clave de cierre del capítulo,
`story.ch1.e5`)

Control estable del nodo vecinal del puerto: el repeater que cuelga de la
grúa nº 9, la del cable de izado soldado a la pista, y da red a media docena
de casas fuera del censo. Para mantenerlo necesitas exactamente lo que el
capítulo ha enseñado: entrar, mirar quién tiene permisos, ajustarlos, dejarlo
vivo y marcharte sin ruido.

- Técnico: la secuencia completa. `chmod` y `chown` sobre lo justo; el
  resto, dejarlo igual que estaba.
- Beat: el nodo lo montó un operador que ya no está. En su `README`
  interno dejó: «si lo lees, sigue tú». No firmó.
- Karma: cerrar el nodo con permisos correctos (azul: más difícil de
  robar, más fácil de auditar) o con una puerta para vosotros (rojo: los
  Apagados entran gratis; Lumen lo detectará antes o después).
- Cierre de capítulo: el primer fragmento puede caer aquí (ver
  `FRAGMENTOS.md`, fragmento 1 — la foto).

---

## ESCENA DE HUB — Zeta pone números (`story.ch1.zeta1`)

La primera vez que vuelves con un encargo completo y ella con uno mejor:

> — Doce minutos yo. ¿Cuántos tú? No, no me lo digas. Lo leo en el
> espejo, el espejo no miente a la gente que sabe leerlo. Bien. La
> próxima me toca a mí.

Y la primera vez que te ve morir dos veces ante el mismo nodo:

> — Otra vez el mismo firewall. Cero. Te está esperando, y encima ya no
> se sorprende. No hay nada peor para una máquina que se acostumbra a ti.
> Cambia el turno. O cambia de herramienta.

---

## COLA DE POST-MORTEM — Ceniza (cap. 1)

*Extracto integrable: líneas por clase de evento (§2.6.2/§2.6.3), no
texto genérico. Primera muerte del capítulo, repetición, y el `man` que
nadie consultó.*

Primera expulsión del capítulo, en voz de quien firma informes:

> — El log dice que entraste dos veces al mismo directorio con nombres
> distintos. Eso es no mirar. `ls -l` primero, `cd` después. La próxima
> sala te va a costar lo mismo que esta si no cambias eso.

Repetición ante el mismo obstáculo (sube el tono, añade un dato, nunca
repite):

> — Segunda vez. El permiso que te faltaba no ha cambiado; el que lo
> puso tampoco. Lo que ha cambiado es el tiempo de respuesta de Lumen:
> cada reintento tuyo lo miden. Hay un manual en la propia máquina,
> `man chmod`. Léelo ahí, no en mi mesa.

Y la que dejó escrito el turno en que el jugador resuelve sin mirar los
permisos y falla tarde:

> — Has perdido once minutos en un error de dos. Los permisos estaban en
> la primera columna desde el primer comando. Los archivos no esconden
> nada; los dueños, sí. Aprende a leer dueños.

---

## GANCHO DE CIERRE — Lo que cuelga del techo

El capítulo cierra la noche en que el nodo de las francesas queda
estable. Ceniza revisa los permisos que dejaste, nodo a nodo, y no dice
nada hasta el último:

> — Está limpio. Demasiado. Nadie que lleve dos semanas en esto deja un
> nodo tan redondo. Yo firmé código así cuando llevaba años. Algún día me
> contarás de dónde te viene.

Es la primera pregunta que te hace sobre ti y no la sabes responder. Ella
tampoco. El post-mortem de esa noche incluye una línea que no estaba en
el formulario:

> Expediente 000: rendimiento por encima de la banda esperada para un
> operador sin historial. Origen del adiestramiento: desconocido. Se
> recomienda mantener observación.

Mientras, en la mesa de encargos, hay un papel nuevo con la caligrafía de
siempre. No trae dirección ni hora. Trae una pregunta:

```
¿Recuerdas tu primer trabajo? Nosotros tampoco.
La ventana de las 11:04 se abrió dos veces esa mañana.
```

*Fin del capítulo 1. Sigue en el capítulo 2 «Facturas»: cruzar el Umbral
bajo persiguiendo quién abrió la segunda.*
