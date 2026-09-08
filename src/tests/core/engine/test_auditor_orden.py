"""O1 06/09 — Tests faltantes `auditor_orden` (+4, higiene) — REPOSICIÓN 08/09.

Los 4 casos exactos de la deuda Artorias 06/09 en abierto.md:
- sort -k12 con/sin -t/-n/long opts cita columna/delimitador/numérico
- sort sin -k no dispara (E2 golden intacto)
- cut -f4 | sort -k12 dispara ambas (corte+orden, 3 líneas)
- determinismo y sin imports sandbox

REGLA: SOLO tests — postmortem.py/textos.json INTACTOS.
"""
from __future__ import annotations

from core.engine.postmortem import LINE_KEY_ORDEN
from core.engine import build_postmortem
from core.engine.postmortem import _extract_sort_args
from data.textos import load_textos, resolve


def _sd_sort(line: str) -> dict:
    return {
        "history": [{"line": line, "result": {"exit_code": 0, "noise": [{"data": {"command": "sort", "amount": 1}}]}}],
        "total_noise": 1,
    }

def _sd_both_cut_and_sort(cut_line: str, sort_line: str) -> dict:
    return {
        "history": [
            {"line": cut_line, "result": {"exit_code": 0, "noise": [{"data": {"command": "cut", "amount": 1}}]}},
            {"line": sort_line, "result": {"exit_code": 0, "noise": [{"data": {"command": "sort", "amount": 1}}]}},
        ],
        "total_noise": 2,
    }


def test_orden_con_k_variantes_cita_columna_delimitador_numerico():
    """sort -k12 con/sin -t/-n/long opts → auditor_orden con columna/delimitador/numérico."""
    textos = load_textos()
    # -k12 simple (sin -t, sin -n)
    sd1 = _sd_sort("sort -k12 /srv/camara-faro/purgas.csv")
    inf1 = build_postmortem(sd1, {"noise_budget": 12})
    assert "auditor_orden" in inf1
    assert inf1["auditor_orden"]["args"]["columna"] == "12"
    assert inf1["auditor_orden"]["args"]["delimitador"] == ""
    assert inf1["auditor_orden"]["args"]["numerico"] == "no numérico"
    assert inf1["auditor_orden"]["line_key"] == LINE_KEY_ORDEN
    assert resolve(LINE_KEY_ORDEN, inf1["auditor_orden"]["args"], textos) == inf1["auditor_orden_text"]

    # -t '|' -k12
    sd2 = _sd_sort("sort -t '|' -k12 -n /srv/camara-faro/purgas.csv")
    inf2 = build_postmortem(sd2, {"noise_budget": 12})
    assert inf2["auditor_orden"]["args"]["columna"] == "12"
    assert inf2["auditor_orden"]["args"]["delimitador"] == "|"
    assert inf2["auditor_orden"]["args"]["numerico"] == "numérico"

    # long opts --field-separator='|' --key=12 --numeric-sort
    sd3 = _sd_sort("sort --field-separator='|' --key=12 --numeric-sort /srv/camara-faro/purgas.csv")
    inf3 = build_postmortem(sd3, {"noise_budget": 12})
    assert inf3["auditor_orden"]["args"]["columna"] == "12"
    assert inf3["auditor_orden"]["args"]["delimitador"] == "|"
    assert inf3["auditor_orden"]["args"]["numerico"] == "numérico"

    # -k12.2, -t con long --delimiter
    sd4 = _sd_sort("sort -t'|' -k12.2 /srv/camara-faro/purgas.csv")
    inf4 = build_postmortem(sd4, {"noise_budget": 12})
    assert inf4["auditor_orden"]["args"]["columna"] == "12"
    assert inf4["auditor_orden"]["args"]["delimitador"] == "|"


def test_orden_sin_k_no_dispara_golden_e2_intacto():
    """sort sin -k no dispara orden (golden E2 dato2 = cut|sort|uniq -c sin -k)."""
    sd = _sd_sort("sort /srv/camara-faro/purgas.csv")
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_orden" not in inf
    assert "auditor_orden_text" not in inf
    assert len(inf["lines_resolved"]) == 1  # solo pico/cruce, sin orden

    # E2 golden real: cut -d'|' -f4 | sort | uniq -c  →  sort sin -k, solo corte
    sd_e2 = {
        "history": [{"line": "cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c", "result": {"exit_code": 0, "noise": [{"data": {"command": "cut", "amount": 1}}]}}],
        "total_noise": 1,
    }
    inf_e2 = build_postmortem(sd_e2, {"noise_budget": 12})
    assert "auditor_corte" in inf_e2
    assert "auditor_orden" not in inf_e2
    assert len(inf_e2["lines_resolved"]) == 2  # pico + corte, sin orden


def test_orden_y_corte_juntos_tres_lineas():
    """cut -f4 | sort -k12 dispara ambas (corte+orden, 3 líneas)."""
    sd = {
        "history": [{"line": "cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort -t'|' -k12 -n /srv/camara-faro/purgas.csv", "result": {"exit_code": 0, "noise": [{"data": {"command": "cut", "amount": 1}}]}}],
        "total_noise": 1,
    }
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_corte" in inf
    assert "auditor_orden" in inf
    assert len(inf["lines_resolved"]) == 3
    # orden cita 12/|/numérico
    assert inf["auditor_orden"]["args"]["columna"] == "12"
    assert inf["auditor_orden"]["args"]["delimitador"] == "|"
    assert inf["auditor_orden"]["args"]["numerico"] == "numérico"
    # corte cita 4/|
    assert inf["auditor_corte"]["args"]["column"] == "4"
    # textos resuelven
    textos = load_textos()
    assert resolve(inf["auditor_orden"]["line_key"], inf["auditor_orden"]["args"], textos) == inf["auditor_orden_text"]
    assert resolve(inf["auditor_corte"]["line_key"], inf["auditor_corte"]["args"], textos) == inf["auditor_corte_text"]


def test_orden_determinismo_y_sin_imports_sandbox():
    """Determinismo y sin imports de sandbox (solo engine + data)."""
    sd = _sd_sort("sort -t '|' -k12 -n /srv/camara-faro/purgas.csv | head -n 3")
    inf1 = build_postmortem(sd, {"noise_budget": 12})
    inf2 = build_postmortem(sd, {"noise_budget": 12})
    assert inf1 == inf2
    # Sin imports sandbox: el fichero no importa core.sandbox (solo engine + data)
    import pathlib
    p = pathlib.Path(__file__).read_text(encoding="utf-8")
    import_lines = [l for l in p.splitlines() if l.strip().startswith("from ") or l.strip().startswith("import ")]
    assert not any("sandbox" in l for l in import_lines)
    # extract helper también determinista y sin sandbox
    assert _extract_sort_args("sort -k12 foo") is not None
    assert _extract_sort_args("sort foo") is None
