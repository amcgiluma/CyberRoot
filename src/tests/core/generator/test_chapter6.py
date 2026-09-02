"""O3 (02/09, Ornstein) — sala-dato del cap. 6 «Faro»: la Lista + cebo pipe-0.

La Lista (§2.4/§9) es el volcado íntegro del censo con las marcas de cada
purga; `CENSO-LISTA.md` es la fuente de verdad narrativa. La sala-dato
materializa `registro.csv`/`purgas.csv` al formato EXACTO (delimitador `|`,
fila `PR-0091` con fecha `EN BLANCO`, sujeto `000`, motivo `ENSAYO`) + el
cebo pipe-0 (`censo-borrador.csv` → `grep 000 | wc -l` = 0).

Lección de los 2 tests stale de #16: el test que asuma la quest REAL
`story.ch6.e1` va con `skipif` hasta que S2 la ponga (solo Smough toca
`curriculum.json` hoy). La costura O3↔S2 la verifica Artorias en la combinada.
"""

from __future__ import annotations

import pytest

from core.curriculum import load_curriculum
from core.curriculum.model import Curriculum, Quest
from core.generator import GeneratorError, generate
from core.generator.chapter6 import (
    CEBO_CONTENT,
    CEBO_PATH,
    PURGAS_CONTENT,
    PURGAS_PATH,
    REGISTRO_CONTENT,
    REGISTRO_PATH,
)
from core.sandbox.fs import FileNode

_REAL = load_curriculum()
_HAS_CH6_E1 = _REAL.quest("story.ch6.e1") is not None


def _curriculo_ch6() -> Curriculum:
    """Currículo en memoria con la quest `story.ch6.e1` del CONTRATO ch6.

    Usa la familia conteo viva (head/tail/sort/uniq, cap. 6) + grep/wc/pipe
    ya enseñados. Coherente con CENSO-LISTA.md y con S2 (sin `cut`).
    """
    real = load_curriculum()
    # Si ya existe en el JSON real (tras S2), reutiliza el real.
    if real.quest("story.ch6.e1") is not None:
        return real
    q = Quest(
        id="story.ch6.e1",
        chapter=6,
        tint="grey",
        requires=("c.grep", "c.wc", "c.pipe", "c.head", "c.tail", "c.sort", "c.uniq"),
        title_key="story.ch6.e1.title",
        beat_key="story.ch6.e1.beat",
    )
    return Curriculum(version=real.version, concepts=real.concepts, quests=real.quests + (q,))


def _resolver(inc, path: str):
    return inc.room.fs.resolve(path, "/")


def test_sala_ch6_coloca_lista_y_cebo() -> None:
    """AC de O3: la sala-dato contiene registro/purgas al formato exacto + cebo."""
    cur = _curriculo_ch6()
    inc = generate(42, 6, curriculum=cur)
    assert inc.chapter == 6
    # Registro y purgas al formato CENSO-LISTA.md (cabecera + fila PR-0091)
    reg = _resolver(inc, REGISTRO_PATH)
    assert isinstance(reg, FileNode)
    assert reg.content == REGISTRO_CONTENT
    assert reg.content.startswith("residente_id|")
    assert "000291|VERA MONTEJO" in reg.content

    pur = _resolver(inc, PURGAS_PATH)
    assert isinstance(pur, FileNode)
    assert pur.content == PURGAS_CONTENT
    assert "PR-0091|EN BLANCO|000|--|ENSAYO" in pur.content

    # Cebo pipe-0: fichero trampa sin 000
    cebo = _resolver(inc, CEBO_PATH)
    assert isinstance(cebo, FileNode)
    assert cebo.content == CEBO_CONTENT
    assert "000" not in cebo.content or cebo.content.count("000") == 0


def test_sala_ch6_determinista_por_seed() -> None:
    """Misma seed ⇒ misma Incursion (la sala-dato no rompe determinismo)."""
    cur = _curriculo_ch6()
    assert generate(7, 6, curriculum=cur).to_dict() == generate(7, 6, curriculum=cur).to_dict()
    r = generate(7, 6, curriculum=cur)
    assert str(r.room.id).startswith("room-ch6-")


def test_sala_ch6_validable_canonica() -> None:
    """`generate` SIEMPRE valida antes de devolver (grep 000 | wc -l → 1)."""
    cur = _curriculo_ch6()
    inc = generate(0, 6, curriculum=cur)
    assert inc.room.canon.steps
    # La canónica es una tubería grep|wc
    assert inc.room.canon.steps[0].argv[0] == "grep"
    assert "ENSAYO" in inc.room.canon.steps[0].argv
    assert "wc" in inc.room.canon.steps[0].argv


def test_cebo_pipe0_da_cero_y_golden_da_uno() -> None:
    """El cebo `grep ENSAYO censo-borrador | wc -l` → 0, la golden → 1."""
    from core.generator import new_session

    cur = _curriculo_ch6()
    inc = generate(5, 6, curriculum=cur)
    shell = new_session(inc)
    # Cebo
    r0 = shell.execute(f"grep ENSAYO {CEBO_PATH} | wc -l")
    assert r0.stdout.strip() == "0"
    # Golden real
    r1 = shell.execute(f"grep ENSAYO {PURGAS_PATH} | wc -l")
    assert r1.stdout.strip() == "1"


def test_regresion_cap0_y_cap2_intactos_con_curriculo_ch6() -> None:
    """Regresión obligatoria: caps 0/2 intactos con el currículo aumentado."""
    cur = _curriculo_ch6()
    # cap 0
    a = generate(0, 0, curriculum=cur).to_dict()
    b = generate(0, 0, curriculum=cur).to_dict()
    assert a == b
    assert a["room"]["chapter"] == 0
    # cap 2
    c = generate(1, 2, curriculum=cur)
    assert c.chapter == 2
    assert c.room.id.startswith("room-ch2-")


@pytest.mark.skipif(not _HAS_CH6_E1, reason="quest story.ch6.e1 aún no en main — la pone S2 (Smough) esta tarde; skipif evita stale como en #16")
def test_ch6_con_curriculo_real_genera_sala_dato() -> None:
    """Con el currículo REAL (tras S2), `generate(1, 6)` SÍ produce sala-dato."""
    inc = generate(1, 6, curriculum=load_curriculum())
    assert inc.chapter == 6
    assert inc.room.id.startswith("room-ch6-")
    # La Lista está en el mundo
    pur = _resolver(inc, PURGAS_PATH)
    assert isinstance(pur, FileNode)
    assert "PR-0091" in pur.content


def test_generate_cap6_sin_quest_es_error_accionable() -> None:
    """Guarda de honestidad: sin quest del cap. 6 → GeneratorError."""
    real = load_curriculum()
    filtradas = tuple(q for q in real.quests if q.chapter != 6)
    sin_ch6 = Curriculum(version=real.version, concepts=real.concepts, quests=filtradas)
    with pytest.raises(GeneratorError):
        generate(1, 6, curriculum=sin_ch6)
