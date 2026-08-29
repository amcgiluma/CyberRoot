"""core.progression — metaprogresión: el Espejo de Gris (ARCHITECTURE §2.7).

v0 (T2, 29/08): desbloqueos POR COMPETENCIA con UNA regla — completar el
contrato del cap. 0 marca `c.cp` como dominado y el estado persiste en el
save. Regla dura §4.2: el espejo acelera/personaliza, jamás sustituye saber.
Sin RNG, sin reloj real, sin pyxel, stdlib only. Ver PLAN.md (decisiones e
hitos de la T2). Dueño: Seath (`feat/meta-ui`).
"""

from core.progression.progression import CAP0_CONTRACT_BOON, evaluate_unlocks

__version__ = "0.1.0"

__all__ = ["CAP0_CONTRACT_BOON", "evaluate_unlocks"]