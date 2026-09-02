"""Tests puros del prompt y de las líneas de terminal (Seath, 02/09).

Sin pyxel, sin display. Cubren H2.
"""

from render.terminal import build_prompt, terminal_lines, wrap_lines
from render.theme import TERM_COLS
from core.generator import generate, new_session
from core.generator.chapter0 import OFFICE_DIR


def test_build_prompt_cwd_root():
    assert build_prompt("cero", "oficina-vecinal-muelle-norte", "/") == "cero@oficina-vecinal-muelle-norte:/$"


def test_build_prompt_cwd_srv():
    assert build_prompt("cero", "nodo", "/srv") == "cero@nodo:/srv$"


def test_build_prompt_usuario_generico():
    # El plan menciona `usuario@nodo:/ruta$` como convención; el helper lo permite.
    assert build_prompt("usuario", "nodo", "/srv") == "usuario@nodo:/srv$"


def test_wrap_lines_corta():
    assert wrap_lines("hola", 10) == ["hola"]


def test_wrap_lines_corte_duro():
    assert wrap_lines("abcdefghij", 5) == ["abcde", "fghij"]


def test_wrap_lines_respeta_saltos():
    assert wrap_lines("a\nb\nc", 10) == ["a", "b", "c"]


def test_terminal_lines_sin_historial():
    inc = generate(7, chapter=0)
    shell = new_session(inc)
    lines = terminal_lines(shell, inc.room.host)
    assert lines[0][0] == build_prompt("cero", inc.room.host, shell.cwd)
    assert len(lines) == 1


def test_terminal_lines_con_ls_real():
    inc = generate(42, chapter=0)
    shell = new_session(inc)
    shell.execute(f"ls {OFFICE_DIR}")
    lines = terminal_lines(shell, inc.room.host)
    # Primera línea es el prompt solo (host largo → split).
    assert lines[0][0].startswith("cero@")
    # Debe contener el comando ls en la segunda línea.
    assert any("ls" in t for t, _ in lines)
    # Y la salida del ls (al menos README).
    assert any("README" in t for t, _ in lines)
    assert any("nombre_de_proveedor.txt" in t for t, _ in lines)


def test_prompt_no_desborda_term_cols():
    # Host muy largo no debe producir prompt > TERM_COLS sin truncar.
    long_host = "x" * 80
    p = build_prompt("cero", long_host, "/srv/oficina-vecinal-muelle-norte")
    assert len(p) <= TERM_COLS
    assert p.endswith("…") or len(p) < TERM_COLS + 10
