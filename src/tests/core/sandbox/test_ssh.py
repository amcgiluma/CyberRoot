"""test_ssh.py — S1 (06/09): Red simulada cap.4 pieza1: ssh básico + host-key + stack.

Criterio S1:
- ssh a host A con FS propio → cwd/pwd/ls reflejan A; segundo ssh a B apila; exit vuelve a A
- Sin huella cacheada → pregunta host-key OpenSSH exacta; yes → conecta y cachea; segundo ssh al mismo host NO repite pregunta
- no → sin conexión, mensaje honesto, sin ruido de sesión establecida
- Ruido familia Red (2), determinista por seed/host
"""

from __future__ import annotations

from core.sandbox.commands.red import fingerprint_for_host
from core.sandbox.fs import DirNode, FileNode, FileSystem
from core.sandbox.shell import Shell


def _fs_for_host(name: str, files: dict[str, str]) -> FileSystem:
    children = {k: FileNode(name=k, content=v) for k, v in files.items()}
    return FileSystem(root=DirNode(name="/", children={"home": DirNode(name="home", children=children)}))


def _shell_with_hosts():
    local = FileSystem(root=DirNode(name="/", children={"tmp": DirNode(name="tmp", children={"local.txt": FileNode(name="local.txt", content="local")})}))
    host_a = _fs_for_host("alpha", {"a.txt": "AAA", "compartido.txt": "A"})
    host_b = _fs_for_host("beta", {"b.txt": "BBB", "otro.txt": "B"})
    shell = Shell(local, host="local", commands=("ls", "cat", "ssh", "exit", "cd"))
    shell.register_host("alpha", host_a)
    shell.register_host("beta", host_b)
    return shell, local, host_a, host_b


def test_ssh_conecta_y_refleja_fs_remoto():
    shell, _, host_a, _ = _shell_with_hosts()
    # Primer ssh a alpha sin cache → prompt host-key
    r1 = shell.execute("ssh alpha")
    assert r1.exit_code == 0
    assert "The authenticity of host 'alpha' can't be established." in r1.stdout
    assert "ED25519 key fingerprint is SHA256:" in r1.stdout
    assert "Are you sure you want to continue connecting (yes/no/[fingerprint])?" in r1.stdout
    # Aún no conectado (cwd sigue local)
    assert shell.host == "local"
    # Responder yes → conecta
    r2 = shell.execute("yes")
    assert r2.exit_code == 0
    assert "Permanently added 'alpha'" in r2.stdout
    assert "Connected to alpha" in r2.stdout
    assert shell.host == "alpha"
    # ls debe reflejar A
    r3 = shell.execute("ls /home")
    assert "a.txt" in r3.stdout
    assert "b.txt" not in r3.stdout


def test_ssh_segundo_host_apila_y_exit_desapila():
    shell, _, _, _ = _shell_with_hosts()
    shell.execute("ssh alpha")
    shell.execute("yes")
    # segundo ssh a beta → prompt
    r = shell.execute("ssh beta")
    assert "The authenticity of host 'beta'" in r.stdout
    shell.execute("yes")
    assert shell.host == "beta"
    r2 = shell.execute("ls /home")
    assert "b.txt" in r2.stdout
    # exit vuelve a alpha
    shell.execute("exit")
    assert shell.host == "alpha"
    r3 = shell.execute("ls /home")
    assert "a.txt" in r3.stdout
    # exit vuelve a local
    shell.execute("exit")
    assert shell.host == "local"


def test_ssh_yes_cachea_no_repite_pregunta():
    shell, _, _, _ = _shell_with_hosts()
    shell.execute("ssh alpha")
    shell.execute("yes")
    shell.execute("exit")
    # segundo ssh al mismo host NO repite pregunta
    r = shell.execute("ssh alpha")
    assert r.exit_code == 0
    assert "Connected to alpha" in r.stdout
    assert "authenticity" not in r.stdout
    assert shell.host == "alpha"


def test_ssh_no_no_conecta_y_sin_ruido_establecida():
    shell, _, _, _ = _shell_with_hosts()
    r1 = shell.execute("ssh alpha")
    assert r1.exit_code == 0
    before_noise = shell.total_noise
    # pending, ahora "no"
    r2 = shell.execute("no")
    assert r2.exit_code == 1
    assert "Host key verification failed" in r2.stdout
    assert shell.host == "local"
    # no debe haber ruido extra de sesión establecida (solo el de los prompts)
    # r2 tiene noise 0 (plan: sin ruido de sesión establecida)
    assert r2.noise == () or sum(ev.data.get("amount", 0) for ev in r2.noise) == 0
    # Siguiente intento vuelve a preguntar (no cacheó)
    r3 = shell.execute("ssh alpha")
    assert "authenticity" in r3.stdout


def test_ssh_fingerprint_determinista():
    fp1 = fingerprint_for_host("alpha")
    fp2 = fingerprint_for_host("alpha")
    fp3 = fingerprint_for_host("beta")
    assert fp1 == fp2
    assert fp1 != fp3
    assert fp1.startswith("SHA256:")
    # conectar via fingerprint en vez de yes
    shell, _, _, _ = _shell_with_hosts()
    r = shell.execute("ssh alpha")
    fp = fingerprint_for_host("alpha")
    assert fp in r.stdout
    r2 = shell.execute(fp)
    assert "Connected to alpha" in r2.stdout
    assert shell.host == "alpha"


def test_ssh_host_no_registrado_error():
    shell, _, _, _ = _shell_with_hosts()
    r = shell.execute("ssh gamma")
    assert r.exit_code == 255
    assert "Could not resolve hostname" in r.stderr
    assert shell.host == "local"


def test_ssh_user_at_host_parse():
    shell, _, _, _ = _shell_with_hosts()
    r1 = shell.execute("ssh user@alpha")
    assert "authenticity of host 'alpha'" in r1.stdout
    r2 = shell.execute("yes")
    assert shell.host == "alpha"


def test_ssh_noise_familia_red():
    shell, _, _, _ = _shell_with_hosts()
    before = shell.total_noise
    shell.execute("ssh alpha")  # prompt con noise 2
    assert shell.total_noise == before + 2
    shell.execute("yes")  # conecta con noise 2
    assert shell.total_noise == before + 4


def test_ssh_serializacion_roundtrip_preserva_stack_y_known():
    shell, _, _, _ = _shell_with_hosts()
    shell.execute("ssh alpha")
    shell.execute("yes")
    shell.execute("ssh beta")
    shell.execute("yes")
    # stack tiene 2 entradas (local->alpha->beta)
    d = shell.to_dict()
    restored = Shell.from_dict(d)
    assert restored.host == "beta"
    assert restored.known_hosts == shell.known_hosts
    assert len(restored.host_stack) == 2
    # exit en restored debe volver a alpha
    restored.execute("exit")
    assert restored.host == "alpha"
    assert restored.to_dict()["host"] == "alpha"
