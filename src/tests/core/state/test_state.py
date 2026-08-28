"""T1 `state` v0 — batería de 10 tests de GameState y save/load versionado.

Cubre (PLAN §5): roundtrips in-memory y vía disco, atomicidad del save
(original intacto ante fallo de serialización, `.tmp` residual tolerado),
JSON escrito a mano (§1.5), migraciones white-box v0→v1, rechazo de versiones
desconocidas/ilegibles, y la sesión canónica del cap. 0 con extracción `cp`.

Carpeta NUEVA sin `__init__.py` (regla O1 del repo): los paquetes padre de
`src/tests` ya tienen el suyo; aquí la piel de FS se construye en local SIN
importar de `src/tests/core/sandbox/`.
"""

from __future__ import annotations

import json

import pytest

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell
from core.state.state import (
    GameState,
    SaveIntegrityError,
    SaveVersionError,
    _MIGRATIONS,
    save,
    load,
)

OFICINA = "/srv/oficina-vecinal-muelle-norte"
PROVEEDOR = "nombre_de_proveedor.txt"


# --------------------------------------------------------------------------
# piel del cap. 0 (construida aquí mismo, regla O1)
# --------------------------------------------------------------------------

def _fs_oficina() -> FileSystem:
    """FS del tutorial: la oficina en /srv y el USB colgado de la raíz."""
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "oficina-vecinal-muelle-norte": DirNode(
                            name="oficina-vecinal-muelle-norte",
                            children={
                                PROVEEDOR: FileNode(
                                    name=PROVEEDOR,
                                    content=(
                                        "CANDELAS  ·  proveedor nº 47  ·  "
                                        "facturación externa  ·  114 facturas/mes\n"
                                    ),
                                    owner="recepcion",
                                    group="empleados",
                                    mtime=1044,  # 11:04, tiempo simulado
                                ),
                                "log.txt": FileNode(
                                    name="log.txt",
                                    content="08:59 turno de mañana\n11:04 SIN REGISTRO\n",
                                    mtime=1030,
                                ),
                                "README": FileNode(
                                    name="README",
                                    content="Sistema de gestion de la oficina vecinal.\n",
                                    mtime=900,
                                ),
                            },
                        )
                    },
                ),
                "usb": DirNode(name="usb", children={}),
            },
        )
    )


def _cap0_shell() -> Shell:
    """Shell del tutorial ya corrido: leer dossier (cat) + extraer (cp).

    cat=1 + cp=3 → total_noise == 4 (mismo perfil que test_gancho_cp del cap. 0).
    """
    shell = Shell(
        _fs_oficina(), host="oficina-vecinal-muelle-norte", commands=("cp", "cat", "ls")
    )
    res = shell.execute(f"cat {OFICINA}/{PROVEEDOR}")
    assert res.exit_code == 0, res.stderr
    res = shell.execute(f"cp {OFICINA}/{PROVEEDOR} /usb/")
    assert res.exit_code == 0, res.stderr
    assert shell.total_noise == 4  # cp(3) + cat(1)
    return shell


def _empty_shell() -> Shell:
    """Shell mínimo sin historial (para tests de formato/serialización)."""
    return Shell(FileSystem(root=DirNode(name="/")))


# --------------------------------------------------------------------------
# 1–3 · roundtrips in-memory
# --------------------------------------------------------------------------

def test_roundtrip_inmemory() -> None:
    """from_dict(to_dict) reproduce el dict exacto sobre una sesión usada."""
    g = GameState(shell=_cap0_shell())
    assert GameState.from_dict(g.to_dict()).to_dict() == g.to_dict()


def test_roundtrip_copy_is_independent() -> None:
    """Ejecutar en la copia no muta el original (history/tick/total_noise)."""
    shell = _empty_shell()
    shell.execute("cd /srv")  # muta history y tick (ruido 0)
    g = GameState(shell=shell)
    original = g.to_dict()

    copy = GameState.from_dict(original)
    copy.shell.execute("cd /oficina-vecinal-muelle-norte")
    copy.shell.execute("ls /srv")

    assert copy.to_dict()["shell"]["tick"] == original["shell"]["tick"] + 2
    assert len(copy.to_dict()["shell"]["history"]) == len(
        original["shell"]["history"]
    ) + 2
    # El original queda EXACTAMENTE como estaba:
    assert g.to_dict() == original


def test_json_roundtrip() -> None:
    """to_dict → json.dumps/loads → from_dict → to_dict idéntico."""
    g = GameState(shell=_cap0_shell())
    blob = json.dumps(g.to_dict(), ensure_ascii=False, sort_keys=True)
    rebuilt = GameState.from_dict(json.loads(blob))
    assert rebuilt.to_dict() == g.to_dict()


# --------------------------------------------------------------------------
# 4–6 · save/load a disco y atomicidad
# --------------------------------------------------------------------------

def test_save_load_disk_roundtrip(tmp_path) -> None:
    """save→load idéntico y sin `.tmp` residual tras el guardado."""
    g = GameState(shell=_cap0_shell())
    p = tmp_path / "save.json"
    save(g, p)
    g2 = load(p)
    assert g2.to_dict() == g.to_dict()
    assert g2.version == 1
    assert list(tmp_path.glob("*.tmp")) == []


def test_load_handwritten_json(tmp_path) -> None:
    """§1.5: un save volcado a mano (json.dump directo) carga idéntico."""
    g = GameState(shell=_cap0_shell())
    p = tmp_path / "mano.json"
    p.write_text(
        json.dumps(g.to_dict(), ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    assert load(p).to_dict() == g.to_dict()


def test_save_failure_leaves_original_intact(tmp_path) -> None:
    """Un estado no serializable (set() en history) falla y NO toca el save previo."""
    shell = _cap0_shell()
    g = GameState(shell=shell)
    p = tmp_path / "save.json"
    save(g, p)                      # save válido PRIMERO
    original = g.to_dict()

    malo = GameState(shell=shell)
    malo.shell.history.append({"line": "x", "result": {"set": set()}})
    with pytest.raises(SaveIntegrityError):
        save(malo, p)

    # El contenido ORIGINAL de p queda intacto (el replace nunca llegó):
    assert load(p).to_dict() == original


# --------------------------------------------------------------------------
# 7–8 · versionado y migraciones
# --------------------------------------------------------------------------

def test_migration_v0_to_v1() -> None:
    """White-box: migración sintética v0→v1 reconstruye un save sin `version`."""
    snapshot = dict(_MIGRATIONS)
    try:
        _MIGRATIONS.clear()
        _MIGRATIONS[0] = lambda d: {**d, "version": 1}
        shell_dict = _cap0_shell().to_dict()
        g = GameState.from_dict({"shell": shell_dict})  # SIN clave "version"
        assert g.version == 1
        assert g.shell.to_dict() == shell_dict
    finally:
        _MIGRATIONS.clear()
        _MIGRATIONS.update(snapshot)


def test_unknown_version_rejected() -> None:
    """Versión desconocida o ilegible → SaveVersionError (número en el mensaje)."""
    shell_dict = _empty_shell().to_dict()
    with pytest.raises(SaveVersionError) as ei:
        GameState.from_dict({"version": 999999, "shell": shell_dict})
    assert "999999" in str(ei.value)
    with pytest.raises(SaveVersionError):
        GameState.from_dict({"version": "no-es-int", "shell": shell_dict})


# --------------------------------------------------------------------------
# 9 · estabilidad de doble ida y vuelta
# --------------------------------------------------------------------------

def test_double_roundtrip_stability(tmp_path) -> None:
    """save→load→save→load reproduce el dict original (n=2 estable)."""
    g = GameState(shell=_cap0_shell())
    p1 = tmp_path / "a.json"
    p2 = tmp_path / "b.json"
    save(g, p1)
    g2 = load(p1)
    assert g2.version == 1
    save(g2, p2)
    assert load(p2).to_dict() == g.to_dict()


# --------------------------------------------------------------------------
# 10 · sesión canónica del cap. 0: roundtrip completo in-memory + disco
# --------------------------------------------------------------------------

def test_session_cap0_roundtrip(tmp_path) -> None:
    """La extracción del cap. 0 sobrevive entera (memory y disco); ruido 4."""
    g = GameState(shell=_cap0_shell())

    # La copia quedó en /usb y el original intacto en la oficina:
    assert g.shell.fs.read_file("/usb/" + PROVEEDOR).startswith("CANDELAS")
    assert g.shell.fs.read_file(f"{OFICINA}/{PROVEEDOR}").startswith("CANDELAS")

    # Roundtrip in-memory:
    rebuilt = GameState.from_dict(g.to_dict())
    assert rebuilt.to_dict() == g.to_dict()
    assert rebuilt.shell.fs.read_file("/usb/" + PROVEEDOR).startswith("CANDELAS")
    assert rebuilt.shell.fs.read_file(f"{OFICINA}/{PROVEEDOR}").startswith("CANDELAS")
    assert rebuilt.shell.total_noise == 4

    # Roundtrip vía disco:
    p = tmp_path / "cap0.json"
    save(g, p)
    disk = load(p)
    assert disk.to_dict() == g.to_dict()
    assert disk.version == 1
    assert disk.shell.fs.read_file("/usb/" + PROVEEDOR).startswith("CANDELAS")
    assert disk.shell.fs.read_file(f"{OFICINA}/{PROVEEDOR}").startswith("CANDELAS")
    assert not disk.shell.fs.resolve(f"{OFICINA}/{PROVEEDOR}") is disk.shell.fs.resolve(
        "/usb/" + PROVEEDOR
    )
    assert len(disk.shell.history) == 2
    assert disk.shell.total_noise == 4