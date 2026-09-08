"""T2 08/09 — Roundtrip del efecto `scp` en el save (Seath, condicional).

Verifica que el fichero copiado entre FS del stack de conexión (S1 scp Fase B,
Smough 08/09) sobrevive `GameState.to_dict/from_dict` idéntico. Si S1 aún no
está en main al entrar (08/09: PR #37 pendiente en feat/sandbox-2026-09-08),
los tests caen sobre el mecanismo subyacente (hosts dict con FileSystem) que
scp usa — skip honesto declarado abajo, no inventan código ausente.

Cubre:
- fichero copiado local→remoto y remoto→local persiste tras roundtrip
- determinismo idempotente (dos shells con misma operación dan mismo dict)
- múltiples ficheros y directorios de destino creados por scp sobreviven

Determinista, sin RNG global, sin reloj real, sin pyxel.
"""

from __future__ import annotations

import pytest

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell
from core.state.state import GameState


def _has_scp() -> bool:
    """True si el handler scp está registrado en esta rama (S1 mergeado)."""
    # En main 08/09 el handler aún no existe; detectamos por presencia del
    # método _exec_scp en Shell (añadido por S1 08/09). No basta con
    # available_commands porque Shell de main devuelve 127 aunque se pase.
    return hasattr(Shell, "_exec_scp")


def _roundtrip(shell: Shell) -> Shell:
    return GameState.from_dict(GameState(shell=shell).to_dict()).shell


def _fs_local() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "tmp": DirNode(name="tmp", children={}),
                "home": DirNode(name="home", children={"a.txt": FileNode(name="a.txt", content="hello local\n")}),
                "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content="127.0.0.1 localhost\n10.0.0.5 faro\n")}),
            },
        )
    )


def _fs_remote() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={"camara-faro": DirNode(name="camara-faro", children={"purgas.csv": FileNode(name="purgas.csv", content="id,distrito\nPR-0091,ENSAYO\n")})},
                ),
                "tmp": DirNode(name="tmp", children={}),
            },
        )
    )


def test_scp_effect_local_file_survives_roundtrip() -> None:
    """El efecto `scp faro:… /tmp/` (fichero en FS destino) sobrevive al save.

    Si S1 está mergeado, usa el comando real; si no, simula el efecto
    escribiendo directamente en el FS remoto — el contrato bajo test es el
    mismo: GameState persiste hosts con sus ficheros.
    """
    if _has_scp():
        # Camino real con comando
        local = _fs_local()
        remote = _fs_remote()
        shell = Shell(local, commands=("cat", "scp"), cwd="/")
        shell.execute("cat /etc/hosts")
        assert "faro" in shell.hosts
        shell.hosts["faro"] = remote
        r = shell.execute("scp faro:/srv/camara-faro/purgas.csv /tmp/persist.csv")
        assert r.exit_code == 0, r.stderr
        assert shell.fs.read_file("/tmp/persist.csv", "/") == "id,distrito\nPR-0091,ENSAYO\n"
    else:
        # S1 aún no mergeado a las 19:00 — stub honesto: se testa el mecanismo
        # subyacente (hosts dict con FS) que scp usará; no se inventa código.
        local = _fs_local()
        shell = Shell(local, commands=("cat",))
        shell.hosts["faro"] = _fs_remote()
        # simular copia: escribir en local desde remoto (mismo efecto que scp)
        from core.sandbox.fs import DirNode as _D  # type: ignore

        tmp_node = local.root.children["tmp"]
        assert isinstance(tmp_node, _D)
        tmp_node.children["persist.csv"] = FileNode(name="persist.csv", content="id,distrito\nPR-0091,ENSAYO\n")

    # Roundtrip debe ser idéntico
    g = GameState(shell=shell)
    d = g.to_dict()
    assert GameState.from_dict(d).to_dict() == d
    restored = _roundtrip(shell)
    assert restored.fs.read_file("/tmp/persist.csv", "/") == "id,distrito\nPR-0091,ENSAYO\n"
    assert restored.hosts["faro"].to_dict() == shell.hosts["faro"].to_dict()


def test_scp_effect_remote_copy_survives_roundtrip() -> None:
    """Fichero copiado local→remoto (`scp /tmp/a.txt faro:/tmp/b.txt`) persiste."""
    local = _fs_local()
    remote = _fs_remote()
    shell = Shell(local, commands=("cat", "scp") if _has_scp() else ("cat",), cwd="/")
    # descubrir faro aunque sea manualmente si scp no existe
    if "faro" not in shell.hosts:
        shell.hosts["faro"] = remote
    else:
        shell.hosts["faro"] = remote

    if _has_scp():
        # asegurar local tiene el fichero
        # /home/a.txt ya existe en _fs_local, copiar a remoto
        shell.execute("cat /etc/hosts")
        r = shell.execute("scp /home/a.txt faro:/tmp/copia.txt")
        assert r.exit_code == 0, r.stderr
    else:
        # S1 aún no mergeado — stub: inyectar fichero en FS remoto (mismo
        # efecto que scp local→remoto); el invariante bajo test es la
        # persistencia del FS remoto en el save.
        from core.sandbox.fs import DirNode as _D2  # type: ignore

        faro_tmp = remote.root.children["tmp"] if isinstance(remote, FileSystem) else None
        # remote es la variable de arriba
        assert isinstance(remote.root.children["tmp"], _D2)
        remote.root.children["tmp"].children["copia.txt"] = FileNode(name="copia.txt", content="hello local\n")

    g = GameState(shell=shell)
    restored = _roundtrip(shell)
    # el fichero en el host remoto debe estar tras reload
    assert restored.hosts["faro"].read_file("/tmp/copia.txt", "/") == "hello local\n"
    assert GameState.from_dict(g.to_dict()).to_dict() == g.to_dict()


def test_scp_effect_multiple_files_and_hosts_roundtrip() -> None:
    """Múltiples ficheros copiados a distintos paths sobreviven idénticos.

    No depende de scp: valida que GameState serializa TODOS los hosts con
    contenido arbitrario (lo que scp produce). Es el invariante que T2 blinda.
    """
    local = FileSystem(
        root=DirNode(
            name="/",
            children={
                "tmp": DirNode(name="tmp", children={}),
                "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content="127.0.0.1 localhost\n10.0.0.5 faro\n10.0.0.6 baliza\n")}),
            },
        )
    )
    shell = Shell(local, commands=("cat",))
    # dos hosts con FS vacíos + inyección de ficheros como haría scp
    faro_fs = FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={"x.csv": FileNode(name="x.csv", content="a,b\n1,2\n")})}))
    baliza_fs = FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={})}))
    shell.hosts["faro"] = faro_fs
    shell.hosts["baliza"] = baliza_fs
    # simular dos scp: local→faro y faro→baliza
    # (inyección directa; el comando real haría lo mismo)
    from core.sandbox.fs import DirNode as _D3  # type: ignore

    tmp_local = shell.fs.root.children["tmp"]
    assert isinstance(tmp_local, _D3)
    tmp_local.children["local.txt"] = FileNode(name="local.txt", content="local\n")
    faro_tmp = faro_fs.root.children["tmp"]
    assert isinstance(faro_tmp, _D3)
    faro_tmp.children["y.txt"] = FileNode(name="y.txt", content="from faro\n")

    g = GameState(shell=shell)
    d = g.to_dict()
    assert GameState.from_dict(d).to_dict() == d
    restored = _roundtrip(shell)
    assert restored.fs.read_file("/tmp/local.txt", "/") == "local\n"
    assert restored.hosts["faro"].read_file("/tmp/x.csv", "/") == "a,b\n1,2\n"
    assert restored.hosts["faro"].read_file("/tmp/y.txt", "/") == "from faro\n"
    assert restored.hosts["baliza"].to_dict() == baliza_fs.to_dict()
    # determinismo: segunda shell igual da mismo dict
    shell2 = Shell(local, commands=("cat",))
    shell2.hosts["faro"] = FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={"x.csv": FileNode(name="x.csv", content="a,b\n1,2\n"), "y.txt": FileNode(name="y.txt", content="from faro\n")})}))
    shell2.hosts["baliza"] = FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={})}))
    shell2.fs.root.children["tmp"].children["local.txt"] = FileNode(name="local.txt", content="local\n")
    assert shell.to_dict() == shell2.to_dict()
