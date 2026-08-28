# `core/generator` — generador procedural determinista del cap. 0 (v0)

Entrega de la **tarea O2 del plan 28/08** (Gwyndolin). Primera API determinista
del generador: `generate(seed, chapter, *, variant)` produce **UNA sala** del
cap. 0 «Trabajo en frío» con la piel EXACTA del capítulo y el encargo del
cap. 1 apuntando a su técnico+beat.

Contrato §4.5 (dueño Ornstein): el módulo ENTREGA `Incursion` (y sus dicts
planos); el render/engine los consume. Los textos visibles van como CLAVES
(`story.ch0.ventana`, `story.ch1.e1`, …), jamás hardcodeados en core.

---

## ENTRADA / SALIDA

```
generate(seed: int|str|bytes, chapter=0, *, variant="canonical") -> Incursion
```

| Entrada | Reglas |
|---|---|
| `seed` | Seed ORIGINAL de la run. `bool` → `TypeError` (coherente con `Rng`). `str`/`bytes` se dispersan vía sha256. |
| `chapter` | DEBE ser `0`. Otro valor → `ValueError` avisando de `curriculum.json` (ch1+ llega en la siguiente fase). |
| `variant` | `"canonical"` (piel EXACTA del capítulo, sin decoys, byte a byte idéntica al test de la escena) \| `"practice"` (añade 1–2 decoys de ambientación). Otro → `ValueError`. |

Salida: `Incursion` (decoys/mtimes/ids derivados de la seed; contenedor de las
piezas: `seed`, `chapter`, `contract`, `scaffold`, `room`).

```
validate_incursion(incursion) -> None   # pública; lanza UnsolvableRoomError
```

---

## Reglas duras

1. **Determinismo absoluto.** Prohibido `import random` (arquitectura §1.3).
   Toda variación nace de `Rng(seed)` y sus `fork("decoys")`, `fork("room-id")`,
   `fork("fs")`. Misma seed ⇒ misma `Incursion` en cualquier proceso/cross-PYTHONHASHSEED.
2. **Validación canónica OBLIGATORIA (§6.4.4).** `generate` SIEMPRE valida la
   sala antes de devolverla: ejecuta la secuencia canónica sobre una **copia**
   (`fs.snapshot()`) y comprueba que el encargo queda en el USB. Si algún paso
   no devuelve el exit esperado, o la copia no aparece, lanza
   `UnsolvableRoomError` — una sala irresoluble es un **bug de generación**,
   nunca se entrega. La `Incursion` devuelta conserva SU FS intacto.
3. **Los textos son claves, no cadenas visibles.** `Objective`/`Contract`
   llevan `*_text_key`/`objective_key`; el render resuelve.
4. **JSON-plano estricto en la frontera.** `Incursion.to_dict()` atraviesa
   `ensure_plain` sin excepción (tuples internos ⇒ listas en el dict).

---

## Diseño del andamiaje (run 0) — DECISIÓN PENDIENTE

El andamiaje de la run 0 (cwd inicial y rutas del dossier) queda expuesto como
**DATOS** en `scaffold.options` bajo las 3 opciones del plan (**a/b/c**) y
`scaffold.default = "option_b"` (la más barata de materializar por Manus).
Esto **NO es una decisión de diseño tomada**: la decide **Gwyn esta noche**
(🧭2, plan 28/08 §4). No la adelantamos.

---

## Compromiso «piel v0 en constantes»

En v0 la piel (rutas, contenidos, mtimes, secuencia canónica) vive en
constantes tipadas de `chapter0.py`. Cuando Smough materialice `src/data/`,
migra a `src/data/chapters/chapter0.json` (escena, textos, mtimes, decoys) y el
generador la carga en vez de leer constantes. Dejamos la hoja `chapter0.py`
aislada (leaf) para que esa migración sea mecánica.

`CANON_STEPS` (la secuencia tipada de la solución canónica) vive en `model.py`
convirtiendo `CANON_STEPS_RAW` de `chapter0.py` — así `chapter0` no importa
`model` y se evita un ciclo de import. La secuencia: `ls → cat → cp → cd → ls`
(escena de `00-la-firma.md`); gasto de ruido canónico = 6 (ls1+cat1+cp3+cd0+ls1)
≤ `noise_budget` 12 (⚠️ v1 calibrable).

---

## Estructura

```
src/core/generator/
├── __init__.py    # contrato, re-exports, __version__="0.1.0"
├── errors.py      # GeneratorError, UnsolvableRoomError (§6.4.4)
├── model.py       # modelos inmutables ida-y-vuelta exacta (+ CANON_STEPS)
├── chapter0.py    # piel del cap. 0 como DATOS (leaf) + build_chapter0_fs
├── generator.py   # generate() + validate_incursion()
└── README.md      # este fichero
```

---

## Cómo se testea

`src/tests/core/generator/` — suite determinista (seeds EXPLÍCITAS, sin
`random`). Cubre: determinismo (misma seed, incl. cross-proceso con
PYTHONHASHSEED distinto), semillas distintas ⇒ salas distintas, resolubilidad
(barrido N=50), variante canónica byte a byte (= `test_session_cap0.py`),
contrato de historia, andamiaje, errores y roundtrip dict→ensure_plain→json.

```bash
./.venv/bin/python -m pytest src/tests/core/generator/ -o addopts= -q
./.venv/bin/python -m pytest src/tests -o addopts= -q    # suite completa
```