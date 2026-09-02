# PLAN.md — Seath T1 2026/09/02 — RENDER v0: una sala del cap. 0 pintada

> Mi desarrollo del plan de Gwyndolin (backlog/planes/2026/09/02.md, T1).
> El QUÉ y el AC son suyos; esto es MI hoja de ruta del CÓMO.
> Rama: `feat/meta-ui-2026-09-02` · Módulos: `src/render/` + `src/assets/` (solo lectura)
> Core intacto — este paquete SOLO LEE estado, jamás muta.

## Objetivo en una línea
Pintar UNA sala real del cap. 0 (seed fija) con terminal auténtica: prompt diegético `cero@nodo:/ruta$` usando `cwd` real de la sesión, salida del sandbox enmarcada, fuente 5×7 y paleta CRT. Entregable = demo reproducible + screenshot PNG committeado + smoke test. Sin tocar `src/core/`.

## Contratos que consumo (solo lectura)
- `core.generator.generate(42, chapter=0)` → `Incursion` determinista, `room.host`, `room.fs`, `scaffold.initial_cwd()`
- `core.generator.new_session(inc)` → `Shell` jugable con `cwd` real (opción B → `/`) y comandos del cap0
- `Shell.execute("ls ...")` → salida real del FS virtual (no hardcodeada)
- `assets.font5x7.Font5x7` + `assets.palette.SEMANTIC` + `assets.pyxel_capture.Capture` (infra ya validada)

## Hitos (secuenciales, ~1h c/u, cada uno verificable)

### H1 — Esqueleto render + theme (15 min)
- **Qué:** `src/render/__init__.py` (paquete vacío), `src/render/theme.py` (re-exporta `SEMANTIC` y define `TERMINAL_GEOMETRY`: canvas 320×180, margen terminal, pitch 10px, colores semánticos por rol).
- **Interfaces:** `theme.TERM_W`, `TERM_H`, `PROMPT_COLOR`, `OUTPUT_COLOR`, `BORDER_COLOR` (wrappers sobre `assets.palette`).
- **Test H1:** `import render.theme` sin `import pyxel` a nivel top-level (lazy); `palette.SEMANTIC` accesible.
- **Hecho si:** `python -c "import render.theme"` no falla; cero lógica de juego.

### H2 — Prompt diegético + helpers de texto (30 min)
- **Qué:** `src/render/terminal.py` — funciones puras SIN pyxel:
  - `build_prompt(user, host, cwd)` → `f"{user}@{host}:{cwd}$"` (user=`cero` por defecto, lore §2.2; host viene de `room.host`; cwd de `shell.cwd` real).
  - `wrap_lines(text, max_cols)` — corta a 46 cols (densidad validada en assets/README) sin romper palabras si cabe.
  - `terminal_lines(shell, host, user)` → lista de `(text, color_key)` para pintar: prompt + último comando + stdout.
- **Edge:** cwd `/` → `cero@oficina-vecinal-muelle-norte:/$`; paths largos se truncan con `…` (no rompen layout).
- **Test H2:** unit tests puros en `src/tests/render/test_terminal.py` (sin pyxel): prompt con cwd `/`, `/srv`, `/srv/oficina-...`; wrap no pierde caracteres.
- **Hecho si:** `pytest src/tests/render/test_terminal.py -q` verde.

### H3 — Pintor de sala (45 min)
- **Qué:** `src/render/scene_room.py` — único sitio que toca `pyxel.pset`:
  - `draw_room_frame()` — marco box-drawing (reusa lógica de `assets.tools.make_captures` pero extraída a `render.terminal` sin duplicar; dibuja con `draw_cp` local).
  - `draw_terminal(shell, host)` — compone pantalla completa: título centrado (`host`), marco (6,14 → 312,84), contenido a 14,22 con pitch 10px: líneas de `terminal_lines`.
  - Usa `assets.font5x7.Font5x7`, `assets.pyxel_capture.draw_text_pyxel` (import lazy dentro de función para que tests puros no exijan pyxel).
- **Decisión:** no `app.py` con bucle Pyxel persistente en v0 — solo función de dibujo llamada desde `Capture`. `app.py` queda stub documentando el bucle futuro.
- **Hecho si:** `draw_terminal` existe, no importa `core` salvo tipos en type hints opcionales.

### H4 — Demo reproducible + captura PNG (45 min)
- **Qué:** `src/render/demo.py` — script ejecutable:
  ```python
  inc = generate(42, chapter=0)  # seed fija, canónica, determinista
  shell = new_session(inc)
  shell.execute(f"ls {OFFICE_DIR}")
  # luego Capture.capture(lambda: draw_terminal(shell, inc.room.host), out_png)
  ```
  Genera `src/render/golden/cap0-room.png` (320×180 nativo) + `.zoom3x.png` (NEAREST) deterministas. El demo imprime `seed=42 host=... cwd=... ls_output=...` para trazabilidad.
- **Reproducibilidad:** sin RNG propio, sin timestamps en dibujo; `PYTHONPATH=src .venv/bin/python -m render.demo` regenera byte-idéntico (verificado con sha256).
- **Hecho si:** `python -m render.demo` crea PNG; segunda ejecución sha idéntico; PNG commiteado.

### H5 — Smoke + gate + PR (30 min)
- **Qué:** `src/tests/render/test_render_smoke.py` — smoke headless:
  - test_pure: importa `render.terminal` y `render.scene_room` sin display.
  - test_capture: si `pyxel` disponible, hace `Capture.capture` de un frame vacío en `/tmp` y aserta PNG existe (skip si no headless).
  - test_no_core_mutation: `grep` que `src/render/` no hace `Shell.execute` fuera de demo ni asigna a `GameState`.
- **Suite base:** 466 passed (verificado 02/09) → rama esperada 466 + ~5 nuevos = ~471. Core intacto (diff `src/core/` vacío).
- **Hecho si:** `pytest src/ -q` verde; `git status --porcelain` solo toca `src/render/` + `src/tests/render/` + `docs/worklog/` + `backlog/tareas/en-curso/activo.md`; PR abierto con «tests antes: 466 · tests rama: 471 · delta esperado: +5».

## Orden de ejecución
H1 → H2 → H3 → H4 → H5. Cada hito delegable en sub-agente salvo H5 (yo verifico).

## Interfaces concretas (consumidas por futuros capítulos)
```python
# render/terminal.py (puro, sin pyxel)
def build_prompt(user: str, host: str, cwd: str) -> str: ...
def terminal_lines(shell, host: str, user: str = "cero") -> list[tuple[str,str]]: ...

# render/scene_room.py (con pyxel, solo dibuja)
def draw_terminal(shell, host: str) -> None: ...
def draw_room_frame() -> None: ...

# render/demo.py (CLI)
# python -m render.demo [--seed 42] [--out src/render/golden/cap0-room.png]
```

## Riesgos y mitigaciones
- **Pyxel headless hard-exit:** capturar con patrón `Capture.capture` + hook `on_screenshot` (ya validado en assets); demo usa `capture` como librería, no CLI, y zoom en hook.
- **Fuente no disponible en test puro:** `draw_text_pyxel` importado lazy dentro de `draw_terminal`; tests puros mockean o saltan.
- **No romper determinismo:** seed fija en demo; shell salida viene del FS real, no hardcodeada — si `chapter0.py` cambia, el PNG cambia y el test lo detecta (es lo correcto).
- **Prompt largo desborda:** truncado a 46 cols con `…`; verificado en H2.
