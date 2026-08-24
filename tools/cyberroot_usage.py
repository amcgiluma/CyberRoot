#!/usr/bin/env python3
"""CyberRoot — panel de uso diario del Concilio.

Vuelca `opencode stats` desglosado por modelo a docs/USAGE.md en el repo
y hace commit+push. Se ejecuta como cron sin agente (no_agent=True) para
gastar cero tokens de razonamiento.

Salida (stdout): un resumen de una línea. Si no hay datos, stdout vacío.
"""
import subprocess, sys, os, datetime

REPO = "/home/juanma/CyberRoot"
USAGE = os.path.join(REPO, "docs", "USAGE.md")
DAYS = 1
# Ruta absoluta: los crons no heredan el PATH del shell interactivo.
OPENCODE = "/home/juanma/.opencode/bin/opencode"

def run(cmd):
    try:
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=60)
        return r.stdout
    except Exception as e:
        return f"ERR: {e}"

def main():
    today = datetime.date.today().isoformat()
    if not os.path.isdir(REPO):
        print(f"ERROR: repo no existe ({REPO})"); sys.exit(1)
    if not os.path.isfile(USAGE):
        with open(USAGE, "w") as f:
            f.write("# USAGE — Panel de uso del Concilio\n\n")
    # Métricas en crudo por modelo
    stats = run([OPENCODE, "stats", "--days", str(DAYS), "--models"])
    if "ERR:" in stats:
        print(stats.strip()); sys.exit(1)
    # Si no hay sesiones aún, stats es casi vacío → no escribir ruido
    if "Overview" not in stats and "COST" not in stats and "Sessions" not in stats:
        # La cabecera ASCII siempre está; detectar ausencia de filas de coste
        if stats.strip().count("┌") < 2:
            # No hay datos todavía → silencioso (nada que reportar)
            print("")
            return
    # Append del día
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(USAGE, "a") as f:
        f.write(f"\n## {stamp}\n```\n{stats}\n```\n")
    # commit + push
    subprocess.run(["git", "add", "docs/USAGE.md"], cwd=REPO)
    subprocess.run(["git", "commit", "-m", f"chore: panel de uso {today}"], cwd=REPO,
                   capture_output=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=REPO, capture_output=True)
    # Resumen de una línea para Telegram
    # extraer total cost
    total = "?"
    for line in stats.splitlines():
        if "Total Cost" in line:
            total = line.split("│")[2].strip() if "│" in line else line
    print(f"📊 Panel de uso actualizado ({today}): Total coste {total}. Ver docs/USAGE.md")

if __name__ == "__main__":
    main()