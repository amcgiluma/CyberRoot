# engine/ — El motor roguelite

> **Qué hace:** dirige el ciclo completo de una incursión y su vuelta al Hub:
> mapa de nodos → salas → extracción/detección → liquidación → post-mortem.
> Orquesta `sandbox/` (ejecuta comandos) y `generator/` (crea la incursión);
> aplica las reglas de números del diseño.
>
> Normativa: `docs/DESIGN.md` §4.1 (loop), §7 (dopamina/números), §4.7 (Hub) ·
> arquitectura: `../ARCHITECTURE.md` §2.5.

## Responsabilidades
- **Run**: estado de la incursión, sala actual, rutas, entradas/salidas de
  sala; modos mapa↔terminal como ESTADOS del core (el render solo los pinta).
- **Vigilancia/detección**: % sube por ruido de acciones (regla de luz §6.0.2:
  más luz = más vigilancia base por anillo). NUNCA sube por reloj artificial
  (§7.9). Al llegar al umbral → expulsión.
- **Economía DATOS×COMBO** (§7.1): base por tipo de dato; combo por escalones
  (+0,1 por cadena limpia, baja UN escalón por fallo, DOS por tramo de
  detección); liquidación total al extraer, parcial (50 % ⚠️ v1 de lo ya
  extraído, sin combo) al ser expulsado + bonus de profundidad (§7.7).
- **Apuestas de run** (§7.3): deep scan, ruta ruidosa, «una sala más».
- **Sinergias** (§5.2, catálogo v1 en §7.8): detección de disparadores
  pipeline/recon→ejecución/estado persistente/etc., leyendo el historial de
  comandos de la run. Los efectos son numéricos/eventos — el juice lo añade el
  render con los mismos eventos.
- **Cierre de run**: informe post-mortem (siempre, §4.7) + cola de eventos
  hacia el Hub (historia avance SIEMPRE — el contenido vive en `data/story/`).
- Números calibrables: constantes documentadas en un solo sitio para que el
  harness las ajuste sin reescribir lógica.

## Entradas / salidas
- ENTRADA: comandos de jugador (`exec`, `ui.*`) + `IncursionInstance` del
  generador + perfil del jugador (boons, karma).
- SALIDA: mutaciones de estado de run + `Event`s (combo, alerta, hallazgo,
  expulsión, liquidación…).

## Cómo se testea
- Run completa headless: resolver una incursión sembrada ejecutando su
  secuencia canónica → éxito esperado, métricas exactas.
- Expulsión forzada (ruido máximo) → parcial cobrado correcto, lección en cola,
  avance narrativo presente.
- Combo: cadenas limpias/fallidas/tramos de alerta → escalones exactos.
- Determinismo: misma seed + mismos comandos → misma partida entera.

## Dueño
Ornstein (`feat/engine`). También construye `tools/harness/` sobre esta API.

---

## v0 (O2, 30/08) — post-mortem del Auditor leyendo el historial real

Primer fichero del módulo: `postmortem.py` (la pieza que el Hub muestra
SIEMPRE primero, §4.7). `build_postmortem(shell_dict, state)` es una función
PURA, testeable headless (sin I/O, sin RNG, sin estado global).

- **EN**: `Shell.to_dict()` (historial de la sesión real) + `state` con
  `noise_budget` (la MISMA unidad que `total_noise`, 🧭10; default 12 ⚠️ v1).
- **SALIDA**: dict plano con `factura` (cuentas por comando + `errores`),
  `total_noise` vs `noise_budget`, `dentro_presupuesto`, y una línea del
  Auditor (`line_key` + `args`) que cita el comando CONCRETO que disparó la
  detección — el que hace CRUZAR el presupuesto acumulado si lo hay, o el
  pico (más ruido individual) si no. Voz: formulario seco (PERSONAJES.md).
  El texto va como CLAVE + args; el render resuelve la prosa contra `data/`
  (convención §3: core no hardcodea textos).
- **Tests**: `src/tests/core/engine/test_postmortem.py` (8 tests) — factura
  de la sesión canónica (ls 2 · cat 1 · cp 1 · cd 1 · errores 0), total 6/12,
  pico sin cruce, cruce con presupuesto 5, errores contados, default de
  presupuesto, helpers deterministas, informe JSON-plano.

```bash
./.venv/bin/python -m pytest src/tests/core/engine -o addopts= -q
```

---

## v0.2 (O1+O2, 31/08) — flujo de ENCARGO del cap. 2 + post-mortem conectado

Segundo fichero del módulo: `session.py` — el flujo completo de un encargo del
currículo REAL: **listar → abrir (validando prereqs) → generar la sala del
contrato → jugar → cerrar.** Un `postmortem.py` lo consume al CERRAR (O2).

- `listar_encargos(curriculum, chapter, knowledge=None)` → vitrina de la mesa
  del Hub: los encargos del capítulo ordenados por id, con `abrible`/`falta`
  si se pasa `knowledge`. NO genera nada (🧭8=(b)).
- `rechazo_accionable(...)` → qué conceptos faltan (el «no puedes» es un dato,
  no una negativa).
- `abrir_encargo(curriculum, quest_id, knowledge, run_seed=0)` → valida
  `Contract.prereqs_met` al ABRIR (nunca en `generate()`); si procede, genera
  la sala (seed determinista `quest_id:run_seed`) y devuelve un
  `EncargoSession` (Incursion + Shell viva). `session.ejecutar(line)` juega.
- `cerrar_encargo(session, modo="completado"|"expulsión")` → adjunta
  `build_postmortem(shell_dict, state)` como dato estructurado del cierre.

Para que la golden del cap. 2 (`grep 11:04 centralita/turnos/turno.log |
wc -l` → `2`) fuera JUGABLE dentro del flujo, el generador ganó soporte del
cap. 2: `generate(seed, chapter=2, contract_id="story.ch2.e1")` construye la
sala de la centralita (nueva hoja `src/core/generator/chapter2.py`, canon con
la golden) y `generate(seed,0)` queda byte-a-byte idéntico (regresión).

El módulo consume `build_postmortem` como función PURA e intacta: el post-
mortem del cap. 2 factura la línea del pipe (grep/wc) bajo su comando primario
y `total_noise` con el ruido real (grep 2 + wc 1 + cd 0).

---

## v0.3 (O4, 02/09) — el post-mortem entrega la VOZ resuelta

`build_postmortem` construye la línea del Auditor como `line_key` + `args`
(convención §3: core no hardcodea prosa) y desde esta entrega RESUELVE la
prosa contra `data/textos` antes de devolverla, sin romper la API pura. El
dict de cierre gana dos campos legibles sin render:

- `auditor_text`: la cadena final (`resolve(line_key, args)`), p. ej.
  `Expediente 000 …` para la factura del cap. 2 (`grep 11:04 …`).
- `lines_resolved`: lista con las líneas de auditoría formatadas.

El import `core/data/textos → resolve/load_textos` está permitido por
ADR-0001 (`data` no trae deps de core). `_resolve_auditor_text` es honesto:
si `data.textos` falla o devuelve vacío, devuelve la CLAVE cruda en lugar de
crash o de un hueco `{...}` — nunca rompe el cierre de la run. El REPL puede
imprimir la voz del Auditor HOY, sin esperar al render.
