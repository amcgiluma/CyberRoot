"""25/09 O1 — grep -c (P2 factura frugal).

AC del plan 25/09:
- grep -c cuenta (stdout N\\n, exit 0 si >0, 1 si 0)
- combinable -c -i / -cv / -- 
- estado honesto: -c válido, -F/-o/-l siguen invalid
- garantía e2: ps aux | grep -c censo → 1\\n exit0; ceniza → 0\\n exit1
- byte-idéntico sin flags
"""
from __future__ import annotations

from core.sandbox.commands.texto import _run_grep
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell


def _fs_a() -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={
        "a.txt": FileNode(name="a.txt", content="censo\nzzz\nCENSO\ncenso test\n"),
        "b.txt": FileNode(name="b.txt", content="ceniza\nzzz\n"),
    }))

def test_grep_c_stdin_cuenta():
    fs = FileSystem(root=DirNode(name="/", children={}))
    r = _run_grep(fs, "/", ("-c", "censo"), tick=0, stdin="a censo b\nzzz\ncenso\n")
    assert r.stdout == "2\n"
    assert r.exit_code == 0
    assert r.stderr == ""

def test_grep_c_ceniza_cero_exit1():
    fs = FileSystem(root=DirNode(name="/", children={}))
    r = _run_grep(fs, "/", ("-c", "ceniza"), tick=0, stdin="a censo b\nzzz\n")
    assert r.stdout == "0\n"
    assert r.exit_code == 1

def test_grep_c_con_fichero():
    fs = _fs_a()
    r = _run_grep(fs, "/", ("-c", "censo", "a.txt"), tick=0)
    assert r.stdout == "2\n"  # censo + censo test (CENSO no cuenta sin -i)
    assert r.exit_code == 0
    r2 = _run_grep(fs, "/", ("-c", "censo", "b.txt"), tick=0)
    assert r2.stdout == "0\n"
    assert r2.exit_code == 1

def test_grep_c_combinable_vi():
    fs = FileSystem(root=DirNode(name="/", children={}))
    # -c -v: invierte antes de contar
    r = _run_grep(fs, "/", ("-c", "-v", "censo"), tick=0, stdin="censo\nzzz\ncenso\n")
    assert r.stdout == "1\n"  # solo zzz
    assert r.exit_code == 0
    # -cv combinado
    r2 = _run_grep(fs, "/", ("-cv", "censo"), tick=0, stdin="censo\nzzz\ncenso\n")
    assert r2.stdout == "1\n"
    # -- separa
    r3 = _run_grep(fs, "/", ("-c", "--", "censo"), tick=0, stdin="censo\n")
    assert r3.stdout == "1\n"

def test_grep_c_combinable_i():
    fs = FileSystem(root=DirNode(name="/", children={}))
    r = _run_grep(fs, "/", ("-c", "-i", "censo"), tick=0, stdin="CENSO\ncenso\nzzz\n")
    assert r.stdout == "2\n"
    assert r.exit_code == 0
    # -ci combinado
    r2 = _run_grep(fs, "/", ("-ci", "CENSO"), tick=0, stdin="CENSO\ncenso\nzzz\n")
    assert r2.stdout == "2\n"
    # -c -i separados + -v
    r3 = _run_grep(fs, "/", ("-c", "-i", "-v", "censo"), tick=0, stdin="CENSO\ncenso\nzzz\n")
    assert r3.stdout == "1\n"  # solo zzz

def test_grep_c_pipe_shell_real():
    shell = Shell(fs=FileSystem(root=DirNode(name="/", children={})), commands=("ps","grep","cat","ls","wc","env","kill","sudo"))
    # sin intruso el ps no tiene censo → 0
    r = shell.execute("ps aux | grep -c censo")
    assert r.stdout == "0\n"
    assert r.exit_code == 1
    # con intruso via encargo real
    from core.curriculum import load_curriculum
    from core.engine.session import abrir_encargo
    cur = load_curriculum()
    sess = abrir_encargo(cur, "story.ch5.e2", {"c.cat","c.scp","c.grep"}, run_seed=42, volcado_rescatado=True)["session"]
    r2 = sess.ejecutar("ps aux | grep -c censo")
    assert r2.stdout == "1\n", f"got {r2.stdout!r}"
    assert r2.exit_code == 0
    r3 = sess.ejecutar("ps aux | grep -c ceniza")
    assert r3.stdout == "0\n"
    assert r3.exit_code == 1
    # combinado -c -i sobre encargo
    r4 = sess.ejecutar("ps aux | grep -c -i CENSO")
    assert r4.stdout == "1\n"
    assert r4.exit_code == 0

def test_grep_c_invalid_flags_siguen_invalid():
    fs = FileSystem(root=DirNode(name="/", children={}))
    r = _run_grep(fs, "/", ("-F", "censo"), tick=0, stdin="censo\n")
    assert r.exit_code == 2
    assert "invalid option" in r.stderr
    r2 = _run_grep(fs, "/", ("-o", "censo"), tick=0, stdin="censo\n")
    assert r2.exit_code == 2
    r3 = _run_grep(fs, "/", ("-l", "censo"), tick=0, stdin="censo\n")
    assert r3.exit_code == 2

def test_grep_c_sin_flags_byte_identico():
    fs = FileSystem(root=DirNode(name="/", children={"a.txt": FileNode(name="a.txt", content="hola\nHOLa\n")}))
    # sin -c sigue emitiendo líneas
    r = _run_grep(fs, "/", ("hola", "a.txt"), tick=0)
    assert r.stdout == "hola\n"
    assert r.exit_code == 0
    r2 = _run_grep(fs, "/", ("-i", "hola", "a.txt"), tick=0)
    assert r2.stdout == "hola\nHOLa\n"

def test_grep_c_via_stdin_y_fichero_mixto():
    # grep -c con fichero inexistente → exit 2 pero cuenta igual?
    fs = FileSystem(root=DirNode(name="/", children={"a.txt": FileNode(name="a.txt", content="censo\n")}))
    r = _run_grep(fs, "/", ("-c", "censo", "a.txt", "noexiste.txt"), tick=0)
    assert r.exit_code == 2
    assert "No such file" in r.stderr
    assert r.stdout == "1\n"
