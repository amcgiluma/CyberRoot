"""Tests del FS virtual (ARCHITECTURE §2.2, H1 del PLAN.md).

Cubren resolución de rutas (absoluta/relativa/`..`/`.`/`//` colapsada/barra
final), errores estructurados (not_found / not_a_directory / is_a_directory /
invalid_argument), listado ordenado, cambio de cwd con límite en la raíz,
`copy_file` (ok, sobrescritura, errores) y el roundtrip EXACTO
to_dict/from_dict + snapshot con independencia de mutaciones. Docstrings en
español; nombres de test descriptivos.
"""

from __future__ import annotations

import pytest

from core.sandbox.fs import DirNode, FileNode, FileSystem, FsError


def _build_fs() -> FileSystem:
    """Fixture: árbol de 3 niveles usado por casi todos los tests."""
    deep = DirNode(name="b", children={"deep.txt": FileNode(name="deep.txt", content="deep", mtime=7)})
    node = DirNode(
        name="node",
        children={
            "inner.txt": FileNode(name="inner.txt", content="inner", mtime=5),
            "b": deep,
        },
    )
    home = DirNode(
        name="home",
        children={
            "file.txt": FileNode(name="file.txt", content="hi", owner="alice", group="staff", mode="600", mtime=3),
            "node": node,
        },
    )
    etc = DirNode(name="etc", children={"passwd": FileNode(name="passwd", content="root:0", mtime=1)})
    root = DirNode(name="/", children={"etc": etc, "home": home})
    return FileSystem(root=root)


# ---- resolve: rutas y normalización ----------------------------------


def test_resolve_absoluta_devuelve_fichero() -> None:
    """Resolución absoluta hasta un fichero devuelve el nodo con su contenido."""
    fs = _build_fs()
    nodo = fs.resolve("/home/node/inner.txt")
    assert isinstance(nodo, FileNode)
    assert nodo.content == "inner"


def test_resolve_relativa_se_resuelve_desde_cwd() -> None:
    """Relativa `node/deep.txt` se resuelve partiendo de `/home`."""
    fs = _build_fs()
    nodo = fs.resolve("node/b/deep.txt", cwd="/home")
    assert isinstance(nodo, FileNode)
    assert nodo.content == "deep"


def test_resolve_punto_y_punto_punto() -> None:
    """`.` y `..` navegan dentro y fuera del directorio actual."""
    fs = _build_fs()
    assert fs.resolve("./node", cwd="/home").name == "node"
    nodo = fs.resolve("../etc/passwd", cwd="/home")
    assert isinstance(nodo, FileNode)
    assert nodo.content == "root:0"


def test_resolve_punto_punto_desde_raiz_no_sube() -> None:
    """`..` en la raíz se clampa: no existe `/..` más arriba."""
    fs = _build_fs()
    assert fs.resolve("..", cwd="/") is fs.root


def test_resolve_colapsa_barras_dobles() -> None:
    """Slash dobles (`//home//node`) se colapsan como en un FS real."""
    fs = _build_fs()
    nodo = fs.resolve("//home//node//inner.txt")
    assert isinstance(nodo, FileNode)
    assert nodo.content == "inner"


def test_resolve_barra_final_apunta_a_directorio() -> None:
    """Una barra final no rompe la resolución de un directorio."""
    fs = _build_fs()
    nodo = fs.resolve("/home/node/")
    assert isinstance(nodo, DirNode)
    assert nodo.name == "node"


def test_resolve_inexistente_lanza_not_found() -> None:
    """Un componente final ausente produce kind `not_found`."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.resolve("/home/nope")
    assert exc.value.kind == "not_found"
    assert exc.value.path == "/home/nope"


def test_resolve_ruta_vacia_lanza_not_found() -> None:
    """La ruta vacía se considera inexistente (no el cwd)."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.resolve("")
    assert exc.value.kind == "not_found"


def test_resolve_componente_intermedio_fichero_lanza_not_a_directory() -> None:
    """Atravesar un fichero como directorio produce `not_a_directory`."""
    fs = _build_fs()
    # `file.txt` es fichero, no se puede descender a `/home/file.txt/x`.
    with pytest.raises(FsError) as exc:
        fs.resolve("/home/file.txt/deep")
    assert exc.value.kind == "not_a_directory"


# ---- get_dir / read_file / list_dir ----------------------------------


def test_get_dir_devuelve_directorio() -> None:
    """get_dir sobre un directorio existente devuelve el DirNode."""
    fs = _build_fs()
    assert isinstance(fs.get_dir("/home/node"), DirNode)


def test_get_dir_sobre_fichero_lanza_not_a_directory() -> None:
    """get_dir sobre un fichero produce `not_a_directory`."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.get_dir("/home/file.txt")
    assert exc.value.kind == "not_a_directory"


def test_read_file_devuelve_contenido() -> None:
    """read_file devuelve el contenido exacto de un fichero."""
    fs = _build_fs()
    assert fs.read_file("/home/node/inner.txt") == "inner"


def test_read_file_sobre_directorio_lanza_is_a_directory() -> None:
    """Leer un directorio como fichero produce `is_a_directory`."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.read_file("/home/node")
    assert exc.value.kind == "is_a_directory"


def test_list_dir_ordena_por_codepoint() -> None:
    """Los nombres salen ordenados por codepoint, no por inserción."""
    fs = _build_fs()
    assert fs.list_dir("/home") == ["file.txt", "node"]


def test_list_dir_con_cwd_relativa() -> None:
    """list_dir acepta una ruta relativa a la cwd."""
    fs = _build_fs()
    assert fs.list_dir("node", cwd="/home") == ["b", "inner.txt"]


# ---- change_dir ------------------------------------------------


def test_change_dir_relativo() -> None:
    """`cd node` desde `/home` devuelve `/home/node` normalizado."""
    fs = _build_fs()
    assert fs.change_dir("node", cwd="/home") == "/home/node"


def test_change_dir_absoluto_y_con_slashes() -> None:
    """`cd /etc//` se normaliza a `/etc` (sin barra final)."""
    fs = _build_fs()
    assert fs.change_dir("/etc//", cwd="/home") == "/etc"


def test_change_dir_dos_puntos_suben_un_nivel() -> None:
    """`cd ..` desde `/a/b` devuelve `/a`."""
    fs = _build_fs()
    assert fs.change_dir("..", cwd="/a/b") == "/a"


def test_change_dir_dos_puntos_repetido_no_sube_de_la_raiz() -> None:
    """`../..` desde `/a/b` clampa en la raíz `/` (y no pasa de ahí)."""
    fs = _build_fs()
    assert fs.change_dir("../..", cwd="/a/b") == "/"
    # Más allá de la raíz tampoco sube.
    assert fs.change_dir("../../..", cwd="/a/b") == "/"


# ---- copy_file ------------------------------------------------


def test_copy_file_basico_copia_contenido_y_metadatos() -> None:
    """cp copia contenido, dueño, grupo, modo y mtime del fuente al destino."""
    fs = _build_fs()
    fs.copy_file("/home/node/inner.txt", "/etc/nuevo.txt")
    destino = fs.read_file("/etc/nuevo.txt")
    assert destino == "inner"
    nodo = fs.resolve("/etc/nuevo.txt")
    assert isinstance(nodo, FileNode)
    # mtime del destino = mtime del fuente (decisión documentada del plan).
    assert nodo.mtime == fs.resolve("/home/node/inner.txt").mtime


def test_copy_file_con_destino_relativo() -> None:
    """cp acepta destino relativo a la cwd."""
    fs = _build_fs()
    fs.copy_file("inner.txt", "copia.txt", cwd="/home/node")
    assert fs.read_file("/home/node/copia.txt") == "inner"


def test_copy_file_sobrescribe_fichero_existente() -> None:
    """Si el destino ya es fichero, cp lo sobrescribe (como cp real sin -i)."""
    fs = _build_fs()
    fs.copy_file("/home/node/inner.txt", "/home/file.txt")
    assert fs.read_file("/home/file.txt") == "inner"
    nodo = fs.resolve("/home/file.txt")
    assert isinstance(nodo, FileNode)
    # Conserva los metadatos del fuente.
    assert nodo.owner == "root"
    assert nodo.mode == "644"


def test_copy_file_fuente_inexistente_lanza_not_found() -> None:
    """cp de un fuente ausente produce `not_found`."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.copy_file("/no/existe", "/tmp/x")
    assert exc.value.kind == "not_found"


def test_copy_file_fuente_directorio_lanza_not_a_directory() -> None:
    """cp de un directorio como fuente produce `not_a_directory`."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.copy_file("/home/node", "/opt/x")
    assert exc.value.kind == "not_a_directory"


def test_copy_file_destino_directorio_existente_lanza_is_a_directory() -> None:
    """cp a un directorio existente produce `is_a_directory`."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.copy_file("/home/node/inner.txt", "/etc")
    assert exc.value.kind == "is_a_directory"


def test_copy_file_padre_del_destino_inexistente_lanza_not_found() -> None:
    """El directorio padre del destino debe existir (`not_found` si no)."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.copy_file("/home/node/inner.txt", "/no/existe/dest.txt")
    assert exc.value.kind == "not_found"


def test_copy_file_dentro_de_si_mismo_lanza_invalid_argument() -> None:
    """`cp /a /a/b` (destino bajo el propio fuente) es `invalid_argument`."""
    fs = _build_fs()
    with pytest.raises(FsError) as exc:
        fs.copy_file("/home/file.txt", "/home/file.txt/sub")
    assert exc.value.kind == "invalid_argument"


# ---- roundtrip to_dict/from_dict y snapshot --------------------------


def test_roundtrip_dict_es_exacto() -> None:
    """`from_dict(fs.to_dict()).to_dict()` es IDÉNTICO a `fs.to_dict()`."""
    fs = _build_fs()
    fs2 = FileSystem.from_dict(fs.to_dict())
    assert fs2.to_dict() == fs.to_dict()


def test_roundtrip_dict_produce_copia_independiente() -> None:
    """Mutar el recursado NO altera el FS original (copia profunda)."""
    fs = _build_fs()
    fs2 = FileSystem.from_dict(fs.to_dict())
    # Cambia un contenido anidado en la copia.
    fs2.root.children["home"].children["node"].children["inner.txt"].content = "ROTO"
    assert fs.read_file("/home/node/inner.txt") == "inner"
    # Añade un fichero nuevo en la copia.
    fs2.root.children["otro.txt"] = FileNode(name="otro.txt", content="x")
    assert "otro.txt" not in fs.root.children


def test_snapshot_es_independiente() -> None:
    """snapshot() devuelve un FS independiente del original."""
    fs = _build_fs()
    copia = fs.snapshot()
    copia.root.children["home"].children["file.txt"].content = "modificado"
    assert fs.read_file("/home/file.txt") == "hi"
    assert fs.to_dict() != copia.to_dict()


def test_snapshot_igual_a_original_al_inicio() -> None:
    """snapshot() replica el estado completo del FS en el momento de copiar."""
    fs = _build_fs()
    assert fs.snapshot().to_dict() == fs.to_dict()


# ---- FsError como dato estructurado ---------------------------------


def test_fs_error_expone_kind_y_path() -> None:
    """Los errores son datos (kind + path), no jerarquía de clases."""
    err = FsError("not_found", "/tmp/x")
    assert err.kind == "not_found"
    assert err.path == "/tmp/x"
    assert "not_found" in str(err)
    assert "not_found: /tmp/x" == str(err)