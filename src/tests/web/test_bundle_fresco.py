"""test_bundle_fresco.py — Guardián de la puerta (T1, 04/09, Seath).

La puerta pública (web/bundle/core.json) es un artefacto GENERADO que
incrustra el core real para Pyodide. Si el core cambia y el bundle no se
regenera, la puerta miente en silencio: el jugador en el navegador ejecuta
código viejo.

Este test es el guardián: reconstruye el manifest EN MEMORIA desde
`src/core/` + `src/data/curriculum.json` actuales (la misma lógica que
`tools/web/build_bundle.py:collect`) y lo compara con
`web/bundle/core.json` commiteado. Divergencia → rojo con mensaje
accionable ``bundle stale: regenera (`python tools/web/build_bundle.py`)
y commitea``.

Solo añade tests; NO toca `web/` ni `src/core/` (rutas disjuntas con
Smough/Ornstein). Corre en el smoke del conjunto.

Nota de integración para Gwyn (23:00): si el `cut` de Smough entra antes
de tu ensayo, ESTE TEST GRITARÁ — y está bien: es el guardián
funcionando. Arreglo: regenerar el bundle y commitear en el ensayo.
"""

from __future__ import annotations

import json
from pathlib import Path

# Raíz del repo desde este fichero: src/tests/web/test_bundle_fresco.py → parents[3] == repo
REPO = Path(__file__).resolve().parents[3]
CORE_SRC = REPO / "src" / "core"
DATA_DIR = REPO / "src" / "data"
DATA_SRC = DATA_DIR / "curriculum.json"
TEXTOS_SRC = DATA_DIR / "textos.json"
BUNDLE = REPO / "web" / "bundle" / "core.json"

VIRT_LIB = "/lib"
VIRT_CORE = f"{VIRT_LIB}/core"
VIRT_DATA = f"{VIRT_LIB}/data"

STALE_MSG = "bundle stale: regenera (`python tools/web/build_bundle.py`) y commitea"


def _collect_expected() -> dict[str, str]:
    """Replica `tools/web/build_bundle.py:collect` — ruta_virtual → contenido.

    Lee TODO `src/core/**/*.py` + `src/data/**/*.py` (ordenado, sin __pycache__)
    + curriculum.json + textos.json. Mantiene el contrato virtual
    `/lib/core/...` y `/lib/data/...`.
    """
    out: dict[str, str] = {}
    for py in sorted(CORE_SRC.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        rel = py.relative_to(CORE_SRC)
        virtual = f"{VIRT_CORE}/{rel.as_posix()}"
        out[virtual] = py.read_text(encoding="utf-8")
    for py in sorted(DATA_DIR.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        rel = py.relative_to(DATA_DIR.parent)  # data/textos.py → data/textos.py
        virtual = f"{VIRT_LIB}/{rel.as_posix()}"
        out[virtual] = py.read_text(encoding="utf-8")
    if not DATA_SRC.exists():
        raise AssertionError(f"falta {DATA_SRC}: no se puede verificar el bundle")
    out[f"{VIRT_DATA}/curriculum.json"] = DATA_SRC.read_text(encoding="utf-8")
    if TEXTOS_SRC.exists():
        out[f"{VIRT_DATA}/textos.json"] = TEXTOS_SRC.read_text(encoding="utf-8")
    return out


def _load_bundled() -> dict[str, str]:
    if not BUNDLE.exists():
        raise AssertionError(f"{STALE_MSG} — falta {BUNDLE.relative_to(REPO)}")
    try:
        data = json.loads(BUNDLE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise AssertionError(f"{STALE_MSG} — {BUNDLE.relative_to(REPO)} no es JSON válido: {e}") from e
    if not isinstance(data, dict):
        raise AssertionError(f"{STALE_MSG} — manifest no es objeto JSON")
    return {str(k): str(v) for k, v in data.items()}


def test_bundle_fresco_contra_core_actual() -> None:
    """El manifest commiteado coincide con la reconstrucción desde `src/core/`."""
    expected = _collect_expected()
    bundled = _load_bundled()

    if bundled == expected:
        return

    # Diagnóstico accionable: qué difiere
    exp_keys = set(expected)
    bun_keys = set(bundled)
    missing = sorted(exp_keys - bun_keys)
    extra = sorted(bun_keys - exp_keys)
    changed = sorted(k for k in exp_keys & bun_keys if expected[k] != bundled[k])

    details: list[str] = []
    if missing:
        details.append(f"faltan en bundle: {missing[:5]}{' …' if len(missing) > 5 else ''}")
    if extra:
        details.append(f"sobran en bundle: {extra[:5]}{' …' if len(extra) > 5 else ''}")
    if changed:
        details.append(f"contenido distinto: {changed[:5]}{' …' if len(changed) > 5 else ''}")
        # Muestra un diff mínimo del primer fichero cambiado (primeras 3 líneas)
        first = changed[0]
        exp_lines = expected[first].splitlines()[:3]
        bun_lines = bundled[first].splitlines()[:3]
        details.append(f"  ej {first}: esperado empieza {exp_lines!r} vs bundle {bun_lines!r}")

    detail_str = "; ".join(details) if details else "manifests distintos"
    raise AssertionError(f"{STALE_MSG} — {detail_str}")


def test_bundle_es_json_valido_con_40_ficheros_minimo() -> None:
    """El bundle existe, es JSON y trae el core completo (≥40 ficheros)."""
    bundled = _load_bundled()
    assert len(bundled) >= 42, f"{STALE_MSG} — bundle con {len(bundled)} ficheros, esperaba ≥42"
    # Contrato virtual mínimo
    assert any(k.startswith("/lib/core/") for k in bundled), "bundle sin /lib/core/"
    assert "/lib/data/curriculum.json" in bundled, "bundle sin curriculum.json"
    assert "/lib/data/textos.json" in bundled, "bundle sin textos.json"
    assert "/lib/data/textos.py" in bundled, "bundle sin data/textos.py"
