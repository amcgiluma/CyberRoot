# src/ — Código de CyberRoot

> Mapa corto. Cada módulo tiene su `README.md`; entra ahí antes de tocar nada.
> Tabla completa de dueños y ramas: `docs/PROJECT-MAP.md` §3.

```
src/
  core/     → TODA la lógica del juego. Python puro, 0 deps de Pyxel,
              testeable headless. Detalle interno: core/ARCHITECTURE.md
  render/   → capa DELGADA de Pyxel: dibuja estado + traduce input a comandos.
              SIN lógica de juego.
  assets/   → arte binario consumido por render: fuentes bitmap, paleta CRT,
              sprites, sfx.
  data/     → datos de juego en JSON (boons, currículo, sinergias, plantillas
              de salas, encargos, textos). ÚNICA fuente de verdad de contenido;
              nada de texto visible hardcodeado en core.
  tests/    → pytest sobre core (headless) + test de arquitectura + smoke
              opcional de render (pyxel headless=True).
```

## Las 3 reglas que nadie rompe (detalle en `core/ARCHITECTURE.md`)

1. **`core/` no importa `pyxel` jamás** — lo vigila un test automático.
2. **Todo entra como comando** (`{"cmd": "exec", "argv": [...]}` o acción UI);
   el core responde con eventos observables. El render consulta, nunca muta.
3. **RNG siempre seedeada** → runs reproducibles, tests deterministas, bugs
   reproducibles por el harness.

## Dueños (resumen — ver PROJECT-MAP §3)

| Carpeta | Dueño | Rama |
|---|---|---|
| `core/sandbox/`, `core/curriculum/` | Smough | `feat/sandbox` |
| `core/engine/`, `core/generator/`, `core/common/`, `tools/harness/` | Ornstein | `feat/engine` |
| `core/state/`, `core/progression/`, `core/karma/`, `render/`, `assets/` | Seath | `feat/meta-ui` |
| `data/` | reparto por fichero → `data/README.md` | la rama del dueño |

Regla anti-colisión: una rama NUNCA toca rutas de otro dueño; si una tarea lo
exige, se abre en `tareas/pendiente/abierto.md` y la ejecuta el dueño.
