"""S2 07/09 — sort --help GNU-honesto (Smough, higiene).

AC: sort -k0 y sort -t ab rematan con \"Try 'sort --help' for more information.\" sin tocar exits/stdout válidos.
"""
from core.sandbox.commands.conteo import _run_sort
from core.sandbox.fs import DirNode, FileNode, FileSystem

_HELP = "Try 'sort --help' for more information."


def _fs():
    return FileSystem(root=DirNode(name="/", children={"f": FileNode(name="f", content="a\n")}))  # type: ignore[arg-type]


def test_sort_k0_remata_hint():
    fs = _fs()
    r = _run_sort(fs, "/", ("-k0", "f"), tick=0)
    assert r.exit_code == 2
    assert r.stderr == f"sort: field number is zero: invalid field specification '0'\n{_HELP}"


def test_sort_t_multi_char_remata_hint():
    fs = _fs()
    r = _run_sort(fs, "/", ("-t", "ab", "f"), tick=0)
    assert r.exit_code == 2
    assert r.stderr == f"sort: multi-character tab 'ab'\n{_HELP}"


def test_sort_valido_sin_hint_ni_cambio_stdout():
    fs = FileSystem(root=DirNode(name="/", children={"f": FileNode(name="f", content="b\na\n")}))  # type: ignore[arg-type]
    r = _run_sort(fs, "/", ("f",), tick=0)
    assert r.exit_code == 0
    assert r.stderr == ""
    assert r.stdout == "a\nb\n"
