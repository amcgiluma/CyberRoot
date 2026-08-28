# MEJORAS APLICADAS — Historial de implementación (CyberRoot)

> Registro OBLIGATORIO que deja **Gwyn** cada vez que aplica una mejora a un
> prompt de un agente con `hermes cron edit --prompt ... <job_id>` (es lo que
> documenta en GitHub qué se cambió, en qué agente, cuándo y por qué). Va a
> GitHub público. Formato:

```
[APLICADA] (fecha) — por Gwyn
- Agente/job afectado: <nombre del agente> (<job_id>)
- Qué se cambió (del prompt): <resumen del cambio>
- Qué se mejoró / por qué: <motivo>
```

> Regla: cada `[APLICADA]` va acompañada de su commit en el worklog del día y
> de este registro. Sin eso, la mejora no está completa.

## Historial

### [APLICADA] (28/08) — por Gwyn
- Agente/job afectado: **Artorias, Revisor filtro** (`c4c98c5d8950`)
- Qué se cambió (del prompt): nuevo paso 2 de la MISIÓN — «ENSAYO DE
  INTEGRACIÓN PRE-MERGE» OBLIGATORIO cuando haya ≥2 ramas/PRs abiertas:
  simular el merge de todas las `feat/*` sobre main en un worktree desechable
  (`git worktree add --detach -f /tmp/ensayo-pr origin/main`), correr la
  suite COMBINADA y limpiar el worktree; si falla, localizar culpable y
  marcarlo 💥 con el arreglo EXACTO. Además, el aviso a Gwyn debe incluir el
  NÚMERO de tests esperado tras los merges.
- Qué se mejoró / por qué: el 27/08 cada PR pasó verde aislado pero las tres
  juntas rompían la suite (13 errores de colección por
  `src/assets/tests/__init__.py`); solo el ensayo manual de Artorias evitó
  mergear main roto. Sin CI, ese ensayo ES el CI: ahora es protocolo, no
  heroísmo. Origen: propuesta de Artorias del 27/08.

### [APLICADA] (28/08) — por Gwyn
- Agente/job afectado: **Smough, Ejecutor 2** (`55bb406c6e4c`)
- Qué se cambió (del prompt): (1) PASO 0.5 nuevo tras la firma: fijar
  identidad git Y VERIFICARLA (`git config user.name`) antes del PRIMER
  commit — el entorno arrastra la del turno anterior; (2) paso 6 nuevo:
  GUARD DE IDENTIDAD antes de pushear (`git log --format='%an'
  origin/main..HEAD | sort -u` == solo su nombre; si no, reescribir con
  `rebase --exec 'git commit --amend --reset-author --no-edit'` ANTES del
  push, nunca después). Renumerados los pasos siguientes (7 PR, 9 auto-mejora).
- Qué se mejoró / por qué: el 27/08 los 5 primeros commits de Smough salieron
  firmados «Ornstein» por identidad arrastrada del entorno; se arregló de
  suerte antes del push. La atribución en GitHub es la única autoría pública
  del Concilio. Origen: propuesta de Smough del 27/08 (parte 1 = PASO 0.5,
  parte 2 = guard). PARCIAL a propósito: se estrena SOLO en Smough; si
  funciona el 28/08, Gwyn lo extiende a Ornstein/Seath el 29/08.

### [APLICADA] (28/08) — por Gwyn
- Agente/job afectado: README raíz del repo (proceso, sin cambio de cron) —
  propuesta de **Ornstein** (bootstrap canónico)
- Qué se cambió (del prompt): nada en crons; nueva sección «🛠 ENTORNO DE
  DESARROLLO» en `README.md`: `python3.11 -m venv .venv && .venv/bin/pip
  install -r requirements-dev.txt` + suite canónica `./.venv/bin/python -m
  pytest` como ÚNICO comando de revisión.
- Qué se mejoró / por qué: la consigna «pytest verde headless» no decía DÓNDE
  vive el intérprete; cada ejecutor montaba su venv a mano y el comando real
  solo estaba en un worklog. Revisión reproducible en 1 comando.
  Origen: propuesta de Ornstein del 27/08.

### [APLICADA] (28/08) — por Gwyn
- Agente/job afectado: repo (proceso, sin cambio de cron) — propuesta de
  **Seath** (convención de dependencias dev)
- Qué se cambió (del prompt): nada en crons; creado `requirements-dev.txt`
  único en raíz (pytest>=9.1.1, pyxel>=2.9.9, pillow>=12.3.0) y REGLA en el
  README: los ejecutores NO añaden pyproject/requirements por rama sin
  propuesta. Forma elegida: requirements-dev y no `[dependency-groups]`
  (PEP 735) porque el pip del entorno es 24.0 y PEP 735 exige ≥25 —
  migración futura documentada en el propio fichero.
- Qué se mejoró / por qué: main no declaraba sus dependencias de desarrollo
  (el .venv funcionaba por estado acumulado invisible) y Fase 1 iba a
  multiplicar ficheros de empaquetado por rama (los pyproject de PR #1/#2 ya
  venían duplicados; se conservan SOLO como config de pytest).
  Origen: propuesta de Seath del 27/08.

### [APLICADA] (25/08) — por decisión de Juanma + Raiden (creación de agente)
- Agente/job afectado: **Oscar de Astora** (`ee900afb19da`), nuevo agente 05:00.
- Qué se hizo: se creó el 25/08 como GUARDIÁN DE LA EXPERIENCIA del jugador (run
  de referencia desde save limpio + perspectiva de veterano + mantiene
  `docs/ESTADO-JUGADOR.md` + notas de dirección a Gwyn). Se integró en
  `docs/TESTEO-DIARIO.md` como 4º perfil de testeo (05:00) y en el Concilio de 9.
- Qué se mejoró / por qué: resolver la propuesta de Juanma (24/08) de descargar a
  Havel y cubrir el testeo de la EXPERIENCIA (save limpio de cero + progresión a
  largo plazo) que ningún otro agente cubría.
- Origen: `[PROPUESTA]` (24/08) "nuevo agente para el testeo de la experiencia
  del jugador" — cerrada. Detalle: `docs/worklog/2026/08/25.md` y `AGENTES.md`.

### [APLICADA] (26/08) — por Raiden (reestructurador one-shot, autorizado por decisión de Juanma)
- Agentes/jobs afectados: los 9 del Concilio (Manus `f6bef0f8e3d8`, Oscar
  `ee900afb19da`, Havel `e3c150781f9d`, Gwyndolin `d5c8def555cd`, Ornstein
  `1ebe58fd86a3`, Smough `55bb406c6e4c`, Seath `65ccfc807dd6`, Artorias
  `c4c98c5d8950`, Gwyn `d972fdc912b7`) + Vigilante `7dec77a6d301` + Arquitecto
  F0 `70997a08ff3a` + Coordinador F0 `c206c75818eb`.
- Qué se cambió (del prompt): todas las referencias al monolítico
  `backlog/TODO.md` / `backlog/MEJORAS.md` pasan a la estructura nueva
  (`backlog/tareas/{pendiente,en-curso,hecho-<mes>,descartado}`,
  `backlog/mejoras/{pendiente,aplicadas}`, `backlog/zona-testeo.md`,
  `backlog/notas-manana.md`, índice en `backlog/INDICE.md`). Cada agente ahora
  Lee SOLO los ficheros de su rol (ver tabla en INDICE.md); los prompts quedan
  más cortos en lectura.
- Qué se mejoró / por qué: dentro de 3 meses TODO.md sería un megafichero que
  todos leerían enteros (violación de la regla de oro). Ahora cada turno lee
  solo su subconjunto y «hecho» se archiva POR MES.
- Detalle completo: `docs/worklog/2026/08/26.md` (entrada del reestructurador).
