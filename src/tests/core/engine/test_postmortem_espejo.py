"""O1 13/09 — Eco del espejo v0: el Auditor nombra tu repertorio.

4 casos obligatorios:
- ① scp→cut|grep dispara espejo (volcado)
- ② join -v dispara espejo (testigos)
- ③ ps aux|grep dispara espejo (reloj)
- sin firma byte-idéntico (sin espejo)

Más 1 bonus: las 3 juntas en una sola línea determinista ①→②→③.
"""
from __future__ import annotations

from core.engine import build_postmortem
from core.engine.postmortem import LINE_KEY_ESPEJO, _has_espejo_reloj, _has_espejo_volcado
from data.textos import load_textos, resolve


def _sd(lines: list[str]) -> dict:
    return {
        "history": [
            {"line": l, "result": {"exit_code": 0, "noise": [{"data": {"command": l.split()[0] if l.split() else "?", "amount": 1}}]}}
            for l in lines
        ],
        "total_noise": len(lines),
    }


def test_espejo_scp_cut_grep_dispara_volcado():
    """Firma ①: scp a /tmp/volcado.csv seguido de cut|grep → espejo con 'copiaste el volcado'."""
    sd = _sd([
        "cat /etc/hosts",
        "scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv",
        "cut -d'|' -f1 /tmp/volcado.csv | grep TR-",
    ])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_espejo" in inf
    assert inf["auditor_espejo"]["line_key"] == LINE_KEY_ESPEJO
    assert "copiaste el volcado" in inf["auditor_espejo"]["args"]["huellas"]
    assert "copiaste el volcado" in inf["auditor_espejo_text"]
    assert inf["auditor_espejo_text"] != LINE_KEY_ESPEJO
    textos = load_textos()
    assert resolve(LINE_KEY_ESPEJO, inf["auditor_espejo"]["args"], textos) == inf["auditor_espejo_text"]
    assert inf["auditor_espejo_text"] in inf["lines_resolved"]
    # determinismo
    assert build_postmortem(sd, {"noise_budget": 12}) == inf
    # helpers
    assert _has_espejo_volcado(sd) is True
    # scp sin cut|grep no dispara
    sd2 = _sd(["scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv", "ls /tmp"])
    assert _has_espejo_volcado(sd2) is False
    assert "auditor_espejo" not in build_postmortem(sd2, {"noise_budget": 12})


def test_espejo_join_con_v_dispara_testigos():
    """Firma ②: join con -v → espejo con 'cruzaste dos testigos'."""
    sd = _sd(["join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv"])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_espejo" in inf
    assert "cruzaste dos testigos" in inf["auditor_espejo"]["args"]["huellas"]
    assert "cruzaste dos testigos" in inf["auditor_espejo_text"]
    # join también sigue disparando su propia línea auditor_join (no colisiona)
    assert "auditor_join" in inf
    # variante -v1
    sd2 = _sd(["join -t'|' -v1 /tmp/a /tmp/b"])
    assert "auditor_espejo" in build_postmortem(sd2, {"noise_budget": 12})


def test_espejo_ps_aux_grep_dispara_reloj():
    """Firma ③: ps aux | grep 11:04 → espejo con 'leíste el reloj'."""
    sd = _sd(["ps aux | grep 11:04"])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_espejo" in inf
    assert "leíste el reloj" in inf["auditor_espejo"]["args"]["huellas"]
    assert "leíste el reloj" in inf["auditor_espejo_text"]
    assert _has_espejo_reloj(sd) is True
    # variante sin aux pero con hora
    sd2 = _sd(["ps aux|grep 03:14"])
    assert "auditor_espejo" in build_postmortem(sd2, {"noise_budget": 12})
    # grep suelto sin ps no dispara
    sd3 = _sd(["grep 11:04 /tmp/foo"])
    assert _has_espejo_reloj(sd3) is False
    assert "auditor_espejo" not in build_postmortem(sd3, {"noise_budget": 12})


def test_espejo_sin_firma_byte_identico():
    """Sin ninguna firma → informe byte-idéntico a hoy (sin espejo)."""
    sd = _sd(["ls /srv", "cat /srv/camara-faro/purgas.csv"])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_espejo" not in inf
    assert "auditor_espejo_text" not in inf
    assert len(inf["lines_resolved"]) == 1  # solo pico/cruce
    # verifica que no hay huellas
    assert _has_espejo_volcado(sd) is False
    assert _has_espejo_reloj(sd) is False
    # sin imports sandbox
    import pathlib
    src = pathlib.Path("src/core/engine/postmortem.py").read_text(encoding="utf-8")
    assert "LINE_KEY_ESPEJO" in src
    import_lines = [l for l in src.splitlines() if l.strip().startswith("from ") or l.strip().startswith("import ")]
    assert not any("sandbox" in l for l in import_lines)


def test_espejo_las_tres_en_una_sola_linea_orden_determinista():
    """Con las 3 firmas, UNA sola línea enumerándolas en orden ①→②→③."""
    sd = _sd([
        "scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv",
        "cut -d'|' -f1 /tmp/volcado.csv | grep TR-",
        "join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv",
        "ps aux | grep 11:04",
    ])
    inf = build_postmortem(sd, {"noise_budget": 12})
    assert "auditor_espejo" in inf
    huellas = inf["auditor_espejo"]["args"]["huellas"]
    # orden ①→②→③
    assert huellas.index("copiaste el volcado") < huellas.index("cruzaste dos testigos") < huellas.index("leíste el reloj")
    assert huellas == "copiaste el volcado, cruzaste dos testigos y leíste el reloj"
    # solo UNA línea espejo
    assert sum(1 for k in inf if k.startswith("auditor_espejo")) == 2  # _ + _text
    assert inf["lines_resolved"].count(inf["auditor_espejo_text"]) == 1
    textos = load_textos()
    assert resolve(LINE_KEY_ESPEJO, {"huellas": huellas}, textos) == inf["auditor_espejo_text"]
