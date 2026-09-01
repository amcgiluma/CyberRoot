"""S2 (01/09) — golden tests de la familia conteo (`head`/`tail`/`sort`/`uniq`).

Semántica contra coreutils REAL verificada el 01/09 (Ubuntu): salidas y exit
codes byte a byte. Son la familia «lectura frugal» (menos ruido por la misma
información que un `cat` entero) y la barrera técnica hacia el cap. 6.

Golden central: el tracto de pipes del cap. 2 (`grep ... | wc -l`) sigue
INTACTO con estos comandos activos en la sesión (no se rompen las tuberías).
"""

from __future__ import annotations

from core.sandbox.commands.conteo import (
    _run_head,
    _run_sort,
    _run_tail,
    _run_uniq,
    HEAD_SPEC,
    SORT_SPEC,
    TAIL_SPEC,
    UNIQ_SPEC,
)
from core.sandbox.fs import DirNode, FileNode, FileSystem

DATA = "zeta\nalpha\nalpha\nbeta\nDelta\n"


def _fs() -> FileSystem:
    return FileSystem(
        root=DirNode(name="/", children={
            "datos.txt": FileNode(name="datos.txt", content=DATA),
        }),
    )


def _head(argv, stdin=""):
    return _run_head(_fs(), "/", argv, tick=0, stdin=stdin)


def _tail(argv, stdin=""):
    return _run_tail(_fs(), "/", argv, tick=0, stdin=stdin)


def _sort(argv, stdin=""):
    return _run_sort(_fs(), "/", argv, tick=0, stdin=stdin)


def _uniq(argv, stdin=""):
    return _run_uniq(_fs(), "/", argv, tick=0, stdin=stdin)


# ---- head ----------------------------------------------------------------

def test_head_default_primeras_10() -> None:
    res = _head(("datos.txt",))
    assert res.exit_code == 0
    assert res.stdout == DATA


def test_head_n_primeras() -> None:
    res = _head(("-n", "2", "datos.txt"))
    assert res.exit_code == 0
    assert res.stdout == "zeta\nalpha\n"


def test_head_n_cero_es_vacio() -> None:
    """GNU real: `head -n 0` no emite nada (exit 0)."""
    res = _head(("-n", "0", "datos.txt"))
    assert res.exit_code == 0
    assert res.stdout == ""


def test_head_lee_stdin() -> None:
    res = _head(("-n", "1"), stdin="x\ny\nz\n")
    assert res.stdout == "x\n"


def test_head_fichero_inexistente_exit1_gnu() -> None:
    res = _head(("no_existe.txt",))
    assert res.exit_code == 1
    assert res.stderr == (
        "head: cannot open 'no_existe.txt' for reading: No such file or directory"
    )


def test_head_numero_invalido_exit1() -> None:
    res = _head(("-n", "abc", "datos.txt"))
    assert res.exit_code == 1
    assert "invalid number of lines" in res.stderr


# ---- tail ----------------------------------------------------------------

def test_tail_default_ultimas_10() -> None:
    res = _tail(("datos.txt",))
    assert res.exit_code == 0
    assert res.stdout == DATA


def test_tail_n_ultimas() -> None:
    res = _tail(("-n", "2", "datos.txt"))
    assert res.exit_code == 0
    assert res.stdout == "beta\nDelta\n"


def test_tail_lee_stdin() -> None:
    res = _tail(("-n", "2"), stdin="a\nb\nc\n")
    assert res.stdout == "b\nc\n"


def test_tail_fichero_inexistente_exit1_gnu() -> None:
    res = _tail(("no_existe.txt",))
    assert res.exit_code == 1
    assert res.stderr == (
        "tail: cannot open 'no_existe.txt' for reading: No such file or directory"
    )


# ---- sort ----------------------------------------------------------------

def test_sort_ordena_por_byte() -> None:
    """GNU real: sort (LC_ALL=C) ordena MAYÚSCULAS antes que minúsculas."""
    res = _sort(("datos.txt",))
    assert res.exit_code == 0
    assert res.stdout == "Delta\nalpha\nalpha\nbeta\nzeta\n"


def test_sort_u_unicos() -> None:
    res = _sort(("-u", "datos.txt"))
    assert res.stdout == "Delta\nalpha\nbeta\nzeta\n"


def test_sort_lee_stdin() -> None:
    res = _sort((), stdin="b\na\n")
    assert res.stdout == "a\nb\n"


def test_sort_fichero_inexistente_exit2_gnu() -> None:
    res = _sort(("no_existe.txt",))
    assert res.exit_code == 2
    assert res.stderr == "sort: cannot read: no_existe.txt: No such file or directory"


# ---- uniq ----------------------------------------------------------------

def test_uniq_solo_colapsa_adyacentes_sin_ordenar() -> None:
    """GNU real: `uniq` NO ordena — solo fusiona contiguos; no reordena."""
    res = _uniq(("datos.txt",))
    assert res.stdout == "zeta\nalpha\nbeta\nDelta\n"


def test_uniq_c_cuenta_alineado_ancho7() -> None:
    """GNU real: `uniq -c` antepone la cuenta derecha-alineada en ancho 7."""
    res = _uniq(("-c", "datos.txt"))
    assert res.exit_code == 0
    assert res.stdout == (
        "      1 zeta\n"
        "      2 alpha\n"
        "      1 beta\n"
        "      1 Delta\n"
    )


def test_uniq_lee_stdin() -> None:
    res = _uniq((), stdin="a\na\nb\n")
    assert res.stdout == "a\nb\n"


def test_uniq_fichero_inexistente_exit1_gnu() -> None:
    """GNU real: `uniq` reporta DISTINTO que head/tail (sin «cannot open»)."""
    res = _uniq(("no_existe.txt",))
    assert res.exit_code == 1
    assert res.stderr == "uniq: no_existe.txt: No such file or directory"


# ---- ruido (familia «lectura frugal») ------------------------------------

def test_ruido_perfil_conteo() -> None:
    assert HEAD_SPEC.noise == 1
    assert TAIL_SPEC.noise == 1
    assert SORT_SPEC.noise == 2
    assert UNIQ_SPEC.noise == 1