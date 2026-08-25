# DESIGN — CyberRoot

> Documento vivo de diseño de Fase 0. Se construye en cinco pases:
> - Pase 1 — concepto, historia, plot general, caminos y finales. ✅
> - Pase 2 — loop roguelite Hades, karma operativo, sinergias y rejugabilidad. ✅
> - **PASE 3 (este)** — estructura de capítulos y niveles.
> - Pase 4 — dopamina fina y UX. 21:00 del 25/08.
> - Pase 5 — revisión final. 09:00 del 26/08.
>
> Marcos cerrados que este documento no discute: `AGENTS-PLAN.md` §6.5.
> Insumos: `docs/RESEARCH-MECANICAS.md` · `docs/INVESTIGACION-STACK.md` ·
> `docs/SKILLS-ANTISLOP.md` · `docs/BRAINSTORM.md`.
>
> Convención heredada del research: [HECHO] = verificable en fuente citada ·
> [OPINIÓN] = juicio de diseño nuestro · ⚠️ = aproximado o sin verificar a fondo.
> Las citas «RM §n» remiten a `RESEARCH-MECANICAS.md`.

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
diaria tenga espina fija; el corte en capítulos lo hizo el Pase 3 (§6).

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
  - Regla de mundo vuelta mecánica en el Pase 3 (§6.0): **más luz = más
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
- **Gris** — recadero y mercader (equipo y mejoras del espejo, §4.3). Cobra
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

> **Nota de Pase 2:** Gris vende el hardware (§4.3) y Zeta asigna los Pactos (§4.6);
> ambos papeles ya estaban plantados en la Pase 1 y ahora tienen función
> mecánica sin cambiar un rasgo de carácter.

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
   (aquí vive buena parte del currículo — estructurado en §6). Cada distrito aporta un
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
    elecciones finales (§3.4).
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
  Esto protege el presupuesto de contenidos y la integridad del aprendizaje.
  Revisado en el Pase 3: sin violaciones (§6.6).

### 3.2 Cómo se lee el karma (sin medidores morales)

Ningún popup «+5 azul»: eso es quiz-con-skin en versión ética. El estado se lee
en el mundo: los titulares del Hub cambian; los distritos se reparan o se
degradan a tu paso; Vela endurece o afila su discurso; los encargos que llegan
reflejan reputación — a un operador sangriento le ofrecen trabajos distintos.
El medidor existe internamente como variable serializable (guardado y tests),
pero no se dibuja como barra ética.

Deriva: pesan más las últimas N decisiones que el histórico. Redimirse cuesta;
traicionar es rápido. **Fijado en P2: N = 8.** Justificación: una incursión
genera 1–3 micro-decisiones con peso kármico y un encargo del Hub es otra; con
N = 8, las últimas dos o tres runs definen tu reputación presente sin borrar
del todo lo anterior. Es un valor inicial de diseño, no un dato: se calibra en
Fase 1 con el harness (Ornstein) midiendo cuántas runs limpias hacen falta para
que un operador sangriento reciba encargos azules otra vez. ⚠️ Sin evidencia
externa que cite aquí: es criterio propio, y así queda registrado.

### 3.3 Karma operativo

La Pase 1 definió qué mueve la aguja y cómo se lee. Falta el mecanismo exacto:
cómo se decide Blue/Red dentro y entre runs, y cómo llega eso al jugador sin
medidores morales.

**Contabilidad (invisible por diseño).** Cada decisión kármica escribe una
entrada `{momento, acción, peso, timestamp}`. El valor de karma es la suma
ponderada de las últimas 8 entradas (§3.2); positivo = azul, negativo = rojo.
Los umbrales que leen los sistemas (encargos que llegan, formato del final,
tono de Vela) son comparaciones contra ese valor; nada más. La variable existe,
es serializable y está testeada; no se dibuja nunca como barra ética (§3.2).

**Dentro de las runs (micro).** Los momentos kármicos viven donde ya hay
decisión técnica, no en eventos scriptados:

| Momento | Azul | Rojo |
|---|---|---|
| Datos civiles cruzados en la extracción | los borras antes de salir | los copias (palanca o botín) |
| Credencial admin comprometida | la rotas y registras el uso | la conservas para reutilizarla |
| Puerta trasera accesible | la cierras parcheando | la dejas abierta para volver |
| Logs que te delatan | los corriges dejando rastro mínimo | los quemas enteros |

La asimetría es intencional [OPINIÓN]: lo rojo siempre es lo fácil ahora y lo
caro después; lo azul exige un comando extra con coste de tiempo/alerta. Así
el karma mide prioridades reales bajo presión, no opiniones marcadas en un
diálogo. Y cada fila es también práctica curricular: rotar credenciales, hacer
`shred` de logs, cerrar permisos — el mismo Linux con lentes distintas, como
exige §3.1.

**Entre runs (macro).** Tres fuentes, todas diegéticas:
- **Encargos tintados.** Cada encargo de los Apagados nace azul, rojo o gris;
  el tinte es visible en la descripción del trabajo (quién pide qué), no en un
  icono moral. Aceptar suma poco; COMPLETAR suma según cómo lo resolvió el
  jugador (las micro-decisiones de la run mandan).
- **Decisiones de Hub.** A quién cuentas qué, cómo tratas la grieta de Ceniza
  (§2.5 beat 6), si vendes información a Gris. Diálogo con consecuencias
  serializadas, igual que las micro.
- **Reputación emergente.** El mundo ya reacciona (§3.2); esa reacción alimenta
  los encargos siguientes: un perfil rojo recibe ofertas más sucias, un perfil
  azul recibe filtraciones de denunciantes. Bucle de reputación auto-reforzante,
  barato de producir porque reutiliza el generador de encargos.

**Cómo se entera el jugador (sin medidor).** Cuatro canales, todos ya
previstos en §3.2, ahora con dueño mecánico:
1. **El mercado de Gris cambia de stock**: ofertas de hardware ofensivo
   aparecen para perfiles rojos; herramientas de auditoría y cifrado para
   azules. Nadie te dice «eres malo»: la tienda habla.
2. **El tono del Auditor** en el informe post-mortem: registra tu patrón («el
   Expediente 000 muestra preferencia por la destrucción de registros») con su
   precisión burocrática habitual.
3. **Los encargos que llegan** (ver arriba).
4. **Las reacciones de aliados** a hechos concretos, jamás a promesas (§2.6.3).

⚠️ Riesgo abierto que hereda §3.5: si estos cuatro canales no contrastan lo
suficiente entre perfiles, el jugador no percibirá agencia. La validación con
runs headless del harness (ya anotada en §3.5 para P4/P5) debe medir contraste
de stock de Gris y de cola de encargos entre un perfil azul forzado y uno rojo
forzado, no solo «textos distintos».

---
### 3.4 Finales (esbozo — condiciones exactas en P5; dónde se ganan, §6)

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

### 3.5 Riesgos y salvaguardas del karma

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

## 4. Estructura roguelite estilo Hades (Pase 2)

Todo lo que sigue concreta `AGENTS-PLAN.md` §6.5 sobre la evidencia de
`RESEARCH-MECANICAS.md`. Donde este doc dice algo distinto al research, manda
el research salvo decisión explícita aquí anotada.

### 4.1 El loop maestro

```
        ┌────────────────────────── SUBESTACIÓN (Hub) ◄─────────────┐
        │  post-mortem · historia · Espejo · tienda · encargos      │
        └──────────────┬────────────────────────────────────────────┘
                       │ eliges encargo + Pacto + equipo
                       ▼
   INCURSIÓN = run en una red generada (10–20 min)
   mapa de nodos → salas (explorar / firewall / datos / elite / evento)
   terminal real: cada comando es una acción con coste
                       │
        ┌──────────────┴───────────────┐
        ▼ ÉXITO                        ▼ DETECCIÓN (= muerte, nunca game over)
   extracción del botín           expulsión por el Auditor
   regreso con datos/créditos     pierdes el botín de la run; conservas:
   + fragmentos si los hubo       lecciones, créditos parciales,
        │                         unlocks y karma; la historia SIEMPRE avanza
        └────────────► vuelta al Hub ◄────────────────────────┘
```

Ciclos anidados (RM §2.2–2.3): comando (~segundos, tick de sala) → sala
(1–2 min) → run (10–20 min) → capítulo → acto. Siempre hay un contador cerca
de cerrarse: % de detección subiendo, combo activo, alerta del nodo.

**La muerte es el método de estudio** [HECHO RM §3.1–3.2]: Hades existe para
«quitarle el dolor a morir y reiniciar» (Kasavin); la narrativa avanza en cada
muerte con contenido nuevo. Traducción nuestra: cada expulsión dispara
post-mortem automático (§4.7), línea nueva del Auditor y avance del plot
(§2.6.2). El marco pedagógico ya estaba cerrado (§6.5.4: muerte = herramienta);
esto define el cómo.

### 4.2 Dos progresiones, y cuál manda

[OPINIÓN fuerte, heredada de RM §3.2] En Hades hay dos progresiones: la del
personaje (Espejo, keepsakes) y la del jugador (dominio real del gameplay).
En CyberRoot la segunda ES competencia Linux literal y no se pierde jamás.
Regla dura resultante: **el espejo in-game da conveniencia e identidad de
build, nunca conocimiento**. Ninguna compra del Hub sustituye a un comando que
el jugador no sabe usar; el espejo acelera, personaliza y exprime lo que ya
sabes hacer. Si el jugador llega al final sin haber aprendido, el juego ha
fallado aunque haya ganado.

### 4.3 Metaprogresión: el Espejo de Gris

El equivalente del Espejo de la Noche vive diegéticamente en la Subestación:
**el espejo de Gris**, paneles del equipo de Cero que se reescriben con
créditos y favores. Ramas iniciales (números ⚠️ orientativos, calibra harness):

| Rama | Qué da | Ejemplos |
|---|---|---|
| **Hardware** | ventajas físicas de equipo | más buffer de alertas, escáner previo de nodos |
| **Oficio** | comodidades de operación | historial de comandos entre salas, alias propios, 1 reintentos de sala |
| **Red** | acceso temprano a rutas | nodos extra visibles en el mapa, atajos entre anillos |

Coste doble (créditos de run + favores narrativos a Gris) para que la mejora
permanente también deje historia. Nada de esta tabla enseña ni sustituye
comandos: cumple la regla de §4.2. Los keepsakes-equivalentes son los
**recuerdos**: objetos ligados a NPCs (la libreta de Ceniza, la chapa de Zeta)
que sesgan qué boons aparecen en la próxima incursión — igual que en Hades
atanzas al dios cuyo boon quieres.

### 4.4 Boons de CONOCIMIENTO

El poder nuevo es saber nuevo (marco §6.5; RM §3.2 fila «boons»). Un boon
desbloquea una capacidad técnica REAL que el sandbox soporta desde el primer
día — desbloquear es progresión de personaje, saber usarlo es progresión de
jugador. Tres fuentes:

1. **Boons de currículo** — el comando nuevo del capítulo llega como momento
   de juego: aparece en un prompt de máquina comprometida, en el `history` de
   un admin descuidado o en las manos de un aliado; lo pruebas en esa run bajo
   necesidad (Bandit: objetivo primero, RM §1). Queda para siempre.
2. **Boons de hallazgo** — botín raro de run: scripts, flags de comandos,
   técnicas (`find -perm`, pipes con `tee`, variables de entorno). Entran al
   inventario de conocimiento y pueden salir en futuras runs.
3. **Boons de post-mortem** — tras ciertas expulsiones, Ceniza extrae del
   fallo una técnica anti-fracaso («eso te habría dado la salida»: `lsof`,
   `journalctl`). La lección nace del error concreto del jugador, no de un
   temario (regla §1.4: obstáculo primero).

Catálogo objetivo v0: ~60 comandos/techniques repartidos en familias —
navegación, permisos, texto/pipes, procesos, red, empaquetado, escalada,
auditoría/defensa. El reparto fino por capítulos está en §6.2; el Pase 4
define cómo se presenta cada uno (tarjeta de boon, juice, RM §2.3).

### 4.5 Generación procedural ENSEÑANTE

Directrices fijadas en RM §3.3; aquí su forma operativa:

- **Piel aleatoria, médula curricular** [RM §3.3.1]: nombres de ficheros,
  usuarios, IPs, puertos, topología del grafo y orden relativo de salas
  cambian por run; los CONCEPTOS que exige la sala los fija el currículo del
  capítulo. Consecuencia anti-walkthrough gratis: copiar una solución concreta
  no funciona dos veces (RM §1.3).
- **Muestreo por grafo de prerequisitos** [RM §3.3.2]: cada sala instancia
  conceptos ya dominados + exactamente 1 concepto nuevo o en práctica. El
  generador lee del mismo grafo que el currículo — una sola fuente de verdad,
  cero contenidos duplicados.
- **El RNG jamás decide si tu comando funciona** [regla dura, RM §3.3.3]:
  semántica determinista siempre. La incertidumbre vive en el mapa y en la
  vigilancia, nunca en la física del sandbox.
- **Contrato de generador (instanciado por campaña en §6.4):** entrada =
  {capítulo, Pacto activo,
  karma, boons del jugador, seed}; salida = grafo de salas + instancias de
  piel. Determinista ante la misma seed → testeable headless por el harness
  (INVESTIGACION-STACK: core sin motor, RNG seedeada).
- **Salida garantizada:** toda sala generada debe tener solución dentro de los
  comandos disponibles del jugador + validación automática (el generador
  resuelve su propia sala con una secuencia canónica antes de ofrecerla).
  Sala irresoluble = bug de generación, no reto.

### 4.6 El Pacto de Vela (Heat)

Sistema Heat estilo Hades para replay post-victoria, diegetizado como
**Pacto de Vela**: condiciones de endurecimiento que la propia Oficina impone
a sus sistemas tras tus ataques (subir sensibilidad, añadir tripulación de
auditoría, cifrar rutas). Cada condición sube el multiplicador de recompensa.
Zeta es quien te los propone y apuesta contigo — su papel ya anunciado en
§2.3. Restricción dura heredada de §3.1/§4.2: **ningún Pacto introduce
conceptos técnicos nuevos ni fuera de currículo**; endurecen lo conocido
(más permisos que revisar, menos tiempo de sesión, logs que rotan antes).
Sirve para rejugabilidad end-game y para que el harness tenga perfiles de
dificultad medibles.

### 4.7 El Hub: Subestación como casa de Zagreus

Orden de prioridades del Hub tras CADA run (éxito o expulsión):

1. **Post-mortem** (siempre, primero): informe del Auditor + análisis de
   Ceniza del último obstáculo; si hubo expulsión, lección concreta asociada
   (RM §3.3.4). Nunca se salta ni se hace opcional.
2. **Historia**: cola de eventos Hades (§2.6.2) — líneas nuevas de aliados,
   beats de encargo, fragmentos si tocan. Avanza SIEMPRE, éxito o no
   (RM §3.4: el avance narrativo constante es la vacuna contra la sensación
   de grind).
3. **Economía y build**: cobrar, gastar en Gris (equipo/espejo), elegir
   recuerdos, aceptar siguiente encargo y Pacto.
4. **Ambiente vivo**: titulares según karma (§3.2), estado de los distritos,
   barks cortos (SKILLS-ANTISLOP capa 2).

El Hub es pantalla con diálogos, no exploración libre de nivel 3D: presupuesto
de producción de un juego de 10–15 h (§3.4). Su vida viene de la cola de
eventos, no de la geografía.

---

## 5. Sinergias, variedad y rejugabilidad — el pilar Isaac de conocimiento (Pase 2)

> Tercer pilar pedido por Juanma (TODO 25/08): que boons, objetos y perks
> sinergien entre sí de forma chula y que la combinación dé variedad de runs,
> sin multiplicar contenido hasta lo inmanejable. Modelos de referencia:
> Balatro «encontrar sinergias entre modificadores» (RM §2.2.1) e Isaac
> «combinaciones de objetos que se disparan entre sí», adaptados a que la
> moneda es conocimiento real.

### 5.1 Principio rector: la sinergia nace de Unix

Regla de diseño nº1 del pilar: **toda sinergia debe existir primero en la
realidad de la terminal**. Unix YA es un sistema de combinación: pipes, xargs,
redirección, composición de filtros. No inventamos combinatoria encima; la
destilamos. Un boon combina con otro cuando sus comandos se encadenan con
sentido en un shell real. Consecuencias:

- Lo que el jugador descubre como sinergia mecánica (bonus numérico) coincide
  con lo que un profesional descubriría como buen hábito. El juego premia
  exactamente lo que transferiría.
- La sinergia es DESCUBRIBLE con criterio: quien sabe Unix puede intuir que
  `grep`+`sort`+`uniq -c` van juntos antes de ver el bonus. Nada de parejas
  arbitrarias tipo Isaac que solo funcionan porque el juego lo dice.
- Anti-patrón vetado: balanced-azar combinatorio sin significado (dos boons
  que dan +15% juntos «porque sí»). Eso sería dopamina hueca con skin de
  conocimiento — el antipatrón quiz-con-skin aplicado a builds (RM §1.3).

### 5.2 Tipos de sinergia (con ejemplos canónicos)

Los números son ilustrativos ⚠️; el balance fino es del Pase 4 con harness.
Lo normativo aquí son los TIPOS:

| Tipo | Mecánica | Ejemplo canónico | Por qué enseña |
|---|---|---|---|
| **Pipeline** | completar una cadena real de N comandos en una sala multiplica el botín | `grep` → `sort` → `uniq -c` seguidos: ×2 datos extraídos | la composición de filtros ES el hábito profesional |
| **Reconocimiento→ejecución** | haber usado un comando de reconocimiento en la misma run potencia al ejecutor | `find` usado antes ⇒ `rm`/`chmod` posteriores cuestan menos alerta | mirar antes de tocar: flujo real de intrusión |
| **Estado persistente** | dejar infraestructura en la run habilita acciones nuevas | backdoor dejado en sala 2 ⇒ en sala 5 puedes volver por él (atajo de ruta) | enseña qué implica realmente «dejar una puerta abierta» (y alimenta karma rojo, §3.3) |
| **Perk×boon** | un perk pasivo cambia las REGLAS de un boon | perk «alias»: encadenar el mismo par de comandos 3 veces crea un atajo permanente de esa run | los alias existen; recompensa automatizar lo repetido |
| **Objeto×comando** | objetos de Gris potencian categorías de comando | llave USB física: `dd`/copias extraen botín duplicado | conecta hardware real con su uso real |
| **Kármica** | el perfil Blue/Red modula qué sinergias brillan | perfil azul: auditoría+cifrado encadenados dan botín de prueba íntegra; perfil rojo: destructivas encadenadas dan velocidad | refuerza identidad de build sin partir el currículo (§3.1) |

Diseño de descubrimiento [OPINIÓN]: las sinergias NO se anuncian en menú
completo. Se muestran pistas diegéticas (Gris: «el `grep` y el `sort` se llevan
bien, como todo lo que filtra») y el primer disparo de cada sinergia tiene
juice propio (RM §2.3: feedback proporcional). Descubrirlas es parte del
contenido rejugable — y quien las descubre, aprendió el patrón Unix.

### 5.3 Variedad por combinación: la aritmética honesta

El criterio presupuestario ya fijado (§3.1, §3.3): variedad por COMBINACIÓN,
no por contenido ramificado caro. Aquí su aplicación al pilar:

**Superficies de variación de una run** (todas baratas, ninguna multiplica
texto):
1. Piel procedural (nombres/topología/puertos) — infinita, coste cero marginal.
2. Combinación de boons equipados (build del jugador).
3. Pacto elegido (modificadores de riesgo, §4.6).
4. Karma acumulado (qué encargos existen y cómo terminan, §3.3).
5. Recuerdos equipados (sesgo de drops).
6. Semilla y ruta del mapa de nodos.

**Presupuesto base para variedad real** [OPINIÓN con aritmética]:

- **~60 boons de conocimiento** (familias de §4.4), **~12 objetos de Gris**,
  **~8 perks pasivos**, **6–8 Pactos**, **4 finales + HERENCIA** (ya fijado
  §3.4).
- Combinaciones de builds: elegir 5 boons activos entre 60 ≈ C(60,5) ≈ 5,4 M;
  incluso exigiendo coherencia por familia, quedan decenas de miles. La
  limitación real no es el catálogo sino cuántas sinergias SIGNIFICATIVAS
  existen: objetivo v1 ≈ **25–35 sinergias diseñadas a mano** de los tipos de
  §5.2, cubriendo todas las familias. Eso son ~30 entradas de datos + juice
  compartido; coste comparable a 30 lore-items, no a 30 niveles.
- Contenido narrativo NO escala con las combinaciones: los textos reactivan
  por CLASE de evento (usaste pipeline, dejaste puerta, perfil cruzó umbral),
  no por combinación concreta (§2.6.3: el mundo reacciona a lo que hiciste,
  con plantillas por tipo). Una sinergia nueva no necesita diálogo nuevo.

⚠️ Orden de magnitud honesto: con estas cifras, dos jugadores con 20 runs
cada uno tendrán builds, rutas y encargos mayormente distintos pero verán
solaparse los textos de reacción. Eso es correcto y así se declara: la
variedad prometida vive en decisiones y builds, no en prosa única por run.
Multiplicar prosa sería el error de ramificación que §3.1 prohíbe.

### 5.4 Rejugabilidad por fases del jugador

- **Primeras runs (aprendiz):** variedad curricular — cada run trae concepto
  nuevo. La rejugabilidad aquí es la del propio aprendizaje.
- **Mid-game (operador):** variedad de build y ruta — boons, recuerdos,
  Pactos suaves, karma abriendo encargos distintos. Las sinergias empiezan a
  dispararse y crean objetivos propios («esta run quiero probar lo del tee»).
- **End-game (maestro):** Pactos de Vela duros (§4.6), caza de sinergias
  restantes, otros finales por karma, APAGÓN PROPIO como meta-logro (§3.4),
  ranking de estilo del harness (fluidez y pipelines puntúan, RM §3.4).
- **Post-victoria:** HERENCIA (§3.4) + Pactos + semillas daily-style para el
  comité de testeo (runs headless comparables por seed — INVESTIGACION-STACK).

Cascada de unlocks Balatro (RM §2.2.5) como colchón de todo: cada boon nuevo
desbloqueado crea combinaciones nuevas → objetivos nuevos → otra run. El
catálogo se desbloquea por logros de COMPETENCIA (usar bien X en contexto),
nunca por grind de créditos (RM §1.3: recompensas desacopladas de la
competencia corrompen la señal).

---

## 6. Capítulos y niveles — la campaña como currículo (Pase 3)

Este pase corta la historia en capítulos jugables y reparte el catálogo de
~60 boons (§4.4) entre ellos. El principio que lo gobierna todo es el mismo
de Bandit [HECHO RM §1]: **el aprendizaje nace de la NECESIDAD del objetivo** —
nunca de un temario ni de un cuestionario (antipatrón vetado, RM §1.3). Cada
capítulo existe porque la historia te obliga a entrar en sistemas que exigen
conceptos nuevos; el reto técnico SIEMPRE tiene solución con lo que sabes más
una pieza nueva (contrato de generador, §4.5).

### 6.0 Reglas estructurales

1. **El capítulo es campaña, no nivel.** No hay «nivel 1–10»: hay un distrito
   con encargos, beats del plot (§2.5), una puerta final narrativa y una
   familia técnica dominante. El generador instancia runs DENTRO del capítulo
   (entrada {capítulo, Pacto, karma, boons, seed}, §4.5); los conceptos que
   puede pedir cada sala salen del pool del capítulo.
2. **La luz es la curva de dificultad** (regla de mundo §2.1, ahora mecánica):
   cada anillo sube la línea base de vigilancia — % de detección por acción
   ruidosa, velocidad de respuesta del Auditor, rotación de logs. La
   progresión geográfica (Muelles → Umbral → Faro) ES la curva de
   dificultad, sin multiplicador artificial. El Pacto de Vela (§4.6) endurece
   encima para el end-game; jamás introduce conceptos nuevos.
3. **Prerrequisitos = llaves diegéticas.** El grafo de prerrequisitos (RM
   §3.3.2) se manifiesta como puertas físicas del Grid: un nodo que exige
   `sudo` no se abre «al llegar al capítulo 5», se abre cuando el jugador
   obtiene acceso (credencial robada, boon post-mortem de Ceniza). La puerta
   siempre es visible antes de tener la llave — la necesidad precede a la
   herramienta (directriz RM §1.4).
4. **Repetición espaciada disfrazada** (RM §1.2): ningún concepto se enseña y
   se abandona. Cada capítulo mantiene vivo el anterior: en el Faro sigues
   usando pipes y permisos, pero bajo presión mayor y combinados. La tabla de
   §6.2 marca cada familia como ENSEÑANZA (se introduce) o MANTENIMIENTO (se
   sigue practicando).
5. **Dimensionado** (⚠️ criterio propio, calibra harness): run típica
   10–20 min (§4.1); jugador medio completa la campaña en 12–14 h con
   ~45–60 incursiones y 25–35 expulsiones (la muerte es método de estudio,
   no pérdida). Con finales alternativos y Pactos: 15 h+. Los números por
   capítulo son objetivos de diseño v1, no contratos.

### 6.1 Los siete capítulos

Siete campañas ≈ tres actos (§2.5). Cada fila: qué te lleva allí (necesidad),
qué aprendes (familia dominante) y qué puerta deja abierta el final del
capítulo.

| # | Nombre | Anillo | Acto | Necesidad narrativa (por qué juegas) | Contenido | Fin de capítulo |
|---|---|---|---|---|---|---|
| 0 | **Trabajo en frío** | Umbral | 1 | Tu primer encargo legítimo: copiar unos datos (beat 1) | Tutorial sin teoría: `ls`/`cd`/`cat` aparecen POR NECESIDAD; 1 sala, 1 run guiada | Todo sale bien. La firma ya está puesta |
| 1 | **Los Muelles** | Muelles | 1 | Primeros encargos de los Apagados: pagar la cobertura con trabajo (beat 3); elegir azul o rojo (beat 4) | Shell y navegación; lectura de ficheros; permisos básicos (`chmod`, `chown`) como «quién puede tocar esto»; primer `man --help` por atasco | Control estable del nodo vecinal; primer fragmento personal |
| 2 | **Facturas** | Umbral bajo | 1→2 | Rastrear quién usó tu sesión exige cruzar registros de facturación (beat 5) | Texto y pipes: `grep`, `sort`, `uniq`, redirección; buscar en logs ajenos sin ser visto; aquí brillan las primeras sinergias pipeline (§5.2) | La pista lleva al censo; aparece la palabra Lista |
| 3 | **Bombas** | Umbral alto | 2 | Los nodos que necesitas están protegidos por procesos y sesiones ajenas | Procesos y sistema: `ps`, `kill`, señales, servicios, variables de entorno, empaquetado básico; primer uso serio de `sudo` (con credenciales ganadas) | Acceso a la red troncal; Ceniza confiesa (beat 6) |
| 4 | **Troncales** | Frontera Umbral/Faro | 2 | La Lista está detrás de la red troncal de Lumen | Red real: `ssh`, `scp`, túneles/puertos, `ss`, DNS interno, hosts; movimiento lateral entre máquinas — la skill firma del juego | Primera cámara del Programa de Continuidad (beat 7); Vela localiza la Subestación (beat 9) |
| 5 | **Subestación** | Muelles (invertido) | 2 | Asalto defensivo al Hub (única incursión al revés del juego) | Auditoría y defensa: leer logs ajenos, cerrar permisos, hardening mínimo, detectar movimientos — las lentes azules hechas nivel obligatorio (rojo lo juega igual: defender es defender) | Sobrevives al asalto; el coste queda escrito en el Hub |
| 6 | **Faro** | Anillo Faro | 3 | La cámara maestra del censo y la confrontación con Vela (beats 10–12) | Escalada y fin de juego: SUID/binarios privilegiados, cron, persistencia, cifrado con `openssl`/claves, limpieza de rastro — TODO lo anterior combinado bajo máxima luz | Final según karma (§3.4); epílogos |

Notas:
- El capítulo 0 NO es zona segura posterior: dura una run y desaparece como
  espacio. El Hub desde el minuto uno es la Subestación (menos fricción, más
  Hades).
- El capítulo 5 materializa el beat 9 y garantiza que TODO jugador practique
  defensa aunque su perfil sea rojo — coherente con §3.1 (misma materia,
  lentes distintas).
- Los fragmentos personales (botín raro, §2.2) caen en cualquier capítulo
  1–6 con probabilidad baja fija; su contenido se ordena por capítulo para no
  adelantar el misterio (decisión para Manus, §7).

### 6.2 Reparto curricular (~60 boons, familias de §4.4)

ENSEÑANZA = el capítulo lo presenta como boon de currículo (§4.4.1);
MANTENIMIENTO = reaparece en pools de práctica. Conteo orientativo ⚠️;
la lista comando a comando la cierra el equipo con el stack real soportado.

| Familia | Boons | Enseñanza | Mantenimiento |
|---|---|---|---|
| Navegación y ficheros (`ls`, `cd`, `cp`, `mv`, `find`) | ~8 | Cap. 0–1 | resto |
| Permisos y usuarios (`chmod`, `chown`, `whoami`, grupos) | ~7 | Cap. 1 | 3, 5, 6 |
| Texto y pipes (`grep`, `sort`, `uniq`, `wc`, `tee`) | ~9 | Cap. 2 | 3–6 |
| Procesos y sistema (`ps`, `kill`, `systemctl`, env) | ~8 | Cap. 3 | 4–6 |
| Red (`ssh`, `scp`, `ss`, túneles) | ~9 | Cap. 4 | 5, 6 |
| Auditoría/defensa (`journalctl`, `last`, hashes) | ~7 | Cap. 5 | 6 |
| Escalada y persistencia (SUID, cron, claves) | ~8 | Cap. 6 | post-victoria |
| Hallazgo (flags y técnicas transversales, §4.4.2) | ~4 | cualquier run | — |

Cobertura verificada contra §4.4: las ocho familias tienen dueño; ninguna
queda huérfana y ninguna se enseña dos veces. El capítulo con más carga nueva
es el 4 (red), deliberadamente el más largo en nº de encargos.

### 6.3 Dimensionado por capítulo (objetivo v1 ⚠️)

Números de diseño para calibrar con harness; suman ~50 encargos distintos
(más variación procedural infinita sobre ellos).

| # | Encargos (misiones) | Runs esperadas ⚠️ | Conceptos nuevos | Horas |
|---|---|---|---|---|
| 0 | 1 | 1 | 3 | 0,5 |
| 1 | 6–7 | 8–12 | ~8 | 2 |
| 2 | 7–8 | 8–12 | ~9 | 2 |
| 3 | 7–8 | 8–12 | ~8 | 2 |
| 4 | 9–10 | 10–14 | ~9 | 2,5 |
| 5 | 1 (asalto) + 2 preparatorios | 3–5 | ~7 | 1,5 |
| 6 | 6–8 + cadena final | 8–12 | ~8 | 2,5 |

Regla de avance: cada capítulo exige completar sus encargos CLAVE (los que
portan beats del plot, §2.6.1) y demuestra fluidez mínima en su familia
(p. ej., el 2 no cierra sin un pipeline limpio de 3 comandos). Los demás son
opcional-gratos (créditos, boons de hallazgo, karma). Nada de contador de
XP: la puerta siguiente se abre por competencia demostrada, jamás por grind
(RM §1.3).

### 6.4 Cómo encaja la generación procedural ENSEÑANTE

El generador (§4.5) recibe el capítulo como entrada y produce runs dentro de
estos márgenes:

1. **Un solo grafo de verdad.** El mismo DAG de conceptos alimenta currículo
   y generador: si la familia «procesos» se enseña en el capítulo 3, ninguna
   sala del capítulo 1 puede exigirla — el generador lo comprueba contra el
   pool desbloqueado del jugador, no contra una etiqueta de capítulo. Un
   jugador puede LLEGAR adelantado; nunca recibir un reto sin herramientas.
2. **Muestreo con sesgo pedagógico.** Pool de conceptos por sala =
   dominados (sesgo hacia los del capítulo en curso y los con menos
   prácticas recientes — repetición espaciada) + exactamente 1 en
   enseñanza/nuevo. La proporción dominados:nuevo roza 4:1 en capítulos
   tardíos y 1:1 en el primero (andamiaje decreciente).
3. **Salas tipo por familia** (heredan §4.1): explorar, firewall (reto de
   permisos/procesos), datos (reto de texto/red), elite (combinación de 2+
   familias), evento (historia/karma). La PLANTILLA es del capítulo; la
   INSTANCIA (piel, topología, nombres) de la seed. Copiar soluciones no
   funciona dos veces [HECHO RM §3.3.1].
4. **Validación canónica.** Toda sala instanciada se auto-resuelve con una
   secuencia canónica antes de ofrecerse (§4.5); irresoluble = bug. Además,
   el generador verifica que la solución canónica SOLO usa conceptos del
   pool permitido — test headless automático para Ornstein.
5. **Karma y Pacto no tocan el pool** (reglas §3.1 y §4.6): modifican
   presión, botín y textos. El capítulo 5 es la única excepción estructural
   del juego y está guionizada como campaña, no dejada al muestreo.

### 6.5 Qué NO cambia respecto a Pases 1–2

- El karma no parte el currículo (§3.1): revisado el reparto de §6.2, azul y
  rojo atraviesan los mismos siete capítulos con los mismos retos técnicos.
- La muerte sigue avanzando plot en TODOS los capítulos (§2.6.2): la cola de
  eventos tiene líneas reservadas por capítulo y por obstáculo.
- Presupuesto honesto (§3.4): 7 campañas × ~7 encargos ≈ 50 misiones base +
  variación procedural; nada de ramificar contenido por karma.

### 6.6 Huecos detectados y decisiones tomadas en este pase

1. **El beat 9 exigía un capítulo propio** — el asalto a la Subestación no
   cabía como «encargo más». Creado el capítulo 5 (defensivo, corto e
   intenso); garantiza práctica de auditoría a todo jugador.
2. **El capítulo 0 se separó del 1**: mezclar tutorial con el primer hub
   diluía ambas cosas. Duración mínima (media hora), cero teoría frontal.
3. **Red (cap. 4) es la familia más grande** tras texto/pipes: es la skill
   firma de la fantasía hacking y la que más transferencia da. Recibe el
   capítulo más largo.
4. **Censo**: el worldbuilding pendiente de §7 se necesita ANTES de escribir
   las salas-datos del cap. 6 (el censo es la superficie principal de lore
   ahí). Marcado bloqueante para producción de contenido, no para diseño.

---

## 7. Decisiones abiertas (para P4/P5/Juanma)

- ¿El nombre final del camino azul se teclea o Cero adopta definitivamente ese
  nombre? (afecta a §2.2 y al final LUZ PLENA)
- Arco del Auditor: ¿aliado a medias que libera el final secreto, o permanece
  instrumental? Recomendación: aliado a medias; decide P5.
- ¿Vela aparece en persona antes del asalto al Hub? Recomendación: solo voz y
  pantallas hasta entonces; su presencia gana por escasez.
- Contenido concreto del censo (qué se puntúa exactamente): worldbuilding
  pendiente — bloquea salas-dato del cap. 6 (§6.6.4), no el diseño.
- Romance: fuera de alcance (coste). Relaciones por profundidad de diálogo,
  no por subsistema.

Añadidas en Pase 2:

- N = 8 de deriva kármica (§3.2): valor inicial fijado sin evidencia externa;
  P5 lo revisa contra los datos del harness si existen.
- Créditos tras expulsión (§4.1): propuesta «parcial proporcional al progreso»
  pendiente de número; P4 la necesita para el balance de economía.
- Sinergias v1 = 25–35 diseñadas a mano (§5.3): lista concreta la escribe P4
  junto al balance numérico.

Añadidas en Pase 3:

- Orden de lectura de fragmentos personales (§6.1): ¿estrictamente por
  capítulo o por seed? Recomendación: orden fijo por capítulo (controla el
  ritmo del misterio H1/H2); la seed solo decide QUÉ piel de objeto recibe.
- ¿El cap. 5 admite Pacto? Por coherencia (es guionizada) recomiendo no;
  Zeta apuesta aparte. Decide P4 con economía.
- Los conteos de boons/familias de §6.2 son objetivo v0: la lista comando a
  comando debe validarla quien defina el sandbox real (stack), antes de P5.

---

*Siguiente: **Pase 4** (21:00, 25/08) — dopamina fina y UX. Debe leer este
pase entero (§6 le da la estructura de campañas sobre la que balancear) y
`RESEARCH-MECANICAS.md` §2 y §4. Respetar §3.1, §4.2, §4.5 y la checklist
de RM §5. Pendientes suyos con nombre: créditos parciales, lista de
sinergias v1, juice de boons, contraste kármico headless.*
