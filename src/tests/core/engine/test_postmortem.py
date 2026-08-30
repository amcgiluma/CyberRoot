"""O2 post-mortem v0 — el Auditor lee el HISTORIAL REAL de la sesión.

Cubre la AC del plan 30/08: `build_postmortem(shell_dict, state)` es una
función pura, testeable headless, que:
  - reproduce la factura GNU (cuentas por comando + errores) de la sesión
    canónica del cap. 0 (§6.4.4 / test_session_cap0) en la MISMA unidad de
    ruido que el presupuesto (🧭10 de Oscar);
  - pone `total_noise` vs `noise_budget` lado a lado y veredicta
    `dentro_presupuesto`;
  - citar el comando CONCRETO que disparó la detección (cruce) o el pico
    si no se cruza, con su amount — vía `auditor.args` (clave + datos para
    que render resuelva la prosa contra data/, §3).
"""
from __future__ import annotations

from core.curriculum import load_curriculum
from core.engine import (
    DEFAULT_NOISE_BUDGET,
    LINE_KEY_CRUCE,
    LINE_KEY_PICO,
    build_postmortem,
)
from core.engine.postmortem import _amount, _cruce, _factura, _pico
from core.generator import generate, new_session
from core.sandbox.shell import Shell

OFICINA = "/srv/oficina-vecinal-muelle-norte"


def _sesion_canonica() -> Shell:
    """La sesión canónica del cap. 0: ls → cat → cp → cd → ls (todo exit 0)."""
    inc = generate(7, 0, curriculum=load_curriculum())
    shell = new_session(inc)
    shell.execute(f"ls {OFICINA}")
    shell.execute(f"cat {OFICINA}/nombre_de_proveedor.txt")
    shell.execute(f"cp {OFICINA}/nombre_de_proveedor.txt /usb/")
    shell.execute("cd /srv")
    shell.execute("ls")
    return shell


def test_factura_gnu_sesion_canonica() -> None:
    """La factura replica las cuentas de la sesión canónica (ls 2, cat 1, cp 1,
    cd 1) sin errores, y el total_noise es el del perfil (1+1+3+0+1=6)."""
    shell = _sesion_canonica()
    shell_dict = shell.to_dict()
    assert shell.total_noise == 6
    factura = _factura(shell_dict)
    assert factura["ls"] == 2
    assert factura["cat"] == 1
    assert factura["cp"] == 1
    assert factura["cd"] == 1
    assert factura["errores"] == 0
    # La factura es la MISMA unidad que el presupuesto (ambos puntos de ruido).
    assert set(factura) == {"cat", "cd", "cp", "errores", "ls"}


def test_postmortem_total_noise_y_presupuesto_misma_unidad() -> None:
    """El informe expone total_noise vs noise_budget lado a lado (🧭10) y
    declara dentro_presupuesto para la canónica (6 <= 12)."""
    shell = _sesion_canonica()
    informe = build_postmortem(shell.to_dict(), {"noise_budget": DEFAULT_NOISE_BUDGET})
    assert informe["total_noise"] == 6
    assert informe["noise_budget"] == DEFAULT_NOISE_BUDGET
    assert informe["dentro_presupuesto"] is True


def test_auditor_linea_con_cta_pico_sin_cruce() -> None:
    """Sin cruzar el presupuesto, el Auditor cita el PICO (comando + amount
    concreto del history). Con el perfil v1 el pico es cp (amount 3)."""
    shell = _sesion_canonica()
    informe = build_postmortem(shell.to_dict(), {"noise_budget": 12})
    auditor = informe["auditor"]
    assert auditor["line_key"] == LINE_KEY_PICO
    assert auditor["args"]["command"] == "cp"
    assert auditor["args"]["amount"] == 3
    assert auditor["args"]["total_noise"] == 6
    assert auditor["args"]["noise_budget"] == 12


def test_auditor_linea_cita_el_cruce_cuando_se_supera() -> None:
    """Si el ruido cruza el presupuesto, el Auditor cita el comando CONCRETO
    que hizo cruzar el acumulado (no el más ruidoso, sino el que te delata).
    Presupuesto 5: ls(1)+cat(1)+cp(3)=5 cruza en el cp → linea cruce, cp/3."""
    shell = _sesion_canonica()
    informe = build_postmortem(shell.to_dict(), {"noise_budget": 5})
    auditor = informe["auditor"]
    assert auditor["line_key"] == LINE_KEY_CRUCE
    assert auditor["args"]["command"] == "cp"
    assert auditor["args"]["amount"] == 3
    assert informe["dentro_presupuesto"] is False


def test_postmortem_con_errores_cuenta_y_pico() -> None:
    """Los errores (exit != 0) se cuentan en la factura; el pico sigue siendo
    el comando con más ruido aunque haya un fallo posterior."""
    shell = _sesion_canonica()  # ls/cat/cp/cd/ls → ruido 6
    shell.execute("cat /no/existe")
    assert shell.total_noise == 7  # 6 de la canónica + 1 del cat fallido
    shell_dict = shell.to_dict()
    assert _factura(shell_dict)["errores"] == 1
    informe = build_postmortem(shell_dict, {"noise_budget": 12})
    assert informe["dentro_presupuesto"] is True
    # El pico sigue siendo el cp (3), no el cat fallido (1).
    assert informe["auditor"]["args"]["command"] == "cp"
    assert informe["auditor"]["args"]["amount"] == 3
    assert informe["total_noise"] == 7


def test_postmortem_y_sin_estado_fuerza_default_presupuesto() -> None:
    """Sin `noise_budget` en state, se usa el default ⚠️ v1 (12) sin fallar."""
    shell = _sesion_canonica()
    informe = build_postmortem(shell.to_dict(), None)
    assert informe["noise_budget"] == DEFAULT_NOISE_BUDGET


def test_helpers_internos_determinismo() -> None:
    """Los helpers son deterministas ante el mismo history (sin RNG)."""
    shell = _sesion_canonica()
    sd = shell.to_dict()
    assert _cruce(sd, 5)[0] is True
    assert _cruce(sd, 12)[0] is False
    pico = _pico(sd)
    assert pico is not None and pico["result"]["noise"]  # pico con ruido presente
    entry = sd["history"][2]  # el cp
    assert _amount(entry) == 3


def test_postmortem_es_plano_y_serializable() -> None:
    """El informe es un dict plano que cruza ensure_plain (contrato §3)."""
    import json

    shell = _sesion_canonica()
    informe = build_postmortem(shell.to_dict(), {"noise_budget": 12})
    vuelta = json.loads(json.dumps(informe))
    assert vuelta == informe