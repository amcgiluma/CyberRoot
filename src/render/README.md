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

## Dueño
Seath (`feat/meta-ui`). Único paquete autorizado a importar pyxel.
