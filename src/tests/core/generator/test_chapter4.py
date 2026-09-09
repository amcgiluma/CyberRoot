"""O1 09/09 — Red cap.4 en el generator (chapter4.py + hosts + allowlist)."""

from core.generator import generate, new_session
from core.generator.chapter4 import TRONCAL_PATH, TRONCAL_CONTENT
from core.sandbox.shell import DEFAULT_CH4_COMMANDS


def test_generate_42_4_deterministic() -> None:
    a = generate(42, 4)
    b = generate(42, 4)
    assert a.to_dict() == b.to_dict()
    assert a.room.fs.to_dict() == b.room.fs.to_dict()


def test_hosts_2_3_y_cat_descubre_ls_no() -> None:
    inc = generate(42, 4)
    # /etc/hosts debe existir y tener 2-3 entradas — probamos vía Shell crudo
    # (sin new_session pre-poblado) para verificar la regla «leer descubre, listar no»
    from core.sandbox.shell import Shell, _parse_hosts_content

    shell = Shell(inc.room.fs.snapshot(), commands=DEFAULT_CH4_COMMANDS)
    res = shell.execute("cat /etc/hosts")
    assert res.exit_code == 0, res.stderr
    assert "faro" in res.stdout
    assert "troncal-01" in res.stdout
    expected = set(_parse_hosts_content(res.stdout))
    assert expected <= set(shell.hosts.keys())
    assert len(expected) in (2, 3)
    # ls /etc NO descubre (regla «leer descubre, listar no»)
    shell2 = Shell(generate(42, 4).room.fs.snapshot(), commands=DEFAULT_CH4_COMMANDS)
    assert "faro" not in shell2.hosts
    r2 = shell2.execute("ls /etc")
    assert r2.exit_code == 0
    assert shell2.hosts == {}, "ls no debe descubrir hosts"


def test_scp_multi_host_funciona() -> None:
    inc = generate(42, 4)
    shell = new_session(inc)
    # descubrir primero
    r = shell.execute("cat /etc/hosts")
    assert r.exit_code == 0
    # scp desde faro (piel cap6)
    r1 = shell.execute("scp faro:/srv/camara-faro/purgas.csv /tmp/")
    assert r1.exit_code == 0, f"scp faro falla: {r1.stderr}"
    # verificar fichero copiado
    from core.sandbox.fs import FileNode

    node = shell.fs.resolve("/tmp/purgas.csv", "/")
    assert isinstance(node, FileNode)
    assert "PR-0091" in node.content
    # scp desde troncal-01
    r2 = shell.execute(f"scp troncal-01:{TRONCAL_PATH} /tmp/")
    assert r2.exit_code == 0, f"scp troncal falla: {r2.stderr}"
    node2 = shell.fs.resolve("/tmp/volcado.csv", "/")
    assert isinstance(node2, FileNode)
    assert "TR-001" in node2.content
    assert node2.content == TRONCAL_CONTENT


def test_ch4_allowlist_y_6_intacto() -> None:
    assert "ssh" in DEFAULT_CH4_COMMANDS
    assert "scp" in DEFAULT_CH4_COMMANDS
    assert "cut" in DEFAULT_CH4_COMMANDS
    # generate(42,6) byte-idéntico (no tocado por ch4)
    a = generate(42, 6)
    b = generate(42, 6)
    assert a.to_dict() == b.to_dict()
    # ch6 sigue sin ssh/scp (frontera deliberada)
    shell6 = new_session(generate(42, 6))
    r = shell6.execute("ssh faro")
    assert r.exit_code == 127
    assert "command not found" in r.stderr
