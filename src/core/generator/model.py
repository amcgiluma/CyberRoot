"""model.py — objetos de valor del generador (INMUTABLES, ida-y-vuelta exacta).

Los `to_dict`/`from_dict` son inversas exactas y la frontera usa TUPLES
internamente ↔ LISTAS en el dict plano (el contrato JSON-plano estricto de
`ensure_plain` rechaza tuples). `Room.fs` viaja como `{"fs": fs.to_dict()}`
y se reconstruye con `FileSystem.from_dict`.

Estos datos son el CONTRATO §4.5 que el generador entrega al resto del core:
el render/engine los consume como dicts planos; la clase es solo la forma
tipada de construirlos (dueño Ornstein).

Solo stdlib; prohibido `import random`; sin estado global mutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from core.sandbox.fs import FileSystem

from core.generator.chapter0 import (
    OFFICE_DIR,
    PROVIDER_FILE,
    USB_DIR,
    CANON_STEPS_RAW,
)
from core.generator.chapter2 import CANON_STEPS_RAW_CH2
from core.generator.chapter3 import CANON_STEPS_RAW_CH3_SUDO
from core.generator.chapter6 import CANON_STEPS_RAW_CH6
from core.generator.errors import GeneratorError

#: La secuencia canónica como data tipada (conversión de la RAW de chapter0).
#: Vive AQUÍ (no en chapter0.py) para no crear un ciclo de import: chapter0
#: es una HOJA y no importa `model`; `model` importa los datos de chapter0.
#: Es la solución canónica y DEBE seguir resolviendo la sala byte a byte.
CANON_STEPS: tuple["CanonStep", ...] = ()
# (se rellena tras definir CanonStep, abajo)


@dataclass(frozen=True)
class CanonStep:
    """Un paso de la solución canónica: argv + exit code esperado."""

    argv: tuple[str, ...]
    expect_exit: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"argv": list(self.argv), "expect_exit": self.expect_exit}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "CanonStep":
        return cls(argv=tuple(str(a) for a in d["argv"]), expect_exit=int(d["expect_exit"]))


#: Rellenamos la constante con los pasos reales (tras definir la clase).
CANON_STEPS = tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW)

#: Secuencia canónica del cap. 2 («Facturas»): cd a la oficina + la golden
#: `grep 11:04 centralita/turnos/turno.log | wc -l` → "2" (S1 / O1, 31/08).
CANON_STEPS_CH2 = tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW_CH2)

#: Secuencia canónica de la sala sudo del cap. 3 («Bombas», O1 01/09): en v0
#: lee la credencial (`cat`) — la ejecución real del `sudo` es de S1 y la
#: cubre el ensayo de integración. Ver cabecera de `chapter3.py`.
CANON_STEPS_CH3_SUDO = tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW_CH3_SUDO)

#: Secuencia canónica de la sala-dato del cap. 6 «Faro» (O3 02/09): revela la
#: purga de nadie contando `000` en purgas.csv — `grep 000 | wc -l` → "1".
CANON_STEPS_CH6 = tuple(CanonStep(argv=raw) for raw in CANON_STEPS_RAW_CH6)


@dataclass(frozen=True)
class CanonSolution:
    """La solución canónica de la sala: secuencia ORDENADA de pasos."""

    steps: tuple[CanonStep, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"steps": [s.to_dict() for s in self.steps]}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "CanonSolution":
        return cls(steps=tuple(CanonStep.from_dict(s) for s in d["steps"]))


@dataclass(frozen=True)
class Objective:
    """El encargo del cap. 0: qué fichero y a dónde (textos por clave)."""

    id: str = "copy-provider-file"
    story_key: str = "story.ch0.ventana"
    summary_text_key: str = "story.ch0.dossier"
    file: str = PROVIDER_FILE
    src: str = f"{OFFICE_DIR}/{PROVIDER_FILE}"
    dst_dir: str = USB_DIR

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "story_key": self.story_key,
            "summary_text_key": self.summary_text_key,
            "file": self.file,
            "src": self.src,
            "dst_dir": self.dst_dir,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Objective":
        return cls(
            id=str(d["id"]),
            story_key=str(d["story_key"]),
            summary_text_key=str(d["summary_text_key"]),
            file=str(d["file"]),
            src=str(d["src"]),
            dst_dir=str(d["dst_dir"]),
        )


@dataclass(frozen=True)
class Contract:
    """Contrato de historia: el encargo AZUL del cap. 1 que esta sala inicia.

    Tras 🧭8=(b) (Gwyn, DESIGN §6.1) la sala SIGUE contratando
    `objectives` del cap. 1 (`story.ch1.e1`) aunque sus `requires`
    (`c.ls-la`, `c.permisos-leer`) NO estén en el pool del cap. 0: la sala
    es ESCENARIO (ofrece la entrada a ese encargo) y la evaluación de
    prereqs vive en `prereqs_met`, que se llama al ABRIR el encargo — NUNCA
    dentro de `generate()`. Un contrato cuyo objective_key no existe en el
    currículo se reporta como NO satisfecho (no evaluable → no se abre).
    """

    chapter: int
    objective_key: str = "story.ch1.e1"
    brief_text_key: str = "story.ch1.e1.brief"
    karma_hint: str = "azul"

    def prereqs_met(self, curriculum: Any, knowledge: Iterable[str]) -> bool:
        """¿Están los prereqs del encargo del contrato cubiertos por `knowledge`?

        API de evaluación 🧭8=(b): se invoca al ABRIR el encargo (el engine
        la consulta cuando el jugador lo acepta), nunca durante la
        generación de la sala. La sala puede contratar un encargo que el
        capítulo aún no enseña; es el JUGADOR quien debe dominar antes.

        - `curriculum`: un `Curriculum` (o duck-type con `.quest(id)`); si
          `objective_key` no existe → False (no evaluable → no se abre).
        - `knowledge`: iterable de ids de conceptos dominados (p. ej.
          `state.knowledge`).
        - Devuelve True si todos los `requires` del encargo ⊆ `knowledge`.
        """
        quest = curriculum.quest(self.objective_key) if curriculum else None
        if quest is None:
            return False
        return frozenset(quest.requires) <= frozenset(knowledge)

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "objective_key": self.objective_key,
            "brief_text_key": self.brief_text_key,
            "karma_hint": self.karma_hint,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Contract":
        return cls(
            chapter=int(d["chapter"]),
            objective_key=str(d["objective_key"]),
            brief_text_key=str(d["brief_text_key"]),
            karma_hint=str(d["karma_hint"]),
        )


@dataclass(frozen=True)
class RunScaffold:
    """Andamiaje de la run 0: cwd inicial y rutas del dossier — DATOS.

    ⚠️ La decisión de qué opción materializar es de Gwyn (🧭2, plan 28/08 §4),
    NO una decisión de diseño tomada aquí. Exponemos las 3 opciones a/b/c como
    datos; `default` marca la más barata de materializar por Manus.
    """

    note: str
    options: dict[str, dict[str, str]] = field(default_factory=dict)
    default: str = "option_b"

    def to_dict(self) -> dict[str, Any]:
        return {"note": self.note, "options": self.options, "default": self.default}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "RunScaffold":
        return cls(
            note=str(d["note"]),
            options={str(k): dict(v) for k, v in d["options"].items()},
            default=str(d["default"]),
        )

    def initial_cwd(self) -> str:
        """cwd inicial de la sesión según el DEFAULT del scaffold (opción B → "/").

        La sesión que produce la Incursión nace AQUÍ (`generator.new_session`),
        NO en el default de la Shell: es la opción B como COMPORTAMIENTO (🧭2).
        Si Gwyn materializara mañana otra opción como `default`, la run
        arrancaría donde toca sin tocar lógica de generación.
        """
        options = self.options.get(self.default)
        if options is None or "initial_cwd" not in options:
            raise GeneratorError(
                f"scaffold default={self.default!r} sin 'initial_cwd' en options"
            )
        return options["initial_cwd"]


@dataclass(frozen=True)
class Room:
    """Una sala generada del cap. 0: FS + solución canónica + encargo.

    Los campos con valores por defecto van AL FINAL (requisito de dataclass):
    el orden conceptual del plan y este son equivalentes en serialización.
    """

    id: str
    chapter: int
    fs: FileSystem
    canon: CanonSolution
    objective: Objective
    type: str = "datos"  # plantilla §6.4.3
    host: str = "oficina-vecinal-muelle-norte"
    concept_pool: tuple[str, ...] = ("c.cat", "c.cd", "c.cp", "c.ls")
    decoys: tuple[str, ...] = ()
    noise_budget: int = 12  # ⚠️ v1 calibrable; la canónica gasta 6

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "chapter": self.chapter,
            "host": self.host,
            "concept_pool": list(self.concept_pool),
            "fs": self.fs.to_dict(),
            "canon": self.canon.to_dict(),
            "objective": self.objective.to_dict(),
            "decoys": list(self.decoys),
            "noise_budget": self.noise_budget,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Room":
        return cls(
            id=str(d["id"]),
            type=str(d["type"]),
            chapter=int(d["chapter"]),
            host=str(d["host"]),
            concept_pool=tuple(str(c) for c in d["concept_pool"]),
            fs=FileSystem.from_dict(d["fs"]),
            canon=CanonSolution.from_dict(d["canon"]),
            objective=Objective.from_dict(d["objective"]),
            decoys=tuple(str(x) for x in d["decoys"]),
            noise_budget=int(d["noise_budget"]),
        )


@dataclass(frozen=True)
class Incursion:
    """La run completa: seed ORIGINAL + capítulo + contrato + andamiaje + sala."""

    seed: int | str
    chapter: int
    contract: Contract
    scaffold: RunScaffold
    room: Room

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "chapter": self.chapter,
            "contract": self.contract.to_dict(),
            "scaffold": self.scaffold.to_dict(),
            "room": self.room.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Incursion":
        return cls(
            seed=d["seed"],
            chapter=int(d["chapter"]),
            contract=Contract.from_dict(d["contract"]),
            scaffold=RunScaffold.from_dict(d["scaffold"]),
            room=Room.from_dict(d["room"]),
        )