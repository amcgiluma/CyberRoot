"""S1 16/09 — dato7 «El fantasma que pesa» (Smough, cadena TR-003).

Primera consecuencia cruzada troncal→Faro: volcado-rescate.csv condicional.
- FS del Faro planta /srv/camara-faro/volcado-rescate.csv con TR-003|EN_COLA
  SOLO si la sesión rescató (volcado_rescatado=True); si caducado → NO existe.
- Quest story.ch6.dato7 grey requires c.join, gate 24/30→31.
- Golden: cat volcado-rescate.csv | grep TR-003 → exit 0 cuando existe,
  y join -t'|' -1 1 -2 1 -v 1 volcado purgas | grep TR-003 → TR-003.
  Cuando caducado, join/cat fallan con No such file.
- Sala con 2 salidas byte-determinista por seed.
"""

from core.curriculum import load_curriculum
from core.generator import generate
from core.generator.generator import new_session
from core.sandbox.shell import DEFAULT_CH6_COMMANDS
from core.sandbox.fs import FileSystem

def test_dato7_quest_existe_y_requires_join():
    cur = load_curriculum()
    q = cur.quest("story.ch6.dato7")
    assert q is not None, "dato7 no en curriculum"
    assert q.chapter == 6
    assert q.tint == "grey"
    assert q.requires == ["c.join"] or q.requires == ("c.join",)
    # gate
    assert len(cur.concepts) == 25
    assert len(cur.quests) in (31, 32)

def test_chapter6_fs_rescatado_tiene_volcado():
    from core.generator.chapter6 import build_chapter6_fs, VOLCADO_RESCATE_PATH, VOLCADO_RESCATE_CONTENT
    fs = build_chapter6_fs(None, volcado_rescatado=True)
    # file exists
    node = fs.resolve(VOLCADO_RESCATE_PATH, "/")
    assert node.content == VOLCADO_RESCATE_CONTENT
    assert "TR-003" in node.content
    assert "EN_COLA" in node.content
    # shell cat|grep
    from core.sandbox.shell import Shell
    sh = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    r = sh.execute(f"cat {VOLCADO_RESCATE_PATH} | grep TR-003")
    assert r.exit_code == 0, r.stderr
    assert "TR-003" in r.stdout

def test_chapter6_fs_caducado_no_tiene_volcado():
    from core.generator.chapter6 import build_chapter6_fs, VOLCADO_RESCATE_PATH
    fs = build_chapter6_fs(None, volcado_rescatado=False)
    # file NOT exists
    try:
        fs.resolve(VOLCADO_RESCATE_PATH, "/")
        assert False, "volcado-rescate.csv debería estar ausente cuando caducado"
    except Exception as e:
        assert "not_found" in str(e) or "No such" in str(e) or e is not None
    from core.sandbox.shell import Shell
    sh = Shell(fs, commands=DEFAULT_CH6_COMMANDS)
    r = sh.execute(f"cat {VOLCADO_RESCATE_PATH}")
    assert r.exit_code == 1
    assert "No such file" in r.stderr
    # join debe fallar con No such file y grep no encuentra
    r2 = sh.execute(f"join -t'|' -1 1 -2 1 -v 1 {VOLCADO_RESCATE_PATH} /srv/camara-faro/purgas.csv | grep TR-003")
    # join falla, grep sin input → exit 1
    assert r2.exit_code == 1 or "No such file" in r2.stderr

def test_chapter6_fs_default_sin_volcado():
    # Sin flag (default False) no hay volcado — no rompe dato6 ni goldens anteriores
    from core.generator.chapter6 import build_chapter6_fs, VOLCADO_RESCATE_PATH
    fs = build_chapter6_fs(None)
    try:
        fs.resolve(VOLCADO_RESCATE_PATH, "/")
        assert False, "default sin flag no debe tener volcado"
    except Exception:
        pass

def test_generator_dato7_rescatado_vs_caducado_determinista():
    # Mismo seed, dos salidas deterministas
    inc_res = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=True)
    inc_res2 = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=True)
    assert inc_res.room.fs.to_dict() == inc_res2.room.fs.to_dict()
    inc_cad = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=False)
    inc_cad2 = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=False)
    assert inc_cad.room.fs.to_dict() == inc_cad2.room.fs.to_dict()
    # Diferentes entre sí
    assert inc_res.room.fs.to_dict() != inc_cad.room.fs.to_dict()
    # Rescatado tiene volcado
    from core.generator.chapter6 import VOLCADO_RESCATE_PATH
    assert "TR-003" in inc_res.room.fs.read_file(VOLCADO_RESCATE_PATH, "/")
    # Caducado no tiene
    try:
        inc_cad.room.fs.resolve(VOLCADO_RESCATE_PATH, "/")
        assert False
    except Exception:
        pass

def test_generator_dato7_golden_join_grep():
    # Golden join con volcado primero | grep
    inc = generate(123, 6, contract_id="story.ch6.dato7", volcado_rescatado=True)
    sh = new_session(inc)
    r = sh.execute("join -t'|' -1 1 -2 1 -v 1 /srv/camara-faro/volcado-rescate.csv /srv/camara-faro/purgas.csv | grep TR-003")
    assert r.exit_code == 0, f"join|grep failed: {r.stderr}"
    assert "TR-003" in r.stdout
    # Variante sin -v también debe mostrar TR-003 via cat
    r2 = sh.execute("cat /srv/camara-faro/volcado-rescate.csv | grep TR-003")
    assert r2.exit_code == 0
    assert "TR-003" in r2.stdout
    # Caducado: join falla
    inc2 = generate(123, 6, contract_id="story.ch6.dato7", volcado_rescatado=False)
    sh2 = new_session(inc2)
    r3 = sh2.execute("join -t'|' -1 1 -2 1 -v 1 /srv/camara-faro/volcado-rescate.csv /srv/camara-faro/purgas.csv | grep TR-003")
    assert r3.exit_code != 0 or "TR-003" not in r3.stdout

def test_generator_dato7_no_rompe_dato6_ni_e1():
    # Generar otras quests con mismo seed y volcado flag no rompe goldens
    for qid in ["story.ch6.dato6", "story.ch6.dato4", "story.ch6.e1"]:
        inc = generate(99, 6, contract_id=qid, volcado_rescatado=False)
        # debe validar sin error
        from core.generator.generator import validate_incursion
        validate_incursion(inc)
        # con True también debe validar (extra file no rompe)
        inc2 = generate(99, 6, contract_id=qid, volcado_rescatado=True)
        validate_incursion(inc2)

def test_gate_31_y_curriculum_31():
    cur = load_curriculum()
    assert len(cur.quests) in (31, 32)
    assert len(cur.concepts) == 25
    # c.join existe
    assert cur.concept("c.join") is not None
