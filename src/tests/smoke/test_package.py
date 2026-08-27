"""smoke — el paquete core.common importa y expone su API mínima."""

from core.common import Rng, Event, EventBus


def test_smoke_imports() -> None:
    rng = Rng(1)
    assert isinstance(rng.uint64(), int)
    bus = EventBus()
    seen = []
    bus.subscribe("event.exec", lambda e: seen.append(e))
    ev = bus.publish("event.exec", data={"argv": ["ls"]})
    assert seen == [ev]
