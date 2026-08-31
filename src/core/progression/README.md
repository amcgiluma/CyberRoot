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

## v0.3 (T1+T2, 31/08/2026): recalibrado 🧭11 + eco 🧭9 pre-render

**T1 (P2, 🧭11) — recalibrado «Cero rastro».** `UMBRAL_CERO_RASTRO` pasa de 4
→ 5 y «Cero rastro» exige además factura limpia (`_no_exit_errors`). Datos
medidos 31/08 por Oscar y Havel, independientes: min honesto = 5, canónico
§6.4.4 = 6, puro `cp` memorizado = 3. El umbral 4 era imposible de ganar
honesto (la canónica cierra en 6). Con 5, la canónica NO lo gana y un
min-honesto sin errores SÍ. «Cero rastro» = frugalidad + pulcritud; «Mano de
seda» (solo ausencia de errores) queda intacto y distinto. Gwyn valida al
mergear (puede rectificar con el mismo dato a otra opción de 🧭11: medir solo
la extracción — cambio de una constante + una condición, mismo coste).

**T2 (P2, 🧭9) — eco pre-render: `evaluate_unlocks` emite `progression.unlocked`**
al bus común. Al dominar un concepto, emite `{"concepto", "tick", "order"}`
(los tres datos ya viven en `state.mastered` desde T1/PR #12). La forma del eco
(firmada por Gwyn en DESIGN §6.1: diegético, cap. 1, Gris nombra lo dominado,
prohibido el toast de sistema) la pintará el render futuro SIN tocar el core —
el render solo se suscribe a este tipo. ⚠️ Frontera respetada: la constante
`UNLOCK_EVENT_TYPE` vive en `progression/`, NO se toca `common/` (de Ornstein);
el parámetro `bus` es OPCIONAL (None = comportamiento previo, backward-compat).
`evaluate_unlocks(state, *, bus=None) -> list[str]`.

## Cómo se testea
- Unlock por competencia: sin uso real NO hay unlock aunque sobren créditos
  (`test_progression.py` — 22 tests: desbloqueo, idempotencia, sesión parcial/
  vacía sin desbloquear, eco 🧭9 (payload, sin bus, re-evaluar no re-emite),
  persistencia en save, roundtrip exacto, save v1 previo con inventario vacío,
  + momento del dominio, resumen de competencia (canónica/factura/legado) y
  logros (ambos, idempotencia, ruido extra >5, ruido 6 no gana, min-honesto
  ruido 5 gana, error mata ambos, persistencia)).
- Economía: comprar/equipar/cobrar — aritmética exacta y persistente.
- Stock contrastado: perfil azul vs rojo forzados → ofertas distintas.

```bash
./.venv/bin/python -m pytest src/tests/core/progression -q
```

## Dueño
Seath (`feat/meta-ui`), junto a `state/` y `karma/`.