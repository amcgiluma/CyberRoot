"""S1 (31/08) — golden tests de `ps` y `env` (familia procesos, cap. 3).

CERO RNG: los procesos son PIEL del generador — se inyectan como `fs.processes`
(Proceso en fs.py) y el comando los reproduce en orden de PID. Cabeceras y
formato verificadas contra coreutils real (Ubuntu, 31/08): `ps` →
`    PID TTY          TIME CMD`; `ps aux` → cabecera completa con USER; `env`
→ orden por clave (codepoint) para reproducibilidad byte a byte (§5).
"""

from __future__ import annotations

from core.sandbox.commands.procesos import (
    _run_env,
    _run_ps,
    ENV_SPEC,
    PS_SPEC,
)
from core.sandbox.fs import DirNode, FileSystem, Proceso


def _fs(
    procs: tuple[Proceso, ...] = (
        Proceso(pid=1, user="root", cmd="/usr/lib/systemd/systemd --system"),
        Proceso(pid=742, user="ceniza", cmd="/usr/sbin/demonio-03:00 --vigilar"),
        Proceso(pid=1041, user="operator", cmd="grep -R listado /srv/censo"),
    ),
) -> FileSystem:
    """FS con procesos simulados de la subestación del cap. 3 (piel fija)."""
    return FileSystem(
        root=DirNode(name="/"),
        processes=procs,
        environment={
            "LANG": "C.UTF-8",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin",
            "SHELL": "/bin/sh",
            "USER": "operator",
        },
    )


def _ps(argv: tuple[str, ...] = ()):
    return _run_ps(_fs(), "/", argv, tick=0)


def _env(argv: tuple[str, ...] = ()):
    return _run_env(_fs(), "/", argv, tick=0)


# ---- ps ---------------------------------------------------------------

def test_ps_cabecera_compacta_gnu() -> None:
    """GNU real: `ps` sin flags → cabecera `    PID TTY          TIME CMD`."""
    res = _ps()
    assert res.exit_code == 0
    assert res.stdout.startswith("    PID TTY          TIME CMD\n")
    # Orden por PID ascendente (determinismo §5) — el demonio 742 antes del 1041.
    lines = res.stdout.splitlines()[1:]
    assert len(lines) == 3
    assert all(l.startswith("    1 ") or l.startswith("  742 ") or l.startswith(" 1041 ") for l in lines)
    assert res.stdout.index("  742 ") < res.stdout.index(" 1041 ")


def test_ps_aux_muestra_columna_user() -> None:
    """`ps aux` (la forma que pide Manus en E1/E4): la columna USER DELATA.

    La prosa del cap. 3: «la diferencia entre los dos cabe en una columna, y
    esa columna te ha costado dos expulsiones» (post-mortem de Ceniza).
    """
    res = _ps(("aux",))
    assert res.exit_code == 0
    assert res.stdout.startswith(
        "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n"
    )
    assert "ceniza" in res.stdout
    assert "operator" in res.stdout
    # El demonio pertenece a ceniza: `ps aux` lo muestra (lo que `ps` no delata
    # con la suficiente claridad para Manus).
    demonio = [l for l in res.stdout.splitlines() if "demonio-03:00" in l]
    assert demonio and demonio[0].startswith("ceniza")


def test_ps_opcion_desconocida_exit_2() -> None:
    res = _ps(("-x",))
    assert res.exit_code == 2
    assert res.stderr == "ps: unknown option -- 'x'"


def test_ps_operando_buscar_por_pid_rechazado() -> None:
    """`ps 123` (operando para buscar por PID) no está en el contrato del cap.
    3 — rechazo GNU-honesto con el operando citado."""
    res = _ps(("123",))
    assert res.exit_code == 2
    assert "123" in res.stderr


def test_ps_sin_procesos_solo_cabecera() -> None:
    res = _run_ps(FileSystem(), "/", (), tick=0)
    assert res.exit_code == 0
    assert res.stdout == "    PID TTY          TIME CMD\n"


def test_ps_emite_ruido_perfil() -> None:
    assert PS_SPEC.noise == 1


# ---- env --------------------------------------------------------------

def test_env_lista_variables_ordenadas_por_clave() -> None:
    """`env` imprime `VAR=valor` ordenadas por clave (codepoint → §5)."""
    res = _env()
    assert res.exit_code == 0
    keys = [l.split("=", 1)[0] for l in res.stdout.splitlines()]
    assert keys == sorted(keys)
    assert "SHELL=/bin/sh" in res.stdout
    assert res.stdout.splitlines()[0] == "LANG=C.UTF-8"


def test_env_flag_rechazado_gnu() -> None:
    res = _env(("-i",))
    assert res.exit_code == 2
    assert res.stderr.startswith("env: invalid option")


def test_env_programa_no_soportado_didactico() -> None:
    """`env VAR=x cmd` (ejecutar con entorno modificado) no es del cap. 3."""
    res = _env(("FOO=1", "sh"))
    assert res.exit_code == 2
    assert "not supported in this session yet" in res.stderr


def test_env_sin_variables_stdout_vacio() -> None:
    res = _run_env(FileSystem(), "/", (), tick=0)
    assert res.exit_code == 0
    assert res.stdout == ""


def test_env_emite_ruido_perfil() -> None:
    assert ENV_SPEC.noise == 1