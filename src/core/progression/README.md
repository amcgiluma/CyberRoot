# progression/ — Metaprogresión: el Espejo de Gris

> **Qué hace:** todo lo que persiste entre runs — ramas del espejo (Hardware /
> Oficio / Red), recuerdos equipables, tienda de objetos de Gris, economía
> (créditos + favores narrativos), desbloqueos por competencia y récords
> personales.
>
> Normativa: `docs/DESIGN.md` §4.2–4.3 (regla dura y espejo), §7.5–7.6
> (unlocks/récords) · `../ARCHITECTURE.md` §2.7. Plan e hitos: `PLAN.md`.

## La regla dura que este módulo custodia
**El espejo da conveniencia e identidad de build, nunca conocimiento**
(§4.2): ninguna compra sustituye a un comando que el jugador no sabe usar.
Si una mejora propuesta rompe esto, se corta en diseño, no en código.

## v0 (T2, 29/08): el primer unlock por competencia respira
Una herramienta, no el árbol entero: `evaluate_unlocks(state)` inspecciona el
estado y marca dominado el concepto cuya competencia quedó DEMOSTRADA. La
evidencia se lee del historial de la sesión (nunca por grind ni por compra).

```python
from core.state import GameState
from core.progression import evaluate_unlocks, CAP0_CONTRACT_BOON

nuevos = evaluate_unlocks(state)          # [CAP0_CONTRACT_BOON] si lo domina ahora
state.save_game(state, "save.json")        # la dominación persiste en el save
```

- **Regla v0 — contrato del cap. 0 → `c.cp`:** si la sesión contiene un `cp`
  con `exit_code == 0` cuyo destino cae bajo `/usb` (la extracción canónica
  del dossier, §6.4.4), el concepto `c.cp` queda dominado en
  `state.knowledge`. Idempotente: llamadas repetidas no re-marcan.
- El inventario vive como `GameState.knowledge: dict[str, bool]`, sub-dict
  hermano de `"shell"` en el save (GameState agrega, no aplana). Un save v1
  previo sin la clave carga con `knowledge == {}` (campo opcional en el
  formato, documentado en `PLAN.md`).
- `progression` NO importa `core.state` en runtime (solo `TYPE_CHECKING`):
  recibe el `GameState` por composición y escribe `state.knowledge`. El que
  conecta ambos es el orquestador (`game.py` futuro) o el test.

## Responsabilidades (casta completa — fuera de v0)
- Compras y equipamiento (objetos ~12, perks ~8, recuerdos por NPC).
- Desbloqueos POR COMPETENCIA (§7.5.3): usa bien X en contexto → siguiente
  tarjeta de la familia; JAMÁS por grind de créditos.
- Récords personales persistentes (mejor combo, pipeline más largo, sala más
  valiosa — §7.6). Sin leaderboard, nunca.
- Señales kármicas de stock (§3.3 canal 1): el inventario ofertado por Gris
  depende del perfil — la lógica lee `karma.py`; los textos viven en `data/`.

## v0.2 (T1+T2, 30/08/2026): el save recuerda CUÁNDO dominaste + logros

**T1 (P2) — meta de unlock + resumen de competencia (prepara 🧭9).** El unlock
de ayer era data muda. Ahora `evaluate_unlocks` guarda el MOMENTO del dominio
(`state.mastered[boon] = {"tick": …, "order": …}`: tick simulado al detectarse +
secuencia monótona) y se expone el resumen:

```python
from core.progression import evaluate_unlocks, resumen_competencia

nuevos = evaluate_unlocks(state)          # [CAP0_CONTRACT_BOON] + marca mastered
res = resumen_competencia(state)          # {"dominados":[{concepto,tick,order}…],
                                          #  "factura":{por_comando, totals}}
```
SIN UI ni forma (eso lo decide Gwyn): `resumen_competencia` entrega SOLO los
datos con los que el Hub/tienda pintará el eco. La `factura` es la GNU de la
sesión (§7.2/🧭10): usos/ruido/errores por comando, en la misma unidad que el
noise_budget.

**T2 (P3) — Mecanismo de logros por factura.** `evaluate_logros(state) -> list`:
«Cero rastro» (cap. 0 completo con `total_noise ≤ UMBRAL_CERO_RASTRO`) y
«Mano de seda» (extracción sin ni un `exit != 0`). Persisten en
`state.logros` (dict id→True, roundtrip). Umbral ⚠️ v1 calibrable (cliente: O3
del harness). Sin popup moral: el logro es un dato del save.

- `mastered` y `logros` son sub-dicts OPCIONALES hermanos de `"shell"` en el
  save v1: un save previo sin ellos carga con `{}` (backward-compat, como
  `knowledge`). No se sube SAVE_VERSION (campo opcional documentado, §2.6).

## Cómo se testea
- Unlock por competencia: sin uso real NO hay unlock aunque sobren créditos
  (`test_progression.py` — 17 tests: desbloqueo, idempotencia, sesión parcial/
  vacía sin desbloquear, persistencia en save, roundtrip exacto, save v1
  previo con inventario vacío, + momento del dominio, resumen de competencia
  (canónica/factura/legado) y logros (ambos, idempotencia, ruido extra, error,
  persistencia)).
- Economía: comprar/equipar/cobrar — aritmética exacta y persistente.
- Stock contrastado: perfil azul vs rojo forzados → ofertas distintas.

```bash
./.venv/bin/python -m pytest src/tests/core/progression -q
```

## Dueño
Seath (`feat/meta-ui`), junto a `state/` y `karma/`.