# `core/generator` — generador procedural determinista (v0.2)

Entrega de **O1/O2 del plan 29/08** (Gwyndolin). La API pública
`generate(seed, chapter, *, variant, curriculum)` produce **UNA Incursion** del
cap. 0 «Trabajo en frío» con la piel EXACTA del capítulo. **La sala consume el
curriculum.json real**: su `concept_pool` y su `objective` (la quest) vienen del
currículo, no de constantes hardcodeadas.

Contrato §4.5 (dueño Ornstein): el módulo ENTREGA `Incursion` (y sus dicts
planos); el render/engine los consume. Los textos visibles van como CLAVES
(`story.ch0.ventana`, `story.ch1.e1`, …), jamás hardcodeados en core.

---

## ENTRADA / SALIDA

```python
generate(seed: int|str|bytes, chapter=0, *, variant="canonical",
         curriculum: Curriculum|None = None) -> Incursion
```

| Entrada | Reglas |
|---|---|
| `seed` | Seed ORIGINAL de la run. `bool` → `TypeError` (coherente con `Rng`). `str`/`bytes` se dispersan vía sha256. |
| `chapter` | DEBE ser `0`; otro valor → `ValueError` (ch1+ llega cuando curriculum cubra más capítulos y exista piel). |
| `variant` | `"canonical"` (piel EXACTA del capítulo, sin decoys) \| `"practice"` (1–2 decoys de ambientación). Otro → `ValueError`. |
| `curriculum` | Curriculum ya cargado (el harness lo carga UNA vez y lo reusa en N seeds). `None` → `load_curriculum()``. |

Salida: `Incursion` (`seed`, `chapter`, `contract`, `scaffold`, `room`).

```python
validate_incursion(incursion) -> None     # pública; lanza UnsolvableRoomError
new_session(incursion) -> Shell           # sesión jugable (copia del FS, cwd del scaffold)
```

**`new_session`, la sesión que produce la Incursión** (🧭2, opción B como
comportamiento): copia del FS (la Incursión conserva el suyo intacto), cwd
nacido de `RunScaffold.initial_cwd()` (default `option_b` → `/`), y el set de
comandos del cap. 0. La usa `validate_incursion` y el harness; el engine
montará aquí al jugador.

---

## Consumo del curriculum (O1, 29/08)

- **`concept_pool`** = los ids de los conceptos que el capítulo enseña
  (`Curriculum.chapter_concepts(0)` → `c.ls/cd/cat/cp`), determinista y sin RNG.
  Se acabó el pool hardcodeado con nombres de comando y decoys mezclados: los
  decoys de ambientación viven SOLO en `room.decoys`.
- **La quest** (`objective.story_key`) se toma del **pool del capítulo**
  (`quests_for_chapter`, cap. 0 → `story.ch0.ventana`) y su `requires` debe
  estar cubierto por el pool (§6.4.1): si no, `GeneratorError` accionable.
- Borrar `chapter0.py` como fuente de datos (quest/conceptos) **no rompe la
  generación**: solo sigue aportando la piel (FS, decoys, secuencia canónica).
- El harness puede inyectar `curriculum` para no releer el JSON en cada seed.

---

## Reglas duras

1. **Determinismo absoluto.** Prohibido `import random` (arquitectura §1.3).
   Toda variación nace de `Rng(seed)` y sus `fork`. Misma seed ⇒ misma
   `Incursion` en cualquier proceso/cross-PYTHONHASHSEED.
2. **Validación canónica OBLIGATORIA (§6.4.4).** `generate` SIEMPRE valida la
   sala antes de devolverla ejecutando la secuencia canónica sobre una copia
   (`new_session`); si algún paso no devuelve el exit esperado o la copia no
   aparece en el USB, lanza `UnsolvableRoomError`. La `Incursion` devuelta
   conserva SU FS intacto.
3. **Los textos son claves, no cadenas visibles.**
4. **JSON-plano estricto en la frontera.** `Incursion.to_dict()` atraviesa
   `ensure_plain` sin excepción.

---

## Andamiaje de la run 0 — OPCIÓN B materializada

El `scaffold` expone las 3 opciones a/b/c como DATOS y `default = "option_b"`
(🧭2: `initial_cwd = "/"` y rutas absolutas del dossier; las relativas se
enseñan en el cap. 1). **`new_session` arranca SIEMPRE en
`scaffold.default`'s `initial_cwd`** → la opción B es, desde hoy, el
comportamiento real de la sesión, no solo datos. Si Gwyn materializara otra
opción como `default`, la run arrancaría donde toca sin tocar lógica.

## Costura 🧭8 (documentada, decisión de Gwyn esta noche)

`contract.objective_key = story.ch1.e1` exige `c.ls-la`/`c.permisos-leer`, que
el cap. 0 no enseña. **Hoy NO se resuelve** (plan 29/08): cubierta con test
xfail (`test_costura_navig8.py`) + comentario con el repro. Gwyn decide (a) la
sala contrata `story.ch0.ventana` o (b) los prereqs se evalúan al abrir el
encargo. El `objective` (la quest del cap. 0) YA contrata `story.ch0.ventana`.

---

## Estructura

```
src/core/generator/
├── __init__.py    # contrato, re-exports, __version__ (0.2.0)
├── errors.py      # GeneratorError, UnsolvableRoomError (§6.4.4)
├── model.py       # modelos inmutables (+ CANON_STEPS, RunScaffold.initial_cwd)
├── chapter0.py    # piel del cap. 0 como DATOS (leaf) + build_chapter0_fs
├── generator.py   # generate() / validate_incursion() / new_session()
└── README.md      # este fichero
```

## Cómo se testea

`src/tests/core/generator/` — determinista (seeds EXPLÍCITAS). Cubre
determinismo (misma seed, cross-PYTHONHASHSEED), semillas distintas ⇒ salas
distintas, resolubilidad (barrido N=50), variante canónica byte a byte, consumo
de curriculum (`test_consumo_curriculum.py`), costura 🧭8
(`test_costura_navig8.py`, xfail), contrato, andamiaje, errores y roundtrip.

```bash
./.venv/bin/python -m pytest src/tests/core/generator -o addopts= -q
./.venv/bin/python -m pytest src/tests -o addopts= -q    # suite completa
```

Harness: `tools/harness/` (mismo dueño) corre N seeds y mide resolubilidad /
determinismo / distribución de conceptos — ver su README.