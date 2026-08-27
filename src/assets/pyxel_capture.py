"""Captura headless con Pyxel del render de la fuente 5×7 (hito H2).

Capa 2 del módulo de fuente de CyberRoot: dibuja texto con :class:`Font5x7`
píxel a píxel sobre un canvas Pyxel headless y vuelca un PNG nativo (la
evidencia). Complementa al rasterizador de referencia de Pillow
(:func:`assets.font5x7.render_text_pbm`), que es el contraste de estos tests.

Detalles de comportamiento verificados con pyxel 2.9.9 en headless:
  * ``pyxel.init(..., headless=True)`` funciona sin DISPLAY ni Xvfb.
  * Para obtener resolución NATIVA hay que pasar ``capture_scale=1`` en init
    (sin él, un canvas 320×180 produce un PNG 640×360).
  * Dibujar antes de ``pyxel.run`` se pierde; hay que dibujar dentro del
    callback ``draw()`` y hacer ``pyxel.screenshot`` justo después en el mismo
    frame.
  * ``pyxel.quit()`` dentro de un callback termina el proceso sin devolver
    control a quien llamó a ``pyxel.run`` (no se captura una ``SystemExit``
    en todas las build: aquí hard-exit). El trabajo posterior a la captura
    (p. ej. generar el zoom) debe realizarse en el hook ``on_screenshot``.

Cliente de la paleta CRT de §8.5 (:mod:`assets.palette`).
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Callable

import pyxel

from assets.font5x7 import Font5x7
from assets.palette import SEMANTIC, apply


class Capture:
    """Configura un canvas Pyxel headless y captura un frame como PNG."""

    def __init__(self, width: int = 320, height: int = 180) -> None:
        self.width = width
        self.height = height

    def capture(
        self,
        draw_fn: Callable[[], None],
        out_png: str,
        on_screenshot: Callable[[], None] | None = None,
    ) -> None:
        """Inicializa Pyxel headless, dibuja un frame y lo guarda en ``out_png``.

        Determinista: no hay RNG ni tiempo real en el dibujo. La paleta CRT
        (§8.5) se aplica antes del bucle y el frame capturado es el n.º 2.

        ``on_screenshot`` (opcional) se invoca justo después de ``screenshot``
        y antes de ``quit`` en el mismo frame. Está ahí porque en Pyxel 2.9.9
        en headless ``quit()`` termina el proceso sin devolver control a quien
        llamó a ``pyxel.run`` (ni una ``SystemExit`` capturable): cualquier
        trabajo posterior a la captura debe hacerse dentro de este hook.
        """
        pyxel.init(self.width, self.height, headless=True, capture_scale=1)
        apply()

        frame = {"n": 0}

        def update() -> None:  # pragma: no cover - requerido por pyxel.run
            pass

        def draw() -> None:
            if frame["n"] == 2:
                pyxel.cls(SEMANTIC["fondo"])
                draw_fn()
                pyxel.screenshot(out_png, scale=1)
                if on_screenshot is not None:
                    on_screenshot()
                pyxel.quit()
            frame["n"] += 1

        try:
            pyxel.run(update, draw)
        except SystemExit:
            # pyxel.quit() lanza SystemExit dentro de draw(); pyxel.run nunca
            # retorna normal. Esperado y correcto.
            pass


def draw_text_pyxel(
    text: str, x: int, y: int, color: int, font: Font5x7 | None = None
) -> None:
    """Dibuja ``text`` con :class:`Font5x7` usando ``pyxel.pset`` píxel a píxel.

    Cada glifo ocupa ``GLYPH_W``×``GLYPH_H`` px con ``TRACKING`` px (1) de
    separación. Convención de bits: bit 0 de cada columna es la FILA SUPERIOR
    (documentada en :class:`Font5x7`) y la columna 0 es la izquierda.
    """
    font = font or Font5x7()
    for gi, cp in enumerate(font.cp437_encode(text)):
        col_origin = gi * (Font5x7.GLYPH_W + Font5x7.TRACKING)
        for cx, column in enumerate(font.glyph(cp)):
            for row in range(Font5x7.GLYPH_H):
                if (column >> row) & 1:  # bit 0 = fila superior
                    pyxel.pset(x + col_origin + cx, y + row, color)


def zoom_png(src: str, factor: int) -> str:
    """Escala ``src`` a ``factor``× con PIL NEAREST para inspección humana.

    Devuelve la ruta del fichero ``.zoom{factor}x.png`` creado junto a ``src``.
    El PNG nativo de ``src`` queda intacto: la escala es solo para verlo.
    """
    from PIL import Image

    img = Image.open(src)
    w, h = img.size
    scaled = img.resize((w * factor, h * factor), Image.NEAREST)
    out = os.path.splitext(src)[0] + f".zoom{factor}x.png"
    scaled.save(out)
    return out


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m assets.pyxel_capture",
        description="Dibuja texto 5×7 con Pyxel headless y guarda un PNG nativo.",
    )
    parser.add_argument("--text", required=True, help="Texto a dibujar.")
    parser.add_argument("--x", type=int, default=0, help="X de la esquina superior izquierda.")
    parser.add_argument("--y", type=int, default=0, help="Y de la esquina superior izquierda.")
    parser.add_argument("--out", required=True, help="Ruta del PNG nativo de salida.")
    parser.add_argument(
        "--color",
        default="texto",
        choices=sorted(SEMANTIC),
        help="Color semántico (§8.5) para la tinta (por defecto: texto).",
    )
    parser.add_argument(
        "--zoom",
        type=int,
        default=0,
        help="Si >1, guarda además una copia escalada xN con PIL NEAREST.",
    )
    parser.add_argument("--w", type=int, default=320, help="Ancho del canvas Pyxel.")
    parser.add_argument("--h", type=int, default=180, help="Alto del canvas Pyxel.")
    args = parser.parse_args(argv)

    color = SEMANTIC[args.color]
    capture = Capture(args.w, args.h)
    hook: Callable[[], None] | None = None
    if args.zoom and args.zoom > 1:
        # El zoom se genera dentro del frame, tras screenshot y antes de quit:
        # en headless, pyxel.quit() termina el proceso sin devolver control.

        def _do_zoom() -> None:
            zoom_png(args.out, args.zoom)

        hook = _do_zoom
    capture.capture(
        lambda: draw_text_pyxel(args.text, args.x, args.y, color),
        args.out,
        on_screenshot=hook,
    )

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main(sys.argv[1:]))