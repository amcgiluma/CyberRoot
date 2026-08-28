"""Golden tests de los comandos del sandbox (ARCHITECTURE §2.2, H2 PLAN).

Comandos `ls`/`cd` (navigation.py) y `cat`/`cp` (files.py) + contratos base
(`CommandResult`, `CommandSpec`, `CommandRegistry`). Cada test compara
stdout/stderr/exit code BYTE A BYTE contra el resultado GNU real documentado
(DESIGN §2.6.8, PLAN decisiones 2-3): `ls` una columna ordenada por codepoint
y exit 2 ante error; `cd` builtin que normaliza y valida; `cat` que conserva
el contenido exacto y termina en 1 ante error; `cp` que copia metadatos y
mapea `FsError` a texto GNU. Docstrings en español.
"""

from __future__ import annotations

import pytest

from core.sandbox.commands.base import (
    CommandRegistry,
    CommandResult,
    CommandSpec,
    build_registry,
    noise_event,
)
from core.sandbox.commands.files import (
    CP_SPEC,
    CAT_SPEC,
    SPECS as FILE_SPECS,
    _run_cat,
    _run_cp,
)
from core.sandbox.commands.navigation import (
    CD_SPEC,
    LS_SPEC,
    SPECS as NAV_SPECS,
    _run_cd,
    _run_ls,
)
from core.sandbox.fs import DirNode, FileNode, FileSystem


def _fs() -> FileSystem:
    """Fixture: árbol de ejemplo con ficheros, dirs vacíos y jerarquía."""
    root = DirNode(
        name="/",
        children={
            "etc": DirNode(
                name="etc",
                children={"passwd": FileNode(name="passwd", content="root:0\n", mtime=1)},
            ),
            "home": DirNode(
                name="home",
                children={
                    "b.txt": FileNode(name="b.txt", content="bee\n", mtime=4),
                    "empty": DirNode(name="empty"),
                    "file.txt": FileNode(
                        name="file.txt", content="hi", owner="alice", group="staff",
                        mode="600", mtime=3,
                    ),
                    "log.txt": FileNode(
                        name="log.txt", content="log line\nwithout-end", mtime=2
                    ),
                    "node": DirNode(
                        name="node",
                        children={
                            "inner.txt": FileNode(name="inner.txt", content="inner\n", mtime=5),
                            "sub": DirNode(
                                name="sub",
                                children={"deep.txt": FileNode(name="deep.txt", content="deep\n", mtime=6)},
                            ),
                        },
                    ),
                },
            ),
        },
    )
    return FileSystem(root=root)


# ---- contratos base ------------------------------------------------


def test_command_result_roundtrip_dict_exacto() -> None:
    """to_dict/from_dict de CommandResult es ida y vuelta exacta (noise como lista)."""
    res = CommandResult(stdout="a\nb\n", stderr="ls: x: err", exit_code=2,
                        noise=noise_event("ls", ("x",), 7), new_cwd=None)
    assert CommandResult.from_dict(res.to_dict()) == res
    # noise se serializa como lista.
    assert isinstance(res.to_dict()["noise"], list)
    assert res.ok is False


def test_command_result_ok_es_exit_zero() -> None:
    """.ok refleja exactamente exit_code == 0."""
    assert CommandResult().ok
    assert not CommandResult(exit_code=1).ok
    assert not CommandResult(exit_code=127).ok


def test_registry_registra_obtiene_y_ordena_por_codepoint() -> None:
    """names/specs salen ordenados por codepoint; get devuelve None si falta."""
    reg = build_registry(NAV_SPECS + FILE_SPECS)
    assert reg.names() == ("cat", "cd", "cp", "ls")
    assert [s.name for s in reg.specs()] == ["cat", "cd", "cp", "ls"]
    assert reg.get("ls") is LS_SPEC
    assert reg.get("cd") is CD_SPEC
    assert reg.get("cp") is CP_SPEC
    assert reg.get("cat") is CAT_SPEC
    assert reg.get("zzz_inventado") is None


def test_registry_sobrescribe_por_nombre() -> None:
    """register con el mismo nombre sobrescribe la spec anterior."""
    reg = CommandRegistry()
    dummy = CommandSpec(name="ls", concepts=frozenset(), noise=0,
                        run=lambda fs, cwd, argv, tick: CommandResult())
    reg.register(LS_SPEC)
    reg.register(dummy)
    assert reg.get("ls") is dummy
    assert reg.names() == ("ls",)


def test_command_registry_es_instancia_no_global() -> None:
    """Dos registries no comparten estado (sin globals mutables, ARCHITECTURE §3)."""
    a = CommandRegistry()
    b = CommandRegistry()
    a.register(LS_SPEC)
    assert b.names() == ()
    assert a.names() == ("ls",)


def test_noise_event_tiene_forma_event_con_cantidad_del_perfil() -> None:
    """Cada comando emite un `Event` de ruido con su cantidad de NOISE_PROFILE."""
    (ev,) = noise_event("ls", ("a",), 3)
    assert ev.to_dict() == {
        "type": "event.noise",
        "data": {"command": "ls", "amount": 1, "argv": ["a"]},
        "tick": 3,
    }
    assert noise_event("cd", (), 0)[0].data["amount"] == 0
    assert noise_event("cat", ("f",), 1)[0].data["amount"] == 1
    assert noise_event("cp", ("s", "d"), 2)[0].data["amount"] == 3


# ---- ls -------------------------------------------------------------


def test_ls_una_columna_ordenada_por_codepoint() -> None:
    """ls sin operandos lista la cwd, una entrada por línea, orden codepoint."""
    fs = _fs()
    res = _run_ls(fs, "/home", (), 0)
    assert res.stdout == "".join(f"{n}\n" for n in ["b.txt", "empty", "file.txt", "log.txt", "node"])
    assert res.stderr == ""
    assert res.exit_code == 0
    assert res.ok


def test_ls_de_un_fichero_imprime_el_operando_tal_cual() -> None:
    """GNU `ls ruta/a/fichero` imprime `ruta/a/fichero`, no el nombre base."""
    fs = _fs()
    res = _run_ls(fs, "/", ("/home/file.txt",), 0)
    assert res.stdout == "/home/file.txt\n"
    assert res.exit_code == 0


def test_ls_fichero_con_barra_final_es_not_a_directory() -> None:
    """GNU `ls fichero/` → «Not a directory» (exit 2), no lo imprime."""
    fs = _fs()
    res = _run_ls(fs, "/", ("/home/file.txt/",), 0)
    assert res.stdout == ""
    assert res.stderr == "ls: cannot access '/home/file.txt/': Not a directory"
    assert res.exit_code == 2


def test_ls_dir_con_barra_final_sin_cabecera() -> None:
    """GNU `ls /etc/` con UN operando: sin cabecera, solo hijos (sonda real)."""
    fs = _fs()
    res = _run_ls(fs, "/", ("/etc/",), 0)
    assert res.stdout == "passwd\n"
    assert res.exit_code == 0


def test_ls_varios_operandos_formato_dir_cabeceras() -> None:
    """ls de dirs imprime `op:` como cabecera y luego sus hijos (multi-operando)."""
    fs = _fs()
    res = _run_ls(fs, "/", ("/home/node", "/etc"), 0)
    assert res.stdout == (
        "/home/node:\n"
        "inner.txt\n"
        "sub\n"
        "\n"
        "/etc:\n"
        "passwd\n"
    )
    assert res.stderr == ""
    assert res.exit_code == 0


def test_ls_operando_inexistente_y_valido_sigue_y_exit_2() -> None:
    """Un operando erróneo anota stderr exacto, exit 2, y NO corta los demás."""
    fs = _fs()
    res = _run_ls(fs, "/", ("nope", "/etc"), 0)
    assert res.stdout == "/etc:\npasswd\n"
    assert res.stderr == "ls: cannot access 'nope': No such file or directory"
    assert res.exit_code == 2
    assert not res.ok


def test_ls_operando_a_traves_de_fichero_not_a_directory() -> None:
    """ls descender bajo un fichero produce el mensaje 'Not a directory'."""
    fs = _fs()
    res = _run_ls(fs, "/home", ("file.txt/zz",), 0)
    assert res.stdout == ""
    assert res.stderr == "ls: cannot access 'file.txt/zz': Not a directory"
    assert res.exit_code == 2


# ---- cd -------------------------------------------------------------


def test_cd_sin_argumentos_va_a_la_raiz() -> None:
    """cd con 0 operandos va al home=raíz '/', sin tocar el FS."""
    fs = _fs()
    res = _run_cd(fs, "/home/node", (), 0)
    assert res.new_cwd == "/"
    assert res.exit_code == 0
    assert res.stdout == ""


def test_cd_ok_devuelve_cwd_normalizada_sin_barra_final() -> None:
    """cd a destino válido normaliza la ruta y colapsa la barra final."""
    fs = _fs()
    # Ruta relativa simple.
    res = _run_cd(fs, "/", ("home",), 0)
    assert res.new_cwd == "/home"
    # Barra final colapsada: mismo resultado normalizado.
    res2 = _run_cd(fs, "/", ("home/",), 0)
    assert res2.new_cwd == "/home"
    # Varios niveles /`..` sobre cwds REALES (get_dir valida contra el FS).
    res3 = _run_cd(fs, "/home", ("node/sub",), 0)
    assert res3.new_cwd == "/home/node/sub"
    res4 = _run_cd(fs, "/home/node", ("..",), 0)
    assert res4.new_cwd == "/home"
    for r in (res, res2, res3, res4):
        assert r.exit_code == 0


def test_cd_a_un_fichero_not_a_directory_exit_1() -> None:
    """cd a un fichero produce 'Not a directory' y NO cambia la cwd."""
    fs = _fs()
    res = _run_cd(fs, "/home", ("file.txt",), 0)
    assert res.stderr == "cd: file.txt: Not a directory"
    assert res.exit_code == 1
    assert res.new_cwd is None


def test_cd_inexistente_no_such_file_exit_1() -> None:
    """cd a un destino ausente produce el mensaje GNU y exit 1, sin new_cwd."""
    fs = _fs()
    res = _run_cd(fs, "/home", ("nope",), 0)
    assert res.stderr == "cd: nope: No such file or directory"
    assert res.exit_code == 1
    assert res.new_cwd is None


def test_cd_demasiados_argumentos() -> None:
    """cd con más de un operando es 'cd: too many arguments' (bash real)."""
    fs = _fs()
    res = _run_cd(fs, "/home", ("a", "b"), 0)
    assert res.stderr == "cd: too many arguments"
    assert res.exit_code == 1
    assert res.new_cwd is None


# ---- cat ------------------------------------------------------------


def test_cat_preserva_contenido_sin_newline_final() -> None:
    """cat NO añade un \n extra: vuelca el contenido exacto (sin newline final)."""
    fs = _fs()
    res = _run_cat(fs, "/home", ("log.txt",), 0)
    assert res.stdout == "log line\nwithout-end"
    assert res.exit_code == 0


def test_cat_varios_ficheros_concatenados_byte_a_byte() -> None:
    """cat concatena los ficheros en orden, respetando sus newlines ya presentes."""
    fs = _fs()
    res = _run_cat(fs, "/", ("/home/file.txt", "/etc/passwd"), 0)
    assert res.stdout == "hi" + "root:0\n"
    assert res.exit_code == 0


def test_cat_inexistente_stderr_y_exit_1() -> None:
    """cat de un fichero ausente: mensaje GNU, stderr exacto, exit 1."""
    fs = _fs()
    res = _run_cat(fs, "/home", ("nope.txt",), 0)
    assert res.stdout == ""
    assert res.stderr == "cat: nope.txt: No such file or directory"
    assert res.exit_code == 1


def test_cat_de_un_directorio_is_a_directory_exit_1() -> None:
    """cat de un directorio produce 'Is a directory' y exit 1."""
    fs = _fs()
    res = _run_cat(fs, "/home", ("node",), 0)
    assert res.stderr == "cat: node: Is a directory"
    assert res.exit_code == 1


def test_cat_mixto_bueno_y_malo_imprime_bueno_y_exit_1() -> None:
    """cat con bueno+malo imprime el bueno, anota el malo en stderr y termina en 1."""
    fs = _fs()
    res = _run_cat(fs, "/home", ("file.txt", "nope.txt"), 0)
    assert res.stdout == "hi"
    assert res.stderr == "cat: nope.txt: No such file or directory"
    assert res.exit_code == 1


def test_cat_sin_argumentos_error_didactico_v0() -> None:
    """cat sin operandos: v0 sin stdin → error didáctico claro, exit 1."""
    fs = _fs()
    res = _run_cat(fs, "/home", (), 0)
    assert res.stdout == ""
    assert res.stderr == "cat: no input file given"
    assert res.exit_code == 1


# ---- cp -------------------------------------------------------------


def test_cp_ok_copia_contenido_y_metadatos() -> None:
    """cp copia contenido, dueño, grupo, modo y mtime al destino (PLAN decisión)."""
    fs = _fs()
    res = _run_cp(fs, "/", ("/home/file.txt", "/etc/copy.txt"), 0)
    assert res.exit_code == 0
    assert res.stdout == ""
    assert res.stderr == ""
    orig = fs.resolve("/home/file.txt")
    dest = fs.resolve("/etc/copy.txt")
    assert isinstance(orig, FileNode)
    assert isinstance(dest, FileNode)
    assert dest.content == orig.content == "hi"
    assert dest.owner == orig.owner == "alice"
    assert dest.group == orig.group == "staff"
    assert dest.mode == orig.mode == "600"
    assert dest.mtime == orig.mtime == 3


def test_cp_sobrescribe_destino_existente() -> None:
    """cp sin -i sobrescribe el fichero destino existente con contenido y metadatos."""
    fs = _fs()
    res = _run_cp(fs, "/", ("/home/file.txt", "/etc/passwd"), 0)
    assert res.exit_code == 0
    dest = fs.resolve("/etc/passwd")
    assert isinstance(dest, FileNode)
    assert dest.content == "hi"
    assert dest.mtime == 3  # el del fuente, no el 1 original de passwd


def test_cp_a_directorio_existente_copia_dentro() -> None:
    """GNU real: `cp fichero dir/` copia DENTRO del dir (dir/fichero)."""
    fs = _fs()
    res = _run_cp(fs, "/", ("/home/file.txt", "/home/empty"), 0)
    assert res.exit_code == 0
    assert res.stderr == ""
    dentro = fs.resolve("/home/empty/file.txt")
    assert isinstance(dentro, FileNode)
    assert dentro.content == "hi"
    assert dentro.mtime == 3


def test_cp_a_directorio_existente_con_colision_sobrescribe() -> None:
    """Si dir/<base> ya existe como fichero, `cp fichero dir/` lo sobrescribe."""
    fs = _fs()
    # empty/log.txt existe (ver fixture); copiamos file.txt como log.txt:
    # primero copiamos a un nombre base que exista dentro de /home/empty.
    res = _run_cp(fs, "/", ("/home/file.txt", "/home/empty"), 0)
    assert res.exit_code == 0
    # Colisión: el segundo cp encuentra empty/file.txt ya existente → sobrescribe.
    res2 = _run_cp(fs, "/", ("/home/file.txt", "/home/empty/"), 0)
    assert res2.exit_code == 0
    destino = fs.resolve("/home/empty/file.txt")
    assert isinstance(destino, FileNode)
    assert destino.content == "hi"
    assert destino.mtime == 3


def test_cp_fichero_sobre_si_mismo_are_the_same_file() -> None:
    """GNU real: `cp f f` → «cp: 'f' and 'f' are the same file», exit 1."""
    fs = _fs()
    res = _run_cp(fs, "/", ("/etc/passwd", "/etc/passwd"), 0)
    assert res.exit_code == 1
    assert res.stderr == "cp: '/etc/passwd' and '/etc/passwd' are the same file"
    # GNU rechaza la operación: el contenido no cambia.
    assert fs.resolve("/etc/passwd").content == "root:0\n"


def test_cp_dentro_de_si_mismo_invalid_argument() -> None:
    """cp cuyo destino cae bajo el propio fuente produce 'Invalid argument'."""
    fs = _fs()
    res = _run_cp(fs, "/", ("/home/file.txt", "/home/file.txt/sub"), 0)
    assert res.stderr == "cp: /home/file.txt/sub: Invalid argument"
    assert res.exit_code == 1


def test_cp_fuente_inexistente_cannot_stat() -> None:
    """cp con fuente ausente produce el mensaje GNU 'cannot stat' con el src."""
    fs = _fs()
    res = _run_cp(fs, "/", ("/no/existe", "/etc/x"), 0)
    assert res.stderr == "cp: cannot stat '/no/existe': No such file or directory"
    assert res.exit_code == 1


def test_cp_padre_del_destino_inexistente_not_found() -> None:
    """cp cuyo padre del destino no existe mapea not_found con el dst."""
    fs = _fs()
    res = _run_cp(fs, "/", ("/home/file.txt", "/no/existe/dest.txt"), 0)
    assert res.stderr == "cp: /no/existe/dest.txt: No such file or directory"
    assert res.exit_code == 1


def test_cp_cero_argumentos_missing_file_operand() -> None:
    """cp sin operandos: 'missing file operand' (faltan src y dst)."""
    fs = _fs()
    res = _run_cp(fs, "/home", (), 0)
    assert res.stderr == "cp: missing file operand"
    assert res.exit_code == 1


def test_cp_un_argumento_missing_destination() -> None:
    """cp con un solo operando: 'missing destination file operand'."""
    fs = _fs()
    res = _run_cp(fs, "/home", ("file.txt",), 0)
    assert res.stderr == "cp: missing destination file operand"
    assert res.exit_code == 1


def test_cp_demasiados_argumentos_target_no_es_directorio() -> None:
    """cp con >2 operandos: el último sería dir destino (no soportado) → error GNU."""
    fs = _fs()
    res = _run_cp(fs, "/home", ("file.txt", "b.txt", "dest"), 0)
    assert res.stderr == "cp: target 'dest' is not a directory"
    assert res.exit_code == 1