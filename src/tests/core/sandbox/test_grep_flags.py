"""22/09 S1 — grep -v / -i (BUG 🧭27).

AC del plan Gwyndolin:
1. `grep -v sujeto purgas.csv` → exit 0 filtra header
2. `ps aux | grep -v root` → exit 0 vía pipe
3. `grep -i` insensible
4. `grep` sin flags byte-idéntico (cap.2 no rompe)
5. combinado -vi / -iv
Delta esperado +5±2 (aquí 6 tests, dentro del margen; 5 cubren AC, 1 cubre exit 1 invertido).
"""

from __future__ import annotations

from core.sandbox.commands.texto import _run_grep
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell


def _fs_purgas() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "data": DirNode(
                    name="data",
                    children={
                        "purgas.csv": FileNode(
                            name="purgas.csv",
                            content="sujeto,distrito,estado\n001,muelles,activo\n002,faro,activo\nsujeto_test,umbral,baja\n",
                        ),
                    },
                ),
            },
        )
    )


def test_grep_v_filtra_header():
    fs = _fs_purgas()
    res = _run_grep(fs, "/", ("-v", "sujeto", "data/purgas.csv"), tick=0)
    assert res.exit_code == 0
    # header y sujeto_test contienen "sujeto" → filtrados; quedan 2 líneas
    assert res.stdout == "001,muelles,activo\n002,faro,activo\n"


def test_grep_v_pipe_ps_aux():
    # `ps aux | grep -v root` vía shell pipe real (stdin)
    shell = Shell(
        fs=FileSystem(root=DirNode(name="/", children={})),
        commands=("ps", "grep", "cat", "ls", "wc", "env", "kill", "sudo"),
    )
    res = shell.execute("ps aux | grep -v root")
    assert res.exit_code == 0
    # al menos una línea sin "root" (cabecera USER)
    assert "USER" in res.stdout or "operator" in res.stdout
    assert res.stderr == ""


def test_grep_i_insensible():
    fs = FileSystem(root=DirNode(name="/", children={
        "a.txt": FileNode(name="a.txt", content="Hola\nHOLA\nhola\nzzz\n")
    }))
    res = _run_grep(fs, "/", ("-i", "hola", "a.txt"), tick=0)
    assert res.exit_code == 0
    assert res.stdout == "Hola\nHOLA\nhola\n"
    # sin -i solo minúsculas exactas
    res2 = _run_grep(fs, "/", ("hola", "a.txt"), tick=0)
    assert res2.stdout == "hola\n"


def test_grep_vi_combinado():
    fs = FileSystem(root=DirNode(name="/", children={
        "a.txt": FileNode(name="a.txt", content="Hola\nHOLA\nhola\nzzz\n")
    }))
    # -v -i separados
    r1 = _run_grep(fs, "/", ("-v", "-i", "hola", "a.txt"), tick=0)
    assert r1.exit_code == 0
    assert r1.stdout == "zzz\n"
    # -vi combinado
    r2 = _run_grep(fs, "/", ("-vi", "hola", "a.txt"), tick=0)
    assert r2.stdout == "zzz\n"
    # -iv combinado
    r3 = _run_grep(fs, "/", ("-iv", "HOLA", "a.txt"), tick=0)
    assert r3.stdout == "zzz\n"


def test_grep_sin_flags_byte_identico():
    # Re-ejecuta golden central: byte-idéntico sin flags
    fs = FileSystem(root=DirNode(name="/", children={
        "srv": DirNode(name="srv", children={
            "centralita": DirNode(name="centralita", children={
                "turnos": DirNode(name="turnos", children={
                    "turno.log": FileNode(name="turno.log", content="11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt\n11:04 sesion 000 ruido 1 objetivo -\n08:59 turno de manana\n")
                })
            })
        })
    }))
    res = _run_grep(fs, "/", ("11:04", "srv/centralita/turnos/turno.log"), tick=0)
    assert res.exit_code == 0
    assert res.stdout == "11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt\n11:04 sesion 000 ruido 1 objetivo -\n"
    # stdin vía pipe sin flags también byte-idéntico
    res2 = _run_grep(fs, "/", ("11:04",), tick=0, stdin="11:04 a\nzzz\n11:04 b\n")
    assert res2.stdout == "11:04 a\n11:04 b\n"


def test_grep_v_exit_1_si_todo_matchea():
    fs = FileSystem(root=DirNode(name="/", children={
        "a.txt": FileNode(name="a.txt", content="sujeto\nsujeto\n")
    }))
    # -v deja 0 líneas → exit 1 (GNU)
    res = _run_grep(fs, "/", ("-v", "sujeto", "a.txt"), tick=0)
    assert res.exit_code == 1
    assert res.stdout == ""
    # sin invertir, al menos una coincide → exit 0
    res2 = _run_grep(fs, "/", ("sujeto", "a.txt"), tick=0)
    assert res2.exit_code == 0

