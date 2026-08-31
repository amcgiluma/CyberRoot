"""session.py — flujo de ENCARGO del capítulo (O1 + O2, 31/08, Ornstein).

Hermano de `postmortem.py`, en el mismo módulo `core/engine`: orquesta el ciclo
completo de un encargo del currículo REAL — listar → abrir → validar →
generar → jugar → cerrar. Headless, solo stdlib (ARCHITECTURE §1).

Une tres piezas:
- `curriculum` (qué encargos hay y sus prereqs),
- `generator` (genera la sala del contrato, determinista por seed),
- `engine.postmortem` (el informe del Auditor, se adjunta al CIERRE — O2).

REGLAS duras heredadas:
- La evaluación de prereqs vive al ABRIR el encargo (🧭8=(b)), NUNCA dentro de
  `generate()` — esta es la API que el engine consulta cuando el jugador acepta.
- `build_postmortem` se CONSUME aquí, pero permanece FUNCIÓN PURA e intacta
  (solo el flujo la llama con `Shell.to_dict()` y el `state` de la sala).
- La seed de sala es DETERMINISTA POR QUEST+SEED: `f"{quest_id}:{run_seed}"`.
- core NO hardcodea prosa: los textos del encargo viajan como claves del
  curriculum (`title_key`/`brief_text_key`); el render las resuelve contra
  `src/data/`.

Una sesión abierta (EncargoSession) retiene la Incursion + la Shell viva: el
bucle de juego muta la sesión; `cerrar_encargo` produce un dict plano con el
informe del Auditor listo para el Hub. Solo stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from core.engine.postmortem import build_postmortem
from core.generator import Incursion, generate
from core.generator.model import Contract
from core.sandbox.shell import DEFAULT_CAP0_COMMANDS, DEFAULT_CH2_COMMANDS, Shell

#: Conjunto de capítulos cuyo flujo de encargo está materializado (v0: 0 y 2).
SUPPORTED_CHAPTERS: frozenset[int] = frozenset({0, 2})

_KARMA_HINT_ES: dict[str, str] = {"blue": "azul", "red": "rojo", "grey": "gris"}


def _commands_for(chapter: int) -> tuple[str, ...]:
    """Set de comandos de la sesión por capítulo (el 0 es escenario sin pipes)."""
    return DEFAULT_CH2_COMMANDS if chapter == 2 else DEFAULT_CAP0_COMMANDS


@dataclass
class EncargoSession:
    """Una sesión de encargo ABIERTA: la Incursion generada + su Shell viva.

    `ejecutar` es la puerta de juego (envuelve `shell.execute`); `shell_dict`
    y `state` alimentan `cerrar_encargo` (→ post-mortem). Headless en el
    sentido de que la Shell es ida-y-vuelta exacta.
    """

    quest_id: str
    chapter: int
    incursion: Incursion
    shell: Shell
    seed: str
    contract: Contract = field(default_factory=lambda: Contract(chapter=0))

    def ejecutar(self, line: str) -> Any:
        """Ejecuta una línea de terminal y muta la sesión."""
        return self.shell.execute(line)

    def shell_dict(self) -> dict[str, Any]:
        """`Shell.to_dict()` — historial REAL que consume el post-mortem."""
        return self.shell.to_dict()

    def state(self) -> dict[str, Any]:
        """`state` plano para `build_postmortem`: el budget de ruido de la sala."""
        return {"noise_budget": self.incursion.room.noise_budget}


def _quest_dict(curriculum: Any, q: Any, knowledge: Iterable[str] | None) -> dict[str, Any]:
    """Encargo del curriculum a dict plano para el flujo, con `abrible`/`falta`."""
    requires = tuple(q.requires)
    d: dict[str, Any] = {
        "id": q.id,
        "chapter": q.chapter,
        "tint": q.tint,
        "karma_hint": _KARMA_HINT_ES.get(q.tint, "gris"),
        "requires": requires,
        "title_key": q.title_key,
        "beat_key": q.beat_key,
    }
    if knowledge is not None:
        have = frozenset(knowledge)
        d["abrible"] = frozenset(requires) <= have
        d["falta"] = sorted(set(requires) - have)
    return d


def listar_encargos(
    curriculum: Any,
    chapter: int,
    *,
    knowledge: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Encargos disponibles de un capítulo, ordenados por id (determinista).

    No genera nada: es la vitrina de la mesa del Hub. Con `knowledge`, cada
    encargo se marca `abrible` (prereqs ⊆ conocimiento) y `falta` los que le
    faltan — pero NO se abre ni se genera aquí (🧭8=(b)).
    """
    if chapter not in SUPPORTED_CHAPTERS:
        raise ValueError(
            f"flujo de encargo no materializado para el capítulo {chapter} "
            f"(v0: 0 y 2)"
        )
    quests = sorted(curriculum.quests_for_chapter(chapter), key=lambda q: q.id)
    return [_quest_dict(curriculum, q, knowledge) for q in quests]


def rechazo_accionable(curriculum: Any, quest_id: str, knowledge: Iterable[str]) -> dict[str, Any]:
    """Qué conceptos le faltan al jugador para abrir `quest_id`.

    El rechazo de apertura es ACCIONABLE: el flujo devuelve los conceptos que
    faltan (por id) para que el jugador sepa qué dominar, no un «no puedes».
    Funciona aunque el encargo no exista (missing = requiere de un quest None).
    """
    quest = curriculum.quest(quest_id)
    requires = tuple(quest.requires) if quest is not None else ()
    have = frozenset(knowledge)
    return {
        "quest_id": quest_id,
        "abrible": frozenset(requires) <= have,
        "missing": sorted(set(requires) - have),
        "requires": requires,
    }


def _seed_de_sala(quest_id: str, run_seed: Any) -> str:
    """Seed DETERMINISTA por quest + seed de run (sala reproducible)."""
    return f"{quest_id}:{run_seed}"


def abrir_encargo(
    curriculum: Any,
    quest_id: str,
    knowledge: Iterable[str],
    *,
    run_seed: Any = 0,
) -> dict[str, Any]:
    """Abre `quest_id`: valida prereqs al ABRIR (🧭8=(b)) y, si procede,
    genera la sala del contrato y monta la sesión jugable.

    - Si faltan prereqs → `{"abrible": False, "missing": [...]}` (rechazo
      accionable), SIN generar nada.
    - Si los tiene → `{"abrible": True, "session": EncargoSession, "quest": ...}`
      con `session.incursion` generada (seed = quest+run_seed) y `session.shell`
      lista para jugar.

    `prereqs_met` se evalúa AQUÍ (al abrir), nunca en `generate()`: la sala se
    genera aunque el capítulo no haya enseñado aún el concepto — es el jugador
    quien decide aceptar el reto.
    """
    quest = curriculum.quest(quest_id)
    if quest is None:
        return {"abrible": False, "missing": list(knowledge), "quest_id": quest_id}
    chapter = quest.chapter
    if chapter not in SUPPORTED_CHAPTERS:
        return {
            "abrible": False,
            "missing": [f"capítulo {chapter} sin flujo materializado"],
            "quest_id": quest_id,
        }

    contract = Contract(
        chapter=chapter,
        objective_key=quest.id,
        brief_text_key=f"{quest.id}.brief",
        karma_hint=_KARMA_HINT_ES.get(quest.tint, "gris"),
    )
    if not contract.prereqs_met(curriculum, knowledge):
        return {
            "abrible": False,
            "missing": sorted(set(quest.requires) - frozenset(knowledge)),
            "quest_id": quest_id,
            "requires": tuple(quest.requires),
        }

    seed = _seed_de_sala(quest_id, run_seed)
    # Cap. 2 → sala del contrato concreto (contract_id); cap. 0 → su única quest.
    incursion = generate(seed, chapter, contract_id=quest.id) if chapter == 2 else generate(seed, chapter)
    session = EncargoSession(
        quest_id=quest_id,
        chapter=chapter,
        incursion=incursion,
        shell=Shell(
            incursion.room.fs.snapshot(),
            host=incursion.room.host,
            commands=_commands_for(chapter),
            cwd=incursion.scaffold.initial_cwd(),
        ),
        seed=seed,
        contract=contract,
    )
    return {
        "abrible": True,
        "session": session,
        "quest": _quest_dict(curriculum, quest, list(knowledge)),
    }


def cerrar_encargo(
    session: EncargoSession, *, modo: str = "completado"
) -> dict[str, Any]:
    """Cierra la sesión del encargo y adjunta el post-mortem del Auditor.

    Al CERRAR (completado o expulsión), el flujo produce `build_postmortem`
    sobre el historial REAL de la sesión y lo empaqueta como dato estructurado:
    `{quest_id, modo, postmortem}`. La función pura de `postmortem.py`
    permanece intacta; aquí SOLO se consume.

    `modo`: "completado" (el encargo se resolvió) o "expulsión" (se cortó por
    ruido/vigilancia). El post-mortem es el mismo; cambia el indicador que el
    Hub muestra (expulsión → liquidación parcial, §7.7).
    """
    if modo not in ("completado", "expulsión"):
        raise ValueError(
            f"modo de cierre desconocido: {modo!r} (espera completado|expulsión)"
        )
    post = build_postmortem(session.shell_dict(), session.state())
    return {"quest_id": session.quest_id, "modo": modo, "postmortem": post}


__all__ = [
    "SUPPORTED_CHAPTERS",
    "EncargoSession",
    "listar_encargos",
    "rechazo_accionable",
    "abrir_encargo",
    "cerrar_encargo",
]