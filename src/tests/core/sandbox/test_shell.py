"""Tests del Shell (H3): parsing, 127, sintaxis futura, historial, serialización."""

from __future__ import annotations

from core.sandbox.commands.files import SPECS as FILE_SPECS
from core.sandbox.commands.navigation import SPECS as NAVIGATION_SPECS
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, Shell, SPECS_ALL


def _fs() -> FileSystem:
    """Fixture con la piel mínima de una oficina vecinal (cap. 0)."""
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "etc": DirNode(name="etc", children={"passwd": FileNode(name="passwd", content="root:0\n")}),
                "home": DirNode(
                    name="home",
                    children={
                        "proveedor.txt": FileNode(name="proveedor.txt", content="CANDELAS\n"),
                        "log.txt": FileNode(name="log.txt", content="11:04\n"),
                    },
                ),
            },
        )
    )


def _shell(commands: tuple[str, ...] = DEFAULT_CAP0_COMMANDS) -> Shell:
    return Shell(_fs(), host="oficina-vecinal-muelle-norte")


# ---- comandos del set y desconocidos ------------------------------------

def test_set_cap0_no_incluye_cp_mientras_gwyn_decide() -> None:
    """🧭1 pendiente: cp NO está en el set por defecto (PLAN decisión 1)."""
    assert "cp" not in DEFAULT_CAP0_COMMANDS
    assert tuple(sorted(DEFAULT_CAP0_COMMANDS)) == ("cat", "cd", "ls")


def test_registro_solo_contiene_los_pedidos() -> None:
    shell = _shell()
    assert shell.registry.names() == ("cat", "cd", "ls")
    shell_cp = Shell(_fs(), commands=("cp", "ls"))
    assert shell_cp.registry.names() == ("cp", "ls")


def test_comando_desconocido_exit_127_mensaje_sh() -> None:
    shell = _shell()
    res = shell.execute("frobnicate /etc")
    assert res.exit_code == 127
    assert res.stderr == "sh: command not found: frobnicate"


def test_linea_vacia_no_hace_nada_y_no_consumira_historial() -> None:
    shell = _shell()
    res = shell.execute("   ")
    assert res.exit_code == 0 and res.stdout == ""
    assert shell.history == []


# ---- sintaxis NO soportada (caps. 1-2) -----------------------------------

def test_pipe_rechazado_con_exit_2() -> None:
    res = _shell().execute("cat /etc/passwd | wc -l")
    assert res.exit_code == 2
    assert res.stderr == "sh: syntax not supported in this session"


def test_glob_y_redireccion_rechazados() -> None:
    shell = _shell()
    for line in ("cat *.txt", "ls > out.txt", "cat a?b"):
        res = shell.execute(line)
        assert res.exit_code == 2, line
        assert res.stderr == "sh: syntax not supported in this session", line


def test_comillas_convenierten_metacaracteres_en_literales() -> None:
    """`cat "a*b.txt"` es un nombre literal en shell real: pasa el parser."""
    shell = _shell()
    res = shell.execute('cat "no_existo*.txt"')
    # No es error de SINTAXIS: es not_found normal de cat (exit 1).
    assert res.exit_code == 1
    assert res.stderr == "cat: no_existo*.txt: No such file or directory"


def test_comillas_sin_cerrar_error_lexico() -> None:
    res = _shell().execute('cat "sin cerrar')
    assert res.exit_code == 2
    assert res.stderr == "sh: syntax error: unexpected end of file"


# ---- cwd, tick, ruido, historial -----------------------------------------

def test_cd_muta_cwd_y_los_relativos_la_siguen() -> None:
    shell = _shell()
    assert shell.execute("cd /home").new_cwd == "/home"
    assert shell.cwd == "/home"
    shell.execute("cd ..")
    assert shell.cwd == "/"  # no sube más allá de la raíz
    shell.execute("cd home")
    res = shell.execute("cat proveedor.txt")
    assert res.stdout == "CANDELAS\n"


def test_error_no_cambia_cwd() -> None:
    shell = _shell()
    shell.execute("cd /home")
    res = shell.execute("cd /no/existe")
    assert res.exit_code == 1
    assert shell.cwd == "/home"


def test_tick_avanza_por_comando_y_ruido_se_acumula() -> None:
    shell = _shell()
    t0 = shell.tick
    shell.execute("ls /etc")     # ruido 1
    shell.execute("cat /etc/passwd")  # ruido 1
    shell.execute("cd /")        # ruido 0
    shell.execute("nope")        # ruido 0 (desconocido)
    assert shell.tick == t0 + 4
    assert shell.total_noise == 2


def test_historial_registra_linea_y_resultado() -> None:
    shell = _shell()
    shell.execute("ls")
    assert len(shell.history) == 1
    assert shell.history[0]["line"] == "ls"
    assert shell.history[0]["result"]["exit_code"] == 0


# ---- serialización de la sesión ------------------------------------------

def test_sesion_roundtrip_ida_y_vuelta_exacto() -> None:
    shell = _shell()
    shell.execute("cd /home")
    shell.execute("cat proveedor.txt")
    shell.execute("cd ..")
    d = shell.to_dict()
    shell2 = Shell.from_dict(d)
    assert shell2.to_dict() == d
    # Independencia de mutaciones: ejecutar en la copia no toca la original.
    shell2.execute("cat /etc/passwd")
    assert len(shell.history) == 3
    assert shell2.tick == shell.tick + 1


def test_todas_las_specs_estan_disponibles_para_el_set() -> None:
    """cp/cat/cd/ls existen como specs aunque el set del cap. 0 no incluya cp."""
    assert {s.name for s in SPECS_ALL} == {"ls", "cd", "cat", "cp"}
    assert FILE_SPECS and NAVIGATION_SPECS
