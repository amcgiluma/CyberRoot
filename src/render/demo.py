"""demo — demo reproducible del render v0 (Seath, 02/09).

Genera UNA sala real del cap. 0 con seed fija, ejecuta un `ls` del
sandbox y captura la pantalla con `assets.pyxel_capture.Capture`.

Uso:
    PYTHONPATH=src .venv/bin/python -m render.demo
    PYTHONPATH=src .venv/bin/python -m render.demo --seed 42 --out src/render/golden/cap0-room.png

Reproducibilidad: sin RNG propio, sin timestamps en el dibujo.
Segunda ejecución → PNG byte-idéntico (sha256 estable).
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

# El demo solo corre como script; no es importado por tests puros.


def _run(seed: int, out_png: str) -> str:
    # Imports lazy: no contaminan el import de `render` en tests puros.
    from core.generator import generate, new_session
    from core.generator.chapter0 import OFFICE_DIR
    from assets.pyxel_capture import Capture, zoom_png
    from assets.palette import SEMANTIC
    from render.scene_room import draw_terminal

    inc = generate(seed, chapter=0)
    shell = new_session(inc)
    # Ejecutar un comando real contra el FS virtual para tener salida.
    shell.execute(f"ls {OFFICE_DIR}")

    # Captura headless (patrón validado en assets: frame 2 + hook zoom).
    # out_png se resuelve a absoluto: pyxel.screenshot falla con relativos
    # tras el init en algunas builds (cf. make_captures usa GOLDEN_DIR absoluto).
    out_path = Path(out_png).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cap = Capture(320, 180)

    def _draw():
        draw_terminal(shell, inc.room.host, user="cero")

    def _zoom():
        zoom_png(str(out_path), 3)

    cap.capture(_draw, str(out_path), on_screenshot=_zoom)

    # El proceso termina vía pyxel.quit() hard-exit; si llegamos aquí
    # es porque Capture lo capturó con SystemExit. Devolvemos el out.
    return str(out_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m render.demo")
    parser.add_argument("--seed", type=int, default=42, help="Seed de la sala (default 42).")
    parser.add_argument(
        "--out",
        default="src/render/golden/cap0-room.png",
        help="PNG nativo de salida (320×180).",
    )
    args = parser.parse_args(argv)

    # _run hace pyxel.quit() hard-exit, así que el zoom y el print deben
    # hacerse ANTES o en el hook. Aquí delegamos todo a _run y no retornamos.
    out = _run(args.seed, args.out)
    # Si Capture no hard-exiteó (en algunos entornos sí retorna), imprimimos.
    try:
        data = Path(out).read_bytes()
        sha = hashlib.sha256(data).hexdigest()[:12]
        print(f"demo cap0 seed={args.seed} → {out} sha256:{sha}")
        zoom = out.replace(".png", ".zoom3x.png")
        if Path(zoom).exists():
            print(f"  zoom: {zoom}")
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
