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
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS, DEFAULT_CH3_COMMANDS, Shell

from core.generator.chapter0 import (
    DECOY_CONTENT,
    DECOY_POOL,
    OFFICE_DIR,
    build_chapter0_fs,
)
from core.generator.chapter2 import (
    CH2_GREP_WC_EXPECTED,
    TURNO,
    TURNO_FILE,
    build_chapter2_fs,
)
from core.generator.chapter3 import (
    AUTH_LOG_PATH,
    SUDO_CREDENTIAL_FILE,
    SUDO_CREDENTIAL_PATH,
    build_chapter3_fs,
)
from core.generator.errors import GeneratorError, UnsolvableRoomError
from core.generator.model import (
    CANON_STEPS,
    CANON_STEPS_CH2,
    CANON_STEPS_CH3_SUDO,
    CanonSolution,
    Contract,
    Incursion,
    Objective,
    Room,
    RunScaffold,
)

#: Variantes de sala soportadas en v0.
VARIANTS = ("canonical", "practice")

#: Tinte kármico del curriculum (blue/red/grey) → pista legible del contrato
#: (azul/rojo/gris). El Scheme de tintes del diseño usa la forma en español
#: como `karma_hint` del `Contract`.
_TINT_ES: dict[str, str] = {"blue": "azul", "red": "rojo", "grey": "gris"}

#: Comandos de la sesión por capítulo (el cap. 0 es escenario sin pipes; el
#: cap. 2 añade grep/wc; el cap. 3 añade ps/env — sets ya definidos en el
#: sandbox).
def _session_commands(chapter: int) -> tuple[str, ...]:
    if chapter == 2:
        return DEFAULT_CH2_COMMANDS
    if chapter == 3:
        return DEFAULT_CH3_COMMANDS
    return DEFAULT_CAP0_COMMANDS

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


def _taught_up_to(curriculum: Curriculum, chapter: int) -> frozenset[str]:
    """Conceptos enseñados en capítulos ≤ `chapter` (invariante §6.4.1).

    Un encargo puede depender de herramientas de capítulos ANTERIORES
    (p.ej. `story.ch2.e5` usa `c.cp`, enseñado en el cap. 0): el invariante
    pedagógico exige que `quest.requires` ⊆ acciones enseñadas en ≤ `chapter`,
    no solo las del propio capítulo. Determinista, sin RNG.
    """
    return frozenset(c.id for c in curriculum.concepts if c.chapter <= chapter)


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
        commands=_session_commands(room.chapter),
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

    # La aserción de resolubilidad final es POR CAPÍTULO (§6.4.4): cada sala
    # debe dejar resolverse con su solución canónica.
    if room.chapter == 0:
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
    elif room.chapter == 2:
        # La golden del cap. 2: la tubería `grep 11:04 ... | wc -l` del canon
        # debe producir EXACTAMENTE la doble apertura (`2`). El exit 0 de la
        # tubería no basta (siempre es 0): el CONTENIDO es la invariante.
        last = shell.history[-1]["result"]
        raw = str(last.get("stdout", ""))
        if raw.strip() != CH2_GREP_WC_EXPECTED:
            raise UnsolvableRoomError.from_step(
                step_index=len(room.canon.steps) - 1,
                argv=("grep", "11:04", TURNO, "|", "wc", "-l"),
                expect_exit=0,
                exit_code=0,
                stderr=f"golden cap. 2 devolvió {raw.strip()!r}, esperaba {CH2_GREP_WC_EXPECTED!r}",
            )
    elif room.chapter == 3:
        # AC de O1 (01/09): la sala sudo del cap. 3 contiene la credencial en
        # `SUDO_CREDENTIAL_PATH` Y el `auth.log` en `AUTH_LOG_PATH`. El canon
        # (`cat` de la credencial) ya prueba la 1.ª; aquí se verifica que
        # AMBAS existen en el FS de validación (la credencial sigue siendo
        # legible y el auth.log está presente para que S1 firme).
        for path in (SUDO_CREDENTIAL_PATH, AUTH_LOG_PATH):
            node = shell.fs.resolve(path, "/")
            if isinstance(node, DirNode):
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps),
                    argv=("resolve", path),
                    expect_exit=0,
                    exit_code=1,
                    stderr=f"{path} existe pero es un directorio",
                )


def generate(
    seed: SeedLike,
    chapter: int = 0,
    *,
    variant: str = "canonical",
    curriculum: Curriculum | None = None,
    contract_id: str | None = None,
) -> Incursion:
    """Genera UNA Incursion determinista y validada, consciente del capítulo.

    - `seed`: int | str | bytes (SEED ORIGINAL de la run; bool → TypeError,
      coherente con `Rng`).
    - `chapter`: 0 (la firma) o 2 (facturas). Otro valor → ValueError.
      Para el cap. 2, `contract_id` elige el encargo concreto del pool
      (`story.ch2.e1`–`e5`); si se omite, el primero del capítulo.
    - `variant`: "canonical" (la piel EXACTA del capítulo, sin decoys) o
      "practice" (añade decoys de ambientación). Otro valor → ValueError.
    - `curriculum`: Curriculum ya cargado (el harness lo reusa en N seeds).
      None → `load_curriculum()` lee `curriculum.json`.
    - `contract_id`: solo para el cap. 2; el encargo que la sala ofrece.

    La sala toma su quest del pool del capítulo (`quests_for_chapter`) y su
    concept_pool del currículo, NO de constantes hardcodeadas (borrar las
    constantes como fuente de datos no rompe la generación). Termina SIEMPRE
    validando la sala (`validate_incursion`) antes de devolverla: una sala
    irresoluble es un bug (UnsolvableRoomError).
    """
    if isinstance(seed, bool):
        raise TypeError("seed bool no admitida por el generador (usa 0/1 explícitos)")
    if chapter not in (0, 2, 3):
        raise ValueError(
            f"solo los caps. 0 (la firma), 2 (facturas) y 3 (Bombas, sala sudo) "
            f"están disponibles en v0.1; el resto llega con curriculum.json "
            f"(recibido chapter={chapter})"
        )
    if variant not in VARIANTS:
        raise ValueError(f"variant desconocida: {variant!r} (espera canonical|practice)")
    if contract_id is not None and chapter not in (2, 3):
        raise ValueError("contract_id solo aplica a los caps. 2 y 3 (el cap. 0 ofrece su única quest)")

    if curriculum is None:
        curriculum = load_curriculum()

    if chapter == 0:
        return _generate_cap0(seed, variant, curriculum)
    if chapter == 2:
        return _generate_cap2(seed, variant, curriculum, contract_id)
    return _generate_cap3(seed, variant, curriculum, contract_id)


def _generate_cap0(
    seed: SeedLike, variant: str, curriculum: Curriculum
) -> Incursion:
    """Ruta del cap. 0 — EXACTAMENTE el comportamiento histórico (regresión)."""
    chapter = 0
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
        chapter=chapter,
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


def _generate_cap2(
    seed: SeedLike,
    variant: str,
    curriculum: Curriculum,
    contract_id: str | None,
) -> Incursion:
    """Ruta del cap. 2 «Facturas»: la oficina con centralita y su golden.

    Construye una sala del cap. 2 determinista por seed. La quest del encargo
    es `contract_id` (si se da, p.ej. `story.ch2.e1`) o la primera del pool
    del capítulo. `generate()` NO evalúa prereqs (🧭8=(b)): la decisión de
    abrir el encargo vive en el engine (`Contract.prereqs_met`), no aquí.
    """
    chapter = 2
    concept_pool = _concept_pool(curriculum, chapter)

    rng = Rng(seed)
    id_rng = rng.fork("room-id")
    fs_rng = rng.fork("fs")

    fs = build_chapter2_fs(fs_rng)
    room_id = f"room-ch2-{id_rng.below(2**32):08x}-{variant}"

    ch_quests = curriculum.quests_for_chapter(chapter)
    if not ch_quests:
        raise GeneratorError(
            f"capítulo {chapter} sin quests en curriculum.json: no hay encargo "
            f"que esta sala pueda ofrecer (viola §6.4.1)"
        )
    if contract_id is not None:
        quest = curriculum.quest(contract_id)
        if quest is None or quest.chapter != chapter:
            raise GeneratorError(
                f"contract_id {contract_id!r} no es un encargo del capítulo {chapter}"
            )
    else:
        quest = ch_quests[0]
    # Invariante §6.4.1 sobre el pool ACUMULADO (≤ capítulo), no solo el del
    # propio cap. 2 (e5 usa `c.cp` del cap. 0).
    missing = set(quest.requires) - _taught_up_to(curriculum, chapter)
    if missing:
        raise GeneratorError(
            f"quest {quest.id!r} requiere conceptos que ningún capítulo ≤ {chapter} "
            f"enseña: {sorted(missing)} (viola §6.4.1)"
        )

    objective = Objective(
        id=f"serie-{quest.id}",
        story_key=quest.id,
        summary_text_key=quest.title_key,
        file=TURNO_FILE,
        src=f"{OFFICE_DIR}/{TURNO}",
    )
    contract = Contract(
        chapter=chapter,
        objective_key=quest.id,
        brief_text_key=f"{quest.id}.brief",
        karma_hint=_TINT_ES.get(quest.tint, "gris"),
    )
    scaffold = RunScaffold(note=_SCAFFOLD_NOTE, options=_SCAFFOLD_OPTIONS)
    canon = CanonSolution(steps=CANON_STEPS_CH2)

    room = Room(
        id=room_id,
        chapter=chapter,
        fs=fs,
        canon=canon,
        objective=objective,
        concept_pool=concept_pool,
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


def _generate_cap3(
    seed: SeedLike,
    variant: str,
    curriculum: Curriculum,
    contract_id: str | None,
) -> Incursion:
    """Ruta de la sala sudo del cap. 3 «Bombas» (O1, 01/09).

    Materializa la forma FIRMADA de Gwyn (DESIGN §6.1): la credencial
    narrativa de `sudo` es un FICHERO del mundo que coloca el scaffold
    (`SUDO_CREDENTIAL_PATH`) y el `auth.log` presente (`AUTH_LOG_PATH`) donde
    S1 firmará cada `sudo`. La canónica de HOY la LEE (`cat`); la ejecución
    real del `sudo` es de S1 y la cubre el ensayo de integración.

    ALCANCE v0: genera SOLO la sala-credencial (la quest del cap. 3 que exige
    `c.sudo`). La generación completa del cap. 3 para las quests de procesos
    (`c.ps`/`c.env`) es una tarea aparte y se apoya en que el sandbox exponga
    el resto; pedir una quest de procesos hoy es un `GeneratorError` claro, no
    una sala de mentira.
    """
    chapter = 3
    concept_pool = _concept_pool(curriculum, chapter)

    rng = Rng(seed)
    id_rng = rng.fork("room-id")
    fs_rng = rng.fork("fs")

    fs = build_chapter3_fs(fs_rng)
    room_id = f"room-ch3-{id_rng.below(2**32):08x}-{variant}"

    ch_quests = curriculum.quests_for_chapter(chapter)
    if not ch_quests:
        raise GeneratorError(
            f"capítulo {chapter} sin quests en curriculum.json: no hay encargo "
            f"que esta sala pueda ofrecer (viola §6.4.1)"
        )
    if contract_id is not None:
        quest = curriculum.quest(contract_id)
        if quest is None or quest.chapter != chapter:
            raise GeneratorError(
                f"contract_id {contract_id!r} no es un encargo del capítulo {chapter}"
            )
    else:
        sudo_quests = [q for q in ch_quests if "c.sudo" in q.requires]
        if not sudo_quests:
            raise GeneratorError(
                f"capítulo {chapter}: ninguna quest del pool exige `c.sudo` — la "
                f"generación completa del cap. 3 (procesos) es una tarea aparte; "
                f"hoy solo se genera la sala-credencial (quest que exige c.sudo)"
            )
        quest = sudo_quests[0]
    if "c.sudo" not in quest.requires:
        raise GeneratorError(
            f"quest {quest.id!r} del cap. {chapter} no exige `c.sudo`: la "
            f"generación v0 del cap. 3 cubre SOLO la sala-credencial sudo"
        )
    # Invariante §6.4.1: `c.sudo` debe estar enseñado en un capítulo ≤ 3.
    missing = set(quest.requires) - _taught_up_to(curriculum, chapter)
    if missing:
        raise GeneratorError(
            f"quest {quest.id!r} requiere conceptos que ningún capítulo ≤ {chapter} "
            f"enseña: {sorted(missing)} (viola §6.4.1)"
        )

    objective = Objective(
        id=f"serie-{quest.id}",
        story_key=quest.id,
        summary_text_key=quest.title_key,
        file=SUDO_CREDENTIAL_FILE,
        src=SUDO_CREDENTIAL_PATH,
    )
    contract = Contract(
        chapter=chapter,
        objective_key=quest.id,
        brief_text_key=f"{quest.id}.brief",
        karma_hint=_TINT_ES.get(quest.tint, "gris"),
    )
    scaffold = RunScaffold(note=_SCAFFOLD_NOTE, options=_SCAFFOLD_OPTIONS)
    canon = CanonSolution(steps=CANON_STEPS_CH3_SUDO)

    room = Room(
        id=room_id,
        chapter=chapter,
        fs=fs,
        canon=canon,
        objective=objective,
        concept_pool=concept_pool,
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