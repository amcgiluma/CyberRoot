"""Golden tests para `join` (S3 10/09) — una la Lista por campo de unión.

Semántica contrastada contra coreutils REAL (join 9.4, Ubuntu, 10/09).
Golden del briefing (quest dato4, cap. 6):
  `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` → PR-0091 (la purga
  de nadie, ENSAYO) como no-pareja de FILE1 con el campo de unión primero.
"""

from __future__ import annotations

from core.sandbox.commands.join import _run_join, JOIN_SPEC, SPECS
from core.sandbox.commands.cut import SPECS as CUT_SPECS
from core.sandbox.noise import NOISE_PROFILE
from core.sandbox.shell import Shell, DEFAULT_CH6_COMMANDS
from core.sandbox.fs import DirNode, FileNode, FileSystem

PURGAS = (
    "purga_id|fecha|sujeto|distrito|motivo_codigo|prev_puntuacion|post_credito|puerta_cerrada|archivo_referencia\n"
    "PR-0144|03-07|000462|UMBRAL-BAJO|CONTINUIDAD|438|0|1|OH-UBA-14-0007\n"
    "PR-0151|11-07|000537|MUEL-01|REASIGNACION|0|0|1|OH-HOSP-47-C-0191\n"
    "PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C\n"
    "PR-0092|11-07|000483|UMBRAL-BAJO|EN BLANCO, revisado|500|0|1|OH-UBA-14-0092\n"
)
REG = (
    "residente_id|nombre|fecha_nac|distrito|vivienda|empleador|ingresos_mes|antiguedad_meses|chequeo|sanciones|marcas_purga|puntuacion|estado\n"
    "000291|VERA MONTEJO G.|12-03-1987|UMBRAL-ALTO|B14-E3-P14|LUMEN DIV. FACTURACION|2140|214|SIN CHEQUEO|0|0|712|ACTIVO\n"
    "000462|E. ROLDAN S.|03-11-2001|UMBRAL-BAJO|C07-E1-P02|LAVANDERIA CICLON|1280|96|HOSP-47-C|1|1|438|EN DEUDA\n"
    "000537|J. HERRERA V.|27-08-1963|MUEL-01|D03-E2-P01|ASTILLEROS DEL MUEL SE|0|0|EN BLANCO|0|2|0|PURGADO 19\n"
)


def _fs() -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={
        "purgas.csv": FileNode(name="purgas.csv", content=PURGAS),
        "registro.csv": FileNode(name="registro.csv", content=REG),
    }))


def _join(argv, stdin=""):
    return _run_join(_fs(), "/", argv, tick=0, stdin=stdin)


# ---- golden del briefing --------------------------------------------------

def test_golden_v1_da_PR_0091():
    r = _join(("-t", "|", "-1", "3", "-2", "1", "-v", "1", "purgas.csv", "registro.csv"))
    assert r.exit_code == 0
    # PR-0091 (sujeto 000) y PR-0092 (sujeto 000483) no tienen pareja en registro.
    assert "000|PR-0091|EN BLANCO|--|ENSAYO|--|0|1|HOSP-47-C" in r.stdout
    assert "000483|PR-0092" in r.stdout


def test_golden_v1_pegado_t_quote():
    # shell convierte -t'|' en el token '-t|' (pegado)
    r = _join(("-t|", "-1", "3", "-2", "1", "-v1", "purgas.csv", "registro.csv"))
    assert r.exit_code == 0
    assert "PR-0091" in r.stdout
    assert "000483|PR-0092" in r.stdout


# ---- salida normal combinada ---------------------------------------------

def test_join_normal_combina_parejas():
    r = _join(("-t", "|", "-1", "3", "-2", "1", "purgas.csv", "registro.csv"))
    assert r.exit_code == 0
    # PR-0144 (000462) → registro E. ROLDAN; PR-0151 (000537) → J. HERRERA.
    # Sin -v no salen no-parejas (PR-0091, PR-0092) ni cabeceras.
    assert "PR-0091" not in r.stdout
    assert "000462|PR-0144|03-07|UMBRAL-BAJO|CONTINUIDAD|438|0|1|OH-UBA-14-0007|E. ROLDAN S.|" in r.stdout
    assert "000537|PR-0151|11-07|MUEL-01|REASIGNACION|0|0|1|OH-HOSP-47-C-0191|J. HERRERA V.|" in r.stdout


def test_join_default_delim_blank():
    fs = FileSystem(root=DirNode(name="/", children={
        "f1": FileNode(name="f1", content="1 a\n2 b\n"),
        "f2": FileNode(name="f2", content="1 AA\n2 BB\n3 CC\n"),
    }))
    r = _run_join(fs, "/", ("f1", "f2"), tick=0)
    assert r.exit_code == 0
    assert r.stdout == "1 a AA\n2 b BB\n"
    rv = _run_join(fs, "/", ("-v", "2", "f1", "f2"), tick=0)
    assert rv.stdout == "3 CC\n"


# ---- errores GNU ----------------------------------------------------------

def test_join_missing_operand():
    r = _join(())
    assert r.exit_code == 1
    assert r.stderr == "join: missing operand\nTry 'join --help' for more information."


def test_join_missing_operand_despues_de_uno():
    r = _join(("purgas.csv",))
    assert r.exit_code == 1
    assert "missing operand after 'purgas.csv'" in r.stderr
    assert "Try 'join --help'" in r.stderr


def test_join_extra_operand():
    r = _join(("a", "b", "c"))
    assert r.exit_code == 1
    assert "extra operand 'c'" in r.stderr
    assert "Try 'join --help'" in r.stderr


def test_join_campo_invalido():
    r = _join(("-1", "x", "purgas.csv", "registro.csv"))
    assert r.exit_code == 1
    assert "invalid field number: 'x'" in r.stderr


def test_join_campo_cero():
    r = _join(("-1", "0", "purgas.csv", "registro.csv"))
    assert r.exit_code == 1
    assert "invalid field number: '0'" in r.stderr


def test_join_v_invalido():
    r = _join(("-v", "3", "purgas.csv", "registro.csv"))
    assert r.exit_code == 1
    assert "invalid field number: '3'" in r.stderr


def test_join_fichero_inexistente():
    r = _join(("noexiste.csv", "registro.csv"))
    assert r.exit_code == 1
    assert "join: noexiste.csv: No such file or directory" in r.stderr


def test_join_t_multichar():
    r = _join(("-t", "ab", "purgas.csv", "registro.csv"))
    assert r.exit_code == 1
    assert "multi-character tab 'ab'" in r.stderr


def test_join_option_invalida():
    r = _join(("-q", "purgas.csv", "registro.csv"))
    assert r.exit_code == 1
    assert "invalid option -- 'q'" in r.stderr
    assert "Try 'join --help'" in r.stderr


def test_join_t_sin_arg_se_come_operando():
    # GNU getopt: `-t` se come el siguiente token como delimitador.
    r = _join(("-t", "purgas.csv", "registro.csv"))
    assert r.exit_code == 1
    assert "multi-character tab 'purgas.csv'" in r.stderr


# ---- help / version / ruido ----------------------------------------------

def test_join_help():
    r = _join(("--help",))
    assert r.exit_code == 0
    assert r.stdout.startswith("Usage: join [OPTION]... FILE1 FILE2")


def test_join_version():
    r = _join(("--version",))
    assert r.exit_code == 0
    assert "join (GNU coreutils)" in r.stdout


def test_join_ruido_2():
    assert NOISE_PROFILE["join"] == 2
    assert JOIN_SPEC.noise == 2


def test_join_spec_exposed():
    assert SPECS == (JOIN_SPEC,)
    assert CUT_SPECS  # SPECS_ALL intacto sin join


# ---- sesión / gates -------------------------------------------------------

def test_join_gate_127_cap0():
    s = Shell(FileSystem(root=DirNode(name="/", children={})), commands=("cat", "ls"))
    r = s.execute("join f1 f2")
    assert r.exit_code == 127
    assert "command not found" in r.stderr


def test_join_ch6_expone():
    s = Shell(_fs(), commands=DEFAULT_CH6_COMMANDS)
    r = s.execute("join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv")
    assert r.exit_code == 0
    assert "PR-0091" in r.stdout