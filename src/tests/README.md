# tests/ — La red de seguridad (pytest, headless)

> **Qué garantiza:** que el juego funciona SIN pantalla y que nadie rompe la
> arquitectura. Es el «verificador autónomo» del proyecto: cada PR pasa aquí
> antes de merge (Artorias 💥/✅), y el harness extiende estos tests a escala.

## La regla (convención ÚNICA de tests — tarea O1, 28/08)

1. **Todos los tests viven en `src/tests/`**, espejando el árbol de `src/`:
   código en `src/core/generator/` ⇄ tests en `src/tests/core/generator/`.
   Válido para `core/`, `render/`, `assets/`, `data/` y todo lo que venga.
2. **PROHIBIDO cualquier otro directorio `tests`** dentro de `src/` (p. ej.
   `src/assets/tests/`, `src/render/tests/`), CON O SIN `__init__.py`. Un
   paquete `tests` alternativo colisiona con `src/tests/` al integrar ramas:
   fue la causa de los 13 errores de colección del PR #3 (27/08).
3. **Un `__init__.py` por carpeta de tests** (vacío), coherente con el resto
   del árbol; la colección va por `pythonpath = ["src"]` del `pyproject.toml`
   (pytest ≥ 8 lo aplica), no por hacks de `sys.path` (si alguno sobrevive,
   solo como cinturón y tirantes apuntando a `src/`).
4. El guard `src/tests/architecture/test_tests_layout.py` fuerza la regla 2:
   si creas un `tests` fuera de `src/tests/`, la suite ROMPE con instrucciones.
5. Origen: propuesta de Artorias (27/08, `pendiente/abierto.md`); migración
   de `src/assets/tests/` → `src/tests/assets/` ejecutada por Ornstein (28/08).

## Estructura

```
tests/
  architecture/      → LA FRONTERA (rápidos, corren SIEMPRE primero)
    test_core_no_pyxel.py       core/ no importa pyxel JAMÁS
    test_core_stdlib_only.py    core/ solo stdlib
    test_random_global_prohibido.py  nada usa `random` global; todo recibe seed
    test_tests_layout.py        UN solo árbol de tests: src/tests/ (regla O1)
    test_render_delgado.py      render/ no muta estado (solo comandos) [por venir]
  core/
    common/            RNG determinista, bus de eventos, tipos base
    sandbox/           golden tests de comandos (salida byte a byte, exit codes)
    curriculum/        DAG válido: sin ciclos, cobertura §6.2 completa [por venir]
    generator/         determinismo por seed + TODA sala resoluble (barrido masivo)
    engine/            run éxito/expulsión headless, combo, economía, post-mortem [por venir]
    state/             save/load ida-y-vuelta idéntico + migraciones [por venir]
    progression/       unlocks SOLO por competencia; aritmética de economía [por venir]
    karma/             N=8, bandas, condiciones de finales §3.4.1 [por venir]
  assets/              fuente bitmap 5×7 (capa 1 + capa 2 Pyxel) — migrado el 28/08
  data/                esquemas JSON: claves, referencias, DAG curricular [por venir]
  integration/
    test_run_canonica.md(→.py)  una incursión COMPLETA resuelta de principio a fin [por venir]
  render/              smoke headless opcional (pyxel.init(headless=True)) [por venir]
```

## Convenciones
- Comando local: `python -m pytest src/tests -q` (desde raíz del repo).
- Determinismo: toda prueba fija seed explícita. Aleatoriedad oculta = bug de test.
- Los tests son ESPECIFICACIÓN: un ejecutor nuevo lee el test del módulo para
  entender el comportamiento esperado antes de leer implementación.
- Sala irresoluble o solución canónica fuera de pool = ROJO (§6.4.4).
- CI mentalidad: suite entera < 1 min en Fase 1; el barrido pesado de seeds
  vive en `tools/harness/`, no en pytest.

## Quién toca qué
- Cada dueño añade tests EN su carpeta con SU rama (mismos dueños que `core/`):
  `src/tests/core/generator/` y `src/tests/core/engine/` → Ornstein
  (`feat/engine`); `src/tests/core/sandbox|curriculum/` → Smough
  (`feat/sandbox`); `src/tests/assets/`, `render/`, `state/`, `progression/`,
  `karma/` → Seath (`feat/meta-ui`).
- `architecture/`: cambiarla exige propuesta en `mejoras/pendiente/` — es la
  constitución del repo, no se toca para «que pase mi PR».
