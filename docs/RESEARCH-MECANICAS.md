# RESEARCH MECÁNICAS — aprender sin deberes · dopamina Balatro · roguelite Hades · UX dual

> Fecha: 24/08/2026 · Agente: **Research Mecánicas + Dopamina** (Fase 0, Día 1)
> Estado: definitivo v1.0. Insumo directo para el Diseñador Jefe (P1–P5, 25–26/08).
> Los marcos cerrados por Juanma viven en `AGENTS-PLAN.md` §6.5; este doc los
> fundamenta con evidencia y los convierte en directrices accionables.
>
> Convención: **[HECHO]** = verificable en la fuente citada · **[OPINIÓN]** =
> juicio de diseño nuestro · **⚠️** = dudoso, aproximado o sin verificar a fondo.

---

## 0. Resumen ejecutivo (para el Diseñador)

1. El aprendizaje orgánico tiene un modelo probado: **objetivo primero, comando después** (Bandit). La lección nunca precede a la necesidad.
2. La dopamina de Balatro es **arquitectura de números**, no decoración: puntuación compuesta (base × multiplicador), bucles de 30–60 s, unlocks que alimentan la siguiente partida y *juice* en cada tick de cálculo. Todo eso se traslada literal a un roguelite de hacking.
3. Hades resuelve el problema pedagógico central del roguelite educativo: **la muerte como avance** (narrativa que progresa al morir + metaprogresión permanente). Nuestra versión: cada fallo deja una lección y el aprendizaje real del jugador ES la metaprogresión.
4. La generación procedural debe aleatorizar el **escenario** (nombres, puertos, topología) pero NO el **contenido pedagógico**: el concepto a practicar se fija por currículo, la piel varía.
5. UX dual validada por referencias: capa estratégica visual (mapa de nodos estilo Slay the Spire + HUD numérico pixel-art) sobre resolución táctica en terminal real. Las dos capas comparten un único canal de feedback.

---

## 1. Aprender sin parecer deberes

### 1.1 Referencias verificadas

**OverTheWire: Bandit** — https://overthewire.org/wargames/bandit/
[HECHO] Wargame por SSH "aimed at absolute beginners"; enseña lo básico necesario para jugar al resto de wargames. Cada nivel exige obtener la contraseña del siguiente explorando el sistema. La propia web avisa que parte de aprender es leer mucha documentación nueva.
- Lo que funciona [OPINIÓN respaldada]: motivación por necesidad pura — nadie te explica `grep`, lo necesitas *ya* para pasar de nivel. Herramienta real, entorno real. Su longevidad (referencia estándar desde hace más de una década) es la mejor prueba del modelo.
- Debilidades [OPINIÓN]: feedback mínimo (contraseña sí/no), cero mecánica de juego, y existe todo un ecosistema de walkthroughs que permite "resolver copiando" sin aprender — el antipatrón que CyberRoot debe impedir por diseño.

**Terminus (MIT, mprat)** — https://www.mprat.org/projects/terminus/ · https://github.com/mprat/Terminus
[HECHO] Aventura de texto que enseña comandos de terminal: el mundo ES un sistema de ficheros y las acciones SON comandos (`ls`, `cd`, `grep`…). Creada por dos estudiantes (MIT/UChicago).
- Lo que funciona [OPINIÓN]: demostró que envolver comandos en narrativa ("explora, rescata") baja la barrera de entrada a cero; el mapa mental del juego y el del filesystem coinciden.
- Debilidades [OPINIÓN]: catálogo corto de comandos y novedad de una sola sentada; proyecto esencialmente dormido ⚠️ (sin releases recientes). Lección: la envoltura narrativa sin bucle de recompensa sostenido no retiene.

**Root-Me** — https://www.root-me.org/ (descrita también en la plataforma europea de skills digitales: https://digital-skills-jobs.europa.eu/en/learning-space/resources/root-me-challenge-your-hacking-skills)
[HECHO] Plataforma de retos CTF (scripting, cripto, red, forense, web…) con puntos por reto, rankings y perfiles públicos.
- Lo que funciona [OPINIÓN]: demuestra que la capa extrínseca (puntos, ranking) engancha encima de retos reales; catálogo enorme como fuente de ideas de retos.
- Debilidades [OPINIÓN]: es una plataforma, no un juego — no hay loop narrativo ni progresión de personaje; pared de dificultad brutal para principiantes (asume Linux básico). CyberRoot cubre justo el hueco que Root-Me deja: del cero absoluto al nivel que Root-Me exige.

**Hacknet** (Team Fractal Alligator, 2015) — https://store.steampowered.com/app/365450/Hacknet/
[HECHO] Simulador comercial de hacking con interfaz de terminal ficticia, misiones guiadas por historia y estética muy alabada. ⚠️ Los detalles concretos (comandos simulados del "Hacknet OS", trama del admin muerto) son de memoria general, no re-verificados hoy.
- Lo que funciona [OPINIÓN]: es LA referencia del "sentirse hacker" — la fantasía vende la experiencia. Valida nuestra estética CRT/terminal.
- Debilidad crítica para nosotros [OPINIÓN]: los comandos son simulados e inventados → transferencia parcial a Linux real. CyberRoot usa comandos REALES precisamente para no pagar ese coste.

**Evidencia académica (game-based learning):**
- Clark, Tanner-Smith & Killingsworth (2016), *"Digital Games, Design, and Learning: A Systematic Review and Meta-Analysis"*, Review of Educational Research — [HECHO] meta-análisis de 69 estudios K-16: el aprendizaje con juegos digitales supera a condiciones sin juego con efecto positivo moderado-pequeño (g≈0.33 reportado en literatura secundaria ⚠️ cifra exacta por confirmar en el PDF); los análisis de moderadores muestran que **el efecto varía según características de diseño del juego**, no según el medio en sí. URLs: https://www.researchgate.net/publication/357301072 (resumen) · https://joanganzcooneycenter.org/2017/06/ (equipo Vanderbilt).
- Wouters et al. (2013), *Computers & Education* — [HECHO] meta-análisis previo de serious games: ganancias cognitivas Y motivacionales frente a instrucción convencional (g≈0.29 cognitivo ⚠️ de memoria, citar con cautela).
- Deterding et al. (2011) — [HECHO] definición canónica de *gamification*: "uso de elementos de diseño de juegos en contextos no lúdicos". Útil para nombrar el enemigo: gamificar un cuestionario ≠ juego.
- Ryan & Deci, Self-Determination Theory — [HECHO consolidado] motivación intrínseca florece con autonomía, competencia y relación. Marco útil: Bandit da autonomía+competencia; los cuestionarios con skin rara vez dan ninguna de las tres.
- ⚠️ No localizado hoy un estudio específico sobre "learn-by-need vs tutorial-first" en CLI: lo tratamos como principio de diseño bien respaldado por práctica (Bandit, Terminus, la propia documentación de Bandit sobre leer cuando hace falta), no como hecho experimental.

### 1.2 Qué funciona (síntesis)

| Principio | Evidencia | 
|---|---|
| Objetivo antes que herramienta (need-to-know) | Bandit; estructura de misiones de Hacknet |
| Herramientas reales en sandbox seguro → transferencia | Bandit/Root-Me usan sistemas reales |
| Feedback inmediato y sin ambigüedad | CTFs: flag correcta = validación instantánea |
| Narrativa como pegamento emocional | Terminus, Hacknet, Hades (§3) |
| Fallo = información, no castigo | Hades (§3); CTFs permiten reintento infinito |
| Curva de maestría con repetición espaciada disfrazada | Los conceptos reaparecen como herramientas, no como repaso |

### 1.3 Qué falla

- **Cuestionario con skin** [HECHO por definición Deterding + OPINIÓN]: puntos/badges encima de un quiz sigue siendo un quiz; la motivación extrínseca se desploma al retirarla. Es el antipatrón nº1 que el Diseñador debe vetar.
- **Tutoriales front-loaded**: muros de texto antes de jugar matan la autonomía (SDT). Bandit empieza en el nivel 0 con un objetivo y cero teoría.
- **Pared de dificultad sin andamiaje**: Root-Me filtra a principiantes; la secuencia de conceptos debe ser un grafo de prerequisitos explícito (§3.4).
- **Recompensas desacopladas de la competencia**: si el badge no certifica habilidad real, pierde valor y además corrompe la señal.
- **Resolver-copiando**: walkthroughs externos convierten Bandit en transcripción. En CyberRoot esto se mitiga con variación procedural (§3.4): copiar una solución concreta no funciona dos veces igual.

### 1.4 Directrices para CyberRoot

1. Toda lección nace de un obstáculo de misión, jamás de una pantalla de texto previa [directriz].
2. Comandos reales en sandbox real (contenedor/jaula), nunca sintaxis inventada estilo Hacknet [decisión coherente con BRAINSTORM §7 y stack].
3. La ayuda contextual aparece tras el primer fallo concreto, no antes (just-in-time) [directriz].
4. Cada misión valida COMPETENCIA (el objetivo técnico), no memorización; los rewards in-game certifican que lo hiciste [directriz].

---

## 2. Dopamina tipo Balatro

### 2.1 Qué hace Balatro realmente (hechos verificados)

[HECHO] Balatro (LocalThunk/Playstack, 02/2024) es un roguelike de póker: manos con valor base, Jokers que modifican reglas, y umbrales de puntuación por ciega. Análisis de diseño consultados hoy:

- **Feedback jugoso como diferencia entre hoja de cálculo y máquina de dopamina**: "The entire experience gap between 'spreadsheet' and 'dopamine machine' is bridged by feedback design" — https://blakecrosley.com/guides/design/balatro . Detalla: la puntuación es base × mult que escala en cadena, y cada paso del cálculo se ANIMA por separado.
- **Bucles de feedback de alta densidad**: "high-density feedback loops and meticulously polished operational details" — https://medium.com/@yyh19971004/balatro-design-analysis-visual-packaging-and-interactive-feedback-cc6fa6a65370 . Cada acción (jugar carta, activar Joker, sumar chips) dispara respuesta audiovisual en <1 s.
- **"Numbers go up" como gancho reconocido**: Metacritic destaca "a continuous flow of numbers-go-up dopamine hits" — https://www.metacritic.com/game/balatro/ .
- **Metaprogresión que alimenta cada run**: los desbloqueos (Jokers, mazos) llegan por objetivos concretos y "fuel each run" — https://skyboxcritics.com/2025/05/01/balatro-the-numbers-game/ .
- Ventas >5M según Playstack (inicios 2025) ⚠️ de memoria, no re-verificado hoy.

**Teoría de juice** [HECHO]: charla *"Juice it or lose it"* (Martin Jonasson & Petri Purho, 2012) — definición operativa: "A juicy game feels alive and responds to everything you do, tons of cascading action and response for minimal user input". Demo en vivo: Breakout aburrido → irresistible añadiendo flash, shake, partículas y sonido. URL: https://www.youtube.com/watch?v=Fy0aCDmgnxg (transcripción/citas en https://www.cs.cornell.edu/courses/cs4154/2015fa/sessions/lecture14.pdf ).

**Nota honesta sobre "dopamina"** [OPINIÓN]: es taquillera, no técnica. Lo que la psicología describe es refuerzo intermitente variable (schedules de Skinner) y señales de *wanting* (Berridge). Para diseño basta la traducción práctica: **recompensas frecuentes, visibles, crecientes y a veces sorprendentes**. No hace falta neurociencia para aplicar esto.

### 2.2 Descomposición: las 5 palancas de Balatro

1. **Puntuación compuesta** — número base × multiplicador: dos palancas separadas que el jugador aprende a escalar. El interés no es el valor absoluto sino ENCONTRAR SINERGIAS entre modificadores.
2. **Ciclos cortísimos** — mano (~10 s) → ciega (~1–2 min) → ante (~5 min): siempre hay un contador a punto de cerrarse cerca.
3. **Juice escalado al significado** — shake/partículas/pitch suben CON el número: el feedback codifica magnitud, no solo éxito/fallo.
4. **Economía de riesgo** — rerolls, dinero por intereses, saltarse recompensas pequeñas por mayores: decisiones de apuesta constantes.
5. **Cascadas de desbloqueo** — cada unlock crea nuevas combinaciones → nuevos objetivos → nuevas runs.

### 2.3 Traducción a CyberRoot (menú de mecánicas para el Diseñador)

| Palanca Balatro | Mecánica CyberRoot propuesta |
|---|---|
| Chips × Mult | **Datos × Combo**: cada acción correcta suma "datos extraídos"; el multiplicador de combo sube por acciones consecutivas sin error/detección y cae (no se resetea a 1, baja un nivel) al equivocarte |
| Ciclos cortos | **Tick de sala** (cada comando = pulso) → **sala** (1–2 min) → **run/nodo** (5–15 min) → **incursión completa** |
| Juice proporcional | Shake de HUD, flash CRT, pitch de bleeps y tamaño de números escalan con el multiplicador; un hallazgo crítico (flag/root) rompe el layout momentáneamente |
| Riesgo/recompensa | Rutas ruidosas con más botín vs sigilo lento; "deep scan" que duplica loot pero suma % detección; cobrar el botín ya conseguido o seguir profundizando |
| Cascadas de unlocks | Cada comando nuevo dominado habilita builds/synergias (p.ej. `grep`+`cat` encadenados dan bonus de fluidez); el bestiario de servicios crece |

Regla de oro anti-ruido [OPINIÓN]: el juice debe codificar INFORMACIÓN (magnitud, tipo de evento), no decorar. Si todo brilla igual, nada brilla. Y el ruido nunca puede tapar la salida de la terminal: legibilidad > espectáculo (riesgo de fuente bitmap ya anotado por Research Stack).

Anti-patrón a vigilar [OPINIÓN]: dopamina sin aprendizaje produce retención sin transferencia (jugón que no sabe `chmod`). Por eso cada palanca numérica queda amarrada a un evento de competencia REAL (un comando correcto, un pipeline bien encadenado), nunca a azar puro.

---

## 3. Roguelite estilo Hades

### 3.1 Qué dice Hades (hechos verificados)

- [HECHO] Objetivo explícito de desarrollo: "take the pain out of dying and having to restart" (Greg Kasavin, director creativo) — https://www.gamedeveloper.com/design/how-supergiant-weaves-narrative-rewards-into-i-hades-i-cycle-of-perpetual-death .
- [HECHO] La narrativa avanza en CADA muerte con diálogos nuevos en cola; Kasavin lo compara con rebobinar un capítulo y encontrar contenido nuevo — https://www.inlander.com/culture/hades-writer-greg-kasavin-on-how-he-made-video-game-deaths-drive-a-feel-good-story-22725237 .
- [HECHO] A diferencia de roguelikes con permadeath total, la historia persiste y evoluciona entre runs — https://www.gameshub.com/news/features/hades-greg-kasavin-breaks-down-supergiants-unique-approach-to-narrative-262459-2193/ .
- [HECHO, conocimiento estable] Sistemas de metaprogresión permanentes (Espejo de la Noche con Oscuridad, recuerdos/keepsakes, aspectos de armas), boons de dioses como modificadores de run con sinergias, cámaras diseñadas cosidas proceduralmente, y sistema Heat/Pacto para replay tras la victoria. ⚠️ Detalle fino de números no verificado hoy; suficiente a este nivel de diseño.

### 3.2 El loop traducido a enseñanza de Linux

| Hades | CyberRoot | Función pedagógica |
|---|---|---|
| Run (escapar del inframundo) | Incursión en una red generada | Práctica situada bajo presión |
| Muerte → Casa de Hades | Te detectan → expulsión → Hub | El fallo NO borra progreso: reframe del error como parte del ciclo |
| Diálogo nuevo tras cada muerte | Post-mortem en el Hub: qué falló + lección + pista | Cada derrota deja una lección concreta (muerte = herramienta pedagógica, marco cerrado §6.5.4) |
| Espejo de la Noche | Mejoras permanentes del equipo/perfil | Metaprogresión in-game |
| Boons de dioses | Boons de CONOCIMIENTO: comandos/exploits/perks nuevos | El poder nuevo ES saber nuevo |
| Caminos/armamentos → finales | Karma Blue/Red → arcos y finales | Misma materia (Linux) con lentes defensa/ofensa |

**La clave estructural** [OPINIÓN fuerte]: en Hades hay DOS progresiones (la del personaje: espejo/recursos; y la del jugador: dominio del gameplay). En CyberRoot la del jugador es literalmente su competencia en Linux — y esa NUNCA se pierde al morir. El espejo in-game debe ser conveniencia (acelerar, personalizar), no sustituto: si das power fantasy sin competencia, el jugador llega al muro final sin haber aprendido y abandona. El aprendizaje real es la metaprogresión definitiva; el resto es azúcar.

### 3.3 Generación procedural ENSEÑANTE

Principios derivados (para el Diseñador P2):

1. **Aleatoriza la PIEL, fija la MÉDULA** [directriz]: nombres de ficheros, IPs, puertos, servicios, usuarios y topología cambian por run; el concepto a practicar (permisos, pipes, grep, ssh…) lo decide el CURRÍCULO del capítulo, no el RNG. Así la variedad mata el "resolver copiando" sin tocar el objetivo pedagógico.
2. **Generación dirigida por grafo de prerequisitos** [directriz]: cada sala/run se instancia muestreando del grafo de conceptos (navegación → permisos → procesos → red → escalada…), garantizando que la sala practicable exija SOLO conceptos ya desbloqueados + 1 concepto nuevo como reto. Esto implementa "andamiaje" (ZPD) sin tutoriales.
3. **El RNG nunca decide si tu comando funciona** [regla dura]: la semántica de los comandos es determinista; la incertidumbre vive en el mapa (qué hay detrás de cada nodo, guardias/trampas), como en Hades las cámaras varían pero las mecánicas son estables.
4. **Post-mortem automático como lección** [directriz]: al morir, el sistema identifica el último obstáculo y genera la pista/lección asociada en el Hub. La muerte tiene SIEMPRE lectura pedagógica (marco §6.5.4).
5. ⚠️ Lectura de fondo opcional: PCG académico (Togelius et al., search-based PCG 2011; Summerville et al., PCGML 2018) — contexto general, NO aplicado directamente aquí; nuestro generador es de plantillas con parámetros + grafo curricular, mucho más simple.

### 3.4 Riesgos del género para educación (y mitigaciones)

- Frustración por dificultad → Hades ya lo resolvió: modo Dios (facilidad progresiva invisible). Equivalente: ajustar tiempo de detección, no bajar contenido técnico. [OPINIÓN]
- Sensación de grind si el Hub exige repetición → que el avance narrativo llegue SIEMPRE tras cada run, exitosa o no (fórmula Hades). [OPINIÓN respaldada en §3.1]
- Optimizar la build en vez de aprender → puntuar la COMPETENCIA (fluidez, pipelines, sin errores) por encima del botín acumulado. [OPINIÓN]

---

## 4. UX: dos capas (pixel-art visual + terminal real)

### 4.1 Por qué necesita mapa de nodos

[HECHO] El mapa de nodos ramificado como columna vertebral de run fue popularizado por Slay the Spire (Mega Crit, 2019): el jugador ve el grafo, evalúa rutas por riesgo/recompensa y planifica. Hades usa cámaras encadenadas con bifurcaciones ocasionales — menos mapa, más flujo.
[OPINIÓN] Para CyberRoot, el mapa cumple tres funciones a la vez: (1) decisión estratégica de ruta (dopamine de planear), (2) representación literal de una RED (diegetic: es un diagrama de red hackeable — el mapa ES diegesis), (3) contenedor de la progresión del capítulo. Recomendación: nodos visibles con tipo de sala insinuado (loot/guardia/datos), como STS muestra élites/tiendas — información imperfecta que crea decisiones.

### 4.2 Por qué HUD visual + feedback numérico

[HECHO+OPINIÓN] Todo el gancho Balatro (§2.2) requiere superficie visible constante: combo/mult, recursos, % detección, timers. Un prompt de terminal pelado no puede mostrar nada de eso sin ensuciar la línea de comandos. El HUD pixel-art (Pyxel, paleta CRT — ver `docs/INVESTIGACION-STACK.md`) lleva los números; la terminal queda LIMPIA para trabajar. Además el HUD es el canal donde el juice escala (shake/flash por magnitud).

### 4.3 Por qué la resolución en terminal real

- Autenticidad y transferencia: Bandit demuestra que comandos reales enseñan mejor (§1.1); Hacknet demuestra el coste de fingirlos (§1.1).
- Fantasía: "de verdad pareces un hacker" (BRAINSTORM §4) — escribir comandos reales ES la fantasía cumplida, no simulada.
- Testeo autónomo: la lógica de terminal vive en `core/` (sin pyxel) testeable headless (INVESTIGACION-STACK, reglas de frontera). [HECHO]

### 4.4 Cómo combinar las capas (propuesta de integración)

1. **Un estado, dos renderizadores** [directriz arquitectónica]: el core emite eventos (comando_ok, dato_extraído, alerta_subida…) y la capa visual (mapa, HUD, animaciones) y la capa terminal (texto, colores ANSI) consumen LOS MISMOS eventos. El juice no es cosmética: es el mismo dato visto dos veces.
2. **Modos de foco claros** [directriz]: en modo MAPA el teclado navegra/equipa; al entrar en sala, foco total en terminal; ESC vuelve al mapa. Nunca mezclar input de navegación y de comandos.
3. **Puentes de feedback cruzado** [directriz]: un comando correcto pulsa el nodo actual + suma al combo del HUD; una alerta tiñe el mapa. El jugador percibe UNA pantalla viva, no dos apps pegadas.
4. **Legibilidad primero** [regla dura]: la terminal in-game usa fuente bitmap validada (tarea `[PENDIENTE]` en TODO — bloqueante para el Diseñador P4). Si la fuente no se lee, se cambia de fuente antes que sacrificar texto.
5. **La estética CRT nace de la restricción** [OPINIÓN]: 16 colores de Pyxel + scanlines + verde/ámbar dan coherencia gratis; el pixel-art no decora, unifica.

---

## 5. Directrices consolidadas para el Diseñador Jefe (checklist)

1. Obstáculo primero, lección después; ayuda just-in-time tras el primer fallo. (§1.4)
2. Vetar todo patrón quiz-con-skin; toda recompensa certifica competencia técnica real. (§1.3)
3. Puntuación compuesta (datos × combo) + ciclos cortos + juice proporcional a magnitud. (§2.2–2.3)
4. Loop Hades completo: run → expulsión → Hub (historia + post-mortem + mejoras) → run; la muerte deja lección SIEMPRE. (§3.2)
5. Metaprogresión dual: in-game (espejo) y la REAL del jugador (su Linux); el espejo nunca sustituye saber. (§3.2)
6. Procedural: piel aleatoria, médula curricular; RNG jamás decide semántica de comandos. (§3.3)
7. Mapa de nodos diegético con información imperfecta; HUD numérico persistente; terminal limpia. (§4.1–4.2)
8. Eventos compartidos core→(HUD|terminal); modos de foco separados; legibilidad > espectáculo. (§4.4)

## 6. Fuentes

**Juegos/plataformas:** OverTheWire Bandit (https://overthewire.org/wargames/bandit/) · Terminus (https://www.mprat.org/projects/terminus/, https://github.com/mprat/Terminus) · Root-Me (https://www.root-me.org/, https://digital-skills-jobs.europa.eu/en/learning-space/resources/root-me-challenge-your-hacking-skills) · Hacknet (https://store.steampowered.com/app/365450/Hacknet/)
**Diseño/dopamina:** Blake Crosley, *Balatro: Juicy Feedback* (https://blakecrosley.com/guides/design/balatro) · Análisis Medium (https://medium.com/@yyh19971004/balatro-design-analysis-visual-packaging-and-interactive-feedback-cc6fa6a65370) · Metacritic Balatro (https://www.metacritic.com/game/balatro/) · Skybox, *The numbers game* (https://skyboxcritics.com/2025/05/01/balatro-the-numbers-game/) · *Juice it or lose it* (https://www.youtube.com/watch?v=Fy0aCDmgnxg; notas Cornell: https://www.cs.cornell.edu/courses/cs4154/2015fa/sessions/lecture14.pdf)
**Hades:** Game Developer (https://www.gamedeveloper.com/design/how-supergiant-weaves-narrative-rewards-into-i-hades-i-cycle-of-perpetual-death) · Inlander/Kasavin (https://www.inlander.com/culture/hades-writer-greg-kasavin-on-how-he-made-video-game-deaths-drive-a-feel-good-story-22725237) · GamesHub (https://www.gameshub.com/news/features/hades-greg-kasavin-breaks-down-supergiants-unique-approach-to-narrative-262459-2193/)
**Académico:** Clark, Tanner-Smith & Killingsworth 2016 (ResearchGate: https://www.researchgate.net/publication/357301072; Joan Ganz Cooney Center: https://joanganzcooneycenter.org/2017/06/) · Wouters et al. 2013 ⚠️ citado de memoria · Deterding et al. 2011 (definición de gamificación) · Ryan & Deci (SDT)

---
*Próximo consumidor: Diseñador P1 (11:00, 25/08) para concepto/historia; P2 (16:00, 25/08) para el loop roguelite; P4 (14:00, 26/08) para dopamina/UX. Este doc no sustituye a DESIGN.md: lo alimenta.*
