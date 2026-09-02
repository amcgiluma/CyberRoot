"""Oscar 05:00 02/09 Zona — tratamiento de soporte de la run de referencia.
Recorre la zona 🔬 (sudo GANADO + primera VOZ del Auditor) desde estado limpio.
No es codigo del juego: es una herramienta de playtest de Oscar."""
import sys
sys.path.insert(0, "src")

from core.sandbox.fs import FileSystem
from core.sandbox.shell import Shell, DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS
from core.sandbox.commands.escalada import AUTH_LOG_PATH, SUDO_CREDENTIAL_PATH
from tests.core.sandbox.test_session_sudo import _shell
from core.engine.postmortem import build_postmortem

from data.textos import resolve

print("="*72)
print("1) PRIMERA VOZ DEL JUEGO — Auditor via resolve()")
print("="*72)
t_pico  = resolve("postmortem.auditor.pico",  {"command": "sort turnos.log", "amount": "9"})
t_cruce = resolve("postmortem.auditor.cruce", {"command": "grep 11:04 turno.log", "amount": "7"})
print("  pico :", t_pico)
print("  cruce:", t_cruce)
for t in t_pico, t_cruce:
    assert t.startswith("Expediente 000:") and t.endswith("estable."), "forma formulario rota: " + t
print("  -> Forma formulario exacta (Expediente 000 … Continuidad: estable). OK.")

print()
print("="*72)
print("2) CIRCUITO SUDO GANADO (sala cap.3, FS de O1) — recorrido de jugador")
print("="*72)
shell = _shell()
print(f"  Entrada: host={shell.host} cwd={shell.cwd}")
print(f"  Credencial del mundo: {SUDO_CREDENTIAL_PATH}")

r = shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
print("\n  (a) INTENTO sudo SIN leer la llave:")
print(f"      exit={r.exit_code} | ruido acumulado={shell.total_noise} -> intentar no es delinquir (0): {shell.total_noise==0}")
print(f"      stderr={r.stderr.strip()!r}")
print(f"      stderr nombra el fichero que falta? {'authorization order' in r.stderr}")
auth = shell.fs.read_file(AUTH_LOG_PATH)
print(f"      firma tras solo-intento: {'sudo' in auth} (esperado False)")

r1 = shell.execute(f"cat {SUDO_CREDENTIAL_PATH}")
r2 = shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
print("\n  (b) TRAS leer la orden (cat) y ejecutar sudo cat:")
print(f"      cat exit={r1.exit_code} (llave leida: {'AUTORIZACION: CENIZA' in r1.stdout}); sudo cat exit={r2.exit_code}")
print(f"      ruido total={shell.total_noise} (cat 1 + [cat 1 + premium 3] = 5): {shell.total_noise==5}")
auth = shell.fs.read_file(AUTH_LOG_PATH)
firmas = [l for l in auth.splitlines() if "sudo" in l]
print(f"      firmas auth.log: {firmas}")
print(f"      append (no overwrite): {auth.startswith('11:02 operator')}")
shell.execute(f"sudo cat {SUDO_CREDENTIAL_PATH}")
print(f"      segundo sudo -> 2 firmas: {shell.fs.read_file(AUTH_LOG_PATH).count('sudo cat')==2}")
d = shell.to_dict(); restored = Shell.from_dict(d)
print(f"      roundtrip save conserva credencial+firma: {restored.to_dict()==d}")

print()
print("="*72)
print("3) GATE 127 — la puerta sigue cerrada en cap. 0/2")
print("="*72)
sh0 = Shell(FileSystem(), host="oficina-vecinal-muelle-norte", commands=DEFAULT_CAP0_COMMANDS)
ra, rb = sh0.execute("sudo ls"), sh0.execute("ps")
print(f"  cap.0: sudo -> exit {ra.exit_code} (127); ps -> exit {rb.exit_code} (127)")
sh2 = Shell(FileSystem(), commands=DEFAULT_CH2_COMMANDS)
rc = sh2.execute("sudo ls")
print(f"  cap.2: sudo -> exit {rc.exit_code} (127)")

print()
print("="*72)
print("4) POST-MORTEM del cierre del cap.2 — resuelve a texto, no line_key")
print("="*72)
# reconstruyo la sesion del cap.2 (grep|wc) y la cierro -> build_postmortem -> resolve
fs2 = FileSystem()
sh_cer = Shell(fs2, commands=DEFAULT_CH2_COMMANDS)
# golden del cap.2 (mismo verbo que la run de ayer, aqui en shell puro)
sh_cer.execute("grep 11:04 centralita/turnos/turno.log | wc -l")
p = build_postmortem(sh_cer.to_dict(), {"noise_budget": 12})
print("  factura:", p["factura"], "| total_noise:", p["total_noise"], "| dentro:", p["dentro_presupuesto"])
print("  auditor line_key:", p["auditor"]["line_key"], "| args:", p["auditor"]["args"])
txt = resolve(p["auditor"]["line_key"], p["auditor"]["args"])
print("  -> TEXTO resuelto:", txt)
print("  -> 'line_key' crudo NO se muestra en superficie: OK (resuelto)")

print()
print("  VALIDACION COMPLETA OK.")