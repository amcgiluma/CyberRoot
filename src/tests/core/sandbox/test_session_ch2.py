"""S1 (30/08) — Sesión END-TO-END del cap. 2 «Facturas».

Replica `test_session_cap0.py` con el FS extendido del cap. 2 (la misma
oficina, ahora con `centralita/turnos/` — canon del cap. 2 de Manus). La
secuencia canónica VERIFICA la línea EXACTA del capítulo:

    $ grep 11:04 centralita/turnos/turno.log | wc -l
    2

Golden contra GNU real (verificado 30/08: `grep 11:04 ... | wc -l` → `2`).
La tubería no es gratis: grep(2) + wc(1) facturan su ruido por separado.
"""

from __future__ import annotations

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import DEFAULT_CH2_COMMANDS, Shell

OFICINA = "/srv/oficina-vecinal-muelle-norte"
TURNO = "centralita/turnos/turno.log"


def _fs_oficina() -> FileSystem:
    """FS del cap. 2: el fixture del cap. 0 + centralita (nota integrador ch2)."""
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "oficina-vecinal-muelle-norte": DirNode(
                            name="oficina-vecinal-muelle-norte",
                            children={
                                "centralita": DirNode(
                                    name="centralita",
                                    children={
                                        "turnos": DirNode(
                                            name="turnos",
                                            children={
                                                "turno.log": FileNode(
                                                    name="turno.log",
                                                    content=(
                                                        "11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt\n"
                                                        "11:04 sesion 000 ruido 1 objetivo -\n"
                                                        "08:59 turno de manana\n"
                                                    ),
                                                ),
                                            },
                                        ),
                                        "facturas": DirNode(name="facturas", children={}),
                                    },
                                ),
                                "nombre_de_proveedor.txt": FileNode(
                                    name="nombre_de_proveedor.txt",
                                    content=(
                                        "CANDELAS  ·  proveedor nº 47  ·  "
                                        "facturación externa  ·  114 facturas/mes\n"
                                    ),
                                ),
                                "log.txt": FileNode(
                                    name="log.txt",
                                    content="08:59 turno de mañana\n11:04 SIN REGISTRO\n",
                                    mtime=1030,
                                ),
                            },
                        )
                    },
                ),
                "usb": DirNode(name="usb", children={}),
            },
        )
    )


def test_escena_cap2_grep_pipe_wc_linea_exacta() -> None:
    """La línea EXACTA del cap. 2: `grep 11:04 ... | wc -l` → `2`."""
    shell = Shell(_fs_oficina(), host="oficina-vecinal-muelle-norte", commands=DEFAULT_CH2_COMMANDS)
    shell.execute(f"cd {OFICINA}")
    res = shell.execute(f"grep 11:04 {TURNO} | wc -l")
    assert res.exit_code == 0, res.stderr
    assert res.stdout == "2\n"
    # Y el grep sin pipe imprime las dos líneas de la apertura.
    res2 = shell.execute(f"grep 11:04 {TURNO}")
    assert res2.exit_code == 0
    assert res2.stdout == (
        "11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt\n"
        "11:04 sesion 000 ruido 1 objetivo -\n"
    )
    # Sesión completa reproducible ida y vuelta exacta.
    assert Shell.from_dict(shell.to_dict()).to_dict() == shell.to_dict()


def test_tuberia_factura_ruido_de_ambos_comandos() -> None:
    """AC S1: cada comando de la tubería factura su amount (no es gratis)."""
    shell = Shell(_fs_oficina(), host="oficina-vecinal-muelle-norte", commands=DEFAULT_CH2_COMMANDS)
    shell.execute(f"cd {OFICINA}")
    # grep(2) + wc(1) = 3; más el cd(0). Historial: cd + una línea de pipe.
    shell.execute(f"grep 11:04 {TURNO} | wc -l")
    assert shell.total_noise == 3
    assert len(shell.history) == 2
    # Cada evento de ruido viaja con su comando y amount (para el engine).
    noise_cmds = {
        ev["data"]["command"]: int(ev["data"]["amount"])
        for h in shell.history
        for ev in h["result"]["noise"]
    }
    assert noise_cmds["grep"] == 2 and noise_cmds["wc"] == 1