"""Contrato de historia: el encargo del cap. 1 al que esta sala apunta."""

from __future__ import annotations

from core.generator import generate
from core.generator.chapter0 import OFFICE_DIR, PROVIDER_FILE


def test_contrato_apunta_al_encargo_azul_e1_cap1() -> None:
    inc = generate(7)
    assert inc.contract.objective_key == "story.ch1.e1"
    assert inc.contract.brief_text_key == "story.ch1.e1.brief"
    assert inc.contract.karma_hint == "azul"


def test_objetivo_cap0_ventana_dossier() -> None:
    inc = generate(7)
    obj = inc.room.objective
    assert obj.story_key == "story.ch0.ventana"
    assert obj.summary_text_key == "story.ch0.dossier"
    assert obj.file == "nombre_de_proveedor.txt"
    assert obj.src == f"{OFFICE_DIR}/{PROVIDER_FILE}"
    assert obj.dst_dir == "/usb"