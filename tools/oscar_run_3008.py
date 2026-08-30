"""Run de referencia OSCAR 30/08 — zona: circuito competencia→unlock→save."""
import os, sys
os.environ.setdefault("PYTHONPATH", "src")
from core.generator import generate, new_session
from core.state import GameState, save_game, load_game
from core.progression import evaluate_unlocks

inc = generate("oscar-20260830-r1", 0, variant="canonical")

def L(sep="="):
    print(sep * 70)

print(L(), "\nRUN DE REFERENCIA — 30/08 — save limpio, camino del cap. 0", L())
print("Sala:", inc.room.id)
print("Contrato:", inc.contract.objective_key, "| karma:", inc.contract.karma_hint)
print("Objetivo:", inc.room.objective.story_key, "| pool:", inc.room.concept_pool)
print("Decoys:", list(inc.room.decoys) or "(none)")
print("Presupuesto de ruido:", inc.room.noise_budget)
print("Canon:", [(list(s.argv), s.expect_exit) for s in inc.room.canon.steps])

print("\n[F1] cwd nace en:", new_session(inc).cwd, "| scaffold.initial_cwd():",
      inc.scaffold.initial_cwd())

sh = new_session(inc)
factura = []
def cuenta(line):
    res = sh.execute(line)
    factura.append((line, res.noise[0].data["amount"] if res.noise else 0,
                    res.exit_code, (res.stderr or "")[:70]))
    return res

print("\n[F2] El viaje del dossier (aprender por necesidad, cumbre cp):")
for s in inc.room.canon.steps:
    cmd = " ".join(s.argv)
    r = cuenta(cmd)
    tag = "OK " if r.exit_code == 0 else "FAIL"
    print(f"   ${cmd}  -> {tag} exit={r.exit_code}")
    if cmd.startswith("cat") and r.stdout:
        pass

print("\n[F2b] Curiosidad honesta + error lector:")
cuenta("ls /srv/oficina-vecinal-muelle-norte")
cuenta("ls -l")
cuenta("cp /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt /usb/")

print("\n[FACTURA] ruido total tras el viaje:", sh.total_noise, "de",
      inc.room.noise_budget)
for l, d, ec, err in factura:
    extra = f"  ({err})" if err and ec != 0 else ""
    print(f"   +{d:>2}  $ {l}  [exit {ec}]{extra}")

print("\n[F3] §4.2 — el unlock NO se dispara sin la evidencia (sin cp a /usb):")
inc2 = generate("oscar-20260830-noev", 0)
sh2 = new_session(inc2)
sh2.execute("ls /srv/oficina-vecinal-muelle-norte")
sh2.execute("cat /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt")
sh2.execute("ls /usb")
gs_no = GameState(shell=sh2)
nuevos_no = evaluate_unlocks(gs_no)
print("   sin cp a /usb -> newly:", nuevos_no, "| knowledge:", dict(gs_no.knowledge))

print("\n[F4] La sesión REAL (con cp a /usb) -> unlock + save -> load:")
gs = GameState(shell=sh)
print("   knowledge ANTES:", dict(gs.knowledge))
nuevos = evaluate_unlocks(gs)
print("   newly_dominated:", nuevos, "| knowledge tras evaluación:", dict(gs.knowledge))

save_path = "/tmp/oscar_cap0_save.json"
save_game(gs, save_path)
gs2 = load_game(save_path)
print("   ROUNDTRIP: knowledge persiste =", dict(gs2.knowledge))
print("   tick tras load:", gs2.shell.tick, "| total_noise tras load:",
      gs2.shell.total_noise)
print("   idempotencia (2a eval):", evaluate_unlocks(gs2), "(vacio = no re-marca)")
print("   VEREDICTO: c.cp dominado en save:", gs2.knowledge.get("c.cp") is True)
print(L())