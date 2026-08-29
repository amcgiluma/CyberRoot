"""🧭8 (Oscar, 29/08): la costura del contrato del cap. 0 queda DOCUMENTADA.

El `contract.objective_key` del cap. 0 apunta a `story.ch1.e1` (el encargo AZUL
que esta sala inicia), pero ESA quest requiere `c.ls-la` y `c.permisos-leer`,
conceptos que el cap. 0 NO enseña (su pool es solo `c.ls/cd/cat/cp`). Según el
plan 29/08, HOY NO la resolvemos: la dejamos cubierta con este test xfail y
**Gwyn decide esta noche** entre:
  (a) la sala del cap. 0 contrata `story.ch0.ventana` (ya lo hace en el
      `objective`), o
  (b) los prereqs de un encargo se evalúan al ABRIRLO, no al generar la sala
      (la sala es escenario; el contrato es compromiso del jugador).

El test aserta la INVARIANTE DESEADA — que el encargo del contrato sea
resoluble con el pool del cap. 0 — que HOY se incumple: por eso es xfail.
Cuando Gwyn materialice (a) o (b), la invariante se cumple, el test pasa de
verdad y se le quita el marcador xfail.
"""
from __future__ import annotations

import pytest

from core.curriculum import load_curriculum
from core.generator import generate


@pytest.mark.xfail(
    reason=(
        "🧭8 costura: contract.objective_key=story.ch1.e1 pide c.ls-la y "
        "c.permisos-leer, que el cap. 0 no enseña (pool c.ls/cd/cat/cp). "
        "Gwyn decide (a) contratar story.ch0.ventana o (b) evaluar prereqs "
        "al abrir el encargo. Deja de ser xfail al materializarlo."
    ),
    strict=False,
)
def test_el_encargo_del_contrato_es_resoluble_en_el_pool_del_cap0() -> None:
    """xfail: el encargo del contrato del cap. 0 NO es resoluble hoy.

    Invariante deseada §6.4.1: el `objective_key` del contrato apunta a una
    quest cuyo `requires` está cubierto por el pool del cap. 0. Hoy no se
    cumple (story.ch1.e1 exige c.ls-la/c.permisos-leer ∉ pool) → xfail.
    """
    inc = generate(7, 0)
    cur = load_curriculum()
    quest = cur.quest(inc.contract.objective_key)
    assert quest is not None, f"{inc.contract.objective_key} debiera existir en el JSON"
    pool = frozenset(inc.room.concept_pool)
    # Queremos que el encargo del contrato sea resoluble con lo que enseña la
    # sala. Hoy es FALSO (fallará → xfail): la costura está abierta.
    assert frozenset(quest.requires) <= pool