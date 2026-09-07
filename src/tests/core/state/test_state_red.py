"""T2 07/09 — Persistencia del estado red (hosts/known_hosts) en el save.

Refuerzo del roundtrip que S1 07/09 (Smough, `_note_hosts_discovery`) produce:
el host DES-CUBIERTO con `cat /etc/hosts` y la caché `known_hosts` de la red
simulada deben sobrevivir ida y vuelta a través de `GameState.to_dict`/
`from_dict` (el save delega en `Shell.to_dict`/`from_dict` — ARCHITECTURE
§1.5). No se toca comportamiento: solo se blinda lo que S1 ya generaba.

Cubre (plan 07/09 §T2 y costura T↔S):
- host descubierto por lectura sobrevive al roundtrip, con su FS stub vacío,
  y relver no duplica (S1: solo se crea si no existía).
- `known_hosts` idéntico post-reload.
- sin `/etc/hosts`, `cat` falla GNU-honesto y el estado red sigue vacío.

Determinista: sin RNG global, sin reloj real, sin pyxel (ARCHITECTURE §1.5/§3).
"""

from __future__ import annotations

from core.sandbox.commands.red import fingerprint_for_host
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell
from core.state.state import GameState

HOSTS_CONTENT = "127.0.0.1 localhost\n10.0.0.1 faro\n"


def _fs_with_hosts() -> FileSystem:
    """FS local con `/etc/hosts` a dos nombres (localhost + faro)."""
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "etc": DirNode(
                    name="etc",
                    children={"hosts": FileNode(name="hosts", content=HOSTS_CONTENT)},
                )
            },
        )
    )


def _fs_without_hosts() -> FileSystem:
    """FS local SIN `/etc/hosts` (la lectura debe fallar GNU-honesto)."""
    return FileSystem(
        root=DirNode(name="/", children={"etc": DirNode(name="etc", children={})})
    )


def _roundtrip(shell: Shell) -> Shell:
    """Save/reload del estado completo; devuelve la Shell reconstruida."""
    return GameState.from_dict(GameState(shell=shell).to_dict()).shell


def test_roundtrip_hosts_discovered_via_cat() -> None:
    """El host des-cubierto por `cat /etc/hosts` sobrevive al save/reload.

    `faro` queda registrado como FS stub (raíz vacía), `known_hosts` sigue
    vacío (eso es del ssh), el roundtrip es byte-idéntico y un segundo `cat`
    sobre la copia restaurada NO duplica (S1 solo crea el host si no existe).
    """
    shell = Shell(_fs_with_hosts())
    res = shell.execute("cat /etc/hosts")
    assert res.exit_code == 0, res.stderr
    assert "faro" in shell.hosts
    # S1 descubre como stub: raíz `/` vacía.
    assert shell.hosts["faro"].to_dict()["root"]["children"] == {}
    assert shell.known_hosts == {}  # descubrir es leer, no ssh

    g = GameState(shell=shell)
    roundtrip = _roundtrip(shell)
    # Roundtrip EXACTO a nivel de dict serializado (determinismo §1.5).
    assert GameState.from_dict(g.to_dict()).to_dict() == g.to_dict()

    # El host des-cubierto vive en la copia con su FS stub idéntico.
    assert "faro" in roundtrip.hosts
    assert roundtrip.hosts["faro"].to_dict() == shell.hosts["faro"].to_dict()
    assert roundtrip.known_hosts == {}

    # Relver en la copia restaurada no duplica: la lectura vuelve a pasar por
    # el hook de S1 pero el host ya existe → se queda en 1.
    res2 = roundtrip.execute("cat /etc/hosts")
    assert res2.exit_code == 0, res2.stderr
    assert set(roundtrip.hosts) == {"faro"}


def test_roundtrip_known_hosts_persists() -> None:
    """La caché `known_hosts` (huella ED25519 determinista) viaja en el save.

    Se registra un host y su huella verificada; tras save/reload el `known_hosts`
    reconstruido es idéntico al original.
    """
    faro_fs = FileSystem(root=DirNode(name="/", children={}))
    shell = Shell(_fs_with_hosts(), commands=("cat", "ssh", "exit"))
    shell.register_host("faro", faro_fs)
    shell.known_hosts["faro"] = fingerprint_for_host("faro")

    g = GameState(shell=shell)
    assert g.to_dict()["shell"]["known_hosts"] == {
        "faro": fingerprint_for_host("faro")
    }

    roundtrip = _roundtrip(shell)
    assert roundtrip.hosts["faro"].to_dict() == faro_fs.to_dict()
    assert roundtrip.known_hosts == {"faro": fingerprint_for_host("faro")}
    assert GameState.from_dict(g.to_dict()).to_dict() == g.to_dict()


def test_roundtrip_hosts_empty_without_file() -> None:
    """Sin `/etc/hosts` la lectura falla y el estado red queda vacío tras reload.

    Un save tomado ANTES de descubrir nada reconstruye con `hosts` y
    `known_hosts` vacíos (nada se inventa en el viaje de ida y vuelta).
    """
    shell = Shell(_fs_without_hosts())
    res = shell.execute("cat /etc/hosts")
    assert res.exit_code == 1
    assert "No such file or directory" in res.stderr
    assert shell.hosts == {}
    assert shell.known_hosts == {}

    g = GameState(shell=shell)
    roundtrip = _roundtrip(shell)
    assert roundtrip.hosts == {}
    assert roundtrip.known_hosts == {}
    assert GameState.from_dict(g.to_dict()).to_dict() == g.to_dict()