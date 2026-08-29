"""T2 — progression v0: el primer unlock por competencia respira sobre el save.

AC de Gwyndolin (plan 29/08): completar la run canónica del cap. 0 marca
`c.cp` como dominado y persiste en el save (load lo recupera); roundtrip
exacto. Carpeta NUEVA sin `__init__.py` (regla O1): la piel del cap. 0 se
construye aquí SIN importar de `src/tests/core/sandbox/`.
"""

from __future__ import annotations

from core.progression import CAP0_CONTRACT_BOON, evaluate_unlocks
from core.sandbox import Shell
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.state import GameState
from core.state.state import load, save

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
                                    content=("CANDELAS  ·  proveedor nº 47  ·  "
                                             "facturación externa\n"),
                                    owner="recepcion",
                                    group="empleados",
                                    mtime=1044,
                                ),
                            },
                        )
                    },
                ),
                "usb": DirNode(name="usb", children={}),
            },
        )
    )


def _cap0_completed_shell() -> Shell:
    """Canónica: leer dossier (cat) + extraer (cp a /usb) → contrato cumplido."""
    shell = Shell(_fs_oficina(), host="oficina-vecinal-muelle-norte",
                  commands=("cp", "cat", "ls"))
    assert shell.execute(f"cat {OFICINA}/{PROVEEDOR}").exit_code == 0
    res = shell.execute(f"cp {OFICINA}/{PROVEEDOR} /usb/")
    assert res.exit_code == 0, res.stderr
    return shell


def _cap0_partial_shell() -> Shell:
    """Solo leyó el dossier (cat), NO extrajo: contrato sin completar."""
    shell = Shell(_fs_oficina(), host="oficina-vecinal-muelle-norte",
                  commands=("cp", "cat", "ls"))
    assert shell.execute(f"cat {OFICINA}/{PROVEEDOR}").exit_code == 0
    return shell


# --------------------------------------------------------------------------
# 1-4 · la regla: qué desbloquea y qué no
# --------------------------------------------------------------------------

def test_cap0_completion_marks_cp_dominated() -> None:
    st = GameState(shell=_cap0_completed_shell())
    newly = evaluate_unlocks(st)
    assert newly == [CAP0_CONTRACT_BOON]
    assert st.knowledge[CAP0_CONTRACT_BOON] is True


def test_evaluate_unlocks_is_idempotent() -> None:
    st = GameState(shell=_cap0_completed_shell())
    evaluate_unlocks(st)
    assert evaluate_unlocks(st) == []  # ya dominado: nada nuevo
    assert st.knowledge[CAP0_CONTRACT_BOON] is True


def test_partial_session_does_not_unlock() -> None:
    st = GameState(shell=_cap0_partial_shell())
    assert evaluate_unlocks(st) == []
    assert CAP0_CONTRACT_BOON not in st.knowledge


def test_empty_shell_no_unlock() -> None:
    st = GameState(shell=Shell(FileSystem(root=DirNode(name="/"))))
    assert evaluate_unlocks(st) == []
    assert st.knowledge == {}


# --------------------------------------------------------------------------
# 5-7 · persistencia y roundtrip
# --------------------------------------------------------------------------

def test_unlock_persists_in_save(tmp_path) -> None:
    st = GameState(shell=_cap0_completed_shell())
    evaluate_unlocks(st)
    p = tmp_path / "save.json"
    save(st, p)
    loaded = load(p)
    assert loaded.knowledge[CAP0_CONTRACT_BOON] is True


def test_knowledge_roundtrip_exact() -> None:
    st = GameState(shell=_cap0_completed_shell())
    evaluate_unlocks(st)
    rebuilt = GameState.from_dict(st.to_dict())
    assert rebuilt.to_dict() == st.to_dict()
    assert rebuilt.knowledge == {CAP0_CONTRACT_BOON: True}


def test_knowledge_defaults_empty_in_old_v1_save() -> None:
    """Un save v1 previo (sin la clave `knowledge`) carga con el inventario vacío."""
    d = {"version": 1, "shell": _cap0_completed_shell().to_dict()}
    st = GameState.from_dict(d)
    assert st.knowledge == {}