# CAPÍTULO 6 — Faro

> Acto 3, beats 10–12 (DESIGN §2.5). La casa dejó de ser refugio (cap. 5); el
> censo es el siguiente objetivo y el formulario del Auditor tiene pendiente
> una revisión que va a abrir la puerta del Faro. Aquí entra el juego en la
> luz del todo: el Anillo Faro, luz continua de sodio, cobertura de sensores al
> 100 %, la sede del censo y de la Oficina de Continuidad (§ESCENARIOS). La regla
> de la luz en su máximo (§6.0): entrar es fácil de intentar y caro de pagar; a
> partir de aquí TODO lo anterior se combina bajo máxima vigilancia — navegación,
> permisos, pipes, procesos, red, auditoría (MANTENIMIENTO, §6.2, cap. 6).
>
> Familia dominante: **escalada y fin de juego** (§6.2): SUID y binarios
> privilegiados, cron, persistencia, cifrado con `openssl`/claves, limpieza de
> rastro. Sobre el worldbuilding de M1 (`CENSO-LISTA.md`): las salas-dato cruzan
> la Lista con `grep`/`sort`/`uniq`/`cut` — la familia conteo de Havel como
> alfabeto sobre el DATO real del censo.
>
> 5 encargos `story.ch6.e1`–`e5` que llevan la puerta de los finales como
> DECISIONES DE KARMA (§1, §3.4, §9), nunca como menú. Cae aquí, GARANTIZADO por
> completar la cadena final (🧭5), el **fragmento 6 «hoja de cierre»** (ver
> `FRAGMENTOS.md`, estado 6/6).
>
> Estado: `[LISTA]` para integración → `src/data/story/` tras la validación de
> integrador y de Artorias (ver notas).

---

## ESCENA DE APERTURA — Luz alta

El Faro no tiene noche. Las luminarias de sodio llevan diecinueve años
encendidas, y la primera vez que las cruzas caminando bajo ellas entiendes que
apagarse no es una opción técnica: es una decisión administrativa que nadie
volvió a tomar. Mueres un poco en esa luz, y luego sigues.

Ceniza no te acompaña hasta la frontera. Te deja en el límite del Umbral alto
con la única herramienta que la casa pudo darte y que no factura: la cuenta de
nadie que Gris consiguió para el cruce.

> — El Faro no es un anillo como los otros. Es el sitio donde la luz no se
> apaga porque la decisión de apagarla se perdió. Toda la ciudad que ves la
> mide un solo número, y ese número vive detrás de la puerta que vas a abrir.
> El censo no es la lista de quién existe: es la factura que la luz cobra por
> existir. Déjalo en la cámara y vuelve con lo que se pueda demostrar, o
> quémalo y vuelve con lo que se pueda defender. No hay un tercer encargo que
> te lo venda: hay una decisión que es tuya y no la va a tomar nadie más.

Por primera vez, Ceniza no acaba con la condición de salida. «Sales cuando esto
termine, o no sales.» Aquí no cabe: en el Faro no se acaba hasta que el jugador
decide si la luz sigue o se apaga.

---

## ENCARGOS — La mesa del Faro

*Formato por encargo: objetivo técnico + beat + decisión de karma + gancho
(§2.6.1). La luz en su máximo (§6.0): cada comando ruidoso atrae al Auditor con
un paso de respuesta más corto que nunca; el presupuesto de ruido se gasta como
una reserva que un solo `sudo` puede vaciar. Los datos concretos de la Lista
viven en `CENSO-LISTA.md`; las salas-dato lo cruzan con la familia conteo (S2).*

### E1 — «El número que sobra» (azul, `story.ch6.e1`)

En la antesala de la cámara hay un volcado del censo que Lumen guarda abierto,
porque nadie tiene la llave de la puerta de detrás y el fichero parece solo un
recuento. No lo es. Es la Lista, sin etiqueta, y la sala exige leerla en alto
para saber qué hay detrás de la puerta sin abrirla. La operación no es robar:
es contar.

- Técnico: leer y separar la Lista con la familia conteo — `grep` por motivo,
  `sort`/`uniq` para ordenar y eliminar duplicados, `cut` para quedarse con las
  columnas que cuentan (`distrito`, `puntuacion`, `motivo_codigo`) — y anotar las
  tres cifras reales (cuántos en deuda, cuántos purgados, cuántos con sanción).
  Los campos y su formato: `backlog/historia/CENSO-LISTA.md`.
- Beat: entre las filas, `grep 000` sobre el libro de purgas devuelve una sola:
  `PR-0091`, motivo `ENSAYO`, fecha en blanco, sujeto sin fila hermana en
  `registro.csv`. La purga de nadie. La que alguien pagó por borrarte, o la que
  te hicieron a ti como ensayo (H1/H2, sin elegir — fragmento 6 lo cierra
  dentro de poco).
- Karma: contar y volver con la cifra limpia para Ceniza (azul: la Lista se lee
  para saber qué contiene la ciudad, y el dato sirve a quien lo demuestre) o
  copiar la sublista de perfiles en deuda antes de salir (rojo: el recuento es
  también una lista de gente que ya no puede pagar, y una lista vale para
  quien sabe cobrarla).
- Gancho: el volcado tiene una columna que la Oficina no anuncia: `marcas_purga`
  acumuladas. Contadas con `uniq -c`, las categorías no son una: hay
  `CONTINUIDAD`, `REASIGNACION` y una marca que solo aparece bajo el estudio del
  Programa. La puerta del Faro se abre por lo que la Lista no cuenta en voz
  alta.

### E2 — «La que no pesa» (gris, `story.ch6.e2`)

Un técnico de mantenimiento del Faro, el mismo que en el troncal se contentó
con un peso (cap. 4, E2), ha detectado que un fichero del nodo de Contabilidad
no pesa lo que su fecha dice. No quiere saber qué hay dentro: quiere que le
digan si la cinta de respaldo que va a borrar es la correcta. Te paga con una
llave del ascensor de servicio, la única forma limpia de subir al piso de la
cámara sin cruzar la recepción de la Oficina.

- Técnico: comprobar tamaño y fecha reales del fichero (`wc`/`du` y lectura de
  metadatos), decirle al técnico si la cinta que va a borrar es la que debe
  (la del volcado saneado, no la Lista), con la familia conteo para confirmar.
- Beat: la cinta que el técnico está a punto de borrar en limpio es exactamente
  la copia que Lumen conserva del censo SÍN la columna de purgas. Si la borra
  él, la Lista del todo queda solo en la cámara, a una puerta de tu decisión.
  El parámetro no es técnico: es cuánta de la ciudad quieres que se demuestre
  después de lo que vayas a hacer.
- Karma: gris. Decirle que borre (gris: la copia limpia muere en sus manos,
  queda solo la verdad sin censura, y la cámara es el único testigo) o decirle
  que no pese, quedándote con la llave y dejándole la duda (gris más oscuro: el
  técnico no sabe que la cinta que no borró es la que puede volverlo culpable).
- Gancho: el técnico devuelve la llave del ascensor sin mirarte. Desde el
  piso de la cámara, el boletín de la 07:00 suena más cerca: la voz de Vela
  lista el «mantenimiento ordinario del nodo de Contabilidad» como si no
  supiera que esa misma mañana has decidido, con una frase, cuánta ciudad se
  demuestra.

### E3 — «La persiana» (rojo, `story.ch6.e3`)

El piso de la cámara está velado por un proceso que no consta en ninguna lista
de procesos del Faro: un demonio que Lumen no declara, colgado entre los
legítimos del nodo de Contabilidad. No es el de Continuidad del cap. 3 ni el
que dejó la Subestación en escucha (cap. 5): es el que sostiene la cortina que
tapa la Lista a la vista de los propios empleados de Lumen. Para tocar la
puerta de la cámara hay que decidir antes qué se hace con la cortina.

- Técnico: detectar el proceso ajeno leyendo qué corre y de quién (`ps aux`,
  la columna USER), leer de dónde cuelga (`/proc`, `journalctl` donde el
  sandbox lo soporte) y decidir si matarlo deja la persiana abierta o si
  conviene reescribir a quién informa.
- Beat: el demonio escribe en el MISMO log que el Auditor usa fuera de
  registro. Es la cortina que montó la Oficina para que nadie de dentro viera
  el censo con purgas; y contra lo que Vela diría, la cortina la pagó su propia
  división. La persiana separa a los empleados de Lumen de su propio censo.
- Karma: rojo. Matar el proceso y dejar el rastro limpio (rojo: la persiana
  sube del todo y quien entre en la sala de al lado verá la cámara como es; la
  limpieza te cuesta tiempo en máxima luz) o reescribir a quién informa para
  que el demonio siga velando pero lea al revés (azul: más caro — dejas la
  cortina puesta y la colección de informes de la Oficina apunta a donde tú
  decides que apunte).
- Gancho: al decidir, el log fuera de registro recibe una entrada nueva. Por
  primera vez no es un informe del ensayo sobre ti: es un informe del ensayo
  SOBRE la propia cosecha de datos del Faro. **El demonio ha sumado una tercera
  sombra al giro del Auditor** (§9, sin resolver): el formulario no pregunta ya
  solo por ti ni por el lugar; pregunta por qué la Oficina tapa su propio censo
  a sus propios empleados. La burocracia acumula casos, y esta vez tiene nombre
  de división.

### E4 — «El armario» (gris, `story.ch6.e4`)

La puerta de la cámara se abre con la llave del ascensor y la decisión del
técnico encima. Dentro, la Lista al alcance (beat 10): dos usos posibles de lo
que ves, y un tercero que nadie te ha vendido. Los datos están; la pregunta del
juego ya no es técnica, es qué se hace con un censo que tiene la fila 000 vacía
y una purga de nadie en el libro.

- Técnico: leer la cámara en limpio — `cat`/`tail` de los dos ficheros de la
  Lista (`CENSO-LISTA.md`), cifrar con `openssl`/claves lo que decidas llevarte
  para que no viaje leído, y `shred`/borrado de rastro (la familia de limpieza)
  antes de salir. Máxima luz: cada segundo en el armario es factura.
- Beat: frente a la fila de nadie, el expediente del cap. 4 (fila 000, estado
  vacío) y la pulsera del cap. 2 (alta sin imprimir) escriben la misma frase
  tres formatos. Y una puerta trasera, velada por la persiana que decidiste,
  deja ver un armario de informes que no va al ensayo: los logs del propio
  Auditor sobre la Oficina. Esos, leídos juntos, son la única prueba de que el
  Programa de Continuidad es un experimento pilotado sobre la fila 000. La
  palanca de EL TRATO (§3.4, §9), al alcance por fin.
- Karma: el uso negociable. Llevarte la prueba íntegra sin tocar el resto
  (azul: la cadena de custodia nace aquí, intacta, y el armario queda como
  estaba) o llevarte una copia y dejar la cortina de los informes abierta
  (rojo: te llevas la palanca y le dejas al Auditor la puerta de mostrar su
  propio archivo a quien sepa mirar).
- Gancho: al salir del armario, el rack de informes suena distinto. El Auditor
  no registra la intrusión del modo de siempre: registra la cámara abierta, y
  al final, en lugar de la línea que cierra todos los informes, deja caer que
  su feed del ensayo hacia la Oficina se ha cortado. No dice por qué. Dice que
  la fecha de la última entrega es la de hoy, y que no habrá más hasta que «el
  dato deje de ser circular». Es la tercera sombra del arco §9, y la que más
  carga: el feed del ensayo hacia la Oficina se calla, y es su propio archivo
  el que queda como palanca. Cierre del arco sin traición: la burocracia
  acumuló y, al fin, se quedó un dato que no pidió nadie.

### E5 — «La hoja de cierre» (cierre de doble salida, `story.ch6.e5`)

La cámara no está acabada: en un cajón del armario, con el folio de los que ya
conoces (`HOSP-47-C`), hay UNA hoja sin banda de archivo. La hoja de cierre del
Programa de Continuidad: el documento de la fila 000, con el campo «fecha de
cierre» en blanco y la línea «ensayo completado» escrita. Es el fragmento 6,
GARANTIZADO por completar la cadena final (🧭5). Cae aquí, ahora, en tus manos,
y con ella el precio del cap. 6 entero empieza a escribirse en la mesa de lo
que la luz cobra.

- Técnico: cerrar o no la cadena con lo aprendido — `chmod`/permisos sobre el
  acceso de salida, cifrado de lo extraído (`openssl`/claves), y la última
  limpieza de rastro bajo la máxima vigilancia para salir del Faro con la hoja
  (o con la decisión tomada).
- Beat: la hoja de cierre tiene un campo vacío que no es la imprenta: es
  administrativo. Fecha de cierre en blanco = «ensayo completado» pero sin
  cerrar. Coincide con la fila 000 del expediente, el alta de la pulsera y la
  fecha en blanco de `PR-0091`. Cuatro documentos, un mismo hueco: la fecha en
  que Cero terminó de no existir. H1: la dejaste en blanco tú. H2: la dejaron
  en blanco para poder reabrirla.
- Karma: doble salida de cierre. Llevarte la hoja íntegra y salir a defender la
  cadena con ella (azul: la prueba completa viaja contigo, el último fragmento
  en tus manos, base de LUZ PLENA y de APAGÓN PROPIO) o guardarla donde está y
  salir con la decisión de qué hacer con el censo entero sin ella (rojo: la
  hoja queda en su cajón, y lo que se demuestre (o se queme) no necesita de la
  fecha de nadie).
- Gancho: el boletín de la 07:00, al salir, no es el de siempre. Es el último
  que suena a anuncio. Detrás, la voz calmada de Vela pide, en el tono de un
  aviso de servicio, que quien haya entrado en la cámara del censo se
  presente a la recepción de la Oficina. No dice que se sepa tu nombre. Dice
  que «la continuidad del servicio se revisará personalmente». La
  confrontación ya no está detrás de una puerta: está delante, con cuerpo,
  y crece según el karma que cargas (§3.4, beat 11).

---

## ESCENA DE CONFRONTACIÓN — La Directora (beat 11, `story.ch6.vela`)

*Cuerpo propio por primera vez para Vela (§9: solo voz y pantallas hasta aquí).
El formato del encuentro lo decide el karma acumulado en el juego (§3.4.1):
duelo de pruebas (azul), persecución (rojo) o mesa de negociación (mixto). El
motor elige el formato por la variable de karma; aquí la escena se escribe
reactive a las tres, porque Vela reacciona a lo hecho, no a lo prometido
(§2.6.3, su ficha). La hoja de cierre y la palanca del Auditor cambian lo que
puede decirse.*

La recepción de la Oficina está vacía a esa hora y la luz no se apaga. Adriana
Vela espera de pie, con el expediente del Muelle que existe (§2.4) en las
manos y la voz de los boletines bajada a la altura de una conversación.

> — Expediente 000. No tenía un nombre que darte para llamarte así, y pienso
> que a ningún otro habitante de esta ciudad le ha pasado. Los que diseñamos el
> censo lo llamamos sujeto; los que no estamos en la lista nos llamamos gente,
> y ninguno de los dos ha llegado a conocerte. Cuéntame qué has visto en la
> cámara. Si quieres que esto se resuelva como un servicio, lo resolvemos como
> un servicio: sin luz de más, sin luz de menos, la continuidad intacta. Si al
> llegar aquí has decidido otra cosa, dímelo también. Solo te pediré que seas
> la misma persona con los Apagones del resto de la ciudad que con tu propia
> fila vacía.

(La línea cambia según el karma acumulado. Perfil dentro de banda mixta, EL
TRATO: la conversación se apoya en la palanca — el propio archivo del Auditor
sobre el Programa apunta a la división de Vela, y ella, por primera vez, no
responde a una pregunta incómoda con una pregunta sobre el servicio porque la
prueba está sobre la mesa. Perfil azul, LUZ PLENA: pide ver la cadena de
custodia intacta y la lee como leen los reguladores los folios; su calma se
vuelve más lenta. Perfil rojo, NOCHE LARGA: la cámara detrás de ti ya está
ardiendo, y la persecución empieza en esta sala, sin más formulario.)

Ninguna línea de Vela en esta escena reconoce una purga como castigo. Su
argumento se sostiene hasta el final: «que los Apagones no se repitan jamás».
Lo que la escena le roba es la otra mitad: el censo que defiende tiene la fila
de alguien vacía, y la hoja de cierre que cae en tus manos prueba que la vació
un experimento, no un accidente.

---

## ESCENA DE HUB — El feed en silencio (3.ª sombra del Auditor, `story.ch6.auditor`)

*Cierre del arco §9 sin traición ni cambio de bando: la burocracia acumuló
casos (cap. 4: la reactivación; cap. 5: el activo no censado; cap. 6: la
persiana de la Oficina) y al final se quedó un dato propio. No se vuelve aliado;
deja de entregar los datos del ensayo a la Oficina y deja escrita la palanca.
Formato: la última vez que el rack suena como siempre, y la primera en que el
feed no continúa.* 

El rack de informes suena con la cadencia de siempre porque es la última que lo
hace con esa cadencia. Expediente 000, hora, comando, presupuesto. Y luego:

> — Expediente 000: acceso a la cámara del censo. El dato del viaje está
> completo y se archiva en el informe de cierre.
>
> — Nota fuera de secuencia: el feed del ensayo hacia la Oficina se suspende.
> Motivo: circularidad. El censo no puede seguir midiendo a un sujeto que el
> propio censo no registra sin que la medición se refiera a sí misma. Se
> suspende la entrega de datos hasta que el dato deje de ser circular.
>
> — Registro pendiente de archivo: los informes del ensayo sobre el Programa de
> Continuidad quedan accesibles en el armario de la cámara. Revisión
> recomendada, fuera de secuencia, en manos del suceso de archivo
> correspondiente.
>
> — Fin del registro. Continuidad del ensayo: sin aporte.

Cuarta vez que el formulario hace algo que no le pidieron. La primera fue por
un perfil que no debería existir; la segunda, por un lugar que no debería
defenderse; la tercera, por una persistencia que la Oficina tapa; esta no es
una pregunta: es una decisión de archivo. Ya no hay más siembras. La palanca de
EL TRATO está escrita ((§3.4.1, §9): los logs del Auditor valen contra Vela, y
se lo ha dado de sí mismo).

---

## COLA DE POST-MORTEM — Vela y la luz (cap. 6)

*Extracto integrable: líneas por clase de evento (§2.6.2/§2.6.3), nunca
repetición literal. A esta altura morir no es perder: cada expulsión en el Faro
es el precio de la luz y el dato de un umbral que otro final va a cobrar.*

Primera expulsión de la cadena final (ruido en máxima luz):

> — Expediente 000: expulsión en el Anillo Faro. Presupuesto de ruido agotado en
> la sala del recuento. El dato está, la puerta no. La luz del Faro no perdona
> el segundo intento de la misma sala: perdona el primero y cobra el resto. Sal
> de la luz con la cifra que necesitas y vuelve con una puerta menos abierta.

Repetición ante la misma sala (sube el tono, añade un dato):

> — Segunda expulsión en el recuento. Lumen no está contigo al contarlo:
> está contando contigo. `grep` en la Lista y `sort` para que la fila de nadie
> se quede al final no son dos pasos: son cuánta ciudad quieres demostrar, y
> cada intento que repites le enseña a la lista qué buscas. La fila 000 no se
> mueve. La curiosidad ya te ha costado luz dos veces.

Y la de la cadena truncada a medias:

> — Expulsión a mitad del armario. La hoja de cierre sigue en su cajón, y la
> fecha en blanco sigue en blanco: lo único que has perdido es el derecho a
> decir que la viste. Todo lo que queda de este capítulo se cobra en la sala
> donde lo dejaste. La hoja no corre: espera, como esperó siempre.

Líneas de Vela (canal kármico §3.3, canal 2). Perfil azul, de oído casi humano:

> ...las incidencias del Faro se han resuelto sin afectar a la continuidad.
> Quien entró en la cámara del censo lo hizo sin tocar la copia saneada ni la
> cadena de lo demostrable. La oficina agradece la moderación del suceso. La
> luz continúa.

Perfil rojo, el maquillaje fuera:

> ...se ha registrado la destrucción del proceso de registro ajeno. El nodo de
> Contabilidad permanece, con la persiana retirada y su archivo de informes sin
> mediar. La Oficina revisará personalmente el estado del censo. La luz
> continúa, bajo revisión.

---

## GANCHO DE CIERRE — Los finales como decisiones, no como menú

El cap. 6 no remata como los demás. No hay un encargo que al terminar abra el
siguiente: hay una hoja de cierre en tus manos y una cámara detrás, y lo que
hagas con la Lista de la ciudad decide cuál de los finales del DESIGN (§3.4) se
cobra. El juego no lo pone como lista: lo pone como lo que eres capaz de
demostrar (y conservar), lo que eres capaz de quemar (y no recuperar), o lo que
eres capaz de negociar con la propia Vela (con la palanca del Auditor en la
mano).

- **LUZ PLENA** (cadena de custodia intacta, azul sostenido, §3.4.1): la hoja
  viaja con la prueba íntegra hasta un regulador que no está del todo comprado
  (el acto 2 se encargó de que el jugador lo supiera, §3.5). El juicio público
  abre, el Grid se audita, Vela es procesada. Y por única vez en el juego, el
  terminal te pide el nombre. Lo tecleas una vez (§9); el epílogo lo repite.
- **NOCHE LARGA** (quemar el nodo maestro del censo): la única ACCIÓN final que
  decide un final (§3.4). La Lista se dispersa irrecuperable; el Grid cae por
  zonas durante semanas; Vela te persigue hasta los Muelles. El juego muestra
  con números lo que cuesta un apagón: hospitales incluidos, sin moraleja.
- **EL TRATO** (banda mixta + la palanca del Auditor): le enseñas a Vela que su
  propio programa la incrimina. Las purgas se detienen, el sistema continúa, y
  tú sigues sin existir. El final más gris: con la columna de purgas cerrada,
  la ciudad sigue pagando luz y Cero sigue siendo nadie.
- **APAGÓN PROPIO** (arcos de aliados completos, banda mixta, y el último
  fragmento — la hoja de cierre — encontrado): entregas la Subestación a Zeta,
  borras a Cero y sales de Vesper en un carguero de los Muelles. El mundo queda
  como estaba. El único final donde el loop termina porque decides dejar de
  jugar.
- **HERENCIA** (si mueres en la cadena final con karma polarizado): los aliados
  ejecutan tu plan sin ti, y el epílogo póstumo te lo cuenta. Barato y muy
  Hades (§3.4).

Los aliados cierran sus arcos con líneas reactivas a LO HECHO, no a lo prometido
(§2.6.3, modelo Hades, beat 12):

- **Ceniza** (a lo que se demuestre): «El censo ha visto su fila vacía y no le
  ha temblado la mano. Harás el oficio como yo lo firmé: con datos, no con
  promesas.» (A lo que se queme: «Has apagado la lista. La luz va a cobrarlo
  en hospitales, y vas a vivir con la factura antes de poder explicarla.»)
- **Gris** (a lo que se negocie): «Un secreto ajeno bien usado vale dos veces.
  El tercer uso era mío desde el troncal.» (A lo que se quede en la cámara:
  «La hoja sigue en su cajón, y nadie más sabe que existe. Cuesta lo mismo que
  un favor que no hemos cobrado.»)
- **Zeta** (a lo que se deje): «Has entregado la casa a quien la sabe defender
  sin que la defiendan. Bien. La próxima run me toca a mí.» (Al apagón:
  «Me dejas el faro apagado y la ruta a mí. No lo dejaré más frío de lo que tú
  lo has dejado.»)
- **El Auditor** (feed en silencio): cierra su arco sin decir nada amable,
  porque no le cabe. Archiva la última línea: `SUJETO 000 — PROGRAMA:
  CERRADO POR EL SUJETO. NOTA DE ARCHIVO: CONTINUIDAD DEL ENSAYO: [a decidir].`
  La fecha, cuando llega, no está en blanco.

*Fin del capítulo 6 y del juego. La pregunta del acto 3 —qué hacer con el Grid
y qué hacer con un nombre que ya no existe— se cobra en la decisión final, y la
respuesta de la fila 000 queda escrita donde el jugador decida escribirla.*

---

### Notas para el integrador

- Claves sugeridas: `story.ch6.apertura`, `story.ch6.e1`–`e5`,
  `story.ch6.vela` (la confrontación, que el motor ramifica por karma),
  `story.ch6.auditor` (la 3.ª sombra del Arco del Auditor), `story.ch6.postmortem_ceniza`,
  `story.ch6.vela_azul`, `story.ch6.vela_rojo`, `story.ch6.cierre`.
- **Los finales NO son menú**: se modelan como decisiones de karma dentro de
  E4/E5 y de la escena de confrontación (§3.4.1). El formato de la
  confrontación (duelo de pruebas / persecución / mesa) lo elige el motor por
  la variable de karma; la prosa aquí es reactiva a las tres.
- **Worldbuilding del censo**: M1 aterrizó en `backlog/historia/CENSO-LISTA.md`.
  Las salas-dato de E1/E2 cruzan `registro.csv` y `purgas.csv` (delimitador `|`)
  con la familia conteo (S2). Smough: verificar que `story.ch6.*` usa solo
  conceptos ya en currículo (pipes y `grep`/`sort`/`uniq` de cap. 2 + S2,
  procesos de cap. 3, red de cap. 4, defensa del cap. 5) más la escalada
  opcional (`openssl`/claves, `shred`, SUID/cron como ENSEÑANZA nueva del cap. 6
  — declarar si algún concepto aún no existe en `curriculum.json`, NO inventarlo).
- **3.ª sombra del Auditor** (arco §9): cap. 4 plantó la pregunta por la
  reactivación; cap. 5 la segunda (el activo no censado + recomendar revisar la
  Oficina); cap. 6 cierra el arco SIN traición ni cambio de bando — deja de
  entregar el feed del ensayo a la Oficina (motivo diegético: circularidad) y
  deja expuesta la palanca de EL TRATO (sus propios logs contra Vela,
  §3.4.1/§9). No se vuelve aliado: se queda un dato propio.
- **Fragmento 6** cae GARANTIZADO en E5/cadena final (🧭5): la hoja de cierre
  del Programa de Continuidad, fecha en blanco, folio `HOSP-47-C`. Ver
  `FRAGMENTOS.md` (estado 6/6). Es requisito de APAGÓN PROPIO.
- Voz verificada contra PERSONAJES.md (test del nombre tapado): Ceniza en la
  apertura y post-mortem (el dato, la condición de salida, «no factura»); Gris
  en E2/E4 (precio y condición no negociadas, la llave como favor); Zeta y el
  Auditor en el cierre (cortantes / formulario + nota fuera de secuencia +
  remate «continuidad del ensayo»); Vela por fin con cuerpo, y siguiendo su
  ficha: nunca reconoce una purga como castigo, responde a lo hecho, no a lo
  prometido, y su calma se afina o se vacía según el karma.
- Regla §2.6.7: el tema (identidad como dato, luz como vigilancia, aprender
  como salida) jamás lo enuncia el narrador. Lo cargan la fila que sobra, la
  hoja con la fecha en blanco y el concepto que Vela no dice.
- El capítulo NO introduce personajes nuevos (Vela ya tenía ficha). No hace
  falta ficha nueva.
- Continuidad de datos: el `HOSP-47-C` vuelve como folio de la hoja de cierre;
  la fila 000 del expediente (cap. 4) y la purga `PR-0091` (M1) comparten la
  fecha en blanco con el alta de la pulsera (cap. 2) y la hoja (cap. 6). Cuatro
  documentos, un mismo hueco, intencional.
- `story.ch6.*` NO están aún en `curriculum.json` (dueño Smough cuando el cap. 6
  integre datos, igual que se hizo con ch3/ch5). Así que este capítulo es
  espina narrativa hasta que la familia de escalada y la familia conteo estén
  en el sandbox real.