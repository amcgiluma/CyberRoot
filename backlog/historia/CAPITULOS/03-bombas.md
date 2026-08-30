# CAPÍTULO 3 — Bombas

> Acto 2, beats 5–6 (DESIGN §2.5). El rastro del proceso vivo del cap. 2
> lleva al Umbral alto: la subestación secundaria en servicio y las
> máquinas que nadie apaga. Aquí el juego enseña a leer procesos y
> matarlos con criterio (`ps`, `kill`, señales, `systemctl`, variables de
> entorno, empaquetado — §6.2), y a usar el primer `sudo` serio con
> credenciales ganadas (§6.1). 7–8 encargos sobre el distrito (§6.3); aquí
> solo el material narrativo: escenas, diálogos, karma, ganchos y la
> **grieta de Ceniza plantada** (beat 6, §2.5) — confesión que señala,
> no que resuelve. Fragmento 3 (el contrato) disponible como botín
> (ver `FRAGMENTOS.md`). Estado: `[LISTA]` para integración →
> `src/data/story/`.

---

## ESCENA DE APERTURA — La subestación despierta

El Umbral alto no se parece a los Muelles. Detrás del cordón de sensores,
las dos avenidas que Gris nombró se encienden de golpe a las 23:20 y no
se apagan hasta las 06:00; entre los dos haces de luz hay media milla de
fachadas con el aliento dentro. La patrulla pasa cada veintidós minutos.
Contados a mano por una amiga de Gris que ya no da las gracias.

La subestación secundaria es la copia en miniatura de la tuya, salvo un
detalle: esta tiene corriente. Mantenimiento remoto activo, un turno que
rota de verdad, y algo dentro que vela cuando todo lo demás duerme. Ceniza
te lo monta en la mesa como quien desmonta una pieza para enseñar el
mecanismo:

> — El proceso que abrió la segunda ventana está en esa máquina. No es un
> programa suelto: es un demonio con su propio servicio, arrancado por el
> sistema, con sus permisos y su horario. Vas a entrar, vas a ver qué
> corre, y vas a decidir qué hacer con él. Los procesos no se matan por
> rabia: se señalan, se les manda una orden, y solo entonces se les quita
> la vida si no queda otra. Ese es el orden. Guárdalo.

Primera vez que tocas una máquina en servicio. La luz cuenta. Cada
comando ruidoso aquí sube la factura de otra manera: el Alto cobra en
alertas lo que los Muelles cobraban en tiempo. Cuando entras, las dos
avenidas están encendidas, y sabes que de eso a la nuca del Faro no hay
sino un palmo de lo que no se apaga jamás.

---

## ENCARGOS — La mesa (muestra integrable)

*Formato por encargo: objetivo técnico + beat + decisión de karma + gancho
post-mortem (§2.6.1). Los textos entran como claves; el generador pone la
piel procedural encima (nombres, PIDs, rutas). Capítulo con deriva hacia
el descenso del Acto 2: la luz del Alto hace que cada salida pida más y
pague menos.* 

### E1 — «El demonio de la 03:00» (azul, `story.ch3.e1`)

Un proceso que vigila los contadores del Alto lleva arrancado
diecinueve años, más que la subestación que lo aloja. El turno de la 03:00
lo reaplica cada noche porque hace años que nadie lo toca y alguien en
Lumen decidió que si no se podía apagar, se mantenía. La asociación de
vecinos quiere saber qué vigila exactamente; lleva tres inviernos
pidiéndolo sin respuesta.

- Técnico: `ps aux` para ver qué corre y de quién subsiste; leer la
  variable de entorno que lo arranca (`env` del proceso) para saber qué
  camino ejecuta de verdad y qué no le dejan ejecutar.
- Beat: el demonio vigila los contadores del Alto, sí; la parte que nadie
  declaró es que también vigila las bajas. Cada noche compara a los que
  el censo da por presentes con los que el medidor de luz ve moverse.
  Nadie programó eso en un martes: se heredó del padre del proceso.
- Karma: rotar la credencial del servicio y registrarlo (azul) o dejarla
  viva para volver a mirar por ahí tú mismo (rojo). El demonio no sabe a
  quién cuida, solo que tiene que cuidar.
- Gancho: al salir, la patrulla tarda más de lo que el turno esperaba.
  El mapa del Alto cambia de forma esa noche, y nadie sabe por qué.

### E2 — «El fusible» (gris, `story.ch3.e2`)

Un servicio del Umbral alto lleva horas en bucle de reinicio: arranca,
muere a los seis segundos, arranca. El sistema lo intenta según su
política y no pregunta qué pasó. Un proveedor de mantenimiento cobra por
hora de intento. Zeta lo ha visto reiniciar once veces desde que te
consiguió la entrada y apuesta a que el proceso ni siquiera es necesario
— que alguien lo dejó encendido para cobrar el reinicio.

- Técnico: `ps` para cazar su PID, averiguar de qué señal le llega la
  parada, y decidir: pararlo en seco (`kill`) a ver si el sistema decide
  que no lo necesita, o leer su configuración de arranque (`systemctl
  cat`, estado del servicio) para saber a quién le sirve seguir en bucle.
- Beat: en la configuración hay un comentario firmado con iniciales que
  no figuran en el censo del personal. «No apagar hasta nuevo aviso.
  Quién avisa: yo.» No hay medio de saber quién es «yo».
- Karma: gris. Detener el bucle ahorra al proveedor horas y al Alto una
  factura, pero si el servicio era la red eléctrica de un nodo civil,
  apagarlo cuesta más de lo que ahorra. El gris aquí lo decide el dato
  que leas, no la postura con la que entres.
- Gancho: si lo matas y el sistema no lo relanza, Zeta te cuenta las
  veces que ella probó lo mismo: once, y no hubo relanzamiento. «El bucle
  era la trampa, no el proceso.»

### E3 — «El paquete sin remite» (rojo, `story.ch3.e3`)

El Alto recibe cada jueves un paquete firmado por un certificado que
caducó en verano. Quienes lo abre no miran quién lo firmó; abren lo que
trae. El paquete instala una actualización en el demonio del censo y deja
una copia comprimida en un directorio temporal. Gris quiere la copia
antes de que se borre sola, y lo pide como quien pide el peso de la fruta:
«tiene que salir entera, y nadie se entera.»

- Técnico: descomprimir lo que hay en el directorio temporal (`tar`,
  `gzip`) para leer qué instala de verdad; comparar el contenido con lo
  que el certificado dice firmar.
- Beat: la actualización no toca el censo: toca la lista de purgados.
  Añade un nombre nuevo a la sección que no debería tocarse con un parche
  rutinario. El nombre no es de nadie que conste.
- Karma: rojo. Entregar la copia entera a Gris (rojo: la guarda para
  vender la información, y el que la compre decide el uso) o deshacer lo
  que el paquete instaló y que no se entere nadie (azul: más arriesgado,
  dejas huella de que viste lo que no debías). Lo que el paquete deja
  escondido solo lo saben quienes lo leen.
- Gancho: al día siguiente el directorio temporal está vacío y reluciente.
  El proceso que lo limpió no figura en ningún turno.

### E4 — «La cuenta que no cuadra» (rojo, `story.ch3.e4`)

La subestación secundaria factura a un servicio del Faro que no existe en
el censo de consumo. El turno de mantenimiento de la noche ve la factura,
la marca como «revisar» y nadie la revisa porque nadie quiere subir al
Faro a preguntar. Los Apagados quieren saber de dónde sale la factura
antes de que Lumen mire dos veces la subestación que les da sombra.

- Técnico: seguir procesos por su propietario real (`ps` con detalle de
  usuario), leer las variables de entorno del que no debería estar
  (`env`), y si hace falta elevar — primera vez aquí — usar `sudo` con
  la credencial que el capítulo te ha ido ganando, no con la que te
  prestaron. El primer sudo serio del juego: la llave se gana, no se
  mendiga.
- Beat: la factura sale de un proceso arrancado con permisos de
  administración que no pertenece a ningún servicio registrado. Está
  pagando una línea de datos externa desde antes de los Apagones, y las
  facturas las sella un nombre de administrador que fue purgado hace
  siete años. Los muertos que facturan serían graciosos si no fueran
  contabilidad en vivo.
- Karma: rojo. Copiar el log de la cuenta y llevárselo a Gris (rojo: es
  la prueba de que Lumen factura por los muertos, y valor se le da
  donde se le compra) o cerrar la línea y borrar el rastro a tu paso
  (azul: cuesta un `sudo` más y deja la subestación un poco más quieta).
- Gancho: la línea externa, al cerrarse, deja visible una pequeña
  ventana abierta hacia el Faro. No la cierres tú hoy. Eso es del
  capítulo siguiente.

### E5 — «La lista del reinicio» (cierre de capítulo, `story.ch3.e5`)

Encontrar, dentro de la subestación secundaria, el demonio exacto que
abrió la segunda ventana de las 11:04. No es el mismo servicio de la
03:00: es un hermano gemelo, arrancado con la misma imagen, con un número
distinto de PID. En su configuración de arranque está la lista de ventanas
que ha abierto, y la primera fecha coincide con el día de tu firma.

- Técnico: la secuencia completa del capítulo en un solo proceso: `ps`
  para encontrarlo, `env` para leer de dónde sale su credencial, `sudo`
  para mirar su configuración real si hace falta, y la señal (`kill`)
  correcta según lo que llegues a decidir.
- Beat: el demonio no abrió la ventana: la vuelve a abrir cada vez que
  el sistema se reinicia. Tu firma está escrita en su argumento como
  parte del arranque, no como resultado de nada que tú hicieras. Algo lo
  arrancó con tu número por defecto, en una ciudad donde tu número no
  existe salvo en dos archivos. La ventana no se abrió porque algo lo
  decidiera esa mañana: se abrió porque el arranque la traía puesta.
- Karma: pararlo con la señal limpia y registrar el porqué (azul: el
  reinicio no lo relanza, y por una noche el Alto deja de abrir tu
  ventana) o dejarlo corriendo y copiar su configuración entera (rojo:
  la lista de ventanas futuras vale más que el silencio de una noche).
- Cierre de capítulo: el fragmento 3 puede caer aquí (ver
  `FRAGMENTOS.md`, fragmento 3 — el contrato).

---

## ESCENA DE HUB — Gris y la factura del Alto (regla de la luz, ahora en vivo)

La regla que Gris te explicó en los Muelles como tarifa se cobra aquí con
moneda distinta. Vuelves con menos créditos y más alertas; Gris no te deja
preguntar, te contesta antes de que lo hagas:

> — Ahora ya sabes por qué el Faro no tiene precio: tiene dueño. El Alto
> te deja subir hasta que algo te mire dos veces, y la segunda mirada ya
> la facturan en alertas, no en moneda. Subir es barato la primera vez.
> La segunda la pagas con la nuca. Conozco a tres operadores que lo
> olvidaron y a ninguno que lo vuelva a olvidar. Si quieres llegar al
> troncal, deja de ahorrar miradas: el Faro no perdona la cuarta.

## ESCENA DE HUB — La grieta de Ceniza (beat 6 §2.5) — `story.ch3.ceniza`

*La escena que planteaba el beat 6 del Acto 2, sin resolverla. Manus la
escribe como contradicción: Ceniza sabía que el primer trabajo era veneno
y no avisó. Cola de eventos: se dispara la primera vez que el jugador
vuelve con la configuración del demonio gemelo en las manos. Formato post-
mortem, la grieta en su propia voz — señala, no consuela, no se disculpa
del todo.*

Ceniza lee la lista de reinicios del demonio y monta el informe en
silencio. No levanta la vista. Cuando habla, lo hace con la cadencia del
turno de guardia, no con la voz de mentora:

> — Esa primera fecha es el día de tu firma. Ya lo sé. Lo sé desde que te
> puse la puerta delante, y no te lo dije.
>
> — El primer trabajo era veneno. Lo sabía antes de dártelo. No te avisé
> porque un perfil sin registro es la única llave que abre ciertos nodos
> de Continuidad sin que la luz se encienda entera. Te necesitaba dentro
> para llegar a esto: a un proceso que arranca con tu número y que solo
> alguien sin historial puede leer sin disparar las cuatro alarmas a la
> vez.
>
> — No te pido que lo entiendas ahora. Te pido que sepas la diferencia
> entre usarte y advertirte. Te usé, y te advertí a medias. Eso es lo que
> hicieron con la Lista antes de ti, y yo no quise ser la que lo hace
> otra vez sin decirlo. Hasta aquí no lo dije. A partir de aquí, no voy a
> volver a esconderte una puerta.
>
> [Aquí NO hay resolución ni floritura: la relación se repara o se rompe
> según lo que el jugador haga en el Hub a partir de ahora — DESIGN §2.5
> beat 6. El texto termina con el hecho, no con un abrazo. Ceniza no
> promete una salida segura; dice dónde está la puerta y qué costó.]

---

## COLA DE POST-MORTEM — Ceniza y el Auditor (cap. 3)

*Extracto integrable: líneas por clase de evento (§2.6.2/§2.6.3), nunca
repetición literal. Capítulo donde los procesos piden la señal, no el hacha.*

Primera expulsión del capítulo:

> — El log dice que entraste a mirar procesos sin ver de quién eran. Lo
> que mataste no era el demonio: era un servicio del censo con la misma
> cara. `ps` no es para ver qué hay: es para ver quién. Si no lees la
> columna del usuario, estás disparando a una fotografía.

Repetición ante el mismo obstáculo (sube el tono, añade un dato):

> — Segunda vez con el mismo nombre de proceso. El demonio y el servicio
> comparten imagen; lo que no comparten es el propietario. Lee `ps aux`.
> La diferencia entre los dos cabe en una columna, y esa columna te ha
> costado dos expulsiones. La próxima, `ps` primero y teclado después.

Y la del `sudo` usado sin llave ganada:

> — Elevaste con una credencial que no era tuya y sin saber de quién era.
> Eso no es subir: es pedir prestada una puerta ajena y que te cierren la
> cara. `sudo` con la llave que ganas no es un atajo: es la diferencia
> entre entrar y llamar a que te abran. No llames hasta saber quién
> vive dentro.

Líneas del Auditor (canal kármico §3.3, canal 2). Perfil azul:

> Expediente 000: manipulación de procesos con conservación del historial
> y registro de las órdenes enviadas. Clasificación: mantenimiento no
> autorizado. Continuidad del ensayo: estable.

Perfil rojo:

> Expediente 000: manipulación de procesos con destrucción de registros y
> apropiación de configuración. Clasificación: alteración del servicio.
> Continuidad del ensayo: estable, bajo observación de firma.

---

## GANCHO DE CIERRE — La ventana hacia el Faro

Cuando el demonio gemelo queda callado o copiado — según lo que hicieras —,
la ventana que su línea externa dejaba abierta hacia el Faro sigue ahí.
Ceniza la mira como quien mira una puerta que no piensa abrir todavía:

> — Eso que ves del otro lado no es un enlace: es el troncal. La red que
> cruza al Faro. El proceso que plantó tu número salió de ahí, y lo que
> lo plantó sigue dentro. La Lista no está en la subestación: está en el
> nodo que la custodia, al otro lado de la luz que no se apaga.
>
> — Vas a necesitar lo que has aprendido para dejar los Muelles y la
> sombra: leer quién corre, saber a quién visitas, y no matar nada hasta
> que sepas de quién es la mano. Y ahora, cuando entres, tendrás que
> hacerlo con los ojos abiertos y conmigo detrás diciéndote lo que vea.
> No vuelvo a esconderte una puerta. Eso no significa que vaya a
> protegerme de la tuya.

El boletín de las 07:00, la voz calmada de siempre:

> ...la subestación del Alto ha completado su ciclo de mantenimiento. Los
> servicios recuperan la normalidad. El censo se mantiene íntegro y la
> continuidad del servicio, garantizada. Gracias por su confianza.

En los días siguientes, la subestación secundaria deja de abrir la
ventana de las 11:04. En el Faro, algo que nadie apaga percibe la
diferencia, y empieza a hacer preguntas que no están en el formulario de
las 07:00.

*Fin del capítulo 3. Sigue en el capítulo 4 «Troncales»: cruzar la luz
que no se apaga buscando el nodo que custodia la Lista, y al dueño de la
mano que plantó tu número.*

---

### Notas para el integrador

- Claves sugeridas: `story.ch3.apertura`, `story.ch3.e1`–`story.ch3.e5`,
  `story.ch3.gris`, `story.ch3.ceniza` (la grieta, beat 6),
  `story.ch3.postmortem_ceniza`, `story.ch3.auditor_azul`,
  `story.ch3.auditor_rojo`, `story.ch3.troncal`.
- Voz verificada contra PERSONAJES.md (Ceniza, Gris, Zeta, Auditor, Vela).
  Test del nombre tapado: la grieta de Ceniza lee como ella — dato antes
  que ánimo, el consuelo es un hecho, la salida nunca se promete. Gris
  da la regla de la luz como tarifa con la cifra ya dada. Zeta cuenta
  sus once intentos. El Auditor cierra con frase-neutra-juicio.
- Karma de cap. 3: E1 azul, E2 gris, E3 rojo, E4 rojo, E5 de cierre con
  ambas salidas. Deriva del capítulo hacia el descenso del Acto 2: más
  líneas rojas y grises que en el 2, coherente con §3.3 (reputación
  emergente: un perfil que sube al Alto recibe trabajos más sucios).
  Aceptar suma poco; lo que manda es cómo se resuelve cada run.
- ⚠️ Bloques de terminal: los del capítulo usan `ps`, `env`, `sudo` y
  señales. Verificar contra exactamente lo que el sandbox soporte cuando
  el cap. 3 entre en currículo (igual que el cap. 0 se verificó contra
  `test_session_cap0.py` y el 2 contra su SESIÓN pendiente). Hasta
  entonces son contrato pedagógico, no salida reproducible. Los PIDs y
  nombres de proceso son piel procedural del generador.
- Primer `sudo` serio del juego: la credencial se GANA durante el
  capítulo (E3/E4), nunca se presta de entrada (regla §2.6.1: sin barrera
  técnica superada no hay avance). Decisión pedagógica para Smough: el
  sandbox debe poder modelar una credencial que habilita `sudo` sin
  proponer `sudo` antes de que el currículo lo presente.
- `story.ch3.*` aún NO están en `curriculum.json` (dueño Smough cuando
  toque el cap. 3). El 3 es la familia «Procesos y sistema» (§6.2).
- Continuidad de la cifra: el resto del corpus usa el 47 (CANDELAS nº 47,
  HOSP-47-C, NHC 47-C-0191); este capítulo introduce el 03:00 como hora
  muerta del Alto y no rompe el 47 — el demonio de E1 es del turno de las
  03:00, y el folio del fragmento 3 es 14-0007. Los dos son candados del
  mismo archivo que nadie ha abierto entero.
- La grieta de Ceniza (E5 → `story.ch3.ceniza`) es beat 6 del Acto 2
  (§2.5): se PLANTA aquí, no se resuelve. Las consecuencias (reparar o
  romper la relación) se deciden en las decisiones de Hub de capítulos
  posteriores; este texto no adelanta resolución. Regla §2.6.7: el tema
  (usar para proteger) jamás se enuncia por el narrador; lo dice Ceniza
  como hecho, no como lección.