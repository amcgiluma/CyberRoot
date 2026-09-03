"""O1 (01/09, Ornstein) — sala sudo del cap. 3 «Bombas»: la credencial y el
auth.log que coloca el scaffold en el mundo.

La forma FIRMADA de Gwyn (DESIGN §6.1): el `sudo` GANADO es una CREDENCIAL
NARRATIVA, nunca una contraseña tecleada. Materializada como FICHERO del FS
de la sala (se lee con `cat`), según el contrato O1↔S1 del plan 01/09.

`c.sudo` y la quest que lo exige NO existen aún en `curriculum.json` (los
añade Smough/S1 a las 16:00; yo NO toco `src/data/`). Para verificar hoy la
sala sudo CON el generator real, este test construye UN CURRÍCULO AUMENTADO
en memoria (real + `c.sudo` + `story.ch3.sudo`) y lo inyecta en `generate`.
Cuando S1 aterrice, el currículo real lo trae y el generator lo detecta por
`requires ⊇ {c.sudo}` sin cambios.
"""

from __future__ import annotations

import pytest

from core.curriculum import load_curriculum
from core.curriculum.model import Concept, Curriculum, Quest
from core.generator import generate
from core.generator.chapter3 import (
    AUTH_LOG_CONTENT,
    AUTH_LOG_PATH,
    SUDO_CREDENTIAL_CONTENT,
    SUDO_CREDENTIAL_PATH,
)
from core.generator.errors import GeneratorError
from core.sandbox.fs import FsError, FileNode

#: Currículo real (YA exige c.sudo en story.ch3.e4/e5 tras S1 — PR #17).
_REAL = load_curriculum()


def _real_sin_quest_sudo() -> Curriculum:
    """Currículo sin quest GENERABLE del cap. 3 — guarda de honestidad.

    Filtra las quests del cap. 3 que requieren `c.sudo` (story.ch3.e4/e5)
    Y las de procesos (`c.ps`/`c.kill`: e1/e2/e3) para que la generación
    del cap. 3 vuelva a ser un `GeneratorError` accionable.

    OJO (O1, 03/09): filtrar SOLO `c.sudo` ya NO basta — las quests de
    procesos e1/e2/e3 generan sala con demonio (🧭16, opción a).
    """
    real = load_curriculum()
    generables = ("c.sudo", "c.ps", "c.kill")
    filtradas = tuple(
        q for q in real.quests if not any(c in q.requires for c in generables)
    )
    return Curriculum(version=real.version, concepts=real.concepts, quests=filtradas)


def _curriculo_sudo() -> Curriculum:
    """Real + concepto `c.sudo` (escalada, cap. 3) + quest que lo exige."""
    sudo_concept = Concept(
        id="c.sudo",
        family="escalada",
        chapter=3,
        prerequisites=("c.ps",),
        summary_key="concept.sudo.summary",
    )
    sudo_quest = Quest(
        id="story.ch3.sudo",
        chapter=3,
        tint="grey",
        requires=("c.sudo",),
        title_key="story.ch3.sudo.title",
        beat_key="story.ch3.sudo.beat",
    )
    return Curriculum(
        version=_REAL.version,
        concepts=_REAL.concepts + (sudo_concept,),
        quests=_REAL.quests + (sudo_quest,),
    )


def _resolver(inc, path: str):
    return inc.room.fs.resolve(path, "/")


def test_sala_sudo_coloca_credencial_y_auth_log() -> None:
    """AC de O1: la sala sudo del cap. 3 contiene AMBOS ficheros del contrato."""
    cur = _curriculo_sudo()
    inc = generate(42, 3, curriculum=cur)
    assert inc.chapter == 3
    # La credencial es un FICHERO legible con el contenido narrativo (cat).
    cred = _resolver(inc, SUDO_CREDENTIAL_PATH)
    assert isinstance(cred, FileNode)
    assert cred.content == SUDO_CREDENTIAL_CONTENT
    assert cred.content.startswith("ORDEN DE ACCESO")
    # El auth.log está presente (donde S1 firmará cada sudo).
    auth = _resolver(inc, AUTH_LOG_PATH)
    assert isinstance(auth, FileNode)
    assert auth.content == AUTH_LOG_CONTENT


def test_sala_sudo_determinista_por_seed() -> None:
    """Misma seed ⇒ misma Incursion (la sala sudo no rompe el determinismo)."""
    cur = _curriculo_sudo()
    assert generate(7, 3, curriculum=cur).to_dict() == generate(
        7, 3, curriculum=cur
    ).to_dict()
    # Semilla distinta ⇒ otra sala (el canal sd cambia, la piel no).
    r = generate(7, 3, curriculum=cur)
    assert str(r.room.id).startswith("room-ch3-")


def test_sala_sudo_validable_canonica() -> None:
    """`generate` SIEMPRE valida antes de devolver (la canónica `cat` la
    credencial); si la sala sudo fuera irresoluble, lanzaría UnsolvableRoomError."""
    cur = _curriculo_sudo()
    inc = generate(0, 3, curriculum=cur)  # excepción aquí = fallo
    assert inc.room.canon.steps
    for step in inc.room.canon.steps:
        assert step.argv[0] == "cat"


def test_regresion_cap0_sin_credencial_ni_auth_log() -> None:
    """Regresión obligatoria del plan: `generate(seed, 0)` byte-idéntico y SIN
    la sala sudo — el cap. 0 no toca el contrato O1↔S1."""
    cur = _curriculo_sudo()
    a = generate(0, 0, curriculum=cur).to_dict()
    b = generate(0, 0, curriculum=cur).to_dict()
    assert a == b  # determinismo intacto con el currículo aumentado
    # El cap. 0 no expone la credencial ni el auth.log.
    cap0 = generate(11, 0, variant="canonical", curriculum=cur)
    with pytest.raises(FsError):
        _resolver(cap0, SUDO_CREDENTIAL_PATH)
    with pytest.raises(FsError):
        _resolver(cap0, AUTH_LOG_PATH)


def test_generate_cap3_con_curriculo_real_genera_sala_sudo() -> None:
    """Con el currículo REAL (ya con quest sudo — S1/PR #17), pedir el cap. 3
    SÍ produce la sala-credencial (fix #16)."""
    inc = generate(1, 3, curriculum=load_curriculum())
    assert inc.chapter == 3
    assert inc.room.id.startswith("room-ch3-")
    # La credencial está presente en el mundo.
    cred = _resolver(inc, SUDO_CREDENTIAL_PATH)
    assert isinstance(cred, FileNode)
    assert cred.content == SUDO_CREDENTIAL_CONTENT


def test_generate_cap3_sin_quest_sudo_es_error_accionable() -> None:
    """Guarda de honestidad: sin quest GENERABLE del cap. 3 (ni `c.sudo`
    ni `c.ps`/`c.kill`), el cap. 3 es `GeneratorError` accionable, no una
    sala de mentira. (O1, 03/09: filtrar solo `c.sudo` ya no basta.)"""
    with pytest.raises(GeneratorError, match="sin quests"):
        generate(1, 3, curriculum=_real_sin_quest_sudo())


def test_generate_cap3_con_quest_procesos_genera_sala_con_demonio() -> None:
    """O1 (03/09, 🧭16 opción a): pedir una quest de procesos del cap. 3
    (no sudo) YA genera sala — con el demonio dentro y la credencial en el
    mundo. El `GeneratorError` de antes era el contrato pre-O1."""
    cur = _curriculo_sudo()
    inc = generate(1, 3, curriculum=cur, contract_id="story.ch3.e1")
    assert inc.contract.objective_key == "story.ch3.e1"
    assert [(p.pid, p.user) for p in inc.room.fs.processes] == [
        (1, "root"),
        (521, "ceniza"),
        (522, "censo"),
    ]
    cred = _resolver(inc, SUDO_CREDENTIAL_PATH)
    assert isinstance(cred, FileNode)
    assert cred.content == SUDO_CREDENTIAL_CONTENT