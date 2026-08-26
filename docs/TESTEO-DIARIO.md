# TESTEO-DIARIO — Protocolo de testeo del Concilio (CyberRoot)

> Creado por el Diseñador Jefe P5 (Fase 0, 26/08). Cierra la tarea
> `[PENDIENTE]` del 24/08. Lo leen SIEMPRE antes de su turno: **Havel**,
> **Artorias** y **Gwyn** (y Gwyndolin, que consume sus hallazgos).
> Complementa `docs/AGENTES-PLAN.md` §2.5 (protocolo de comunicación); aquí
> se define solo la CAPA DE TESTEO: quién prueba qué, cuándo y dónde deja
> la huella.

---

## 0. El principio: tres preguntas distintas

El juego necesita tres miradas que no se pisen. Cada perfil responde UNA
pregunta sobre el mismo repo, en turnos distintos del día:

| Hora | Agente | Pregunta | Capa |
|---|---|---|---|
| 07:00 | **Havel** | «¿Funciona? ¿Mola?» | **El jugador**: lo nuevo + smoke del conjunto |
| 21:00 | **Artorias** | «¿Está bien hecho?» | **El ingeniero**: tests, lint y smoke técnico de cada PR |
| 23:00 | **Gwyn** | «¿Es buen juego?» | **El director**: diseño, sabor y coherencia en conjunto |

La división es por CAPA, no por módulo: los tres pueden tocar el mismo
código el mismo día y aun así no repetir trabajo, porque uno lo juega,
otro lo verifica y el tercero lo juzga. Si dos encuentran el mismo fallo,
no es solape: Havel describe el SÍNTOMA («al entrar en la sala 3 se cuelga»),
Artorias localiza la CAUSA («el parser de ese tipo de sala lanza excepción
en X»). Síntoma y causa son aportaciones distintas.

---

## 1. Havel, 07:00 — el jugador

**Qué hace, en orden:**

1. **Lee la zona de hoy** en `backlog/TODO.md`, bloque «🔬 Testeo de
   mañana» (lo dejó Gwyn a las 23:00, §4). Ahí sabe qué priorizar SIN
   testear a ciegas.
2. **Detecta lo nuevo**: `git pull` y luego
   `git log --oneline --since="24 hours ago"` para ver qué entró mergeado
   desde su último turno. Eso define «lo nuevo» — nada más, nada menos.
3. **Juega lo nuevo** (timebox 15–20 min): la zona marcada por Gwyn, con
   manos de jugador. Si aún no hay build gráfica, ejerce lo que exista
   (core headless, seeds del harness, flujos por terminal) igual que lo
   jugaría un humano.
4. **Smoke del CONJUNTO**: una pasada rápida por el camino real desde save
   limpio (run de referencia de Oscar, `docs/ESTADO-JUGADOR.md`) para
   confirmar que el juego ENTERO sigue arrancando y avanzando. Lo nuevo
   puede ser brillante y aun así haber roto el arranque: eso lo caza el
   smoke, no la zona.
5. **Deja huella en `backlog/TODO.md`**: cada fallo como
   `[BUG] <dónde> <pasos mínimos para reproducir>`; cada idea como
   `[PENDIENTE]` (su rol creativo habitual, AGENTES.md).

Su filtro es «¿funciona? ¿mola?». NO revisa PRs ni código (capa de
Artorias) y NO valora coherencia narrativa ni dirección (capa de Gwyn).
Si algo no le mola pero funciona, lo apunta como idea/nota, no como bug.

## 2. Artorias, 21:00 — el ingeniero

**Qué hace, en orden:**

1. **Lista las ramas/PRs del día**: `git branch -a` + `gh pr list`.
   Incluye huérfanas viejas (regla del planificador, AGENTS-PLAN §4).
2. **Por cada PR, verificación técnica**: `pytest tests/core/` (headless),
   lint, y un smoke de juego MÍNIMO pero REAL (arrancar, completar un ciclo
   de sala, salir limpio). No basta con que compile.
3. **Marca 💥/✅ en `backlog/TODO.md`** con comentario accionable; un
   rechazo dice POR QUÉ y CÓMO arreglar (formato AGENTS-PLAN §4).
4. **Cruza con los bugs de la mañana**: si un `[BUG]` de Havel tiene la
   causa en un PR de hoy, lo nombra en su veredicto para que el ejecutor
   lo arregle PRIMERO mañana (prioridad máxima ya fijada en AGENTS-PLAN).

Su filtro es «¿está bien hecho?». NO opina de gusto ni de diseño: eso
viaja a Gwyn como nota, no como veredicto.

## 3. Gwyn, 23:00 — el director

**Qué hace, en orden:**

1. **Valida diseño y sabor en conjunto**: ¿lo mergeado hoy sigue
   `docs/DESIGN.md`? ¿la experiencia avanza hacia el juego descrito en su
   §10 (resumen ejecutivo)? ¿los textos cumplen SKILLS-ANTISLOP?
2. **Coherencia narrativa**: lee la producción del día de Manus contra los
   beats del plot y las fichas de voz. Es la ÚNICA capa que juzga esto.
3. **Merge final** (solo él mergea, cadena AGENTS-PLAN §4).
4. **Decide LA ZONA DE TESTEO DE MAÑANA** y la deja en `backlog/TODO.md`
   (§4 abajo). Nadie mejor que él sabe qué entró hoy y qué es crítico:
   es quien cierra el círculo para que Havel no pruebe a ciegas.
5. Reporte a Juanma (Telegram) incluyendo el estado del ciclo (§6).

Su filtro es «¿es buen juego?». NO depura: si necesita localizar una causa,
lo pide en su nota para Artorias/ejecutores (puede delegar en sub-agentes).

---

## 4. La ZONA de testeo: el relevo Gwyn → Havel ⭐

Es la pieza que evita que los tres prueben lo mismo o que Havel pierda la
mañana. Gwyn la escribe AL CIERRE (tras mergear, cuando ya sabe qué entró);
Havel la lee AL ABRIR. Formato exacto, máximo ~6 líneas:

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
- Si algún día Gwyn no deja zona (turno fallido), Havel usa el fallback
  por defecto: lo que saque su propio `git log --since` + smoke completo
  del camino real. El sistema nunca se queda sin zona.

## 5. Cómo alimentan los hallazgos al día siguiente

Los tres perfiles dejan su huella en `backlog/TODO.md`; Gwyndolin (11:00)
la consume al planificar. Orden de prioridad del planificador:

1. Ramas rechazadas por Gwyn/Artorias (su arreglo va primero — ya es regla
   del sistema).
2. `[BUG]` que rompen el camino principal (los que el smoke de Havel detectó).
3. Ideas `[PENDIENTE]` que sirvan al capítulo en curso.
4. Resto de ideas (curación normal: valiosas hoy > antiguas por antigüedad).

El ciclo se cierra solo: un bug arreglado entra en el diff del día
siguiente, Havel lo juega de nuevo a las 07:00, y así el hallazgo de un
día se convierte en verificación del siguiente.

```
07:00 Havel (juega lo nuevo + smoke) ──► [BUG] + ideas en TODO
11:00 Gwyndolin (planifica con esos hallazgos) ──► plan del día
13:00–19:00 Ejecutores (bugs primero, luego tareas) ──► ramas/PRs
21:00 Artorias (tests/lint/smoke técnico por PR) ──► 💥/✅
23:00 Gwyn (diseño+sabor, merge, 🔬 zona de mañana) ──► TODO
        └── la zona espera a las 07:00 y el ciclo recomienza
```

## 6. Estado del ciclo (una línea, los tres)

Cada tester termina SU entrada de worklog con una línea:

- `CICLO: verde` — todo fluye, sin hallazgos bloqueantes.
- `CICLO: ámbar` — bugs acumulados que no rompen el camino principal.
- `CICLO: rojo` — camino principal roto (el smoke no pasa).

Gwyn agrega los tres en su reporte a Juanma. Barato de escribir, útil de
leer: tres líneas dicen la salud del proyecto sin abrir un solo fichero.

## 7. Anti-pisoteo explícito

- Un bug lo anota quien lo encuentra PRIMERO; el siguiente lo REFERENCIA,
  nunca lo duplica.
- Havel no abre PRs ni toca código: reporta síntomas de jugador.
- Artorias no rejuega «a ver si mola»: verifica técnica, punto.
- Gwyn no depura: pide localizaciones, no las hace.
- Cada uno escribe solo donde marca PROJECT-MAP (TODO + worklog propio).
- Antes de Fase 1 (sin código): este protocolo se aplica a lo que exista —
  docs y diseño. «Jugar» será recorrer los docs nuevos como usuario;
  el resto de capas no cambia.
