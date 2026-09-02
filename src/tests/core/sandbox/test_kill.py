"""test_kill.py — golden tests de `kill` / señales v0 (S1, 02/09, cap. 3).

CERO RNG (§2.2): los procesos son piel del generador — se inyectan como
`fs.processes` y el comando los muta de forma determinista. Mensajes y exits
en inglés/GNU (DESIGN §2.6.8), verificados contra `kill` real (bash builtin).
"""

from __future__ import annotations

from core.sandbox.commands.senal import KILL_SPEC
from core.sandbox.commands.base import CommandResult
from core.sandbox.fs import DirNode, FileSystem, Proceso
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH3_COMMANDS, DEFAULT_CH6_COMMANDS, Shell
from core.sandbox.commands.senal import _run_kill


def _fs_pair() -> FileSystem:
    """FS con el par ceniza/censo (521/522) + init, idéntico a test_session_ch3."""
    return FileSystem(
        root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={})}),
        processes=(
            Proceso(pid=1, user="root", cmd="/init"),
            Proceso(pid=521, user="ceniza", cmd="/usr/sbin/demonio-11:04 --ventana"),
            Proceso(pid=522, user="censo", cmd="/usr/sbin/demonio-11:04 --vigilar-censo"),
        ),
        environment={"USER": "operator"},
    )


def _kill(argv: tuple[str, ...], fs: FileSystem | None = None) -> CommandResult:
    f = fs if fs is not None else _fs_pair()
    return _run_kill(f, "/", argv, tick=0)


# ---- golden GNU: errores ---------------------------------------------

def test_kill_sin_args_error() -> None:
    res = _kill(())  # type: ignore
    assert res.exit_code == 1
    assert res.stderr == "kill: not enough arguments"


def test_kill_pid_inexistente_golden() -> None:
    res = _kill(("999",))
    assert res.exit_code == 1
    assert res.stderr == "kill: (999) - No such process"


def test_kill_pid_no_numerico_golden() -> None:
    res = _kill(("abc",))
    assert res.exit_code == 1
    assert "arguments must be process or job IDs" in res.stderr


def test_kill_senal_invalida_golden() -> None:
    res = _kill(("-XYZ", "521"))
    assert res.exit_code == 1
    assert res.stderr == "kill: invalid signal 'XYZ'"


def test_kill_s_opcion_sin_arg_golden() -> None:
    res = _kill(("-s",))
    assert res.exit_code == 1
    assert "option requires an argument" in res.stderr


def test_kill_s_senal_invalida_golden() -> None:
    res = _kill(("-s", "BOGUS", "521"))
    assert res.exit_code == 1
    assert res.stderr == "kill: invalid signal 'BOGUS'"


# ---- física: -9 mata, -HUP reinicia ---------------------------------

def test_kill_9_mata_proceso() -> None:
    fs = _fs_pair()
    res = _run_kill(fs, "/", ("-9", "522"), tick=5)
    assert res.exit_code == 0, res.stderr
    assert [p.pid for p in fs.processes] == [1, 521]
    # evento sandbox.signal emitido
    sigs = [e for e in res.noise if e.type == "sandbox.signal"]
    assert len(sigs) == 1 and sigs[0].data["signal"] == "KILL" and sigs[0].data["pid"] == 522
    assert sigs[0].tick == 5


def test_kill_default_term_mata() -> None:
    fs = _fs_pair()
    res = _run_kill(fs, "/", ("521",), tick=2)
    assert res.exit_code == 0
    assert 521 not in [p.pid for p in fs.processes]
    sigs = [e for e in res.noise if e.type == "sandbox.signal"]
    assert sigs[0].data["signal"] == "TERM" and sigs[0].data["signal_num"] == 15


def test_kill_hup_reinicia_con_config_distinta() -> None:
    fs = _fs_pair()
    res = _run_kill(fs, "/", ("-HUP", "521"), tick=7)
    assert res.exit_code == 0, res.stderr
    # proceso sigue
    assert 521 in [p.pid for p in fs.processes]
    p521 = next(p for p in fs.processes if p.pid == 521)
    assert " --reloaded" in p521.cmd
    assert fs.environment.get("HUP_521") == "1"
    sigs = [e for e in res.noise if e.type == "sandbox.signal"]
    assert sigs[0].data["signal"] == "HUP" and sigs[0].data["signal_num"] == 1
    # observable en ps/env lo testea test_session_kill


def test_kill_hup_aliases() -> None:
    for flag in ("-1", "-SIGHUP", "-HUP", "-s",):
        fs = _fs_pair()
        argv = (flag, "HUP", "522") if flag == "-s" else (flag, "522")
        # -s HUP necesita dos tokens: ya testeado arriba, -s HUP 522 = -s HUP + pid
        if flag == "-s":
            argv = ("-s", "HUP", "522")
        res = _run_kill(fs, "/", argv, tick=0)
        assert res.exit_code == 0, f"{flag} failed: {res.stderr}"
        assert " --reloaded" in next(p.cmd for p in fs.processes if p.pid == 522)


def test_kill_multiples_pids() -> None:
    fs = _fs_pair()
    res = _run_kill(fs, "/", ("521", "522"), tick=0)
    assert res.exit_code == 0
    assert [p.pid for p in fs.processes] == [1]
    assert len([e for e in res.noise if e.type == "sandbox.signal"]) == 2


def test_kill_parcial_uno_falla_otro_mata() -> None:
    fs = _fs_pair()
    res = _run_kill(fs, "/", ("999", "521"), tick=0)
    assert res.exit_code == 1
    assert "No such process" in res.stderr
    # 521 sí se mató a pesar del error en 999
    assert 521 not in [p.pid for p in fs.processes]
    assert 522 in [p.pid for p in fs.processes]


def test_kill_ruido_perfil_2() -> None:
    assert KILL_SPEC.noise == 2
    fs = _fs_pair()
    shell = Shell(fs, commands=DEFAULT_CH3_COMMANDS)
    shell.execute("kill -9 522")
    assert shell.total_noise == 2
    # -HUP también 2 (mismo comando)
    fs2 = _fs_pair()
    sh2 = Shell(fs2, commands=DEFAULT_CH3_COMMANDS)
    sh2.execute("kill -HUP 521")
    assert sh2.total_noise == 2


def test_kill_gate_127_cap0_y_cap2() -> None:
    s0 = Shell(_fs_pair(), commands=DEFAULT_CAP0_COMMANDS)
    assert s0.execute("kill 521").exit_code == 127
    from core.sandbox.shell import DEFAULT_CH2_COMMANDS
    s2 = Shell(_fs_pair(), commands=DEFAULT_CH2_COMMANDS)
    assert s2.execute("kill -9 522").exit_code == 127
    # ch3 sí existe
    s3 = Shell(_fs_pair(), commands=DEFAULT_CH3_COMMANDS)
    assert s3.execute("kill 999").exit_code == 1  # no 127, llegó al handler
    # ch6 también
    s6 = Shell(_fs_pair(), commands=DEFAULT_CH6_COMMANDS)
    assert s6.execute("kill 999").exit_code == 1
