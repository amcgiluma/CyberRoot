"""O1 (03/09, Ornstein) — el demonio del cap. 3 en el mundo real (🧭16, opción a).

El generator inyecta LAZY el par `ceniza:521 --ventana` / `censo:522
--vigilar-censo` (réplica exacta del FS handmade de `test_session_kill.py`,
el golden de la física `kill`) SOLO cuando la quest de la sala requiere
`c.ps`/`c.kill`. La credencial + `auth.log` se colocan SIEMPRE (circuito S1
intacto): `generate(42,3)` con la quest sudo queda con credencial y auth.log
byte-exactos.

Sin tocar `src/core/sandbox/` (dueño Smough/S1 hoy): la física `kill` se
ejercita a través de la Shell pública, igual que el golden.
"""

from __future__ import annotations

from core.generator import generate, new_session
from core.generator.chapter3 import (
    AUTH_LOG_CONTENT,
    AUTH_LOG_PATH,
    CHAPTER3_ENVIRONMENT,
    SUDO_CREDENTIAL_CONTENT,
    SUDO_CREDENTIAL_PATH,
    build_chapter3_fs,
)
from core.generator.generator import _requiere_procesos
from core.sandbox.fs import FileNode


def test_sudo_de_hoy_credencial_y_auth_log_exactos_mas_demonio() -> None:
    """Criterio 1: `generate(42,3)` con la quest sudo no mueve S1 ni un byte.

    La quest sudo de hoy (`story.ch3.e4`) también requiere `c.ps`, así que
    su sala gana el demonio SIN que la credencial ni el `auth.log` cambien.
    """
    inc = generate(42, 3)
    assert inc.contract.objective_key == "story.ch3.e4"
    cred = inc.room.fs.resolve(SUDO_CREDENTIAL_PATH, "/")
    assert isinstance(cred, FileNode)
    assert cred.content == SUDO_CREDENTIAL_CONTENT
    alog = inc.room.fs.resolve(AUTH_LOG_PATH, "/")
    assert isinstance(alog, FileNode)
    assert alog.content == AUTH_LOG_CONTENT
    assert [(p.pid, p.user) for p in inc.room.fs.processes] == [
        (1, "root"),
        (521, "ceniza"),
        (522, "censo"),
    ]


def test_quest_de_procesos_explicita_tambien_inyecta() -> None:
    """Criterio 2a: con quest de procesos, el FS contiene 521/522."""
    inc = generate(42, 3, contract_id="story.ch3.e2")
    assert inc.contract.objective_key == "story.ch3.e2"
    por_pid = {p.pid: p for p in inc.room.fs.processes}
    assert por_pid[521].user == "ceniza"
    assert por_pid[522].user == "censo"
    # La credencial sigue en el mundo aunque la quest no sea la sudo.
    cred = inc.room.fs.resolve(SUDO_CREDENTIAL_PATH, "/")
    assert isinstance(cred, FileNode)
    assert cred.content == SUDO_CREDENTIAL_CONTENT


def test_ps_muestra_columna_user_y_fisica_kill_del_golden() -> None:
    """Criterio 2b: misma física que el golden de `test_session_kill.py`.

    `ps aux` muestra la columna USER (ceniza vs censo); `kill -9 522`
    mata y `kill -HUP 521` deja `--reloaded` + `HUP_521=1`.
    """
    inc = generate(42, 3)
    shell = new_session(inc)
    ps = shell.execute("ps aux").stdout
    assert ps.splitlines()[0].startswith("USER")
    assert "ceniza" in ps and "censo" in ps

    assert shell.execute("kill -9 522").exit_code == 0
    ps_muerto = shell.execute("ps aux").stdout
    assert "vigilar-censo" not in ps_muerto
    assert "ceniza" in ps_muerto  # 521 sigue vivo

    assert shell.execute("kill -HUP 521").exit_code == 0
    assert "--reloaded" in shell.execute("ps aux").stdout
    assert "HUP_521=1" in shell.execute("env").stdout


def test_lazy_sin_quest_de_procesos_no_hay_demonio() -> None:
    """El demonio entra LAZY: sin `c.ps`/`c.kill` no hay procesos ni env."""
    fs = build_chapter3_fs(None)
    assert tuple(fs.processes) == ()
    assert fs.environment is None or "HUP_521" not in fs.environment
    # ...pero la credencial y el auth.log sí están (circuito S1).
    cred = fs.resolve(SUDO_CREDENTIAL_PATH, "/")
    assert isinstance(cred, FileNode)
    assert cred.content == SUDO_CREDENTIAL_CONTENT
    alog = fs.resolve(AUTH_LOG_PATH, "/")
    assert isinstance(alog, FileNode)
    assert alog.content == AUTH_LOG_CONTENT


def test_requiere_procesos_por_literal_del_plan() -> None:
    """`c.kill` aún no es concepto del currículo: se acepta por literal."""
    assert _requiere_procesos(("c.ps", "c.env")) is True
    assert _requiere_procesos(("c.kill",)) is True
    assert _requiere_procesos(("c.sudo",)) is False
    assert _requiere_procesos(("c.ls", "c.cat")) is False


def test_determinismo_con_demonio() -> None:
    """Criterio 3: determinismo por seed intacto con procesos dentro."""
    a = generate(42, 3)
    b = generate(42, 3)
    assert a.room.id == b.room.id
    assert a.room.fs.to_dict() == b.room.fs.to_dict()
    c = generate(43, 3)
    assert [p.pid for p in c.room.fs.processes] == [1, 521, 522]
    assert c.room.fs.environment == dict(CHAPTER3_ENVIRONMENT)
