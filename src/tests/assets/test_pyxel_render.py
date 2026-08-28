"""Tests del render Pyxel headless (hito H2).

Valida PÍXEL A PÍXEL el render de Pyxel contra el rasterizador de referencia
:func:`assets.font5x7.render_text_pbm`. Cada test que necesita Pyxel arranca
el CLI ``assets.pyxel_capture`` en un SUBPROCESO (solo con el venv del repo y
``PYTHONPATH=src``) para aislar el estado global de Pyxel por test.

Estos tests NO importan ``pyxel`` en este proceso (nada de estado compartido);
si Pyxel no está instalado en el entorno, se saltan con ``importorskip``.
"""

import os
import subprocess
import sys

import pytest

from PIL import Image

pytest.importorskip("pyxel")

REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
SRC = os.path.join(REPO_ROOT, "src")

sys.path.insert(0, SRC)

from assets.font5x7 import Font5x7  # noqa: E402
from assets import palette  # noqa: E402


def _run_cli(*args: str) -> None:
    """Ejecuta el CLI de captura Pyxel en subproceso, aislado por test."""
    env = dict(os.environ)
    # Subproceso con su propio estado de Pyxel; nada de esto contamina tests.
    env["PYTHONPATH"] = SRC
    proc = subprocess.run(
        [sys.executable, "-m", "assets.pyxel_capture", *args],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, (
        f"CLI pyxel_capture falló (rc={proc.returncode})\n"
        f"stdout: {proc.stdout}\nstderr: {proc.stderr}"
    )


# ---------------------------------------------------------------------------
# Paleta CRT (§8.5)
# ---------------------------------------------------------------------------

def test_paleta_constantes():
    # Los 5 semánticos obligatorios de §8.5 existen en SEMANTIC (mapa nombre→slot).
    for name in ("fondo", "texto", "aviso", "amenaza", "hallazgo"):
        assert name in palette.SEMANTIC

    # Los 5 semánticos tienen valores RGB plausibles (0..255, con al menos un
    # canal dominante, y el fondo no es blanco).
    assert palette.BLACK[1] > palette.BLACK[0]      # leve tinte verde en el fondo
    assert palette.BLACK != (255, 255, 255)
    assert palette.PHOSPHOR[1] > 120                # verde vivo
    assert palette.AMBER[1] > palette.AMBER[2]      # ámbar: rojo>azul
    assert palette.LUMEN_RED[0] > 200               # rojo dominante
    assert palette.GOLD[0] > 200 and palette.GOLD[1] > 100

    # Exactamente 16 slots definidos.
    assert len(palette.SEMANTIC) >= 5
    slots = {palette.SEMANTIC[k] for k in palette.SEMANTIC}
    assert 0 <= min(slots) and max(slots) <= 15
    # Al menos los 16 índices están cubiertos por el mapa SEMANTIC.
    assert set(range(16)).issubset(slots)


# ---------------------------------------------------------------------------
# Render pixel a pixel: Pyxel vs rasterizador de referencia
# ---------------------------------------------------------------------------

def test_render_A_coincide_con_referencia_pil(tmp_path):
    """Render Pyxel de 'A' en (2,2) == rasterizador de referencia, píxel a píxel."""
    out_png = str(tmp_path / "A.png")
    _run_cli("--text", "A", "--x", "2", "--y", "2", "--out", out_png, "--color", "texto")

    img = Image.open(out_png)
    # capture_scale=1 → resolución nativa del canvas 320×180.
    assert img.size == (320, 180)

    font = Font5x7()
    cols = font.glyph(ord("A"))
    assert cols == (0x7C, 0x12, 0x11, 0x12, 0x7C)

    texto_rgb = palette.PHOSPHOR
    fondo_rgb = palette.BLACK

    # Bit 0 de cada columna = fila superior. Col c, fila r → píxel (x+c, y+r).
    for c, col in enumerate(cols):
        for r in range(Font5x7.GLYPH_H):
            expected = texto_rgb if (col >> r) & 1 else fondo_rgb
            got = img.getpixel((2 + c, 2 + r))
            assert got == expected, f"píxel ({2 + c},{2 + r}) esperaba {expected}, era {got}"


def test_render_pangrama_acentos(tmp_path):
    """Render Pyxel de 'áéíóúñ¿¡': la tinta prevista es color texto y el acento de 'á' existe."""
    out_png = str(tmp_path / "pangrama.png")
    _run_cli("--text", "áéíóúñ¿¡", "--x", "1", "--y", "1", "--out", out_png, "--color", "texto")

    img = Image.open(out_png)
    assert img.size == (320, 180)

    font = Font5x7()
    texto = "áéíóúñ¿¡"
    data = font.cp437_encode(texto)
    assert data == bytes([0xA0, 0x82, 0xA1, 0xA2, 0xA3, 0xA4, 0xA8, 0xAD])
    assert font.glyph(0xA0) == (0x20, 0x54, 0x54, 0x79, 0x41)  # á

    texto_rgb = palette.PHOSPHOR
    fondo_rgb = palette.BLACK

    # 1) Todos los píxeles de tinta previstos (calculados con Font5x7) son color texto.
    for gi, cp in enumerate(data):
        col_origin = gi * (Font5x7.GLYPH_W + Font5x7.TRACKING)
        for c, col in enumerate(font.glyph(cp)):
            for r in range(Font5x7.GLYPH_H):
                if (col >> r) & 1:
                    assert img.getpixel((1 + col_origin + c, 1 + r)) == texto_rgb

    # 2) El acento de 'á' existe: hay tinta en la fila superior (r=0) del primer glifo.
    toprow_ink = any(
        (col >> 0) & 1 for col in font.glyph(0xA0)
    )
    assert toprow_ink
    # En el PNG, ese trozo concreto no debe ser fondo.
    assert any(
        img.getpixel((1 + c, 1)) != fondo_rgb for c in range(Font5x7.GLYPH_W)
    )


def test_zoom_png(tmp_path):
    """--zoom 4: dimensión y píxel (0,0) coinciden con el nativo."""
    out_png = str(tmp_path / "zoom.png")
    _run_cli("--text", "A", "--x", "2", "--y", "2", "--out", out_png, "--color", "texto", "--zoom", "4")

    native = Image.open(out_png)
    assert native.size == (320, 180)

    zoom_path = out_png.rsplit(".", 1)[0] + ".zoom4x.png"
    assert os.path.exists(zoom_path)
    zoom = Image.open(zoom_path)
    assert zoom.size == (native.size[0] * 4, native.size[1] * 4)
    assert zoom.size == (1280, 720)
    assert zoom.getpixel((0, 0)) == native.getpixel((0, 0))