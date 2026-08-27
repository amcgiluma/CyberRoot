# assets/ — Arte binario consumido por render/

> **Qué hay:** recursos NO serializables que Pyxel carga directamente.
> Nada de lógica, nada de datos de juego (eso va a `data/`).

## Fuente bitmap 5×7 — decisión y veredicto (hito C, 27/08/2026)

**EL riesgo visual nº 1 del stack (INVESTIGACION-STACK riesgo 2) está validado:
la fuente 5×7 cumple y pygame-ce queda DESCARTADA** (ver «Veredicto» abajo).

### Qué es

Tabla clásica **Adafruit-GFX 5×7** (`tools/glcdfont.c.ref`, copia de referencia):
**CP437 completo — 256 glifos × 5 columnas** (1280 bytes), formato columna-de-7px
con **bit 0 = fila superior**. Módulos (pygame-ce queda DESCARTADA — ver
«Veredicto»):

| Fichero | Capa | Qué da |
|---|---|---|
| `font5x7.py` | 1 (sin Pyxel) | `Font5x7` (glifos, `cp437_encode`, `text_size`), `CHAR_EXTENSIONS` (→←↑↓→0x1A..0x1B, —≈0xC4), `render_text_pbm` (rasterizador de referencia Pillow) |
| `palette.py` | 1 | Paleta CRT de 16 slots; 5 semánticos §8.5: `BLACK (4,10,8)`, `PHOSPHOR (33,255,105)`, `AMBER (255,176,0)`, `LUMEN_RED (255,45,60)`, `GOLD (255,200,40)` |
| `pyxel_capture.py` | 2 (Pyxel real headless) | `Capture.capture(draw_fn, out_png)` — PNG nativo 320×180, determinista; `draw_text_pyxel` (pset píxel a píxel); `zoom_png` (NEAREST) |
| `tools/make_captures.py` | 3 | Genera las capturas oficiales de `golden/` (reproducible, sha256 estables) |
| `golden/*.png` | evidencia | 3 capturas oficiales + 3 zooms ×3 (commiteadas) |
| `tests/` | pytest | 29 tests: parser, extensión, paleta y **validación píxel a píxel Pyxel↔parser** |

### Cobertura del español (DESIGN §2.6.8)

La tabla CP437 trae de serie **á é í ó ú ñ ü ¡ ¿ ª º ·** y todo el box-drawing
(`┌ ─ ┐ │ └ ┘ ...`). Extensión propia para lo que el codec cp437 de Python no
mapea: **→ ← ↑ ↓** existen como glifos DOS en 0x18–0x1B de la tabla (verificado
byte a byte) y `—` reutiliza la línea horizontal 0xC4. **`…` NO existe**: los
textos del juego usan `...` (documentado; `cp437_encode` falla alto y claro).

### Veredicto de legibilidad (a resolución nativa 320×180, con evidencia)

**LEGIBLE — la fuente valida. Riesgo desactivado.** Evidencia: `golden/` (regenerable
con el comando de abajo) y revisión píxel a píxel del bitmap:

- Mayúsculas, minúsculas y dígitos nítidos a 1×. El `#` de prompt y el `$` se
  distinguen sin ambigüedad; `0/O` y `1/l/I` diferenciados por diseño de la tabla.
- **Acentos**: el acento ocupa la fila superior del glifo y se lee como tilde real
  en la captura (á é í ó ú ñ verificados en `captura-03`). A 1× son *compactos*
  (la letra se comprime bajo el acento): legibles, no elegantes. Limitación
  conocida, no bloqueante. Si Fase 1 pide más finura, redibujar SOLO 5 glifos
  (á é í ó ú) es una tarde — decisión para Gwyn, no lo he hecho unilateralmente.
- **Sin descenders** (g, j, p, q, y no bajan bajo la línea base): herencia de la
  tabla clásica; convive bien con el estilo terminal.
- Símbolos de UI verificados en `captura-01`: marco box-drawing limpio a 1 px,
  flecha `→` legible, `·` visible (2×2 px, sutil a 1× — usar con moderación).
- Densidad: 46 caracteres × 17 líneas por pantalla de terminal (pitch 10 px),
  holgado para las salidas del sandbox del cap. 0.
- **Escala de juego**: dibujar SIEMPRE a 1× sobre canvas 320×180 y dejar que la
  ventana de Pyxel escale por factor entero — nunca escalar la fuente.
- **pygame-ce DESCARTADA**: Pyxel headless cubre render + captura sin DISPLAY
  (sin siquiera Xvfb; detalles técnicos en el docstring de `pyxel_capture.py`).
  Cero bloqueos encontrados.

### Regenerar las capturas

```bash
cd <raíz del repo>
PYTHONPATH=src .venv/bin/python -m assets.tools.make_captures   # --clean para sobreescribir
PYTHONPATH=src .venv/bin/python -m pytest src/assets/tests/ -q  # 29 verdes
sha256sum src/assets/golden/*.png                                # estable entre ejecuciones
```

Requisitos: `pyxel` + `pillow` en `.venv` (headless: no necesita DISPLAY ni Xvfb).

### Nota de implementación para render/

El dibujo va **píxel a píxel con `pyxel.pset`** usando `Font5x7` — la fuente
builtin de Pyxel está PROHIBIDA en este módulo (la evidencia de esta validación
es la tabla). Los 4 colores semánticos §8.5 se consumen vía `palette.SEMANTIC`
(claves: `fondo`, `texto`, `aviso`, `amenaza`, `hallazgo`…); los valores RGB son
v1 calibrables sin tocar código de UI.

---

## Previsto (resto del módulo)

| Carpeta | Contenido | Notas |
|---|---|---|
| `palette/` | paleta CRT propia `.pyxpal` | §8.5 ya operativa vía `palette.py` (runtime); `.pyxpal` solo si Pyxel Resource editor hace falta |
| `sprites/` | nodos del mapa (conectado/comprometido/quemado), iconos de boon por familia, retratos pixel-art del Hub | §8.5: cada sprite comunica estado |
| `sfx/` | chiptune 4 canales: acierto, pipeline, hallazgo crítico, alerta, expulsión sobria | §7.4 |

## Reglas

1. Solo lo toca **Seath** (`feat/meta-ui`) — mismo dueño que `render/`.
2. Formato nativo de Pyxel (.pyxres/.pyxpal) o PNG fuente; nombres estables:
   renombrar un asset rompe referencias silenciosamente.
3. Los 4 colores SEMÁNTICOS (§8.5) se respetan en TODO asset nuevo.
4. Arte «bonito suelto» prohibido: pixel-art funcional que comunica estado.
5. Plan de implementación del hito fuente: ver `PLAN.md` (hitos H1–H5).
