"""test_stat.py — stat como lector del testigo 03:14/512 (S1 21/09, Smough).

AC del plan T3:
- stat /tmp/volcado-custodia.csv → exit 0 con Modify: 03:14:00 + Size: 512 si rescate
- stat mismo path → exit 1 cannot stat No such file si caducado
- stat fuera de allowlist CH5 → 127 honesto (no entra en DEFAULT_CH5*)
- boon c.stat en curriculum, help.stat en textos
"""
from core.curriculum import load_curriculum
from core.generator.chapter5 import build_chapter5_fs
from core.sandbox.commands.stat import _run_stat
from core.sandbox.shell import Shell, DEFAULT_CH5_COMMANDS, DEFAULT_CH5E1_COMMANDS, DEFAULT_CH5E3_COMMANDS


def test_stat_rescate_muestra_03_14_y_512() -> None:
    fs = build_chapter5_fs(None, volcado_rescatado=True)
    res = _run_stat(fs, "/", ("/tmp/volcado-custodia.csv",), 0)
    assert res.exit_code == 0
    assert "Modify: 2025-09-21 03:14:00" in res.stdout or "Modify: 03:14:00" in res.stdout
    assert "Size: 512" in res.stdout
    assert res.stderr == ""


def test_stat_caducado_cannot_stat_exit_1() -> None:
    fs = build_chapter5_fs(None, volcado_rescatado=False)
    res = _run_stat(fs, "/", ("/tmp/volcado-custodia.csv",), 0)
    assert res.exit_code == 1
    assert "cannot stat" in res.stderr
    assert "No such file" in res.stderr
    assert res.stdout == ""


def test_stat_no_esta_en_allowlist_ch5_base_y_e1_e3() -> None:
    """Stat NO entra en las allowlists del cap.5 → 127 honesto fuera de encargo."""
    assert "stat" not in DEFAULT_CH5_COMMANDS
    assert "stat" not in DEFAULT_CH5E1_COMMANDS
    assert "stat" not in DEFAULT_CH5E3_COMMANDS
    # Shell base ch5 → stat debe dar 127
    from core.sandbox.fs import FileSystem, DirNode
    fs = FileSystem(root=DirNode(name="/", children={}))
    shell = Shell(fs, commands=DEFAULT_CH5_COMMANDS)
    res = shell.execute("stat /tmp/volcado-custodia.csv")
    assert res.exit_code == 127
    assert "command not found" in res.stderr
    # Shell con stat sí funciona (para el jugador que lo aprende fuera de encargo)
    shell2 = Shell(fs, commands=("stat", "cat"))
    # sin fichero → exit 1, no 127
    res2 = shell2.execute("stat /tmp/volcado-custodia.csv")
    assert res2.exit_code == 1
    assert "cannot stat" in res2.stderr


def test_curriculum_tiene_c_stat_y_textos_help_stat() -> None:
    cur = load_curriculum()
    c = cur.concept("c.stat")
    assert c is not None
    assert c.family == "hallazgo"
    assert c.prerequisites == ("c.ls",) or list(c.prerequisites) == ["c.ls"]
    assert c.chapter == 1
    # textos
    import json, pathlib
    textos = json.loads(pathlib.Path("src/data/textos.json").read_text(encoding="utf-8"))
    assert "help.stat" in textos["texts"]
    assert "concept.stat.summary" in textos["texts"]
    assert "03:14" in textos["texts"]["help.stat"]
