# state/ — Estado agregador y guardado

> **Qué hace:** ensambla TODO lo persistente del juego en un único
> `GameState` serializable a JSON ida-y-vuelta: perfil del jugador, run actual
> (si la hay), Hub, unlocks, historial kármico, récords. Y lo guarda/carga de
> forma atómica.
>
> Normativa: INVESTIGACION-STACK («guardado como dato plano serializable») ·
> `../ARCHITECTURE.md` §2.6.

## Responsabilidades
- Definir `GameState` (dataclasses planas ↔ dict ↔ JSON) y sus sub-estructuras.
- Save/load atómico (escribir-temporal + renombrar), versionado
  `schema_version` desde el día 1 con migraciones simples encadenadas.
- Fachada de consulta para render/harness: leer estado SIN poder mutarlo por
  debajo (toda mutación = comando al engine/progresión/karma).

## Entradas / salidas
- ENTRADA: piezas de los otros módulos (perfil de progression, run del engine,
  entradas de karma).
- SALIDA: `GameState.to_dict() / from_dict()`, ficheros de save.

## Cómo se testea
- Ida-y-vuelta: partida arbitraria → save → load → idéntica (test canónico).
- Saves de versiones anteriores migran sin pérdida (fixtures de saves viejos).
- Un save escrito a mano corrupto falla con error claro, no con traceback
  profundo.

## Dueño
Seath (`feat/meta-ui`), junto a `progression/` y `karma.py`.
