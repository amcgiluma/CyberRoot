"""Hito H3 (PLAN.md) — Capturas oficiales reproducibles del módulo de fuente 5×7.

Genera las 3 capturas PNG nativas (320×180) del módulo de fuente + un zoom ×3 de
cada una, en ``src/assets/golden/``, con sha256 ESTABLES entre ejecuciones
(determinista: sin RNG ni timestamps en el dibujo).

Uso (desde la raíz del repo):
    PYTHONPATH=src .venv/bin/python -m assets.tools.make_captures

Salidas (en ``src/assets/golden/``):
    captura-01-prompt-terminal.png     (+ .zoom3x.png)
    captura-02-informe-auditor.png     (+ .zoom3x.png)
    captura-03-hoja-glifos.png         (+ .zoom3x.png)

El script se debe poder correr N veces y producir PNG idénticos byte a byte.
``make_captures.py --clean`` además borra el directorio golden/ antes de
regenerar; el resultado es idéntico, de modo que golden/ puede regenerarse en
cualquier momento.

POR QUÉ CADA CAPTURA VIVE EN SU PROPIO PROCESO
------------------------------------------------
``pyxel.quit()`` (pyxel 2.9.9 headless) es un hard-exit: termina el proceso sin
devolver control a ``pyxel.run`` (la ``SystemExit`` no se captura en todas las
builds; aquí no se captura) y una segunda ``pyxel.init`` en el MISMO proceso
falla al reinicializar la pila de audio. Por eso este orquestador lanza un
subproceso por captura (de SÍ MISMO, con ``--capture N``), y cada subproceso
llama a ``Capture.capture()`` como LIBRERÍA (no al CLI ``assets.pyxel_capture``)
pasando el zoom en el hook ``on_screenshot``, que se ejecuta dentro del frame,
justo antes de ``pyxel.quit()``.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

from assets.font5x7 import Font5x7
from assets.pyxel_capture import Capture, draw_text_pyxel, zoom_png
from assets.palette import SEMANTIC

# ---------------------------------------------------------------------------
# Rutas y constantes
# ---------------------------------------------------------------------------
MODULE_DIR = Path(__file__).resolve().parent      # src/assets/tools
ASSETS_DIR = MODULE_DIR.parent                     # src/assets
GOLDEN_DIR = ASSETS_DIR / "golden"                 # src/assets/golden
SRC_DIR = ASSETS_DIR.parent                        # src
REPO_ROOT = SRC_DIR.parent                         # raíz del repo

WIDTH, HEIGHT = 320, 180
ZOOM = 3

_C = SEMANTIC
FONT = Font5x7()

# Códigos CP437 de box-drawing (verificados con tinta en la tabla).
_BOX_TL = 0xC9  # ┌
_BOX_TR = 0xBB  # ┐
_BOX_BL = 0xC8  # └
_BOX_BR = 0xBC  # ┘
_BOX_H = 0xCD   # ─
_BOX_V = 0xBA   # │


def draw_cp(codepoint: int, x: int, y: int, color: int) -> None:
    """Dibuja un glifo CP437 por su código (box-drawing p. ej.)."""
    import pyxel  # nos limitamos a pyxel.pset, igual que draw_text_pyxel

    for cx, col in enumerate(FONT.glyph(codepoint)):
        for row in range(Font5x7.GLYPH_H):
            if (col >> row) & 1:  # bit 0 = fila superior
                pyxel.pset(x + cx, y + row, color)


def draw_box(
    x1: int, y1: int, x2: int, y2: int, color: int,
) -> None:
    """Dibuja un marco de box-drawing (┌─┐ │ └─┘) dentro del canvas.

    La rejilla usa el paso real de la fuente: 6 px en horizontal (5 de glifo
    + 1 de tracking) y 7 px en vertical (altura del glifo).
    """
    h = Font5x7.GLYPH_W + Font5x7.TRACKING
    draw_cp(_BOX_TL, x1, y1, color)
    draw_cp(_BOX_TR, x2, y1, color)
    draw_cp(_BOX_BL, x1, y2, color)
    draw_cp(_BOX_BR, x2, y2, color)
    for x in range(x1 + h, x2, h):
        draw_cp(_BOX_H, x, y1, color)
        draw_cp(_BOX_H, x, y2, color)
    for y in range(y1 + Font5x7.GLYPH_H, y2, Font5x7.GLYPH_H):
        draw_cp(_BOX_V, x1, y, color)
        draw_cp(_BOX_V, x2, y, color)


def draw_prompt_line(prompt: str, rest: str, x: int, y: int) -> None:
    """Dibuja una línea ``$ ...``: el prompt ($) brillante, el resto en texto."""
    draw_text_pyxel(prompt, x, y, _C["texto_brillante"])
    draw_text_pyxel(
        rest,
        x + FONT.text_size(prompt)[0],
        y,
        _C["texto"],
    )


# ---------------------------------------------------------------------------
# Captura 1 — prompt / terminal del cap. 0
# ---------------------------------------------------------------------------
def _c1_prompt_terminal() -> None:
    # Título (barra) sobre el marco.
    title = "oficina-vecinal-muelle-norte"
    tw = FONT.text_size(title)[0]
    draw_text_pyxel(title, (WIDTH - tw) // 2, 4, _C["texto_dim"])

    # Marco. x=6..312, y=14..84.
    draw_box(6, 14, 312, 84, _C["texto"])

    # Contenido: margen izquierdo 14 (marco 6 + 8), líneas cada 10 px.
    x = 14
    draw_text_pyxel(
        "conectando → oficina-vecinal-muelle-norte...", x, 22, _C["texto_dim"]
    )
    draw_prompt_line("$", " ls", x, 32)
    draw_text_pyxel("nombre_de_proveedor.txt  log.txt  README", x, 42, _C["texto"])
    draw_prompt_line("$", " cat nombre_de_proveedor.txt", x, 52)
    draw_text_pyxel(
        "CANDELAS · proveedor nº 47 · facturación externa", x, 62, _C["texto"]
    )
    draw_text_pyxel("· 114 facturas/mes", x, 72, _C["texto"])


# ---------------------------------------------------------------------------
# Captura 2 — informe del Auditor (§4.7, sobrio, sin marco)
# ---------------------------------------------------------------------------
def _c2_informe_auditor() -> None:
    lines = [
        ("AUDITOR — registro de sesión", _C["texto_brillante"]),
        ("1 fichero accedido, 0 marcados para borrado.", _C["texto"]),
        ("Salida limpia. Continuidad del servicio:", _C["texto"]),
        ("no interrumpida.", _C["texto"]),
        ("Expediente 000: expulsión un 40%.", _C["texto"]),
    ]
    y = 8
    for text, color in lines:
        draw_text_pyxel(text, 8, y, color)
        y += 10


# ---------------------------------------------------------------------------
# Captura 3 — hoja de glifos (criterio de aceptación) + acentos CP437
# ---------------------------------------------------------------------------
_ASCII_START = 32
_ASCII_END = 126  # inclusive
_GLYPHS = _ASCII_END - _ASCII_START + 1  # 95


def _c3_hoja_glifos() -> None:
    COLS = 12
    ROWS = 8
    CELL_W = 20
    CELL_H = 18
    start_x = 40  # centrado horizontal: (320 - 12*20) / 2
    start_y = 12

    for cell in range(_GLYPHS):
        row, col = divmod(cell, COLS)
        cx = start_x + col * CELL_W
        cy = start_y + row * CELL_H
        cp = _ASCII_START + cell
        # Glifo centrado en la celda.
        gx = cx + (CELL_W - Font5x7.GLYPH_W) // 2
        draw_text_pyxel(chr_cp(cp), gx, cy, _C["texto"])
        # Su código en texto_dim, debajo.
        code = "%03d" % cp
        cx_code = cx + (CELL_W - FONT.text_size(code)[0]) // 2
        draw_text_pyxel(code, cx_code, cy + 9, _C["texto_dim"])

    # Línea de muestra con los acentos CP437 + sus códigos, debajo de la grilla.
    accent_glyphs = "áéíóúñü¡¿ªº·→"
    accent_codes = "A0 82 A1 A2 A3 A4 81 AD A8 A6 A7 FA 1A"
    grid_bottom = start_y + ROWS * CELL_H
    ay = grid_bottom + 2
    draw_text_pyxel(accent_glyphs, 8, ay, _C["texto"])
    draw_text_pyxel(accent_codes, 8, ay + 10, _C["texto_dim"])


def chr_cp(codepoint: int) -> str:
    """Devuelve el carácter CP437 de ``codepoint`` para dibujarlo con Font5x7.

    Reutiliza el codec stdlib: el inverso de ``cp437_encode``. Los caracteres
    de control (0x00-0x1F) se devuelven como tal; aquí solo se usan 32..126.
    """
    return bytes([codepoint]).decode("cp437")


# ---------------------------------------------------------------------------
# Capturas (lista ordenada; índice = orden de documento)
# ---------------------------------------------------------------------------
_CAPTURES: list[tuple[str, Callable[[], None]]] = [
    # (nombre base, dibujante)
    ("captura-01-prompt-terminal", _c1_prompt_terminal),
    ("captura-02-informe-auditor", _c2_informe_auditor),
    ("captura-03-hoja-glifos", _c3_hoja_glifos),
]


def _render_one(which: int) -> None:
    """Dibuja y guarda la captura ``which`` y su zoom, en ESTE proceso.

    ``Capture.capture()`` hard-exits vía ``pyxel.quit()``, así que el zoom se
    genera dentro del frame (hook ``on_screenshot``), justo antes de ``quit``.
    """
    name, draw_fn = _CAPTURES[which]
    out = str(GOLDEN_DIR / (name + ".png"))
    capture = Capture(WIDTH, HEIGHT)

    def do_zoom() -> None:
        # pyxel.quit() hard-exitea justo después del hook; el zoom tiene que
        # generarse aquí, dentro del frame y antes de quit().
        zoom_png(out, ZOOM)

    capture.capture(draw_fn, out, on_screenshot=do_zoom)


def _run_capture_subprocess(which: int) -> None:
    """Lanza un subproceso (de este módulo) que hace una captura, aislado.

    Necesario porque cada ``Capture.capture()`` hard-exits su proceso.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_DIR)
    proc = subprocess.run(
        [sys.executable, "-m", "assets.tools.make_captures", "--capture", str(which)],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"captura {which} falló (rc={proc.returncode})\n"
            f"stdout: {proc.stdout}\nstderr: {proc.stderr}"
        )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--clean":
        if GOLDEN_DIR.exists():
            shutil.rmtree(GOLDEN_DIR)
        argv = argv[1:]
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    # Modo subproceso: una sola captura.
    if argv and argv[0] == "--capture":
        which = int(argv[1])
        _render_one(which)
        return 0

    if argv:
        print(__doc__)
        return 2

    # Orquestador: elimina capturas previas y regenera (borra/regenera ≡ idéntico).
    for name, _ in _CAPTURES:
        for old in GOLDEN_DIR.glob(name + "*.png"):
            old.unlink()

    for which in range(len(_CAPTURES)):
        _run_capture_subprocess(which)

    for name, _ in _CAPTURES:
        native = GOLDEN_DIR / (name + ".png")
        zoom = GOLDEN_DIR / (name + f".zoom{ZOOM}x.png")
        if not native.exists() or not zoom.exists():
            raise RuntimeError(f"falta salida esperada: {native} o {zoom}")

    print(f"Capturas oficiales regeneradas en {GOLDEN_DIR}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())