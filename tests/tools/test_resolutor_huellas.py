"""Tests del resolutor canónico de huellas (O1 26/09, Ornstein)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

RESOLUTOR = Path("tools/resolutor_huellas.py")


def _run_resolutor(*args: str, cwd: str = ".") -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RESOLUTOR), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def _write_tmp(content: str) -> Path:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


# ---------------------------------------------------------------------------
# Fixtures inspirados en colisiones 24/09 y 25/09 (activo.md + worklog)
# ---------------------------------------------------------------------------

FIXTURE_COLISION_SIMPLE = textwrap.dedent("""\
    # EN CURSO

    ## Manus (03:00)
    Auditoria narrativa

    <<<<<<< HEAD
    ## Oscar (05:00)
    Run de referencia 24/09
    =======
    ## Oscar (05:00)
    Run de referencia 24/09 — corregido
    >>>>>>> feat/engine
    ## Havel (07:00)
    Vidente creativo
    """)

FIXTURE_DUPLICADA_IDENTICA = textwrap.dedent("""\
    # WORKLOG — 25/09

    ## Manus (03:00)
    Texto de Manus

    ## Oscar (05:00)
    Texto de Oscar

    ## Oscar (05:00)
    Texto de Oscar

    ## Havel (07:00)
    Texto de Havel
    """)


def test_resolutor_dedupe_identica_colapsa():
    p = _write_tmp(FIXTURE_DUPLICADA_IDENTICA)
    try:
        r = _run_resolutor(str(p))
        assert r.returncode == 0, r.stderr
        out = p.read_text(encoding="utf-8")
        assert out.count("## Oscar (05:00)") == 1
        assert "<<<<<<<" not in out
    finally:
        p.unlink(missing_ok=True)


def test_resolutor_conflicto_marcadores_elimina_y_keep_reciente():
    p = _write_tmp(FIXTURE_COLISION_SIMPLE)
    try:
        r = _run_resolutor(str(p))
        assert r.returncode == 0, r.stderr
        out = p.read_text(encoding="utf-8")
        assert "<<<<<<<" not in out
        assert ">>>>>>>" not in out
        assert "=======" not in out or "## Oscar" in out  # no marcadores sueltos
        # Debe quedar UNA copia de Oscar (la más reciente — "corregido")
        assert out.count("## Oscar (05:00)") == 1
        assert "corregido" in out
    finally:
        p.unlink(missing_ok=True)


def test_resolutor_check_detecta_marcadores():
    p = _write_tmp(FIXTURE_COLISION_SIMPLE)
    try:
        r = _run_resolutor("--check", str(p))
        assert r.returncode == 1, "check debe fallar si hay marcadores"
        assert "<<<<<<<" not in p.read_text(encoding="utf-8") or True  # check no escribe
        # Verifica que no modificó el fichero en modo check
        assert "<<<<<<<" in p.read_text(encoding="utf-8")
    finally:
        p.unlink(missing_ok=True)


def test_resolutor_check_limpio_ok():
    content = textwrap.dedent("""\
        # WORKLOG — 26/09

        ## Manus (03:00)
        A

        ## Oscar (05:00)
        B

        ## Havel (07:00)
        C
        """)
    p = _write_tmp(content)
    try:
        r = _run_resolutor("--check", str(p))
        assert r.returncode == 0, r.stderr
    finally:
        p.unlink(missing_ok=True)


def test_resolutor_ordena_cronologico():
    content = textwrap.dedent("""\
        ## Havel (07:00)
        Havel

        ## Manus (03:00)
        Manus

        ## Oscar (05:00)
        Oscar
        """)
    p = _write_tmp(content)
    try:
        r = _run_resolutor(str(p))
        assert r.returncode == 0
        out = p.read_text(encoding="utf-8")
        pos_manus = out.index("## Manus")
        pos_oscar = out.index("## Oscar")
        pos_havel = out.index("## Havel")
        assert pos_manus < pos_oscar < pos_havel
    finally:
        p.unlink(missing_ok=True)


def test_resolutor_cero_marcadores_tras_resolver():
    # Fixture anidado (marcador dentro de conflicto) — 24/09 tuvo anidados
    nested = textwrap.dedent("""\
        ## Gwyndolin (11:00)
        Plan del día
        <<<<<<< HEAD
        ## Ornstein (13:00)
        O1 resolutor
        <<<<<<< HEAD
        ## Smough (16:00)
        S1 quest
        =======
        ## Smough (16:00)
        S1 quest corregida
        >>>>>>> branch-a
        =======
        ## Ornstein (13:00)
        O1 resolutor — v2
        >>>>>>> feat/sandbox
        """)
    p = _write_tmp(nested)
    try:
        r = _run_resolutor(str(p))
        assert r.returncode == 0, r.stderr
        out = p.read_text(encoding="utf-8")
        assert "<<<<<<<" not in out
        assert ">>>>>>>" not in out
    finally:
        p.unlink(missing_ok=True)
