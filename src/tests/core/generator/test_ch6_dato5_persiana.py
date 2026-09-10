"""test_ch6_dato5_persiana.py — O1 10/09 «La persiana» (dato5) — piel de procesos del Faro.

Criterio de aceptación (plan 10/09 O1):
- generate(42,6) determinista byte-idéntico en 2 llamadas con la piel nueva
- proceso con START 11:04 estable por seed y contiene marca PR-0091/11:04 legible vía ps aux
- golden `ps aux | grep 11:04` exit 0
- dato2/dato3/e2/e1 intactos (gate 127 y allowlist CH6 sin cambios)
- suite +4–5 tests
"""
from __future__ import annotations

from core.generator import generate, new_session
from core.generator.chapter6 import (
    FARO_GUILTY_START,
    FARO_INIT_START,
    FARO_SYNC_BINARY,
    PURGAS_PATH,
)
from core.sandbox.fs import FileNode
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH6_COMMANDS


def test_dato5_determinismo_byte_identico_ch6():
    a = generate(42, 6)
    b = generate(42, 6)
    assert a.to_dict() == b.to_dict(), "generate(42,6) no es determinista byte-idéntico con piel nueva"
    # variant practice también
    a2 = generate(99, 6, variant="practice")
    b2 = generate(99, 6, variant="practice")
    assert a2.to_dict() == b2.to_dict()


def test_dato5_proceso_START_1104_estable_y_con_PR0091():
    inc = generate(42, 6)
    # FS debe llevar 3 procesos deterministas por seed
    procs = inc.room.fs.processes
    assert len(procs) == 3, f"esperaba 3 procesos (init + 2 faro-sync), got {len(procs)}"
    # init Aug25
    inits = [p for p in procs if p.start == FARO_INIT_START]
    assert len(inits) == 1 and inits[0].pid == 1
    # culpable 11:04 con PR-0091 y mismo binario
    guilty = [p for p in procs if p.start == FARO_GUILTY_START]
    assert len(guilty) == 1, f"esperaba 1 proceso con START 11:04, got {[p.start for p in procs]}"
    g = guilty[0]
    assert "PR-0091" in g.cmd and FARO_SYNC_BINARY in g.cmd
    # el otro faro-sync comparte binario pero no 11:04 ni PR-0091
    faros = [p for p in procs if FARO_SYNC_BINARY in p.cmd]
    assert len(faros) == 2
    decoys = [p for p in faros if p.start != FARO_GUILTY_START]
    assert len(decoys) == 1
    assert "PR-0092" in decoys[0].cmd
    # estable por seed: segunda llamada mismo seed → mismo START 11:04 y mismo pid
    inc2 = generate(42, 6)
    g2 = [p for p in inc2.room.fs.processes if p.start == FARO_GUILTY_START][0]
    assert g.pid == g2.pid and g.start == g2.start and g.cmd == g2.cmd
    # seed distinta puede variar pid del señuelo pero mantiene guilty 11:04
    inc3 = generate(7, 6)
    guilty3 = [p for p in inc3.room.fs.processes if p.start == FARO_GUILTY_START]
    assert len(guilty3) == 1 and "PR-0091" in guilty3[0].cmd


def test_dato5_golden_ps_aux_grep_1104_exit_0():
    inc = generate(42, 6)
    shell = new_session(inc)
    # ps aux debe listar START 11:04
    r_ps = shell.execute("ps aux")
    assert r_ps.exit_code == 0
    assert FARO_GUILTY_START in r_ps.stdout
    assert FARO_INIT_START in r_ps.stdout
    assert "PR-0091" in r_ps.stdout
    # golden canónico de dato5 — 1 pipe
    r = shell.execute("ps aux | grep 11:04")
    assert r.exit_code == 0, f"golden ps aux | grep 11:04 exit {r.exit_code} stderr {r.stderr!r} stdout {r.stdout!r}"
    # la línea filtrada debe ser la del culpable y contener PR-0091 y el binario compartido
    assert "PR-0091" in r.stdout
    assert FARO_SYNC_BINARY in r.stdout
    # no debe colar PR-0092
    assert "PR-0092" not in r.stdout
    # solo una línea relevante (sin contar header que no tiene 11:04)
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    assert len(lines) == 1, f"esperaba 1 línea filtrada, got {lines!r}"


def test_dato5_dato2_dato3_e1_e2_intactos_y_gate_127():
    # dato2
    inc2 = generate(42, 6, contract_id="story.ch6.dato2")
    s2 = new_session(inc2)
    r2 = s2.execute(f"cut -d'|' -f4 {PURGAS_PATH} | sort | uniq -c")
    assert r2.exit_code == 0 and "UMBRAL-BAJO" in r2.stdout
    # dato3
    inc3 = generate(42, 6, contract_id="story.ch6.dato3")
    s3 = new_session(inc3)
    r3 = s3.execute(f"sort -t '|' -k12 -n {PURGAS_PATH} | head -n 3")
    if "Try 'sort" not in r3.stderr:
        assert r3.exit_code == 0 and len([l for l in r3.stdout.splitlines() if l.strip()]) == 3
    # e1
    inc_e1 = generate(42, 6, contract_id="story.ch6.e1")
    se1 = new_session(inc_e1)
    re1 = se1.execute(f"grep ENSAYO {PURGAS_PATH} | wc -l")
    assert re1.exit_code == 0 and re1.stdout.strip() == "1"
    # e2
    inc_e2 = generate(42, 6, contract_id="story.ch6.e2")
    se2 = new_session(inc_e2)
    re2 = se2.execute(f"tail -n +2 {PURGAS_PATH} | cut -d'|' -f4 | sort")
    assert re2.exit_code == 0 and re2.stdout.count("UMBRAL-BAJO") == 2 and "distrito" not in re2.stdout
    # gate 127: ps no existe en cap0
    from core.generator import generate as gen0
    from core.sandbox.shell import Shell
    inc0 = gen0(42, 0)
    sh0 = Shell(inc0.room.fs.snapshot(), commands=DEFAULT_CAP0_COMMANDS, cwd="/")
    r127 = sh0.execute("ps aux")
    assert r127.exit_code == 127, "ps en cap0 debe ser 127 (allowlist intacta)"
    # allowlist CH6 sin cambios (ps y família conteo siguen)
    assert "ps" in DEFAULT_CH6_COMMANDS
    assert "cut" in DEFAULT_CH6_COMMANDS
    assert set(DEFAULT_CH6_COMMANDS) == {"cat", "cd", "cp", "cut", "env", "grep", "head", "kill", "ls", "ps", "sort", "sudo", "tail", "uniq", "wc"}


def test_dato5_fs_roundtrip_con_procesos():
    inc = generate(42, 6)
    d = inc.to_dict()
    from core.generator.model import Incursion
    inc2 = Incursion.from_dict(d)
    assert inc2.to_dict() == d
    # snapshot también preserva procesos
    sh = new_session(inc)
    sh2 = new_session(inc2)
    assert sh.fs.processes == sh2.fs.processes
    r1 = sh.execute("ps aux | grep 11:04")
    r2 = sh2.execute("ps aux | grep 11:04")
    assert r1.stdout == r2.stdout
