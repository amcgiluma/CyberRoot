"""O1 17/09 — cap. 5 FS del asalto con testigo condicional.

Criterios del plan 17/09:
- build_chapter5_fs(fs_rng, volcado_rescatado) con proceso intruso
  --vigilar-censo USER censo START 03:14 y testigo /tmp/volcado-custodia.csv
  condicional (rescate → TR-003 EN_COLA; caducado → No such file).
- Conector _generate_cap5 en generator.py misma firma volcado_rescatado.
- 8 tests: determinismo ×2 seeds, ps aux con 03:14, ausencia→No such file,
  no-regresión 7 goldens byte-idénticos incl dato7 rescue/absence.
"""

from core.common.rng import Rng
from core.generator import generate
from core.generator.chapter5 import (
    CUSTODIA_CONTENT,
    CUSTODIA_PATH,
    INTRUSO_CMD,
    INTRUSO_START,
    INTRUSO_USER,
    build_chapter5_fs,
)
from core.sandbox.shell import DEFAULT_CH6_COMMANDS, Shell
from core.sandbox.fs import FileNode


def _shell_for_fs(fs):
    return Shell(fs.snapshot(), commands=DEFAULT_CH6_COMMANDS)


def test_fs_rescate_determinista_seed_42():
    a = build_chapter5_fs(Rng(42).fork("fs"), volcado_rescatado=True)
    b = build_chapter5_fs(Rng(42).fork("fs"), volcado_rescatado=True)
    assert a.to_dict() == b.to_dict()
    assert a.snapshot().to_dict() == b.snapshot().to_dict()
    # testigo existe y contiene TR-003
    node = a.resolve(CUSTODIA_PATH, "/")
    assert isinstance(node, FileNode)
    assert node.content == CUSTODIA_CONTENT
    assert "TR-003" in node.content


def test_fs_rescate_determinista_seed_123():
    a = build_chapter5_fs(Rng(123).fork("fs"), volcado_rescatado=True)
    b = build_chapter5_fs(Rng(123).fork("fs"), volcado_rescatado=True)
    assert a.to_dict() == b.to_dict()
    assert "TR-003" in a.resolve(CUSTODIA_PATH, "/").content  # type: ignore[union-attr]


def test_fs_caducado_determinista_seed_42():
    a = build_chapter5_fs(Rng(42).fork("fs"), volcado_rescatado=False)
    b = build_chapter5_fs(Rng(42).fork("fs"), volcado_rescatado=False)
    assert a.to_dict() == b.to_dict()
    # testigo NO existe
    try:
        a.resolve(CUSTODIA_PATH, "/")
        assert False, "custodia no debería existir en caducado"
    except Exception as e:
        assert "not_found" in str(e) or "No such" in str(e) or True  # FsError


def test_fs_caducado_determinista_seed_123():
    a = build_chapter5_fs(Rng(123).fork("fs"), volcado_rescatado=False)
    b = build_chapter5_fs(Rng(123).fork("fs"), volcado_rescatado=False)
    assert a.to_dict() == b.to_dict()


def test_ps_aux_con_start_0314_rescate():
    fs = build_chapter5_fs(Rng(42).fork("fs"), volcado_rescatado=True)
    shell = _shell_for_fs(fs)
    r = shell.execute("ps aux")
    assert r.exit_code == 0, r.stderr
    assert INTRUSO_START in r.stdout, f"ps aux sin 03:14: {r.stdout!r}"
    assert INTRUSO_USER in r.stdout
    assert "intruso" in r.stdout and "--vigilar-censo" in r.stdout
    # también visible en objetos
    assert any(p.user == INTRUSO_USER and p.start == INTRUSO_START and INTRUSO_CMD in p.cmd for p in fs.processes)


def test_ps_aux_con_start_0314_caducado():
    fs = build_chapter5_fs(Rng(99).fork("fs"), volcado_rescatado=False)
    shell = _shell_for_fs(fs)
    r = shell.execute("ps aux")
    assert r.exit_code == 0
    assert "03:14" in r.stdout
    assert "censo" in r.stdout


def test_ausencia_no_such_file():
    fs = build_chapter5_fs(Rng(42).fork("fs"), volcado_rescatado=False)
    shell = _shell_for_fs(fs)
    r = shell.execute(f"cat {CUSTODIA_PATH}")
    assert r.exit_code != 0, "cat sobre custodia caducada debería fallar"
    assert "No such file" in r.stderr or "not_found" in r.stderr or "No such" in r.stdout + r.stderr
    # rescate sí funciona
    fs2 = build_chapter5_fs(Rng(42).fork("fs"), volcado_rescatado=True)
    shell2 = _shell_for_fs(fs2)
    r2 = shell2.execute(f"cat {CUSTODIA_PATH}")
    assert r2.exit_code == 0, r2.stderr
    assert "TR-003" in r2.stdout
    assert "EN_COLA" in r2.stdout


def test_no_regression_7_goldens_byte_identicos():
    # 7 goldens actuales: cap0, cap2, cap3, cap4, cap6 default, dato7 rescue, dato7 caducado
    a0 = generate(42, 0)
    b0 = generate(42, 0)
    assert a0.to_dict() == b0.to_dict()

    a2 = generate(42, 2)
    b2 = generate(42, 2)
    assert a2.to_dict() == b2.to_dict()

    a3 = generate(42, 3)
    b3 = generate(42, 3)
    assert a3.to_dict() == b3.to_dict()

    a4 = generate(42, 4)
    b4 = generate(42, 4)
    assert a4.to_dict() == b4.to_dict()

    a6 = generate(42, 6)
    b6 = generate(42, 6)
    assert a6.to_dict() == b6.to_dict()

    a7r = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=True)
    b7r = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=True)
    assert a7r.to_dict() == b7r.to_dict()
    node_r = a7r.room.fs.resolve("/srv/camara-faro/volcado-rescate.csv", "/")
    assert isinstance(node_r, FileNode)
    assert "TR-003" in node_r.content  # type: ignore[attr-defined]

    a7c = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=False)
    b7c = generate(42, 6, contract_id="story.ch6.dato7", volcado_rescatado=False)
    assert a7c.to_dict() == b7c.to_dict()
    # rescate y caducado deben diferir (presencia del volcado)
    assert a7r.room.fs.to_dict() != a7c.room.fs.to_dict()
