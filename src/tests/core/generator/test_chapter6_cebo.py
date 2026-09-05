"""O3 05/09 — Cebo del Faro: el 0 que miente por ruta

Criterio: generate(42,6) expone cebo; grep ENSAYO purgas.csv|wc -l desde / → 0 con stderr, exit 0
Con absoluta o cd → 1
"""
from core.curriculum import load_curriculum
from core.generator import generate, new_session
from core.generator.chapter6 import CEBO_RUTA_FILE, CEBO_RUTA_PATH


def test_cebo_presente_y_canonico_intacto():
    inc = generate(42, 6, curriculum=load_curriculum())
    shell = new_session(inc)
    # Cebo fichero presente
    assert shell.fs.resolve(CEBO_RUTA_PATH, '/') is not None
    # Canónico absoluto intacto
    r = shell.execute("grep ENSAYO /srv/camara-faro/purgas.csv | wc -l")
    assert r.stdout.strip() == "1"
    assert r.exit_code == 0


def test_cebo_ruta_relativa_miente_con_0():
    inc = generate(42, 6, curriculum=load_curriculum())
    shell = new_session(inc)
    # cwd es / (option_b)
    assert shell.cwd == "/"
    # grep relativo sin cd → 0 honesto, stderr de grep, exit 0 del wc
    r = shell.execute("grep ENSAYO purgas.csv | wc -l")
    assert r.stdout.strip() == "0"
    # wc decide exit 0, pero grep avisa por stderr
    assert "No such file" in r.stderr or "purgas.csv" in r.stderr
    assert r.exit_code == 0
    # Con absoluta o tras cd → 1
    shell2 = new_session(inc)
    shell2.execute("cd /srv/camara-faro")
    r2 = shell2.execute("grep ENSAYO purgas.csv | wc -l")
    assert r2.stdout.strip() == "1"
    r3 = shell2.execute("grep ENSAYO /srv/camara-faro/purgas.csv | wc -l")
    assert r3.stdout.strip() == "1"
