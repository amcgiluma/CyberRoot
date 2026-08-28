"""Resolubilidad: la sala generada SIEMPRE deja resolver el encargo.

Barrido N=50 en practice + N=10 en canonical (~60 sesiones de 5 comandos,
<2 s). Para cada sala: (a) generate no lanza; (b) la secuencia canónica corre
con exit 0; (c) la copia queda en el USB con el prefijo CANDELAS; (d) el
ruido total de la sesión canónica ≤ noise_budget.
"""

from __future__ import annotations

from core.generator import generate
from core.generator.chapter0 import USB_DIR
from core.sandbox.fs import FileNode
from core.sandbox.shell import Shell

PRACTICE_SEEDS = list(range(50))
CANONICAL_SEEDS = list(range(10))


def _session_noise_y_copia(inc) -> tuple[int, str]:
    """Corre la solución canónica sobre una COPIA; devuelve (noise, contenido)."""
    shell = Shell(inc.room.fs.snapshot(), host=inc.room.host)
    for step in inc.room.canon.steps:
        res = shell.execute(" ".join(step.argv))
        assert res.exit_code == step.expect_exit, (step.argv, res.stderr)
    # La copia debe existir como fichero (el cp escribió en el FS de la sesión).
    node = shell.fs.resolve(f"{USB_DIR}/{inc.room.objective.file}", "/")
    assert isinstance(node, FileNode), f"{USB_DIR}/{inc.room.objective.file}"
    return shell.total_noise, node.content


def test_practice_resoluble_barrido_50() -> None:
    for seed in PRACTICE_SEEDS:
        inc = generate(seed, 0, variant="practice")
        noise, content = _session_noise_y_copia(inc)
        assert content.startswith("CANDELAS"), f"seed={seed}: copia sin dossier"
        assert noise <= inc.room.noise_budget, f"seed={seed}: noise {noise} > cota"


def test_canonical_resoluble_barrido_10() -> None:
    for seed in CANONICAL_SEEDS:
        inc = generate(seed, 0, variant="canonical")
        noise, content = _session_noise_y_copia(inc)
        assert content.startswith("CANDELAS"), f"seed={seed}"
        assert noise <= inc.room.noise_budget, f"seed={seed}: noise {noise} > cota"