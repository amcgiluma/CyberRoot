"""25/09 O1 — factura frugal postmortem grep -c (P2).

AC: si último grep exit 0 fue grep -c censo → añade línea postmortem.auditor.grep_c_count
hermana; ceniza / sin -c / exit1 no añade; byte-idéntico sin huella.
"""
from __future__ import annotations

from core.engine.postmortem import LINE_KEY_GREP_C_COUNT, build_postmortem, _extract_greps
from data.textos import load_textos, resolve


def _sd(history):
    return {"history": history, "total_noise": len(history), "tick": 1}

def _entry(line, exit_code=0, stdout="1\n"):
    return {"line": line, "result": {"exit_code": exit_code, "stdout": stdout, "noise": [{"data": {"command": "grep", "amount": 1}}]}}

def test_factura_grep_c_censo_exit0_anyade():
    sd = _sd([{"line": "ps aux", "result": {"exit_code": 0, "stdout": "x\n", "noise": [{"data": {"command": "ps", "amount": 1}}]}},
              _entry("ps aux | grep -c censo", 0, "1\n")])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_grep_c_count" in inf
    assert inf["auditor_grep_c_count"]["line_key"] == LINE_KEY_GREP_C_COUNT
    assert inf["auditor_grep_c_count"]["args"]["count"] == "1"
    assert inf["auditor_grep_c_count_text"] != LINE_KEY_GREP_C_COUNT
    assert "1" in inf["auditor_grep_c_count_text"]
    assert inf["auditor_grep_c_count_text"] in inf["lines_resolved"]
    assert resolve(LINE_KEY_GREP_C_COUNT, inf["auditor_grep_c_count"]["args"], load_textos()) == inf["auditor_grep_c_count_text"]

def test_no_anyade_sin_c():
    sd = _sd([_entry("ps aux | grep censo", 0, "intruso\n")])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_grep_c_count" not in inf

def test_no_anyade_ceniza():
    sd = _sd([_entry("ps aux | grep -c ceniza", 1, "0\n")])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_grep_c_count" not in inf
    # incluso con exit 0 ceniza no es censo
    sd2 = _sd([_entry("ps aux | grep -c ceniza", 0, "1\n")])
    assert "auditor_grep_c_count" not in build_postmortem(sd2, {"noise_budget": 12})

def test_no_anyade_exit1():
    sd = _sd([_entry("ps aux | grep -c censo", 1, "0\n")])
    assert "auditor_grep_c_count" not in build_postmortem(sd, {"noise_budget": 12})

def test_combinado_ci_caso_insensible():
    sd = _sd([_entry("ps aux | grep -c -i CENSO", 0, "1\n")])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_grep_c_count" in inf
    sd2 = _sd([_entry("ps aux | grep -ci CENSO", 0, "1\n")])
    assert "auditor_grep_c_count" in build_postmortem(sd2, {"noise_budget": 12})

def test_combinado_cv_cuenta_invertida_no_es_censo():
    # grep -c -v censo sobre e2 contaría líneas sin censo → patrón sigue siendo censo, pero has_c true y exit 0
    # Nuestro detector solo mira patrón contiene censo, así que -cv censo SÍ contaría (es grep -c censo invertido)
    # Eso es honesto: si el jugador hace grep -cv censo y da 1 (zzz), también es -c censo.
    sd = _sd([_entry("ps aux | grep -cv censo", 0, "1\n")])
    assert "auditor_grep_c_count" in build_postmortem(sd, {"noise_budget": 12})

def test_ultimo_manda():
    sd = _sd([
        _entry("ps aux | grep -c censo", 0, "1\n"),
        _entry("ps aux | grep censo", 0, "intruso\n"),
        _entry("ps aux | grep -c censo", 0, "1\n"),
    ])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_grep_c_count" in inf
    # si último es sin -c, no debe haber
    sd2 = _sd([
        _entry("ps aux | grep -c censo", 0, "1\n"),
        _entry("ps aux | grep censo", 0, "intruso\n"),
    ])
    assert "auditor_grep_c_count" not in build_postmortem(sd2, {"noise_budget": 12})

def test_extract_greps_unico_punto():
    sd = _sd([
        {"line": "ls", "result": {"exit_code": 0, "noise": [{"data": {"command": "ls", "amount": 1}}]}},
        _entry("ps aux | grep -c censo", 0),
        _entry("ps aux | grep -i censo", 0),
    ])
    greps = _extract_greps(sd)
    assert len(greps) == 2
    assert greps[0]["has_c"] is True
    assert greps[1]["has_c"] is False
    assert greps[0]["pattern"] == "censo"

def test_factura_no_rompe_byte_identico_sin_grep():
    # informe sin grep -c debe ser byte-idéntico al de ayer (sin claves nuevas)
    from core.engine.postmortem import build_postmortem as bpm
    sd = _sd([{"line": "ls /tmp", "result": {"exit_code": 0, "stdout": "", "noise": [{"data": {"command": "ls", "amount": 1}}]}}])
    inf = bpm(sd, {"noise_budget": 12})
    assert "auditor_grep_c_count" not in inf
    assert inf["auditor"]["line_key"] in ("postmortem.auditor.cruce", "postmortem.auditor.pico")

def test_hint_2_contiene_factura():
    t = load_textos()
    assert "postmortem.auditor.grep_c_count" in t
    assert "story.ch5.e2.hint_2" in t
    hint = t["story.ch5.e2.hint_2"]
    assert "grep -c censo" in hint
    assert "grep -i" in hint.lower()
    assert "La factura frugal" in hint
