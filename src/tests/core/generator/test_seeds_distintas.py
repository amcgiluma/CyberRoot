"""Semillas distintas ⇒ salas distintas; ambas resolubles tras roundtrip."""

from __future__ import annotations

from core.generator import generate, validate_incursion
from core.generator.model import Incursion


def test_seeds_distintas_producen_salas_distintas() -> None:
    """generate(1) vs generate(2) en practice → to_dict DIFERENTES."""
    a = generate(1, 0, variant="practice")
    b = generate(2, 0, variant="practice")
    assert a.to_dict() != b.to_dict()
    # Al menos el room_id difiere (id derivado de la seed vía fork).
    assert a.room.id != b.room.id


def test_ambas_reconstruidas_siguen_resolubles() -> None:
    """Tras from_dict, ambas pasan validate_incursion de nuevo."""
    for seed in (1, 2):
        inc = generate(seed, 0, variant="practice")
        reconstruida = Incursion.from_dict(inc.to_dict())
        validate_incursion(reconstruida)  # no lanza
        assert reconstruida.to_dict() == inc.to_dict()