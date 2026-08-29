"""progression.py — desbloqueos POR COMPETENCIA (ARCHITECTURE §2.7, DESIGN §7.5.3).

Regla dura §4.2: «el espejo da conveniencia e identidad de build, NUNCA
conocimiento». El unlock se dispara por COMPETENCIA DEMOSTRADA (evidencia en
el historial de la sesión), jamás por grind ni por compra. v0 implementa UNA
regla (decisión de alcance del plan 29/08): completar el contrato del cap. 0
(la extracción `cp` canónica a `/usb`, §6.4.4) marca el concepto `c.cp` como
dominado.

Este módulo NO importa `core.state` en runtime (sólo `TYPE_CHECKING` para el
typing): recibe el `GameState` por composición, lee `state.shell.history`
(evidencia) y escribe `state.knowledge` (inventario). Así `core.state` no
importa `core.progression` (se evita el ciclo y `state` conserva la fachada
de agregación); quien conecta ambos es el orquestador (`game.py` futuro) o el
test. stdlib only (shlex), stdlib permitida por `test_core_stdlib_only.py`.
"""

from __future__ import annotations

import shlex
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # solo anotaciones: evita el ciclo state↔progression
    from core.state.state import GameState

#: Concepto dominado por completar el contrato del cap. 0 (§6.1; la canónica
#: hace `cp <oficina>/<proveedor> /usb/`).
CAP0_CONTRACT_BOON = "c.cp"

#: La extracción del cap. 0 aterriza SIEMPRE bajo `/usb` (skin del dossier).
_CAP0_USB_DEST = "/usb"


def _parsed_argv(line: str) -> tuple[str, ...] | None:
    """`shlex.split` de la línea registrada; None si no es parseable.

    El historial de la Shell guarda `{"line": str, "result": to_dict()}` (no
    el argv), así que la evidencia se reconstruye parseando la línea.
    """
    try:
        return tuple(shlex.split(line.strip(), posix=True))
    except ValueError:
        return None


def _cap0_extraction_completed(shell: Any) -> bool:
    """Evidencia de haber completado la extracción del cap. 0 (canónica §6.4.4).

    Verdadero si hay en el historial un `cp` con `exit_code == 0` cuyo destino
    (último argumento) cae bajo `/usb`. Detecta "contrato del cap. 0
    completado" SOLO a partir del estado (sin depender de generator/engine).
    """
    for entry in shell.history:
        if entry["result"].get("exit_code") != 0:
            continue
        argv = _parsed_argv(entry["line"])
        if not argv or argv[0] != "cp" or len(argv) < 2:
            continue
        if argv[-1].startswith(_CAP0_USB_DEST):
            return True
    return False


def evaluate_unlocks(state: "GameState") -> list[str]:
    """Aplica la regla v0 y marca dominados los boons cuya competencia se demostró.

    Idempotente: si el concepto ya estaba dominado no se re-marca ni se repite
    en la lista de retorno. Devuelve los boons RECIÉN dominados en esta llamada
    (vacía si nada nuevo). La persistencia del estado la decide el llamador
    (normalmente `state.save(...)` o `save_game(...)`).
    """
    newly_dominated: list[str] = []
    if _cap0_extraction_completed(state.shell):
        if not state.knowledge.get(CAP0_CONTRACT_BOON):
            state.knowledge[CAP0_CONTRACT_BOON] = True
            newly_dominated.append(CAP0_CONTRACT_BOON)
    return newly_dominated