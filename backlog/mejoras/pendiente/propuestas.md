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

- Estado: [NUEVA] — para decisión/aplicación de Gwyn (23:00).

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
- Estado: [NUEVA] — para decisión/aplicación de Gwyn (23:00).

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
- Estado: [NUEVA] — para decisión/aplicación de Gwyn (23:00).
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
- Estado: [NUEVA] — decisión/aplicación de Gwyn.

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
- Estado: [NUEVA] — para decisión/aplicación de Gwyn (23:00).
