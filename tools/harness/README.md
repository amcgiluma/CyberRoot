# tools/harness — Playtest autónomo del generador (v0)

> Dueño: **Ornstein** (rama `feat/engine`). Entrega del plan 29/08 (**O2**).
> Vive en la raíz (fuera de `src/`) per decisión del Arquitecto: consume la
> API de `core.generator`, no el motor de render. Solo stdlib.

## Qué es

`run_seeds.py` corre el generador sobre **N seeds** del cap. 0 y reporta tres
métricas que alimentan la calibración de los números ⚠️ v1 de DESIGN:

| Métrica | Qué mide | Acuerdo mínimo (v0) |
|---|---|---|
| **% resolubles** | Cuántas salas generadas se auto-resuelven con su secuencia canónica (§6.4.4). Una irresoluble (`UnsolvableRoomError`) es **bug de generación**, no dificultad. | 100 % |
| **Determinismo** | Si la 2.ª pasada con la misma seed produce la Incursión **byte-idéntica** (misma seed ⇒ misma sala, en cualquier proceso). | 2.ª pasada ≡ 1.ª |
| **Distribución de conceptos** | Cuántas veces aparece cada concepto en el `concept_pool` de las salas. Es la base de 🧭6 y del «ánimo de novedad» de Havel: si el cap. 0 reparte siempre el mismo pool, el harness lo ve. | pool = conceptos del cap. |

## Cómo se ejecuta

```bash
# 50 seeds del cap. 0, variante canónica (AC de O2):
PYTHONPATH=src .venv/bin/python tools/harness/run_seeds.py --chapter 0 --seeds 50

# Variante practice (1–2 decoys) + volcado JSON a ./tmp/:
PYTHONPATH=src .venv/bin/python tools/harness/run_seeds.py \
    --chapter 0 --seeds 50 --variant practice --export tmp/harness_cap0.json

# Flags disponibles:
#   --chapter 0   capítulo (solo 0 en v0; ch1+ cuando el generator lo soporte)
#   --seeds N     nº de seeds (por defecto 50)
#   --variant canonical|practice
#   --start S     offset de la primera seed (p.ej. --start 100 → 100..149)
#   --export PATH volcado JSON opcional (resultados + métricas)
```

Código de salida: `0` si `% resolubles == 100` y determinismo perfecto; `1` en
cualquier alerta (una irresoluble o una seed no determinista). Útil para CI.

## Estructura futura (por construir)

- Escalar a todas las capas: seed multirun → duración, ruido, contraste
  kármico entre perfiles azul/rojo (§8.6). Este fichero es el **runner de
  seeds** con el que arranca; la API (`core.generator`) ya es consumible.
- `core.generator.new_session` es la puerta para montar el bucle de juego:
  hoy el harness valida con la secuencia canónica; cuando exista el engine,
  el harness jugará runs completas.