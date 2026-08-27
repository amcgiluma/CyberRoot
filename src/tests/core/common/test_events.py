"""test_events.py — especificación determinista del bus de eventos (DESIGN §4.5,
ARCHITECTURE §3, decisión §5.2).

Garantías bajo test:
- FIFO estricto por orden de suscripción dentro de un mismo tipo.
- Comodín (None) recibe TODOS los tipos; el orden global de notificación es el
  de suscripción, filtrando por tipo → un comodín intercalado se sitúa en su
  puesto exacto entre los handlers específicos.
- unsubscribe idempotente; comodín y específico son registros separados.
- Excepción de handler PROPAGA (fail-fast) y el bus sigue usable después.
- `data` es SNAPSHOT: mutar el dict original tras publish NO altera el Event.
- to_dict/from_dict ida-y-vuelta exacto (igualdad total incl. tick).
- ValueError si type vacío o no-str (publish y from_dict).
- Historial opcional: sin record_history → history() vacío; con k recorta.
- Doble suscripción del mismo handler → se dispara DOS veces.

Solo stdlib + pytest; sin `import random`.
"""

from __future__ import annotations

import pytest

from core.common.events import Event, EventBus, EventTypes


def _collect(order: list[str], label: str):
    """Factory de handler que anota su orden de llamada."""
    def handler(ev: Event) -> None:
        order.append(f"{label}:{ev.type}")
    return handler


# ----------------------------------------------------------------------------
# FIFO estricto por orden de suscripción dentro de un mismo tipo
# ----------------------------------------------------------------------------
def test_fifo_estricto_tres_subscriptores_mismo_tipo() -> None:
    bus = EventBus()
    order: list[str] = []
    h1 = _collect(order, "a")
    h2 = _collect(order, "b")
    h3 = _collect(order, "c")
    bus.subscribe(EventTypes.EXEC, h1)
    bus.subscribe(EventTypes.EXEC, h2)
    bus.subscribe(EventTypes.EXEC, h3)

    returned = bus.publish("event.exec", data={"n": 1})

    assert isinstance(returned, Event)
    assert order == ["a:event.exec", "b:event.exec", "c:event.exec"]


# ----------------------------------------------------------------------------
# Comodín: recibe todos los tipos; orden global = orden de suscripción filtrado
# ----------------------------------------------------------------------------
def test_comodin_recibe_todos_los_tipos() -> None:
    bus = EventBus()
    seen: list[str] = []
    bus.subscribe(None, _collect(seen, "wild"))

    bus.publish(EventTypes.EXEC)
    bus.publish(EventTypes.NOISE)
    bus.publish(EventTypes.TEXT)

    assert seen == ["wild:event.exec", "wild:event.noise", "wild:event.text"]


def test_orden_global_con_comodines_intercalados() -> None:
    """Suscripciones intercaladas → cada evento notifica en orden de
    suscripción filtrado por tipo. Un comodín en posición 2 se dispara tras el
    específico en posición 1 y antes del específico en posición 3."""
    bus = EventBus()
    order: list[str] = []
    h_spec_a = _collect(order, "exec-a")
    h_wild = _collect(order, "wild")
    h_spec_b = _collect(order, "exec-b")

    bus.subscribe(EventTypes.EXEC, h_spec_a)
    bus.subscribe(None, h_wild)               # comodín intercalado
    bus.subscribe(EventTypes.EXEC, h_spec_b)

    bus.publish(EventTypes.EXEC)
    # wild no filtra EXEC → entra en su puesto (posición 2 de suscripción)
    assert order == ["exec-a:event.exec", "wild:event.exec", "exec-b:event.exec"]

    order.clear()
    bus.publish(EventTypes.TEXT)
    # TEXT no lo escucha ningún específico, SOLO el comodín
    assert order == ["wild:event.text"]


# ----------------------------------------------------------------------------
# unsubscribe: idempotente; comodín y específico independientes
# ----------------------------------------------------------------------------
def test_unsubscribe_true_false_idempotente() -> None:
    bus = EventBus()
    h = _collect([], "x")
    bus.subscribe(EventTypes.EXEC, h)

    assert bus.unsubscribe(EventTypes.EXEC, h) is True
    assert bus.unsubscribe(EventTypes.EXEC, h) is False  # idempotente
    assert bus.unsubscribe(EventTypes.EXEC, h) is False


def test_unsub_no_recibe_mas() -> None:
    bus = EventBus()
    order: list[str] = []
    h1 = _collect(order, "stay")
    h2 = _collect(order, "go")
    bus.subscribe(EventTypes.EXEC, h1)
    bus.subscribe(EventTypes.EXEC, h2)
    bus.unsubscribe(EventTypes.EXEC, h1)

    bus.publish("event.exec")
    assert order == ["go:event.exec"]


def test_comodin_y_especifico_son_registros_separados() -> None:
    bus = EventBus()
    order: list[str] = []
    h = _collect(order, "h")
    bus.subscribe(EventTypes.EXEC, h)   # registro específico
    bus.subscribe(None, h)              # registro comodín SEPARADO

    # Quitar el específico no toca el comodín.
    assert bus.unsubscribe(EventTypes.EXEC, h) is True
    bus.publish("event.exec")
    assert order == ["h:event.exec"]    # solo el comodín quedaba

    order.clear()
    assert bus.unsubscribe(None, h) is True
    bus.publish("event.exec")
    assert order == []  # sin suscripciones


# ----------------------------------------------------------------------------
# Excepción de handler PROPAGA y el bus sigue usable
# ----------------------------------------------------------------------------
def test_excepcion_handler_propaga_y_bus_sigue_usable() -> None:
    bus = EventBus()
    boom_log: list[str] = []
    boom = _collect(boom_log, "boom")
    called = {"n": 0}

    def exploding(_ev: Event) -> None:
        called["n"] += 1
        if called["n"] == 1:
            raise RuntimeError("fail-fast dev")  # solo la primera invocación

    bus.subscribe(EventTypes.EXEC, boom)
    bus.subscribe(EventTypes.EXEC, exploding)
    bus.subscribe(EventTypes.EXEC, boom)

    with pytest.raises(RuntimeError, match="fail-fast"):
        bus.publish("event.exec")
    # boom se llamó UNA vez (la 2ª suscripción quedó interrumpida por la excepción)
    assert boom_log == ["boom:event.exec"]
    assert called["n"] == 1

    # El bus NO se rompe: un publish posterior notifica normal y no lanza.
    order: list[str] = []
    seen = _collect(order, "s")
    bus.subscribe(EventTypes.EXEC, seen)
    bus.publish("event.exec")
    assert called["n"] == 2          # exploding ya pasó de rosca
    assert order == ["s:event.exec"]  # se seen notificó en su puesto
    assert boom_log == ["boom:event.exec"] * 3  # 1 + 2 suscripciones restantes


# ----------------------------------------------------------------------------
# Snapshot de data
# ----------------------------------------------------------------------------
def test_snapshot_data_no_cambia_al_mutarlo_despues() -> None:
    bus = EventBus(record_history=10)
    original = {"x": 1, "y": [2]}  # copia superficial: el valor y:list se COMPARTE
    bus.publish("event.exec", data=original, tick=3)

    original["x"] = 999          # mutar tras publicar NO altera el snapshot
    original["nueva"] = "clave"  # añadir tampoco

    ev = bus.history()[0]
    assert ev.data["x"] == 1
    assert "nueva" not in ev.data


# ----------------------------------------------------------------------------
# to_dict / from_dict roundtrip total incl. tick
# ----------------------------------------------------------------------------
def test_to_from_dict_roundtrip_igualdad_total() -> None:
    ev = Event(type=EventTypes.EXEC, data={"hp": 10, "pos": [1, 2]}, tick=7)
    assert Event.from_dict(ev.to_dict()) == ev

    # Sin tick ni data → valores por defecto, roundtrip idéntico.
    bare = Event(type="event.noise")
    assert Event.from_dict(bare.to_dict()) == bare

    # to_dict devuelve copias: mutar el dict de salida no afecta al Event.
    d = ev.to_dict()
    d["data"]["hp"] = -1
    assert ev.data["hp"] == 10


def test_from_dict_data_none_o_ausente_es_dict_vacio() -> None:
    ev = Event.from_dict({"type": "event.exec", "tick": 2})
    assert ev.data == {}
    assert ev.tick == 2
    ev2 = Event.from_dict({"type": "event.exec", "data": None})
    assert ev2.data == {}


# ----------------------------------------------------------------------------
# ValueError en type vacío / no-str
# ----------------------------------------------------------------------------
def test_publish_type_vacio_o_no_str_raise_valueerror() -> None:
    bus = EventBus()
    with pytest.raises(ValueError):
        bus.publish("")
    # "   " es str NO vacío → VÁLIDO (contrato: type no-vacío, no "sin blancos")
    ok = bus.publish("   ")
    assert ok.type == "   "
    with pytest.raises(ValueError):
        bus.publish(123)  # type: ignore[arg-type]  # no-str
    with pytest.raises(ValueError):
        bus.publish(None)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        Event(type="")
    with pytest.raises(ValueError):
        Event(type=42)  # type: ignore[arg-type]


def test_from_dict_sin_type_o_type_no_str_raise_valueerror() -> None:
    with pytest.raises(ValueError):
        Event.from_dict({})
    with pytest.raises(ValueError):
        Event.from_dict({"data": {}})
    with pytest.raises(ValueError):
        Event.from_dict({"type": ""})   # str vacío rechazado igual
    with pytest.raises(ValueError):
        Event.from_dict({"type": 7})    # type: ignore[arg-type]
    with pytest.raises(ValueError):
        Event.from_dict(None)  # type: ignore[arg-type]


# ----------------------------------------------------------------------------
# Historial
# ----------------------------------------------------------------------------
def test_sin_record_history_history_siempre_vacio() -> None:
    bus = EventBus()  # por defecto NO guarda historial
    bus.publish("event.exec")
    bus.publish("event.text")
    assert bus.history() == ()


def test_record_history_maxlen_recorta_ultimos_k() -> None:
    bus = EventBus(record_history=3)
    for i in range(5):
        bus.publish("event.exec", data={"i": i}, tick=i)

    hist = bus.history()
    # últimos 3, antiguo→reciente
    assert [e.data["i"] for e in hist] == [2, 3, 4]
    assert [e.tick for e in hist] == [2, 3, 4]

    # limit recorta DESDE el final manteniendo orden antiguo→reciente
    assert [e.tick for e in bus.history(limit=2)] == [3, 4]
    assert bus.history(limit=0) == ()
    assert bus.history(limit=99) == hist


def test_clear_history() -> None:
    bus = EventBus(record_history=5)
    bus.publish("event.exec")
    bus.clear_history()
    assert bus.history() == ()
    bus.publish("event.text")
    assert [e.type for e in bus.history()] == ["event.text"]


# ----------------------------------------------------------------------------
# Doble suscripción del mismo handler → dispara dos veces
# ----------------------------------------------------------------------------
def test_mismo_handler_dos_veces_dispara_dos_veces() -> None:
    bus = EventBus()
    order: list[str] = []
    h = _collect(order, "h")
    bus.subscribe(EventTypes.EXEC, h)
    bus.subscribe(EventTypes.EXEC, h)  # doble suscripción (documentado)

    bus.publish("event.exec")
    assert order == ["h:event.exec", "h:event.exec"]

    # unsubscribe elimina UNA ocurrencia
    assert bus.unsubscribe(EventTypes.EXEC, h) is True
    order.clear()
    bus.publish("event.exec")
    assert order == ["h:event.exec"]  # queda la segunda
    assert bus.unsubscribe(EventTypes.EXEC, h) is True
    order.clear()
    bus.publish("event.exec")
    assert order == []


# ----------------------------------------------------------------------------
# publish acepta un Event ya construido (lo usa tal cual)
# ----------------------------------------------------------------------------
def test_publish_acepta_event_preconstruido() -> None:
    bus = EventBus(record_history=1)
    pre = Event(type=EventTypes.NOISE, data={"k": 1}, tick=5)
    order: list[str] = []
    bus.subscribe(None, _collect(order, "w"))
    returned = bus.publish(pre, data={"ignorado": True})  # kwargs ignorados
    assert returned is pre
    assert order == ["w:event.noise"]
    assert bus.history()[0] is pre


# ----------------------------------------------------------------------------
# Constantes del catálogo v0 (abierto §5.2)
# ----------------------------------------------------------------------------
def test_eventtypes_constantes_v0() -> None:
    assert EventTypes.EXEC == "event.exec"
    assert EventTypes.NOISE == "event.noise"
    assert EventTypes.TEXT == "event.text"
    # catálogo abierto: los tres son tipos distintos
    assert len({EventTypes.EXEC, EventTypes.NOISE, EventTypes.TEXT}) == 3


def test_subscribe_devuelve_handler_usable_como_decorador() -> None:
    bus = EventBus()
    order: list[str] = []

    @bus.subscribe(EventTypes.EXEC)
    def _h(ev: Event) -> None:
        order.append(ev.type)

    returned = bus.publish("event.exec")
    assert returned.type == "event.exec"
    assert order == ["event.exec"]