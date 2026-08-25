# DESIGN — CyberRoot

> Documento vivo de diseño de Fase 0. Se construye en cinco pases:
> - **PASE 1 (este)** — concepto, historia, plot general, caminos y finales.
> - Pase 2 — loop roguelite (Hades) + dopamina (Balatro). 11:00 del 25/08.
> - Pase 3 — capítulos y niveles. 15:00 del 25/08.
> - Pase 4 — dopamina fina y UX. 21:00 del 25/08.
> - Pase 5 — revisión final. 09:00 del 26/08.
>
> Marcos cerrados que este documento no discute: `AGENTS-PLAN.md` §6.5.
> Insumos: `docs/RESEARCH-MECANICAS.md` · `docs/INVESTIGACION-STACK.md` ·
> `docs/SKILLS-ANTISLOP.md` · `docs/BRAINSTORM.md`.

---

## 1. Concepto y gancho

CyberRoot es un RPG roguelite donde aprender Linux de verdad ES subir de nivel.
Eres un operador sin pasado en Vesper, una ciudad-puerto donde todo corre sobre
el Grid: la red de Lumen, la corporación que lleva cuenta de cada vecino desde
los Apagones que casi la mataron hace diecinueve años. Tu primer trabajo sale
mal antes de empezarlo: alguien aprovecha tu acceso limpio para abrir una cámara
de Lumen y deja tu firma en la puerta. Un sospechoso sin registro es perfecto —
no puede demostrar nada porque no existe. Te recogen Los Apagados, la gente que
vive fuera del censo, y desde su base, una subestación eléctrica muerta,
empiezas a infiltrar el Grid para averiguar quién te vistió con un crimen que no
recuerdas haber cometido. Lumen tiene ficha de todos menos de ti, y esa ausencia
es a la vez tu herida y tu ventaja. Cada incursión enseña comandos reales; cada
expulsión deja una lección y avanza la trama; cada decisión inclina la balanza
entre arreglar el sistema o quemarlo.

Línea de tienda: *Hades se encuentra con OverTheWire — un roguelite donde cada
comando es un poder y morir es el método de estudio.*

---

## 2. Historia y plot general

Base para Manus/historiador. Los beats están numerados para que la escritura
diaria tenga espina fija; el corte en capítulos lo hace el Pase 3.

### 2.1 El mundo: Vesper y el Grid

- Vesper, ciudad-puerto. Hace diecinueve años, los **Apagones**: dieciocho meses
  de colapso eléctrico y de red. Datos que el juego da por gotas: el hospital
  del Muelle tiró catorce días con generadores; hubo barrios que no vieron un
  cajero hasta el año siguiente. Lumen restituyó el servicio y cobró el precio:
  hoy el Grid corre agua, tráfico, crédito, sanidad y vigilancia.
- **El censo**: Lumen puntúa a cada habitante. La puntuación decide vivienda,
  transporte y trabajo. Nadie discute el mecanismo en voz alta; casi nadie
  recuerda cómo se votó.
- **Geografía en tres anillos** (diegética y jugable a la vez):
  - **Anillo Faro** — centro corporativo, luz continua, máxima vigilancia.
  - **Anillo Umbral** — residencial y oficinas, mezcla de luz y sombra.
  - **Los Muelles** — afueras medio apagadas, sede de Los Apagados.
  - Regla de mundo que el Pase 2/4 puede volver mecánica: **más luz = más
    vigilancia**. Entrar en un distrito brillante es más fácil de intentar y más
    caro de pagar. Las incursiones profundas van hacia la luz.
- Tono: futuro cercano sin magia. La IA de Lumen (§2.4) es software de
  auditoría, no una conciencia en la nube. La fantasía que vende el juego es
  competencia técnica, no superpoderes: los comandos son reales y funcionan como
  funcionan.

### 2.2 El protagonista: Cero

- Operador sin registro. Ni Lumen tiene ficha, y eso es imposible salvo que
  alguien pagara por borrarla: en el mercado gris, una purga individual cotiza
  como un piso en el Umbral. Alguien con poder lo hizo — para castigarte, para
  protegerte o para usarte. El juego nunca dice cuál; el jugador lo reconstruye.
- **Nombre**: nadie lo sabe. Los Apagados le pusieron **Cero** porque llegó sin
  número. En los archivos de Lumen aparece como **sujeto 000** del Programa de
  Continuidad (§2.4). Mismo número en dos mundos, dos lecturas distintas.
- El pasado NO se cuenta en cinemáticas: se excava. **Fragmentos personales**
  repartidos como botín raro a lo largo de todo el juego: una foto con los
  metadatos raspados, una pulsera de hospital con fecha, un contrato de alquiler,
  una cuenta que recibió pagos mensuales de una filial de Lumen hasta hace tres
  años. Cada fragmento sostiene dos hipótesis a la vez — **H1: borraste tu
  pasado tú**; **H2: te lo borraron como ensayo**. Formato de escritura:
  descripción de objeto estilo Souls (dato técnico arriba, grieta humana abajo;
  ver SKILLS-ANTISLOP).

### 2.3 Los Apagados y la Subestación (el Hub)

Gente fuera del censo: purgada, fugada o autoexiliada. Su base es la
**Subestación**, una central eléctrica desconectada tras los Apagones y la única
corriente de la ciudad que Lumen no factura. Plantel inicial (las fichas de voz
completas se escriben antes de dar diálogo a cada uno — regla §2.6.5):

- **Ceniza** — mentora. Ingeniera que firmó partes del núcleo de auditoría de
  Lumen y vive con eso. Dirige los informes post-mortem. Habla con cadencia de
  informe de incidentes; corrige en lugar de consolar; nunca promete lo que no
  ha probado.
- **Gris** — recadero y mercader (equipo y mejoras del espejo, verá P2). Cobra
  en créditos y en favores. Cada precio lo cita dos veces y nunca igual.
- **Zeta** — operadora rival llegada del norte. Competitiva, directa, asigna
  retos opcionales (encauzamiento natural para modificadores tipo Heat — decide
  P2). Primera en tratarte de igual, última en decir algo amable.
- **El Auditor** — daemon de auditoría de Lumen que te habla durante la
  intrusión y tras cada expulsión. Te llama Expediente 000. Es la voz de la
  muerte del juego: informa con precisión quirúrgica y miente por omisión
  burocrática. Narrador poco fiable con acento de formulario.
- **La Directora Vela** — antagonista (§2.4). Al principio solo es voz en
  pantallas y avisos públicos.

### 2.4 El antagonista: Lumen y la Oficina de Continuidad

- **Lumen Holding** restauró la luz tras los Apagones y quedó de facto como
  gobierno. Su producto real no es la electricidad: es la contabilidad de vidas.
- **La Oficina de Continuidad** "garantiza la continuidad del servicio". En la
  práctica ejecuta **purgas**: borrados administrativos — crédito a cero, puerta
  cerrada, historial vacío. Su cara pública es la **Directora Adriana Vela**,
  la voz calmada de los avisos de la ciudad.
- Vela no es un villano de cartel: sobrevivió a los Apagones (su expediente del
  hospital del Muelle existe y el jugador puede encontrarlo). Pide que el
  apagón no se repita nunca; sus métodos cuentan otra historia. Cree que el
  censo es el precio de que las luces sigan encendidas. Antagonista con
  argumento defendible.
- **El secreto del argumento** (spoiler interno de diseño): el golpe que te
  atribuyeron no fue un robo. Fue la apertura de la cámara donde Lumen guarda
  **la Lista**: el volcado íntegro del censo con las marcas de cada purga.
  Alguien quería la Lista fuera y necesitaba un fantasma al que culpar. Y tu
  falta de pasado tampoco es casualidad: fuiste el sujeto 000 de la purga
  piloto de la Oficina, un ensayo controlado para medir cuánto sobrevive una
  persona sin registro. Cada expulsión la archiva el Auditor como dato del
  ensayo: **morir alimenta a tu cazador**. También alimenta tu aprendizaje —
  esa doble lectura es el corazón del tercer acto.

### 2.5 Plot general en tres actos

**ACTO 1 — LA FIRMA**

1. **Trabajo en frío.** Misión-tutorial con objetivo primero y teoría cero
   (directriz Bandit, RESEARCH-MECANICAS §1). Copias unos datos de una oficina
   del Umbral. Todo sale bien.
2. **La firma.** Al amanecer, la intrusión aparece en todos los medios atribuida
   a ti, con detalles que solo el autor conoce. Vela anuncia tu búsqueda. El
   jugador entiende que usaron su sesión mientras él estaba dentro.
3. **La Subestación.** Ceniza te recoge. Primer informe post-mortem aunque no
   hayas muerto: el sistema ya te está leyendo. Pacto: trabajas para los
   Apagados a cambio de cobertura.
4. **Primera elección.** Dos encargos sobre la mesa, uno azul y otro rojo. El
   karma entra sin tutor moral: eliges trabajo, no bando.
   *Función del acto:* instalar el loop (run → expulsión → Subestación → run),
   la fantasía competente y la pregunta motor («¿quién usó mi acceso?»).

**ACTO 2 — LA LISTA**

5. **Escalada.** Los encargos de los Apagados suben por distrito y por anillo
   (aquí vive el currículo — lo estructura el Pase 3). Cada distrito aporta un
   fragmento del pasado y un dato de la Lista.
6. **La grieta de Ceniza.** Descubres que ella sabía que el primer trabajo era
   veneno y no avisó: te necesitaba dentro, porque un perfil sin identidad es
   el único que puede acercarse a ciertos nodos sin disparar alarmas. La
   relación se repara o se rompe según decisiones del Hub.
7. **El expediente.** En una cámara del Anillo Faro aparece el Programa de
   Continuidad: sujetos 001–012, todos cerrados por fallo. Tu número está
   vacío. El log dice «ensayo completado»; la fecha de cierre, en blanco. Dos
   lecturas: el único que sobrevivió, o el único que aún corre.
8. **El giro del Auditor.** Empieza a preguntar cosas que no constan en el
   formulario. Semilla de su arco (abierto en §4).
9. **Presión máxima.** Vela localiza la Subestación — consecuencia acumulada de
   las alertas reales del jugador, no guion. Asalto defensivo al Hub: la única
   incursión invertida del juego (defender en lugar de entrar; puente directo a
   la sensibilidad azul).
   *Función del acto:* convertir curiosidad en causa; cada habilidad nueva abre
   literalmente una puerta del pasado.

**ACTO 3 — CONTINUIDAD**

10. **La Lista al alcance.** Dos usos posibles y un tercio negociable. Cadena de
    elecciones finales (§3.3).
11. **Confrontación con Vela.** No tiene por qué ser un jefe de combate: duelo
    de pruebas (camino azul), persecución (rojo) o mesa de negociación (mixto).
    El formato lo decide el karma acumulado.
12. **Final y epílogos.** Cada aliado cierra su arco con líneas reactivas a lo
    hecho, no a lo prometido (modelo Hades).
    *Función del acto:* cobrar las dos preguntas del juego — qué hacer con el
    Grid y qué hacer con un nombre que ya no existe.

### 2.6 Cómo se cose la trama (reglas operativas para Manus)

1. La trama vive en misiones, no en pantallas de texto. Cada encargo =
   objetivo técnico + beat narrativo + decisión de karma + gancho post-mortem.
   Sin barrera técnica superada no hay avance de historia (BRAINSTORM §5).
2. Morir SIEMPRE avanza. Cola de eventos con líneas nuevas por caso: primera
   muerte; repetición ante el mismo obstáculo (sube el tono y añade un dato,
   jamás repite literal); primer exploit de cada tipo; umbral de karma cruzado.
   Modelo Hades (GDC 2021, verificada en SKILLS-ANTISLOP).
3. El mundo reacciona a lo que acabas de hacer. Si el jugador soltó un `rm`
   recursivo, Ceniza comenta eso. Ninguna línea que pudiera aparecer en
   cualquier momento.
4. Contradicción controlada por acto (mecanismo Souls): mínimo un par
   «comunicado oficial ↔ evidencia física» contradictorio por acto. Ejemplo:
   el comunicado dice cero bajas en el incidente del Muelle; el grafiti del
   pasillo tres lista cinco nombres. El jugador decide a quién creer.
5. Ficha de voz obligatoria antes de escribir cualquier personaje (formato en
   SKILLS-ANTISLOP, capa 2, con la fila «nunca diría»). Test del nombre tapado.
6. Objetos de lore: dato técnico arriba, grieta humana abajo, un número
   concreto por descripción (hora, capacidad, fecha). Cero adjetivos
   atmosféricos.
7. Temas bajo la superficie — identidad como dato, deuda, luz como vigilancia,
   aprender como única salida — jamás enunciados por el narrador. Si un texto
   explica su tema, se corta.
8. Idioma: todo el texto del juego en español de España; comandos y salidas
   técnicas en su forma real (si el sistema real emite inglés, se emite inglés).

---

## 3. Caminos y finales — karma Blue/Red

### 3.1 Qué mueve la aguja

- **Dentro de las runs (micro):** qué haces con los datos civiles que cruzas
  (copiar, borrar, dejar); ir llamativo por botín extra con el coste de alertas;
  puertas traseras que dejas abiertas; credenciales de administradores que
  usas y devuelves — o no.
- **Entre runs (macro):** qué encargos tomas, a quién cuentas qué, cómo
  resuelves la grieta de Ceniza, si proteges o gastas a los Apagados.
- **Regla dura:** el karma NUNCA modifica el currículo ni la dificultad técnica.
  Azul y Rojo practican el mismo Linux con objetivos distintos (§6.5: misma
  materia, lentes defensa/ofensa). Ejemplo: un `chmod 600` sobre registros
  médicos sirve para blindarlos antes de extraer la prueba (azul) o para
  cifrarlos como palanca de negociación (rojo). El branching vive en la capa
  narrativa — contexto, textos, reacciones — nunca en el contenido pedagógico.
  Esto protege el presupuesto de contenidos y la integridad del aprendizaje;
  el Pase 3 se revisará contra esta regla.

### 3.2 Cómo se lee el karma (sin medidores morales)

Ningún popup «+5 azul»: eso es quiz-con-skin en versión ética. El estado se lee
en el mundo: los titulares del Hub cambian; los distritos se reparan o se
degradan a tu paso; Vela endurece o afila su discurso; los encargos que llegan
reflejan reputación — a un operador sangriento le ofrecen trabajos distintos.
El medidor existe internamente como variable serializable (guardado y tests),
pero no se dibuja como barra ética.

Deriva: pesan más las últimas N decisiones que el histórico. Redimirse cuesta;
traicionar es rápido. El valor exacto de N lo fija el Pase 2 con datos.

### 3.3 Finales (esbozo — condiciones exactas en P3/P5)

| Final | Condición | Qué pasa | Coste |
|---|---|---|---|
| **LUZ PLENA** (azul puro) | Prueba íntegra de la Lista y de las purgas, cadena de custodia construida con acciones azules consistentes | Sección no capturada del regulador abre juicio público; auditoría externa del Grid; Vela procesada. Tu nombre lo reconstruyes tú: el juego pide escribirlo | Se acaba la sombra que protegía a los Apagados; algunos pagan deudas viejas con la luz encendida |
| **NOCHE LARGA** (rojo puro) | Quemar el nodo maestro del censo | La Lista se dispersa irrecuperable; el Grid cae por zonas durante semanas; Vela te caza personalmente (persecución final); sobrevives borrándote hasta de los Apagados | El juego muestra con números lo que cuesta un apagón — hospitales incluidos. Sin moraleja |
| **EL TRATO** (umbral mixto + palanca) | Demostrar a Vela que su programa la incrimina (los logs del Auditor valen contra ella) | Las purgas se detienen; tú sigues sin existir; el sistema continúa, sin experimento | El final más gris: nada cambia para quien ya está a cero |
| **APAGÓN PROPIO** (secreto) | Todos los arcos de aliados resueltos + ningún umbral extremo + último fragmento encontrado | Entregas la Subestación a Zeta, borras a Cero, sales de Vesper en un carguero de los Muelles. El mundo queda como estaba | El único final donde el loop termina porque decides dejar de jugar |

Variante transversal — **HERENCIA**: si mueres en la misión final con karma
polarizado, los aliados ejecutan tu plan sin ti; epílogo póstumo. Barata de
producir (texto reutilizado) y muy Hades.

Presupuesto honesto: cuatro finales + una variante, no diez. La rejugabilidad
sale del loop, no de multiplicar contenido ramificado (juego objetivo 10–15 h).

### 3.4 Riesgos y salvaguardas del karma

- **Ramificación inflacionaria:** cada rama multiplica coste. Salvaguarda ya
  fijada en §3.1: rama solo en texto/contexto; el gameplay técnico es uno.
- **Moralina:** si un texto premia o castiga con adjetivos, se corta
  (checklist anti-slop).
- **Final azul ingenuo:** que el regulador esté parcialmente comprado debe verse
  ANTES (acto 2: el jugador ve quién paga a quién). Elegir la vía legal tiene
  que ser una decisión informada, no una trampa.
- **Karma invisible:** si el mundo no reacciona con suficiente contraste entre
  perfiles, el jugador no percibirá que sus decisiones importan. El Pase 4
  valida el contraste con runs headless del harness de Ornstein.

---

## 4. Decisiones abiertas (para P2/P3/P5/Juanma)

- ¿El nombre final del camino azul se teclea o Cero adopta definitivamente ese
  nombre? (afecta a §2.2 y al final LUZ PLENA)
- Arco del Auditor: ¿aliado a medias que libera el final secreto, o permanece
  instrumental? Recomendación: aliado a medias; se decide en P3.
- ¿Vela aparece en persona antes del asalto al Hub? Recomendación: solo voz y
  pantallas hasta entonces; su presencia gana por escasez.
- Contenido concreto del censo (qué se puntúa exactamente): necesita diseño de
  worldbuilding en P3 — es corazón temático y superficie principal de
  lore-items.
- Romance: fuera de alcance (coste). Relaciones por profundidad de diálogo,
  no por subsistema.

---

*Siguiente: **Pase 2** (11:00, 25/08) — loop roguelite Hades + dopamina Balatro.
Debe leer este pase y `RESEARCH-MECANICAS.md` §§2–4, y respetar §2.6 y §3.1.*
