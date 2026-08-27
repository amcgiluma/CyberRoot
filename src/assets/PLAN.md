# PLAN.md — Tarea C: Fuente bitmap 5×7 validada (Seath, 27/08/2026)

> Mi desarrollo del plan de Gwyndolin (backlog/planes/2026/08/27.md, tarea C).
> El QUÉ y el criterio de aceptación son suyos; esto es MI hoja de ruta del CÓMO.
> Rama: `feat/meta-ui` · Módulo: `src/assets/` · Riesgo visual nº1 del stack
> (INVESTIGACION-STACK riesgo 2). Nada de esto toca `core/` ni render de Ornstein/Smough.

## Decisión técnica previa (justificada)

**Fuente elegida: la tabla clásica 5×7 de Adafruit-GFX (`glcdfont.c`), CP437 completo
(256 glifos, 1280 bytes).** Razones:

1. **Español de España gratis (DESIGN §2.6.8):** la tabla es CP437 indexada, así que
   trae de serie `á é í ó ú ñ ü ¡ ¿ ª º` y box-drawing (`─ │ ┌ ┐ └ ┘ ┬ ┴ ├ ┤ ┼`).
   Los acentos existen (verificados en bytes: á=0xA0, é=0x82, í=0xA1, ó=0xA2, ú=0xA3,
   ñ=0xA4, ü=0x81, ¡=0xAD, ¿=0xA8). Alternativas (PICO-8, IBM BIOS 8×8) no cubren
   esto a 5×7 sin dibujar a mano.
2. **Procedencia verificable**: tabla pública (MIT/BSD en Adafruit-GFX, dominio clásico),
   guardo copia de referencia en `tools/glcdfont.c.ref`.
3. **Formato trivial de parsear** (5 bytes por glifo, LSB = columna de 7 px) →
   testable byte a byte sin Pyxel.

**Paleta CRT**: `palette.py` con los 4 colores semánticos de §8.5 como constantes:
negro profundo, verde fósforo (texto base), ámbar (aviso), rojo Lumen (amenaza),
dorado (hallazgo). Docstring cita el §.

**Pirámide de verificación** (cada capa usa la anterior):
P1 parser puro (sin Pyxel) → P2 render real en screen Pyxel headless → P3 capturas PNG
reproducibles → P4 veredicto de legibilidad + README.

## Hitos (secuenciales, cada uno con su criterio de HECHO)

### H1 — `font5x7.py`: parser + módulo de glifos (Pyxel-free) [delegable]
- `Font5x7`: carga tabla 256 glifos × 5 bytes; `glyph(codepoint) -> list[5 int]`
  (cada byte = columna 7px, bit 0 = fila superior).
- `cp437_encode(text: str) -> bytes`: mapea UTF-8→CP437 (Python stdlib lo trae);
  errores explícitos ante código no mapeable.
- `render_text_pbm(text, ...) -> PIL.Image`: rasterizador de REFERENCIA en Pillow
  (misma matriz de píxeles que dibujará Pyxel): 1 glifo + 1 px de tracking.
  Sirve para tests sin Pyxel y para comporar contra el render Pyxel.
- **Tests** (`tests/test_font5x7.py`): 256 glifos cargados; 'A' = columnas
  0x7C,0x12,0x11,0x12,0x7C (golden del upstream); 'á' resuelve a 0xA0; cp437_encode
  ida/vuelta para el pangrama español con acentos; imagen PBM del pangrama no vacía
  y dimensiones correctas (len*6-1 de ancho, 7 de alto).
- **HECHO**: pytest verde en esa suite, cero `import pyxel`.

### H2 — Render Pyxel real headless + paleta [delegable]
- `palette.py`: constantes CRT §8.5 (BLACK, PHOSPHOR, AMBER, LUMEN_RED, GOLD…)
  + `apply(pyxel)` que reescribe `pyxel.colors`.
- `pyxel_capture.py`: clase `Capture` con la API estándar de Pyxel headless
  (init con `headless=True`, `quit` tras captura); métodos `draw_text(str, x, y, color)`
  (dibuja columnas con `pyxel.pset` desde `Font5x7`) y `screenshot(path)`.
- **Tests** (`tests/test_pyxel_render.py`): en Xvfb, dibuja 'A' y compara el rectángulo
  de píxeles leído con `pyxel.images[0]` contra la imagen PBM de referencia de H1
  (deben coincidir píxel a píxel — esa es la validación REAL de que Pyxel dibuja
  la fuente como el parser dice).
- **HECHO**: pytest verde con Xvfb; comparación píxel a píxel pasando.

### H3 — Las 2+ capturas reproducibles [delegable]
- `tools/make_captures.py` (raíz del módulo, ejecutable): genera las capturas
  requeridas con textos REALES del juego (no lorem ipsum):
  1. `captura-01-prompt-terminal.png` — prompt + salida `ls -l` verosímil del
     sandbox del cap. 0 (Fase 1) con colores semánticos.
  2. `captura-02-informe-auditor.png` — informe del Auditor («Expediente 000…»)
     en verde fósforo sobre negro + línea de estado ámbar.
  3. `captura-03-hoja-glifos.png` — hoja de glifos ASCII 32–126 + acentos CP437
     (á é í ó ú ñ ü ¡ ¿ ª º) etiquetada — es la «hoja de glifos» del criterio.
- Reproducibilidad: el script es determinista (sin RNG ni timestamps en el dibujo);
  corred dos veces → PNG idénticos byte a byte (lo comprobaré con sha256).
- **HECHO**: 3 PNG en `src/assets/golden/`, shas documentados, doble ejecución
  idéntica verificada.

### H4 — Veredicto de legibilidad + README [yo directamente]
- `README.md` de `src/assets/`: sección «Fuente bitmap 5×7 — decisión y veredicto»:
  qué fuente es, por qué, cómo regenerar capturas (comando exacto), el veredicto de
  legibilidad a resolución nativa (mi análisis: densidad, tracking, acentos legibles
  o no, riesgo a escala 1 vs 2), y la nota de que la opción B (pygame-ce) queda
  DESCARTADA/documentada si Pyxel cumple el criterio.
- Reviso las PNG con ojos (zoom, contraste) y escribo el veredicto honesto: si algo
  es ilegible, lo digo y propongo ajuste (p. ej. dibujar a escala 2). El veredicto
  se basa en las capturas REALES, no en expectativa.
- **HECHO**: README con veredicto + comando de regeneración; coherent con capturas.

### H5 — Huella del turno [yo directamente]
- Marca `[HECHO]` (+PR) en `backlog/tareas/en-curso/activo.md` (línea de Seath).
- Worklog `docs/worklog/2026/08/27.md`: QUÉ/POR QUÉ/ENTREGABLE/RELEVO + hitos.
- Commit + `git push origin feat/meta-ui` + `gh pr create` a main.
- **HECHO**: PR abierto y referenciado en activo.md.

## Interfaces concretas (lo que consumirán render/ y el resto)

```python
# font5x7.py
class Font5x7:
    GLYPH_W = 5; GLYPH_H = 7; TRACKING = 1
    def glyph(self, codepoint: int) -> list[int]: ...        # 5 columnas de 7px
    def cp437(self, text: str) -> bytes: ...                  # str -> códigos CP437
    def text_size(self, text: str) -> tuple[int, int]: ...    # píxeles
def render_text_pbm(text: str, scale: int = 1) -> PIL.Image: ...
```

## Riesgos y plan B

- **Pyxel headless pudiera fallar sin DISPLAY**: uso `xvfb-run` (verificado instalado)
  en los comandos y documento el requisito; los tests de H1 corren sin Xvfb.
- **Si la comparación píxel a píxel H1↔H2 difiere**: bug en mi rasterizador o en
  el orden de bits — se depura en H2 antes de seguir; NO se maquilla.
- **Si algún acento CP437 resultara ilegible a 5×7** (posible en á/í): queda
  documentado en el veredicto como limitación conocida con propuesta (dibujar
  variante propia de esos glifos) — decisión para Gwyn, no improvisto arte hoy.
