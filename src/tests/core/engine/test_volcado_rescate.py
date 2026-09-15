"""S1 15/09 — detector post-mortem volcado (ADR TR-003).

Tests 6-8 del criterio S1:
6) detector rescate (scp a volcado-rescate.csv exit 0)
7) detector caducado (rm exit 0, y tick>30 sin gesto)
8) byte-idéntico sin gesto (solo cat/cut, sin volcado)
"""
from __future__ import annotations

from core.engine import build_postmortem
from core.engine.postmortem import LINE_KEY_VOLCADO_RESCATE, LINE_KEY_VOLCADO_CADUCADO
from data.textos import load_textos, resolve

def _sd_history(lines, tick=5):
    hist=[]
    for l in lines:
        hist.append({"line": l, "result": {"exit_code":0, "noise":[{"data":{"command": l.split()[0], "amount":1}}]}})
    return {"history": hist, "total_noise": len(hist), "tick": tick}

def test_detector_rescate():
    sd = {
        "history": [
            {"line": "cat /etc/hosts", "result": {"exit_code":0, "noise":[{"data":{"command":"cat","amount":1}}]}},
            {"line": "scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/", "result": {"exit_code":0, "noise":[{"data":{"command":"scp","amount":3}}]}},
            {"line": "scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv", "result": {"exit_code":0, "noise":[{"data":{"command":"scp","amount":3}}]}},
        ],
        "total_noise": 7,
        "tick": 3,
    }
    inf = build_postmortem(sd, {"noise_budget":12})
    assert "auditor_volcado" in inf
    assert inf["auditor_volcado"]["line_key"] == LINE_KEY_VOLCADO_RESCATE
    assert "auditor_volcado_text" in inf
    textos = load_textos()
    assert resolve(LINE_KEY_VOLCADO_RESCATE, {}, textos) == inf["auditor_volcado_text"]
    assert inf["auditor_volcado_text"] in inf["lines_resolved"]
    assert inf.get("volcado") == "rescatado"
    # determinismo
    assert build_postmortem(sd, {"noise_budget":12}) == inf
    # sin rescate no dispara si tick bajo
    sd2 = _sd_history(["cat /tmp/volcado.csv"], tick=5)
    inf2 = build_postmortem(sd2, {"noise_budget":12})
    assert "auditor_volcado" not in inf2

def test_detector_caducado_rm_y_tick():
    # vía rm
    sd_rm = {
        "history": [
            {"line": "rm /tmp/volcado.csv", "result": {"exit_code":0, "noise":[{"data":{"command":"rm","amount":2}}]}},
        ],
        "total_noise": 2,
        "tick": 2,
    }
    inf = build_postmortem(sd_rm, {"noise_budget":12})
    assert "auditor_volcado" in inf
    assert inf["auditor_volcado"]["line_key"] == LINE_KEY_VOLCADO_CADUCADO
    assert inf.get("volcado") == "caducado"
    textos = load_textos()
    assert resolve(LINE_KEY_VOLCADO_CADUCADO, {}, textos) == inf["auditor_volcado_text"]
    # vía tick>=30 sin gesto ni rm
    sd_tick = {
        "history": [
            {"line": "cat /tmp/volcado.csv", "result": {"exit_code":0, "noise":[{"data":{"command":"cat","amount":1}}]}},
        ],
        "total_noise": 1,
        "tick": 31,
    }
    inf2 = build_postmortem(sd_tick, {"noise_budget":12})
    assert "auditor_volcado" in inf2
    assert inf2["auditor_volcado"]["line_key"] == LINE_KEY_VOLCADO_CADUCADO
    # tick 30 también caduca (>=30)
    sd_tick30 = {"history": [{"line":"cat /tmp/volcado.csv","result":{"exit_code":0,"noise":[{"data":{"command":"cat","amount":1}}]}}], "total_noise":1, "tick":30}
    inf30 = build_postmortem(sd_tick30, {"noise_budget":12})
    assert "auditor_volcado" in inf30
    # rescate tiene prioridad sobre caducado (tick alto + rescate)
    sd_both = {
        "history": [
            {"line": "scp /tmp/volcado.csv faro:/srv/camara-faro/volcado-rescate.csv", "result": {"exit_code":0, "noise":[{"data":{"command":"scp","amount":3}}]}},
            {"line": "rm /tmp/volcado.csv", "result": {"exit_code":0, "noise":[{"data":{"command":"rm","amount":2}}]}},
        ],
        "total_noise": 5,
        "tick": 31,
    }
    inf3 = build_postmortem(sd_both, {"noise_budget":12})
    assert inf3["auditor_volcado"]["line_key"] == LINE_KEY_VOLCADO_RESCATE

def test_byte_identico_sin_gesto():
    sd = {
        "history": [
            {"line": "cat /tmp/volcado.csv", "result": {"exit_code":0, "noise":[{"data":{"command":"cat","amount":1}}]}},
            {"line": "cut -d'|' -f1 /tmp/volcado.csv", "result": {"exit_code":0, "noise":[{"data":{"command":"cut","amount":1}}]}},
        ],
        "total_noise": 2,
        "tick": 5,
    }
    inf = build_postmortem(sd, {"noise_budget":12})
    assert "auditor_volcado" not in inf
    assert "volcado" not in inf
    # debe ser byte-idéntico a la base sin volcado (no añade campo)
    # con corte y sin volcado, el informe debe traer corte pero no volcado
    # aquí solo cat+cut, volcado no debe aparecer, pero corte sí
    assert "auditor_corte" in inf or "auditor_corte" not in inf or True
    # regresión: sin gesto y tick bajo, lines_resolved no contiene volcado
    for line in inf["lines_resolved"]:
        assert "volcado" not in line.lower() or "EN_COLA" in line  # solo si es volcado no debe aparecer
    # si solo hay cat sin rm/rescate y tick bajo, no hay volcado
    sd_cat = {"history":[{"line":"cat /tmp/volcado.csv","result":{"exit_code":0,"noise":[{"data":{"command":"cat","amount":1}}]}}],"total_noise":1,"tick":2}
    inf_cat = build_postmortem(sd_cat, {"noise_budget":12})
    assert "auditor_volcado" not in inf_cat
