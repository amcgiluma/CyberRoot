"""Tests unitarios de la capa 1 (parser puro + rasterizador de referencia).

Pytest puro: sin fixtures de red, sin sleep, 100 % determinista y sin Pyxel.
"""

import os
import sys

import pytest

# El módulo vive en src/assets/font5x7.py; exponemos su carpeta sin exigir
# que src/assets sea un paquete instalado.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from font5x7 import Font5x7, render_text_pbm


# ---------------------------------------------------------------------------
# Tabla / glifos
# ---------------------------------------------------------------------------

def test_tabla_tiene_1280_bytes():
    assert len(Font5x7.FONT_BYTES) == 1280  # 256 glifos × 5 columnas


def test_todos_los_glifos_son_bytes_validos():
    for byte in Font5x7.FONT_BYTES:
        assert 0 <= byte <= 0xFF


def test_glyph_A_golden():
    # Golden del upstream Adafruit-GFX (verificado contra glcdfont.c).
    assert Font5x7().glyph(0x41) == (0x7C, 0x12, 0x11, 0x12, 0x7C)


def test_glyph_minuscula_a_golden():
    assert Font5x7().glyph(0x61) == (0x20, 0x54, 0x54, 0x78, 0x40)


def test_glyph_cero_golden():
    assert Font5x7().glyph(0x30) == (0x3E, 0x51, 0x49, 0x45, 0x3E)


def test_glyph_a_acento_golden():
    # á con acento (CP437 0xA0).
    assert Font5x7().glyph(0xA0) == (0x20, 0x54, 0x54, 0x79, 0x41)


def test_glyph_enie_golden():
    # ñ con tilde en fila 1 (CP437 0xA4).
    assert Font5x7().glyph(0xA4) == (0x00, 0x7A, 0x0A, 0x0A, 0x72)


def test_glyph_fuera_de_rango_lanza_valueerror():
    f = Font5x7()
    for bad in (-1, 256, 1000):
        with pytest.raises(ValueError):
            f.glyph(bad)


def test_glyph_en_bordes_no_lanza():
    f = Font5x7()
    assert len(f.glyph(0x00)) == 5
    assert len(f.glyph(0xFF)) == 5


# ---------------------------------------------------------------------------
# Codificación CP437
# ---------------------------------------------------------------------------

def test_cp437_encode_pangrama_acentos():
    f = Font5x7()
    assert f.cp437_encode("áéíóúñü¡¿") == bytes(
        [0xA0, 0x82, 0xA1, 0xA2, 0xA3, 0xA4, 0x81, 0xAD, 0xA8]
    )


def test_cp437_encode_ordinales():
    f = Font5x7()
    assert f.cp437_encode("ª") == b"\xa6"
    assert f.cp437_encode("º") == b"\xa7"


def test_cp437_encode_ascii_identidad():
    f = Font5x7()
    assert f.cp437_encode("ABCabc012") == b"ABCabc012"


# ---------------------------------------------------------------------------
# text_size
# ---------------------------------------------------------------------------

def test_text_size_anchos():
    f = Font5x7()
    assert f.text_size("A") == (5, 7)
    assert f.text_size("AB") == (11, 7)  # (5+1)*2 - 1

def test_text_size_vacio_documentado():
    # String vacío → ancho mínimo de un glifo (5,7), coherente con render.
    f = Font5x7()
    assert f.text_size("") == (5, 7)


def test_text_size_acentos_mismo_ancho():
    f = Font5x7()
    assert f.text_size("áé") == (11, 7)


# ---------------------------------------------------------------------------
# render_text_pbm
# ---------------------------------------------------------------------------

def test_render_pbm_dimensiones_pangrama():
    img = render_text_pbm("áé")
    # (5+1)*2 - 1 = 11 px de ancho, 7 de alto.
    assert img.size == (11, 7)
    assert img.mode == "L"


def test_render_pbm_pinta_tinta():
    img = render_text_pbm("áé")
    values = img.tobytes()
    assert any(v == 1 for v in values)  # >0 píxeles con valor fg


def test_render_pbm_espacio_es_todo_bg():
    img = render_text_pbm(" ")
    assert all(v == 0 for v in img.tobytes())


def test_render_pbm_escala2_multipla():
    img = render_text_pbm("A", scale=2)
    assert img.size == (10, 14)


def test_render_pbm_vacio_coherente_con_text_size():
    # String vacío → imagen mínima de (5,7) toda bg (mismo criterio que text_size).
    img = render_text_pbm("")
    assert img.size == (5, 7)
    assert all(v == 0 for v in img.tobytes())


# ---------------------------------------------------------------------------
# Extensión tipográfica (CHAR_EXTENSIONS)
# ---------------------------------------------------------------------------

def test_extension_flechas_dos():
    # El codec cp437 de Python no codifica →; la tabla SÍ dibuja las flechas
    # DOS en 0x18-0x1B (verificado byte a byte contra glcdfont.c.ref).
    f = Font5x7()
    assert f.cp437_encode("→") == b"\x1a"
    assert f.cp437_encode("←") == b"\x1b"
    assert f.cp437_encode("↑") == b"\x18"
    assert f.cp437_encode("↓") == b"\x19"
    # El glifo de → tiene tinta: flecha reconocible (columna 2 = 0x2A).
    assert f.glyph(0x1A) == (0x08, 0x08, 0x2A, 0x1C, 0x08)


def test_extension_em_dash_reutiliza_linea_horizontal():
    # '—' no tiene glifo propio: se reutiliza 0xC4 (box-drawing ─).
    # Decisión documentada en CHAR_EXTENSIONS; 0xC4 = 5 filas centrales.
    f = Font5x7()
    assert f.cp437_encode("—") == b"\xc4"
    assert f.glyph(0xC4) == (0x10, 0x10, 0x10, 0x10, 0x10)


def test_extension_mixta_con_cp437_base():
    # Línea real del cap. 0: conectando → oficina-vecinal-muelle-norte...
    f = Font5x7()
    enc = f.cp437_encode("conectando → oficina")
    assert b"\x1a" in enc and "conectando ".encode("cp437") in enc


def test_extension_no_inventa_glifo_para_ellipsis():
    # '…' NO existe en la tabla: debe fallar alto y claro (los textos usan ...).
    with pytest.raises(UnicodeEncodeError):
        Font5x7().cp437_encode("…")


# ---------------------------------------------------------------------------
# Ida y vuelta
# ---------------------------------------------------------------------------

def test_ida_vuelta_caracteres_representativos():
    f = Font5x7()
    texto = "áéíóúñü¡¿ABCabc012"
    for byte in f.cp437_encode(texto):  # 0..255 por construcción
        assert len(f.glyph(byte)) == 5  # no lanza