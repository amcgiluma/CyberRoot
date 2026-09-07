"""S1 07/09 — Hosts descubribles leyendo el mundo (FASE A, Smough).

AC:
- cat /etc/hosts registra hostname en Shell.hosts (solo lectura descubre)
- ls /etc no descubre
- sin /etc/hosts, cat falla GNU-honesto y hosts vacío
- roundtrip exacto (to_dict/from_dict)
"""
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell


def _fs_hosts(content: str) -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "etc": DirNode(
                    name="etc", children={"hosts": FileNode(name="hosts", content=content)}
                )
            },
        )
    )


def test_cat_etc_hosts_descubre_faro_stub():
    fs = _fs_hosts("127.0.0.1 localhost\n10.0.0.5 faro\n")
    shell = Shell(fs, commands=("cat", "ls", "ssh", "exit"))
    r = shell.execute("cat /etc/hosts")
    assert r.exit_code == 0
    assert "faro" in r.stdout
    assert len(shell.hosts) == 1
    assert "faro" in shell.hosts


def test_ls_no_descubre_hosts():
    fs = _fs_hosts("127.0.0.1 localhost\n10.0.0.5 faro\n")
    shell = Shell(fs, commands=("cat", "ls", "ssh", "exit"))
    r = shell.execute("ls /etc")
    assert r.exit_code == 0
    assert len(shell.hosts) == 0


def test_cat_sin_hosts_no_descubre_y_falla_gnu():
    fs = FileSystem(root=DirNode(name="/", children={"etc": DirNode(name="etc", children={})}))
    shell = Shell(fs, commands=("cat",))
    r = shell.execute("cat /etc/hosts")
    assert r.exit_code == 1
    assert "No such file or directory" in r.stderr
    assert len(shell.hosts) == 0


def test_roundtrip_con_hosts_descubierto():
    fs = _fs_hosts("127.0.0.1 localhost\n10.0.0.5 alpha\n")
    shell = Shell(fs, commands=("cat", "ssh"))
    shell.execute("cat /etc/hosts")
    assert "alpha" in shell.hosts
    d = shell.to_dict()
    restored = Shell.from_dict(d)
    assert restored.hosts.keys() == shell.hosts.keys()
    assert restored.hosts["alpha"].to_dict() == shell.hosts["alpha"].to_dict()
    assert restored.known_hosts == shell.known_hosts
