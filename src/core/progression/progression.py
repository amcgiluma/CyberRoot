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

#: Logro «Cero rastro» (§7.6, T2 30/08): cap. 0 completo con `total_noise`
#: igual o inferior al umbral. Umbral ⚠️ v1 calibrable (cliente: O3 harness).
LOGRO_CERO_RASTRO = "logro.cero_rastro"

#: Logro «Mano de seda» (§7.6, T2 30/08): extracción canónica sin ni un
#: `exit != 0` en toda la sesión.
LOGRO_MANO_SEDA = "logro.mano_de_seda"

#: Umbral de ruido del «Cero rastro» ⚠️ v1. La run canónica del cap. 0
#: (cat 1 + cp 3, §6.4.4) cierra en `total_noise == 4`.
UMBRAL_CERO_RASTRO = 4


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
            # Meta del dominio (🧭9): `tick` = tiempo simulado al detectarse,
            # `order` = secuencia de dominio (monótono). El save guarda CUÁNDO.
            state.mastered[CAP0_CONTRACT_BOON] = {
                "tick": state.shell.tick,
                "order": len(state.mastered) + 1,
            }
            newly_dominated.append(CAP0_CONTRACT_BOON)
    return newly_dominated


def _factura_capitulo(shell: Any) -> dict[str, Any]:
    """Factura GNU de la sesión (§7.2, 🧭10): usos/ruido/errores por comando.

    Se lee SOLO del estado serializado (headless, vale sobre un save cargado):
    cada entrada de `history` guarda `{"line", "result"}` con el `noise`
    listo como eventos; `exit_code` marca el error. Comando de una línea no
    parseable → `"sh"` (no rompe la suma). El ruido se agrega por comando en
    la MISMA unidad que el budget (decisión 🧭10 de Oscar).
    """
    por_comando: dict[str, dict[str, int]] = {}
    for entry in shell.history:
        result = entry["result"]
        argv = _parsed_argv(entry["line"])
        cmd = argv[0] if argv else "sh"
        ruido = int(
            sum(
                int(ev.get("data", {}).get("amount", 0))
                for ev in result.get("noise", [])
            )
        )
        fila = por_comando.setdefault(cmd, {"usos": 0, "ruido": 0, "errores": 0})
        fila["usos"] += 1
        fila["ruido"] += ruido
        if result.get("exit_code", 0) != 0:
            fila["errores"] += 1
    ordenado = {cmd: por_comando[cmd] for cmd in sorted(por_comando)}
    return {
        "por_comando": ordenado,
        "total_usos": sum(f["usos"] for f in por_comando.values()),
        "total_ruido": sum(f["ruido"] for f in por_comando.values()),
        "total_errores": sum(f["errores"] for f in por_comando.values()),
    }


def resumen_competencia(state: "GameState") -> dict[str, Any]:
    """Resumen de competencias dominadas + factura del capítulo (prepara 🧭9).

    Sin UI NI forma (eso lo decide Gwyn, plan 30/08): aquí SOLO los datos.
    Devuelve una estructura headless:
        {"dominados": [{"concepto", "tick", "order"}, ...], "factura": {...}}
    `dominados` se deriva de `state.knowledge` (fuente de verdad: QUIÉN domina);
    el momento viene de `state.mastered` (None para un boon ya dominado en un
    save previo a esta meta, por compatibilidad v1). `factura` es la GNU de la
    sesión (§7.2/🧭10) en la misma unidad que el noise_budget.
    """
    dominados: list[dict[str, Any]] = []
    for boon, dominado in state.knowledge.items():
        if not dominado:
            continue
        momento = state.mastered.get(boon)
        dominados.append(
            {
                "concepto": boon,
                "tick": momento["tick"] if momento else None,
                "order": momento["order"] if momento else None,
            }
        )
    # Determinista: por order (los sin meta, al final) y luego por concepto.
    dominados.sort(key=lambda e: (e["order"] if e["order"] is not None else 1 << 30,
                                  e["concepto"]))
    return {"dominados": dominados, "factura": _factura_capitulo(state.shell)}


def _no_exit_errors(shell: Any) -> bool:
    """True si ni una línea del historial terminó con `exit != 0` (Mano de seda)."""
    return all(entry["result"].get("exit_code", 0) == 0 for entry in shell.history)


def evaluate_logros(state: "GameState") -> list[str]:
    """Evalúa y persiste los logros de la sesión (§7.6, T2 30/08).

    Sin popup moral (decisión de alcance): el logro es un DATO del save; el
    momento se pinta cuando haya render/Hub. Idempotente: devuelve SOLO los
    recién ganados. Mecanismo de datos: umbrales como constantes ⚠️ v1
    calibrables (cliente: O3 del harness). Los logros se anclan al contrato del
    cap. 0 completado.
    """
    newly: list[str] = []
    if _cap0_extraction_completed(state.shell):
        if (
            state.shell.total_noise <= UMBRAL_CERO_RASTRO
            and not state.logros.get(LOGRO_CERO_RASTRO)
        ):
            state.logros[LOGRO_CERO_RASTRO] = True
            newly.append(LOGRO_CERO_RASTRO)
        if _no_exit_errors(state.shell) and not state.logros.get(LOGRO_MANO_SEDA):
            state.logros[LOGRO_MANO_SEDA] = True
            newly.append(LOGRO_MANO_SEDA)
    return newly