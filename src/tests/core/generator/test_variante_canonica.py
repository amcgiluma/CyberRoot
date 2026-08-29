"""Variante canónica: la piel EXACTA del capítulo, byte a byte.

Espeja `test_session_cap0.py`: la secuencia canónica sobre el FS de la sala
produce EXACTAMENTE la salida de la escena, el USB NO se lista desde /srv
(cuelga de la raíz) y el FS de la sala canónica es IDÉNTICO al del test
(no hay decoys; ningún fichero de más ni de menos).
"""

from __future__ import annotations

from core.common.rng import Rng
from core.generator import generate
from core.generator.chapter0 import (
    DOSSIER_CONTENT,
    OFFICE_DIR,
    PROVIDER_FILE,
    build_chapter0_fs,
)
from core.sandbox.shell import Shell

SEED = 42


def _run_canon(shell: Shell, inc) -> list[str]:
    """Ejecuta la solución canónica; devuelve los stdout en orden."""
    outs = []
    for step in inc.room.canon.steps:
        res = shell.execute(" ".join(step.argv))
        assert res.exit_code == step.expect_exit, (step.argv, res.stderr)
        outs.append(res.stdout)
    return outs


def test_variante_canonica_piel_exacta() -> None:
    inc = generate(SEED, 0, variant="canonical")
    shell = Shell(inc.room.fs.snapshot(), host=inc.room.host)
    outs = _run_canon(shell, inc)

    # [ls] del office → golden (README < log.txt < nombre_de_proveedor.txt).
    assert outs[0] == f"README\nlog.txt\n{PROVIDER_FILE}\n"
    # [cat] del dossier → línea CANDELAS EXACTA.
    assert outs[1] == DOSSIER_CONTENT
    # El USB cuelga de la raíz: tras cd /srv, `ls` NO lo lista.
    assert outs[-1] == "oficina-vecinal-muelle-norte\n"
    assert shell.cwd == "/srv"


def test_variante_canonica_cwd_final() -> None:
    inc = generate(SEED, 0, variant="canonical")
    shell = Shell(inc.room.fs.snapshot(), host=inc.room.host)
    for step in inc.room.canon.steps:
        shell.execute(" ".join(step.argv))
    assert shell.cwd == "/srv"


def test_variante_canonica_sin_decoys() -> None:
    inc = generate(SEED, 0, variant="canonical")
    assert inc.room.decoys == ()
    # El concept_pool viene del curriculum.json (ids), ya no de constantes.
    assert inc.room.concept_pool == ("c.cat", "c.cd", "c.cp", "c.ls")


def test_variante_canonica_fs_identico_al_test() -> None:
    """El FS de la sala canónica es EXACTAMENTE el del test (nada más)."""
    inc = generate(SEED, 0, variant="canonical")
    canónico = build_chapter0_fs(Rng(0))  # fs_rng se ignora en v0
    assert inc.room.fs.to_dict() == canónico.to_dict()
    # Sanidad: los nombres base esperados están presentes, nada extra.
    office = inc.room.fs.get_dir(OFFICE_DIR, "/")
    assert sorted(office.children) == ["README", "log.txt", PROVIDER_FILE]