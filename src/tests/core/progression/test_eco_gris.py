"""O1 14/09 — Gris reconoce: `progression` dice qué copiaste (mitad Gris de la 🧭9/P1 13/09).

Tras completar `story.ch4.e2` con `scp → cut|grep TR-` limpio, Gris dice UNA
línea diegética `hub.gris.volcado`. Señal mínima desde el save (history del
shell); fallback honesto si `resumen_competencia` no da para más — aquí usamos
directamente el gesto en history (no dependemos de mastered ni de engine).

Criterio del plan: 3–4 tests (con gesto → línea de Gris; sin gesto → byte-idéntico;
determinismo; no colisión). Suite 708 → ≥711.

Prefijo `hub.gris.*` disjunto de `postmortem.espejo.*` y `postmortem.auditor.*`.
No toca engine/postmortem.py.
"""
from __future__ import annotations

from core.progression import GRIS_VOLCADO_KEY, gris_eco, gris_linea
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell
from core.state import GameState


TRONCAL_CONTENT = "id|origen|destino|bytes|estado\nTR-001|faro|troncal-01|1024|OK\nTR-002|troncal-01|nodo-02|2048|OK\nTR-003|faro|troncal-01|512|EN_COLA\n"
HOSTS_2 = "127.0.0.1 localhost\n# Troncal — red cap.4 (faro + troncal)\n10.6.0.5 faro\n10.6.1.10 troncal-01\n"


def _fs_local_2hosts() -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={
        "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content=HOSTS_2)}),
        "tmp": DirNode(name="tmp", children={}),
        "srv": DirNode(name="srv", children={}),
    }))


def _fs_remote_troncal(content: str = TRONCAL_CONTENT) -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={
        "srv": DirNode(name="srv", children={"archivo-troncal": DirNode(name="archivo-troncal", children={"volcado.csv": FileNode(name="volcado.csv", content=content)})}),
        "tmp": DirNode(name="tmp", children={}),
        "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content="127.0.0.1 localhost\n")}),
    }))


def _fs_remote_faro() -> FileSystem:
    return FileSystem(root=DirNode(name="/", children={
        "srv": DirNode(name="srv", children={"camara-faro": DirNode(name="camara-faro", children={"purgas.csv": FileNode(name="purgas.csv", content="purga_id|fecha\nPR-0091|EN BLANCO\n")})}),
        "tmp": DirNode(name="tmp", children={}),
        "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content="127.0.0.1 localhost\n")}),
    }))


def _shell_con_gesto() -> Shell:
    shell = Shell(_fs_local_2hosts(), host="troncal", commands=("cat","cut","grep","scp","ls"))
    shell.execute("cat /etc/hosts")
    shell.hosts["faro"] = _fs_remote_faro()
    shell.hosts["troncal-01"] = _fs_remote_troncal(TRONCAL_CONTENT)
    r = shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/")
    assert r.exit_code == 0, r.stderr
    r2 = shell.execute("cut -d'|' -f1 /tmp/volcado.csv | grep TR-")
    assert r2.exit_code == 0
    assert "TR-001" in r2.stdout
    return shell


def _shell_sin_gesto() -> Shell:
    # Solo scp sin cut|grep, o shell vacío
    shell = Shell(_fs_local_2hosts(), host="troncal", commands=("cat","cut","grep","scp","ls"))
    shell.execute("cat /etc/hosts")
    shell.hosts["troncal-01"] = _fs_remote_troncal(TRONCAL_CONTENT)
    shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/")
    # no hace el cut|grep -> no gesto completo
    return shell


def test_gris_con_gesto_devuelve_linea():
    st = GameState(shell=_shell_con_gesto())
    eco = gris_eco(st)
    assert eco is not None
    assert eco["line_key"] == GRIS_VOLCADO_KEY == "hub.gris.volcado"
    assert "512 bytes" in eco["text"] and "03:14" in eco["text"]
    assert "Copiaste el volcado que no pesa" in eco["text"]
    # prefijo disjunto
    assert not eco["line_key"].startswith("postmortem.")


def test_gris_sin_gesto_byte_identico_none():
    st = GameState(shell=_shell_sin_gesto())
    assert gris_eco(st) is None
    assert gris_linea(st) is None
    # shell vacía también None
    st2 = GameState(shell=Shell(FileSystem(root=DirNode(name="/"))))
    assert gris_eco(st2) is None


def test_gris_determinismo():
    s1 = GameState(shell=_shell_con_gesto())
    s2 = GameState(shell=_shell_con_gesto())
    assert gris_eco(s1) == gris_eco(s2)
    assert gris_linea(s1) == gris_linea(s2)
    # con y sin gesto no colisiona
    s3 = GameState(shell=_shell_sin_gesto())
    assert gris_eco(s1) != gris_eco(s3)


def test_gris_texto_resuelve_desde_data():
    """El texto viene de data/textos.json y contiene la voz de Gris (mercado)."""
    from data.textos import resolve
    esperado = resolve(GRIS_VOLCADO_KEY, {})
    st = GameState(shell=_shell_con_gesto())
    assert gris_eco(st)["text"] == esperado
    assert "Gris" in esperado or "mesa" in esperado or "precio" in esperado
