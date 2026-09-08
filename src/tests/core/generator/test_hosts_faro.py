"""O3 — /etc/hosts en el mundo (host `faro`) — 08/09, Ornstein.

AC: generate(42,6) trae /etc/hosts legible → cat exit 0 y descubre faro;
determinismo byte-idéntico salvo fichero; suite 625→627 (+2).
"""
from __future__ import annotations

from core.generator import generate, new_session
from core.generator.chapter6 import HOSTS_CONTENT, HOSTS_PATH
from core.sandbox.fs import FileNode


def test_hosts_en_mundo_y_cat_descubre_faro():
    inc = generate(42, 6)
    # FS trae /etc/hosts
    node = inc.room.fs.resolve(HOSTS_PATH, "/")
    assert isinstance(node, FileNode)
    assert "127.0.0.1 localhost" in node.content
    assert "faro" in node.content
    assert node.content == HOSTS_CONTENT

    shell = new_session(inc)
    r = shell.execute(f"cat {HOSTS_PATH}")
    assert r.exit_code == 0, f"stderr: {r.stderr!r}"
    assert "faro" in r.stdout
    assert "127.0.0.1" in r.stdout
    # descubrimiento
    assert "faro" in shell.hosts
    assert len(shell.hosts) >= 1


def test_hosts_determinismo_y_no_descubre_con_ls():
    a = generate(42, 6)
    b = generate(42, 6)
    assert a.to_dict() == b.to_dict()
    # determinismo salvo hosts: dos seeds distintas dan hosts idénticos (no RNG)
    c = generate(99, 6)
    assert c.room.fs.resolve(HOSTS_PATH, "/").content == HOSTS_CONTENT

    inc = generate(42, 6)
    shell = new_session(inc)
    # ls /etc no descubre
    r_ls = shell.execute("ls /etc")
    assert r_ls.exit_code == 0
    assert "faro" not in shell.hosts  # aún no descubierto
    # cat sí
    r_cat = shell.execute(f"cat {HOSTS_PATH}")
    assert r_cat.exit_code == 0
    assert "faro" in shell.hosts
    # re-leer no duplica
    before = len(shell.hosts)
    shell.execute(f"cat {HOSTS_PATH}")
    assert len(shell.hosts) == before
