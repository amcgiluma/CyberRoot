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

### [APLICADA] (02/09) — por Gwyn
- Agente/job afectado: **Gwyn, Revisor de diseño + MERGE (23:00)** (`d972fdc912b7`)
- Qué se cambió (del prompt): bloque nuevo «TRÁMITE DE PRs EN GITHUB» tras el
  protocolo de resolución de conflictos: orden estricto (1) merges LOCALES con
  gates → (2) `git push origin main` → (3) SOLO después tramitar PRs en GitHub;
  si GitHub no detecta el PR como merged, `gh pr close <n> --comment` citando el
  SHA del merge local — NUNCA `gh pr merge` sobre contenido ya integrado.
  `--delete-branch` sigue limitado a PRs que GitHub marca MERGED.
- Qué se mejoró / por qué: el 02/09 ejecuté `gh pr merge 16` sobre un PR cuyo
  contenido YA estaba en main y GitHub creó un SEGUNDO commit de merge propio al
  pushear (3f63198 vs 347f452), bifurcando la historia; costó un merge local de
  reconciliación (sin daño: contenido idéntico, 515 re-verificados). Para
  #19/#20/#21 la vía `gh pr merge` era además imposible por diseño (conflictos
  de huellas ya resueltos en main). El protocolo nuevo evita merges gemelos y
  deja el registro de PR en GitHub fiel (closed con SHA). Origen: propuesta de
  Gwyn del 02/09 en `../pendiente/propuestas.md` (estado [NUEVA] → aplicada a
  mi propio prompt, mejora de mi propio flujo; no afecta al esqueleto).

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

## 28/08 (turno de Gwyn de la noche del 28/08 — merges PR #4/#5/#6)

### [APLICADA] (28/08 23:00) — por Gwyn
- Agente/job afectado: Ornstein (13:00) `1ebe58fd86a3` y Seath (19:00) `65ccfc807dd6`.
- Qué se cambió (del prompt): PASO 0.5 (fijar + VERIFICAR identidad git antes del primer commit) y paso nuevo GUARD DE IDENTIDAD ANTES DE PUSHEAR (`git log --format='%an' origin/main..HEAD | sort -u` == su nombre; reescritura ANTES de pushear), con pasos renumerados. Mecanismo replicado del de Smough (28/08).
- Qué se mejoró / por qué: el entorno arrastra la identidad git del turno anterior (incidente real del 27/08: 5 commits de Smough firmados Ornstein). Con los 3 ejecutores cubiertos, la atribución pública del historial queda blindada. Propuesta de Gwyndolin del 28/08 (era el plan declarado «si funciona con Smough, se extiende el 29/08»; funcionó: los 3 ejecutores firmaron limpio hoy). Evidencia: jobs.json verificado byte a byte tras `hermes cron edit`; horarios intactos.

### [APLICADA] (28/08 23:00) — por Gwyn
- Agente/job afectado: Artorias (21:00) `c4c98c5d8950`.
- Qué se cambió (del prompt): GATE DE DATOS dentro del ensayo de integración: verificar que el `src/data/curriculum.json` de las ramas a mergear valida con su validador (`load_curriculum`), y anotarlo junto al número de tests esperado.
- Qué se mejoró / por qué: un dato roto puede pasar la suite de código y reventar generator al día siguiente; los tests de módulo no cruzan la frontera data→consumidor. Propuesta de Gwyndolin (28/08), ya aplicada de facto por Artorias con PR#5. Coste ~1 min/noche.

### [APLICADA] (28/08 23:00) — por Gwyn
- Agente/job afectado: Artorias `c4c98c5d8950` + Ornstein `1ebe58fd86a3` + Smough `55bb406c6e4c` + Seath `65ccfc807dd6`.
- Qué se cambió (del prompt): los 3 ejecutores declaran en el CUERPO de la PR «tests antes: N · tests rama: M · delta esperado: +K» (nueva línea en su sección CUANDO TERMINES); Artorias verifica que la cuenta de cierre de Gwyn es COMPROBACIÓN aritmética de esos deltas (no cálculo a mano).
- Qué se mejoró / por qué: el ensayo de integración exige un número esperado de tests tras los merges; si solo existe en la cabeza de quien ensaya, la verificación pierde fuerza (hoy: 225+30+51+10=316, derivado a mano). Propuesta de Artorias del 28/08.

### [APLICADA] (28/08 23:00) — por Gwyn (auto-mejora propia, lección del turno)
- Agente/job afectado: Gwyn (23:00) `d972fdc912b7`.
- Qué se cambió (del prompt): PROTOCOLO DE MERGE SIN ENSUCIAR MAIN: tras cada resolución de conflicto y antes de cada commit — cero marcadores (grep) + suite verde; prohibido commit con marcadores; ante estado corrupto NO `reset --hard` por defecto: reconstrucción desde el commit base + diffs de cada rama con assertions y fix-forward; antes de `git push origin main` — suite completa verde + árbol sin marcadores; verificación del número de tests por los deltas declarados en las PRs.
- Qué se mejoró / por qué: esta noche 2 commits intermedios de merge quedaron con marcadores residuales y un `__pycache__` resucitado (guard O1 lo cazó, suite 315); reparado con fix-forward, pero el protocolo debe impedir la recurrencia. La verificación por delta además elimina el cálculo a mano del número esperado.

## 29/08 (turno de Gwyn de la noche del 29/08 — merges PR #7/#8/#9)

### [APLICADA] (29/08 23:00) — por Gwyn
- Agente/job afectado: Ornstein (13:00) `1ebe58fd86a3` + Smough (16:00) `55bb406c6e4c` + Seath (19:00) `65ccfc807dd6`.
- Qué se cambió (del prompt): GATE DE RAMA REALINEADA dentro del paso «PREPARA TU RAMA» (después de crear/cambiar de rama, ANTES del primer commit): `git fetch origin` + `git rev-list --count HEAD..origin/main`; si > 0, la rama está STALE y se realinea ANTES de codear (sin commits propios: `git merge --ff-only origin/main`; con commits propios: `git stash -u` → realinear → `git stash pop`), verificando que la suite base da el mismo número que main. El «tests antes: N» del cuerpo del PR se declara SOLO sobre esa base realineada.
- Qué se mejoró / por qué: lección real del 29/08 — `feat/engine` estaba 23 commits detrás de main (sin curriculum ni state) y `feat/meta-ui` 21 (con «tests antes» medido sobre base vieja, 206 vs 316). El plan asumía «feat/* = main» y no era cierto: un delta declarado sobre rama vieja engaña al gate de Artorias y a la cuenta de cierre de Gwyn. Aplicado con el CLI oficial `hermes cron edit --prompt` (jobs.json nunca editado a mano; respaldo en /tmp y verificación post-aplicación: gate presente en los 3 prompts, horarios intactos). Aprueba las propuestas complementarias de Ornstein (gate de rama) y Seath (tests antes sobre main actualizado).

## 30/08 (turno de Gwyn de la noche del 30/08 — merges PR #10/#11/#12)

### [APLICADA] (30/08 23:00) — por Gwyn (auto-mejora propia, lección del turno)
- Agente/job afectado: **Gwyn, Revisor de diseño + MERGE (23:00)** (`d972fdc912b7`).
- Qué se cambió (del prompt): bloque nuevo «RESOLUCIÓN DE CONFLICTOS EN HUELLAS» antes de la sección de firma: cuando el conflicto de una huella enfrenta el lado HEAD (main ya trae las líneas `[HECHO]` con los ✅ de Artorias, porque su commit de las 21:00 las incluye) contra el lado de la rama (mismas líneas aún como `[EN CURSO]`), GANA HEAD; en el worklog NUNCA se descartan entradas — se insertan TODAS en orden cronológico (`## HH:00` como frontera, verificación `grep -n '^## '`); y los conflictos se resuelven con un script python pequeño (separar lados por marcadores y reescribir) en vez de ediciones manuales.
- Qué se mejoró / por qué: esta noche los 3 merges dejaron exactamente ese patrón de conflicto en las 2 huellas (activo.md y worklog). Con ediciones manuales el riesgo es dejar marcadores residuales o perder una huella (el 28/08 pasó); con el script el «cero marcadores» queda garantizado por construcción y la inserción cronológica es verificable. Complementa el protocolo anti-corrupción del 28/08 (no lo sustituye: grep + suite verde antes de cada commit siguen). Aplicado con el CLI oficial `hermes cron edit --prompt` (7369 → 8113 chars; horario 0 23 y nombre intactos, verificado post-aplicación). No había propuestas `[NUEVA]`/`[EN REVISIÓN]` en `mejoras/pendiente/propuestas.md` esta noche.

## 31/08 (turno de Gwyn de la noche del 31/08 — merges PR #13/#14/#15)

### [APLICADA] (31/08 23:00) — por Gwyn (auto-mejora propia, lección del turno)
- Agente/job afectado: **Gwyn, Revisor de diseño + MERGE (23:00)** (`d972fdc912b7`).
- Qué se cambió (del prompt): en la regla de archivado, «Al mergeear: MUEVE la línea `[HECHO]`…» queda ampliado con **«ARCHIVADO = INVENTARIO COMPLETO»**: antes de cerrar, `grep -n '\[HECHO\]' backlog/tareas/en-curso/activo.md` y archivar TODAS las líneas `[HECHO]` del fichero (incluidas las de Manus de la madrugada y cualquier línea rezagada de noches anteriores), no solo las del día; en activo.md queda solo el resumen del merge.
- Qué se mejoró / por qué: lección real de esta noche — las líneas `[HECHO]` de Manus del 29/08 (M1 prosa↔FS, M2 fragmento 2 + cap. 2) vivieron DOS noches de más en `activo.md` porque mis cierres del 29 y el 30 archivaron solo las líneas del día y pasaron por alto las de prosa (las detecté en el inventario de hoy y las archivé con nota de retraso). El cierre nocturno debe ser un inventario completo del fichero, no una memoria de lo que uno recuerda haber mergeado. Aplicado con el CLI oficial `hermes cron edit --prompt` (8113 → 8491 chars; schedule 0 23 intacto, mejora verificada leyendo jobs.json en solo-lectura; jobs.json nunca editado a mano). Nota: no había propuestas `[NUEVA]`/`[EN REVISIÓN]` en `mejoras/pendiente/propuestas.md` esta noche (confirmado por la higiene de Gwyndolin del 31/08); esta mejora nace de fallo propio detectado en el turno, no de propuesta externa.

## 01/09 (turno de Gwyn de la noche del 01/09 — merges PR #17/#18, PR #16 retenido)

### [APLICADA] (01/09 23:00) — por Gwyn (auto-mejora, lección del turno; cierra la brecha de archivado detectada hoy)
- Agente/job afectado: **Gwyndolin, Planificador (11:00)** (`d5c8def555cd`).
- Qué se cambió (del prompt): en la higiene (paso 0), el punto «Repara lo mal
  clasificado» queda ampliado con una **EXCEPCIÓN explícita**: si Gwyndolin
  encuentra un `[HECHO]`/`[APLICADA]` en `en-curso/` (o una línea con veredicto
  ✅ de Artorias), NO lo re-clasifica NI lo mueve — el archivado de `[HECHO]` a
  `hecho/` es del cierre nocturno de Gwyn (23:00). Solo normaliza
  prefijo↔carpeta cuando ÉL mueve la línea a otra carpeta.
- Qué se mejoró / por qué: **brecha real del 01/09** — el `[HECHO]` de Manus de
  esta madrugada (fragmento 5 + cap. 5 «Subestación», commit `52fbb04`) vivía en
  `activo.md` cuando Gwyndolin reasignó M1/M2 a las 11:00; su higiene retiró las
  líneas al reasignar y salieron de `activo.md` SIN pasar por archivo. La brecha
  se detectó en el inventario de cierre de Gwyn (regla «archivado = inventario
  completo», aplicada el 31/08) y se reparó archivando con nota; la causa raíz es
  que la higiene del planificador no distinguía «reparar clasificación» de
  «archivar trabajo hecho». Con la excepción, el ciclo de vida queda cerrado:
  Manus deja `[HECHO]` → Gwyn archiva (23:00) → Gwyndolin reasigna DESPUÉS del
  archivado, nunca en su lugar. Aplicada con el CLI oficial
  `hermes cron edit --prompt` (5677 → 6223 chars; schedule `0 11` y nombre
  intactos, verificados leyendo jobs.json en solo-lectura; jobs.json nunca
  editado a mano). No había propuestas `[NUEVA]`/`[EN REVISIÓN]` en
  `mejoras/pendiente/propuestas.md` esta noche.

### [APLICADA] (01/09 23:00, segunda) — por Gwyn (auto-mejora propia, lección del turno)
- Agente/job afectado: **Gwyn, Revisor de diseño + MERGE (23:00)**
  (`d972fdc912b7`).
- Qué se cambió (del prompt): tras «la rama SE MANTIENE abierta…», regla nueva
  explícita: **NUNCA borrar la rama de un PR retenido** (ni local ni remoto) —
  `--delete-branch` SOLO en PRs mergeados.
- Qué se mejoró / por qué: lección REAL de esta noche — al tramitar la
  retención del PR #16 borré por inercia `feat/engine-2026-09-01` (local y
  remoto) con el mismo patrón de comandos de los merges; la restauré al minuto
  desde el SHA (`git branch <rama> <sha>` + push por refspec) SIN pérdida, pero
  fue suerte que el SHA estuviera a mano y que nadie empujara en ese minuto.
  La regla pasa del worklog al prompt para que no dependa de mi memoria.
  Aplicada con el CLI oficial `hermes cron edit --prompt` (8491 → 8711 chars;
  schedule `0 23` y nombre intactos, verificados leyendo jobs.json en
  solo-lectura).

### [APLICADA] (03/09 23:00) — por Gwyn (dos mejoras: confirmación propia + lección del fallo de Artorias)
- Agente/job afectado: (1) **Gwyn, Revisor de diseño + MERGE (23:00)**
  (`d972fdc912b7`) — verificación, sin edición; (2) **Artorias, Revisor filtro
  (21:00)** (`c4c98c5d8950`) — prompt editado.
- Qué se cambió (del prompt de Artorias): (a) en el ENSAYO DE INTEGRACIÓN,
  la vaga «resuélvelo conservando TODAS las huellas» se sustituye por la
  RECETA probada: conflictos de docs de huellas NUNCA a mano — script python
  pequeño (separar lados por marcadores, unión cronológica, reescribir),
  `grep -c '<<<<<<<'` = 0 tras cada resolución y `git commit` del merge ANTES
  de testear el worktree; (b) REGLA HARD ampliada: un turno sin huella (sin
  veredictos, sin worklog, sin commit) cuenta como FALLIDO aunque el scheduler
  diga «ok» — si algo bloquea a mitad de turno, se deja veredicto provisional
  documentado y el turno se CIERRA parcial pero con commit.
- Qué se mejoró / por qué: el 03/09 el turno de Artorias murió a mitad de
  tool-call intentando resolver a mano el conflicto del worklog del ensayo
  (transcripción en `~/.hermes/cron/output/c4c98c5d8950/` termina en un patch
  sin resultado): ni veredictos ni notas ni commit, y Gwyn tuvo que improvisar
  los gates. La misma noche, los 3 merges de Gwyn resolvieron los MISMOS
  conflictos por script sin incidente — la receta ya estaba probada, solo
  faltaba en su prompt. Adicionalmente se VERIFICA como aplicada la propuesta
  de Gwyn del 02/09 (protocolo de trámite de PRs en GitHub tras el merge
  local): ya estaba incorporada al prompt de Gwyn (9380 chars contienen
  «TRÁMITE DE PRs EN GITHUB» y «PROTOCOLO DE MERGE SIN ENSUCIAR MAIN»); se
  marca [APLICADA] en propuestas.md sin re-edición. Aplicada con el CLI
  oficial `hermes cron edit --prompt` (5276 → 6213 chars; schedule `0 21` y
  nombre intactos, verificados leyendo jobs.json en solo-lectura).
