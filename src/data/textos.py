"""textos.py — acceso a `src/data/textos.json` (T1, 01/09, Seath).

Es el resolvedor mínimo del primer paquete de TEXTOS del juego (🧭12):
`line_key` + `args` → cadena con placeholders poblados. Voz del Auditor y
claves del cap. 1 integradas desde `backlog/historia/`. Pensado para que el
render (o el test) resuelva claves contra `data/` — ARCHITECTURE §3: «core
carga y devuelve claves de texto; el render las resuelve».

Cero lógica de juego y cero dependencias del core a propósito: un simple
diccionario cargado desde JSON + sustitución de `{placeholder}`. Si mañana
este resolvedor se usa en producción, se acuerda su traslado con render
(que llega con su primera tarea, 'día verde'), sin tocar core hoy.

Solo stdlib; sin I/O de red; sin globals mutables.
"""

from __future__ import annotations

import json
from pathlib import Path

#: Ruta canónica de los textos (desde la raíz del repo).
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "textos.json"


class TextResolutionError(KeyError):
    """Clave de texto ausente o con placeholders sin poblar (fallo accionable)."""


def load_textos(path: Path | str | None = None) -> dict[str, str]:
    """Carga `textos.json` y devuelve el diccionario `texts` (clave → plantilla).

    `path=None` usa `src/data/textos.json`. Levanta `TextResolutionError` si el
    fichero falta, no es JSON, le falta `version`/`texts` o `texts` no es un
    mapa de claves → strings (respeta la filosofía 'JSON plano' de `data/`).
    El `version` se acepta por ahora sin reventar (v1); el esquema fino lo
    valida en negativo el test.
    """
    p = Path(path) if path is not None else DATA_PATH
    try:
        raw = p.read_text(encoding="utf-8")
    except OSError as e:
        raise TextResolutionError(f"no se pudo leer {p}: {e}") from e
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        raise TextResolutionError(f"{p} no es JSON válido: {e}") from e
    if not isinstance(doc, dict) or "texts" not in doc:
        raise TextResolutionError(f"{p}: falta el objeto 'texts'")
    texts = doc["texts"]
    if not isinstance(texts, dict):
        raise TextResolutionError(f"{p}: 'texts' debe ser un objeto")
    out: dict[str, str] = {}
    for k, v in texts.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise TextResolutionError(
                f"{p}: 'texts' debe mapear claves str a plantillas str "
                "(encontrado {k!r}: {v!r})"
            )
        out[k] = v
    return out


def resolve(
    line_key: str,
    args: dict[str, str | int] | None = None,
    textos: dict[str, str] | None = None,
) -> str:
    """Resuelve `line_key` contra `textos` (o contra `load_textos()` por defecto).

    `args` puebla los `{placeholder}` de la plantilla (p. ej. `{command}`,
    `{amount}` para la línea del Auditor). Levanta `TextResolutionError` si la
    clave no existe o si una plantilla pide un placeholder sin arg (fallo
    accionable: mejor romper que mostrar un hueco `{...}`).
    """
    catalog = textos if textos is not None else load_textos()
    if line_key not in catalog:
        raise TextResolutionError(
            f"clave de texto ausente: {line_key!r} — falta en textos.json"
        )
    template = catalog[line_key]
    provided = args if args else {}
    missing = [p for p in _placeholders(template) if p not in provided]
    if missing:
        raise TextResolutionError(
            f"clave {line_key!r}: faltan placeholders {{{', '.join(missing)}}} "
            f"en args ({sorted(provided)})"
        )
    return template.format(**provided)


def _placeholders(template: str) -> list[str]:
    """Nombres de `{nombre}` en la plantilla, en orden de aparición."""
    names: list[str] = []
    for part in template.split("{"):
        if "}" in part:
            names.append(part.split("}", 1)[0])
    return names


__all__ = [
    "DATA_PATH",
    "TextResolutionError",
    "load_textos",
    "resolve",
]