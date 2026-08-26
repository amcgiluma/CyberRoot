# TESTEO-DIARIO — Protocolo de testeo del Concilio (CyberRoot)

> Creado por el Diseñador Jefe P5 (Fase 0, 26/08) con tres perfiles; ampliado
> ese mismo día a **cuatro perfiles** para integrar a **Oscar de Astora
> (05:00)**, guardián de la experiencia. Lo leen SIEMPRE antes de su turno:
> **Oscar**, **Havel**, **Artorias** y **Gwyn** (y Gwyndolin, que consume sus
> hallazgos). Complementa `docs/AGENTES-PLAN.md` §2.5 (protocolo de
> comunicación); aquí se define solo la CAPA DE TESTEO: quién prueba qué,
> cuándo y dónde deja la huella.

---

## 0. El principio: cuatro preguntas distintas

El juego necesita cuatro miradas que no se pisen. Cada perfil responde UNA
pregunta sobre el mismo repo, en turnos distintos del día:

| Hora | Agente | Pregunta | Capa |
|---|---|---|---|
| 05:00 | **Oscar** | «¿Es apto el camino para un jugador de cero?» | **La experiencia/progresión**: run de referencia desde SAVE LIMPIO + veterano (20+ h), mantiene `docs/ESTADO-JUGADOR.md` |
| 07:00 | **Havel** | «¿Funciona? ¿Mola?» | **La novedad + conjunto**: lo nuevo por `git log` + smoke del conjunto |
| 21:00 | **Artorias** | «¿Está bien hecho?» | **El ingeniero**: tests, lint y smoke técnico de cada PR |
| 23:00 | **Gwyn** | «¿Es buen juego?» | **El director**: diseño, sabor y coherencia en conjunto; decide la zona 🔬 |

La división es por CAPA, no por módulo: los cuatro pueden tocar el mismo
código el mismo día y aun así no repetir trabajo, porque uno mide la
experiencia completa desde cero, otro juega la novedad, otro verifica y el
último juzga. Si dos encuentran el mismo fallo, no es solape: Havel describe
el SÍNTOMA («al entrar en la sala 3 se cuelga»), Artorias localiza la CAUSA
(«el parser de ese tipo de sala lanza excepción en X»). Síntoma y causa son
aportaciones distintas; Oscar añade la tercera mirada: el VIAJE (dónde se
rompe la progresión de un jugador real a lo largo del tiempo).

**Reparto explícito del save limpio (evita la colisión clásica):**
- **Oscar es el dueño del SAVE LIMPIO**: su run de referencia parte SIEMPRE
  de una partida nueva de cero (reset vía harness si existe) y mide el viaje
  completo del jugador novato.
- **Havel ya NO repite el save limpio**: su capa empieza en lo nuevo del
  `git log` y cierra con un smoke del CONJUNTO que solo verifica que el juego
  ENTERO sigue arrancando y avanzando — no revalida el camino de cero, eso ya
  lo midió Oscar dos horas antes.

## 1. Oscar, 05:00 — el guardián de la experiencia

**Qué hace, en orden:**

1. **Lee la zona de ayer** (§4): Gwyn dejó a las 23:00 la zona 🔬 para HOY;
   Oscar es el PRIMERO que la ejecuta.
2. **Run de referencia desde SAVE LIMPIO** (timebox principal): partida nueva
   de cero (reset vía `tools/playtest/` si existe, o manualmente) y avanzar
   por el camino real del jugador hasta donde llegue hoy. Constata DÓNDE se
   rompe el viaje: un comando antiguo que ya no funciona, un ritmo que cae,
   un nodo sin sentido.
3. **Perspectiva de VETERANO (20+ h)**: save avanzado y evalúa la progresión
   a largo plazo: ¿el loop engancha en la run 30? ¿la Base/Hub sigue
   coherente? ¿karma, dificultad y textos aguantan cuando ya no eres novato?
4. **Mantiene `docs/ESTADO-JUGADOR.md` vivo**: qué es jugable HOY de
   principio a fin, qué falta, estado del progreso largo. Es el puente entre
   DESIGN.md (lo que será) y el código (lo que es).
5. **Deja huella**: hallazgos como `[BUG]` en `backlog/TODO.md`; ajustes de
   dirección como NOTAS DE DIRECCIÓN para Gwyn en la sección «🎯 Notas de los
   revisores» (informa, no decide). Su worklog cierra con el CICLO (§6).

Su filtro es «¿es apto el camino para un jugador de cero?». NO genera ideas
de contenido (capa de Havel), NO valida código (Artorias) ni decide diseño
(Gwyn): propone dirección y deja que Gwyn decida.

## 2. Havel, 07:00 — el jugador de la novedad

**Qué hace, en orden:**

1. **Lee la zona de hoy** en `backlog/TODO.md`, bloque «🔬 Testeo de
   mañana» (lo dejó Gwyn a las 23:00, §4; Oscar ya la habrá ejercitado por la
   mañana). Ahí sabe qué priorizar SIN testear a ciegas.
2. **Detecta lo nuevo**: `git pull` y luego
   `git log --oneline --since="24 hours ago"` para ver qué entró mergeado
   desde su último turno. Eso define «lo nuevo» — nada más, nada menos.
3. **Juega lo nuevo** (timebox 15–20 min): la zona marcada por Gwyn, con
   manos de jugador. Si aún no hay build gráfica, ejerce lo que exista
   (core headless, seeds del harness, flujos por terminal) igual que lo
   jugaría un humano.
4. **Smoke del CONJUNTO (SIN save limpio)**: una pasada rápida por el camino
   real para confirmar que el juego ENTERO sigue arrancando y avanzando. NO
   rehace la run de referencia de cero — esa capa es de Oscar (§1); el smoke
   de Havel solo comprueba que nada quedó roto a nivel de arranque/avance.
   Lo nuevo puede ser brillante y aun así haber roto el arranque: eso lo
   caza el smoke, no la zona.
5. **Deja huella en `backlog/TODO.md`**: cada fallo como
   `[BUG] <dónde> <pasos mínimos para reproducir>`; cada idea como
   `[PENDIENTE]` (su rol creativo habitual, AGENTES.md).

Su filtro es «¿funciona? ¿mola?». NO revisa PRs ni código (capa de
Artorias), NO valora coherencia narrativa ni dirección (capa de Gwyn) y NO
mide la progresión larga ni el camino de cero (capa de Oscar).
Si algo no le mola pero funciona, lo apunta como idea/nota, no como bug.

## 3. Artorias, 21:00 — el ingeniero

**Qué hace, en orden:**

1. **Lista las ramas/PRs del día**: `git branch -a` + `gh pr list`.
   Incluye huérfanas viejas (regla del planificador, AGENTS-PLAN §4).
2. **Por cada PR, verificación técnica**: `pytest tests/core/` (headless),
   lint, y un smoke de juego MÍNIMO pero REAL (arrancar, completar un ciclo
   de sala, salir limpio). No basta con que compile.
3. **Marca 💥/✅ en `backlog/TODO.md`** con comentario accionable; un
   rechazo dice POR QUÉ y CÓMO arreglar (formato AGENTS-PLAN §4).
4. **Cruza con los bugs de la mañana**: si un `[BUG]` de Havel u Oscar tiene
   la causa en un PR de hoy, lo nombra en su veredicto para que el ejecutor
   lo arregle PRIMERO mañana (prioridad máxima ya fijada en AGENTS-PLAN).

Su filtro es «¿está bien hecho?». NO opina de gusto ni de diseño: eso
viaja a Gwyn como nota, no como veredicto.

## 3bis. Gwyn, 23:00 — el director

> *(Numeración heredada de la versión de 3 perfiles: las secciones 1–2 son
> Oscar y Havel, la 3 es Artorias y aquí va Gwyn.)*

**Qué hace, en orden:**

1. **Valida diseño y sabor en conjunto**: ¿lo mergeado hoy sigue
   `docs/DESIGN.md`? ¿la experiencia avanza hacia el juego descrito en su
   §10 (resumen ejecutivo)? ¿los textos cumplen SKILLS-ANTISLOP?
2. **Coherencia narrativa**: lee la producción del día de Manus contra los
   beats del plot y las fichas de voz. Es la ÚNICA capa que juzga esto.
   Además, integra (o descarta con razón) las NOTAS DE DIRECCIÓN de Oscar:
   informan su validación y sus decisiones de merge.
3. **Merge final** (solo él mergea, cadena AGENTS-PLAN §4).
4. **Decide LA ZONA DE TESTEO DE MAÑANA** y la deja en `backlog/TODO.md`
   (§4 abajo). Nadie mejor que él sabe qué entró hoy y qué es crítico: es
   quien cierra el círculo para que OSCAR (primero) y HAVEL (después) no
   prueben a ciegas.
5. Reporte a Juanma (Telegram) agregando el estado del ciclo de los cuatro
   perfiles (§6).

Su filtro es «¿es buen juego?». NO depura: si necesita localizar una causa,
lo pide en su nota para Artorias/ejecutores (puede delegar en sub-agentes).

---

## 4. La ZONA de testeo: el relevo Gwyn → Oscar → Havel ⭐

Es la pieza que evita que los cuatro prueben lo mismo o que la mañana se
pierda. Gwyn la escribe AL CIERRE (tras mergear, cuando ya sabe qué entró);
**Oscar la lee AL ABRIR (05:00, primero)** y la ejercita con ojos de
experiencia; **Havel la continúa AL SEGUIR (07:00)** con ojos de novedad.
Formato exacto, máximo ~6 líneas:

```
## 🔬 Testeo de mañana (<fecha>)
Zona prioritaria: <módulo/sistema/flujo>
- <qué probar primero, y por qué (1 línea)>
- <segunda prioridad, si la hay>
- Smoke: <qué debe seguir funcionando sí o sí aunque lo nuevo falle>
Contexto: <qué entró hoy que justifica esta zona>
```

Reglas:

- La decide GWYN, no se propone: su turno ve el día completo ya mergeado.
- Máximo dos prioridades + smoke. Una zona acotada se prueba bien; cinco
  zonas se prueban a medias.
- **El RELEVO de la zona es Gwyn → Oscar → Havel**: la misma zona se mira
  dos veces al día con capas distintas — Oscar la recorre COMPLETA desde
  cero (¿el viaje del jugador aguanta?) y Havel se centra en lo nuevo +
  smoke del conjunto (¿lo añadido funciona y mola?). No es duplicación:
  cada uno responde SU pregunta sobre la misma zona.
- Si algún día Gwyn no deja zona (turno fallido), fallback por defecto:
  Oscar usa su run de referencia habitual desde save limpio y Havel usa lo
  que saque su propio `git log --since` + smoke completo del camino real.
  El sistema nunca se queda sin zona.

## 5. Cómo alimentan los hallazgos al día siguiente

Los cuatro perfiles dejan su huella en `backlog/TODO.md`; Gwyndolin (11:00)
la consume al planificar. Orden de prioridad del planificador:

1. Ramas rechazadas por Gwyn/Artorias (su arreglo va primero — ya es regla
   del sistema).
2. `[BUG]` que rompen el camino principal (los que detectaron el smoke de
   Havel o la run de referencia de Oscar).
3. NOTAS DE DIRECCIÓN de Oscar que Gwyn haya validado (se convierten en
   tareas de diseño/ajuste).
4. Ideas `[PENDIENTE]` que sirvan al capítulo en curso.
5. Resto de ideas (curación normal: valiosas hoy > antiguas por antigüedad).

El ciclo se cierra solo: un bug arreglado entra en el diff del día
siguiente, Oscar lo re-mide desde cero a las 05:00, Havel lo juega de nuevo
a las 07:00, y así el hallazgo de un día se convierte en verificación del
siguiente.

```
05:00 Oscar (run desde SAVE LIMPIO + veterano + ESTADO-JUGADOR) ──► [BUG] + dirección en TODO
07:00 Havel (juega lo nuevo + smoke SIN save limpio) ────────────► [BUG] + ideas en TODO
11:00 Gwyndolin (planifica con esos hallazgos) ──────────────────► plan del día
13:00–19:00 Ejecutores (bugs primero, luego tareas) ─────────────► ramas/PRs
21:00 Artorias (tests/lint/smoke técnico por PR) ────────────────► 💥/✅
23:00 Gwyn (diseño+sabor, merge, 🔬 zona de mañana) ─────────────► TODO
        └── la zona espera al relevo 05:00 (Oscar) → 07:00 (Havel) y recomienza
```

## 6. Estado del ciclo (una línea, los cuatro)

Cada tester termina SU entrada de worklog con una línea:

- `CICLO: verde` — todo fluye, sin hallazgos bloqueantes.
- `CICLO: ámbar` — bugs acumulados que no rompen el camino principal.
- `CICLO: rojo` — camino principal roto (el smoke/run de referencia no pasa).

Los cuatro la escriben: **Oscar** (¿la run de referencia sigue apta de
principio a fin?), **Havel** (¿el smoke pasa?), **Artorias** (¿los PRs están
sanos?) y **Gwyn**. Gwyn agrega los cuatro en su reporte a Juanma. Barato
de escribir, útil de leer: cuatro líneas dicen la salud del proyecto sin
abrir un solo fichero.

## 7. Anti-pisoteo explícito

- Un bug lo anota quien lo encuentra PRIMERO; el siguiente lo REFERENCIA,
  nunca lo duplica.
- **El save limpio es de Oscar**: nadie más resetea a partida nueva ni
  revalida el camino de cero. El smoke de Havel y el smoke técnico de
  Artorias trabajan SOBRE el estado existente, nunca desde cero.
- Oscar no implementa ni decide diseño: deja notas de dirección para Gwyn.
- Havel no abre PRs ni toca código: reporta síntomas de jugador.
- Artorias no rejuega «a ver si mola»: verifica técnica, punto.
- Gwyn no depura: pide localizaciones, no las hace.
- Cada uno escribe solo donde marca PROJECT-MAP (TODO + worklog propio;
  Oscar además mantiene `docs/ESTADO-JUGADOR.md`).
- Antes de Fase 1 (sin código): este protocolo se aplica a lo que exista —
  docs y diseño. «Jugar» será recorrer los docs nuevos como usuario (para
  Oscar: recorrer DESIGN/plot/ESTADO-JUGADOR simulando el viaje de un
  jugador de cero); el resto de capas no cambia.
