"""Smoke test del paquete sandbox (H0): importa y expone la versión.

Zona de Smough. El smoke general del repo vive en src/tests/smoke/ (Ornstein);
este vive aquí para no colisionar con su rama.
"""

from __future__ import annotations

import core.sandbox as sandbox


def test_paquete_sandbox_importable() -> None:
    assert sandbox.__doc__
    assert sandbox.__version__ == "0.1.0"
