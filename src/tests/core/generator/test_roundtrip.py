"""Roundtrip de la Incursion: to_dict es JSON-plano estricto e ida-y-vuelta
exacta con `Incursion.from_dict`, y la reconstruida sigue resolviendo."""

from __future__ import annotations

import json

from core.common.types import ensure_plain
from core.generator import generate, validate_incursion
from core.generator.model import Incursion

SEEDS = (0, 1, 7, 42, 99, 1234567)


def test_to_dict_es_json_plano_estricto() -> None:
    for seed in SEEDS:
        ensure_plain(generate(seed).to_dict())          # canonical
        ensure_plain(generate(seed, variant="practice").to_dict())


def test_roundtrip_dict_y_json_identico() -> None:
    for seed in SEEDS:
        inc = generate(seed, variant="practice")
        original = inc.to_dict()
        # json.dumps → loads atraviesa la frontera con lists (tuples ya listas).
        via_json = json.loads(json.dumps(original))
        reconstruida = Incursion.from_dict(via_json)
        assert reconstruida.to_dict() == original


def test_roundtrip_de_la_fs_viaja_bien() -> None:
    for seed in SEEDS:
        inc = generate(seed, variant="practice")
        reconstruida = Incursion.from_dict(inc.to_dict())
        # El FS viaja: idéntico a dict plano tras el roundtrip.
        assert reconstruida.room.fs.to_dict() == inc.room.fs.to_dict()


def test_validate_de_la_reconstruida_pasa() -> None:
    """La Incursion reconstruida sigue resolviendo (validate no lanza)."""
    for seed in SEEDS:
        for variant in ("canonical", "practice"):
            inc = generate(seed, variant=variant)
            reconstruida = Incursion.from_dict(inc.to_dict())
            validate_incursion(reconstruida)