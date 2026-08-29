"""generator.py — la API pública del generador procedural determinista.

`generate(seed, chapter, *, variant)` produce UNA `Incursion` del cap. 0 con la
piel EXACTA del capítulo (oficina-vecinal-muelle-norte, ventana de las 11:04,
CANDELAS prov. nº 47) y el encargo del cap. 1 (`story.ch1.e1`) apuntando al
técnico+beat. NO depende de `curriculum.json`: usa los conceptos ya activados
(`ls/cd/cat/cp`).

Reglas duras (ver README.md del módulo):
- DETERMINISMO duro: toda aleatoriedad deriva de la seed de run vía `fork`
  (prohibido `random` global). Misma seed ⇒ misma Incursion, en cualquier
  proceso (splitmix64 + fork, `rng.py`).
- VALIDACIÓN CANÓNICA OBLIGATORIA (§6.4.4): `validate_incursion` ejecuta la
  secuencia canónica sobre una COPIA del FS y lanza `UnsolvableRoomError` si
  la sala no deja resolver el encargo. `generate` SIEMPRE valida antes de
  devolver; una sala irresoluble es un bug de generación.
- El RNG jamás decide semántica: aquí solo elige decoys/mtimes/ids.

Solo stdlib; prohibido `import random`.
"""

from __future__ import annotations

from core.common.rng import Rng
from core.common.types import SeedLike
from core.curriculum import Curriculum, load_curriculum
from core.sandbox.fs import DirNode, FileNode
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, Shell

from core.generator.chapter0 import (
    DECOY_CONTENT,
    DECOY_POOL,
    OFFICE_DIR,
    build_chapter0_fs,
)
from core.generator.errors import GeneratorError, UnsolvableRoomError
from core.generator.model import (
    CANON_STEPS,
    CanonSolution,
    Contract,
    Incursion,
    Objective,
    Room,
    RunScaffold,
)

#: Variantes de sala soportadas en v0.
VARIANTS = ("canonical", "practice")

#: Nota del andamiaje de la run 0 (decisión pendiente de Gwyn, 🧭2 plan 28/08 §4).
_SCAFFOLD_NOTE = (
    "El andamiaje de la run 0 (cwd inicial y rutas del dossier) queda expuesto "
    "como DATOS bajo las 3 opciones a/b/c; la decisión de cuál materializar "
    "es de Gwyn esta noche (🧭2, plan 28/08 §4), NO se toma aquí."
)

#: Las 3 opciones de andamiaje del plan (§4) como datos.
_SCAFFOLD_OPTIONS: dict[str, dict[str, str]] = {
    "option_a": {
        "initial_cwd": "/srv/oficina-vecinal-muelle-norte",
        "tutorial": "navegacion_libre",
    },
    "option_b": {
        "initial_cwd": "/",
        "dossier_paths": "absolutas",
        "relativas_en": "cap1",
    },
    "option_c": {
        "initial_cwd": "/",
        "first_lesson": "error_de_ruta_postmortem_1",
    },
}


def _concept_pool(curriculum: Curriculum, chapter: int) -> tuple[str, ...]:
    """Pool de conceptos de la sala DESDE el currículo (§6.4.2): los ids de los
    conceptos que este capítulo ENSEÑA (`c.ls/cd/cat/cp` en el cap. 0).

    Determinista (`Curriculum.chapter_concepts` ordena por id, cero RNG). Ya NO
    mezcla los nombres de los decoys: un filename no es un concepto; los decoys
    de ambientación viven solo en `room.decoys`.
    """
    return tuple(c.id for c in curriculum.chapter_concepts(chapter))


def new_session(incursion: Incursion) -> Shell:
    """Monta una sesión JUGABLE para la Incursion: copia del FS (la Incursión
    conserva SU FS intacto), cwd nacido del DEFAULT del scaffold (opción B → "/")
    y el set de comandos del cap. 0.

    Esta es la sesión que PRODUCE la Incursión (🧭2, opción B como
    comportamiento): su cwd viene de `RunScaffold.initial_cwd()`, NO del default
    de la Shell. La usa la validación canónica y el harness; el engine montará
    aquí al jugador.
    """
    room = incursion.room
    return Shell(
        room.fs.snapshot(),
        host=room.host,
        commands=DEFAULT_CAP0_COMMANDS,
        cwd=incursion.scaffold.initial_cwd(),
    )


def validate_incursion(incursion: Incursion) -> None:
    """Valida canónicamente la sala (§6.4.4): ejecuta la solución canónica
    sobre una COPIA del FS y comprueba que el encargo queda copiado al USB.

    Lanza `UnsolvableRoomError` si algún paso no devuelve el exit esperado o
    si la copia no aparece en `/usb` con el contenido correcto. La Shell de
    validación es DESECHABLE (`fs.snapshot()`): la `Incursion` devuelta por
    `generate` conserva SU FS intacto.
    """
    room = incursion.room
    shell = new_session(incursion)
    for index, step in enumerate(room.canon.steps):
        line = " ".join(step.argv)
        result = shell.execute(line)
        if result.exit_code != step.expect_exit:
            raise UnsolvableRoomError.from_step(
                step_index=index,
                argv=step.argv,
                expect_exit=step.expect_exit,
                exit_code=result.exit_code,
                stderr=result.stderr,
            )

    # La copia debe existir en el USB (del FS DE VALIDACIÓN, el que el cp
    # mutó) y conservar el contenido del dossier. El FS de la Incursion
    # devuelta queda intacto (se trabaja sobre la snapshot).
    obj = room.objective
    target_path = f"{obj.dst_dir}/{obj.file}"
    try:
        target = shell.fs.resolve(target_path, "/")
    except Exception as exc:  # FsError -> no resuelve
        raise UnsolvableRoomError.from_step(
            step_index=len(room.canon.steps),
            argv=("resolve", target_path),
            expect_exit=0,
            exit_code=1,
            stderr=f"fs.resolve: {exc!r}",
        ) from exc
    if isinstance(target, DirNode):
        raise UnsolvableRoomError.from_step(
            step_index=len(room.canon.steps),
            argv=("cat", target_path),
            expect_exit=0,
            exit_code=1,
            stderr=f"{target_path} existe pero es un directorio",
        )
    if not target.content.startswith("CANDELAS"):
        raise UnsolvableRoomError.from_step(
            step_index=len(room.canon.steps),
            argv=("cat", target_path),
            expect_exit=0,
            exit_code=1,
            stderr="copiada sin el prefijo CANDELAS",
        )


def generate(
    seed: SeedLike,
    chapter: int = 0,
    *,
    variant: str = "canonical",
    curriculum: Curriculum | None = None,
) -> Incursion:
    """Genera UNA Incursion del cap. 0, determinista y validada.

    - `seed`: int | str | bytes (SEED ORIGINAL de la run; bool → TypeError,
      coherente con `Rng`).
    - `chapter`: DEBE ser 0 (v0); otro valor → ValueError con aviso de
      `curriculum.json` (ch1+ llega en la siguiente fase).
    - `variant`: "canonical" (la piel EXACTA del capítulo, sin decoys, byte a
      byte idéntica al test de la escena) o "practice" (añade 1–2 decoys de
      ambientación). Otro valor → ValueError.
    - `curriculum`: Curriculum ya cargado (p.ej. el harness lo carga una vez
      y lo reusa en N seeds). None → `load_curriculum()` lee `curriculum.json`.

    La sala toma su quest del pool del capítulo (`quests_for_chapter`, cap. 0 →
    `story.ch0.ventana`) y su concept_pool del currículo (`c.ls/cd/cat/cp`),
    NO de constantes hardcodeadas: borrar esas constantes como fuente de datos
    no rompe la generación. Termina SIEMPRE validando la sala
    (`validate_incursion`) antes de devolverla (una sala irresoluble es un bug
    y se lanza `UnsolvableRoomError`).
    """
    if isinstance(seed, bool):
        raise TypeError("seed bool no admitida por el generador (usa 0/1 explícitos)")
    if chapter != 0:
        raise ValueError(
            f"solo el cap. 0 está disponible en v0; ch1+ llega con curriculum.json "
            f"(recibido chapter={chapter})"
        )
    if variant not in VARIANTS:
        raise ValueError(f"variant desconocida: {variant!r} (espera canonical|practice)")

    if curriculum is None:
        curriculum = load_curriculum()
    concept_pool = _concept_pool(curriculum, chapter)

    rng = Rng(seed)
    decoy_rng = rng.fork("decoys")
    id_rng = rng.fork("room-id")
    fs_rng = rng.fork("fs")

    fs = build_chapter0_fs(fs_rng)

    decoys: tuple[str, ...] = ()
    if variant == "practice":
        k = decoy_rng.below(2) + 1  # 1 o 2 decoys (determinista)
        chosen = decoy_rng.sample(list(DECOY_POOL), k)
        office_dir = fs.get_dir(OFFICE_DIR, "/")
        for name in chosen:
            mtime = 900 + decoy_rng.integers(0, 144)  # mtime simulado, nunca real
            office_dir.children[name] = FileNode(
                name=name, content=DECOY_CONTENT[name], mtime=mtime
            )
        decoys = tuple(chosen)

    room_id = f"room-ch0-{id_rng.below(2**32):08x}-{variant}"

    contract = Contract(chapter=1)
    # La quest del POOL del capítulo (cap. 0 → story.ch0.ventana): el encargo
    # que esta sala ofrece es un nodo del curriculum.json, no una constante. Su
    # `requires` debe estar cubierto por el concept_pool (§6.4.1).
    ch_quests = curriculum.quests_for_chapter(chapter)
    if not ch_quests:
        raise GeneratorError(
            f"capítulo {chapter} sin quests en curriculum.json: no hay encargo "
            f"que esta sala pueda ofrecer (viola §6.4.1)"
        )
    quest = ch_quests[0]
    missing = set(quest.requires) - set(concept_pool)
    if missing:
        raise GeneratorError(
            f"quest {quest.id!r} requiere conceptos que el capítulo {chapter} "
            f"no enseña: {sorted(missing)} (viola §6.4.1)"
        )
    objective = Objective(story_key=quest.id)
    scaffold = RunScaffold(note=_SCAFFOLD_NOTE, options=_SCAFFOLD_OPTIONS)
    canon = CanonSolution(steps=CANON_STEPS)

    room = Room(
        id=room_id,
        chapter=0,
        fs=fs,
        canon=canon,
        objective=objective,
        concept_pool=concept_pool,
        decoys=decoys,
    )
    incursion = Incursion(
        seed=seed,
        chapter=chapter,
        contract=contract,
        scaffold=scaffold,
        room=room,
    )
    validate_incursion(incursion)
    return incursion


#: Referencias públicas del módulo usadas por el README de contratos.
__all__ = ["generate", "new_session", "validate_incursion", "VARIANTS"]