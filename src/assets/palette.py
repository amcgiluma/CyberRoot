"""Paleta CRT de 16 colores estilo fósforo para CyberRoot (DESIGN §8.5).

Paleta v1 calibrable de un monitor de fósforo: negro de fondo con leve tinte
verde, rampa de verdes fósforo (estilo P1/P3 de tubo), ámbar, rojos de alerta,
dorado y grises fríos. Solo 16 slots, como exige la paleta de Pyxel.

Los 5 semánticos obligatorios de §8.5 se exponen como constantes documentadas
con su significado:
  * :data:`BLACK`       — fondo (negro profundo con leve tinte verde).
  * :data:`PHOSPHOR`    — texto base, verde fósforo estilo P1.
  * :data:`AMBER`       — aviso.
  * :data:`LUMEN_RED`   — amenaza/alerta (verde fósforo vivo, denominado Lumen).
  * :data:`GOLD`        — hallazgo crítico.

Para no exigir ``import pyxel`` a quien solo quiera los valores RGB, el accesso
a ``pyxel.colors`` está confinado a :func:`apply`.
"""

from __future__ import annotations

from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Valores RGB (tiples (r, g, b) en 0..255). v1 calibrables.
# ---------------------------------------------------------------------------

# -- Negro de fondo: profundo, con un leve tinte verde fantasma ----------
BLACK: Tuple[int, int, int] = (4, 10, 8)

# -- Verdes fósforo (tubo) -----------------------------------------------
PHOSPHOR: Tuple[int, int, int] = (33, 255, 105)          # P1 verde base (texto)
TEXTO_DIM: Tuple[int, int, int] = (22, 110, 60)          # verde atenuado
TEXTO_BRILLANTE: Tuple[int, int, int] = (168, 255, 186)  # verde sobresaturado
VERDE_OSCURO: Tuple[int, int, int] = (10, 55, 34)

# -- Ámbar / dorado / naranja ---------------------------------------------
AMBER: Tuple[int, int, int] = (255, 176, 0)
GOLD: Tuple[int, int, int] = (255, 200, 40)
NARANJA: Tuple[int, int, int] = (255, 132, 24)

# -- Rojos de alerta --------------------------------------------------------
LUMEN_RED: Tuple[int, int, int] = (255, 45, 60)
ROJO_APAGADO: Tuple[int, int, int] = (150, 28, 38)

# -- Información / espectro -------------------------------------------------
CYAN: Tuple[int, int, int] = (80, 220, 255)
MAGENTA: Tuple[int, int, int] = (255, 80, 200)

# -- Grises fríos -----------------------------------------------------------
GRIS_FRIO: Tuple[int, int, int] = (188, 200, 210)
GRIS_OSCURO: Tuple[int, int, int] = (96, 108, 120)

# -- Blanco de fósforo quemado ---------------------------------------------
BLANCO_FOSFORO: Tuple[int, int, int] = (232, 246, 236)
NEGRO_PURO: Tuple[int, int, int] = (0, 0, 0)


# ---------------------------------------------------------------------------
# Slots de Pyxel (0..15)
# ---------------------------------------------------------------------------
# El orden de los 16 slots define la tabla física; los índices que usan los
# consumidores pasan por SEMANTIC, nunca por constantes sueltas.
_SLOT_BLACK: int = 0        # BLACK
_SLOT_PHOSPHOR: int = 1     # PHOSPHOR
_SLOT_AMBER: int = 2
_SLOT_LUMEN_RED: int = 3
_SLOT_GOLD: int = 4
_SLOT_TEXTO_DIM: int = 5
_SLOT_TEXTO_BRILLANTE: int = 6
_SLOT_CYAN: int = 7
_SLOT_MAGENTA: int = 8
_SLOT_GRIS_FRIO: int = 9
_SLOT_GRIS_OSCURO: int = 10
_SLOT_VERDE_OSCURO: int = 11
_SLOT_NARANJA: int = 12
_SLOT_ROJO_APAGADO: int = 13
_SLOT_BLANCO_FOSFORO: int = 14
_SLOT_NEGRO_PURO: int = 15

# Los 16 slots ordenados por índice (índice 0 = primer elemento).
_COLORS: Tuple[Tuple[int, int, int], ...] = (
    BLACK,
    PHOSPHOR,
    AMBER,
    LUMEN_RED,
    GOLD,
    TEXTO_DIM,
    TEXTO_BRILLANTE,
    CYAN,
    MAGENTA,
    GRIS_FRIO,
    GRIS_OSCURO,
    VERDE_OSCURO,
    NARANJA,
    ROJO_APAGADO,
    BLANCO_FOSFORO,
    NEGRO_PURO,
)

# Mapa semántico nombre → índice de slot Pyxel.
# T2 (28/08): claves a UN solo idioma — castellano, una clave por slot (16
# claves ↔ 16 slots). Fuera los duplicados de la v0: "texto_base" (= texto),
# "alert" (EN, = amenaza), "cian" (= info), "gris" (= gris_frio). Sin
# consumidores rotos: los usos reales viven en make_captures.py y
# pyxel_capture.py (fondo/texto/texto_dim/texto_brillante — intactos).
SEMANTIC: Dict[str, int] = {
    "fondo": _SLOT_BLACK,
    "texto": _SLOT_PHOSPHOR,
    "aviso": _SLOT_AMBER,
    "amenaza": _SLOT_LUMEN_RED,
    "hallazgo": _SLOT_GOLD,
    "texto_dim": _SLOT_TEXTO_DIM,
    "texto_brillante": _SLOT_TEXTO_BRILLANTE,
    "info": _SLOT_CYAN,
    "magenta": _SLOT_MAGENTA,
    "gris_frio": _SLOT_GRIS_FRIO,
    "gris_oscuro": _SLOT_GRIS_OSCURO,
    "verde_oscuro": _SLOT_VERDE_OSCURO,
    "naranja": _SLOT_NARANJA,
    "rojo_apagado": _SLOT_ROJO_APAGADO,
    "blanco_fosforo": _SLOT_BLANCO_FOSFORO,
    "negro": _SLOT_NEGRO_PURO,
}


def apply() -> None:
    """Escribe los 16 slots de la paleta CRT (§8.5) en ``pyxel.colors``.

    Lidiable que se llama después de ``pyxel.init`` (y antes de dibujar) para
    que el cursor de Pyxel use los colores de fósforo de CyberRoot.
    """
    import pyxel  # import local: mantener este módulo importable sin Pyxel.

    # Nota de compatibilidad: en pyxel 2.9.9 ``pyxel.colors`` es un
    # ``builtins.Colors`` cuyo ``__setitem__`` exige un int 0xRRGGBB (no un
    # tupla (r,g,b) como en otras versiones). Empaquetamos la tupla RGB de
    # las constantes al int correspondiente.
    for idx, (r, g, b) in enumerate(_COLORS):
        pyxel.colors[idx] = (r << 16) | (g << 8) | b