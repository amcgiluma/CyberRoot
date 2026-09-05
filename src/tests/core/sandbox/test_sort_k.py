"""S1 (05/09) — sort -k/-t/-n: lectura VERTICAL de la Lista (Smough).

GNU-honesto: `-k` por columna delimitada, `-t` con `|` y `-n` numérico.
Verifica que `sort -t'|' -k12 -n purgas.csv | head -n 3` existe y que los usos
actuales (`sort|head`, `sort|uniq -c`) siguen byte-idénticos.
"""

from __future__ import annotations

from core.sandbox.commands.conteo import _run_sort, SORT_SPEC
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell

PURGAS = (
    "001|foo|bar|Alpha|a|b|c|d|e|f|g|10\n"
    "002|foo|bar|Beta|a|b|c|d|e|f|g|2\n"
    "003|foo|bar|Alpha|a|b|c|d|e|f|g|2\n"
    "004|foo|bar|Gamma|a|b|c|d|e|f|g|1\n"
)


def _fs(files: dict[str, str]) -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={k: FileNode(name=k, content=v) for k, v in files.items()}))


def test_sort_t_pipe_k12_numerico_ordena_por_puntuacion() -> None:
    """`sort -t'|' -k12 -n` ordena por columna 12 (puntuación) numérico."""
    fs = _fs({"purgas.csv": PURGAS})
    res = _run_sort(fs, "/", ("-t|", "-k12", "-n", "purgas.csv"), tick=0)
    assert res.exit_code == 0
    assert res.stderr == ""
    assert res.stdout == (
        "004|foo|bar|Gamma|a|b|c|d|e|f|g|1\n"
        "002|foo|bar|Beta|a|b|c|d|e|f|g|2\n"
        "003|foo|bar|Alpha|a|b|c|d|e|f|g|2\n"
        "001|foo|bar|Alpha|a|b|c|d|e|f|g|10\n"
    )


def test_sort_k12n_sufijo_numerico_equivale_a_guion_n() -> None:
    """`sort -t'|' -k12n` (sufijo n) equivale a `-k12 -n`."""
    fs = _fs({"purgas.csv": PURGAS})
    res = _run_sort(fs, "/", ("-t|", "-k12n", "purgas.csv"), tick=0)
    assert res.exit_code == 0
    assert res.stdout == (
        "004|foo|bar|Gamma|a|b|c|d|e|f|g|1\n"
        "002|foo|bar|Beta|a|b|c|d|e|f|g|2\n"
        "003|foo|bar|Alpha|a|b|c|d|e|f|g|2\n"
        "001|foo|bar|Alpha|a|b|c|d|e|f|g|10\n"
    )


def test_sort_k_con_delimitador_pipe_y_sin_n_lexicografico() -> None:
    """`-k2` con `-t|` usa desde campo 2 hasta final (GNU: a campo final)."""
    fs = _fs({"f": "b|2|z\na|10|x\nc|1|y\n"})
    # -k2 lexicográfico por clave "10|x","1|y","2|z"
    res = _run_sort(fs, "/", ("-t|", "-k2", "f"), tick=0)
    assert res.exit_code == 0
    assert res.stdout == "a|10|x\nc|1|y\nb|2|z\n"
    # -k2,2 solo campo 2 exacto -> lex "1","10","2"
    res2 = _run_sort(fs, "/", ("-t|", "-k2,2", "f"), tick=0)
    assert res2.stdout == "c|1|y\na|10|x\nb|2|z\n"


def test_sort_k_sin_t_default_blanco_token2() -> None:
    """`sort -k2` sin `-t` usa whitespace (tokens colapsados)."""
    fs = _fs({"f": "b 2 z\na 10 x\nc 1 y\n"})
    res = _run_sort(fs, "/", ("-k2", "f"), tick=0)
    assert res.exit_code == 0
    # tokens 2: 2,10,1 -> lex 1,10,2
    assert res.stdout == "c 1 y\na 10 x\nb 2 z\n"


def test_sort_fallback_columna_inexistente_no_crashea() -> None:
    """`-k12` sobre líneas sin 12 columnas → fallback vacío, no crashea."""
    fs = _fs({"w": "a|b\nc\nd|e|f\n"})
    res = _run_sort(fs, "/", ("-t|", "-k12", "-n", "w"), tick=0)
    assert res.exit_code == 0
    # claves vacías (0) ordenan primero, mantienen determinismo
    assert res.stdout == "a|b\nc\nd|e|f\n"
    # Sin -k, mismo fichero byte-idéntico a orden lexical byte
    res2 = _run_sort(fs, "/", ("w",), tick=0)
    assert res2.stdout == "a|b\nc\nd|e|f\n"


def test_sort_errores_gnu_multi_char_y_k_cero() -> None:
    """Errores GNU honestos: multi-char tab y campo cero."""
    fs = _fs({"f": "a\n"})
    res = _run_sort(fs, "/", ("-t||", "-k2", "f"), tick=0)
    assert res.exit_code == 2
    assert "multi-character tab" in res.stderr
    res2 = _run_sort(fs, "/", ("-k0", "f"), tick=0)
    assert res2.exit_code == 2
    assert "field number is zero" in res2.stderr
    res3 = _run_sort(fs, "/", ("-t",), tick=0)
    assert res3.exit_code == 2
    assert "option requires an argument" in res3.stderr


def test_sort_usos_actuales_byte_identicos() -> None:
    """Los usos actuales `sort|head` y `sort|uniq -c` siguen byte-idénticos."""
    # cap.2: sort | head en datos de turnos no usado, simulamos sort default
    data = "zeta\nalpha\nalpha\nbeta\nDelta\n"
    fs = _fs({"datos.txt": data})
    res = _run_sort(fs, "/", ("datos.txt",), tick=0)
    assert res.stdout == "Delta\nalpha\nalpha\nbeta\nzeta\n"
    # Faro: sort | uniq -c  (orden + colapso)
    from core.sandbox.commands.conteo import _run_uniq

    res_sort = _run_sort(fs, "/", (), tick=0, stdin="b\na\na\n")
    assert res_sort.stdout == "a\na\nb\n"
    res_uniq = _run_uniq(fs, "/", ("-c",), tick=0, stdin=res_sort.stdout)
    assert res_uniq.stdout == "      2 a\n      1 b\n"
    # Shell pipeline completo sort -t'|' -k12 -n | head -n 3 (E3 del Faro)
    fs2 = FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "camara-faro": DirNode(
                            name="camara-faro",
                            children={"purgas.csv": FileNode(name="purgas.csv", content=PURGAS)},
                        )
                    },
                )
            },
        )
    )
    shell = Shell(
        fs2,
        cwd="/",
        commands=("cat", "cd", "cp", "cut", "env", "grep", "head", "kill", "ls", "ps", "sort", "sudo", "tail", "uniq", "wc"),
    )
    r = shell.execute("sort -t'|' -k12 -n /srv/camara-faro/purgas.csv | head -n 3")
    assert r.exit_code == 0
    assert r.stdout == (
        "004|foo|bar|Gamma|a|b|c|d|e|f|g|1\n"
        "002|foo|bar|Beta|a|b|c|d|e|f|g|2\n"
        "003|foo|bar|Alpha|a|b|c|d|e|f|g|2\n"
    )


def test_sort_stdin_y_ruido_perfil_intacto() -> None:
    """Stdin + ruido 2 intacto (misma clase que sort hoy)."""
    fs = _fs({})
    res = _run_sort(fs, "/", ("-t|", "-k2", "-n"), tick=0, stdin="b|2\nc|1\na|10\n")
    assert res.exit_code == 0
    assert res.stdout == "c|1\nb|2\na|10\n"
    assert SORT_SPEC.noise == 2
