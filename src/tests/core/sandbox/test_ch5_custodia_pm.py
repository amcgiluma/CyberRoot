"""S1 18/09 — detector post-mortem custodia (cap. 5).

3-4 tests del criterio S1:
- con cat custodia → custodia presente, pico+custodia en lines_resolved
- sin cat → byte-idéntico a hoy (sin custodia)
- cat custodia exit 1 → no dispara
- determinismo
"""
from __future__ import annotations

from core.engine import build_postmortem
from core.engine.postmortem import LINE_KEY_CUSTODIA
from data.textos import load_textos, resolve


def _sd(history_entries, tick=5, total_noise=None):
    hist = []
    for e in history_entries:
        hist.append(e)
    tn = total_noise if total_noise is not None else len(hist)
    return {"history": hist, "total_noise": tn, "tick": tick}


def test_custodia_detectada():
    sd = {
        "history": [
            {"line": "cat /tmp/volcado-custodia.csv", "result": {"exit_code": 0, "noise": [{"data": {"command": "cat", "amount": 1}}]}},
        ],
        "total_noise": 1,
        "tick": 3,
    }
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_custodia" in inf
    assert inf["auditor_custodia"]["line_key"] == LINE_KEY_CUSTODIA
    assert "auditor_custodia_text" in inf
    textos = load_textos()
    assert resolve(LINE_KEY_CUSTODIA, {}, textos) == inf["auditor_custodia_text"]
    assert inf["auditor_custodia_text"] in inf["lines_resolved"]
    # debe haber al menos pico + custodia = 2 líneas
    assert len(inf["lines_resolved"]) >= 2
    # determinismo
    inf2 = build_postmortem(sd, {"noise_budget": 12})
    assert inf == inf2


def test_sin_custodia_byte_identico():
    sd = {
        "history": [
            {"line": "cat /tmp/volcado.csv", "result": {"exit_code": 0, "noise": [{"data": {"command": "cat", "amount": 1}}]}},
            {"line": "cut -d'|' -f1 /tmp/volcado.csv | grep TR-", "result": {"exit_code": 0, "noise": [{"data": {"command": "cut", "amount": 1}}, {"data": {"command": "grep", "amount": 2}}]}},
        ],
        "total_noise": 3,
        "tick": 5,
    }
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_custodia" not in inf
    assert "auditor_custodia_text" not in inf
    # byte-idéntico: sin custodia no añade campo volcado custodia
    # segunda llamada idéntica
    inf2 = build_postmortem(sd, {"noise_budget": 12})
    assert inf == inf2
    # líneas no deben contener custodia
    for line in inf["lines_resolved"]:
        assert "custodia" not in line.lower()


def test_custodia_exit1_no_dispara():
    sd = {
        "history": [
            {"line": "cat /tmp/volcado-custodia.csv", "result": {"exit_code": 1, "noise": [{"data": {"command": "cat", "amount": 1}}]}},
        ],
        "total_noise": 1,
        "tick": 3,
    }
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_custodia" not in inf
    # exit 1 es No such file (caducado) → no custodia
    assert "volcado" not in inf or inf.get("auditor_custodia") is None


def test_custodia_determinismo_y_coexistencia():
    # custodia coexiste con volcado rescate (dos huellas)
    sd = {
        "history": [
            {"line": "scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv", "result": {"exit_code": 0, "noise": [{"data": {"command": "scp", "amount": 3}}]}},
            {"line": "cat /tmp/volcado-custodia.csv", "result": {"exit_code": 0, "noise": [{"data": {"command": "cat", "amount": 1}}]}},
        ],
        "total_noise": 4,
        "tick": 4,
    }
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_volcado" in inf
    assert "auditor_custodia" in inf
    # líneas contienen ambas
    assert any("volcado" in l.lower() for l in inf["lines_resolved"])
    assert any("custodia" in l.lower() for l in inf["lines_resolved"])
    assert build_postmortem(sd, {"noise_budget": 12}) == inf
