"""core.progression — metaprogresión: el Espejo de Gris (ARCHITECTURE §2.7).

v0 (T2, 29/08): desbloqueos POR COMPETENCIA con UNA regla — completar el
contrato del cap. 0 marca `c.cp` como dominado y el estado persiste en el
save. T1/T2 (30/08): el unlock guarda el MOMENTO del dominio (`mastered`:
tick/order) + `resumen_competencia(state)` (lista de dominados + factura del
capítulo) y el MECANISMO de logros por factura (`evaluate_logros`: "Cero
rastro", "Mano de seda"). Regla dura §4.2: el espejo acelera/personaliza,
jamás sustituye saber. Sin RNG, sin reloj real, sin pyxel, stdlib only. Ver
PLAN.md (decisiones e hitos). Dueño: Seath (`feat/meta-ui`).
"""

from core.progression.progression import (
    CAP0_CONTRACT_BOON,
    LOGRO_CERO_RASTRO,
    LOGRO_MANO_SEDA,
    UMBRAL_CERO_RASTRO,
    UNLOCK_EVENT_TYPE,
    evaluate_logros,
    evaluate_unlocks,
    resumen_competencia,
)

__version__ = "0.3.0"

__all__ = [
    "CAP0_CONTRACT_BOON",
    "LOGRO_CERO_RASTRO",
    "LOGRO_MANO_SEDA",
    "UMBRAL_CERO_RASTRO",
    "UNLOCK_EVENT_TYPE",
    "evaluate_logros",
    "evaluate_unlocks",
    "resumen_competencia",
]