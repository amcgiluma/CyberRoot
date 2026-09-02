# `core/generator` — generador procedural determinista (v0.3)

Entrega de **O1/O2 del plan 29/08** (Gwyndolin, v0.2) y **O1 del 31/08**
(Ornstein, v0.3: soporte del cap. 2 «Facturas»). La API pública
`generate(seed, chapter, *, variant, curriculum, contract_id)` produce **UNA
Incursion** del cap. 0 «Trabajo en frío» o del cap. 2 «Facturas» con la piel
EXACTA del capítulo. **La sala consume el curriculum.json real**: su
`concept_pool` y su `objective` (la quest) vienen del currículo, no de
constantes hardcodeadas.

Contrato §4.5 (dueño Ornstein): el módulo ENTREGA `Incursion` (y sus dicts
planos); el render/engine los consume. Los textos visibles van como CLAVES
(`story.ch0.ventana`, `story.ch1.e1`, …), jamás hardcodeados en core.

---

## ENTRADA / SALIDA

```python
generate(seed: int|str|bytes, chapter=0, *, variant="canonical",
         curriculum: Curriculum|None = None,
         contract_id: str|None = None) -> Incursion
```

| Entrada | Reglas |
|---|---|
| `seed` | Seed ORIGINAL de la run. `bool` → `TypeError` (coherente con `Rng`). `str`/`bytes` se dispersan vía sha256. |
| `chapter` | v0: `0` (Trabajo en frío) o `2` (Facturas). Otro → `ValueError` (el resto llega cuando curriculum cubra más capítulos y exista piel). |
| `variant` | `"canonical"` (piel EXACTA del capítulo, sin decoys) \| `"practice"` (1–2 decoys de ambientación). Otro → `ValueError`. |
| `curriculum` | Curriculum ya cargado (el harness lo carga UNA vez y lo reusa en N seeds). `None` → `load_curriculum()``. |
| `contract_id` | Cap. 2: el encargo concreto del pool (`story.ch2.e1`–`e5`); omitido → el primero. Cap. 0 → `ValueError` (ofrece su única quest). |

Salida: `Incursion` (`seed`, `chapter`, `contract`, `scaffold`, `room`).

```python
validate_incursion(incursion) -> None     # pública; lanza UnsolvableRoomError
new_session(incursion) -> Shell           # sesión jugable (copia del FS, cwd del scaffold)
```

**`new_session`, la sesión que produce la Incursión** (🧭2, opción B como
comportamiento): copia del FS (la Incursión conserva el suyo intacto), cwd
nacido de `RunScaffold.initial_cwd()` (default `option_b` → `/`), y el set de
comandos POR CAPÍTULO (cap. 0 → `DEFAULT_CAP0_COMMANDS`; cap. 2 →
`DEFAULT_CH2_COMMANDS`, que añade `grep`/`wc`). La usa `validate_incursion` y
el harness; el engine monta aquí al jugador.

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

## Costura 🧭8 — OPCIÓN (b) MATERIALIZADA (Ornstein, 30/08)

`contract.objective_key = story.ch1.e1` exige `c.ls-la`/`c.permisos-leer`,
que el cap. 0 no enseña. Gwyn eligió la opción **(b)** (DESIGN §6.1): la sala
es ESCENARIO — ofrece la entrada a ese encargo azul del cap. 1 — y los prereqs
se evalúan al **ABRIR** el encargo, nunca dentro de `generate()`. La API es
`Contract.prereqs_met(curriculum, knowledge)` (se llama cuando el engine abre
el contrato). `generate()` NO valida esos prereqs: solo contrata
`story.ch1.e1` como dato. El test `test_costura_navig8.py` pasó de xfail a
VERDE (0 xfails en la suite).

---

## v0.3 — Cap. 2 «Facturas» (O1, 31/08)

`generate(seed, chapter=2, contract_id="story.ch2.e1")` construye la sala del
cap. 2: el FS de la oficina (cap. 0) EXTENDIDO con `centralita/turnos/
turno.log` (nueva hoja `chapter2.py`) y una secuencia canónica que VERIFICA la
línea golden del capítulo (`grep 11:04 centralita/turnos/turno.log | wc -l`
→ `2`). La validación canónica es POR CAPÍTULO (cap. 0 → copia CANDELAS al
USB; cap. 2 → el conteo de la golden). `generate(seed,0)` queda byte-a-byte
idéntico (regresión cubierta). `generate()` sigue sin evaluar prereqs
(🧭8=(b)): el pool acumulado (§6.4.1) se comprueba contra lo enseñado en
capítulos ≤ `chapter` (e5 usa `c.cp` del cap. 0).

---

## v0.4 — Sala sudo del cap. 3 «Bombas» (O1, 01/09)

`generate(seed, chapter=3, contract_id=<quest-sudo>)` construye la
sala-credencial del cap. 3: el scaffold coloca en el FS de la sala la
**credencial narrativa** (`SUDO_CREDENTIAL_PATH`, una orden firmada por
Ceniza — DESIGN §6.1: nunca una contraseña tecleada) y el **`auth.log`**
presente (`AUTH_LOG_PATH`), donde S1 firmará cada `sudo` («el poder deja
factura»). La canónica v0 la LEE (`cat`); la ejecución real del `sudo` es de
S1 (sandbox) y la cubre el ensayo de integración de Artorias.

### ⚠️ CONTRATO O1↔S1 (por literales, NO por import)

El sandbox NO importa del generator (dependencia prohibida, ARCHITECTURE §2).
La coordinación es por CONVENCIÓN, verificada por Artorias en el gate:

| Constante (chapter3.py) | Valor | Lo hace |
|---|---|---|
| `SUDO_CREDENTIAL_PATH` | `/srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt` | O1 la coloca; S1 la LEE (sin credencial → rechazo diegético; con credencial → ejecuta + ruido premium) |
| `AUTH_LOG_PATH` | `/var/log/auth.log` | O1 la deja presente; S1 AÑADE la firma de cada sudo |

Si cambian, cambian A LA VEZ en `feat/engine` (este módulo) y en
`feat/sandbox` (S1).

### Alcance v0

Solo la sala-credencial: una quest del cap. 3 que exija `c.sudo`. La
generación completa del cap. 3 (quests de procesos `c.ps`/`c.env`) es una
tarea aparte; pedirla hoy es un `GeneratorError` claro. `c.sudo` y su quest
llegan a `curriculum.json` con S1 (16:00); el generator lo detecta por
`requires ⊇ {c.sudo}` sin cambios. Test: `test_sala_sudo.py` (currículo
aumentado en memoria).

## Estructura

```
src/core/generator/
├── __init__.py    # contrato, re-exports, __version__ (0.2.0)
├── errors.py      # GeneratorError, UnsolvableRoomError (§6.4.4)
├── model.py       # modelos inmutables (+ CANON_STEPS, RunScaffold.initial_cwd)
├── chapter0.py    # piel del cap. 0 como DATOS (leaf) + build_chapter0_fs
├── chapter2.py    # piel del cap. 2 como DATOS (leaf) + build_chapter2_fs (v0.3)
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