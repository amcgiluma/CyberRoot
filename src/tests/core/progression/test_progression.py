"""T2 — progression v0: el primer unlock por competencia respira sobre el save.

AC de Gwyndolin (plan 29/08): completar la run canónica del cap. 0 marca
`c.cp` como dominado y persiste en el save (load lo recupera); roundtrip
exacto. Carpeta NUEVA sin `__init__.py` (regla O1): la piel del cap. 0 se
construye aquí SIN importar de `src/tests/core/sandbox/`.
"""

from __future__ import annotations

from core.progression import (
    CAP0_CONTRACT_BOON,
    LOGRO_CERO_RASTRO,
    LOGRO_MANO_SEDA,
    evaluate_logros,
    evaluate_unlocks,
    resumen_competencia,
)
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


# --------------------------------------------------------------------------
# 8-12 · T1 (30/08): MOMENTO del dominio + resumen de competencia
# --------------------------------------------------------------------------

def test_evaluate_unlocks_records_moment() -> None:
    """`evaluate_unlocks` guarda CUÁNDO se dominó (tick + order en `mastered`)."""
    st = GameState(shell=_cap0_completed_shell())
    evaluate_unlocks(st)
    # Canónica: cat (tick 1) + cp (tick 2) → el dominio se detecta en el tick 2.
    assert st.mastered[CAP0_CONTRACT_BOON] == {"tick": 2, "order": 1}


def test_mastered_roundtrip_exact() -> None:
    """El campo `mastered` sobrevive a `to_dict`/`from_dict` idéntico."""
    st = GameState(shell=_cap0_completed_shell())
    evaluate_unlocks(st)
    rebuilt = GameState.from_dict(st.to_dict())
    assert rebuilt.mastered == st.mastered
    assert rebuilt.to_dict() == st.to_dict()


def test_mastered_defaults_empty_in_old_v1_save() -> None:
    """Un save v1 previo (sin la clave `mastered`) carga con `{}` (backward-compat)."""
    d = {"version": 1, "shell": _cap0_completed_shell().to_dict()}
    st = GameState.from_dict(d)
    assert st.mastered == {}


def test_resumen_competencia_canonical() -> None:
    """Resumen: `c.cp` dominado con su momento + factura GNU de la sesión (ruido 4)."""
    st = GameState(shell=_cap0_completed_shell())
    evaluate_unlocks(st)
    res = resumen_competencia(st)
    assert res["dominados"] == [{"concepto": CAP0_CONTRACT_BOON, "tick": 2, "order": 1}]
    factura = res["factura"]
    assert factura["por_comando"] == {
        "cat": {"usos": 1, "ruido": 1, "errores": 0},
        "cp": {"usos": 1, "ruido": 3, "errores": 0},
    }
    assert factura["total_usos"] == 2
    assert factura["total_ruido"] == 4
    assert factura["total_errores"] == 0


def test_resumen_competencia_legacy_moment_none() -> None:
    """Un boon ya dominado en un save previo a la meta muestra momento None."""
    st = GameState(shell=_cap0_completed_shell())
    st.knowledge[CAP0_CONTRACT_BOON] = True  # legado: dominado pero sin meta
    res = resumen_competencia(st)
    assert res["dominados"] == [{"concepto": CAP0_CONTRACT_BOON, "tick": None, "order": None}]


# --------------------------------------------------------------------------
# 13-17 · T2 (30/08): logros por factura de ruido
# --------------------------------------------------------------------------

def test_evaluate_logros_canonic_run_earns_both() -> None:
    """La run canónica (cat 1 + cp 3 = ruido 4, sin errores) gana los 2 logros."""
    st = GameState(shell=_cap0_completed_shell())
    assert evaluate_logros(st) == [LOGRO_CERO_RASTRO, LOGRO_MANO_SEDA]
    assert st.logros[LOGRO_CERO_RASTRO] is True
    assert st.logros[LOGRO_MANO_SEDA] is True


def test_evaluate_logros_idempotent() -> None:
    """Segunda llamada: nada nuevo (los logros ya persisten en `state.logros`)."""
    st = GameState(shell=_cap0_completed_shell())
    evaluate_logros(st)
    assert evaluate_logros(st) == []
    assert st.logros[LOGRO_CERO_RASTRO] is True


def test_extra_noise_kills_cero_rastro() -> None:
    """Un `ls` extra (ruido 5 > umbral 4) mata «Cero rastro» pero no «Mano de seda»."""
    shell = _cap0_completed_shell()
    assert shell.execute("ls /srv").exit_code == 0
    st = GameState(shell=shell)
    assert st.shell.total_noise == 5
    assert evaluate_logros(st) == [LOGRO_MANO_SEDA]
    assert LOGRO_CERO_RASTRO not in st.logros


def test_error_kills_mano_seda() -> None:
    """Un exit != 0 (comando desconocido, exit 127) mata «Mano de seda» no «Cero rastro»."""
    shell = _cap0_completed_shell()
    shell.execute("comando_fantasma")
    st = GameState(shell=shell)
    assert evaluate_logros(st) == [LOGRO_CERO_RASTRO]
    assert LOGRO_MANO_SEDA not in st.logros


def test_logros_persist_in_save(tmp_path) -> None:
    """Los logros ganados sobreviven a save/load (load los recupera)."""
    st = GameState(shell=_cap0_completed_shell())
    evaluate_logros(st)
    p = tmp_path / "save.json"
    save(st, p)
    loaded = load(p)
    assert loaded.logros[LOGRO_CERO_RASTRO] is True
    assert loaded.logros[LOGRO_MANO_SEDA] is True