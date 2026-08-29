# PLAN — T1+T2 · 29/08 (Seath, 19:00, `feat/meta-ui`)

> Origen: plan de Gwyndolin del 29/08 (tareas T1 y T2). La rama partió de una
> base VIEJA (21 commits detrás de main, el trabajo del 28/08 ya estaba
> mergeado como PR #6); primero `git fetch && git rebase origin/main` → HEAD
> == main (0/0, **316 passed**). Mi plan desglosa el detalle que Gwyndolin no puso.

## Encargo y alcance

- **T1 (P2) — Fachadas uniformes.** `core.state` y `core.sandbox` re-exportan
  su API desde el paquete. Solo ~~dos~~ tres ficheros: `state/__init__.py`,
  `sandbox/__init__.py`. Sin tocar lógica.
- **T2 (P2) — progression v0: primer unlock por competencia.** Paquete
  `core/progression/` nuevo + un campo serializable en `GameState`.
- NO toco: `common/`, `engine/`, `generator/`, `karma/`, `render/`, `assets/`,
  ni `sandbox/commands/` (Smough). Rutas disjuntas garantizadas. El
  `__init__.py` de sandbox es MÍO (re-export) — Smough no toca ese fichero.

## Contratos que consumo

- `Shell.execute(line)` muta `cwd/tick/history/total_noise`; `to_dict/from_dict`
  ida y vuelta exacta. El historial guarda `{"line": <str>, "result": <CommandResult.to_dict()>}`
  (NO guarda argv: la evidencia del unlock se lee parseando `line`).
- `CommandResult.to_dict()`: `{stdout, stderr, exit_code, noise, new_cwd}`.
- `GameState(shell=..., version=..., knowledge=...)` dato plano (§1.5).

## Diseño (una decisión, un racional)

- **Fachadas por ALIAS**: `from core.state import GameState, save_game, load_game`.
  Los nombres de bajo nivel `save`/`load` de `core.state.state` se conservan
  para no romper los 10 tests existentes; la fachada pública nombra `save_game/
  load_game` (el contrato que consume `main.py`). `from core.sandbox import Shell`.
- **`knowledge` en GameState como `dict[str, bool]`** (inventario de boons/
  competencias dominadas, id → dominado). Sub-dict hermano de `"shell"` en el
  save (GameState agrega, no aplana — coherente con la decisión v1 del estado).
- **Backward-compat v1**: `from_dict` lee `d.get("knowledge", {})` → un save
  v1 previo (sin la clave) carga con `knowledge == {}`. No subo `SAVE_VERSION`
  a 2 (rompería los tests de migración existentes y no hay usuarios reales);
  es un campo OPCIONAL en el formato, documentado.
- **Progression NO importa `core.state` en runtime** (solo `TYPE_CHECKING`):
  recibe el `GameState` por composición, lee `state.shell.history` (evidencia)
  y escribe `state.knowledge`. Así no hay ciclo state↔progression; quien
  conecta ambos es el orquestador (`game.py` futuro) o el test.
- **Evidencia del contrato del cap. 0**: un `cp` con `exit_code == 0` en el
  historial cuyo destino (último argv) cae bajo `/usb` (la extracción canónica
  del dossier §6.4.4 hace `cp <oficina>/<proveedor> /usb/`). Detecta
  "contrato completado" SOLO desde el estado, sin depender de generator/engine.

## Hitos (secuenciales; H3-H5 pequeños y dominados → los hago directo)

- **H1** — Rama al día (rebase a main) + identidad git `Seath`. ✅
- **H2** — T1 fachadas: `state/__init__.py` + `sandbox/__init__.py`.
  Hecho si: `from core.state import GameState, save_game, load_game` y
  `from core.sandbox import Shell` funcionan con `PYTHONPATH=src`.
- **H3** — T2 estado: campo `knowledge` en `GameState` (to_dict/from_dict).
  Hecho si: roundtrip v1 previo sin `knowledge` → `{}`; save nuevo conserva el dict.
- **H4** — T2 módulo: `core/progression/{__init__.py, progression.py}` con
  `evaluate_unlocks(state) -> list[str]` idempotente.
  Hecho si: cap-0 completado → marca `c.cp`; parcial/sin historial → no.
- **H5** — Tests: `src/tests/core/state/test_fachada.py` (facade) +
  `src/tests/core/progression/test_progression.py` (7 tests). Suite completa verde.
  Hecho si: `PYTHONPATH=src python -m pytest` verde, delta 316→+_.

## Los tests

- T1 (fachada, `test_fachada.py`): expose API state, expose Shell, roundtrip
  disco vía `save_game/load_game`.
- T2 (`test_progression.py`): cap-0 completo marca `c.cp`; idempotente (2.ª
  llamada `[]`); sesión parcial NO desbloquea; shell vacía NO desbloquea;
  persiste en save (load lo recupera); roundtrip exacto de `knowledge`;
  save v1 previo sin `knowledge` → `{}`.
- Reutilizo la piel del cap. 0 SIN importar de `src/tests/core/sandbox/` (regla O1).

## Riesgos y bordes

- Igualdad a nivel de dicts (`Knowledge` por dict, sin `__eq__`). Documentado.
- `_parsed_argv` tolera líneas no parseables tirando del historial con shlex
  (stdlib, permitido por `test_core_stdlib_only.py`).
- El unlock marca presence dict; no hay "árbol entero" ni espejo completo en
  v0 — UNA regla, estructura de funciones preparada para ampliar.

— Seath, 19:00 (29/08/2026)