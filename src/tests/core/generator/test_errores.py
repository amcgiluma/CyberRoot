"""Errores de validación del generador y `UnsolvableRoomError` (§6.4.4)."""

from __future__ import annotations

import pytest

from core.generator import (
    generate,
    validate_incursion,
    UnsolvableRoomError,
)
from core.generator.chapter0 import OFFICE_DIR
from core.generator.model import Incursion


def test_chapter_distinto_de_cero_value_error() -> None:
    with pytest.raises(ValueError) as e:
        generate(1, chapter=1)
    assert "curriculum.json" in str(e.value)
    with pytest.raises(ValueError):
        generate(1, chapter=3)


def test_seed_bool_type_error() -> None:
    with pytest.raises(TypeError):
        generate(True)  # bool NO es seed válida (coherente con Rng)


def test_variant_desconocida_value_error() -> None:
    with pytest.raises(ValueError) as e:
        generate(1, variant="noexiste")
    assert "canonical|practice" in str(e.value)


def test_sala_rota_por_fs_levanta_unsolvable() -> None:
    """Un Incursion a mano a la que le quitamos el dossier del FS es IRRESOLUBLE."""
    inc = generate(42)
    d = inc.to_dict()

    # Rompemos el FS: eliminamos el fichero del proveedor de la oficina.
    office = d["room"]["fs"]["root"]["children"]["srv"]["children"][
        "oficina-vecinal-muelle-norte"
    ]
    del office["children"]["nombre_de_proveedor.txt"]

    rota = Incursion.from_dict(d)
    with pytest.raises(UnsolvableRoomError) as e:
        validate_incursion(rota)
    # El mensaje guarda el step que falló (argv + exit_code + stderr).
    assert e.value.argv is not None
    assert e.value.stderr != ""


def test_unsolvable_cuando_no_queda_copia_en_usb() -> None:
    """Si el cp no deja la copia, la sala es irresoluble aunque los pasos
    salga con exit 0 (p.ej. destino roto)."""
    inc = generate(42)
    d = inc.to_dict()

    # Rompemos la secuencia canónica: cambiamos el cp para que copie a un
    # directorio inexistente → exit != 0 en validación.
    steps = d["room"]["canon"]["steps"]
    for s in steps:
        if s["argv"][0] == "cp":
            s["argv"] = ["cp", f"{OFFICE_DIR}/nombre_de_proveedor.txt", "/no_existe/"]
            s["expect_exit"] = 1  # seguimos exigiendo el nuevo fallo (se rompe la sala)
            break

    rota = Incursion.from_dict(d)
    with pytest.raises(UnsolvableRoomError):
        validate_incursion(rota)