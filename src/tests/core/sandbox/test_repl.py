"""Smoke test del REPL (S2, Smough 29/08): `python -m core.sandbox`.

AC de S2: la secuencia canónica del dossier (ls→cat→cp→cd) se juega de verdad
en el REPL; los errores (127, rechazo didáctico `&&`) se muestran idénticos a
la sesión testeada; hay un test mínimo que invoca el bucle programáticamente
(sin TTY, vía `run_repl` con iterable de líneas y callables de captura).

El bucle es determinista (FS estático, sin RNG): los asserts fijan la salida
byte a byte sobre los datos de la escena de `CAPITULOS/00-la-firma.md`.
"""

from __future__ import annotations

from core.sandbox.__main__ import _BANNER, _prompt, build_cap0_session, run_repl
from core.sandbox.shell import Shell


def _correr(shell: Shell, lines: list[str]) -> tuple[str, str]:
    """Ejecuta run_repl capturando stdout(->out) y stderr(->err) por separado."""
    out: list[str] = []
    err: list[str] = []
    run_repl(shell, lines, write_out=out.append, write_err=err.append)
    return "".join(out), "".join(err)


def test_repl_juega_secuencia_canonica_del_dossier() -> None:
    """ls→cat→cp→cd del dossier se juegan en el REPL (AC de S2)."""
    shell = build_cap0_session()
    out, err = _correr(
        shell,
        [
            "ls /srv/oficina-vecinal-muelle-norte",
            "cat /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt",
            "cp /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt /usb/",
            "cd /srv",
            "ls",
        ],
    )
    # El listado del dossier: los 3 ficheros ordenados por codepoint.
    assert out.count("README\nlog.txt\nnombre_de_proveedor.txt\n") == 1
    # El proveedor (contenido exacto, newline incluido).
    assert (
        "CANDELAS  ·  proveedor nº 47  ·  facturación externa  ·  114 facturas/mes\n"
        in out
    )
    # Tras `cd /srv` el prompt cambia a :/srv$ y `ls` lista una entrada.
    assert "operador@oficina-vecinal:/srv$ " in out
    assert "oficina-vecinal-muelle-norte\n" in out  # la entrada de /srv
    # `cp` con éxito no emite nada (stdout vacío): no hay errores.
    assert err == ""
    # Una sesión terminada por fin de iterable: no cuelga y avanza ticks.
    assert shell.tick == 5


def test_repl_muestra_errores_idénticos_a_la_sesión() -> None:
    """Error 127 y rechazo didáctico `&&` salen idénticos a la sesión testeada."""
    shell = build_cap0_session()
    out, err = _correr(shell, ["pwd_noexiste", "ls /srv && cat", "exit"])
    # 127 real de `sh`.
    assert "sh: command not found: pwd_noexiste" in err
    assert "[exit 127]" in err
    # Rechazo didáctico de encadenado (mismo texto que test_shell.py, exit 2).
    assert "sh: syntax not supported in this session" in err
    assert "[exit 2]" in err
    # `exit` cierra: la última línea NO vuelca stdout y el bucle termina.
    assert shell.tick == 2


def test_repl_prompt_diegético_cambia_con_la_cwd() -> None:
    """El prompt refleja la cwd: raíz como `~`, luego la ruta normalizada."""
    shell = build_cap0_session()
    assert _prompt(shell) == "operador@oficina-vecinal:~$ "
    out, _ = _correr(shell, ["cd /srv", "ls"])
    assert "operador@oficina-vecinal:/srv$ " in out
    out2, _ = _correr(build_cap0_session(), [""])
    # Línea vacía (Enter) no cambia cwd ni errores.
    assert "operador@oficina-vecinal:~$ " in out2


def test_repl_banner_abre_la_escena() -> None:
    """El banner diegético enmarca la conexión al nodo cap. 0."""
    shell = build_cap0_session()
    out, _ = _correr(shell, [])
    assert out.startswith(_BANNER)