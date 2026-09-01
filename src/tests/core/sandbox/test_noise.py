"""Tests de noise.py (H1b): perfil de ruido y forma de evento.

Canje S1 (28/08): los eventos SON `core.common.events.Event` reales —
la forma anterior (dicts planos) era el puente mientras PR #1 no estaba
mergeada. El contrato JSON-plano se verifica vía `Event.to_dict()`.
"""

from __future__ import annotations

from core.common.events import Event
from core.common.types import ensure_plain
from core.sandbox.noise import NOISE_EVENT_TYPE, NOISE_PROFILE, NoiseMeter


def test_perfil_contiene_los_comandos_del_cap0_y_pipes() -> None:
    # Cap. 0 (cat/cd/cp/ls) + cap. 2 (grep/wc, S1 30/08) + cap. 3 (ps/env, 31/08;
    # sudo, S1 01/09) + familia conteo (head/tail/sort/uniq, S2 01/09).
    assert set(NOISE_PROFILE) == {
        "cd", "ls", "cat", "cp", "grep", "wc", "ps", "env", "sudo",
        "head", "tail", "sort", "uniq",
    }


def test_cd_no_hace_ruido_y_cp_es_el_mas_ruidoso() -> None:
    assert NOISE_PROFILE["cd"] == 0
    assert NOISE_PROFILE["cp"] > NOISE_PROFILE["grep"] > NOISE_PROFILE["ls"] == NOISE_PROFILE["cat"] == NOISE_PROFILE["wc"]


def test_emit_devuelve_forma_event_snapshot() -> None:
    meter = NoiseMeter()
    ev = meter.emit("cp", ("a.txt", "b.txt"), tick=7)
    assert isinstance(ev, Event)
    assert ev.type == NOISE_EVENT_TYPE == "event.noise"
    assert ev.data == {"command": "cp", "amount": 3, "argv": ["a.txt", "b.txt"]}
    assert ev.tick == 7
    # Snapshot: mutar argv original no altera el evento (coherente con Event).
    argv = ["a.txt", "b.txt"]
    ev2 = meter.emit("cp", tuple(argv), tick=0)
    argv.append("intruso")
    assert ev2.data["argv"] == ["a.txt", "b.txt"]


def test_emit_comando_desconocido_emite_ruido_cero() -> None:
    ev = NoiseMeter().emit("frobnicate", (), tick=1)
    assert ev.data["amount"] == 0


def test_accumulate_devuelve_instancia_nueva_sin_mutar() -> None:
    m0 = NoiseMeter()
    m1 = m0.accumulate("ls")
    m2 = m1.accumulate("cp")
    assert (m0.total, m1.total, m2.total) == (0, 1, 4)
    assert m0 is not m1 is not m2


def test_determinismo_ante_misma_entrada() -> None:
    a = NoiseMeter().emit("cat", ("x",), tick=3)
    b = NoiseMeter().emit("cat", ("x",), tick=3)
    assert a == b


def test_emit_event_roundtrip_json_plano() -> None:
    """Canje S1: el Event serializa a JSON estricto y vuelve idéntico.

    Es el contrato que consume la frontera (ensure_plain de common) y el
    roundtrip de CommandResult: `from_dict(to_dict()) == original`.
    """
    ev = NoiseMeter().emit("cp", ("s", "d"), tick=2)
    d = ev.to_dict()
    ensure_plain(d)
    assert Event.from_dict(d) == ev


def test_tipo_canonico_es_el_de_common() -> None:
    """La constante local ES `EventTypes.NOISE` (una sola fuente de verdad)."""
    from core.common.events import EventTypes

    assert NOISE_EVENT_TYPE == EventTypes.NOISE
