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
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS, DEFAULT_CH3_COMMANDS, DEFAULT_CH4_COMMANDS, Shell

# O3 — chapter6 trae FS con registro/purgas + cebo pipe-0; sus comandos son
# la familia conteo (head/tail/sort/uniq) + grep/wc. Si Smough añade
# DEFAULT_CH6_COMMANDS mañana, la rama 0902 lo heredará sin conflicto.

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
from core.generator.chapter6 import (
    CANON_STEPS_RAW_CH6_E2,
    CANON_STEPS_RAW_CH6_E2_TAIL,
    CANON_STEPS_RAW_CH6_E3,
    CEBO_PATH,
    CH6_GREP_WC_EXPECTED,
    HOSTS_CONTENT,
    HOSTS_PATH,
    NOTA_CORTE_PATH,
    PURGAS_FILE,
    PURGAS_PATH,
    REGISTRO_PATH,
    build_chapter6_fs,
)
from core.generator.errors import GeneratorError, UnsolvableRoomError
from core.generator.model import (
    CANON_STEPS,
    CANON_STEPS_CH2,
    CANON_STEPS_CH3_SUDO,
    CANON_STEPS_CH6,
    CanonSolution,
    CanonStep,
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
    if chapter == 4:
        return DEFAULT_CH4_COMMANDS
    if chapter == 6:
        # O1 10/09 — «La persiana» necesita ps (START forense) + env/kill/sudo
        # heredados del cap. 3 y la familia conteo. Usa el set canónico del shell
        # para no desfasar allowlist (gate 127). Import lazy para evitar ciclo.
        from core.sandbox.shell import DEFAULT_CH6_COMMANDS as _CH6

        return _CH6
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

    O1 09/09: si la sala es del cap. 4, pre-puebla `shell.hosts` con los FS
    remotos deterministas (faro + troncal-01/02) parseando `/etc/hosts` del FS
    local. Así `scp` funciona sin depender de que el descubrimiento cree stub
    vacío — tanto en validate como en el juego.
    """
    room = incursion.room
    shell = Shell(
        room.fs.snapshot(),
        host=room.host,
        commands=_session_commands(room.chapter),
        cwd=incursion.scaffold.initial_cwd(),
    )
    if room.chapter == 4:
        # Pre-puebla hosts remotos deterministas para que validate/scp funcionen
        try:
            from core.generator.chapter4 import build_ch4_remote_fs, HOSTS_PATH
            from core.sandbox.shell import _parse_hosts_content

            try:
                node = shell.fs.resolve(HOSTS_PATH, "/")
                from core.sandbox.fs import FileNode

                text = node.content if isinstance(node, FileNode) else ""
            except Exception:
                text = ""
            for h in _parse_hosts_content(text):
                if h not in shell.hosts:
                    try:
                        shell.hosts[h] = build_ch4_remote_fs(h)
                    except Exception:
                        pass
        except Exception:
            pass
    return shell


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
    elif room.chapter == 6:
        # AC de O3 (02/09) + E2/E3 (05/09, Seath) + O3 hosts (08/09): la sala-dato contiene
        # la Lista al formato EXACTO + cebo pipe-0 + .nota-corte + /etc/hosts (faro).
        for path in (REGISTRO_PATH, PURGAS_PATH, CEBO_PATH, NOTA_CORTE_PATH, HOSTS_PATH):
            node = shell.fs.resolve(path, "/")
            if isinstance(node, DirNode):
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps),
                    argv=("resolve", path),
                    expect_exit=0,
                    exit_code=1,
                    stderr=f"{path} existe pero es un directorio",
                )
        # Validación por quest (E1/E2/E3 comparten FS, goldens distintas)
        quest_id = room.objective.story_key if hasattr(room.objective, "story_key") else ""
        if quest_id == "story.ch6.dato2":
            # E2: cut|sort|uniq -c debe producir salida con distritos
            last = shell.history[-1]["result"]
            raw = str(last.get("stdout", ""))
            if last.get("exit_code", 1) != 0 or not raw.strip():
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps) - 1,
                    argv=("cut", "-d|", "-f4", PURGAS_PATH, "|", "sort", "|", "uniq", "-c"),
                    expect_exit=0,
                    exit_code=int(last.get("exit_code", 1)),
                    stderr=f"golden E2 vacía/exit {last.get('exit_code')}: {last.get('stderr','')!r}",
                )
            # Debe mencionar al menos un distrito conocido (UMBRAL-BAJO/MUEL-01/--)
            if not any(x in raw for x in ("UMBRAL-BAJO", "MUEL-01", "--")):
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps) - 1,
                    argv=("cut", "-d|", "-f4", PURGAS_PATH, "|", "sort", "|", "uniq", "-c"),
                    expect_exit=0,
                    exit_code=0,
                    stderr=f"golden E2 sin distritos conocidos: {raw.strip()!r}",
                )
            cebo_res = shell.execute(f"grep ENSAYO {CEBO_PATH} | wc -l")
            if cebo_res.stdout.strip() != "0":
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps),
                    argv=("grep", "000", CEBO_PATH, "|", "wc", "-l"),
                    expect_exit=0,
                    exit_code=0,
                    stderr=f"cebo pipe-0 devolvió {cebo_res.stdout.strip()!r}, esperaba '0'",
                )
        elif quest_id == "story.ch6.e2":
            # E2 «La que no pesa» (08/09): tail -n +2 | cut -d'|' -f4 | sort  → sin header fantasma, 2 UMBRAL-BAJO
            last = shell.history[-1]["result"]
            raw = str(last.get("stdout", ""))
            if last.get("exit_code", 1) != 0 or not raw.strip():
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps) - 1,
                    argv=("tail", "-n", "+2", PURGAS_PATH, "|", "cut", "-d'|'", "-f4", "|", "sort"),
                    expect_exit=0,
                    exit_code=int(last.get("exit_code", 1)),
                    stderr=f"golden e2 vacía/exit {last.get('exit_code')}: {last.get('stderr','')!r}",
                )
            # Debe NO contener la cabecera fantasma "distrito" y sí contener duplicado UMBRAL-BAJO
            if "distrito" in raw:
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps) - 1,
                    argv=("tail", "-n", "+2", PURGAS_PATH, "|", "cut", "-d'|'", "-f4", "|", "sort"),
                    expect_exit=0,
                    exit_code=0,
                    stderr=f"golden e2 contiene header fantasma 'distrito': {raw.strip()!r} — tail -n +2 no aplicado",
                )
            if raw.count("UMBRAL-BAJO") != 2:
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps) - 1,
                    argv=("tail", "-n", "+2", PURGAS_PATH, "|", "cut", "-d'|'", "-f4", "|", "sort"),
                    expect_exit=0,
                    exit_code=0,
                    stderr=f"golden e2 esperaba 2 UMBRAL-BAJO (distrito repetido), obtuvo {raw.count('UMBRAL-BAJO')}: {raw.strip()!r}",
                )
            # Verifica que el corte con coma rompe (trampa delimitador) y que el cebo sigue 0
            # Ya validado que hosts existe arriba; no necesita check extra
        elif quest_id == "story.ch6.dato3":
            # E3: sort -k12 | head -n 3 — valida solo si sort soporta -k/-t
            last = shell.history[-1]["result"]
            raw = str(last.get("stdout", ""))
            stderr = str(last.get("stderr", ""))
            has_sort_err = "invalid option" in stderr or "Try 'sort" in stderr
            if last.get("exit_code", 0) != 0 or has_sort_err:
                if has_sort_err:
                    # Falta -k/-t en esta rama sola — valida solo FS y deja pasar
                    pass
                else:
                    raise UnsolvableRoomError.from_step(
                        step_index=len(room.canon.steps) - 1,
                        argv=("sort", "-t|", "-k12", "-n", PURGAS_PATH, "|", "head", "-n", "3"),
                        expect_exit=0,
                        exit_code=int(last.get("exit_code", 1)),
                        stderr=f"golden E3 exit {last.get('exit_code')}: {stderr!r}",
                    )
            else:
                lines = [l for l in raw.splitlines() if l.strip()]
                if len(lines) != 3:
                    raise UnsolvableRoomError.from_step(
                        step_index=len(room.canon.steps) - 1,
                        argv=("sort", "-t|", "-k12", "-n", PURGAS_PATH, "|", "head", "-n", "3"),
                        expect_exit=0,
                        exit_code=0,
                        stderr=f"golden E3 esperaba 3 líneas, devolvió {len(lines)}: {raw.strip()!r}",
                    )
        else:
            # E1 (default) — golden grep ENSAYO
            last = shell.history[-1]["result"]
            raw = str(last.get("stdout", ""))
            if raw.strip() != CH6_GREP_WC_EXPECTED:
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps) - 1,
                    argv=("grep", "ENSAYO", PURGAS_PATH, "|", "wc", "-l"),
                    expect_exit=0,
                    exit_code=0,
                    stderr=f"golden cap. 6 devolvió {raw.strip()!r}, esperaba {CH6_GREP_WC_EXPECTED!r}",
                )
            cebo_res = shell.execute(f"grep ENSAYO {CEBO_PATH} | wc -l")
            if cebo_res.stdout.strip() != "0":
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps),
                    argv=("grep", "000", CEBO_PATH, "|", "wc", "-l"),
                    expect_exit=0,
                    exit_code=0,
                    stderr=f"cebo pipe-0 devolvió {cebo_res.stdout.strip()!r}, esperaba '0'",
                )
    elif room.chapter == 4:
        # AC O1 09/09: sala de red cap.4 — /etc/hosts 2-3 hosts + troncal con volcado + scp canon
        from core.generator.chapter4 import HOSTS_PATH as CH4_HOSTS_PATH, TRONCAL_PATH as CH4_TRONCAL_PATH

        for path in (CH4_HOSTS_PATH,):
            node = shell.fs.resolve(path, "/")
            if isinstance(node, DirNode):
                raise UnsolvableRoomError.from_step(
                    step_index=len(room.canon.steps),
                    argv=("resolve", path),
                    expect_exit=0,
                    exit_code=1,
                    stderr=f"{path} existe pero es un directorio",
                )
        # La canon de ch4 ya ejecutó cat+scp; verifica que el volcado llegó a /tmp
        try:
            target = shell.fs.resolve("/tmp/volcado.csv", "/")
        except Exception as exc:
            raise UnsolvableRoomError.from_step(
                step_index=len(room.canon.steps),
                argv=("resolve", "/tmp/volcado.csv"),
                expect_exit=0,
                exit_code=1,
                stderr=f"/tmp/volcado.csv no existe tras scp canon: {exc!r}",
            ) from exc
        if isinstance(target, DirNode):
            raise UnsolvableRoomError.from_step(
                step_index=len(room.canon.steps),
                argv=("cat", "/tmp/volcado.csv"),
                expect_exit=0,
                exit_code=1,
                stderr="/tmp/volcado.csv existe pero es un directorio",
            )
        if "TR-001" not in target.content:
            raise UnsolvableRoomError.from_step(
                step_index=len(room.canon.steps),
                argv=("cat", "/tmp/volcado.csv"),
                expect_exit=0,
                exit_code=1,
                stderr=f"/tmp/volcado.csv sin TR-001: {target.content[:120]!r}",
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
    if chapter not in (0, 2, 3, 4, 6):
        raise ValueError(
            f"solo los caps. 0 (la firma), 2 (facturas), 3 (Bombas, sala sudo), 4 (Troncales) y 6 (Faro, sala-dato) "
            f"están disponibles en v0.1; el resto llega con curriculum.json "
            f"(recibido chapter={chapter})"
        )
    if variant not in VARIANTS:
        raise ValueError(f"variant desconocida: {variant!r} (espera canonical|practice)")
    if contract_id is not None and chapter not in (2, 3, 4, 6):
        raise ValueError("contract_id solo aplica a los caps. 2, 3, 4 y 6 (el cap. 0 ofrece su única quest)")

    if curriculum is None:
        curriculum = load_curriculum()

    if chapter == 0:
        return _generate_cap0(seed, variant, curriculum)
    if chapter == 2:
        return _generate_cap2(seed, variant, curriculum, contract_id)
    if chapter == 3:
        return _generate_cap3(seed, variant, curriculum, contract_id)
    if chapter == 4:
        return _generate_cap4(seed, variant, curriculum, contract_id)
    return _generate_cap6(seed, variant, curriculum, contract_id)


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


def _requiere_procesos(requires: tuple[str, ...] | list[str]) -> bool:
    """La quest pide el demonio si exige `c.ps` o `c.kill` (O1, plan 03/09).

    `c.kill` no existe aún como concepto del currículo (las quests de
    procesos piden `c.ps`/`c.env`); se acepta por literalidad del plan para
    no reabrir la selección cuando llegue.
    """
    return "c.ps" in requires or "c.kill" in requires


def _generate_cap3(
    seed: SeedLike,
    variant: str,
    curriculum: Curriculum,
    contract_id: str | None,
) -> Incursion:
    """Ruta de la sala sudo del cap. 3 «Bombas» (O1, 01/09 + 03/09).

    Materializa la forma FIRMADA de Gwyn (DESIGN §6.1): la credencial
    narrativa de `sudo` es un FICHERO del mundo que coloca el scaffold
    (`SUDO_CREDENTIAL_PATH`) y el `auth.log` presente (`AUTH_LOG_PATH`) donde
    S1 firmará cada `sudo`. La canónica de HOY la LEE (`cat`); la ejecución
    real del `sudo` es de S1 y la cubre el ensayo de integración.

    O1 (03/09, 🧭16 opción a): ADEMÁS inyecta el demonio LAZY — el par de
    procesos `ceniza:521 --ventana` / `censo:522 --vigilar-censo` (réplica
    del golden de `test_session_kill.py`) — SOLO cuando la quest de la sala
    requiere `c.ps`/`c.kill`. La quest sudo por defecto (`story.ch3.e4`)
    también requiere `c.ps`, así que su sala gana el demonio SIN que la
    credencial ni el `auth.log` cambien un byte (el circuito de S1 intacto).
    """
    chapter = 3
    concept_pool = _concept_pool(curriculum, chapter)

    rng = Rng(seed)
    id_rng = rng.fork("room-id")
    fs_rng = rng.fork("fs")

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
        # La quest sudo sigue siendo la puerta por defecto (e4); si el
        # currículo aún no trae sudo, la primera quest de procesos vale.
        sudo_quests = [q for q in ch_quests if "c.sudo" in q.requires]
        if sudo_quests:
            quest = sudo_quests[0]
        else:
            ps_quests = [q for q in ch_quests if _requiere_procesos(q.requires)]
            if not ps_quests:
                raise GeneratorError(
                    f"capítulo {chapter}: ninguna quest del pool exige `c.sudo` "
                    f"ni `c.ps`/`c.kill` — sin encargo generable para el cap. 3"
                )
            quest = ps_quests[0]
    if "c.sudo" not in quest.requires and not _requiere_procesos(quest.requires):
        raise GeneratorError(
            f"quest {quest.id!r} del cap. {chapter} no exige `c.sudo` ni "
            f"`c.ps`/`c.kill`: el cap. 3 v0 cubre la sala-credencial sudo y "
            f"las salas de procesos, nada más"
        )
    # Invariante §6.4.1: `c.sudo` debe estar enseñado en un capítulo ≤ 3.
    missing = set(quest.requires) - _taught_up_to(curriculum, chapter)
    if missing:
        raise GeneratorError(
            f"quest {quest.id!r} requiere conceptos que ningún capítulo ≤ {chapter} "
            f"enseña: {sorted(missing)} (viola §6.4.1)"
        )

    # O1 (03/09): el demonio entra LAZY — solo si la quest lo pide (`c.ps` /
    # `c.kill`). La credencial + auth.log se colocan SIEMPRE (circuito S1).
    with_processes = _requiere_procesos(quest.requires)
    fs = build_chapter3_fs(fs_rng, with_processes=with_processes)
    room_id = f"room-ch3-{id_rng.below(2**32):08x}-{variant}"

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


def _generate_cap6(
    seed: SeedLike,
    variant: str,
    curriculum: Curriculum,
    contract_id: str | None,
) -> Incursion:
    """Ruta de la sala-dato del cap. 6 «Faro» (O3, 02/09).

    Materializa el worldbuilding del censo de Manus (`CENSO-LISTA.md`) como
    FICHEROS del mundo que se cruzan con la familia conteo (head/tail/sort/
    uniq + grep/wc/pipe). La Lista es el volcado íntegro del censo con las
    marcas de cada purga; la anomalía es la purga `PR-0091` (`sujeto=000`,
    `fecha=EN BLANCO`, `motivo_codigo=ENSAYO`).

    CONTRATO ch6 (costura O3↔S2, Gwyndolin 02/09): quest `story.ch6.e1`
    (grey, familia conteo, objetivo revelar la purga `PR-0091`) ↔ sala-dato
    `registro.csv`/`purgas.csv` (formato CENSO-LISTA.md) + cebo pipe-0
    (`censo-borrador.csv` → `grep 000 | wc -l` = 0). Literales compartidos:
    nombres de ficheros, fila `PR-0091`, cabecera `|`.

    ALCANCE v0: genera SOLO la sala-dato de la Lista (E1). La generación
    completa del cap. 6 para E2–E5 es tarea aparte.
    """
    chapter = 6
    concept_pool = _concept_pool(curriculum, chapter)

    rng = Rng(seed)
    id_rng = rng.fork("room-id")
    fs_rng = rng.fork("fs")

    fs = build_chapter6_fs(fs_rng)
    room_id = f"room-ch6-{id_rng.below(2**32):08x}-{variant}"

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
        # Default: E1 si existe, si no la primera jugable (E1/E2/E3 del plan 05/09)
        candidatos = [q for q in ch_quests if q.id == "story.ch6.e1"]
        if candidatos:
            quest = candidatos[0]
        else:
            quest = ch_quests[0]

    # Invariante §6.4.1 sobre el pool ACUMULADO (≤ capítulo).
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
        file=PURGAS_FILE,
        src=PURGAS_PATH,
    )
    contract = Contract(
        chapter=chapter,
        objective_key=quest.id,
        brief_text_key=f"{quest.id}.brief",
        karma_hint=_TINT_ES.get(quest.tint, "gris"),
    )
    scaffold = RunScaffold(note=_SCAFFOLD_NOTE, options=_SCAFFOLD_OPTIONS)
    # Canon por quest: dato2/dato3/e2 tienen goldens propios.
    if quest.id == "story.ch6.dato2":
        from core.generator.chapter6 import CANON_STEPS_RAW_CH6_E2
        canon = CanonSolution(steps=tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW_CH6_E2))
    elif quest.id == "story.ch6.dato3":
        from core.generator.chapter6 import CANON_STEPS_RAW_CH6_E3
        canon = CanonSolution(steps=tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW_CH6_E3))
    elif quest.id == "story.ch6.e2":
        from core.generator.chapter6 import CANON_STEPS_RAW_CH6_E2_TAIL
        canon = CanonSolution(steps=tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW_CH6_E2_TAIL))
    else:
        canon = CanonSolution(steps=CANON_STEPS_CH6)

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


def _generate_cap4(
    seed: SeedLike,
    variant: str,
    curriculum: Curriculum,
    contract_id: str | None,
) -> Incursion:
    """Ruta de la sala de red del cap. 4 «Troncales» (O1, 09/09).

    Materializa `/etc/hosts` con 2-3 hosts (faro + troncal-01 [+troncal-02])
    + FS remotos deterministas. La sala es ESCENARIO de red: su quest será
    `story.ch4.e1` cuando Smough la traiga en `curriculum.json`; mientras tanto
    usa fallback genérico para no bloquear O1 (costura O↔S con nombres exactos).
    """
    chapter = 4
    concept_pool = _concept_pool(curriculum, chapter)
    # Si el currículo aún no trae conceptos de ch4, usa el acumulado hasta 4
    if not concept_pool:
        try:
            concept_pool = tuple(sorted(_taught_up_to(curriculum, chapter)))
        except Exception:
            concept_pool = ()

    rng = Rng(seed)
    id_rng = rng.fork("room-id")
    fs_rng = rng.fork("fs")

    from core.generator.chapter4 import build_chapter4_fs, CANON_STEPS_RAW_CH4

    fs = build_chapter4_fs(fs_rng)
    room_id = f"room-ch4-{id_rng.below(2**32):08x}-{variant}"

    # Quest: intenta coger la del pool ch4, si no existe fallback genérico
    ch_quests = curriculum.quests_for_chapter(chapter) if hasattr(curriculum, "quests_for_chapter") else []
    quest = None
    if contract_id is not None:
        quest = curriculum.quest(contract_id) if hasattr(curriculum, "quest") else None
        if quest is None or quest.chapter != chapter:
            raise GeneratorError(f"contract_id {contract_id!r} no es un encargo del capítulo {chapter}")
    else:
        if ch_quests:
            # Prefiere story.ch4.e1 si existe
            e1 = [q for q in ch_quests if q.id == "story.ch4.e1"]
            quest = e1[0] if e1 else ch_quests[0]
        else:
            quest = None

    if quest is not None:
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
            file="volcado.csv",
            src=f"/srv/archivo-troncal/volcado.csv",
        )
        contract = Contract(
            chapter=chapter,
            objective_key=quest.id,
            brief_text_key=f"{quest.id}.brief",
            karma_hint=_TINT_ES.get(quest.tint, "gris"),
        )
    else:
        # Fallback sin quest aún en curriculum (09/09 antes de O2)
        objective = Objective(
            id="serie-story.ch4.e1",
            story_key="story.ch4.e1",
            summary_text_key="story.ch4.e1.brief",
            file="volcado.csv",
            src="/srv/archivo-troncal/volcado.csv",
        )
        contract = Contract(
            chapter=chapter,
            objective_key="story.ch4.e1",
            brief_text_key="story.ch4.e1.brief",
            karma_hint="azul",
        )

    scaffold = RunScaffold(note=_SCAFFOLD_NOTE, options=_SCAFFOLD_OPTIONS)
    canon = CanonSolution(steps=tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW_CH4))

    room = Room(
        id=room_id,
        chapter=chapter,
        fs=fs,
        canon=canon,
        objective=objective,
        concept_pool=concept_pool if concept_pool else ("c.scp",),
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