# CAPÍTULO 0 — Trabajo en frío

> Acto 1, beats 1–3 (DESIGN §2.5). Tutorial sin teoría: 1 sala, 1 run guiada.
> Objetivo técnico (`ls`/`cd`/`cat` por necesidad) + beat narrativo +
> decisión de karma (aquí, la primera) + gancho post-mortem.
> Estado: `[LISTA]` para integración → `src/data/story/`.

---

## ESCENA DE APERTURA — El dossier

Nadie te explicó el trabajo. Te dieron una dirección del Umbral bajo y un
dato: en la centralita de la oficina vecinal hay un fichero que otra persona
quiere tener. Copiar, no tocar. Eso es todo el briefing.

Carbón en papel de impresora reciclada:

```
OFICINA VECINAL — MUELLE NORTE 12B
turnal: 11:04 (ventana de silencio)
fichero: nombre_de_proveedor.txt  (3 KB, usa el nombre que diga la cadena)
objetivo: copiar, no borrar
```
- Dirección escrita a mano, con erre que parece corrida por calor.
- Nadie firmó. Nadie pidió favores. Corre en sentido de la ciudad: pagas
  cobertura, no preguntas.

Es tu primer encargo legítimo. Todo sale bien al final; es lo que punza.

---

## ESCENA TÉCNICA — La ventana (run guiada, cap. 0)

Ceniza no está contigo. La única voz que entra es la del sistema.

```
conectando → oficina-vecinal-muelle-norte...
$ ls
nombre_de_proveedor.txt  log.txt  README
$ cat nombre_de_proveedor.txt
CANDELAS  ·  proveedor nº 47  ·  facturación externa  ·  114 facturas/mes
$ cd ..
$
```
Copia el fichero. La sesión se cierra sola a los 11 minutos. Nada se rompe,
nadie te ve, el ruido de extracción es mínimo. Vuelves a la calle con la
copia en un USB de 512 MB y un número que ya no te importa: 11:04.

Primera línea del Auditor, al cierre, con su precisión de formulario:

> Registro de sesión: 1 fichero accedido, 0 marcados para borrado. Salida
> limpia. Continuidad del servicio: no interrumpida.

No es una felicitación. Es un recibo. Te lo cobran después, y tú no lo sabes
aún: esa ventana de las 11:04 dejó tu firma donde no estuviste.

---

## ESCENA DE LA MAÑANA — La firma

Amanece y Vesper lleva tu nombre puesto a la espalda, salvo que tú no tienes
nombre. Hay un perfil de ti en todos los medios: la intrusión del Muelle Norte
tiene autor, y el autor eres tú. Saben detalles que solo el inquilino de la
sesión podría saber — la ruta exacta, la hora, el silencio del timestamp. No
los has cometido. Los sabían por ti porque alguien corrió tu sesión mientras
la tenías abierta, y el protocolo de Lumen lo atestigua: IP visitante,
telemetría de terminal, todo limpieza. Eres la única persona de la ciudad,
de las trescientas mil del censo, que no aparece en ninguna parte. Lumen no
tiene ficha tuya. Un sospechoso sin registro es perfecto: no puede demostrar
nada porque no existe.

La voz de Vela abre el boletín de las 07:00. La misma voz que dice que el
servicio funciona dice ahora tu número de formato:

> ...se informa de una intrusión en una instalación de facturación del
> sector 12. Los protocolos de continuidad del servicio están activos. El
> incidente está siendo gestionado. La identidad del responsable, en fase de
> verificación. Gracias por su colaboración.

Verificación. Te acabas de enterar de que existes en su papel a la vez que
dejas de existir en el tuyo.

---

## ESCENA DE RECOGIDA — La Subestación

Ceniza te espera en un callejón del Muelle Norte, junto al contenedor de
residuos del hospital (placa `HOSP-47-C`). No te saluda. Te entrega un
terminal de mano y te indica la entrada de la subestación con la barbilla.

> — Leí tu sesión. Bien por no borrar nada: borrar deja rastro en el libro
> nuevo, aunque no en el viejo. Entra.

Dentro, un lugar que no huele a data center sino a metal sudado. Dos
transformadores vacíos, un tablero con la luz de «CORTE MANUAL» clavada
desde hace diecinueve años, y un rack del hospital vuelto vertical que
parpadea en verde. La tira de LED de la mesa de encargos es la única luz
fija de la sala.

Ceniza se sienta frente al rack y no te pregunta por el trabajo. Pregunta
por la telemetría.

> — El informe dice salida limpia. Tú sabes que no lo fue. En la sala de
> facturación miraste el fichero por fuera; el rastro quedó. No te van a
> coger por eso. Te van a coger por lo que aún no sabes que dejaste.

Te pide lo que pide a todos los que entran aquí: que trabajes para los
Apagados a cambio de cobertura. No lo dice como favor ni como rescate. Lo
dice como intercambio, mientras enciende un aparato que se vuelve el único
espejo de la sala.

> — No prometo que no te encuentren. Prometo que cuando te busquen, no te
> encuentren sola.

---

## DECISIÓN DE KARMA — La primera (suave)

Sobre la mesa, dos papeles clavados con cinta. Gris los fue pegando mientras
lo oíais discutir de precios.

**Encargo azul** — un hospital del Umbral bajo cree que alguien está leyendo
expedientes que no debería leer. Quieren saber quién. (Defensa, rastro de
terceros, sin romper nada.)

**Encargo rojo** — una inmobiliaria del Umbral tiene una lista de viviendas
embargadas que Lumen no contabiliza. Alguien la quiere para presionar a dos
familias concretas. (Reconocimiento rápido, copia de la lista, salir antes
de que suenen.)

Elección de trabajo, no de bando. Karma se lee después, en el mundo, no en
una barra: Gris te ofrecerá hardware ofensivo o herramientas de auditoría
según cómo resuelvas esto; el Auditor lo anotará en el informe como si
observara el tiempo. Ahora solo eliges.

Si mueres en la primera run, no es game over: es un dato. El post-mortem
tuvo línea:

> Expediente 000: expulsión un 40 %. Lección asociada: el objetivo se nombra
> antes de mirarlo. No se busca sin saber qué se busca.

Y otra, más abajo, que no pidió nadie:

> Sujeto sigue siendo observable para el ensayo. Continuidad garantizada.

Morir alimenta a tu cazador. También alimenta tu aprendizaje. Ese nudo es
el corazón de todo.

---

## GANCHO FINAL

Antes de que el sol suba del todo por los Muelles, Gris se acerca a la mesa
de encargos, mira el papel azul, mira el rojo, y suelta, como quien arregla
el cable del cargador de un enchufe que ya no funciona a propósito:

> — El azul lo paga una enfermera que no llega a fin de mes. El rojo lo paga
> alguien con apellido en el Faro. Tú decides si el dinero que te pagan sabe
> de dónde viene. A mí me da igual, yo cobro igual, los dos te cuestan lo
> mismo. Dime cuál.

No sonríe. Ni tú. Esa es la primera vez que la ciudad te pide que elijas
quién eres, y no tienes ni nombre con el que responderle.

*Fin del capítulo 0.*

---

### Notas para el integrador
- Claves sugeridas `story.ch0.dossier`, `story.ch0.ventana`,
  `story.ch0.firma`, `story.ch0.subestacion`, `story.ch0.karma_azul`,
  `story.ch0.karma_rojo`, `story.ch0.postmortem_1`, `story.ch0.gancho`.
- Voz verificada contra PERSONAJES.md (Ceniza/Gris/Auditor/Vela). Nombre
  tapado: cada línea se reconoce por su dueño.
- Karma de cap. 0: decisión marcada `[P2]` peso suave (primer encargo);
  lo que manda es cómo se RESUELVA la run, no elegir (DESIGN §3.3).