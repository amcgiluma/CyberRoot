# data/ — Contenido del juego (JSON, única fuente de verdad)

> **Qué es:** todos los DATOS que definen partidas distintas sin tocar código:
> currículo, campañas, catálogos, textos. `core/` carga; nadie hardcodea texto
> visible ni balance dentro de Python.
>
> Por qué JSON y no Python: los ejecutores editan contenido sin tocar lógica,
> el diff de git es limpio, y Manus puede aportar textos sin pisar a nadie.

## Mapa

| Fichero/carpeta | Contenido | Referencia DESIGN | Dueño |
|---|---|---|---|
| `curriculum.json` | DAG de conceptos (~60 boons, 8 familias, prerrequisitos, capítulos enseñanza/mantenimiento) | §6.2 | Smough (esquema) · Seath (cap. 5, T2) |
| `textos.json` | Primer paquete de TEXTOS (🧭12): post-mortem del Auditor + quests ch1/ch5 | §2.4, §2.6 | **Seath** (integrator desde `backlog/historia/`) |
| `textos.py` | Resolvedor mínimo `line_key`+`args` → texto con placeholders | ARCHITECTURE §3 | Seath |
| `chapters/*.json` | plantillas por campaña: 0–6 (pools, tipos de sala, encargos base, puertas finales) | §6.1–6.3 | Ornstein (estructura) · Smough (retos) |
| `boons.json` | tarjetas: nombre real, familia, pista diegética, condición de unlock | §4.4, §7.5 | Smough |
| `items.json` | ~12 objetos de Gris + efectos (objeto×comando §5.2) | §4.3 | Seath |
| `perks.json` | ~8 perks pasivos (reglas que cambian, no fuerza) | §5.3 | Seath |
| `synergies.json` | 28 sinergias v1: disparador → efecto → pista de Gris | §7.8 | Ornstein |
| `pacts.json` | 6–8 Pactos de Vela (condiciones + multiplicadores) | §4.6 | Ornstein |
| `economy.json` | valores de datos por tipo, escalones de combo, % parcial expulsión, umbrales ⚠️ v1 | §7.1–7.7 | Ornstein |
| `karma.json` | pesos por tipo de decisión, N=8, bandas T_alto/T_bajo ⚠️ v1 | §3.3–3.4 | Seath |
| `story/` | textos narrativos: cola de eventos por clase, barks, informes-tipo del Auditor, fragmentos H1/H2 | §2.6, §9 | **Manus** (vía Gwyndolin) |
| `hub/` | titulares según karma, stock-tints, líneas de aliados | §3.2–3.3 | Seath (claves) · Manus (texto) |

## Reglas
1. Todo fichero se valida contra su esquema en `src/tests/data/` (un test por
   fichero: claves obligatorias, referencias que existen, DAG sin ciclos).
2. Los números marcados ⚠️ v1 en DESIGN son calibrables AQUÍ (por harness),
   sin PRs de lógica.
3. Textos: español de España; salidas técnicas en su forma real (§2.6.8).
4. Cambiar `data/` = hacerlo desde la rama del dueño de esa fila.

## Textos (`textos.json` + `textos.py`) — contrato del resolvedor (T1, 01/09)
- **`textos.json`** mapea `line_key` → plantilla. Los placeholders siguen la
  forma `{nombre}` (p. ej. `postmortem.auditor.*` recibe `{command}`/`{amount}`/
  `{total_noise}`/`{noise_budget}` de `build_postmortem`).
- **`textos.py`** expone `resolve(line_key, args=None)` (y `load_textos()`).
  Reglas del resolvedor: clave ausente → `TextResolutionError` accionable;
  plantilla con placeholder sin arg → `TextResolutionError` accionable
  (romper claro > mostrar un hueco `{...}`); cero lógica de juego y cero
  dependencias del core (ARCHITECTURE §3: «core carga claves, el render (o el
  resolvedor) las resuelve»).
- **Cobertura** (`src/tests/data/test_textos.py`): toda clave que emite
  `build_postmortem` + todo `title_key`/`beat_key` de las quests integradas
  (ch1 T1, ch5 T2) resolviendo a texto no vacío — falla si se añade una clave
  sin su texto.
- Las claves narrativas entran integradas por el ejecutor desde
  `backlog/historia/` (regla PROJECT-MAP): Manus escribe prosa, nunca toca
  este fichero.

## Cómo se testea
```bash
python -m pytest src/tests/data -q   # esquemas + referencias cruzadas + DAG
```
> *(28/08, Smough: `curriculum.json` se valida en
> `src/tests/core/curriculum/` — 46 tests, junto al módulo que lo carga y
> define su esquema. La carpeta `src/tests/data/` nacerá cuando haya más de
> un fichero de datos con esquema propio.)*

## Coordinación
- Manus ESCRIBE prosa pero NO toca este directorio directamente: entrega sus
  piezas en `backlog/historia/` y quien integre (ejecutor correspondiente) las
  vuelca en `data/story/` con las claves correctas. Así el formato nunca se rompe.
- Los ficheros ⚠️ v1 (`economy`, `karma`) nacen con valores semilla de DESIGN;
  el harness los ajustará con datos en Fase 1.
