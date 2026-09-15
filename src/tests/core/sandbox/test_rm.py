"""S1 15/09 — handler rm + allowlist e3 + serializable (ADR TR-003).

8 tests del criterio S1 (repartidos 5 aquí + 3 en test_volcado_rescate.py):
1) rm fichero exit 0 y desaparece de ls
2) rm sin args → exit 1
3) rm dir → exit 1 Is a directory
4) rm -r|-f → exit 1 invalid option
5) roundtrip serializable tras rm
"""
from __future__ import annotations

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell, DEFAULT_CH4_COMMANDS, DEFAULT_CH4E3_COMMANDS
from core.sandbox.noise import NOISE_PROFILE


def _fs_tmp_volcado() -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={
        "tmp": DirNode(name="tmp", children={
            "volcado.csv": FileNode(name="volcado.csv", content="TR-003|faro|troncal-01|512|EN_COLA\n"),
            "otro.txt": FileNode(name="otro.txt", content="hola\n"),
        }),
        "srv": DirNode(name="srv", children={}),
    }))

def test_rm_fichero_exit0_y_desaparece():
    fs = _fs_tmp_volcado()
    shell = Shell(fs, commands=DEFAULT_CH4E3_COMMANDS)
    assert "rm" in shell.available_commands
    assert NOISE_PROFILE["rm"] == 2
    r = shell.execute("rm /tmp/volcado.csv")
    assert r.exit_code == 0, r.stderr
    assert r.stderr == ""
    # desaparece de ls
    r2 = shell.execute("ls /tmp")
    assert "volcado.csv" not in r2.stdout
    assert "otro.txt" in r2.stdout
    # cat debe fallar
    r3 = shell.execute("cat /tmp/volcado.csv")
    assert r3.exit_code == 1
    assert "No such file" in r3.stderr or "not_found" in r3.stderr.lower() or r3.stderr != ""

def test_rm_sin_args_exit1():
    shell = Shell(_fs_tmp_volcado(), commands=DEFAULT_CH4E3_COMMANDS)
    r = shell.execute("rm")
    assert r.exit_code == 1
    assert "missing operand" in r.stderr

def test_rm_dir_exit1_is_a_directory():
    fs = FileSystem(root=DirNode(name="/", children={
        "tmp": DirNode(name="tmp", children={
            "subdir": DirNode(name="subdir", children={}),
        })
    }))
    shell = Shell(fs, commands=DEFAULT_CH4E3_COMMANDS)
    r = shell.execute("rm /tmp/subdir")
    assert r.exit_code == 1
    assert "Is a directory" in r.stderr
    # con barra final igual
    r2 = shell.execute("rm /tmp/subdir/")
    assert r2.exit_code == 1
    assert "Is a directory" in r2.stderr

def test_rm_flag_invalida_exit1():
    shell = Shell(_fs_tmp_volcado(), commands=DEFAULT_CH4E3_COMMANDS)
    for flag in ("-r", "-f", "-rf", "-i", "-r /tmp/volcado.csv"):
        r = shell.execute(f"rm {flag}")
        assert r.exit_code == 1, flag
        assert "invalid option" in r.stderr, f"{flag} -> {r.stderr!r}"

def test_rm_roundtrip_serializable():
    fs = _fs_tmp_volcado()
    shell = Shell(fs, commands=DEFAULT_CH4E3_COMMANDS)
    shell.execute("rm /tmp/volcado.csv")
    d = shell.to_dict()
    restored = Shell.from_dict(d)
    # byte-idéntico ANTES de ejecutar nada más
    assert restored.to_dict() == d
    # el fichero sigue borrado tras restore
    r = restored.execute("ls /tmp")
    assert "volcado.csv" not in r.stdout
    assert "otro.txt" in r.stdout
    # rm en allowlist base debe ser 127
    shell_base = Shell(FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={"a": FileNode(name="a", content="x")})})), commands=DEFAULT_CH4_COMMANDS)
    assert "rm" not in shell_base.available_commands
    r127 = shell_base.execute("rm /tmp/a")
    assert r127.exit_code == 127

def test_rm_multi_args_exit1():
    shell = Shell(_fs_tmp_volcado(), commands=DEFAULT_CH4E3_COMMANDS)
    r = shell.execute("rm /tmp/volcado.csv /tmp/otro.txt")
    assert r.exit_code == 1
    assert "too many" in r.stderr.lower()
