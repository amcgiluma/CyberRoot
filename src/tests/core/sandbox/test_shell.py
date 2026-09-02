"""Tests del Shell (H3): parsing, 127, sintaxis futura, historial, serialización."""

from __future__ import annotations

from core.sandbox.commands.files import SPECS as FILE_SPECS
from core.sandbox.commands.navigation import SPECS as NAVIGATION_SPECS
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import (
    DEFAULT_CAP0_COMMANDS,
    DEFAULT_CH2_COMMANDS,
    SPECS_ALL,
    Shell,
    _PIPE_MSG,
    _SYNTAX_MSG,
)


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

def test_set_cap0_incluye_cp_decision_gwyn() -> None:
    """🧭1 APROBADA por Gwyn (27/08): cp es el 4.º concepto del cap. 0."""
    assert "cp" in DEFAULT_CAP0_COMMANDS
    assert tuple(sorted(DEFAULT_CAP0_COMMANDS)) == ("cat", "cd", "cp", "ls")


def test_registro_solo_contiene_los_pedidos() -> None:
    shell = _shell()
    assert shell.registry.names() == ("cat", "cd", "cp", "ls")
    shell_ls = Shell(_fs(), commands=("ls",))
    assert shell_ls.registry.names() == ("ls",)


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

# ---- tubería (S1, cap. 2) ---------------------------------------------

def _shell_ch2() -> Shell:
    """Shell con el set del cap. 2 (añade grep/wc a los del cap. 0)."""
    return Shell(_fs(), host="oficina-vecinal-muelle-norte", commands=DEFAULT_CH2_COMMANDS)


def test_pipe_una_tuberia_ejecuta_stdout_a_stdin() -> None:
    """`grep 11:04 log | wc -l` encadena: el stdout de grep entra a wc."""
    fs = FileSystem(
        root=DirNode(
            name="/",
            children={
                "home": DirNode(
                    name="home",
                    children={
                        "log.txt": FileNode(
                            name="log.txt",
                            content="11:04 sesion 000 ruido 6 objetivo f.txt\n"
                                    "11:04 sesion 000 ruido 1 objetivo -\n"
                                    "08:59 turno de manana\n",
                        ),
                    },
                ),
            },
        )
    )
    shell = Shell(fs, host="oficina-vecinal-muelle-norte", commands=DEFAULT_CH2_COMMANDS)
    res = shell.execute("grep 11:04 home/log.txt | wc -l")
    assert res.exit_code == 0, res.stderr
    assert res.stdout == "2\n"
    # El ruido de la tubería NO es gratis: grep(2) + wc(1) = 3 (ambos facturan).
    assert shell.total_noise == 3
    # Historial: UNA entrada para la línea, que lleva el ruido de ambos.
    assert len(shell.history) == 1


def test_pipe_multiple_no_soportado_didactico() -> None:
    """`a | b | c` (más de una tubería) se rechaza con mensaje didáctico."""
    res = _shell_ch2().execute("cat /etc/passwd | grep root | wc -l")
    assert res.exit_code == 2
    assert res.stderr == _PIPE_MSG
    assert "grep" not in res.stderr and "cat" not in res.stderr


def test_pipe_con_comillas_pipe_literal() -> None:
    """Un `|` entre comillas es literal (GNU real), no una tubería."""
    fs = FileSystem(
        root=DirNode(
            name="/",
            children={
                "home": DirNode(
                    name="home",
                    children={"a|b.txt": FileNode(name="a|b.txt", content="x\n")},
                ),
            },
        )
    )
    shell = Shell(fs, host="oficina-vecinal-muelle-norte", commands=DEFAULT_CH2_COMMANDS)
    res = shell.execute('cat "/home/a|b.txt"')
    assert res.exit_code == 0, res.stderr
    assert res.stdout == "x\n"


def test_glob_y_redireccion_rechazados() -> None:
    shell = _shell()
    for line in ("cat *.txt", "ls > out.txt", "cat a?b"):
        res = shell.execute(line)
        assert res.exit_code == 2, line
        assert res.stderr == _SYNTAX_MSG, line


def test_encadenado_and_amp_repros_exactos_de_oscar_rechazados() -> None:
    """S3 (28/08): los 3 repros EXACTOS de Oscar (zona 🔬) — didáctico, no mentira.

    Antes: `cd /srv && ls` → «cd: too many arguments» exit 1 (culpaba a cd);
    `ls /srv && cat f` → `ls` trataba `&&`/`cat` como operandos (exit 2);
    `ls; cat X` → «sh: command not found: ls;» exit 127. Ahora: rechazo
    didáctico exit 2 que insinúa el futuro (🧭3) y NO culpa al comando.
    """
    shell = _shell()
    for line in ("cd /srv && ls", "ls /srv && cat fichero", "ls; cat fichero"):
        res = shell.execute(line)
        assert res.exit_code == 2, line
        assert res.stderr == _SYNTAX_MSG, line
        assert "too many arguments" not in res.stderr, line
        assert "command not found" not in res.stderr, line


def test_ampersand_y_punto_y_coma_sueltos_tambien_rechazados() -> None:
    """`&` (background) y `;` suelto son encadenado igual: no se cuelan."""
    shell = _shell()
    for line in ("ls &", "ls ;", "ls ; cat fichero", "&"):
        res = shell.execute(line)
        assert res.exit_code == 2, line
        assert res.stderr == _SYNTAX_MSG, line


def test_comillas_con_ampersand_y_punto_y_coma_son_literales_validos() -> None:
    """Entre comillas `&` y `;` son LITERALES (GNU real), no sintaxis bloqueada.

    Y sin comillas SÍ se rechaza — igual que `sh` real, que interpretaría
    `&` como background: la honestidad GNU corta en ambos sentidos.
    """
    fs = FileSystem(
        root=DirNode(
            name="/",
            children={
                "home": DirNode(
                    name="home",
                    children={
                        "a&b;.txt": FileNode(name="a&b;.txt", content="contenido\n"),
                    },
                ),
            },
        )
    )
    shell = Shell(fs, host="oficina-vecinal-muelle-norte")
    res = shell.execute('cat "/home/a&b;.txt"')
    assert res.exit_code == 0, res.stderr
    assert res.stdout == "contenido\n"
    res2 = shell.execute("cat /home/a&b;.txt")
    assert res2.exit_code == 2
    assert res2.stderr == _SYNTAX_MSG


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
    """Las specs del módulo cubren cap. 0 (cat/cd/cp/ls) + cap. 2 (grep/wc)
    + cap. 3 (ps/env, S1 31/08; kill, S1 02/09) + familia conteo (head/tail/sort/uniq, S2
    01/09). `sudo` NO es una spec: es un wrapper del shell."""
    assert {s.name for s in SPECS_ALL} == {
        "ls", "cd", "cat", "cp", "grep", "wc", "ps", "env",
        "head", "tail", "sort", "uniq", "kill",
    }
    assert FILE_SPECS and NAVIGATION_SPECS
