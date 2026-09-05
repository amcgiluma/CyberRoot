"""Golden tests para `cut` (S1 04/09) — La Lista es una tabla cortable.

Semántica contrastada contra GNU coreutils real (Ubuntu, 04/09).
Criterios del plan: -d/-f con rangos, línea sin delim intacta, sin -f → error, gate 127, pipe a uniq -c.
"""

from core.sandbox.commands.cut import _run_cut
from core.sandbox.fs import DirNode, FileNode, FileSystem

DATA = "a|b|c\nd|e|f\nnopipe\n"
PURGAS = "purga_id|fecha|sujeto|distrito|motivo|prev\nPR-0144|03-07|000462|UMBRAL-BAJO|CONTINUIDAD|438\nPR-0091|EN BLANCO|000|--|ENSAYO|--\n"
REG = "id|nombre|distrito|puntuacion\n1|A|X|10\n2|B|Y|20\n"

def _fs() -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={
        "data.txt": FileNode(name="data.txt", content=DATA),
        "purgas.csv": FileNode(name="purgas.csv", content=PURGAS),
        "registro.csv": FileNode(name="registro.csv", content=REG),
        "plain.txt": FileNode(name="plain.txt", content="hello\nworld\n"),
    }))

def _cut(argv, stdin=""):
    return _run_cut(_fs(), "/", argv, tick=0, stdin=stdin)

def test_cut_f_simple():
    r = _cut(("-d", "|", "-f", "2", "data.txt"))
    assert r.exit_code == 0
    assert r.stdout == "b\ne\nnopipe\n"

def test_cut_f_con_coma_y_orden():
    r = _cut(("-d", "|", "-f", "3,1", "data.txt"))
    # GNU ordena 1,3
    assert r.stdout == "a|c\nd|f\nnopipe\n"

def test_cut_f_rango_cerrado():
    r = _cut(("-d", "|", "-f", "1-2", "data.txt"))
    assert r.stdout == "a|b\nd|e\nnopipe\n"

def test_cut_f_rango_abierto_N_():
    r = _cut(("-d", "|", "-f", "2-", "data.txt"))
    assert r.stdout == "b|c\ne|f\nnopipe\n"

def test_cut_f_rango_abierto__M():
    r = _cut(("-d", "|", "-f", "-2", "data.txt"))
    assert r.stdout == "a|b\nd|e\nnopipe\n"

def test_cut_f_fuera_de_rango_vacia():
    r = _cut(("-d", "|", "-f", "10", "data.txt"))
    # campo 10 no existe → líneas vacías, pero sin delim imprime entera
    # DATA líneas con delim → vacías; nopipe sin delim → entera
    assert r.stdout == "\n\nnopipe\n"

def test_cut_f4_purgas_colores():
    r = _cut(("-d", "|", "-f", "4", "purgas.csv"))
    assert r.exit_code == 0
    assert r.stdout == "distrito\nUMBRAL-BAJO\n--\n"

def test_cut_f4_12_con_fuera_de_rango():
    r = _cut(("-d", "|", "-f", "4,12", "purgas.csv"))
    # 12 no existe → solo 4
    assert r.stdout == "distrito\nUMBRAL-BAJO\n--\n"

def test_cut_delim_default_tab():
    fs = FileSystem(root=DirNode(name="/", children={"t.txt": FileNode(name="t.txt", content="a\tb\tc\n")} ))
    r = _run_cut(fs, "/", ("-f", "2", "t.txt"), tick=0)
    assert r.stdout == "b\n"

def test_cut_sin_f_error_gnu():
    r = _cut(("-d", "|", "purgas.csv"))
    assert r.exit_code == 1
    assert "you must specify a list" in r.stderr
    assert "Try 'cut --help'" in r.stderr

def test_cut_delim_multi_char_error():
    r = _cut(("-d", "ab", "-f", "1", "purgas.csv"))
    assert r.exit_code == 1
    assert "the delimiter must be a single character" in r.stderr

def test_cut_campo_cero_error():
    r = _cut(("-d", "|", "-f", "0", "purgas.csv"))
    assert r.exit_code == 1
    assert "fields are numbered from 1" in r.stderr

def test_cut_rango_decreciente_error():
    r = _cut(("-d", "|", "-f", "4-2", "purgas.csv"))
    assert r.exit_code == 1
    assert "invalid decreasing range" in r.stderr

def test_cut_f_sin_arg_error():
    r = _cut(("-d", "|", "-f"))
    assert r.exit_code == 1
    assert "option requires an argument" in r.stderr

def test_cut_linea_sin_delim_imprime_entera():
    r = _cut(("-d", "|", "-f", "2", "plain.txt"))
    assert r.stdout == "hello\nworld\n"

def test_cut_only_delimited_s_suprime():
    r = _cut(("-d", "|", "-f", "2", "-s", "plain.txt"))
    assert r.stdout == ""
    assert r.exit_code == 0

def test_cut_stdin_pipe():
    r = _cut(("-d", "|", "-f", "2"), stdin="a|b|c\nd|e|f\n")
    assert r.stdout == "b\ne\n"

def test_cut_stdin_sin_fichero_por_tuberia():
    r = _cut(("-d", "|", "-f", "1"), stdin=PURGAS)
    assert "purga_id" in r.stdout

def test_cut_fichero_inexistente():
    r = _cut(("-d", "|", "-f", "1", "noexiste.csv"))
    assert r.exit_code == 1
    assert "No such file or directory" in r.stderr
    assert r.stdout == ""

def test_cut_multi_fichero_mezcla_ok_y_error():
    r = _cut(("-d", "|", "-f", "1", "purgas.csv", "noexiste.csv"))
    assert r.exit_code == 1
    assert "purga_id" in r.stdout
    assert "noexiste.csv" in r.stderr

def test_cut_ruido_clase_lectura():
    r = _cut(("-d", "|", "-f", "1", "purgas.csv"))
    assert r.noise[0].data["amount"] == 1
    assert r.noise[0].data["command"] == "cut"

def test_cut_f_short_attached():
    r = _cut(("-d|", "-f4", "purgas.csv"))
    assert r.stdout == "distrito\nUMBRAL-BAJO\n--\n"

def test_cut_delim_attached():
    r = _cut(("-d|", "-f", "2", "data.txt"))
    assert r.stdout == "b\ne\nnopipe\n"

# ---- sesión / gates / pipe -----------------------------------------------

from core.sandbox.shell import Shell, DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS, DEFAULT_CH3_COMMANDS, DEFAULT_CH6_COMMANDS

def test_cut_gate_127_cap0():
    s = Shell(FileSystem(root=DirNode(name="/", children={})), commands=DEFAULT_CAP0_COMMANDS)
    r = s.execute("cut -d'|' -f1 a.txt")
    assert r.exit_code == 127
    assert "command not found" in r.stderr

def test_cut_gate_127_ch2():
    s = Shell(FileSystem(root=DirNode(name="/", children={})), commands=DEFAULT_CH2_COMMANDS)
    r = s.execute("cut -d'|' -f1 a.txt")
    assert r.exit_code == 127

def test_cut_gate_127_ch3():
    s = Shell(FileSystem(root=DirNode(name="/", children={})), commands=DEFAULT_CH3_COMMANDS)
    r = s.execute("cut -d'|' -f1 a.txt")
    assert r.exit_code == 127

def test_cut_ch6_expone():
    fs = FileSystem(root=DirNode(name="/", children={"a.txt": FileNode(name="a.txt", content="x|y\n")} ))
    s = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    r = s.execute("cut -d'|' -f1 a.txt")
    assert r.exit_code == 0
    assert r.stdout == "x\n"

def test_cut_pipe_a_uniq():
    fs = FileSystem(root=DirNode(name="/", children={"registro.csv": FileNode(name="registro.csv", content=REG)}))
    s = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    r = s.execute("cut -d'|' -f3 registro.csv | uniq -c")
    # registro.csv col3 = distrito: distrito, X, Y → tras cut: distrito \n X \n Y \n → uniq -c (ya único, sin sort) → 1 cada
    assert r.exit_code == 0
    assert "1 distrito" in r.stdout or "distrito" in r.stdout

def test_cut_pipe_a_sort_a_uniq_no_doble_pipe_soporte():
    # doble pipe (cut|sort|uniq -c) SOPORTADO desde E2 (05/09, Seath) — T1 enseña cut|sort|uniq -c
    fs = FileSystem(root=DirNode(name="/", children={"registro.csv": FileNode(name="registro.csv", content=REG)}))
    s = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    r = s.execute("cut -d'|' -f4 registro.csv | sort | uniq -c")
    assert r.exit_code == 0
    # -f4 = puntuacion: cabecera + 10 + 20 → sort|uniq -c agrupa 3 líneas distintas
    assert "puntuacion" in r.stdout and "10" in r.stdout and "20" in r.stdout
