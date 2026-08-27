"""noise.py — contabilidad de ruido por acción (ARCHITECTURE §2.2, DESIGN §7.2).

Cada comando emite un evento de ruido; el coste de DETECCIÓN (% que sube,
tramos) lo decide el ENGINE, no el sandbox (§2.2: «aquí solo se emite»).
Constantes ⚠️ v1 calibrables sin tocar lógica.

Forma del evento: dict plano {type, data, tick} IDÉNTICA a
`core.common.events.Event` de Ornstein (PR #1 aún no mergeada: viajo con
dicts y el canje a la clase real es una importación — PLAN.md decisión 4).
Prohibido `random`: el ruido es determinista por comando.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Tipo canónico compartido con common.events.EventTypes.NOISE (feat/engine).
NOISE_EVENT_TYPE = "event.noise"

#: Ruido base por comando ⚠️ v1 (calibra harness). `cd` no cruza el sistema
#: (ruido 0); leer es barato; copiar datos toca el fichero dos veces (más
#: ruido). El engine convierte cantidad→detección según el anillo (§6.0.2).
NOISE_PROFILE: dict[str, int] = {
    "cd": 0,
    "ls": 1,
    "cat": 1,
    "cp": 3,
}


@dataclass(frozen=True)
class NoiseMeter:
    """Acumulador de ruido de la sesión + emisor de eventos.

    Inmutable por diseño: cada `emit`/`accumulate` devuelve instancia NUEVA,
    coherente con datos de juego sin mutación compartida.
    """

    total: int = 0

    def emit(self, command: str, argv: tuple[str, ...], tick: int) -> dict:
        """Devuelve el evento de ruido del comando (forma Event) SIN mutar.

        Comandos sin entrada en el perfil emiten ruido 0 (comando no
        reconocido aún puede dibujar atención: eso lo decide el engine con
        el exit 127).
        """
        amount = NOISE_PROFILE.get(command, 0)
        return {
            "type": NOISE_EVENT_TYPE,
            "data": {"command": command, "amount": amount, "argv": list(argv)},
            "tick": tick,
        }

    def accumulate(self, command: str) -> "NoiseMeter":
        """Suma al total el ruido del comando y devuelve meter nuevo."""
        return NoiseMeter(total=self.total + NOISE_PROFILE.get(command, 0))
