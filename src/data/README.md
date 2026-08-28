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
| `curriculum.json` | DAG de conceptos (~60 boons, 8 familias, prerrequisitos, capítulos enseñanza/mantenimiento) | §6.2 | Smough |
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
