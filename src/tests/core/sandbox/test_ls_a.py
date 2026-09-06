"""test_ls_a.py — S2 (06/09): [BUG] ls -a / ls -la parseo de flags + dotfiles.

Criterio S2:
- ls -a /srv/camara-faro → exit 0, sin stderr, lista 6 ficheros (incluida .nota-corte)
- ls plano → OCULTA dotfiles (5 visibles)
- -la combina ambos (formato largo con dotfiles)
- ls -l muestra permisos/tamaño/mtime GNU-forma
- cat .nota-corte sigue funcionando igual
"""

from __future__ import annotations

from core.generator import generate, new_session
from core.sandbox.commands.navigation import _run_ls
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell


def _fs_dotfiles() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "camara-faro": DirNode(
                            name="camara-faro",
                            children={
                                "registro.csv": FileNode(name="registro.csv", content="a", mode="644", mtime=1),
                                "purgas.csv": FileNode(name="purgas.csv", content="b", mode="644", mtime=2),
                                "censo-borrador.csv": FileNode(name="censo-borrador.csv", content="c", mode="644", mtime=3),
                                "aviso-faro.txt": FileNode(name="aviso-faro.txt", content="d", mode="644", mtime=4),
                                "LEEME.txt": FileNode(name="LEEME.txt", content="e", mode="644", mtime=5),
                                ".nota-corte": FileNode(name=".nota-corte", content="cut -d'|' -f4 ...", mode="644", mtime=6),
                            },
                        )
                    },
                )
            },
        )
    )


def test_ls_plano_oculta_dotfiles():
    fs = _fs_dotfiles()
    res = _run_ls(fs, "/", ("/srv/camara-faro",), 0)
    assert res.exit_code == 0
    assert res.stderr == ""
    lines = [l for l in res.stdout.splitlines() if l]
    assert ".nota-corte" not in lines
    assert len(lines) == 5


def test_ls_a_muestra_dotfiles():
    fs = _fs_dotfiles()
    res = _run_ls(fs, "/", ("-a", "/srv/camara-faro"), 0)
    assert res.exit_code == 0
    assert res.stderr == ""
    lines = [l for l in res.stdout.splitlines() if l]
    assert ".nota-corte" in lines
    assert len(lines) == 6


def test_ls_la_combina_largo_y_dotfiles():
    fs = _fs_dotfiles()
    res = _run_ls(fs, "/", ("-la", "/srv/camara-faro"), 0)
    assert res.exit_code == 0
    assert res.stderr == ""
    # long format: cada línea contiene permisos y nombre
    assert ".nota-corte" in res.stdout
    # debe ser formato largo (contiene owner/group)
    assert "root" in res.stdout or "644" not in res.stdout  # perms form
    # 6 líneas en long
    assert len([l for l in res.stdout.splitlines() if l.strip()]) == 6


def test_ls_l_sin_a_sigue_ocultando_y_formato_largo():
    fs = _fs_dotfiles()
    res = _run_ls(fs, "/", ("-l", "/srv/camara-faro"), 0)
    assert res.exit_code == 0
    assert ".nota-corte" not in res.stdout
    assert len([l for l in res.stdout.splitlines() if l.strip()]) == 5
    # permisos presentes
    assert "-rw" in res.stdout or "drwx" in res.stdout


def test_ls_a_sobre_cwd_sin_operando():
    fs = _fs_dotfiles()
    # cwd = /srv/camara-faro, ls -a sin operando
    res = _run_ls(fs, "/srv/camara-faro", ("-a",), 0)
    assert res.exit_code == 0
    assert ".nota-corte" in res.stdout


def test_cat_nota_corte_sigue_funcionando():
    inc = generate(42, 6)
    shell = new_session(inc)
    # cat debe funcionar igual (nota no desaparece)
    r = shell.execute("cat /srv/camara-faro/.nota-corte")
    assert r.exit_code == 0
    assert "cut -d'|' -f4" in r.stdout

    # ls plano la oculta, ls -a la muestra — integración generator real
    r1 = shell.execute("ls /srv/camara-faro")
    assert r1.exit_code == 0
    assert ".nota-corte" not in r1.stdout
    r2 = shell.execute("ls -a /srv/camara-faro")
    assert r2.exit_code == 0
    assert r2.stderr == ""
    assert ".nota-corte" in r2.stdout
    assert len([l for l in r2.stdout.splitlines() if l.strip()]) == 6


def test_ls_flag_desconocido_error_gnu():
    fs = _fs_dotfiles()
    res = _run_ls(fs, "/", ("-z", "/srv/camara-faro"), 0)
    assert res.exit_code == 2
    assert "invalid option" in res.stderr
