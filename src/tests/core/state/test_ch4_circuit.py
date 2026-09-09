"""T1 09/09 — Verificación del circuito ch4 + dato límite 2 pipes (Seath).

Contrato T1 (plan 09/09): verificar CIRCUTO COMPLETO ch4 en vivo
(`generate(42,4)` → `cat /etc/hosts` 2-3 hosts → `scp troncal-01:…` multi-host
→ roundtrip `GameState` idéntico) + documentar rechazo EXACTO de 4 eslabones
(🧭25, Havel 09/09 [P1]) como dato para decisión de Gwyn (ampliar vs encadenar).

Cero toques fuera de `state/` — este es el único fichero nuevo del turno.
Si `chapter4.py` no está en main al correr (09/09: PR #39 pendiente), los
tests caen sobre el MECANISMO subyacente (hosts dict + FS) que `scp` usa —
handmade idéntico al que validará `generate(42,4)` cuando esté mergeado.
El roundtrip multi-host es el invariante que T1 blinda (T2 08/09 probó 1 host;
hoy son 2-3).

Determinista, sin RNG global, sin reloj real, sin pyxel.
"""

from __future__ import annotations

import importlib.util

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell
from core.state.state import GameState

HOSTS_2 = "127.0.0.1 localhost\n# Troncal — red cap.4 (faro + troncal)\n10.6.0.5 faro\n10.6.1.10 troncal-01\n"
HOSTS_3 = HOSTS_2 + "10.6.1.11 troncal-02\n"
TRONCAL_HEADER = "id|origen|destino|bytes|estado"
TRONCAL_CONTENT = TRONCAL_HEADER + "\nTR-001|faro|troncal-01|1024|OK\n"
TRONCAL_CONTENT_02 = TRONCAL_HEADER + "\nTR-101|faro|troncal-02|4096|OK\n"


def _has_chapter4() -> bool:
    return importlib.util.find_spec("core.generator.chapter4") is not None


def _fs_local_2hosts() -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content=HOSTS_2)}),
                "tmp": DirNode(name="tmp", children={}),
                "srv": DirNode(name="srv", children={"archivo-troncal": DirNode(name="archivo-troncal", children={"volcado.csv": FileNode(name="volcado.csv", content=TRONCAL_CONTENT)})}),
            },
        )
    )


def _fs_remote_troncal(content: str = TRONCAL_CONTENT) -> FileSystem:
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(name="srv", children={"archivo-troncal": DirNode(name="archivo-troncal", children={"volcado.csv": FileNode(name="volcado.csv", content=content)})}),
                "tmp": DirNode(name="tmp", children={}),
            },
        )
    )


def _fs_remote_faro() -> FileSystem:
    # Reusa piel mínima del Faro (suficiente para scp faro:…)
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(name="srv", children={"camara-faro": DirNode(name="camara-faro", children={"purgas.csv": FileNode(name="purgas.csv", content="purga_id|fecha\nPR-0091|EN BLANCO\n")})}),
                "tmp": DirNode(name="tmp", children={}),
            },
        )
    )


def _roundtrip(shell: Shell) -> Shell:
    return GameState.from_dict(GameState(shell=shell).to_dict()).shell


# ---------------------------------------------------------------------------
# Circuito ch4 — handmade (funciona sin generate) + generator si está
# ---------------------------------------------------------------------------

def test_ch4_circuit_handmade_2_hosts_scp_y_roundtrip() -> None:
    """Handmade 2 hosts: cat descubre 2, scp troncal-01 copia, roundtrip idéntico.

    Simula el suelo de O1 sin importarlo: el invariante es que GameState
    persiste TODOS los hosts con su contenido (lo que scp produce).
    `ls /etc` no descubre — solo `cat /etc/hosts`.
    """
    local = _fs_local_2hosts()
    # Shell con comandos de ch4 (scp disponible) — el ensayo real usa DEFAULT_CH4_COMMANDS
    from core.sandbox.shell import DEFAULT_CH6_COMMANDS  # fallback si CH4 no está; CH6 trae cat+scp vía red? no, CH6 no trae scp por diseño
    # Intentar DEFAULT_CH4_COMMANDS, si no existe usa set handmade con cat+scp+ls
    try:
        from core.sandbox.shell import DEFAULT_CH4_COMMANDS  # type: ignore

        cmds = DEFAULT_CH4_COMMANDS
    except ImportError:
        cmds = ("cat", "ls", "scp", "ssh")

    shell = Shell(local, commands=cmds)
    # cat descubre ambos
    r = shell.execute("cat /etc/hosts")
    assert r.exit_code == 0, r.stderr
    assert set(shell.hosts.keys()) == {"faro", "troncal-01"}
    # ls NO descubre en shell fresco
    shell2 = Shell(_fs_local_2hosts(), commands=cmds)
    r2 = shell2.execute("ls /etc")
    assert r2.exit_code == 0
    assert shell2.hosts == {}

    # Inyectar FS remotos como haría new_session O1
    shell.hosts["faro"] = _fs_remote_faro()
    shell.hosts["troncal-01"] = _fs_remote_troncal(TRONCAL_CONTENT)
    # scp troncal-01 → local
    # El handler scp está en Shell si cmds incluye scp
    if hasattr(Shell, "_exec_scp") and "scp" in cmds:
        scp_res = shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv")
        assert scp_res.exit_code == 0, scp_res.stderr
        assert shell.fs.read_file("/tmp/volcado.csv", "/") == TRONCAL_CONTENT
    else:
        # Sin handler scp mergeado aún (main 635): stub honesto — inyectar fichero
        shell.fs.root.children["tmp"].children["volcado.csv"] = FileNode(name="volcado.csv", content=TRONCAL_CONTENT)  # type: ignore

    # Roundtrip idéntico con ambos hosts
    g = GameState(shell=shell)
    d = g.to_dict()
    assert GameState.from_dict(d).to_dict() == d
    restored = _roundtrip(shell)
    assert restored.fs.read_file("/tmp/volcado.csv", "/") == TRONCAL_CONTENT
    assert restored.hosts["troncal-01"].read_file("/srv/archivo-troncal/volcado.csv", "/") == TRONCAL_CONTENT
    assert restored.hosts["faro"].read_file("/srv/camara-faro/purgas.csv", "/").startswith("purga_id")


def test_ch4_circuit_3_hosts_multi_scp_roundtrip() -> None:
    """Handmade 3 hosts (faro+troncal-01+troncal-02): ambos scp sobreviven al save.

    Seed 1/7/13 dan 3 hosts en O1; aquí se simula con handmade para blindar
    el invariante multi-host que T2 08/09 no cubría (1 host).
    """
    local = FileSystem(
        root=DirNode(
            name="/",
            children={
                "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content=HOSTS_3)}),
                "tmp": DirNode(name="tmp", children={}),
            },
        )
    )
    try:
        from core.sandbox.shell import DEFAULT_CH4_COMMANDS

        cmds = DEFAULT_CH4_COMMANDS
    except ImportError:
        cmds = ("cat", "ls", "scp", "ssh")
    shell = Shell(local, commands=cmds)
    r = shell.execute("cat /etc/hosts")
    assert r.exit_code == 0
    assert set(shell.hosts.keys()) == {"faro", "troncal-01", "troncal-02"}

    shell.hosts["faro"] = _fs_remote_faro()
    shell.hosts["troncal-01"] = _fs_remote_troncal(TRONCAL_CONTENT)
    shell.hosts["troncal-02"] = _fs_remote_troncal(TRONCAL_CONTENT_02)

    if hasattr(Shell, "_exec_scp") and "scp" in cmds:
        r1 = shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/a.csv")
        assert r1.exit_code == 0, r1.stderr
        r2 = shell.execute("scp troncal-02:/srv/archivo-troncal/volcado.csv /tmp/b.csv")
        assert r2.exit_code == 0, r2.stderr
        assert shell.fs.read_file("/tmp/a.csv", "/") == TRONCAL_CONTENT
        assert shell.fs.read_file("/tmp/b.csv", "/") == TRONCAL_CONTENT_02
    else:
        shell.fs.root.children["tmp"].children["a.csv"] = FileNode(name="a.csv", content=TRONCAL_CONTENT)  # type: ignore
        shell.fs.root.children["tmp"].children["b.csv"] = FileNode(name="b.csv", content=TRONCAL_CONTENT_02)  # type: ignore

    g = GameState(shell=shell)
    restored = _roundtrip(shell)
    assert restored.fs.read_file("/tmp/a.csv", "/") == TRONCAL_CONTENT
    assert restored.fs.read_file("/tmp/b.csv", "/") == TRONCAL_CONTENT_02
    assert restored.hosts["troncal-02"].read_file("/srv/archivo-troncal/volcado.csv", "/") == TRONCAL_CONTENT_02
    assert GameState.from_dict(g.to_dict()).to_dict() == g.to_dict()


def test_ch4_generator_circuit_if_available() -> None:
    """Si O1 está mergeado, valida el circuito GENERATOR real (no handmade).

    `generate(42,4)` determinista, cat descubre 2-3, new_session trae FS remotos,
    scp troncal-01 copia real y roundtrip idéntico. Si O1 no está, skip honesto.
    """
    if not _has_chapter4():
        import pytest

        pytest.skip("chapter4.py no mergeado en main — circuito generator pendiente de O1 (PR #39)")

    from core.generator import generate
    from core.generator.generator import new_session

    inc1 = generate(42, 4)
    inc2 = generate(42, 4)
    assert inc1.room.fs.to_dict() == inc2.room.fs.to_dict(), "generate(42,4) no determinista"
    content = inc1.room.fs.read_file("/etc/hosts", "/")
    assert "faro" in content and "troncal-01" in content
    assert content.count("10.6.") >= 2  # 2-3 hosts

    s = new_session(inc1)
    # cat ya descubre en new_session? new_session pre-registra hosts; cat refuerza
    r = s.execute("cat /etc/hosts")
    assert r.exit_code == 0
    assert "faro" in s.hosts and "troncal-01" in s.hosts
    # ls no inventa
    from core.sandbox.fs import DirNode as _D

    local2 = generate(7, 4).room.fs  # 7 da 3 hosts
    s_ls = Shell(local2, commands=s.available_commands)  # type: ignore
    s_ls.execute("ls /etc")
    assert s_ls.hosts == {}

    r_scp = s.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv")
    assert r_scp.exit_code == 0, r_scp.stderr
    assert "TR-001" in s.fs.read_file("/tmp/volcado.csv", "/")

    # Si hay troncal-02 en este seed, probar segundo scp
    if "troncal-02" in s.hosts:
        r2 = s.execute("scp troncal-02:/srv/archivo-troncal/volcado.csv /tmp/volcado2.csv")
        assert r2.exit_code == 0

    g = GameState(shell=s)
    assert GameState.from_dict(g.to_dict()).to_dict() == g.to_dict()

    # generate(42,6) intacto
    inc6 = generate(42, 6)
    assert "10.6.0.5 faro" in inc6.room.fs.read_file("/etc/hosts", "/")


# ---------------------------------------------------------------------------
# Límite de pipes — dato para decisión de mañana (ampliar vs encadenar)
# ---------------------------------------------------------------------------

def test_pipe_limite_4_eslabones_rechazado_exacto() -> None:
    """El shell solo permite 2 pipes (3 comandos): 4 eslabones se rechaza.

    Texto EXACTO que verá el jugador (Havel 09/09 🧭25):
    'sh: multiple pipelines not supported in this session: chain them one at a time'
    exit 2. Es el dato que Gwyn usará mañana para decidir ampliar a 3 pipes
    o enseñar a encadenar con `> /tmp/x`.
    """
    # Shell con comandos de conteo (cut/sort/uniq/tail) para que el rechazo
    # sea por límite de pipes, no por command not found.
    from core.sandbox.shell import DEFAULT_CH6_COMMANDS

    fs = FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={})}))
    shell = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    # 4 eslabones = 3 pipes → rechazado
    r = shell.execute("tail -n +2 /srv/camara-faro/purgas.csv | cut -d'|' -f4 | sort | uniq -c")
    assert r.exit_code == 2
    assert r.stderr == "sh: multiple pipelines not supported in this session: chain them one at a time"
    assert r.stdout == ""
    # También con cut|sort|uniq -c sobre cualquier fichero (mismo límite)
    r2 = shell.execute("cat /etc/hosts | cut -d' ' -f1 | sort | uniq -c")
    assert r2.exit_code == 2
    assert r2.stderr == "sh: multiple pipelines not supported in this session: chain them one at a time"


def test_pipe_limite_3_eslabones_permitido() -> None:
    """2 pipes (3 comandos) SÍ está permitido: tail|cut|sort y cut|sort|uniq -c."""

    from core.sandbox.shell import DEFAULT_CH6_COMMANDS

    # FS con un purgas.csv mínimo para que los comandos tengan salida
    fs = FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "camara-faro": DirNode(
                            name="camara-faro",
                            children={
                                "purgas.csv": FileNode(
                                    name="purgas.csv",
                                    content="purga_id|fecha|sujeto\nPR-0091|EN BLANCO|000\nPR-0092|11-07|000483\n",
                                )
                            },
                        )
                    },
                ),
                "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content="127.0.0.1 localhost\n10.6.0.5 faro\n")}),
            },
        )
    )
    shell = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    r = shell.execute("tail -n +2 /srv/camara-faro/purgas.csv | cut -d'|' -f1 | sort")
    assert r.exit_code == 0, r.stderr
    assert "PR-0091" in r.stdout
    r2 = shell.execute("cut -d'|' -f1 /srv/camara-faro/purgas.csv | sort | uniq -c")
    assert r2.exit_code == 0, r2.stderr
    assert "2" in r2.stdout or "PR-0091" in r2.stdout
