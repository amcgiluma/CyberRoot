"""red.py — familia Red: `ssh` / `exit` / `logout` (ARCHITECTURE §2.2, DESIGN §6.1).

Red simulada mínima para cap. 4+ (pieza 1, 06/09): hosts como FS simultáneos
del mismo Shell. `ssh [user@]host` cambia el FS activo; `exit`/`logout`
des-apila. Sin sockets reales jamás. Primera conexión a host desconocido →
prompt host-key GNU-honesto (OpenSSH) con huella determinista por host.
"""

from __future__ import annotations

import base64
import hashlib

from core.sandbox.commands.base import CommandSpec
from core.sandbox.noise import NOISE_PROFILE

SSH_NAME = "ssh"
SCP_NAME = "scp"
EXIT_NAME = "exit"
LOGOUT_NAME = "logout"


def fingerprint_for_host(host: str) -> str:
    """Huella determinista ED25519 por host (SHA256:base64 sin padding).

    Determinista por host: dos shells con el mismo host generan la misma
    huella; hosts distintos generan huella distinta. Usa SHA256 del nombre
    (sin seed externa hoy; el contrato dice determinista por seed — esta
    forma es estable y cumple: el generator es determinista por seed y el
    nombre del host lo fija el generator; si mañana la seed influye, se añade
    como sufijo aquí sin romper la API).
    """
    digest = hashlib.sha256(host.encode("utf-8")).digest()
    b64 = base64.b64encode(digest).decode("ascii").rstrip("=")
    return f"SHA256:{b64}"


def host_key_prompt(host: str, fingerprint: str) -> str:
    """Mensaje host-key forma OpenSSH exacta (plan S1 06/09)."""
    return (
        f"The authenticity of host '{host}' can't be established.\n"
        f"ED25519 key fingerprint is {fingerprint}.\n"
        f"Are you sure you want to continue connecting (yes/no/[fingerprint])? "
    )


def _run_ssh_placeholder(fs, cwd, argv, tick, stdin=""):
    """Placeholder para registro — el Shell intercepta ssh real (wrapper)."""
    from core.sandbox.commands.base import CommandResult

    return CommandResult(stderr="ssh: placeholder", exit_code=1)


def _run_exit_placeholder(fs, cwd, argv, tick, stdin=""):
    from core.sandbox.commands.base import CommandResult

    return CommandResult(stderr="exit: placeholder", exit_code=0)

def _run_scp_placeholder(fs, cwd, argv, tick, stdin=""):
    from core.sandbox.commands.base import CommandResult

    return CommandResult(stderr="scp: placeholder", exit_code=1)


SCP_SPEC = CommandSpec(
    name=SCP_NAME,
    concepts=frozenset({"scp"}),
    noise=NOISE_PROFILE[SCP_NAME],
    run=_run_scp_placeholder,
)

SSH_SPEC = CommandSpec(
    name=SSH_NAME,
    concepts=frozenset({"ssh"}),
    noise=NOISE_PROFILE[SSH_NAME],
    run=_run_ssh_placeholder,
)

EXIT_SPEC = CommandSpec(
    name=EXIT_NAME,
    concepts=frozenset({"exit"}),
    noise=NOISE_PROFILE[EXIT_NAME],
    run=_run_exit_placeholder,
)

LOGOUT_SPEC = CommandSpec(
    name=LOGOUT_NAME,
    concepts=frozenset({"exit"}),
    noise=NOISE_PROFILE[LOGOUT_NAME],
    run=_run_exit_placeholder,
)

SPECS: tuple[CommandSpec, ...] = (SSH_SPEC, SCP_SPEC, EXIT_SPEC, LOGOUT_SPEC)
