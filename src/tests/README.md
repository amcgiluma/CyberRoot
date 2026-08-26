# tests/ — La red de seguridad (pytest, headless)

> **Qué garantiza:** que el juego funciona SIN pantalla y que nadie rompe la
> arquitectura. Es el «verificador autónomo» del proyecto: cada PR pasa aquí
> antes de merge (Artorias 💥/✅), y el harness extiende estos tests a escala.

## Estructura

```
tests/
  architecture/      → LA FRONTERA (rápidos, corren SIEMPRE primero)
    test_core_no_pyxel.py       core/ no importa pyxel JAMÁS
    test_rng_inyectada.py       nada usa random global; todo recibe seed
    test_render_delgado.py      render/ no muta estado (solo comandos)
  core/
    sandbox/           golden tests de comandos (salida byte a byte, exit codes)
    curriculum/        DAG válido: sin ciclos, cobertura §6.2 completa
    generator/         determinismo por seed + TODA sala resoluble (barrido masivo)
    engine/            run éxito/expulsión headless, combo, economía, post-mortem
    state/             save/load ida-y-vuelta idéntico + migraciones
    progression/       unlocks SOLO por competencia; aritmética de economía
    karma/             N=8, bandas, condiciones de finales §3.4.1
  data/                esquemas JSON: claves, referencias, DAG curricular
  integration/
    test_run_canonica.md(→.py)  una incursión COMPLETA resuelta de principio a fin
  render/              smoke headless opcional (pyxel.init(headless=True))
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
- Cada dueño añade tests EN su carpeta con SU rama (mismos dueños que `core/`).
- `architecture/`: cambiarla exige propuesta en `mejoras/pendiente/` — es la
  constitución del repo, no se toca para «que pase mi PR».
