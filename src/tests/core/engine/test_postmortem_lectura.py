"""O1 04/09 — El Auditor cita lo que LEÍSTE (read_marks).

Criterios del plan:
1. Sesión cap. 3 (cat orden → sudo) → informe añade línea lectura con ruta exacta, resuelta.
2. Sesión con sudo sin lectura previa → variante ciega.
3. Sesión cap. 0 (sin sudo) → informe byte-idéntico al de hoy (sin segunda línea).

Sin imports de sandbox: el post-mortem lee `read_marks` y detecta sudo por historial.
"""
from __future__ import annotations

from core.curriculum import load_curriculum
from core.engine import (
    LINE_KEY_CIEGA,
    LINE_KEY_LECTURA,
    LINE_KEY_PICO,
    build_postmortem,
)
from core.engine.postmortem import _has_sudo
from core.generator import generate, new_session
from core.sandbox.shell import Shell
from data.textos import load_textos, resolve

SUDO_PATH = "/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt"


def _shell_dict_con_sudo(marks: list[str] | None, *, total_noise: int = 5) -> dict:
    """Shell dict mínimo con un sudo en el historial."""
    hist = [
        {
            "line": "sudo cat /etc/hosts",
            "result": {
                "exit_code": 1,
                "noise": [{"tipo": "command", "data": {"command": "sudo", "amount": 3}}],
            },
        }
    ]
    d: dict = {"history": hist, "total_noise": total_noise}
    if marks is not None:
        d["read_marks"] = marks
    return d


def test_lectura_con_sudo_y_marca_cita_ruta_exacta() -> None:
    """Con sudo y read_marks → lectura con path exacto, resuelta (no clave cruda)."""
    sd = _shell_dict_con_sudo([SUDO_PATH])
    informe = build_postmortem(sd, {"noise_budget": 12})
    # Segunda línea presente
    assert "auditor_lectura" in informe
    lec = informe["auditor_lectura"]
    assert lec["line_key"] == LINE_KEY_LECTURA
    assert lec["args"]["path"] == SUDO_PATH
    # Texto resuelto contiene la ruta y no es clave cruda
    assert informe["auditor_lectura_text"] != LINE_KEY_LECTURA
    assert SUDO_PATH in informe["auditor_lectura_text"]
    # lines_resolved gana segunda entrada
    assert len(informe["lines_resolved"]) == 2
    assert informe["lines_resolved"][1] == informe["auditor_lectura_text"]
    # Verifica que resuelve contra textos.json
    textos = load_textos()
    assert resolve(LINE_KEY_LECTURA, {"path": SUDO_PATH}, textos) == informe["auditor_lectura_text"]


def test_ciega_con_sudo_sin_marca_variante_a_ciegas() -> None:
    """Con sudo y read_marks vacío → variante ciega, resuelta."""
    sd = _shell_dict_con_sudo([])
    informe = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_lectura" in informe
    lec = informe["auditor_lectura"]
    assert lec["line_key"] == LINE_KEY_CIEGA
    assert lec["args"] == {}
    assert informe["auditor_lectura_text"] != LINE_KEY_CIEGA
    assert "sin lectura" in informe["auditor_lectura_text"].lower()
    assert len(informe["lines_resolved"]) == 2
    textos = load_textos()
    assert resolve(LINE_KEY_CIEGA, {}, textos) == informe["auditor_lectura_text"]


def test_sin_sudo_informe_byte_identico_sin_segunda_linea() -> None:
    """Sin sudo → sin segunda línea, informe byte-idéntico (cap. 0/2 no ganan texto)."""
    # Sesión canónica del cap. 0 (ls → cat → cp …) sin sudo
    inc = generate(7, 0, curriculum=load_curriculum())
    shell = new_session(inc)
    shell.execute("ls /srv/oficina-vecinal-muelle-norte")
    shell.execute("cat /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt")
    shell.execute("cp /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt /usb/")
    shell_dict = shell.to_dict()
    # No hay sudo en el historial
    assert not _has_sudo(shell_dict)
    informe = build_postmortem(shell_dict, {"noise_budget": 12})
    assert "auditor_lectura" not in informe
    assert "auditor_lectura_text" not in informe
    assert len(informe["lines_resolved"]) == 1
    # La línea sigue siendo pico/cruce sin alterar
    assert informe["auditor"]["line_key"] == LINE_KEY_PICO
    # Determinismo: segunda llamada idéntica
    informe2 = build_postmortem(shell_dict, {"noise_budget": 12})
    assert informe == informe2


def test_session_real_cap3_cat_luego_sudo_gana_lectura() -> None:
    """Circuito real cap. 3: cat orden → sudo → post-mortem cita lectura."""
    inc = generate(42, 3, curriculum=load_curriculum())
    shell = new_session(inc)
    # Antes de leer, read_marks vacío
    assert shell.read_marks == set()
    # Lee la orden (gana marca)
    r1 = shell.execute(f"cat {SUDO_PATH}")
    assert r1.exit_code == 0
    assert SUDO_PATH in shell.read_marks
    # Sudo posterior (eleva, firma)
    r2 = shell.execute("sudo cat /etc/hosts")
    # El sudo puede fallar por /etc/hosts inexistente pero debe haber elevado (premium)
    # Verificamos que history contiene sudo
    assert _has_sudo(shell.to_dict())
    informe = build_postmortem(shell.to_dict(), {"noise_budget": 12})
    assert informe["auditor_lectura"]["line_key"] == LINE_KEY_LECTURA
    assert SUDO_PATH in informe["auditor_lectura_text"]
    assert len(informe["lines_resolved"]) == 2


def test_session_real_cap3_sudo_sin_leer_da_ciega() -> None:
    """Circuito real cap. 3: sudo sin cat previo → variante ciega."""
    inc = generate(42, 3, curriculum=load_curriculum())
    shell = new_session(inc)
    # Sudo directo sin leer
    shell.execute("sudo cat /etc/hosts")
    assert shell.read_marks == set()
    assert _has_sudo(shell.to_dict())
    informe = build_postmortem(shell.to_dict(), {"noise_budget": 12})
    assert informe["auditor_lectura"]["line_key"] == LINE_KEY_CIEGA
    assert "sin lectura" in informe["auditor_lectura_text"].lower()


def test_read_marks_ausente_equivale_a_vacio_no_crash() -> None:
    """Saves viejos sin read_marks (clave ausente) no crashean, dan ciega si hubo sudo."""
    sd = {"history": [{"line": "sudo ls", "result": {"exit_code": 1, "noise": []}}], "total_noise": 0}
    # Sin clave read_marks → tratado como vacío
    informe = build_postmortem(sd, {"noise_budget": 12})
    assert informe["auditor_lectura"]["line_key"] == LINE_KEY_CIEGA


def test_lectura_determinista_por_codepoint() -> None:
    """Múltiples marcas → cita la primera por codepoint (determinista)."""
    sd = _shell_dict_con_sudo([SUDO_PATH, "/a/b/c"])
    informe = build_postmortem(sd, {"noise_budget": 12})
    # Ordenada por codepoint: /a/b/c < /srv/...
    assert informe["auditor_lectura"]["args"]["path"] == "/a/b/c"
    # Segunda llamada idéntica
    assert build_postmortem(sd, {"noise_budget": 12}) == informe
