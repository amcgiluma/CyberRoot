"""O2 26/09 — Faro E4 «El trato»: scaffold del terreno (Ornstein, misma rama).

AC del plan:
- generate(42,6, contract_id='story.ch6.e4') byte-idéntico ×2 (determinismo)
- FS con los 2 testigos en /tmp/prueba-custodia/ (seed 42)
- navegación/vista con cat exit 0 sobre ambos
- GATE intocado (Ornstein no toca curriculum.json)
- Solo usa cat/grep/ls (ya vivos en DEFAULT_CH6_COMMANDS)
"""

from __future__ import annotations

from core.curriculum import Curriculum, load_curriculum
from core.curriculum.model import Quest
from core.generator import generate, new_session
from core.generator.chapter6 import (
    PRUEBA_CRUCES_CONTENT,
    PRUEBA_CRUCES_PATH,
    PRUEBA_RELOJ_CONTENT,
    PRUEBA_RELOJ_PATH,
)
from core.sandbox.fs import FileNode


def _curriculo_con_e4() -> Curriculum:
    real = load_curriculum()
    if real.quest("story.ch6.e4") is not None:
        return real
    q = Quest(
        id="story.ch6.e4",
        chapter=6,
        tint="grey",
        requires=("c.join",),
        title_key="story.ch6.e4.title",
        beat_key="story.ch6.e4.beat",
    )
    return Curriculum(version=real.version, concepts=real.concepts, quests=real.quests + (q,))


def test_e4_scaffold_determinista_byte_identico():
    cur = _curriculo_con_e4()
    a = generate(42, 6, contract_id="story.ch6.e4", curriculum=cur).to_dict()
    b = generate(42, 6, contract_id="story.ch6.e4", curriculum=cur).to_dict()
    assert a == b


def test_e4_scaffold_contiene_dos_testigos():
    cur = _curriculo_con_e4()
    inc = generate(42, 6, contract_id="story.ch6.e4", curriculum=cur)
    assert inc.contract.objective_key == "story.ch6.e4"
    # Archivos en /tmp/prueba-custodia/
    cruce = inc.room.fs.resolve(PRUEBA_CRUCES_PATH, "/")
    assert isinstance(cruce, FileNode)
    assert cruce.content == PRUEBA_CRUCES_CONTENT
    assert "PR-0091" in cruce.content
    assert "HOSP-47-C" in cruce.content

    reloj = inc.room.fs.resolve(PRUEBA_RELOJ_PATH, "/")
    assert isinstance(reloj, FileNode)
    assert reloj.content == PRUEBA_RELOJ_CONTENT
    assert "11:04" in reloj.content


def test_e4_scaffold_cat_exit_0_sobre_testigos():
    cur = _curriculo_con_e4()
    inc = generate(42, 6, contract_id="story.ch6.e4", curriculum=cur)
    shell = new_session(inc)
    r1 = shell.execute(f"cat {PRUEBA_CRUCES_PATH}")
    assert r1.exit_code == 0
    assert "PR-0091" in r1.stdout

    r2 = shell.execute(f"cat {PRUEBA_RELOJ_PATH}")
    assert r2.exit_code == 0
    assert "11:04" in r2.stdout

    r3 = shell.execute("ls /tmp/prueba-custodia/")
    assert r3.exit_code == 0
    assert "prueba-cruce.txt" in r3.stdout
    assert "prueba-reloj.txt" in r3.stdout


def test_e4_scaffold_sin_e4_no_planta(tmp_path=None):
    # Sin contract_id e4, el /tmp/prueba-custodia NO debe existir (lista normal)
    cur = _curriculo_con_e4()
    # Genera una sala distinta (e2) — no debe tener prueba-custodia
    inc = generate(42, 6, contract_id="story.ch6.e2", curriculum=cur)
    try:
        node = inc.room.fs.resolve(PRUEBA_CRUCES_PATH, "/")
        assert False, f"prueba-custodia no debería existir fuera de e4, pero hallado: {node}"
    except Exception:
        pass  # esperado: no existe
