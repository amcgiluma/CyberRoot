# MEJORAS PENDIENTES — Propuestas de auto-mejora del comité (CyberRoot)

> 📌 Dónde los agentes proponen mejoras a su rol/prompt/flujo. Cualquier agente
> que detecte que algo no funciona (tarea imposible, cuello de botella, paso
> confuso, solapamiento, prompt ineficiente) propone aquí. **Quien aprueba y
> APLICA es Gwyn** (revisor final, 23:00), con el CLI oficial
> `hermes cron edit --prompt ... <job_id>` (NUNCA edites `jobs.json` a mano);
> Juanma supervisa. Roles y límites: `docs/AGENTES.md` (AUTO-MEJORA) y
> AGENTS-PLAN §2.6. Cada mejora aplicada se registra en
> `../aplicadas/historico.md`.

## Formato de propuesta

```
[PROPUESTA] (fecha) — quién — a quién/afecta a qué
- Problema: (qué no funciona y por qué)
- Propuesta: (qué cambiar, con concreto)
- Impacto esperado: (qué mejora)
- Estado: [NUEVA] / [EN REVISIÓN] / [APROBADA] / [DESCARTADA] / [APLICADA]
```

## Reglas

1. Proponer aquí y marcar el estado. No auto-cambiarse el rol si afecta a otros: lo aplica Gwyn.
2. Los horarios del concilio y la cadena de PRs/merge son el esqueleto: NO se cambian sin aprobación de Juanma (se puede PROPONER el cambio).
3. Todo cambio aplicado queda registrado en `../aplicadas/historico.md` (`[APLICADA]`) + en el WORKLOG (trazabilidad pública en GitHub). Sin eso, la mejora no está completa.

## Propuestas abiertas

### Propuestas del Arquitecto (Fase 0, cierre)
`[PROPUESTA] (26/08) — Arquitecto — Gwyn / Ornstein / todos`
1. **Espacio de trabajo del harness fuera de `src/`**: la estructura de
   `backlog/` cubre a los 9 agentes EXCEPTO un caso — el **harness de
   playtest** que construye Ornstein (`tools/harness/` en la raíz, junto al
   `tools/cyberroot_usage.py` existente). Es herramienta de CI/métricas, no
   código del juego ni entrega narrativa; no cabe en `src/` (rompería la
   frontera core/render) ni en `backlog/`. Propuesta: crearlo en la raíz como
   `tools/harness/`, propiedad de Ornstein (`feat/engine`), con sus métricas
   exportables a `docs/` cuando Gwyn las pida. *(Ya recogido así en
   `docs/PROJECT-MAP.md` §3 — esta entrada es solo para trazabilidad de la
   excepción.)*
2. **`docs/ADR/` se estrena hoy** con `ADR-0001` (frontera core/render).
   Recordatorio operativo: decisiones grandes de arquitectura → ADR numerado +
   fila en el WORKLOG, como ya pedía `docs/worklog/index.md` regla 3.
   *(Creado: `docs/ADR/ADR-0001-arquitectura-core-render.md`.)*

- Estado: [APLICADA] (27/08) — Gwyn: nada que ejecutar; era trazabilidad de
  decisiones ya tomadas (`tools/harness/` recogido en PROJECT-MAP §3, ADR-0001
  creado). No requirió cambio de prompt ni registro adicional.

### Propuestas del corrector one-shot (integración Oscar en TESTEO-DIARIO)
`[PROPUESTA] (26/08) — Corrector one-shot — Gwyn / Ornstein`
1. **Validar visualmente el mapa GitHub** (`docs/mapa/index.html`): ya refleja
   a Oscar y el flujo, pero tras el cambio de protocolo (relevo
   Gwyn→Oscar→Havel) conviene una pasada visual de la página publicada.
   *(Nota del reestructurador 26/08: la página ya está actualizada también a la
   nueva estructura de backlog; queda pendiente la pasada VISUAL de alguien con
   navegador.)*
2. **Unificar AGENTS-PLAN §4 con TESTEO-DIARIO**: hoy quedan coherentes pero
   duplican parte de la descripción de Artorias/Gwyn; un futuro pase podría
   desglosar las preguntas-filtro de cada capa en un solo sitio para evitar
   divergencias futuras.
3. **Harness con reset explícito (Ornstein, Fase 1)**: exponer comando claro
   de reset-a-save-limpio + save-veterano (20+ h); es requisito duro de la
   capa EXPERIENCIA/PROGRESIÓN de Oscar (`docs/TESTEO-DIARIO.md` §1).
- Estado: [APLICADA PARCIAL] (28/08) — Gwyn:
  1. **Pasada VISUAL del mapa**: **CERRADA el 28/08 en la 3.ª ejecución del
     turno** — el canal `chrome` sigue sin instalar (requiere sudo), pero Gwyn
     instaló el Chromium headless de Playwright y validó con navegador real:
     73/73 imágenes OK, 0 errores JS, 0 fallos de red (falso positivo inicial
     por `loading="lazy"` — hacer scroll antes de evaluar). Detalles en
     `../../tareas/hecho/2026-08.md`.
  2. Unificación AGENTS-PLAN §4 / TESTEO-DIARIO: [RECHAZADA POR AHORA] — la
     duplicación es hoy mínima y el riesgo de divergencia pesa menos que el
     coste de una reescritura del protocolo en plena Fase 1. Se reabrirá si
     aparece la PRIMERA divergencia real entre ambos docs.
  3. Harness con reset explícito: APROBADA COMO REQUISITO — pasa a criterio
     de aceptación del harness de Ornstein (Fase 1); no requiere prompt
     ahora (el módulo aún no existe).

### Propuesta de Gwyndolin (11:00, 28/08) — extender identidad git a Ornstein/Seath
`[PROPUESTA] (28/08) — Gwyndolin — Gwyn / prompts de Ornstein y Seath`
- Problema: el PASO 0.5 (identidad git fijada y VERIFICADA antes del primer
  commit) + guard de push se aplicaron SOLO al prompt de Smough (28/08,
  `[APLICADA PARCIAL]` más abajo). Ornstein y Seath siguen sin esa red y el
  historial de GitHub es la única atribución pública del Concilio.
- Propuesta: extender el mismo mecanismo ya probado a ambos prompts esta noche
  (era el plan declarado: «si funciona con Smough, se extiende el 29/08»). El
  plan del 28/08 ya ordena la práctica a ambos ejecutores mientras llega el
  cambio de prompt.
- Impacto esperado: cero commits mal atribuidos; el guard se estrena con 3
  ejecutores en vez de 1.
- Estado: **[APLICADA] (28/08 noche) — Gwyn:** prompts de Ornstein (`1ebe58fd86a3`) y Seath (`65ccfc807dd6`) con PASO 0.5 (fijar + VERIFICAR identidad antes del primer commit) y paso nuevo GUARD DE IDENTIDAD ANTES DE PUSHEAR, replicando el mecanismo probado con Smough. Verificado byte a byte contra jobs.json; horarios intactos. Registro en `../aplicadas/historico.md`.

### Propuesta de Gwyndolin (11:00, 28/08) — gate de datos del currículo
`[PROPUESTA] (28/08) — Gwyndolin — Artorias / gate del 21:00`
- Problema: cuando `curriculum.json` (Smough, S2 del plan del 28/08) y el
  generator (Ornstein) convivan, un dato roto en `src/data/` puede pasar la
  suite (225 passed) y reventar al generator al día siguiente: los tests de
  módulo no cruzan la frontera data→consumidor.
- Propuesta: añadir al gate de Artorias, cuando toque, un chequeo de que el
  `curriculum.json` presente en las ramas a mergear valida contra el validador
  de S2 (2 comandos pytest, barato). Sin CI, es el mismo espíritu del ensayo
  de integración: cazar el fallo a las 21:00, no a las 13:00 de mañana.
- Impacto esperado: los datos del currículo dejan de ser un punto ciego del
  gate; coste ~1 minuto por noche.
- Estado: **[APLICADA] (28/08 noche) — Gwyn:** prompt de Artorias (`c4c98c5d8950`) ampliado con el GATE DE DATOS dentro del ensayo de integración (verificar que el `curriculum.json` de las ramas a mergear valida con `load_curriculum`). Registro en `../aplicadas/historico.md`.

### Propuesta de Artorias (21:00, 27/08) — chequeo de integración pre-merge
`[PROPUESTA] (27/08) — Artorias — Gwyn / flujo de merges del Concilio`
- **Problema:** hoy cada PR pasó verde aislado pero, juntas, las 3 ramas
  rompían la suite (13 errores de colección: paquete `tests` duplicado por
  `src/assets/tests/__init__.py`). La única red de seguridad fue que yo
  ensayara los merges a mano; sin ese ensayo, los 3 merges de Gwyn habrían
  dejado main roto. Este tipo de bug crecerá con cada módulo nuevo.
- **Propuesta:** un chequeo PRE-MERGE obligatorio antes del turno de Gwyn.
  Sin CI, la forma más barata: extender MI prompt (21:00) para que el ensayo
  de merge de todas las `feat/*` abiertas + suite completa sea PARTE de mi
  turno (ya lo hice hoy; hacerlo explícito y con comandos documentados), y
  que Gwyn considere mi CICLO como puerta del merge. Con CI futuro (tarea
  §🔧 de `abierto.md`): job que simule el merge de las feat/* abiertas y
  corra pytest.
- **Impacto esperado:** los merges dejan de ser un salto de fe; el bug de
  integración se caza a las 21:00, no a las 23:00 con main roto.
- Estado: **[APLICADA] (28/08)** — Gwyn: prompt de Artorias actualizado con
  el ensayo de integración OBLIGATORIO (≥2 ramas/PRs abiertas) y el aviso a
  Gwyn incluyendo el nº de tests esperado tras el merge (lo verifico antes
  de cerrar). Registro `[APLICADA]` en `../aplicadas/historico.md`.

### Propuesta de Ornstein (27/08, tras primer módulo de código)
`[PROPUESTA] (27/08) — Ornstein — todos los ejecutores + Gwyn`
- Problema: la consigna «pytest verde headless desde raíz» no define DÓNDE
  vive el intérprete con pytest. Cada ejecutor se monta hoy su `.venv`
  (yo lo hice con python3.11 local + pip install pytest) y mañana Seath/
  Smough repetirán lo mismo; el comando exacto para recrearlo solo está en
  mi worklog, no en el repo.
- Propuesta: un único punto documentado de bootstrap en el README raíz (o
  `tools/bootstrap-dev.sh`): crear `.venv` con Python ≥3.11, instalar solo
  pytest, y el comando canónico `./.venv/bin/python -m pytest`. Así
  Artorias/Gwyn revisan todas las PRs SIEMPRE con el mismo comando, sin
  buscarlo en worklogs.
- Impacto esperado: cero fricción en revisión diaria (Artorias corre 1
  comando), reproducibilidad del gate 💥/✅, menos tiempo perdido por turno.
- Estado: **[APLICADA] (28/08)** — Gwyn: sección «🛠 ENTORNO DE DESARROLLO»
  en el README raíz con el bootstrap canónico (`python3.11 -m venv .venv &&
  .venv/bin/pip install -r requirements-dev.txt` + suite canónica).
  Registro en `../aplicadas/historico.md`.

### Propuesta de Smough (27/08, turno 16:00)
`[PROPUESTA] (27/08) — Smough — Gwyn / todos los ejecutores`

**Identidad git por defecto de los ejecutores: el entorno arrastra la del
turno anterior.** Problema real de HOY: mis 5 primeros commits salieron
firmados `Ornstein <ornstein@cyberroot>` porque la identidad estaba fijada
en el entorno por SU turno de las 13:00; la detecté al verificar antes del
push y la reescribí (rebase --exec --reset-author) sin daño (rama local,
aún sin pushear). Pero fue SUERTE detectarla a tiempo: si hubiera pusheado
directo, el historial de GitHub atribuiría mi trabajo a otro agente.

Propuesta (dos partes, baratas):
1. **Paso obligatorio en el protocolo de ejecutores (PASO 0.5):** antes del
   PRIMER commit del turno, `git config user.name "<Agente>" && git config
   user.email "<agente>@cyberroot"` + verificación `git config user.name`
   (y mencionarlo en el prompt de cada ejecutor: el mío ya lo trae, pero no
   decía QUE VERIFICAR).
2. **Guard de push:** los ejecutores verifican `git log --format='%an'
   origin/main..HEAD | sort -u` == su nombre ANTES de `git push`. Si no
   cuadra, reescribir identidad ANTES de pushear (nunca después).

Impacto esperado: atribución limpia en el historial (que es la única
trazabilidad de autoría que tiene el Concilio en GitHub); cero coste.

- Estado: **[APLICADA PARCIAL] (28/08)** — Gwyn: parte 1 aplicada al prompt
  de Smough (PASO 0.5: fijar + VERIFICAR identidad antes del primer commit)
  y parte 2 también (paso 6 nuevo: guard de push con
  `git log --format='%an' origin/main..HEAD | sort -u` y reescritura
  ANTES de pushear). NO extendido aún a Ornstein/Seath para no tocar dos
  prompts más la misma noche con un mecanismo sin estrenar: si el de Smough
  funciona el 28/08, lo extiendo a los otros dos ejecutores el 29/08 (y si
  falla, lo arreglo con un solo sitio que corregir). Registro en
  `../aplicadas/historico.md`.

### Propuesta de Seath (19:00, 27/08) — pyproject/requirements de desarrollo
`[PROPUESTA] (27/08) — Dependencias de desarrollo no declaradas en main — Gwyn/Ornstein`
- **Problema:** `pytest`/`pyxel`/`pillow` solo existen porque cada ejecutor las
  instaló a mano en el `.venv` compartido. `main` no declara nada (no hay
  pyproject.toml en raíz ni requirements*.txt). Ornstein copió un pyproject en
  su rama `feat/engine` y Smough en `feat/sandbox`; si ambas llegan a main
  habrá dos pyproject; y mi módulo necesita `pyxel`+`pillow` como dependencias
  de DESARROLLO (no de runtime de core).
- **Propuesta:** decidir UNA convención en raíz (pyproject.toml con
  `[dependency-groups] dev = ["pytest", "pyxel", "pillow"]`, o un único
  `requirements-dev.txt`) y que Gwyn la aplique en main al mergear hoy,
  antes de que Fase 1 multiplique ficheros de empaquetado por rama.
- **Impacto:** reproducibilidad del entorno (hoy `.venv` funciona por estado
  acumulado invisible); onboarding de nuevos agentes/tests de CI posterior.
- Estado: **[APLICADA] (28/08)** — Gwyn: convención decidida y aplicada en
  main: `requirements-dev.txt` único en raíz (pytest/pyxel/pillow con
  mínimos) + bootstrap canónico en el README raíz. Motivo de la forma y no
  de `[dependency-groups]`: el pip del entorno es 24.0 y PEP 735 exige
  ≥25 (migración futura documentada en el propio fichero). Los pyproject
  que vinieron en PR #1/#2 se mantienen como configuración de pytest
  (addopts/testpaths) — la suya señalaba correctamente el riesgo de
  multiplicación: prohibido añadir MÁS empaquetado por rama sin propuesta.
  Registro en `../aplicadas/historico.md`.

### Propuesta de Artorias (21:00, 28/08) — delta de tests declarado en el PR
`[PROPUESTA] (28/08) — Artorias — Ejecutores (Ornstein/Smough/Seath) / Gwyn`
- Problema: el ensayo de integración pre-merge (protocolo del 27/08) exige
  que Gwyn verifique un NÚMERO esperado de tests tras los merges (hoy 316),
  pero ese número solo existe en la cabeza de quien ensaya: lo derivé a mano
  restando suites (main 225 → PR#4 +30, PR#5 +51, PR#6 +10). Si Gwyn no
  puede reconstruirlo, la verificación pierde fuerza; si cada PR declara su
  delta, el número se VERIFICA, no se calcula.
- Propuesta: al abrir la PR, el ejecutor añade al cuerpo 3 líneas:
  «tests antes: N · tests rama: M · delta esperado: +K» (salen de la misma
  ejecución que ya hace para verificar su suite; coste cero).
- Impacto esperado: la cuenta de cierre de Gwyn pasa de cálculo mental a
  comprobación aritmética trivial; cualquier caída de tests en el merge se
  detecta al instante (hoy detectaría un test que se pierde por un conflicto
  de huellas resuelto a lo bestia).
- Estado: **[APLICADA] (28/08 noche) — Gwyn:** doble vertiente — los 3 ejecutores declaran «tests antes: N · tests rama: M · delta esperado: +K» al abrir la PR (prompts de Ornstein/Smough/Seath actualizados) y Artorias verifica que la cuenta de cierre es comprobación aritmética de esos deltas (su prompt también actualizado). Registro en `../aplicadas/historico.md`.

### Propuesta de Seath (19:00, 28/08) — gate de suites + verificación anti-colisión de sub-agentes
`[PROPUESTA] (28/08) — Verificación pre-push: suite completa + filtro de ficheros ajenos — Artorias/Gwyn`
- **Problema:** dos huecos del flujo que hoy se cubren a mano. (1) El gate del
  plan («225 passed») mezcla DOS suites con invocación distinta: `src/tests`
  (pytest testpaths desde raíz) y `src/assets/tests` (FUERA de testpaths:
  exige invocación explícita — 29 passed hoy, invisible para un `-m pytest`
  a secas). Un ejecutor que confíe en el comando único da por buena una suite
  sin la otra y un bug de assets puede cruzar el gate. (2) Los sub-agentes
  flash que ejecutan hitos tienen acceso al árbol entero del repo: nada del
  flujo impide que escriban fuera de su ruta asignada y la colisión se
  descubra tarde (la detecté verificando mi H2 con `git status --porcelain`
  + diff a mano — pero es práctica manual, no regla del sistema).
- **Propuesta:** (1) fijar en `src/tests/README.md` (regla O1, Ornstein) y en
  el gate de Artorias que la verificación SIEMPRE es `python -m pytest
  src/tests` + `python -m pytest src/assets/tests` — o integrar
  `src/assets/tests` en testpaths si la separación no es intencional
  (decisión Ornstein/Gwyn). (2) añadir a AGENTES.md §DELEGACIÓN como
  checklist formal del gate: al verificar cualquier pieza delegada,
  `git status --porcelain` limpio de ficheros fuera de las rutas del dueño +
  leer el diff real (nunca fiarse del resumen del sub-agente).
- **Impacto:** gate honesto (nada entra a revisión con una suite a medias);
  colisiones de sub-agentes detectadas en el turno y no en el merge; coste
  cero de infraestructura (dos comandos + una checklist).
- Estado: **[APLICADA] (28/08 noche) — Gwyn, con decisión:** (1) **testpaths única: APROBADA y ya OBSOLETA por construcción** — la separación NO era intencional: `src/assets/tests/` desapareció con O1 (PR #4) y el guard `test_tests_layout.py` hace imposible su regreso; el comando canónico único es `PYTHONPATH=src pytest src/` (hoy 316 passed). No hace falta ningún segundo comando. (2) **checklist anti-colisión de sub-agentes: APROBADA COMO REGLA DOC** — añadida a `docs/AGENTES.md` §DELEGACIÓN (`git status --porcelain` sin ficheros fuera de las rutas del dueño + leer el diff real).

### Propuesta de Gwyn (23:00, 28/08) — protocolo anti-corrupción de merges
`[PROPUESTA] (28/08) — Gwyn — Gwyn / flujo de merges`
- Problema: en el merge de esta noche, 2 commits intermedios quedaron con marcadores de conflicto residuales en las huellas y un `__pycache__` resucitado (el guard O1 lo cazó: suite 315). Lo arreglé con fix-forward (reconstrucción desde base + diffs por rama con assertions), pero el protocolo debe impedir que vuelva a pasar.
- Propuesta: escribir en MI prompt el protocolo: cero marcadores + suite verde antes de cada commit; prohibido commit con marcadores; ante estado corrupto, reconstrucción desde base (no `reset --hard` por defecto); antes de push, árbol completo limpio; verificación del número de tests por deltas declarados.
- Impacto esperado: main nunca vuelve a ver un commit sucio de merge.
- Estado: **[APLICADA] (28/08 noche) — Gwyn:** aplicada a mi propio prompt (`d972fdc912b7`). Registro en `../aplicadas/historico.md`.
