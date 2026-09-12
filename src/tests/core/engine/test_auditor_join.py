"""O1 12/09 — auditor_join: la cuarta huella del Auditor (reposición).

3 casos:
- join con -v dispara auditor_join
- join sin -v documentado no dispara (byte-idéntico salvo join)
- sin join byte-idéntico
"""
from __future__ import annotations

from core.engine import build_postmortem
from core.engine.postmortem import LINE_KEY_JOIN, _extract_join_args, _find_join
from data.textos import load_textos, resolve


def _sd(line: str) -> dict:
    return {
        "history": [{"line": line, "result": {"exit_code": 0, "noise": [{"data": {"command": "join", "amount": 1}}]}}],
        "total_noise": 1,
    }


def test_join_con_v_dispara():
    """join con -v añade auditor_join con texto resuelto."""
    sd = _sd("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv")
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_join" in inf
    assert inf["auditor_join"]["line_key"] == LINE_KEY_JOIN
    assert "auditor_join_text" in inf
    assert inf["auditor_join_text"] != LINE_KEY_JOIN
    assert "-v" in inf["auditor_join_text"] or "anti-join" in inf["auditor_join_text"]
    textos = load_textos()
    assert resolve(LINE_KEY_JOIN, inf["auditor_join"]["args"], textos) == inf["auditor_join_text"]
    assert inf["auditor_join_text"] in inf["lines_resolved"]
    assert len(inf["lines_resolved"]) == 2  # pico + join
    # determinismo
    assert build_postmortem(sd, {"noise_budget": 12}) == inf
    # variante -v1 sin espacio
    sd2 = _sd("join -t'|' -v1 /tmp/a /tmp/b")
    assert "auditor_join" in build_postmortem(sd2, {"noise_budget": 12})
    # variante tras pipe
    sd3 = {"history": [{"line": "cat /tmp/x | join -t'|' -v 1 - /tmp/b", "result": {"exit_code": 0, "noise": [{"data": {"command": "join", "amount": 1}}]}}], "total_noise": 1}
    assert "auditor_join" in build_postmortem(sd3, {"noise_budget": 12})


def test_join_sin_v_no_dispara_documentado():
    """join sin -v NO dispara — caso documentado."""
    sd = _sd("join -t'|' -1 3 -2 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv")
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_join" not in inf
    assert "auditor_join_text" not in inf
    assert len(inf["lines_resolved"]) == 1
    assert _extract_join_args("join -t'|' /tmp/a /tmp/b") is None
    assert _find_join(sd) is None


def test_sin_join_byte_identico():
    """Sin join → informe byte-idéntico a hoy (sin auditor_join)."""
    sd = {"history": [{"line": "ls /srv", "result": {"exit_code": 0, "noise": [{"data": {"command": "ls", "amount": 1}}]}}], "total_noise": 1}
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_join" not in inf
    assert "auditor_join_text" not in inf
    assert len(inf["lines_resolved"]) == 1
    # sin imports sandbox
    import pathlib
    src = pathlib.Path("src/core/engine/postmortem.py").read_text(encoding="utf-8")
    assert "LINE_KEY_JOIN" in src
    # helper determinista
    assert _extract_join_args("join -v 1 a b") == {}
    assert _extract_join_args("ls /tmp") is None
