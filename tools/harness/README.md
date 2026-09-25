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
| **«Ánimo de novedad» (O2, 01/09)** | Distribución de **familias de comando por run** (del canon): histograma por seed + agregado global + **aviso cuando una familia domina** (>60 % de los comandos de una run). Detecta si el generador repite demasiado una familia y alimenta la calibración del `noise_budget`. | canon → conceptos `c.<comando>` → `family` |

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
#   --calibrar    calibración del budget (O3): 50 seeds × {canonical, practice}
#                 → distribución del total_noise del VIAJE HONESTO vs budget
#                 + % que lo excede + frecuencia de error en la canónica
#   --budget N    noise_budget de la sala (misma unidad que total_noise, 🧭10)
#   --micro-karma calibración micro-karma N=8: 20×3 pares (S1 24/09, Smough)
#                 + ancla real e1/e3/e4 vía _probar_micro_real() + ventana K
#   --karma-seeds N  nº de seeds para micro-karma / stock-gris (default 20)
#   --stock-gris  corpus 🧭47 (S1 25/09, Smough): N seeds × micro-karma real
#                 e1/e3/e4 + histograma azul/rojo + contraste N=8 + lectura
#                 intercalada `grep censo` (0 gris entre huellas +-1) — mide
#                 stock Gris 0% estático y si la lectura cambia K (§8.6)
```

Código de salida: `0` si `% resolubles == 100` y determinismo perfecto; `1` en
cualquier alerta (una irresoluble o una seed no determinista). Útil para CI.

## Corpus 25/09 — stock de Gris + lecturas intercaladas (🧭47, S1 Smough)

Medida honesta del §8.6 sin tocar pesos (weight 1 intacto, 🧭45):

```bash
# 20 seeds (smoke) — AC del plan
PYTHONPATH=src .venv/bin/python tools/harness/run_seeds.py --stock-gris --karma-seeds 20 --export /tmp/stock.json
# 500 seeds (medida completa §8.6)
PYTHONPATH=src .venv/bin/python tools/harness/run_seeds.py --stock-gris --karma-seeds 500 --export /tmp/stock500.json
```

**Qué mide:**
- Histograma real vía `_probar_micro_real()` por seed (e1 `chmod 600/777`, e3 `HUP/-9`, e4 `gris/root`): cada huella es estable `{'1':N}` azul vs `{'-1':N}` rojo en todos los seeds (determinismo del micro-karma).
- Contraste N=8 ventana: `perfil azul puro` y `rojo puro` (secuencia de chmod 600 vs 777) → `pct>=3`/`pct<=-3` y `K_final`. Con N=20 → 90.0% ambos, K_final +-8; con 500 → 99.6%, K_final +-8. Contraste kármico = `|pct_azul - pct_rojo|` = 0.0% (stock Gris 0% estático: Gris no tiene stock kármico aún, §8.6).
- Lectura intercalada (H2, idea Havel 25/09): patrón `huella(+-1) + lectura(0)` ( `chmod 600` antes y después de `ps aux | grep censo` gris) en la misma ventana N=8 → `perfil_azul_intercalado`/`rojo_intercalado`. Resultado 25/09: mismo `pct>=3` (90.0%→90.0% en 20, 99.6%→99.6% en 500) delta 0.0%, pero K_final 8→4 (la lectura gris diluye a la mitad la densidad; la ventana N=8 tarda el doble en saturarse). Conclusión: `grep censo` gris hoy NO cambia el umbral T=3, solo la velocidad; si debiera ser +0.3 azul tenue es decisión de Gwyn (Smough solo reporta).

Payload JSON (`stock_gris`): `n, N, histograma, perfil_azul_puro/rojo_puro, contraste_karmico_pct, lectura_intercalada{...}, stock_gris_estado, nota`.

## Estructura futura (por construir)

- Escalar a todas las capas: seed multirun → duración, ruido, contraste
  kármico entre perfiles azul/rojo (§8.6). Este fichero es el **runner de
  seeds** con el que arranca; la API (`core.generator`) ya es consumible.
- `core.generator.new_session` es la puerta para montar el bucle de juego:
  hoy el harness valida con la secuencia canónica; cuando exista el engine,
  el harness jugará runs completas.