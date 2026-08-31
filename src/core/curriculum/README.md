# curriculum/ — El grafo de verdad único

> **Qué hace:** carga `src/data/curriculum.json` (el DAG de conceptos + los
> encargos como nodos-dato) y responde: ¿qué conceptos tiene desbloqueados
> este jugador? ¿qué pool de práctica corresponde a este capítulo? No conoce
> runs ni salas: conocimiento puro (ARCHITECTURE §2.3, DESIGN §6.2/§6.4).
> **Estado (31/08, Smough — S2):** cap. 0–3 completos, validador del DAG,
> esquema y contrato de consumo documentados.

## Piezas (v0)

| Fichero | Qué hay |
|---|---|
| `model.py` | `Concept` / `Quest` / `Curriculum` (dataclasses FROZEN) + constantes `FAMILIES` (8, DESIGN §6.2), `TINTS` (`blue/red/grey`), `CHAPTERS` (0–6), `SCHEMA_VERSION=1` y `CurriculumError` |
| `validation.py` | `validate(curriculum)` → `CurriculumError` en negativo: **ciclos** (DFS por color, camino legible «a → b → a»), prereq inexistente, prereq de capítulo posterior (§6.4.1), duplicados, capítulo fuera de rango, familia/tint desconocidos, `requires` de quest enseñado después de su capítulo, claves de texto vacías |
| `loader.py` | `load_curriculum(path=None)` → lee `src/data/curriculum.json`; `curriculum_from_dict(doc)` → dict validado → `Curriculum`. Rechaza JSON no plano estricto (`ensure_plain`), versiones desconocidas, campos faltantes y tipos inválidos con mensajes accionables |

## Esquema de `curriculum.json` (version 1)

```jsonc
{
  "version": 1,                       // debe ser 1 (SCHEMA_VERSION)
  "concepts": [                       // lista NO vacía, sin ids duplicados
    {
      "id": "c.cp",                   // str no vacío, único; prefijo "c." por convención
      "family": "navegacion",         // una de FAMILIES (8 familias, DESIGN §6.2)
      "chapter": 0,                   // capítulo de ENSEÑANZA, 0..6
      "prerequisites": ["c.cd"],      // ids existentes; su chapter <= este (§6.4.1)
      "summary_key": "concept.cp.summary"  // clave de texto (core no hardcodea prosa)
    }
  ],
  "quests": [                         // los encargos como nodos-dato (puede ir vacía)
    {
      "id": "story.ch1.e1",           // la clave de historia ES el id
      "chapter": 1,                   // 0..6
      "tint": "blue",                 // blue | red | grey (DESIGN §3.3: tinte visible
                                      // en la descripción, nunca un icono moral)
      "requires": ["c.ls-la"],        // conceptos que la solución canónica usa;
                                      // todos con chapter <= quest.chapter
      "title_key": "story.ch1.e1.title",   // claves de texto (los prosa vive en
      "beat_key": "story.ch1.e1.beat"      // backlog/historia/, entra como clave)
    }
  ]
}
```

Reglas estructurales que el validador impone (y testea en negativo):
- **DAG sin ciclos** — el mensaje de ciclo incluye el camino («a → b → a»).
- **Prereqs existentes y no-futuros** — un concepto se enseña en el mismo
  capítulo o después que cada prereq (invariante pedagógico §6.4.1: nadie
  recibe un reto sin sus herramientas).
- **Quests resolubles cuando llegan** — todo `requires` está enseñado en
  capítulos ≤ el de la quest.
- Textos SIEMPRE como claves (`*_key`): la prosa vive en `data/`/historia.

## Contenido v0 (16 conceptos, 16 quests)

- **Cap. 0 (4):** `c.ls` → `c.cd` → `c.cat` → `c.cp` — EXACTAMENTE el
  `DEFAULT_CAP0_COMMANDS` del sandbox (contrato con generator: la piel del
  cap. 0 sale de aquí). El orden de prereqs es el orden de enseñanza real
  (mirar → moverse → leer → copiar).
- **Cap. 1 (7):** `c.ls-la`, `c.permisos-leer`, `c.chmod`, `c.chown`
  (permisos, familia de §6.2 cap. 1), `c.find`, `c.fechas`, `c.man` —
  derivados de los técnicos de `story.ch1.e1–e5` (CAPITULOS/01-los-muelles.md).
- **Cap. 2 (3, S1+S2 30/08):** `c.grep` → `c.wc` → `c.pipe` (primera
  sinergia de la familia texto — la tubería une los dos comandos que
  encadena). Coherentes con `DEFAULT_CH2_COMMANDS` del sandbox.
- **Cap. 3 (2, S1+S2 31/08):** `c.ps` → `c.env` (familia `procesos`; leer
  qué corre y de quién antes de tocar nada). Coherentes con
  `DEFAULT_CH3_COMMANDS` del sandbox. El `sudo` GANADO es decisión de Gwyn
  (fuera de alcance hasta que defina la forma con datos delante).
- **Quests:** `story.ch0.ventana` (grey, los 4 del cap. 0) + `story.ch1.e1`
  (azul), `e2` (azul), `e3` (gris), `e4` (rojo), `e5` (cierre, gris) +
  `story.ch2.e1`–`e5` (S2, 30/08: E1/E2 azules, E3 gris, E4 rojo, E5 de
  cierre gris — tints según `CAPITULOS/02-facturas.md` de Manus) +
  `story.ch3.e1`–`e5` (S2, 31/08: E1 azul, E2 gris, E3 rojo, E4 rojo, E5 de
  cierre gris — tints según `CAPITULOS/03-bombas.md` de Manus).
  La lista comando a comando de los ~60 boons se cierra contra el sandbox
  real en las fases siguientes (decisión abierta §5.1 de ARCHITECTURE).

## API de consumo (estable — contrato para Ornstein/generator)

```python
from core.curriculum import load_curriculum

cur = load_curriculum()                      # lee src/data/curriculum.json

cur.unlocked({"c.ls", "c.cd"})               # frozenset de ids desbloqueados:
                                             # prereqs ⊆ dominados (NO transitivo)
cur.campaign_pool(1, mastered_ids)           # tuple[Concept,...] ordenado por id:
                                             # conceptos de capítulos <= 1 cuya
                                             # cadena de prereqs ⊆ dominados.
                                             # ES el insumo del muestreo §6.4.2 —
                                             # la ELECCIÓN con RNG es tuya (la
                                             # semilla vive en generator, nunca aquí)
cur.quests_for_chapter(1)                    # tuple[Quest,...] por id (determinista)
cur.quest("story.ch1.e1")                    # Quest | None
cur.concept("c.cp")                          # Concept | None
cur.chapter_concepts(0)                      # conceptos ENSEÑADOS en ese capítulo
```

Garantías: `Curriculum` es frozen (sin estado mutable); `validate` corre
SIEMPRE al cargar (un JSON roto no entra en memoria); consultas sin RNG,
ordenadas por id (determinismo §3); errores = `CurriculumError(CyberRootError)`.
La integración generator↔curriculum se hace en `feat/engine` cuando Ornstein
la tome (las claves `c.ls/cd/cat/cp` ya calzan con sus conceptos activados).

## Cómo se testea

- `./.venv/bin/python -m pytest src/tests/core/curriculum -o addopts= -q`
  (46 tests: 25 validador —cada regla en negativo— + 21 loader sobre el JSON
  real).
- Invariante de datos: el fichero real carga y cumple las reglas del
  validador (no hay «datos que pasan porque nadie los mira»).

## Dueño

Smough (`feat/sandbox`). `src/data/curriculum.json` es del dueño del módulo:
cambios de contenido = rama `feat/sandbox` + PR.
