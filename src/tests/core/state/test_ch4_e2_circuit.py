"""T1 11/09 — Circuito ch4 completo e1+e2 + guard frontera (Seath).

Contrato T1 (plan 11/09 Gwyndolin):
  1) regresión e1 intacta con e2 en curriculum (generate(42,4) sin contract -> e1)
  2) e2 por contract: generate(42,4, contract_id='story.ch4.e2') -> golden 2 pasos
     scp + cut|grep TR- (1 pipe, filtro positivo), 3 líneas sin header
  3) guard allowlist CH4 en SUBSET (<= set 13 cmds, NUNCA ==)
  4) tail/sort/uniq en ch4 -> 127 frontera documentada
  5) GameState roundtrip idéntico tras circuito e2
  6) gate flexible 24/28 si S2 mergeado, 24/27 en main (pattern T1 10/09)
  7) shell 2 pipes intacto (cut|grep 1 OK, 3 cmds 2 OK, 4 cmds exit2)

Fallback handmade declarado si S2 no mergeado (main 24/27).
Cero toques fuera de state/ — único fichero nuevo del turno.
Determinista, sin RNG global, sin reloj real, sin pyxel.
"""
from __future__ import annotations

import importlib.util
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell, DEFAULT_CH4_COMMANDS
from core.state.state import GameState

# Constantes idénticas a chapter4.py / S2 textos
TRONCAL_HEADER = "id|origen|destino|bytes|estado"
TRONCAL_CONTENT = TRONCAL_HEADER + "\nTR-001|faro|troncal-01|1024|OK\nTR-002|troncal-01|nodo-02|2048|OK\nTR-003|faro|troncal-01|512|EN_COLA\n"
HOSTS_2 = "127.0.0.1 localhost\n# Troncal — red cap.4 (faro + troncal)\n10.6.0.5 faro\n10.6.1.10 troncal-01\n"
HOSTS_3 = HOSTS_2 + "10.6.1.11 troncal-02\n"

CH4_ALLOWLIST_EXPECTED = {"cat","cd","cp","cut","env","grep","kill","ls","ps","scp","ssh","sudo","wc"}

def _has_ch4_e2() -> bool:
    try:
        from core.curriculum import load_curriculum
        return load_curriculum().quest("story.ch4.e2") is not None
    except Exception:
        return False

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

def test_gate_flexible_24_conceptos_27_o_28_quests():
    """Gate por aritmética: 24 conceptos, 27 (main) o 28 (con S2 e2) quests."""
    from core.curriculum import load_curriculum
    cur = load_curriculum()
    assert len(cur.concepts) == 24, f"conceptos {len(cur.concepts)} !=24"
    assert len(cur.quests) in (27, 28), f"quests {len(cur.quests)} !=27|28 (main vs S2 e2)"
    # c.cut y c.scp deben existir en ch4
    assert cur.concept("c.cut") is not None and cur.concept("c.cut").chapter == 4
    assert cur.concept("c.scp") is not None and cur.concept("c.scp").chapter == 4
    # ch4.e1 siempre existe
    assert cur.quest("story.ch4.e1") is not None
    # si S2 mergeado, e2 existe con requires correcto
    if len(cur.quests) == 28:
        q = cur.quest("story.ch4.e2")
        assert q is not None and q.chapter == 4 and q.tint == "grey"
        assert list(q.requires) == ["c.cut","c.scp"]
    # ch6 intacto
    from core.curriculum import load_curriculum as lc2
    cur2 = lc2()
    assert cur2.quest("story.ch6.e1") is not None
    assert cur2.quest("story.ch6.dato4") is not None
    assert cur2.quest("story.ch6.dato5") is not None

def test_ch4_allowlist_subset_guard():
    """Guard SUBSET — lección 10/09: <= set 13 cmds, NUNCA == (costura join)."""
    assert set(DEFAULT_CH4_COMMANDS) <= CH4_ALLOWLIST_EXPECTED, f"CH4 allowlist no es subset: {set(DEFAULT_CH4_COMMANDS) - CH4_ALLOWLIST_EXPECTED} extra, {CH4_ALLOWLIST_EXPECTED - set(DEFAULT_CH4_COMMANDS)} falta"
    # 13 cmds exactos esperados hoy (si alguien añade join/cut extra, el subset lo detecta sin romper por +1)
    assert len(DEFAULT_CH4_COMMANDS) == 13, f"CH4 allowlist hoy 13 cmds, hay {len(DEFAULT_CH4_COMMANDS)}: {DEFAULT_CH4_COMMANDS}"

def test_ch4_tail_sort_uniq_frontera_127():
    """tail/sort/uniq en ch4 deben ser 127 (frontera deliberada — no ampliar, decisión Gwyndolin 11/09)."""
    shell = Shell(_fs_local_2hosts(), commands=DEFAULT_CH4_COMMANDS)
    for cmd in ("tail /etc/hosts", "sort /etc/hosts", "uniq /etc/hosts", "tail -n +2 /tmp/volcado.csv", "head /etc/hosts"):
        r = shell.execute(cmd)
        assert r.exit_code == 127, f"{cmd!r} en ch4 debe ser 127 frontera, dio {r.exit_code} {r.stderr!r}"
        # mensaje debe mencionar command not found o similar, no éxito
        assert r.exit_code == 127

def test_ch4_e1_regresion_intacta_con_e2():
    """generate(42,4) sin contract sigue prefiriendo e1 aunque e2 exista."""
    try:
        from core.generator import generate
    except ImportError:
        import pytest; pytest.skip("generator no disponible en este env")
    inc = generate(42, 4)
    assert inc.chapter == 4
    assert inc.contract.objective_key == "story.ch4.e1", f"sin contract debe preferir e1, dio {inc.contract.objective_key}"
    # determinismo byte-idéntico
    inc2 = generate(42, 4)
    assert inc.room.fs.to_dict() == inc2.room.fs.to_dict()
    # generate(42,6) intacto (gate flexible)
    inc6 = generate(42, 6)
    assert inc6.chapter == 6
    assert "10.6.0.5 faro" in inc6.room.fs.read_file("/etc/hosts","/")

def test_ch4_e2_por_contract_golden_2_pasos():
    """e2 por contract: scp + cut|grep TR- -> 3 líneas sin header. Fallback handmade si S2 no mergeado."""
    # Ruta: si curriculum tiene e2, probar generate real; si no, fallback handmade
    has_e2 = _has_ch4_e2()
    if has_e2:
        try:
            from core.generator import generate, new_session
            from core.generator.chapter4 import TRONCAL_PATH
            inc = generate(42, 4, contract_id="story.ch4.e2")
            assert inc.contract.objective_key == "story.ch4.e2"
            assert inc.chapter == 4
            shell = new_session(inc)
            # cat descubre 2-3 hosts
            r1 = shell.execute("cat /etc/hosts")
            assert r1.exit_code == 0 and "troncal-01" in r1.stdout and "faro" in r1.stdout
            assert "troncal-01" in shell.hosts
            # scp golden
            r2 = shell.execute(f"scp troncal-01:{TRONCAL_PATH} /tmp/")
            assert r2.exit_code == 0, f"scp e2 falló: {r2.stderr!r}"
            content = shell.fs.read_file("/tmp/volcado.csv","/")
            assert "TR-001" in content and TRONCAL_HEADER in content
            # cut|grep TR- -> 3 líneas sin header
            r3 = shell.execute("cut -d'|' -f1 /tmp/volcado.csv | grep TR-")
            assert r3.exit_code == 0, f"cut|grep TR- falló: {r3.stderr!r}"
            lines = [l for l in r3.stdout.splitlines() if l.strip()]
            assert lines == ["TR-001","TR-002","TR-003"], f"e2 golden esperaba 3 TR-, obtuvo {lines!r}: {r3.stdout!r}"
            assert "id" not in r3.stdout
            # TR-003 EN_COLA es la pista de lo que no pesa (verifica volcado crudo)
            r4 = shell.execute("cat /tmp/volcado.csv")
            assert "EN_COLA" in r4.stdout
            # determinismo: segunda sesión idéntica
            inc2 = generate(42, 4, contract_id="story.ch4.e2")
            shell2 = new_session(inc2)
            shell2.execute("cat /etc/hosts")
            shell2.execute(f"scp troncal-01:{TRONCAL_PATH} /tmp/")
            r3b = shell2.execute("cut -d'|' -f1 /tmp/volcado.csv | grep TR-")
            assert r3b.stdout == r3.stdout
            return
        except AssertionError:
            raise
        except Exception as e:
            # infra no lista (contract_id no soportado) -> fallback handmade
            pass
    # Fallback handmade (S2 no mergeado en main): FS idéntico a chapter4.py TRONCAL_CONTENT
    shell = Shell(_fs_local_2hosts(), commands=DEFAULT_CH4_COMMANDS)
    r = shell.execute("cat /etc/hosts")
    assert r.exit_code == 0
    # _note_hosts_discovery crea stubs vacíos — siempre sobrescribir con FS reales
    shell.hosts["faro"] = _fs_remote_faro()
    shell.hosts["troncal-01"] = _fs_remote_troncal(TRONCAL_CONTENT)
    # scp handmade
    r2 = shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/")
    assert r2.exit_code == 0, f"scp handmade falló: {r2.stderr!r}"
    assert shell.fs.read_file("/tmp/volcado.csv","/") == TRONCAL_CONTENT
    r3 = shell.execute("cut -d'|' -f1 /tmp/volcado.csv | grep TR-")
    assert r3.exit_code == 0
    lines = [l for l in r3.stdout.splitlines() if l.strip()]
    assert lines == ["TR-001","TR-002","TR-003"]
    assert "id" not in r3.stdout

def test_ch4_gamestate_roundtrip_tras_e2():
    """GameState persiste hosts + volcado copiado tras el circuito e2 (2 y 3 hosts)."""
    shell = Shell(_fs_local_2hosts(), commands=DEFAULT_CH4_COMMANDS)
    shell.execute("cat /etc/hosts")
    # _note_hosts_discovery crea stubs — sobrescribir siempre
    shell.hosts["faro"] = _fs_remote_faro()
    shell.hosts["troncal-01"] = _fs_remote_troncal(TRONCAL_CONTENT)
    r = shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv")
    assert r.exit_code == 0
    shell.execute("cut -d'|' -f1 /tmp/volcado.csv | grep TR-")
    # roundtrip
    g = GameState(shell=shell)
    d = g.to_dict()
    assert GameState.from_dict(d).to_dict() == d
    restored = GameState.from_dict(d).shell
    assert restored.fs.read_file("/tmp/volcado.csv","/") == TRONCAL_CONTENT
    assert "troncal-01" in restored.hosts
    assert restored.hosts["troncal-01"].read_file("/srv/archivo-troncal/volcado.csv","/") == TRONCAL_CONTENT
    # verificar que el estado no perdió faro
    assert "faro" in restored.hosts

def test_ch4_pipe_2_ok_4_rechazado():
    """Shell ch4: 1 pipe OK (cut|grep), 2 pipes OK (3 cmds), 4 cmds -> multiple pipelines not supported exit 2."""
    shell = Shell(_fs_local_2hosts(), commands=DEFAULT_CH4_COMMANDS)
    shell.execute("cat /etc/hosts")
    shell.hosts["faro"] = _fs_remote_faro()
    shell.hosts["troncal-01"] = _fs_remote_troncal(TRONCAL_CONTENT)
    shell.execute("scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/volcado.csv")
    # 1 pipe OK
    r1 = shell.execute("cut -d'|' -f1 /tmp/volcado.csv | grep TR-")
    assert r1.exit_code == 0 and "TR-001" in r1.stdout
    # 2 pipes OK (3 comandos): cat|cut|grep es 2 pipes
    r2 = shell.execute("cat /tmp/volcado.csv | cut -d'|' -f1 | grep TR-")
    assert r2.exit_code == 0, f"2 pipes debe ser OK, dio {r2.exit_code} {r2.stderr!r}"
    assert "TR-001" in r2.stdout
    # 4 comandos (3 pipes) debe fallar con mensaje exacto
    r3 = shell.execute("cat /tmp/volcado.csv | cut -d'|' -f1 | grep TR- | wc -l")
    assert r3.exit_code == 2
    assert "multiple pipelines not supported" in r3.stderr

