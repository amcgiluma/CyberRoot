"""theme — geometría y colores del render v0 (Seath, 02/09).

Re-exporta la paleta CRT de `assets.palette` y fija la geometría
de la terminal (320×180 nativo, pitch 10px, 46 cols × 17 líneas).

No importa `pyxel` a nivel top-level: el binding a `pyxel.colors`
vive en `apply()` lazy, así los tests puros no necesitan display.
"""

from __future__ import annotations

from assets.palette import SEMANTIC

# Canvas nativo del juego (assets/pyel_capture lo usa como default).
CANVAS_W = 320
CANVAS_H = 180

# Terminal enmarcada (coords del marco box-drawing, idénticas a
# assets.tools.make_captures._c1 para coherencia visual).
FRAME_X1 = 6
FRAME_Y1 = 14
FRAME_X2 = 312
FRAME_Y2 = 84

# Contenido dentro del marco (margen 8px desde el borde).
CONTENT_X = 14
CONTENT_Y = 22
LINE_H = 10  # pitch vertical de la fuente + tracking (7 + 3)

# Ancho útil en caracteres (validado en assets/README: 46 cols).
TERM_COLS = 46

# Roles semánticos → clave de SEMANTIC (un idioma, una clave por slot).
PROMPT_COLOR = "texto_brillante"
OUTPUT_COLOR = "texto"
DIM_COLOR = "texto_dim"
BORDER_COLOR = "texto"
TITLE_COLOR = "texto_dim"

__all__ = [
    "CANVAS_W",
    "CANVAS_H",
    "FRAME_X1",
    "FRAME_Y1",
    "FRAME_X2",
    "FRAME_Y2",
    "CONTENT_X",
    "CONTENT_Y",
    "LINE_H",
    "TERM_COLS",
    "PROMPT_COLOR",
    "OUTPUT_COLOR",
    "DIM_COLOR",
    "BORDER_COLOR",
    "TITLE_COLOR",
    "SEMANTIC",
]
