"""O1+O2 (31/08, Ornstein) — flujo de ENCARGO del cap. 2 + post-mortem conectado.

Testea el ciclo completo en `core/engine/session.py`: listar → abrir (validando
prereqs al ABRIR, 🧭8=(b)) → generar la sala del contrato → jugar la golden →
cerrar adjuntando `build_postmortem`. Incluye la regresión de `generate(seed,0)`
y del determinismo del cap. 2 (la sala es reproducible por seed).

La golden del cap. 2:
    `grep 11:04 centralita/turnos/turno.log | wc -l` → `2`
se juega DENTRO del flujo (abrir `story.ch2.e1` y ejecutarla en la sesión).
"""

from __future__ import annotations

from core.curriculum import load_curriculum
from core.engine import (
    abrir_encargo,
    cerrar_encargo,
    listar_encargos,
    rechazo_accionable,
)
from core.generator import generate, new_session

CUR = load_curriculum()

#: Conocimiento del cap. 0 (sin grep/wc/pipe): NO abre e1.
KN_CAP0 = ("c.ls", "c.cd", "c.cat", "c.cp")
#: Conocimiento que SÍ abre `story.ch2.e1` (grep + wc + pipe).
KN_CH2 = ("c.grep", "c.wc", "c.pipe")
#: Conocimiento que además abre e5 (añade c.cp) — el cierre del capítulo.
KN_CH2_CP = KN_CH2 + ("c.cp",)


def test_generate_cap0_regresion_determinista() -> None:
    """Regresión (nota Artorias sobre model.py): `generate(seed,0)` intacto."""
    for seed in (0, 7, 42):
        assert generate(seed, 0).to_dict() == generate(seed, 0).to_dict()


def test_generate_cap2_determinista_por_seed() -> None:
    """La sala del cap. 2 es reproducible: misma seed ⇒ misma Incursion."""
    a = generate(9, 2, contract_id="story.ch2.e1").to_dict()
    b = generate(9, 2, contract_id="story.ch2.e1").to_dict()
    assert a == b


def test_generate_cap2_contrata_el_encargo() -> None:
    """generate(seed,2,contract_id=...) produce la sala del encargo concreto."""
    inc = generate(7, 2, contract_id="story.ch2.e1")
    assert inc.chapter == 2
    assert inc.room.objective.story_key == "story.ch2.e1"
    assert inc.contract.objective_key == "story.ch2.e1"
    assert inc.contract.karma_hint == "azul"  # tint blue → azul


def test_generate_no_evalua_prereqs_al_generar() -> None:
    """🧭8=(b): generate() NO se entera de prereqs; abre quien decide el flujo."""
    # Sin conocimiento de nada, generate() produce la sala igualmente.
    inc = generate(7, 2, contract_id="story.ch2.e1")
    assert inc.room.objective.story_key == "story.ch2.e1"


def test_generate_cap2_golden_playable_en_la_sesion() -> None:
    """La línea golden del cap. 2 se juega dentro de la sesión de la sala."""
    inc = generate(7, 2, contract_id="story.ch2.e1")
    s = new_session(inc)
    first = s.execute("cd /srv/oficina-vecinal-muelle-norte")
    assert first.exit_code == 0
    res = s.execute("grep 11:04 centralita/turnos/turno.log | wc -l")
    assert res.exit_code == 0, res.stderr
    assert res.stdout == "2\n"


def test_listar_encargos_cap2_orden_determinista() -> None:
    """listar_encargos ordena los 5 del cap. 2 por id (vitrina del Hub)."""
    ids = [q["id"] for q in listar_encargos(CUR, 2)]
    assert ids == [
        "story.ch2.e1",
        "story.ch2.e2",
        "story.ch2.e3",
        "story.ch2.e4",
        "story.ch2.e5",
    ]
    assert all(q["karma_hint"] in ("azul", "rojo", "gris") for q in listar_encargos(CUR, 2))


def test_listar_encargos_abribles_con_knowledge() -> None:
    """Con knowledge, cada encargo marca `abrible` y los faltantes."""
    with_kn = listar_encargos(CUR, 2, knowledge=KN_CH2)
    by_id = {q["id"]: q for q in with_kn}
    assert by_id["story.ch2.e1"]["abrible"] is True
    assert by_id["story.ch2.e1"]["falta"] == []
    # e5 además exige c.cp (cap. 0) → no abrible con solo grep/wc/pipe.
    assert by_id["story.ch2.e5"]["abrible"] is False
    assert "c.cp" in by_id["story.ch2.e5"]["falta"]


def test_rechazo_accionable_devuelve_lo_que_falta() -> None:
    """El rechazo es accionable: lista los conceptos que faltan, no un «no»."""
    r = rechazo_accionable(CUR, "story.ch2.e1", KN_CAP0)
    assert r["abrible"] is False
    assert r["missing"] == ["c.grep", "c.pipe", "c.wc"]


def test_abrir_encargo_rechazado_sin_prereqs_no_genera() -> None:
    """Sin prereqs, abrir rechaza con `missing` y NO genera sala."""
    res = abrir_encargo(CUR, "story.ch2.e1", KN_CAP0, run_seed=7)
    assert res["abrible"] is False
    assert res["missing"] == ["c.grep", "c.pipe", "c.wc"]
    assert "session" not in res


def test_flujo_completo_cap2_jugar_golden_y_cerrar() -> None:
    """listar→abrir(e1)→jugar golden→cerrar(completado) adjunta post-mortem."""
    assert any(q["id"] == "story.ch2.e1" for q in listar_encargos(CUR, 2))
    res = abrir_encargo(CUR, "story.ch2.e1", KN_CH2, run_seed=7)
    assert res["abrible"] is True
    s = res["session"]
    assert s.seed == "story.ch2.e1:7"  # seed determinista quest+run

    assert s.ejecutar("cd /srv/oficina-vecinal-muelle-norte").exit_code == 0
    golden = s.ejecutar("grep 11:04 centralita/turnos/turno.log | wc -l")
    assert golden.stdout == "2\n"

    cierre = cerrar_encargo(s, modo="completado")
    assert cierre["quest_id"] == "story.ch2.e1"
    assert cierre["modo"] == "completado"
    pm = cierre["postmortem"]
    assert pm["total_noise"] == 3  # grep(2)+wc(1); cd(0)
    assert pm["dentro_presupuesto"] is True
    assert pm["factura"]["grep"] >= 1
    assert pm["auditor"]["args"]["command"]  # línea del Auditor con comando concreto


def test_cerrar_expulsion_adjunta_mismo_postmortem() -> None:
    """Al cerrar por expulsión, el post-mortem se adjunta igual (modo distinto)."""
    res = abrir_encargo(CUR, "story.ch2.e1", KN_CH2, run_seed=7)
    s = res["session"]
    s.ejecutar("cd /srv/oficina-vecinal-muelle-norte")
    s.ejecutar("grep 11:04 centralita/turnos/turno.log | wc -l")
    c = cerrar_encargo(s, modo="expulsión")
    assert c["modo"] == "expulsión"
    assert c["postmortem"]["dentro_presupuesto"] is True


def test_abrir_e5_con_cp_del_cap0() -> None:
    """El cierre del capítulo (e5) abre con c.cp: prereq de capítulo anterior."""
    res = abrir_encargo(CUR, "story.ch2.e5", KN_CH2_CP, run_seed=7)
    assert res["abrible"] is True, res
    assert res["session"].chapter == 2


def test_generate_cap0_variantes_determinismo() -> None:
    """Regresión de variantes del cap. 0: canonical y practice reproducibles."""
    for v in ("canonical", "practice"):
        assert generate(9, 0, variant=v).to_dict() == generate(9, 0, variant=v).to_dict()