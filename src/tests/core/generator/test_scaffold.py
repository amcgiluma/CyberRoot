"""Andamiaje de la run 0: expuesto como DATOS, decisión DE Gwyn (🧭2)."""

from __future__ import annotations

from core.generator import generate


def test_options_exactamente_las_tres() -> None:
    inc = generate(7)
    opts = inc.scaffold.options
    assert set(opts) == {"option_a", "option_b", "option_c"}


def test_cada_opcion_tiene_initial_cwd() -> None:
    inc = generate(7)
    for name in ("option_a", "option_b", "option_c"):
        assert "initial_cwd" in inc.scaffold.options[name], name


def test_default_es_option_b() -> None:
    inc = generate(7)
    assert inc.scaffold.default == "option_b"


def test_note_menciona_la_decision_pendiente_de_gwyn() -> None:
    inc = generate(7)
    note = inc.scaffold.note
    assert note.strip() != ""
    assert "Gwyn" in note
    assert "🧭" in note