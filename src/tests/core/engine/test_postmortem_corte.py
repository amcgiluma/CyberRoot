"""O1 05/09 — El Auditor cita TU columna: postmortem.auditor.corte

Criterio del plan:
- Run con cut -d'|' -f4 en history → informe con línea de corte, forma formulario, cita columna/patrón, nunca clave cruda.
- Run SIN cut → informe byte-idéntico (sin nueva línea)
- Determinista, sin imports sandbox
"""
from __future__ import annotations

from core.engine import LINE_KEY_CORTE, build_postmortem
from core.engine.postmortem import _extract_cut_args, _find_cut
from data.textos import load_textos, resolve


def _sd_cut(line: str) -> dict:
    return {
        "history": [{"line": line, "result": {"exit_code": 0, "noise": [{"data": {"command": "cut", "amount": 1}}]}}],
        "total_noise": 1,
    }


def test_corte_con_cut_cita_columna_y_pattern():
    """Con cut -d'|' -f4 → auditor_corte con column f4, texto resuelto sin clave cruda."""
    sd = _sd_cut("cut -d'|' -f4 /srv/camara-faro/purgas.csv")
    informe = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_corte" in informe
    ac = informe["auditor_corte"]
    assert ac["line_key"] == LINE_KEY_CORTE
    assert ac["args"]["column"] == "4"
    assert ac["args"]["pattern"] == "|"
    # Texto resuelto no es clave cruda y contiene columna
    assert informe["auditor_corte_text"] != LINE_KEY_CORTE
    assert "4" in informe["auditor_corte_text"]
    # Verifica contra textos.json
    textos = load_textos()
    assert resolve(LINE_KEY_CORTE, ac["args"], textos) == informe["auditor_corte_text"]
    assert len(informe["lines_resolved"]) == 2
    # Determinista
    assert build_postmortem(sd, {"noise_budget": 12}) == informe


def test_corte_sin_cut_byte_identico():
    """Sin cut → sin auditor_corte, lines_resolved 1 (no rompe tríada lector)."""
    sd = {"history": [{"line": "ls /srv", "result": {"exit_code": 0, "noise": [{"data": {"command": "ls", "amount": 1}}]}}], "total_noise": 1}
    informe = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_corte" not in informe
    assert "auditor_corte_text" not in informe
    assert len(informe["lines_resolved"]) == 1


def test_corte_multi_pipe_y_rango_y_ciega_idempotencia():
    """cut en pipe y rango f4,12 → cita; con sudo+corte → 3 líneas deterministas."""
    # multi-pipe
    sd_pipe = {"history": [{"line": "cut -d'|' -f4 /srv/camara-faro/purgas.csv | sort | uniq -c", "result": {"exit_code": 0, "noise": [{"data": {"command": "cut", "amount": 1}}]}}], "total_noise": 1}
    inf_pipe = build_postmortem(sd_pipe, {"noise_budget": 12})
    assert inf_pipe["auditor_corte"]["args"]["column"] == "4"
    # rango
    sd_range = _sd_cut("cut -d'|' -f4,12 /srv/camara-faro/purgas.csv")
    inf_range = build_postmortem(sd_range, {"noise_budget": 12})
    assert inf_range["auditor_corte"]["args"]["column"] == "4,12"
    # idempotencia con lectura: cut + sudo → 3 líneas
    sd_both = {
        "history": [
            {"line": "cut -d'|' -f4 foo", "result": {"exit_code": 0, "noise": [{"data": {"command": "cut", "amount": 1}}]}},
            {"line": "sudo cat /etc/hosts", "result": {"exit_code": 1, "noise": [{"data": {"command": "sudo", "amount": 3}}]}},
        ],
        "total_noise": 4,
        "read_marks": [],
    }
    inf_both = build_postmortem(sd_both, {"noise_budget": 12})
    assert "auditor_corte" in inf_both and "auditor_lectura" in inf_both
    assert len(inf_both["lines_resolved"]) == 3
    assert build_postmortem(sd_both, {"noise_budget": 12}) == inf_both


def test_extract_cut_args_edge_cases():
    """_extract_cut_args sin flag → None; con flags combinados → detecta."""
    assert _extract_cut_args("cut /tmp/foo") is None
    assert _extract_cut_args("ls /srv") is None
    assert _extract_cut_args("cut -d'|' -f4 foo") is not None
    assert _extract_cut_args("cut --delimiter='|' --fields=4 foo") is not None
    # shlex inválido no crashea
    assert _extract_cut_args("cut -d'|' -f4") is not None  # sin fichero sigue siendo flag
