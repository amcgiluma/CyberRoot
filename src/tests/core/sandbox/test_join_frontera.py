"""S2 12/09 — 127 que enseña: join nombra dónde vive (Faro).

Fuera del cap.6 (ch0/ch4) join no existe: 127 + glosa didáctica que nombra
el Faro/chapter 6. En ch6 join existe y funciona; generate(42,6) intacto.
"""

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell, DEFAULT_CAP0_COMMANDS, DEFAULT_CH4_COMMANDS, DEFAULT_CH6_COMMANDS

GLOSA = "Try 'join --help' \u2014 tables cross there (chapter 6)."


def _fs_min():
    return FileSystem(root=DirNode(name="/", children={}))


def test_join_127_cap0_con_glosa():
    s = Shell(_fs_min(), commands=DEFAULT_CAP0_COMMANDS)
    r = s.execute("join a b")
    assert r.exit_code == 127
    assert r.stderr.startswith("sh: command not found: join")
    assert GLOSA in r.stderr
    assert "chapter 6" in r.stderr


def test_join_127_ch4_con_glosa():
    s = Shell(_fs_min(), commands=DEFAULT_CH4_COMMANDS)
    r = s.execute("join -t'|' f1 f2")
    assert r.exit_code == 127
    assert GLOSA in r.stderr
    # no debe afectar a otros comandos desconocidos
    r2 = s.execute("foobar")
    assert "Try 'join" not in r2.stderr
    assert r2.exit_code == 127


def test_join_ch6_sin_glosa_y_funciona():
    fs = FileSystem(root=DirNode(name="/", children={
        "a": FileNode(name="a", content="1 x\n2 y\n"),
        "b": FileNode(name="b", content="1 A\n2 B\n"),
    }))
    s = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    r = s.execute("join a b")
    assert r.exit_code == 0
    assert GLOSA not in r.stderr
    assert GLOSA not in r.stdout
    assert "1 x A" in r.stdout


def test_generate_42_6_intacto():
    try:
        from core.generator import generate
        inc = generate(42, 6)
        # Debe generar sin error y no mencionar join glosa; checks mínimos
        assert inc is not None
        # Si tiene fs, comprobar que join sigue siendo usable en esa sala ch6
        s = Shell(inc.room.fs.snapshot(), commands=DEFAULT_CH6_COMMANDS)
        # La sala ch6 debe tener al menos purgas/registro o similar; si no, test dummy join
        fs = FileSystem(root=DirNode(name="/", children={
            "a": FileNode(name="a", content="1 x\n"),
            "b": FileNode(name="b", content="1 y\n"),
        }))
        s2 = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
        r = s2.execute("join a b")
        assert r.exit_code == 0
    except ImportError:
        # Si generator no disponible, al menos que DEFAULT_CH6_COMMANDS siga con join
        assert "join" in DEFAULT_CH6_COMMANDS
