"""S1 08/09 — Handler scp Fase B (red pieza 2, Smough).

AC:
- scp faro:/srv/camara-faro/purgas.csv /tmp/ con host descubierto crea fichero (ruido 3)
- sin descubrir -> rechazo que NOMBRA qué falta y dónde (/etc/hosts), exit 1, ruido 0
- ruta remota inexistente GNU-honesta (exit 1, ruido scp)
- destino invalido parent no existe (exit 1, ruido scp)
- roundtrip to_dict preserva fichero copiado
"""
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell


def _local_with_hosts_file() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "tmp": DirNode(name="tmp", children={}),
                "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content="127.0.0.1 localhost\n10.0.0.5 faro\n")}),
                "home": DirNode(name="home", children={"a.txt": FileNode(name="a.txt", content="hello local\n")}),
            },
        )
    )


def _remote_faro() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "camara-faro": DirNode(
                            name="camara-faro",
                            children={"purgas.csv": FileNode(name="purgas.csv", content="id,distrito\nPR-0091,ENSAYO\n")},
                        )
                    },
                ),
                "tmp": DirNode(name="tmp", children={}),
            },
        )
    )


def _shell_with_faro_discovered_via_cat() -> Shell:
    local = _local_with_hosts_file()
    remote = _remote_faro()
    shell = Shell(local, commands=("cat", "scp", "ls"), cwd="/")
    # descubrir via cat (Fase A) -> crea stub
    r = shell.execute("cat /etc/hosts")
    assert r.exit_code == 0
    assert "faro" in shell.hosts
    # reemplazar stub vacio por FS real del generador (costura O<->S: el mundo real trae el fichero)
    shell.hosts["faro"] = remote
    return shell


def test_scp_copia_ok_remoto_a_local_con_host_descubierto():
    shell = _shell_with_faro_discovered_via_cat()
    before = shell.total_noise
    r = shell.execute("scp faro:/srv/camara-faro/purgas.csv /tmp/")
    assert r.exit_code == 0, r.stderr
    assert r.stderr == ""
    # ruido scp = 3
    assert len(r.noise) == 1 and r.noise[0].data["amount"] == 3
    assert shell.total_noise == before + 3
    # fichero destino existe dentro de dir (comportamiento cp fichero dir/)
    content = shell.fs.read_file("/tmp/purgas.csv", "/")
    assert content == "id,distrito\nPR-0091,ENSAYO\n"
    # también con user@host
    shell2 = _shell_with_faro_discovered_via_cat()
    r2 = shell2.execute("scp user@faro:/srv/camara-faro/purgas.csv /tmp/de_user.txt")
    assert r2.exit_code == 0
    assert shell2.fs.read_file("/tmp/de_user.txt", "/") == "id,distrito\nPR-0091,ENSAYO\n"


def test_scp_rechazo_no_descubierto_nombra_hosts():
    local = FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={})}))
    shell = Shell(local, commands=("scp",))
    r = shell.execute("scp faro:/srv/camara-faro/purgas.csv /tmp/")
    assert r.exit_code == 1
    # debe NOMBRAR qué falta y dónde leerlo
    assert "faro" in r.stderr
    assert "/etc/hosts" in r.stderr
    assert "no descubierto" in r.stderr
    # ruido 0 (intentar sin descubrir no es delinquir)
    assert r.noise == () or sum(ev.data["amount"] for ev in r.noise) == 0
    assert shell.total_noise == 0
    # también dst no descubierto
    shell.hosts["faro"] = _remote_faro()
    r2 = shell.execute("scp /tmp/a.txt desconocido:/tmp/b.txt")
    assert r2.exit_code == 1
    assert "desconocido" in r2.stderr and "/etc/hosts" in r2.stderr
    assert r2.noise == () or sum(ev.data["amount"] for ev in r2.noise) == 0


def test_scp_ruta_remota_inexistente_gnu():
    shell = _shell_with_faro_discovered_via_cat()
    r = shell.execute("scp faro:/no/existe.csv /tmp/")
    assert r.exit_code == 1
    assert "No such file or directory" in r.stderr
    assert "faro:/no/existe.csv" in r.stderr
    # ruido scp si factura (es intento con host ya descubierto)
    assert len(r.noise) == 1 and r.noise[0].data["amount"] == 3
    # destino local inexistente no se crea
    try:
        shell.fs.read_file("/tmp/existe.csv", "/")
        assert False, "no debe existir"
    except Exception:
        pass


def test_scp_destino_invalido_parent_no_existe():
    shell = _shell_with_faro_discovered_via_cat()
    r = shell.execute("scp faro:/srv/camara-faro/purgas.csv /noexiste/dir/file.csv")
    assert r.exit_code == 1
    assert "No such file or directory" in r.stderr
    assert len(r.noise) == 1
    # también copiar a ruta que es directorio existente como fichero -> Is a directory si intentas sobrescribir dir?
    # En nuestro modelo scp a dir existente copia dentro, así que este caso es parent file
    local2 = FileSystem(
        root=DirNode(
            name="/",
            children={
                "tmp": DirNode(name="tmp", children={"f": FileNode(name="f", content="x")}),
            },
        )
    )
    shell2 = Shell(local2, commands=("scp",))
    shell2.hosts["faro"] = _remote_faro()
    # intentar copiar donde un componente intermedio es fichero (tmp/f es fichero, no dir)
    r2 = shell2.execute("scp faro:/srv/camara-faro/purgas.csv /tmp/f/sub.txt")
    assert r2.exit_code == 1
    assert "Not a directory" in r2.stderr


def test_scp_roundtrip_to_dict_preserva_fichero():
    shell = _shell_with_faro_discovered_via_cat()
    shell.execute("scp faro:/srv/camara-faro/purgas.csv /tmp/persist.csv")
    # local -> remoto también
    shell.hosts["faro"].root.children["home"] = DirNode(name="home", children={})
    shell.execute("scp /tmp/persist.csv faro:/tmp/copia_remota.txt")
    assert shell.fs.read_file("/tmp/persist.csv", "/") == "id,distrito\nPR-0091,ENSAYO\n"
    assert shell.hosts["faro"].read_file("/tmp/copia_remota.txt", "/") == "id,distrito\nPR-0091,ENSAYO\n"
    d = shell.to_dict()
    restored = Shell.from_dict(d)
    assert restored.to_dict() == d
    assert restored.fs.read_file("/tmp/persist.csv", "/") == "id,distrito\nPR-0091,ENSAYO\n"
    assert restored.hosts["faro"].read_file("/tmp/copia_remota.txt", "/") == "id,distrito\nPR-0091,ENSAYO\n"
    # determinismo: dos shells con mismas seeds y operaciones dan mismo to_dict
    shell2 = _shell_with_faro_discovered_via_cat()
    shell2.execute("scp faro:/srv/camara-faro/purgas.csv /tmp/persist.csv")
    shell2.hosts["faro"].root.children["home"] = DirNode(name="home", children={})
    shell2.execute("scp /tmp/persist.csv faro:/tmp/copia_remota.txt")
    assert shell.to_dict() == shell2.to_dict()
