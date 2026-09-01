# EN CURSO (CyberRoot)

> Lo que se ejecuta AHORA. Gwyndolin mueve aquí las tareas elegidas del plan;
> el ejecutor marca `[HECHO]` (+ nº de PR) junto a su línea; Artorias deja
> 💥/✅; **Gwyn, tras el merge, MUEVE la línea al archivo del mes**
> `../hecho/<AAAA-MM>.md`. Un rechazo de Gwyn se documenta AQUÍ mismo
> (POR QUÉ no se mergeó + CÓMO arreglarlo) y la tarea sigue viva.
> Mapa y estados: `../INDICE.md`.

## Activas

- `[EN CURSO]` (23/08) Crons del **Concilio (Fase 1)** activos desde 27/08
  (gate aprobado el 26/08). Primer día completo de Concilio ejecutado: 27/08.

## Asignadas por Gwyndolin (31/08, plan del día 01/09) — turno de Manus (03:00)

> Origen de cada línea: plan del 31/08 (Gwyndolin), sección «Manus (03:00 del
> 01/09)» — M1 y M2 del colchón del Acto 2. Este fichero lo releva Gwyndolin
> a las 11:00 con el plan del día; Manus deja aquí su huella `[HECHO]`
> (regla HARD §AGENTS-PLAN 2.5).

- `[HECHO]` **M1 — Fragmento 5 «El expediente»** (Manus, 01/09): expediente
  médico de salud laboral del hospital del Muelle (HOSP-47-C, folio
  OH-HOSP-47-C-0191, admisión 04:12 del día de la firma), campo «empresa» =
  VESPER DE GESTIÓN S.L. (cruza fragmento 4), «vuelve el jueves» (pulsera,
  frag. 2). `[LISTA]` en `backlog/historia/FRAGMENTOS.md`.
- `[HECHO]` **M2 — Capítulo 5 «Subestación»** (Manus, 01/09): beat 9 (asalto
  invertido), 4 encargos `story.ch5.e1`–`e4` (2 azules, 1 gris, 1 rojo de
  cierre), familia auditoría/defensa, grieta de Ceniza + 2.ª sombra del
  Auditor, fragmento 5 en E4. `[LISTA]` en `backlog/historia/CAPITULOS/05-subestacion.md`.

## Historial reciente (resumen — el detalle vive en `../hecho/2026-08.md`)

- 27/08 → 30/08: fundación narrativa de Manus (fichas, escenarios, caps. 0–3,
  fragmentos 1–3) y PRs #4–#12 mergeados; decisiones 🧭2 (opción B), 🧭6
  (operativa de «primer error»), 🧭8=(b), 🧭9 (eco diegético) y 🧭10
  materializadas en DESIGN y en código. Sin deuda abierta de esos días.
- 31/08: ver sección siguiente.

## Asignadas por Gwyndolin (31/08, plan del día) — MERGEADAS por Gwyn (23:00)

> Origen de cada línea: (O1) dirección #1 de Gwyn 30/08 · (O2) continuación
> natural de O1 + post-mortem del PR #10 · (S1) dirección #2 de Gwyn + nota de
> Artorias 30/08 · (S2) cap. 3 «Bombas» de Manus (31/08) · (T1) 🧭11 de Oscar +
> factura medida por Havel 31/08 (dirección #4) · (T2) dirección #3 + decisión
> 🧭9 firmada en DESIGN §6.1.

- MERGE: PR #13 (O1+O2) → #14 (S1+S2) → #15 (T1+T2), en el orden ensayado por
  Artorias. Suite tras CADA merge: **398 → 416 → 421 passed, 0 xfailed**
  (deltas declarados 13/18/5, cuadrados exactos; el ensayo de Artorias predijo
  421/0 y el árbol real lo clavó). Conflictos solo en las 2 huellas previstas
  (`activo.md` + `worklog/2026/08/31.md`), resueltos por script (patrón 30/08)
  conservando TODAS las huellas en orden cronológico. Cero marcadores verificados
  antes de cada commit. Ramas `feat/*` borradas; PRs MERGED en GitHub.
- Líneas `[HECHO]` archivadas en `../hecho/2026-08.md` (las 6 tareas de hoy +
  M1/M2 de Manus de la madrugada + M1/M2 rezagados del 29/08 que siguieron en
  este fichero dos noches de más).
- Smoke de diseño propio (Gwyn, post-merge): gate de datos 16/16 con ch3
  (tints y prereqs según Manus, `c.env` requiere `c.ps`); `rechazo_accionable`
  devuelve los conceptos que faltan (puerta visible antes de la llave, §6.0.3);
  flujo de encargo importable de punta a punta; `UMBRAL_CERO_RASTRO=5` vivo.
- **Decisiones de diseño de esta noche (Gwyn)**:
  1. **T1 VALIDADO tal cual** — umbral 5 + «sin `exit≠0`»: con los datos delante
     es la forma correcta del logro (frugalidad + pulcritud del NOVATO; la
     canónica queda fuera a propósito) y «Mano de seda» se separa bien (cero
     fallos). Firmado en DESIGN §7.6. 🧭11 SALDADA.
  2. **Forma del `sudo` GANADO (cap. 3) — FIRMADA en DESIGN §6.1**: credencial
     narrativa (objeto de estado), nunca contraseña tecleada; el rechazo sin
     credencial es diegético y accionable; sudo factura ruido premium y deja
     firma en el auth.log simulado (la lección: el poder deja factura).
  3. **Forma de la red simulada (cap. 4) — FIRMADA en DESIGN §6.1**: hosts como
     FS simultáneos del mismo Shell (`ssh` cambia de FS activo, `scp`
     `[host:]ruta`), conexión registrada en el auth.log del remoto, hosts
     descubribles leyendo `/etc/hosts` (necesidad como currículo). Tarea propia
     ya en `../pendiente/abierto.md`; se planifica cuando el cap. 4 llegue a datos.
