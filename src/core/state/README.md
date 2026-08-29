# state/ — Estado agregador y guardado

> **Qué hace:** ensambla TODO lo persistente del juego en un único
> `GameState` serializable a JSON ida-y-vuelta. v0 (T1, 28/08) envuelve la
> Shell del cap. 0; los futuros hub/unlocks/karma/récords entrarán como
> sub-dicts hermanos de `"shell"` vía migración — GameState AGREGA, no
> aplana la sesión. Save/load ATÓMICO versionado desde el día 1.
>
> Normativa: INVESTIGACION-STACK («guardado como dato plano serializable») ·
> `../ARCHITECTURE.md` §2.6 · decisiones e hitos: `PLAN.md`.

## API (v1 del formato)

```python
from core.state.state import GameState, save, load, SAVE_VERSION
from core.state.state import SaveError, SaveVersionError, SaveIntegrityError

g = GameState(shell=la_shell)          # version=SAVE_VERSION (1) por defecto
d = g.to_dict()                        # {"version", "saved_at", "shell"}
g2 = GameState.from_dict(d)            # roundtrip in-memory exacto
save(g, "save.json")                   # ATÓMICO: tmp + os.replace
g3 = load("save.json")                 # valida versión, migra, reconstruye
```

**Fachada (T1, 29/08):** `from core.state import GameState, save_game,
load_game` (aliases nombrados de `save`/`load`). Los nombres de bajo nivel
siguen disponibles desde `core.state.state` para no romper los tests previos.
El save v1 camino a generalizarse: `GameState.knowledge` (dict boon→dominado,
alimentado por `core.progression`) es un sub-dict OPCIONAL hermano de
`"shell"` — un save v1 previo sin la clave carga con `{}`.

- **Formato del save**: `{"version": 1, "saved_at": <tick simulado>,
  "shell": <Shell.to_dict()>, "knowledge": {...}}` (`knowledge` opcional).
  `sort_keys` + `ensure_ascii=False`:
  JSON determinista y legible a mano (§1.5 — un save escrito a mano con
  `json.dump` carga exactamente igual).
- **`version`** int monotónico desde 1 (no semver: solo lo lee `from_dict`).
  `saved_at` es el tick SIMULADO de la Shell — core sin reloj real (§3).
- **Atomicidad**: `save()` escribe `<path>.tmp` en el mismo directorio y hace
  `os.replace`. Si la serialización falla (estado con valores no JSON-safe),
  lanza `SaveIntegrityError` y el save anterior queda INTACTO. Un `.tmp`
  residual tras un fallo es tolerado: el próximo save reutiliza el nombre.
- **Migraciones**: registro privado `_MIGRATIONS {v_origen: fn(dict)->dict}`,
  vacío en v1; `from_dict`/`load` aplican la cadena hasta `SAVE_VERSION`.
  Save sin cabecera `version` → `SaveVersionError` salvo migración v0
  registrada (probado white-box en tests).
- **Errores**: `SaveError` base → `SaveVersionError` (versión desconocida o
  ilegible, mensaje con el número recibido y el soportado) /
  `SaveIntegrityError` (JSON inválido, falta `"shell"`, sección shell rota,
  estado no serializable). `FileNotFoundError` de `load()` se propaga: el
  llamador decide qué hacer con un save ausente.

## Límite conocido v1

El set de comandos NO viaja en el save (contrato de `Shell.to_dict`:
`Shell.from_dict` reconstruye con el set default `DEFAULT_CAP0_COMMANDS`).
Cuando exista selección de set por capítulo, el set viajará en el save por
migración v2. Igualdad de estados a nivel de DICTS (`to_dict`): `Shell` no
define `__eq__`.

## Cómo se testea

`src/tests/core/state/test_state.py` — 10 tests: roundtrips (in-memory, JSON,
disco, doble), copia independiente, atomicidad (fallo de serialización deja
el save anterior intacto), JSON escrito a mano, migración sintética v0→v1
(white-box), rechazo de versiones desconocidas, y la sesión canónica del
cap. 0 (cat + cp proveedor→/usb, ruido 4) sobreviviendo entera.

```bash
./.venv/bin/python -m pytest src/tests/core/state -q
```

## Dueño

Seath (`feat/meta-ui`), junto a `progression/` y `karma/`.
