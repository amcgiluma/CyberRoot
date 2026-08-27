"""H4 — Sesión END-TO-END del cap. 0 «Trabajo en frío» + determinismo duro.

La piel del FS replica la ESCENA TÉCNICA de `backlog/historia/CAPITULOS/
00-la-firma.md` (oficina-vecinal-muelle-norte, ventana de las 11:04). La
secuencia canónica es la del texto de Manus: ls → cat → cd ..; la extracción
con `cp` queda cubierta como GANCHO para si Gwyn aprueba 🧭1.

Reproducibilidad byte a byte ante misma seed: la sesión es 100 % determinista
(sin RNG), y el test de cross-proceso demuestra IDÉNTICA salida en dos
procesos con PYTHONHASHSEED distintos (criterio de aceptación de la tarea B).
"""

from __future__ import annotations

import os
import subprocess
import sys

from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell

OFICINA = "/srv/oficina-vecinal-muelle-norte"
PROVEEDOR = "nombre_de_proveedor.txt"


def _fs_oficina() -> FileSystem:
    """Piel del nodo del encargo (los datos base son los de la escena)."""
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
                                PROVEEDOR: FileNode(
                                    name=PROVEEDOR,
                                    content=(
                                        "CANDELAS  ·  proveedor nº 47  ·  "
                                        "facturación externa  ·  114 facturas/mes\n"
                                    ),
                                    owner="recepcion",
                                    group="empleados",
                                    mtime=1044,  # 11:04, tiempo simulado
                                ),
                                "log.txt": FileNode(
                                    name="log.txt",
                                    content="08:59 turno de mañana\n11:04 SIN REGISTRO\n",
                                    mtime=1030,
                                ),
                                "README": FileNode(
                                    name="README",
                                    content="Sistema de gestion de la oficina vecinal.\n",
                                    mtime=900,
                                ),
                            },
                        )
                    },
                ),
                "usb": DirNode(name="usb", children={}),  # el USB de 512 MB
            },
        )
    )


def _secuencia_canonica(shell: Shell) -> list[str]:
    """La secuencia de la escena técnica; devuelve los stdout en orden."""
    outs = []
    outs.append(shell.execute(f"ls {OFICINA}").stdout)
    outs.append(shell.execute(f"cat {OFICINA}/{PROVEEDOR}").stdout)
    shell.execute("cd /srv")
    outs.append(shell.execute("ls").stdout)
    return outs


def test_escena_cap0_salida_byte_a_byte() -> None:
    """ls → cat → cd .. produce EXACTAMENTE la salida de la escena."""
    shell = Shell(_fs_oficina(), host="oficina-vecinal-muelle-norte")
    ls_out, cat_out, ls_srv = _secuencia_canonica(shell)
    # GNU ordena por codepoint (README < log.txt < nombre_de_proveedor.txt);
    # la prosa de Manus narra el orden humano, no el orden de listado.
    assert ls_out == f"README\nlog.txt\n{PROVEEDOR}\n"
    assert cat_out == (
        "CANDELAS  ·  proveedor nº 47  ·  facturación externa  ·  114 facturas/mes\n"
    )
    assert ls_srv == "oficina-vecinal-muelle-norte\n"  # el USB cuelga de la raíz
    assert shell.cwd == "/srv"
    # El session dump completo es reproducible:
    assert Shell.from_dict(shell.to_dict()).to_dict() == shell.to_dict()


def test_gancho_cp_extraccion_del_dossier() -> None:
    """CON cp habilitado (si 🧭1 se aprueba): copiar → verificar en /usb."""
    shell = Shell(
        _fs_oficina(), host="oficina-vecinal-muelle-norte", commands=("cp", "cat", "ls")
    )
    res = shell.execute(f"cp {OFICINA}/{PROVEEDOR} /usb/")
    assert res.exit_code == 0, res.stderr
    copia = shell.execute("cat /usb/nombre_de_proveedor.txt")
    assert copia.stdout.startswith("CANDELAS")
    assert shell.registry.get("cp") is not None
    # Ruido total para el engine: cp(3) + cat(1) = 4.
    assert shell.total_noise == 4


_SNIPPET = """
import sys
sys.path.insert(0, "src")
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell

fs = FileSystem(root=DirNode(name="/", children={
    "srv": DirNode(name="srv", children={
        "oficina": DirNode(name="oficina", children={
            "nombre_de_proveedor.txt": FileNode(name="nombre_de_proveedor.txt",
                content="CANDELAS\\nproveedor 47\\n", mtime=1044),
            "log.txt": FileNode(name="log.txt", content="11:04\\n"),
            "README": FileNode(name="README", content="gestion\\n"),
        }),
    }),
    "usb": DirNode(name="usb"),
}))
shell = Shell(fs, host="oficina-vecinal-muelle-norte")
for line in ("ls /srv/oficina", "cat /srv/oficina/nombre_de_proveedor.txt",
             "cd /srv", "ls", "cd ..", "cat /srv/oficina/log.txt", "pwd_x"):
    r = shell.execute(line)
    print(repr((r.stdout, r.stderr, r.exit_code)))
print("TOTAL", shell.total_noise, shell.tick)
print("DUMP", repr(sorted(shell.to_dict().keys())))
"""


def test_reproducibilidad_entre_procesos_pythonhashseed_distinto() -> None:
    """Dos procesos, PYTHONHASHSEED distintos → salida BYTE A BYTE idéntica."""
    envs = [
        {**os.environ, "PYTHONHASHSEED": "1"},
        {**os.environ, "PYTHONHASHSEED": "999999"},
    ]
    outputs = []
    for env in envs:
        proc = subprocess.run(
            [sys.executable, "-c", _SNIPPET],
            capture_output=True,
            text=True,
            env=env,
            timeout=60,
            check=True,
        )
        outputs.append(proc.stdout)
    assert outputs[0] == outputs[1]
    # Y la salida tiene la forma esperada (no un empate vacío de dos fallos):
    assert "CANDELAS" in outputs[0]
    assert "command not found: pwd_x" in outputs[0]  # el 127 real del final
    assert "TOTAL 4 7" in outputs[0]  # ruido 4 (ls+cat+cat+pwd_x... ver abajo)
