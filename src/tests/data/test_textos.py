"""test_textos.py — cobertura de claves de texto (T1, 01/09, Seath, 🧭12).

Garantiza la promesa de T1: «toda clave emitida por el post-mortem y toda
quest ch1 resuelve a texto (falla si falta una)». Es el pegamento entre el
tubo (el engine emite `line_key`+`args` en `postmortem.auditor.*`) y los
datos (`textos.json`) — el eco 🧭9 se SIENTE cuando toda clave que emite un
sistema tiene texto detrás.

Cobertura:
1. Las claves que emite `build_postmortem` (`LINE_KEY_CRUCE`, `LINE_KEY_PICO`)
   existen en `textos.json` y resuelven con los `args` reales que produce
   `build_postmortem` (command/amount/total_noise/noise_budget).
2. TODA quest del currículo real (ch1 + ch5, las que T1/T2 integran) tiene su
   `title_key` y `beat_key` resolviendo a texto NO vacío.

Y en negativo, el resolvedor (`data/textos.py`): clave ausente → error
accionable; placeholder sin arg → error accionable (romper mejor que mostrar
un hueco `{...}`); estructura de textos.json invalidada → error.

Solo stdlib + pytest; cero I/O de red.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.curriculum.loader import load_curriculum
from core.engine.postmortem import LINE_KEY_CRUCE, LINE_KEY_PICO, build_postmortem
from data.textos import TextResolutionError, load_textos, resolve

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"


# ----------------------------------------------------------------------------
# 1. Post-mortem: las claves que emite el motor resuelven con args reales
# ----------------------------------------------------------------------------
def _postmortem_shell() -> dict:
    """Un historial mínimo que cruza el presupuesto (amount altos) → cruce.

    `build_postmortem` devuelve `auditor.line_key` y `auditor.args` concretos:
    este test simula lo que el Hub recibirá y resuelve la clave contra data/.
    """
    hist = [
        {
            "line": "ps -ef",
            "result": {
                "exit_code": 0,
                "noise": [{"tipo": "command", "data": {"command": "ps", "amount": 4}}],
            },
        },
        {
            "line": "env",
            "result": {
                "exit_code": 0,
                "noise": [{"tipo": "command", "data": {"command": "env", "amount": 9}}],
            },
        },
    ]
    return {"history": hist, "total_noise": 13}


def test_ambas_claves_auditor_resuelven_con_args_del_motor() -> None:
    """LINE_KEY_CRUCE y LINE_KEY_PICO están en textos.json y resuelven con los
    args (command/amount/...) que el motor puebla en `build_postmortem`."""
    textos = load_textos()
    # Fuerza un cruce: acumulado 4+9=13 ≥ noise_budget 12 → cruce.
    post = build_postmortem(_postmortem_shell(), {"noise_budget": 12})
    assert post["auditor"]["line_key"] == LINE_KEY_CRUCE
    args = post["auditor"]["args"]
    for key in (LINE_KEY_CRUCE, LINE_KEY_PICO):
        t = resolve(key, args, textos)
        assert isinstance(t, str) and t.strip()
        # El arg más distintivo (command) aparece poblado en el texto.
        assert args["command"] in t


def test_auditor_no_cruce_usa_pico_y_resuelve() -> None:
    """Sin cruce (amounts bajos), el motor emite el pico; la clave resuelve."""
    hist = [{
        "line": "cat nota",
        "result": {
            "exit_code": 0,
            "noise": [{"tipo": "command", "data": {"command": "cat", "amount": 2}}],
        },
    }]
    post = build_postmortem({"history": hist, "total_noise": 2}, {"noise_budget": 12})
    assert post["auditor"]["line_key"] == LINE_KEY_PICO
    t = resolve(post["auditor"]["line_key"], post["auditor"]["args"])
    assert t and "cat" in t


# ----------------------------------------------------------------------------
# 2. Currículo: toda quest ch1 Y ch5 tiene title/beat resuelto y no vacío
# ----------------------------------------------------------------------------
def test_todas_las_quests_del_curriculo_resuelven_a_texto() -> None:
    """Cobertura total de claves: TODA quest (ch1 integrada en T1 y ch5 en T2)
    tiene `title_key` y `beat_key` en textos.json resolviendo a texto no vacío.

    Falla si falta una clave: una quest sin texto visible sería un hueco que
    el render no sabría pintar. Se recorre el currículo real (fuente única).
    """
    cur = load_curriculum()
    textos = load_textos()
    for chapter in (1, 5):
        quests = cur.quests_for_chapter(chapter)
        assert quests, f"cap. {chapter} sin quests"
        for q in quests:
            title = resolve(q.title_key, textos=textos)
            assert title.strip(), f"{q.id}: title_key {q.title_key!r} vacío"
            if q.beat_key:
                beat = resolve(q.beat_key, textos=textos)
                assert beat.strip(), f"{q.id}: beat_key {q.beat_key!r} vacío"


def test_ninguna_clave_del_ficharo_queda_huerfana() -> None:
    """Todo title/beat_key del currículo integrable (ch1/ch5) existe en data/.
    Es el otro lado de la cobertura: también en negativo por si se añade una
    quest y se olvida su texto (el test de arriba ya falla, este lo localiza)."""
    cur = load_curriculum()
    textos = load_textos()
    for q in cur.quests_for_chapter(1) + cur.quests_for_chapter(5):
        assert q.title_key in textos
        if q.beat_key:
            assert q.beat_key in textos


# ----------------------------------------------------------------------------
# NEGATIVO — resolvedor robusto (romper claro, no mostrar {..})
# ----------------------------------------------------------------------------
def test_resolve_clave_ausente_lanza_accionable() -> None:
    textos = {"a.b": "hola"}
    with pytest.raises(TextResolutionError, match="ausente"):
        resolve("a.c", textos=textos)


def test_resolve_placeholder_sin_arg_lanza_accionable() -> None:
    textos = {"a.b": "hola {command}"}
    with pytest.raises(TextResolutionError, match="placeholder"):
        resolve("a.b", {}, textos)


def test_load_textos_fichero_sin_texts_rechazado(tmp_path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"version": 1}), encoding="utf-8")
    with pytest.raises(TextResolutionError, match="texts"):
        load_textos(bad)


def test_load_textos_json_roto_rechazado(tmp_path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{no json", encoding="utf-8")
    with pytest.raises(TextResolutionError, match="JSON"):
        load_textos(bad)


def test_load_textos_texts_no_dict_rechazado(tmp_path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"texts": ["x"]}), encoding="utf-8")
    with pytest.raises(TextResolutionError, match="objeto"):
        load_textos(bad)


def test_fichero_real_resuelve_sin_args_para_claves_simples() -> None:
    """Las claves sin placeholder (títulos/beats) resuelven con `resolve()`
    sin pasar args — el path más común del render."""
    t = load_textos()
    assert resolve("story.ch1.e1.title", textos=t) == "El turno de la señora Carmen"
    assert "escuela pública 3" in resolve("story.ch1.e1.beat", textos=t)


def test_briefing_ch6_e1_con_rutas_absolutas() -> None:
    """T2 (03/09, Seath, 🧭15): `story.ch6.e1` resuelve a prosa con voz de
    encargo y rutas absolutas `/srv/camara-faro/…` — el jugador no tropieza
    con el 0-mentiroso POR RUTA. Sin placeholders (resuelve sin args)."""
    t = load_textos()
    assert resolve("story.ch6.e1.title", textos=t) == "El número que sobra"
    beat = resolve("story.ch6.e1.beat", textos=t)
    assert "/srv/camara-faro/" in beat
    assert "/srv/camara-faro/censo-borrador.csv" in beat
    assert "PR-0091" in beat and "ENSAYO" in beat
