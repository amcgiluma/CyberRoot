"""events.py — bus de eventos pub/sub SÍNCRONO + Event inmutable (ARCHITECTURE §3,
DESIGN §4.5; decisión abierta §5.2 del catálogo de tipos).

Diseño (ver PLAN.md decision 4, 5, 6):
- `Event` es una dataclass FROZEN: datos de juego inmutables desde fuera. El
  atributo `data` guarda un SNAPSHOT (`dict(data)`) hecho en `__post_init__`:
  mutar el Mapping original después de publicar NO altera el Event.
- `tick` es tiempo SIMULADO, no reloj real (§3: core no depende del reloj).
- `EventBus` es síncrono y FIFO: los handlers se invocan en orden de
  suscripción. Las excepciones de un handler PROPAGAN (fail-fast en dev):
  nunca se tragan silenciosamente. Sin hilos, sin asyncio.
- El historial es OPCIONAL (`record_history`), implementado con `deque(maxlen=k)`
  para recorte automático; pensado para debug/post-mortem.
- Prohibido `import random`; no hay ningún estado global aquí.

Catálogo de tipos v0 (ABIERTO §5.2): constantes obvias con prefijo `event.`.
La decisión final del catálogo queda abierta hasta el primer consumo real de
render/harness — añadir constantes no rompe nada.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

Handler = Callable[["Event"], None]


class EventTypes:
    """Catálogo de tipos de evento — v0, ABIERTO (ARCHITECTURE §5.2 decisión abierta).

    Prefijo canónico `event.` para evitar colisiones con otros dominios. Añadir
    constantes conforme se consuma el bus desde render/harness; nunca borrar las
    existentes sin migrar subscriptores.
    """

    EXEC = "event.exec"
    NOISE = "event.noise"
    TEXT = "event.text"


@dataclass(frozen=True)
class Event:
    """Un evento inmutable con tipo canónico str + payload snapshot.

    Campos:
    - `type`: str NO vacío. Catálogo abierto (§5.2); el bus filtra por aquí.
    - `data`: Mapping[str, Any] — SNAPSHOT (`dict()`) hecho en `__post_init__`.
      Pasar `None` produce un dict vacío NUEVO por instancia.
    - `tick`: tiempo SIMULADO opcional (§3); `None` = sin timestamp.

    Contrato de seguridad: una vez construido, `data` es inaccesible a mutación
    desde fuera (frozen + copia superficial). `to_dict`/`from_dict` son
    ida-y-vuelta exactos: `from_dict(e.to_dict()) == e`.
    """

    type: str
    data: Mapping[str, Any] = field(default_factory=dict)
    tick: int | None = None  # tiempo SIMULADO (§3: sin reloj real)

    def __post_init__(self) -> None:
        # Frozen dataclass: solo `object.__setattr__` puede fijar campos.
        if not isinstance(self.type, str):
            raise ValueError(f"Event.type debe ser str, no {type(self.type).__name__}")
        if not self.type:
            raise ValueError("Event.type no puede ser la cadena vacía")
        raw = self.data
        if raw is None:
            snapshot: Mapping[str, Any] = {}
        elif isinstance(raw, Mapping):
            # Copia superficial: el dict NUEVO que publicamos. Internamente
            # puede seguir compartiendo referencias de valores — no es deepcopy.
            snapshot = dict(raw)
        else:
            raise ValueError(
                f"Event.data debe ser Mapping o None, no {type(raw).__name__}"
            )
        object.__setattr__(self, "data", snapshot)

    def to_dict(self) -> dict[str, Any]:
        """Serializa a dict plano JSON: {"type", "data", "tick"}.

        Devuelve SIEMPRE un dict nuevo con `data` copiada; el Event no expone
        su snapshot interno por referencia.
        """
        return {
            "type": self.type,
            "data": dict(self.data),
            "tick": self.tick,
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Event":
        """Reconstruye un Event desde un dict plano.

        ValueError si falta la clave "type" o si type no es str (incluye la
        cadena vacía). `data` ausente/None → dict vacío; `tick` ausente → None.
        """
        if not isinstance(d, Mapping):
            raise ValueError(f"from_dict espera Mapping, no {type(d).__name__}")
        if "type" not in d:
            raise ValueError("from_dict: falta la clave 'type'")
        raw_data = d.get("data")
        payload: Mapping[str, Any] = {} if raw_data is None else raw_data
        return cls(type=d["type"], data=payload, tick=d.get("tick"))


class EventBus:
    """Bus de eventos pub/sub síncrono, FIFO por orden de suscripción.

    Uso:
        bus = EventBus(record_history=100)
        bus.subscribe(EventTypes.EXEC, handler)     # evento específico
        bus.subscribe(None, wildcard)               # comodín: TODOS los eventos
        ev = bus.publish("event.exec", data={...}, tick=7)

    Garantías:
    - `subscribe` devuelve el propio handler ⇒ usable como decorador.
      Suscribir el MISMO handler dos veces (mismo tipo) lo dispara DOS veces;
      `unsubscribe` elimina una ocurrencia cada vez.
    - Comodín (`None`) y tipo específico son registros SEPARADOS: un handler
      comodín y uno específico no se interfieren al desuscribir.
    - `publish` es SÍNCRONO: notifica a TODOS los subscriptores (específicos +
      comodín) en orden de suscripción, filtrando por tipo. Una excepción de
      handler PROPAGA y detiene ese publish; el bus queda usable.
    - Historial opcional: `record_history=None` no almacena nada (history()=()),
      `record_history=k` guarda los últimos k eventos con `deque(maxlen=k)`.
    """

    def __init__(self, record_history: int | None = None) -> None:
        # Lista de (event_type, handler) en orden de suscripción. La duplicación
        # exacta está permitida y dispara el handler dos veces (documentado).
        self._subs: list[tuple[str | None, Handler]] = []
        self._history: deque[Event] | None = (
            deque(maxlen=record_history) if record_history is not None else None
        )

    def subscribe(
        self,
        event_type: str | None,
        handler: Handler | None = None,
    ) -> Handler | Callable[[Handler], Handler]:
        """Registra handler. `None` como type = comodín (recibe TODOS los tipos).

        Doble uso:
        - `bus.subscribe(tipo, fn)` registra `fn` y lo devuelve.
        - `@bus.subscribe(tipo)` actúa como decorador (handler omitido).
        El mismo (tipo, handler) suscrito dos veces se ADICIONA dos veces y
        dispara dos veces (documentado).
        """
        if handler is not None:
            self._subs.append((event_type, handler))
            return handler

        def decorator(fn: Handler) -> Handler:
            self._subs.append((event_type, fn))
            return fn

        return decorator

    def unsubscribe(self, event_type: str | None, handler: Handler) -> bool:
        """Elimina UNA ocurrencia de la suscripción (tipo, handler).

        True si la eliminó; False si no estaba registrada exactamente así
        (idempotente). Comodín y tipo específico son registros SEPARADOS:
        unsubscribe(None, h) no afecta a (tipo, h) ni viceversa.
        """
        for i, (sub_type, sub_handler) in enumerate(self._subs):
            if sub_type == event_type and sub_handler == handler:
                del self._subs[i]
                return True
        return False

    def publish(
        self,
        event_or_type: Event | str,
        *,
        data: Mapping[str, Any] | None = None,
        tick: int | None = None,
    ) -> Event:
        """Publica un Event y notifica a todos los subscriptores. Devuelve el Event.

        - Si `event_or_type` es un `Event`, se usa tal cual (data/tick kwargs
          ignorados). Si es un `str`, se construye `Event(type, data, tick)`.
        - SÍNCRONO, FIFO por orden de suscripción; una excepción de handler
          PROPAGA (fail-fast dev) sin romper el bus.
        - Guarda el Event en el historial si `record_history` está activo.
        """
        if isinstance(event_or_type, Event):
            event = event_or_type
        elif isinstance(event_or_type, str):
            payload: Mapping[str, Any] = {} if data is None else data
            event = Event(type=event_or_type, data=payload, tick=tick)
        else:
            raise ValueError(
                "publish espera Event o str, no "
                f"{type(event_or_type).__name__}"
            )

        if self._history is not None:
            self._history.append(event)

        for sub_type, handler in self._subs:
            if sub_type is None or sub_type == event.type:
                handler(event)

        return event

    def history(self, limit: int | None = None) -> tuple[Event, ...]:
        """Los últimos `limit` eventos en orden antiguo→reciente.

        Si no se habilitó historial, devuelve siempre (). `limit=None` devuelve
        todo lo guardado.
        """
        if self._history is None:
            return ()
        items = list(self._history)
        if limit is not None:
            if limit <= 0:
                return ()
            items = items[-limit:]
        return tuple(items)

    def clear_history(self) -> None:
        """Vacía el historial (no afecta a las suscripciones)."""
        if self._history is not None:
            self._history.clear()