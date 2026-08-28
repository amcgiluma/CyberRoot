"""Determinismo DURO del generador: misma seed ⇒ misma Incursion, incluso
entre procesos con PYTHONHASHSEED distinto (criterio de aceptación B).

Modelo: `test_session_cap0::test_reproducibilidad_entre_procesos_...`.
"""

from __future__ import annotations

import os
import subprocess
import sys

from core.generator import generate, validate_incursion
from core.generator.chapter0 import OFFICE_DIR
from core.generator.model import Incursion
from core.sandbox.shell import Shell


def test_misma_seed_misma_sala_canonical() -> None:
    """generate(42) dos veces → Incursion idéntica a dict plano profundo."""
    a = generate(42).to_dict()
    b = generate(42).to_dict()
    assert a == b


def test_misma_seed_misma_sala_practice() -> None:
    """Igual para la variante practice (decoys y mtimes también deterministas)."""
    a = generate(42, variant="practice").to_dict()
    b = generate(42, variant="practice").to_dict()
    assert a == b
    # Y siguen resolubles tras electronía de seed (sanidad).
    validate_incursion(generate(42, variant="practice"))


def test_roundtrip_del_mismo_gen_no_rompe_determinismo() -> None:
    """Roundtrip dict del mismo gen es idéntico (frontera JSON-plana)."""
    inc = generate(99, variant="practice")
    inc2 = Incursion.from_dict(inc.to_dict())
    assert inc2.to_dict() == inc.to_dict()


_SNIPPET = """
import sys
sys.path.insert(0, "src")
from core.generator import generate
from core.generator.chapter0 import OFFICE_DIR
from core.sandbox.shell import Shell

inc = generate(7, 0, variant="practice")
office = inc.room.fs.get_dir(OFFICE_DIR, "/")
files = sorted(office.children)
s = Shell(inc.room.fs.snapshot(), host=inc.room.host)
noise = 0
for st in inc.room.canon.steps:
    r = s.execute(" ".join(st.argv))
    assert r.exit_code == 0, r.stderr
noise = s.total_noise
print(repr({"room_id": inc.room.id, "office_files": files,
            "canon_noise": noise, "seed": repr(inc.seed)}))
"""


def test_cross_proceso_pythonhashseed_distinto() -> None:
    """Dos procesos con PYTHONHASHSEED 1 vs 999999 → salida byte a byte igual."""
    envs = [
        {**os.environ, "PYTHONHASHSEED": "1"},
        {**os.environ, "PYTHONHASHSEED": "999999"},
    ]
    outputs = []
    for env in envs:
        proc = subprocess.run(
            [sys.executable, "-c", _SNIPPET],
            capture_output=True,
            text=True,
            env=env,
            timeout=60,
            check=True,
        )
        outputs.append(proc.stdout)
    assert outputs[0] == outputs[1]
    # No es un empate vacío: el resumen existe y tiene forma esperada.
    assert "room-ch0-" in outputs[0]
    assert "'canon_noise': 6" in outputs[0]