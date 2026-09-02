"""scene_room — pintor de la sala del cap. 0 (Seath, 02/09).

ÚNICO sitio de `src/render/` que toca `pyxel.pset` (frontera core/render).
Todo lo demás es puro. El dibujo usa `Font5x7` píxel a píxel, idéntico a
`assets.pyxel_capture.draw_text_pyxel` y a `assets.tools.make_captures`.

No importa `core` a nivel top-level: el `shell` y el `host` llegan como
datos ya construidos por el generador (solo lectura).
"""

from __future__ import annotations

from typing import Any

from assets.font5x7 import Font5x7
from assets.palette import SEMANTIC

from render.theme import (
    BORDER_COLOR,
    CONTENT_X,
    CONTENT_Y,
    FRAME_X1,
    FRAME_X2,
    FRAME_Y1,
    FRAME_Y2,
    LINE_H,
    TITLE_COLOR,
)

_FONT = Font5x7()

# Códigos CP437 de box-drawing (copiados de assets.tools.make_captures).
_BOX_TL = 0xC9
_BOX_TR = 0xBB
_BOX_BL = 0xC8
_BOX_BR = 0xBC
_BOX_H = 0xCD
_BOX_V = 0xBA


def _draw_cp(codepoint: int, x: int, y: int, color: int) -> None:
    import pyxel

    for cx, col in enumerate(_FONT.glyph(codepoint)):
        for row in range(Font5x7.GLYPH_H):
            if (col >> row) & 1:
                pyxel.pset(x + cx, y + row, color)


def _draw_text(text: str, x: int, y: int, color: int) -> None:
    import pyxel

    for gi, cp in enumerate(_FONT.cp437_encode(text)):
        col_origin = gi * (Font5x7.GLYPH_W + Font5x7.TRACKING)
        for cx, column in enumerate(_FONT.glyph(cp)):
            for row in range(Font5x7.GLYPH_H):
                if (column >> row) & 1:
                    pyxel.pset(x + col_origin + cx, y + row, color)


def draw_box(x1: int, y1: int, x2: int, y2: int, color: int) -> None:
    """Marco box-drawing (┌─┐ │ └─┘) — idéntico al de make_captures."""
    h = Font5x7.GLYPH_W + Font5x7.TRACKING
    _draw_cp(_BOX_TL, x1, y1, color)
    _draw_cp(_BOX_TR, x2, y1, color)
    _draw_cp(_BOX_BL, x1, y2, color)
    _draw_cp(_BOX_BR, x2, y2, color)
    for x in range(x1 + h, x2, h):
        _draw_cp(_BOX_H, x, y1, color)
        _draw_cp(_BOX_H, x, y2, color)
    for y in range(y1 + Font5x7.GLYPH_H, y2, Font5x7.GLYPH_H):
        _draw_cp(_BOX_V, x1, y, color)
        _draw_cp(_BOX_V, x2, y, color)


def draw_terminal(shell: Any, host: str, user: str = "cero") -> None:
    """Dibuja la pantalla completa de la sala del cap. 0.

    - Título centrado con `host` (p. ej. `oficina-vecinal-muelle-norte`).
    - Marco en (6,14)→(312,84) en color `BORDER_COLOR`.
    - Contenido a (14,22) con pitch 10px: líneas de `terminal_lines`.

    Debe llamarse DENTRO del callback `draw()` de `Capture.capture`
    (tras `pyxel.cls`), no antes de `pyxel.run`.
    """
    # Import lazy para que los tests puros no exijan pyxel.
    from render.terminal import terminal_lines

    # Título centrado.
    tw = _FONT.text_size(host)[0]
    # Canvas 320 → centrado.
    title_x = (320 - tw) // 2
    _draw_text(host, title_x, 4, SEMANTIC[TITLE_COLOR])

    # Marco.
    draw_box(FRAME_X1, FRAME_Y1, FRAME_X2, FRAME_Y2, SEMANTIC[BORDER_COLOR])

    # Líneas de terminal.
    lines = terminal_lines(shell, host, user=user)
    y = CONTENT_Y
    for text, color_key in lines:
        if y + Font5x7.GLYPH_H > FRAME_Y2:
            break  # no desborda el marco
        _draw_text(text, CONTENT_X, y, SEMANTIC[color_key])
        y += LINE_H


def draw_room_frame_only() -> None:
    """Solo el marco + título, para smoke sin shell."""
    _draw_text("oficina-vecinal-muelle-norte", (320 - _FONT.text_size("oficina-vecinal-muelle-norte")[0]) // 2, 4, SEMANTIC[TITLE_COLOR])
    draw_box(FRAME_X1, FRAME_Y1, FRAME_X2, FRAME_Y2, SEMANTIC[BORDER_COLOR])
