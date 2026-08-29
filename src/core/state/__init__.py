"""core.state — el estado agregador y el guardado (ARCHITECTURE §2.6).

GameState serializable JSON ida-y-vuelta + save/load ATÓMICO versionado
desde el día 1. Único punto donde las piezas ensamblan; fachada que
consumirá `main.py`. v0 envuelve la Shell del cap. 0; el inventario de
conocimientos dominados (`knowledge`, alimentado por `core.progression`)
vive como sub-dict hermano de `"shell"`. Sin RNG, sin reloj real, sin
pyxel, stdlib only. Ver PLAN.md. Dueño: Seath (`feat/meta-ui`).

Fachada T1 (29/08): re-exporta `GameState`, `save_game` y `load_game`
(alias nombrados de `core.state.state`); los nombres de bajo nivel
`save`/`load` siguen disponibles desde ese submódulo.
"""

from core.state.state import GameState
from core.state.state import load as load_game
from core.state.state import save as save_game

__version__ = "0.1.0"

__all__ = ["GameState", "save_game", "load_game"]