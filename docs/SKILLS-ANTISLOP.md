# Skills anti-slop — manual de escritura de Manus

> Qué herramientas y técnicas usa Manus para que la narrativa y los niveles de
> CyberRoot no suenen a IA ramplona. Es un manual operativo: qué skill abrir,
> cuándo, con qué criterio y cómo lo comprueban los revisores.

## Por qué existe

CyberRoot vive o muere por su texto. La terminal ES la atmósfera: descripciones
de niveles, item descriptions, barks, diálogos. Todo lo que el jugador lee pasa
por un modelo de lenguaje, y los modelos tienen sesgos estadísticos documentados
que producen "AI-slop": prosa inflada, genérica, con ritmo de folleto. El
humanizer lo resume bien: el modelo tiende a la continuación más probable, y la
continuación más probable es justamente lo que ya hemos leído mil veces.

La defensa no es un solo skill. Son tres capas:

1. **Filtro de salida** (humanizer): elimina los patrones reconocibles.
2. **Craft positivo** (técnicas de escritura de videojuegos): añade voz,
   especificidad y estructura narrativa buena. Quitar slop no basta; un texto
   limpio pero sin alma también delata a una IA.
3. **Proceso del concilio** (checklist + revisión): el anti-slop como criterio
   explícito de aceptación/rechazo, no como buena intención.

---

## Capa 1: humanizer como filtro de salida

Skill Hermes: `creative/humanizer` (v2.5.1). Basado en la guía "Signs of AI
writing" de Wikipedia (WikiProject AI Cleanup). Trae 34 patrones con
antes/después.

### Cuándo usarlo

SIEMPRE como último pase antes de publicar cualquier texto de juego o doc de
repo. No durante la escritura: primero se escribe libre, luego se filtra. Filtrar
mientras se escribe produce prosa tímida.

### Matiz importante: es un filtro, no una ley creativa

El humanizer nace de prosa expositiva en inglés (artículos de Wikipedia). En
ficción, algunos "patrones" son recursos legítimos según quién hable:

- **Fragmentación dramática (patrón 31)**: prohibida en narrador y descripciones;
  permitida en un bark o en la voz de un personaje nervioso. "No insistas." funciona
  como diálogo porque la gente habla así.
- **Regla de tres (patrón 10)**: mala en descripción (suena a folleto), legítima si
  es tic caracterial de un personaje concreto.
- **Clichés en boca de personaje**: un secuoya corporativo del Red Team DEBE hablar
  en clichés de LinkedIn. Eso es caracterización, no slop.

Criterio general: el narrador y las descripciones cumplen TODOS los patrones; los
personajes pueden violar los patrones si la violación cuenta algo de ellos.

### Los patrones que más nos van a doler (adaptados a español)

El humanizer lista palabras inglesas. Estas son las equivalencias españolas que
hay que vigilar en nuestro texto:

| Patrón (humanizer) | Equivalente español típico | Ejemplo de slop |
|---|---|---|
| 1. Inflar significado | "testamento de", "papel crucial/pivotante", "marcar un antes y un después" | "Este servidor es un testamento de la era dorada." |
| 3. Gerundios falsos-profundos | "...reflejando...", "...simbolizando...", "...destacando..." | "Los pasillos están vacíos, reflejando la soledad del sistema." |
| 7. Vocabulario IA | "panorama", "hoja de ruta" (metafórico), "apalancar", "robusto" | "en el actual panorama de ciberseguridad" |
| 8. Evitar copula | "actúa como", "funciona como símbolo de" en vez de "es" | "La torre actúa como corazón del datacenter." |
| 9. Paralelismo negativo | "no solo..., sino que también..." | "No es solo un juego, es una experiencia." |
| 14. Rayas de énfasis | guiones largos a cada frase | "El nodo—frío, silencioso—esperaba." |
| 23. Relleno | "cabe destacar", "es importante señalar", "con el fin de" | "Cabe destacar que el exploit requiere root." |
| 27. Autoridad persuasiva | "la verdadera pregunta es", "en el fondo" | "La verdadera pregunta es si confiar en Root." |
| 28. Signposting | "vamos a analizar", "a continuación exploraremos" | "A continuación, exploraremos el subsistema de red." |
| 33. Aperturas de tic | "Así que...", "Curiosamente,", "En esencia," | "Curiosamente, el log estaba vacío." |
| 34. Consuelo pegado | "y está bien", "no pasa nada", "no estás solo" | "Morir forma parte del proceso. Y está bien." |

Comprobación rápida y barata antes de commit:

```bash
grep -nEi "testamento|pivotante|cabe destacar|es importante señalar|no solo.*sino|panorama|curiosamente|en esencia|simbolizando|reflejando" <archivo>
```

Si sale algo, o lo reescribes o justificas en comentario (voz de personaje).

### Voice calibration

El humanizer permite calibrar contra una muestra de voz. En CyberRoot la muestra
no es de Juanma: es el propio corpus del juego. Antes de escribir un personaje,
releer sus últimas 20 líneas en `docs/` y mantener sus patrones (longitud de
frase, vocabulario, puntuación). La coherencia interna del corpus importa más
que cualquier guía externa.

---

## Capa 2: craft por superficie textual

Aquí está el valor añadido que el humanizer NO da. Cada superficie del juego
tiene su técnica correcta.

### Mapa de superficies

| Superficie | Técnica principal | Referencia |
|---|---|---|
| Descripción de niveles / ambiente | Narrativa ambiental estilo FromSoftware | Lokey (2020), análisis DS |
| Diálogo con NPCs | Diálogo reactivo estilo Hades | GDC 2021 (Kasavin/Korb) |
| Barks y eventos reactivos | Sistema de barks (1 idea, corto, contextual) | estándar AAA |
| Item descriptions / logs / lore files | Iceberg de Hemingway + contradicción controlada | Souls + Hemingway |
| Textos de muerte / post-mortem / UI | Voz del sistema, funcional y con carácter | Hades (muerte=diálogo) |

### Niveles y ambiente: el jugador es el arqueólogo

Dark Souls casi no explica: muestra consecuencias y deja que el jugador
reconstruya la causa. Principios extraídos del análisis del environmental
storytelling de FromSoftware (Lokey 2020; literatura académica sobre DSIII):

1. **Describe consecuencias, nunca causas.** Mal: "La IA se rebeló contra sus
   creadores". Bien: "En la pared hay marcas de uñas. Salen de dentro del
   armario de servidores."
2. **Un detalle físico por habitación.** No tres. Un cable arrancado, una silla
   con correas, café seco en el teclado. El detalle específico genera más mundo
   que un párrafo de ambientación.
3. **Las fuentes se contradicen.** El log oficial dice que nadie murió en el
   incidente. El grafiti del pasillo pone cinco nombres. El jugador decide a quién
   creer. Esta contradicción controlada es EL mecanismo Souls y además vacuna
   contra el slop (el slop siempre es consistente y explicativo).
4. **Nada de resúmenes de significado.** Si cierras una descripción diciendo qué
   significa ("una cruda metáfora de..."), has fallado. Corta esa frase: siempre
   sobra.

Ejemplo CyberRoot, nivel "Archivo Muerto":

> Slope: "El Archivo Muerto es un testimonio de la caída del consorcio. Sus
> pasillos silenciosos reflejan la soledad de un sistema olvidado, simbolizando
> la fragilidad de la confianza digital."
>
> Bien: "Los ventiladores siguen encendidos. Nueve años consumiendo la batería
> de reserva porque nadie quiso ser el que volvió a apagarlos."

La versión buena tiene fecha implícita, causa implícita, miedo implícito. Cero
abstracciones.

### Diálogo: reactivo, corto, jerárquico

Hades resolvió narrativa en roguelite con más de 22.000 líneas habladas (GDC
2021, Kasavin y Korb). Lo transferible a nuestro sistema:

1. **El mundo reacciona a lo que acabas de hacer.** Tras un run donde el jugador
   usó sudo rm recursivo, el mentor comenta ESO, no un texto genérico de
   aliento. Regla: ninguna línea de diálogo que pudiera aparecer en cualquier
   momento.
2. **Cola de prioridad de eventos**, no diálogos sueltos: cada evento del juego
   (primera muerte, primer exploit, traición, karma cruzando umbral) tiene líneas
   asociadas en los personajes relevantes. Manus escribe contra esa cola, no
   "diálogo de relleno".
3. **Primera línea = información nueva.** Si la primera frase de un NPC puede
   quitarse sin perder nada, todo el turno sobra.
4. **Repetición con variación, nunca repetición literal.** Cuando el jugador
   vuelve a morir ante el mismo boss, el personaje NO repite: sube el tono, se
   impacienta, suelta un dato nuevo. Hades construye relación mediante esa
   escalera.

### Ficha de voz por personaje (obligatoria antes de escribirlo)

Técnica estándar de game writing (ver Emily Short sobre diseño de conversación):
nadie habla hasta tener ficha. Formato mínimo por personaje en `docs/`:

```
## [Nombre]
Quién es en una frase:
Sintaxis: (frases largas/cortas, subordinaciones, preguntas...)
Vocabulario: (campo semántico que domina, palabras favoritas)
Tic: (muletilla, manía gramatical, qué nota siempre)
Nunca diría: (3 cosas, concretas)
```

La fila "nunca diría" es la más potente contra el slop: el slop es lo que
diría cualquiera. Un personaje definido por negaciones es imposible de confundir
con otro. Test de la ficha: tapa el nombre en cualquier línea del juego; si
podría ser de otro personaje, se reescribe.

Emily Short (columna "Conversation Design in Games", Game Developer 2023) aporta
dos reglas más para escenas: toda conversación tiene un objetivo de escena (qué
cambia para el jugador) y un ritmo (quién empuja, quién resiste). Diálogo sin
objetivo de escena es relleno con voces distintas.

### Item descriptions y lore files

Formato Souls: dato técnico arriba, grieta humana abajo. Nunca adjetivos de
atmósfera.

> Slope: "Antigua llave USB de procedencia misteriosa que guarda secretos del
> pasado."
>
> Bien: "USB de 512 MB. Etiqueta manuscrita: 'copia FINAL (de verdad)'. Última
> modificación: 03:47 del día del incidente."

La especificidad (512 MB, 03:47) es la vacuna anti-slop más barata que existe:
lo estadísticamente probable es vago; lo concreto casi nunca lo es.

### Barks

Reacción de una línea a una acción concreta. Presupuesto estricto:

- Máximo 8-12 palabras.
- Una sola idea.
- Se entiende sin contexto previo.
- Verbos y sustantivos concretos, cero adjetivos atmosféricos.
- Prohibido explicar mecánicas en un bark (para eso está `help`).

"Bark" malo: "¡Cuidado! Los firewalls de esta zona son capaces de detectar tu
intrusión." Bark bueno: "Firewall. Tercero hoy. Te está esperando."

---

## Capa 3: integración en el flujo del concilio

Dónde entra esto en el trabajo diario:

1. **Manus redacta** (plot del día -> superficies). Escritura libre primero;
   ningún filtro durante la redacción.
2. **Auto-pass anti-slop** (obligatorio, documentado en el commit): releer y
   responder por escrito a la pregunta "¿qué delata aquí a una IA?"; corregir
   una vez. Es el proceso interno del propio humanizer, aplicado a cada entrega.
3. **Grep de palabras trampa** (comando de la capa 1) sobre los ficheros nuevos.
4. **Test de ficha de voz**: cada línea de diálogo contra la ficha de su
   personaje. Nombre tapado, autor reconocible.
5. **Revisión Ornstein/Smough** (21/23h): este documento es criterio explícito
   de rechazo. Un rechazo cita patrón + línea ("patrón 3, gerundio falso, línea
   42") para que la corrección sea quirúrgica.
6. **Registro de tics recurrentes**: si el mismo patrón se cuela 3 días seguidos,
   se añade abajo como tic conocido de Manus con su contramedida, para dejar de
   corregirlo a mano.

### Checklist final (antes de marcar texto como terminado)

- [ ] ¿Algún gerundio "profundizador"? (reflejando, simbolizando, destacando)
- [ ] ¿Alguna frase que diga qué significa la escena en vez de mostrarla?
- [ ] ¿Cabe destacar / es importante señalar / no solo... sino?
- [ ] ¿Tres adjetivos atmosféricos juntos en alguna frase?
- [ ] ¿Cada NPC pasa el test del nombre tapado?
- [ ] ¿Cada pieza de lore es una consecuencia verificable, no una explicación?
- [ ] ¿Los barks caben en una línea y valen sin contexto?
- [ ] ¿Hay al menos un dato concreto (número, hora, nombre) por descripción?
- [ ] ¿Leerlo en voz alta suena a persona o a folleto?
- [ ] Respuesta escrita a "¿qué delata aquí a una IA?"

---

## Referencias

- Skill `humanizer` v2.5.1 (Hermes, local): 34 patrones, proceso de doble pasada.
  https://github.com/blader/humanizer
- "Breathing Life into Greek Myth: The Dialogue of Hades", GDC 2021 (Darren Korb
  y Greg Kasavin, Supergiant). https://www.gdcvault.com/play/1026975/
  Verificado hoy: charla real, 22.000+ líneas de diálogo en Hades.
- Emily Short, "Analysis: Conversation Design in Games", Game Developer (2023);
  archivo completo en https://emshort.blog/how-to-play/writing-if/
- Environmental storytelling de Dark Souls: análisis de Lokey
  (https://lokeysouls.com/2020/11/16/environmental-storytelling/) y literatura
  académica sobre DSIII (repositorio UFU).
- Craft de base (consolidado, sin URL): Hemingway (iceberg), Vonnegut ("pity the
  reader; he is in a lot of trouble more often than you think"), Strunk & White.

## Límites honestos

- Ninguna técnica garantiza texto con alma; garantizan eliminar lo peor. La
  calidad final sigue dependiendo de que el plot del día tenga ALGO que contar.
  Un día sin conflicto no se arregla con estilo.
- Las referencias web se verificaron el 24/08/2026; las URLs de blogs pueden
  moverse.
- El grep de palabras trampa es ayuda, no auditoría: el slop grave es
  estructural (ritmo uniforme, ausencia de opinión), y eso solo lo caza la
  lectura atenta del paso 2.
