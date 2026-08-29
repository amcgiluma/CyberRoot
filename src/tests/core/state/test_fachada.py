"""T1 — fachadas uniformes: core.state y core.sandbox re-exportan su API.

AC de Gwyndolin (plan 29/08): `from core.state import GameState, save_game,
load_game` y `from core.sandbox import Shell` funcionan desde raíz con
`PYTHONPATH=src`; sin imports circulares; suite verde.
"""

from __future__ import annotations

from core.sandbox import Shell
from core.sandbox.fs import DirNode, FileSystem
from core.state import GameState, load_game, save_game


def _empty_state() -> GameState:
    return GameState(shell=Shell(FileSystem(root=DirNode(name="/"))))


def test_state_facade_exposes_api() -> None:
    """La fachada de `core.state` expone GameState y los guardados nombrados."""
    g = _empty_state()
    assert isinstance(g, GameState)
    assert callable(save_game)
    assert callable(load_game)


def test_sandbox_facade_exposes_shell() -> None:
    """La fachada de `core.sandbox` expone Shell."""
    s = Shell(FileSystem(root=DirNode(name="/")))
    assert isinstance(s, Shell)
    assert s.cwd == "/"


def test_facade_save_load_game_roundtrip(tmp_path) -> None:
    """save_game/load_game (fachada) guardan y recuperan el estado ida y vuelta."""
    g = _empty_state()
    g.shell.execute("cd /srv")  # deja una huella en history/tick
    p = tmp_path / "save.json"
    save_game(g, p)
    g2 = load_game(p)
    assert g2.to_dict() == g.to_dict()
    assert g2.version == 1