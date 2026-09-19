"""S1 19/09 — allowlists per-encargo Subestación (Smough).

Pattern CH4E3 (PR #57): base (cat,scp) intacta para e2; E1/E3/E4 novas con
verbos de su quest (Gwyndolin 19/09: e1 ls+ps+chmod+kill; e3 ps+env+kill;
e4 chmod+chown+tail+ls). Fuera de su encargo → 127 frontera honesta.
Golden e3 kill sobre intruso jugable (ps aux → censo 522, kill -HUP/-9).

Owner: Smough. GATE OWNER: NADIE toca asserts del gate.
Forma <= set(...) nunca == {...} exacto (regla 19/09).
"""
from core.sandbox.shell import (
    DEFAULT_CH5_COMMANDS,
    DEFAULT_CH5E1_COMMANDS,
    DEFAULT_CH5E3_COMMANDS,
    DEFAULT_CH5E4_COMMANDS,
    Shell,
)
from core.sandbox.fs import DirNode, FileNode, FileSystem, Proceso


def _fs_simple():
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "tmp": DirNode(name="tmp", children={"a.txt": FileNode(name="a.txt", content="hola\n")}),
                "etc": DirNode(name="etc", children={}),
            },
        ),
        processes=(
            Proceso(pid=1, user="root", cmd="/sbin/init", tty="?", cpu="0.0", mem="0.1", vsz="0", rss="0", stat="Ss", start="00:00", time="00:00"),
            Proceso(pid=522, user="censo", cmd="intruso --vigilar-censo", tty="?", cpu="0.0", mem="0.3", vsz="0", rss="0", stat="S", start="03:14", time="00:00"),
        ),
        environment={"PATH": "/usr/bin"},
    )


def test_base_intacta():
    assert set(DEFAULT_CH5_COMMANDS) == {"cat", "scp"}
    # Forma <= nunca == exacto para futuras extensiones, pero hoy base es exacta
    assert set(DEFAULT_CH5_COMMANDS) <= {"cat", "scp"}


def test_e1_superset_y_contiene():
    assert set(DEFAULT_CH5_COMMANDS) <= set(DEFAULT_CH5E1_COMMANDS)
    for cmd in ("ls", "ps", "chmod", "kill"):
        assert cmd in DEFAULT_CH5E1_COMMANDS
    # base siempre dentro
    assert "cat" in DEFAULT_CH5E1_COMMANDS and "scp" in DEFAULT_CH5E1_COMMANDS


def test_e3_superset_y_contiene():
    assert set(DEFAULT_CH5_COMMANDS) <= set(DEFAULT_CH5E3_COMMANDS)
    for cmd in ("ps", "env", "kill"):
        assert cmd in DEFAULT_CH5E3_COMMANDS
    assert "cat" in DEFAULT_CH5E3_COMMANDS


def test_e4_superset_y_contiene():
    assert set(DEFAULT_CH5_COMMANDS) <= set(DEFAULT_CH5E4_COMMANDS)
    for cmd in ("chmod", "chown", "tail", "ls"):
        assert cmd in DEFAULT_CH5E4_COMMANDS


def test_frontera_base_vs_e1():
    fs = _fs_simple()
    shell_base = Shell(fs.snapshot(), commands=DEFAULT_CH5_COMMANDS)
    shell_e1 = Shell(fs.snapshot(), commands=DEFAULT_CH5E1_COMMANDS)
    # base → 127 para ls/ps/chmod/kill
    for cmd in ("ls", "ps", "chmod 644 /tmp/a.txt", "kill 522"):
        res = shell_base.execute(cmd)
        assert res.exit_code == 127, f"base debe rechazar {cmd} con 127"
        assert "command not found" in res.stderr
    # e1 → NO 127 (ls ok, ps ok, chmod ok, kill ok o al menos no 127)
    assert shell_e1.execute("ls /tmp").exit_code == 0
    assert shell_e1.execute("ps").exit_code == 0
    assert shell_e1.execute("chmod 600 /tmp/a.txt").exit_code == 0
    # kill sin señal mata (522 existe)
    res = shell_e1.execute("kill 522")
    assert res.exit_code == 0


def test_frontera_base_vs_e3():
    fs = _fs_simple()
    shell_base = Shell(fs.snapshot(), commands=DEFAULT_CH5_COMMANDS)
    shell_e3 = Shell(fs.snapshot(), commands=DEFAULT_CH5E3_COMMANDS)
    for cmd in ("ps", "env", "kill 522"):
        assert shell_base.execute(cmd).exit_code == 127
        assert shell_e3.execute(cmd).exit_code == 0
    # chmod no está en e3 → 127
    assert shell_e3.execute("chmod 644 /tmp/a.txt").exit_code == 127
    assert shell_e3.execute("chown root /tmp/a.txt").exit_code == 127


def test_frontera_base_vs_e4():
    fs = _fs_simple()
    shell_base = Shell(fs.snapshot(), commands=DEFAULT_CH5_COMMANDS)
    shell_e4 = Shell(fs.snapshot(), commands=DEFAULT_CH5E4_COMMANDS)
    for cmd in ("chmod 644 /tmp/a.txt", "chown root /tmp/a.txt", "tail -n 1 /tmp/a.txt", "ls /tmp"):
        assert shell_base.execute(cmd).exit_code == 127
        assert shell_e4.execute(cmd).exit_code == 0
    # ps/env/kill no están en e4 → 127
    assert shell_e4.execute("ps").exit_code == 127
    assert shell_e4.execute("kill 522").exit_code == 127


def test_golden_e3_kill_hup_y_kill_9():
    # E3 kill sobre intruso jugable — distingue -HUP (reinicia) vs -9 (mata)
    fs = _fs_simple()
    shell = Shell(fs.snapshot(), commands=DEFAULT_CH5E3_COMMANDS)
    # ps aux muestra intruso censo 03:14
    res = shell.execute("ps aux")
    assert res.exit_code == 0
    assert "censo" in res.stdout and "intruso --vigilar-censo" in res.stdout
    # kill -HUP → reinicia, env HUP_522=1
    res = shell.execute("kill -HUP 522")
    assert res.exit_code == 0
    assert shell.fs.environment.get("HUP_522") == "1"
    # ps debe seguir mostrando el pid con --reloaded
    res = shell.execute("ps")
    assert "522" in res.stdout
    # kill -9 → mata (elimina)
    shell2 = Shell(fs.snapshot(), commands=DEFAULT_CH5E3_COMMANDS)
    res = shell2.execute("kill -9 522")
    assert res.exit_code == 0
    res = shell2.execute("ps")
    assert "522" not in res.stdout or "intruso" not in res.stdout


def test_chmod_cambia_mode_y_chown_owner():
    fs = _fs_simple()
    shell = Shell(fs.snapshot(), commands=DEFAULT_CH5E4_COMMANDS)
    # chmod 600 cambia mode
    res = shell.execute("chmod 600 /tmp/a.txt")
    assert res.exit_code == 0
    node = shell.fs.resolve("/tmp/a.txt", "/")
    assert node.mode == "600"
    # chown cambia owner
    res = shell.execute("chown gris /tmp/a.txt")
    assert res.exit_code == 0
    assert shell.fs.resolve("/tmp/a.txt", "/").owner == "gris"
    # chown con grupo
    res = shell.execute("chown gris:apagados /tmp/a.txt")
    assert res.exit_code == 0
    n = shell.fs.resolve("/tmp/a.txt", "/")
    assert n.owner == "gris" and n.group == "apagados"
