"""escalada.py — `sudo` GANADO: elevación con credencial NARRATIVA (cap. 3).

Materializa la forma FIRMADA de Gwyn (DESIGN §6.1, S1 del plan 01/09): el
`sudo` NO es una contraseña tecleada, es una CREDENCIAL narrativa que el juego
GANA (la colocan O1/generator en el FS de la sala como fichero del mundo, y se
lee con `cat`). La ejecución es un wrapper de orquestación del SHELL (necesita
el registry de la sesión para despachar el comando envuelto); aquí viven las
constantes de contrato, el chequeo de credencial, el rechazo diegético y la
firma de `auth.log`.

═══ CONTRATO O1↔S1 (literales compartidos, sin import) ══════════════════════
O1 (`feat/engine`, chapter3.py) colocó en la sala sudo del cap. 3 la credencial
en `SUDO_CREDENTIAL_PATH` y el `auth.log` en `AUTH_LOG_PATH`. El sandbox los
lee por ESTOS mismos literales (copiados aquí); NO importa del generator
(dependencia prohibida, ARCHITECTURE §2). Si una ruta cambia, cambia AQUÍ y en
la rama de Ornstein A LA VEZ; Artorias verifica la coincidencia en el gate.
═══════════════════════════════════════════════════════════════════════════

Forma operativa (v1):
- sin credencial        → rechazo diegético accionable que NOMBRA qué falta y
                          dónde vive; exit 1, ruido 0 (intentar no es delinquir).
- credencial SIN LEER    → rechazo diegético que NOMBRA la orden y manda
                          leerla (`cat <ruta>`); exit 1, ruido 0, SIN firma
                          en `auth.log` (S1, 03/09: el sudo se GANA LEYENDO).
- credencial LEÍDA (`cat` en la sesión, marca en el estado serializable) →
                          ejecuta el comando envuelto, factura ruido PREMIUM
                          (extra sobre el precio base del comando) y deja FIRMA
                          en `auth.log` (usuario, comando, tick): el poder deja
                          factura — la lección llega por la columna USER de `ps`.
"""

from __future__ import annotations

from core.sandbox.fs import FileSystem, FsError
from core.sandbox.noise import NOISE_PROFILE

SUDO_NAME = "sudo"

# --- CONTRATO O1↔S1 (literales compartidos; ver cabecera) ------------------

#: Ruta ABSOLUTA de la credencial narrativa en el FS de la sala sudo del cap. 3.
SUDO_CREDENTIAL_PATH = "/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt"

#: Marcador de contenido que identifica la credencial (método «contenido +
#: ruta» del plan O1/S1). La credencial de O1 incluye esta línea.
SUDO_AUTHZ_MARKER = "AUTORIZACION: CENIZA"

#: Ruta ABSOLUTA del `auth.log` donde sudo firma cada elevación.
AUTH_LOG_PATH = "/var/log/auth.log"

#: Ruido PREMIUM de `sudo` (⚠️ v1, calibra harness): el poder deja factura.
#: Se SUMA al precio base del comando envuelto. Fuente única de verdad:
#: `NOISE_PROFILE["sudo"]` en noise.py (constante documentada para el gate de
#: Artorias y la calibración de O2/O3).
SUDO_PREMIUM_NOISE = NOISE_PROFILE["sudo"]


def check_credential(fs: FileSystem, cwd: str) -> bool:
    """True si la credencial narrativa existe y contiene el marcador.

    Comprueba primero la ruta convencional (`SUDO_CREDENTIAL_PATH`) y luego el
    contenido (`SUDO_AUTHZ_MARKER`). Un fichero en la ruta sin el marcador (p.
    ej. una orden falsa o revocada) NO autoriza: la lección honesta de la forma
    §6.1 es que la llave se gana, no se adivina por el sitio.
    """
    try:
        content = fs.read_file(SUDO_CREDENTIAL_PATH, cwd)
    except FsError:
        return False
    return SUDO_AUTHZ_MARKER in content


#: Mensaje diegético del rechazo sin credencial. NOMBRA qué falta y dónde vive
#: (accionable, DESIGN §6.1) con voz de Linux real en inglés (§2.6.8). La
#: lección del post-mortem la completa el Auditor; aquí basta la puerta útil.
SUDO_NO_CRED_MSG = (
    "sudo: elevation denied: an authorization order is required.\n"
    f"Find it and read it (it names your scope): 'cat {SUDO_CREDENTIAL_PATH}'"
)


#: Mensaje diegético del rechazo con credencial SIN LEER (S1, 03/09, 🧭14b).
#: NOMBRA la orden por su ruta y manda leerla: la llave se gana, no se
#: adivina por el sitio. Voz de Linux real en inglés (§2.6.8); exit 1,
#: ruido 0, sin firma en `auth.log`.
SUDO_UNREAD_MSG = (
    "sudo: elevation denied: you have not read Ceniza's order.\n"
    f"Read it first (it names your scope): 'cat {SUDO_CREDENTIAL_PATH}'"
)

#: Tipo del evento que el shell publica en su bus cuando el jugador LEE la
#: credencial con `cat` (S1, 03/09). Prefijo canónico `event.` (contrato de
#: `common.events.EventTypes`, catálogo abierto §5.2): cuando el engine lo
#: consuma, la constante promociona allí; el sandbox NO toca `common/`
#: (es de Ornstein) y publica por este literal compartido.
SUDO_READ_EVENT_TYPE = "event.credential.read"


def signature_line(user: str, cmd: str, argv: tuple[str, ...], tick: int) -> str:
    """Línea de firma appenda al `auth.log` (usuario, comando, tick).

    `tick {tick} {user} : sudo {cmd} {args...}` — tiempo = tick simulado (no
    hay reloj real, §2.2); comando = el envuelto, para que el Auditor lea qué
    se ejecutó con la llave («el poder deja factura»).
    """
    args = f" {' '.join(argv)}" if argv else ""
    return f"tick {tick} {user} : sudo {cmd}{args}\n"