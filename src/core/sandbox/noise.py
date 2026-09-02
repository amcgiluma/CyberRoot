"""noise.py — contabilidad de ruido por acción (ARCHITECTURE §2.2, DESIGN §7.2).

Cada comando emite un evento de ruido; el coste de DETECCIÓN (% que sube,
tramos) lo decide el ENGINE, no el sandbox (§2.2: «aquí solo se emite»).
Constantes ⚠️ v1 calibrables sin tocar lógica.

Los eventos SON `core.common.events.Event` (canje S1, 28/08: PR #1 mergeada —
deuda del 27/08 saldada). El tipo canónico es `EventTypes.NOISE`; la constante
local `NOISE_EVENT_TYPE` se mantiene por compatibilidad con lectores previos.
Prohibido `random`: el ruido es determinista por comando.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.common.events import Event, EventTypes

#: Tipo canónico compartido con `common.events.EventTypes.NOISE` (iguales por
#: contrato; el canje S1 usa la constante de common como fuente de verdad).
NOISE_EVENT_TYPE = EventTypes.NOISE

#: Ruido base por comando ⚠️ v1 (calibra harness). `cd` no cruza el sistema
#: (ruido 0); leer es barato; copiar datos toca el fichero dos veces (más
#: ruido). El engine convierte cantidad→detección según el anillo (§6.0.2).
NOISE_PROFILE: dict[str, int] = {
    "cd": 0,
    "ls": 1,
    "cat": 1,
    "cp": 3,
    # S1 (30/08): `grep` cruza el fichero patrón por patrón (más caro que un
    # `cat`), `wc` cuenta sobre lo que llega (tubería incluida). ⚠️ v1
    # calibrables con el harness (O3 de Ornstein).
    "grep": 2,
    "wc": 1,
    # S1 (31/08): `ps` y `env` son LECTURA, como `ls`/`cat` — observar no
    # perturba (DESIGN §7.2: el ruido viene de la acción, no de la mirada).
    # ⚠️ v1 calibrables con el harness.
    "ps": 1,
    "env": 1,
    # S1 (01/09): `sudo` = poder. El ruido PREMIUM se SUMA al del comando
    # envuelto (el wrapper emite SOLO este extra; el base ya lo emite el
    # comando). «El poder deja factura» (DESIGN §6.1). ⚠️ v1 calibrable.
    "sudo": 3,
    # S2 (01/09): familia conteo — «lectura frugal» (DESIGN, S2 del plan):
    # head/tail/sort/uniq leen MENOS que un `cat` entero (menos ruido por la
    # misma información). sort cruza el fichero entero + ordena (más caro que
    # un `wc`); uniq colapsa adyacentes. ⚠️ v1 calibrables con el harness.
    "head": 1,
    "tail": 1,
    "sort": 2,
    "uniq": 1,
    # S1 (02/09): `kill` — matar/reiniciar procesos es disruptivo (más que
    # listar, menos que copiar con sudo). El coste de detección lo decide el
    # engine; aquí solo se emite. ⚠️ v1 calibrable con harness.
    "kill": 2,
}


@dataclass(frozen=True)
class NoiseMeter:
    """Acumulador de ruido de la sesión + emisor de eventos.

    Inmutable por diseño: cada `emit`/`accumulate` devuelve instancia NUEVA,
    coherente con datos de juego sin mutación compartida.
    """

    total: int = 0

    def emit(self, command: str, argv: tuple[str, ...], tick: int) -> Event:
        """Devuelve el evento de ruido del comando SIN mutar nada.

        Comandos sin entrada en el perfil emiten ruido 0 (comando no
        reconocido aún puede dibujar atención: eso lo decide el engine con
        el exit 127). El payload viaja con SNAPSHOT de `argv` (Event hace
        copia superficial del Mapping: mutar la tupla/dict original después
        de emitir no altera el evento).
        """
        amount = NOISE_PROFILE.get(command, 0)
        return Event(
            type=NOISE_EVENT_TYPE,
            data={"command": command, "amount": amount, "argv": list(argv)},
            tick=tick,
        )

    def accumulate(self, command: str) -> "NoiseMeter":
        """Suma al total el ruido del comando y devuelve meter nuevo."""
        return NoiseMeter(total=self.total + NOISE_PROFILE.get(command, 0))
