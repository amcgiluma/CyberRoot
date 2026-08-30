"""🧭8 (Oscar, 29/08 → materializada como (b) por Ornstein 30/08): la costura
del contrato del cap. 0 queda CERRADA por la vía (b) que firmó Gwyn.

El `contract.objective_key` del cap. 0 apunta a `story.ch1.e1` (el encargo
AZUL del cap. 1), cuyos prereqs (`c.ls-la`, `c.permisos-leer`) el cap. 0 NO
enseña (su pool es solo `c.ls/cd/cat/cp`). Antes del 30/08 este desajuste
estaba CUBIERTO por un test xfail. Gwyn eligió la opción (b) de DESIGN §6.1:

    (b) los prereqs de un encargo se evalúan al ABRIRLO, no al generar la
        sala. La sala es ESCENARIO (ofrece la entrada a ese encargo); el
        contrato es un COMPROMISO DEL JUGADOR, no una auto-resolución de la
        sala.

Con (b) materializada, la invariante que el xfail exigía (que la quest del
contrato fuera resoluble con el pool del cap. 0) ya NO es la correcta: la
sala puede contratar un encargo que el capítulo aún no enseña. Lo que sí es
normativo es:

  1. `generate(seed, 0)` sigue generando intacto (la sala es escenario, no
     evalúa los prereqs del contrato dentro de `generate()`).
  2. La evaluación de prereqs vive en la API `contract.prereqs_met(knowledge)`
     (o `prereqs_met(curriculum, knowledge)`), que se llama AL ABRIR el
     encargo — nunca dentro del generador.
  3. La API se testea en ambos casos: SIN los prereqs (cap. 0 terminado →
     el encargo aún NO se abre) y CON ellos (cap. 1 dominado → SÍ se abre).

Esto mata el único xfail de la suite (0 xfails al cerrar el día).
"""
from __future__ import annotations

from core.curriculum import load_curriculum
from core.generator import generate


def test_generate_no_evalua_prereqs_del_contrato() -> None:
    """La sala del cap. 0 se genera intacta; el contrato sigue apuntando al
    encargo del cap. 1 aunque sus prereqs no estén en el pool del cap. 0.

    Es la materialización de (b): `generate()` NO resuelve `story.ch1.e1`,
    lo único que hace es contratarlo como escenario. Si `generate()` volviera
    a intentar validar los prereqs del contrato (vía (a)-style), esto fallaría.
    """
    inc = generate(7, 0)
    # El contrato conserva la costura: apunta al encargo del cap. 1.
    assert inc.contract.objective_key == "story.ch1.e1"
    assert inc.contract.brief_text_key == "story.ch1.e1.brief"
    # La sala sigue siendo del cap. 0 con su pool correcto.
    assert inc.room.concept_pool == ("c.cat", "c.cd", "c.cp", "c.ls")


def test_prereqs_met_falso_sin_los_conceptos() -> None:
    """Al ABRIR el encargo SIN los prereqs dominados → no se abre.

    El cap. 0 terminado deja `knowledge` con `c.ls/cd/cat/cp` (o incluso
    vacío). El encargo `story.ch1.e1` exige `c.ls-la` y `c.permisos-leer`,
    que no se dominaron → `prereqs_met` devuelve False.
    """
    inc = generate(7, 0)
    cur = load_curriculum()
    cap0_knowledge = {"c.ls", "c.cd", "c.cat", "c.cp"}
    assert not inc.contract.prereqs_met(cur, cap0_knowledge)


def test_prereqs_met_verdadero_con_los_conceptos() -> None:
    """AL ABRIR el encargo CON los prereqs dominados → se abre.

    Cuando el jugador dominó `c.ls-la` y `c.permisos-leer` (cap. 1), el
    contrato se resuelve: `prereqs_met` devuelve True.
    """
    inc = generate(7, 0)
    cur = load_curriculum()
    cap1_knowledge = {
        "c.ls",
        "c.cd",
        "c.cat",
        "c.cp",
        "c.ls-la",
        "c.permisos-leer",
    }
    assert inc.contract.prereqs_met(cur, cap1_knowledge)


def test_prereqs_met_ignora_knowledge_irrelevante() -> None:
    """Dominar conceptos que el encargo no pide NO abre el encargo.

    Conocimiento ajeno (p. ej. un concepto de red) sin `c.ls-la`/`c.permisos-
    leer` no cumple la condición: la evaluación mira los `requires` EXACTOS
    de la quest, no cualquier concepto dominado.
    """
    inc = generate(7, 0)
    cur = load_curriculum()
    ajeno = {"c.ssh", "c.grep", "c.ls", "c.cd", "c.cat", "c.cp"}
    assert not inc.contract.prereqs_met(cur, ajeno)


def test_prereqs_met_contrato_con_curriculum_nulo_o_quest_ausente() -> None:
    """Un contrato cuyo objective_key no existe no se considera abierto.

    Caso robusto: si `curriculum` es None o la quest no está en el JSON,
    `prereqs_met` no debe explotar sino devolver False (no evaluable → no se
    abre). Es la política de seguridad de (b) ante datos incompletos.
    """
    inc = generate(7, 0)
    assert not inc.contract.prereqs_met(None, {"c.ls-la", "c.permisos-leer"})
    # Mutamos el objective_key a uno inexistente simulando un JSON incompleto.
    from core.generator.model import Contract

    c = Contract(chapter=0, objective_key="story.sea.inexistente")
    cur = load_curriculum()
    assert not c.prereqs_met(cur, {"c.ls-la", "c.permisos-leer"})