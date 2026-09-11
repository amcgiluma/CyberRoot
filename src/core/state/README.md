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
  "shell": <Shell.to_dict()>, "knowledge": {...}, "mastered": {...},
  "logros": {...}}` (`knowledge`/`mastered`/`logros` OPCIONALES, sub-dicts
  hermanos de "shell"; un save v1 previo sin ellos carga con `{}`).
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

`src/tests/core/state/test_state_red.py` — 3 tests: `cat /etc/hosts` descubre
`faro`, `known_hosts` persiste, sin hosts vacío (red Fase A, S1 07/09).

`src/tests/core/state/test_state_scp_roundtrip.py` — 3 tests (T2 08/09, Seath):
el efecto `scp` entre FS del stack (`faro:… ↔ /tmp/`) sobrevive
`GameState.to_dict/from_dict` idéntico; si S1 no está mergeado,
stub honesto con `hosts` FS inyectado (`hasattr(Shell,"_exec_scp")` guard).

`src/tests/core/state/test_ch4_circuit.py` — 5 tests (T1 09/09, Seath):
circuito ch4 multi-host (handmade 2 y 3 hosts + generator condicional si `chapter4.py` está)
y dato EXACTO del límite de 2 pipes (`tail|cut|sort|uniq -c` rechazado exit 2 con
`multiple pipelines not supported: chain them one at a time`; `tail|cut|sort` permitido).
Suite 635→639 (+4) / 1 skipped honesto hasta O1 mergeado.

`src/tests/core/state/test_ch6_datos_circuit.py` — 7 tests (T1 10/09, Seath):
circuito datos ch6 — dato4 `join -t'|' -1 3 -2 1 -v 1` handmade + generator condicional,
dato5 `ps aux | grep 11:04` START forense 11:04 determinista por seed (3 procesos, binario
compartido `faro-sync`), GameState roundtrip con procesos (límite v1: set no viaja, FS sí),
gate flexible 23/25→24/27 + pipe 2 permitido / 4 rechazado `multiple pipelines not supported`.
Suite 648→655 (+7) sobre base realineada; fallback handmade si O1/S2 no mergeados.

`src/tests/core/state/test_ch4_e2_circuit.py` — 7 tests (T1 11/09, Seath):
circuito ch4 completo e1+e2 + guard frontera — regresión e1 intacta con e2 (`generate(42,4)`→e1),
e2 por contract `story.ch4.e2` golden 2 pasos `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` +
`cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → `TR-001/TR-002/TR-003` sin header (1 pipe filtro positivo,
`TR-003|EN_COLA` pista de lo que no pesa), allowlist CH4 SUBSET guard (`<= set(13 cmds)` nunca `==`, lección 10/09),
`tail/sort/uniq/head` en ch4 → 127 frontera deliberada, GameState roundtrip con ch4 multi-host,
pipe 2 OK / 4 rechazado `multiple pipelines not supported`, gate flexible 24/27↔24/28.
Suite 680→687 (+7) sobre base realineada; fallback handmade si S2 no mergeado.

```bash
./.venv/bin/python -m pytest src/tests/core/state -q
```

## Dueño

Seath (`feat/meta-ui`), junto a `progression/` y `karma/`.
