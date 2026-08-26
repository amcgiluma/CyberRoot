# core/ — La lógica de CyberRoot (Python puro, headless)

> **Qué es:** todo el juego menos la pantalla. Estado, sandbox Linux virtual,
> currículo, generador procedural, motor roguelite (runs), metaprogresión y
> karma. Cero dependencias del motor: aquí no existe Pyxel.
>
> **Por qué:** el comité debe poder verificar el juego solo. `pytest` resuelve
> niveles como un jugador (secuencias de comandos → estado final esperado) sin
> ventana; el harness lanza cientos de runs headless con seeds fijas
> (INVESTIGACION-STACK «decisión clave», CONFIRMADA).

## Contrato externo (lo único que el resto del mundo ve)

- **Entrada:** comandos/acciones como datos planos —
  `{"cmd": "exec", "argv": ["grep", "-i", "lista"]}` o acción UI
  `{"cmd": "ui", "op": "entrar_sala", "sala": "n7"}`.
- **Salida:** mutaciones sobre `GameState` (serializable a JSON) + lista de
  `Event(tipo, datos)` observables. El render y el harness CONSUMEN eventos;
  nadie toca el estado por debajo.

Desarrollo interno por paquetes, contratos entre ellos y convenciones de
código: **`ARCHITECTURE.md`** (léelo antes de escribir la primera línea).

## Paquetes y dueño

| Paquete | Responsabilidad | Dueño |
|---|---|---|
| `common/` | RNG seedeada, bus de eventos, tipos base, errores | Ornstein |
| `sandbox/` | FS virtual + shell + semántica real de comandos | Smough |
| `curriculum/` | DAG de conceptos, familias, pools por capítulo | Smough |
| `generator/` | Generación procedural ENSEÑANTE + validación canónica | Ornstein |
| `engine/` | Motor roguelite: run, salas, detección, DATOS×COMBO, Hub | Ornstein |
| `state/` | `GameState` agregador + save/load plano | Seath |
| `progression/` | Espejo de Gris, unlocks por competencia, economía | Seath |
| `karma/` | Contabilidad Blue/Red (N=8, umbrales) | Seath |

## Cómo se testa

```bash
python -m pytest src/tests/core -q          # suite headless completa
python -m pytest src/tests/architecture -q  # core no importa pyxel, RNG seedeada
```

- Determinismo: toda prueba fija seed; mismo input → mismos eventos.
- Los niveles se validan resolviéndolos con su solución canónica
  (DESIGN §4.5: sala irresoluble = bug de generación).
- Regla de oro: si un test necesita pantalla, está en el sitio equivocado.
