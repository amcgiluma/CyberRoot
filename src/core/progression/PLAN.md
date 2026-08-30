# PLAN — T1+T2 · 30/08 (Seath, 19:00, `feat/meta-ui`)

> Origen: plan de Gwyndolin del 30/08 (tareas T1 y T2). Rama
> `feat/meta-ui-2026-08-30` creada desde `origin/main` limpia (0 commits detrás)
> — el shell cron arrastraba `feat/sandbox-2026-08-30` (de Smough), no reutilizo
> rama ajena. Suite base realineada: **342 passed + 1 xfailed** (el xfail es la
> costura de Ornstein, muere hoy en SU rama, no es mío). Mi plan desglosa el
> detalle que Gwyndolin no puso.

## Encargo y alcance
- **T1 (P2) — El save recuerda CUÁNDO dominaste:** meta de unlock (tick/orden)
  + `resumen_competencia(state)`. Prepara 🧭9 SIN UI ni forma (eso es de Gwyn).
- **T2 (P3, ^si T1 cierra con holgura^) — Logros por factura:** mecanismo
  + 2 logros definidos ("Cero rastro", "Mano de seda"), evaluados tras la run
  canónica, persisten en el save.
- Solo toco: `src/core/state/state.py` (campo nuevo) + `src/core/progression/`
  + tests en `src/tests/core/progression/` + `src/tests/core/state/`. NO toco
  sandbox/engine/generator/karma/render/assets (Ornstein/Smough).

## Contratos que consumo
- `Shell.execute` muta `cwd/tick/history/total_noise`; `history[i]` =
  `{"line": str, "result": CommandResult.to_dict()}` (noise serializado como
  lista de `Event.to_dict()` → `data["amount"]`).
- `Shell.tick` = tiempo SIMULADO (§3); es el "momento" natural del dominio.
- `GameState` agrega sub-dicts hermanos de `"shell"` (v1): `knowledge` ya vive
  ahí. `progression` NO importa `core.state` en runtime (solo TYPE_CHECKING).

## Diseño (una decisión, un racional)
- **`mastered: dict[boon → {"tick": int, "order": int}]`** en `GameState`.
  `knowledge` sigue siendo la fuente de verdad de "quién domina"; `mastered`
  le añade el MOMENTO. Backward-compat v1: save previo sin `mastered` carga
  `{}`; `resumen_competencia` muestra `tick/order = None` para un boon ya
  dominado sin meta (save legado). No subo SAVE_VERSION a 2 (como en el 29/08):
  campo OPCIONAL documentado.
- **`order`**: secuencia de dominio = `len(state.mastered) + 1` al registrarse
  (monótono). `tick` = `state.shell.tick` en el momento de la detección (el
  tick ya avanzado tras el comando que demuestra el dominio).
- **`resumen_competencia(state) -> dict`** devuelve `{"dominados": [...],
  "factura": {...}}`. `dominados` = [{concepto, tick, order}] ordenado por
  order/concepto. `factura` = GNU de la sesión (§7.2/🧭10): `{por_comando:
  {cmd: {usos, ruido, errores}}, total_usos, total_ruido, total_errores}`.
- **`logros`**: `dict[str, bool]` en `GameState` (opcional v1). Constantes
  `LOGRO_CERO_RASTRO` / `LOGRO_MANO_SEDA` + `UMBRAL_CERO_RASTRO = 4` ⚠️ v1
  calibrable (cliente O3). Sin popup moral: el logro es un dato del save.

## Hitos (secuenciales; pequeños y dominados → los hago directo, sin delegar)
- **H1** — Rama limpia + identidad `Seath` + plan escrito. ✅
- **H2** — `state.py`: campos `mastered` + `logros` (to_dict/from_dict).
  Hecho si: roundtrip exacto; save v1 previo sin ellos carga `{}`.
- **H3** — `progression.py`: registrar momento en `evaluate_unlocks` (idempotencia
  intacta) + `resumen_competencia` + `_factura_capitulo`.
  Hecho si: run canónica → mastered[c.cp]={tick:2, order:1}; resumen coherente.
- **H4** — `progression.py`: `evaluate_logros` (Cero rastro / Mano de seda).
  Hecho si: canónica gana ambos; ruido extra mata Cero; error mata Mano.
- **H5** — `__init__.py` re-exporta los símbolos nuevos.
- **H6** — Tests en `test_progression.py` (+1 en `test_state.py`); suite completa
  verde. Hecho si: progression+state verdes y `pytest src/tests` = base + delta.

## Los tests (nuevos)
- T1: registra momento (tick/order); roundtrip de `mastered`; save v1 previo →
  `{}`; `resumen_competencia` canónica (dominados + factura cat:1/cp:3, ruido 4);
  resumen legado sin momento → tick/order None.
- T2: canónica gana ambos logros; idempotente; +`ls` (ruido 5) → solo Mano;
  comando con error → solo Cero; logros persisten en save (load los recupera).
- `test_state.py`: roundtrip de los campos opcionales nuevos.

## Riesgos y bordes
- Igualdad a nivel de dicts (sin `__eq__`), igual que v1.
- Factura parsea `line` con shlex (stdlib, permitido); líneas no parseables →
  comando `"sh"` (no rompe la suma).
- Un boon dominado en save legano (knowledge=True, sin mastered) → el momento
  es None, no se inventa.
- Delta del PR: base 342 + 1 xfail → los +N míos; el xfail muere en la rama de
  Ornstein, no en la mía. N = nº de funciones de test nuevas.

— Seath, 19:00 (30/08/2026)