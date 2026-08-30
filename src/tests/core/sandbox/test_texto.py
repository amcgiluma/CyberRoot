"""S1 (30/08) — golden tests de `grep` y `wc` contra GNU real.

Verificados el 30/08 contra coreutils real (Ubuntu): salidas y exit codes
byte a byte. La línea EXACTA del cap. 2 de Manus — `grep 11:04 ... | wc -l`
→ `2` — es el golden central (el shell la cubre en test_shell.py y en
test_session_ch2.py); aquí los casos de borde aislados de cada comando.
"""

from __future__ import annotations

from core.sandbox.commands.texto import (
    _run_grep,
    _run_wc,
    GREP_SPEC,
    WC_SPEC,
)
from core.sandbox.fs import DirNode, FileNode, FileSystem


def _fs() -> FileSystem:
    """Piel mínima del archivo de turnos del cap. 2."""
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "centralita": DirNode(
                            name="centralita",
                            children={
                                "turnos": DirNode(
                                    name="turnos",
                                    children={
                                        "turno.log": FileNode(
                                            name="turno.log",
                                            content=(
                                                "11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt\n"
                                                "11:04 sesion 000 ruido 1 objetivo -\n"
                                                "08:59 turno de manana\n"
                                            ),
                                        ),
                                    },
                                ),
                            },
                        ),
                    },
                ),
            },
        )
    )


def _grep(argv: tuple[str, ...], stdin: str = ""):
    return _run_grep(_fs(), "/", argv, tick=0, stdin=stdin)


def _wc(argv: tuple[str, ...], stdin: str = ""):
    return _run_wc(_fs(), "/", argv, tick=0, stdin=stdin)


# ---- grep -------------------------------------------------------------

def test_grep_patron_en_fichero_filtra_lineas() -> None:
    res = _grep(("11:04", "srv/centralita/turnos/turno.log"))
    assert res.exit_code == 0
    assert res.stdout == (
        "11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt\n"
        "11:04 sesion 000 ruido 1 objetivo -\n"
    )


def test_grep_sin_coincidencia_exit_1() -> None:
    res = _grep(("zzz", "srv/centralita/turnos/turno.log"))
    assert res.exit_code == 1
    assert res.stdout == ""


def test_grep_fichero_inexistente_exit_2_mensaje_gnu() -> None:
    """El post-mortem de Ceniza (cap. 2) cita EXACTO este mensaje."""
    res = _grep(("11:04", "srv/centralita/no_existe.log"))
    assert res.exit_code == 2
    assert res.stderr == "grep: srv/centralita/no_existe.log: No such file or directory"


def test_grep_sin_patron_usage() -> None:
    res = _grep(())
    assert res.exit_code == 2
    assert res.stderr  # mensaje de uso, no cuelga


def test_grep_lee_stdin_cuando_no_hay_fichero() -> None:
    """Sin operandos de fichero, grep filtra el buffer de la tubería."""
    stdin = "11:04 a\n11:04 b\nzzz\n"
    res = _grep(("11:04",), stdin=stdin)
    assert res.exit_code == 0
    assert res.stdout == "11:04 a\n11:04 b\n"


def test_grep_emite_ruido_perfil() -> None:
    assert GREP_SPEC.noise == 2


# ---- wc ---------------------------------------------------------------

def test_wc_l_stdin_solo_numero() -> None:
    """GNU real: `wc -l` sobre stdin escribe SOLO el número (sin nombre)."""
    stdin = "11:04 sesion 000 ruido 6 objetivo f.txt\n11:04 sesion 000 ruido 1 objetivo -\n"
    res = _wc(("-l",), stdin=stdin)
    assert res.exit_code == 0
    assert res.stdout == "2\n"


def test_wc_l_fichero_con_nombre() -> None:
    """GNU real: con fichero en argv, `wc -l` incluye el nombre (N nombre)."""
    res = _wc(("-l", "srv/centralita/turnos/turno.log"))
    assert res.exit_code == 0
    assert res.stdout == "3 srv/centralita/turnos/turno.log\n"


def test_wc_c_cuenta_bytes() -> None:
    """`wc -c` cuenta bytes; sobre stdin, solo el número."""
    res = _wc(("-c",), stdin="one word\n")
    assert res.exit_code == 0
    assert res.stdout == "9\n"


def test_wc_sin_flags_formato_v1_documentado() -> None:
    """Sin flags: `nlines nwords nbytes` (formato v1 simple, sin alineación)."""
    res = _wc((), stdin="line one\nline two\n")
    assert res.exit_code == 0
    assert res.stdout == "2 4 18\n"


def test_wc_fichero_inexistente_exit_1() -> None:
    res = _wc(("-l", "no/existe.txt"))
    assert res.exit_code == 1
    assert res.stderr == "wc: no/existe.txt: No such file or directory"


def test_wc_opcion_desconocida_rechazada() -> None:
    res = _wc(("-x",))
    assert res.exit_code == 1
    assert res.stderr.startswith("wc: invalid option")


def test_wc_emite_ruido_perfil() -> None:
    assert WC_SPEC.noise == 1