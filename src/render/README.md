# render/ — Capa delgada de Pyxel

> **Qué hace:** dibuja el estado y traduce el input a comandos. NADA MÁS:
> aquí no vive ni una regla de juego. Si algo cambia un número, está en
> `core/`; si solo lo enseña, es de aquí.
>
> Normativa: `docs/DESIGN.md` §8 (UX completa) · INVESTIGACION-STACK
> («render consulta, nunca muta») · `../ARCHITECTURE.md` §1.

## El contrato en una línea
```
pyxel frame: input ─► comando {"cmd": ...} ─► core ─► eventos+estado ─► dibujar
```
- **Entrada**: teclado (terminal, modos), ratón (mapa de nodos §8.1). Cada
  pulsación/click se traduce a un comando del core — jamás se muta estado.
- **Salida**: pantalla. Consume los mismos `Event`s que el harness (RM §4.4.1:
  juice = el dato visto dos veces; HUD §8.2 y terminal §8.4 leen el mismo canal).

## Piezas previstas
| Fichero | Qué pinta / captura |
|---|---|
| `app.py` | bucle Pyxel (`init(headless=...)`), gestión de escenas |
| `scene_hub.py` | Subestación: diálogos, cola post-mortem, espejo, tienda |
| `scene_map.py` | grafo de nodos clicable con información imperfecta (§8.1) |
| `scene_room.py` | terminal real (enmarca la salida del parser del core) + foco §8.3 |
| `hud.py` | panel lateral fijo: objetivo/detección/combo/datos/equipo |
| `fx.py` | scanlines, shake, números flotantes — escala por MAGNITUD del evento (§7.4); JAMÁS tapa la terminal |
| `theme.py` | paleta CRT redefinida vía `pyxel.colors` + 4 colores semánticos fijos (§8.5) |

## Riesgos gestionados (INVESTIGACION-STACK)
- **Fuente bitmap 5×7 desde el día 1** (riesgo nº 1 del stack): validada con
  capturas antes de construir pantallas encima.
- Modo `headless=True` oficial para smoke tests sin ventana.

## Cómo se testea
- Smoke headless: la app arranca, corre N frames y muere limpia
  (`pyxel.init(headless=True)`).
- Test tonto de frontera: este paquete no define reglas (grep de asignaciones
  sobre GameState = prohibido).
- Verificación visual fina (fuente, paleta, juice): la hace el Concilio con
  capturas — capa TÉCNICA de Artorias + zona 🔬 de Gwyn.

## v0 — Sala del cap. 0 pintada (Seath, 02/09/2026)

**Entregable T1:** terminal auténtica del cap. 0 con prompt diegético `cero@nodo:/ruta$` (avanza 🧭13) y salida real del sandbox, fuente 5×7 y paleta CRT. Ver `PLAN.md` (hitos H1–H5).

| Fichero | Qué hace (v0) |
|---|---|
| `theme.py` | Geometría 320×180, marco (6,14→312,84), pitch 10px, re-export `SEMANTIC` |
| `terminal.py` | `build_prompt` + `wrap_lines` + `terminal_lines` (puro, sin pyxel) |
| `scene_room.py` | `draw_terminal(shell, host)` — único sitio con `pyxel.pset` |
| `demo.py` | `python -m render.demo` → `golden/cap0-room.png` (320×180) + zoom ×3, seed 42 determinista, sha `c84450443e83` |
| `golden/cap0-room.png` | Screenshot headless committeado (9.5K) — evidencia visual para Artorias/Gwyn |

- **Demo reproducible:** `PYTHONPATH=src .venv/bin/python -m render.demo` (segunda ejecución sha idéntico `c84450443e835609`). No RNG propio, salida viene del FS real (`ls /srv/oficina-vecinal-muelle-norte`).
- **Tests:** `src/tests/render/test_terminal.py` (8) + `test_render_smoke.py` (3) = 11 + 1 de smoke incluido → **12 nuevos**, suite 466→478. Sin tocar `src/core/`.
- **Frontera intacta:** `src/render` solo lee `core.generator` en `demo.py`; fuera de demo no hay `.execute(` ni `GameState`.

## Dueño
Seath (`feat/meta-ui`). Único paquete autorizado a importar pyxel.
