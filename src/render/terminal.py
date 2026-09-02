"""terminal — helpers puros del prompt y de las líneas de terminal (Seath, 02/09).

Puro Python, sin `pyxel`, sin `core` a nivel de import (solo type hints
opcionales). Testeable sin display.

Convención diegética: `cero@nodo:/ruta$` (avanza 🧭13; usuario = Cero
§2.2, nodo = room.host, ruta = shell.cwd real). El `usuario` es
parametrizable para tests, pero el default es `cero`.
"""

from __future__ import annotations

from typing import Any

from assets.font5x7 import Font5x7

from render.theme import TERM_COLS

_FONT = Font5x7()


def build_prompt(user: str, host: str, cwd: str) -> str:
    """Construye `usuario@nodo:/ruta$` con el cwd real.

    - `user`: por defecto `cero` (protagonista §2.2); el llamador puede
      pasar `usuario` genérico si quiere el literal del plan.
    - `host`: `room.host` (p. ej. `oficina-vecinal-muelle-norte`).
    - `cwd`: `shell.cwd` real (opción B → `/`). Si es largo, se trunca
      a `TERM_COLS` con `…` al final (el prompt nunca rompe el layout).

    Ejemplos:
        build_prompt("cero", "oficina-vecinal-muelle-norte", "/")
        → "cero@oficina-vecinal-muelle-norte:/$"
        build_prompt("cero", "nodo", "/srv/oficina-vecinal-muelle-norte")
        → "cero@nodo:/srv/oficina-vecinal-muelle-norte$"
    """
    raw = f"{user}@{host}:{cwd}$"
    # Truncado defensivo: el prompt no debe desbordar la terminal.
    if _FONT.text_size(raw)[0] > TERM_COLS * (Font5x7.GLYPH_W + Font5x7.TRACKING):
        # Corta por caracteres (no por píxeles) dejando hueco para "…".
        max_chars = TERM_COLS - 1
        if len(raw) > max_chars:
            raw = raw[: max_chars - 1] + "…"
    return raw


def wrap_lines(text: str, max_cols: int = TERM_COLS) -> list[str]:
    """Corta `text` en líneas de ≤ `max_cols` sin perder caracteres.

    No hace hyphenation: corta duro por columnas (terminal real).
    Líneas vacías se preservan como `""`.
    """
    if not text:
        return [""]
    out: list[str] = []
    for raw_line in text.split("\n"):
        if not raw_line:
            out.append("")
            continue
        while len(raw_line) > max_cols:
            out.append(raw_line[:max_cols])
            raw_line = raw_line[max_cols:]
        out.append(raw_line)
    return out


def terminal_lines(shell: Any, host: str, user: str = "cero") -> list[tuple[str, str]]:
    """Líneas a pintar en la terminal: (texto, color_key de SEMANTIC).

    Lee `shell.cwd`, `shell.history` y `shell.fs` solo para
    COMPONER texto; no muta nada.

    - Si el historial está vacío, pinta solo el prompt actual.
    - Si hay historial, pinta el último comando ejecutado (prompt +
      línea del comando) y su stdout/stderr (wrapped).
    """
    lines: list[tuple[str, str]] = []
    prompt = build_prompt(user, host, getattr(shell, "cwd", "/"))
    from render.theme import OUTPUT_COLOR, PROMPT_COLOR

    history = getattr(shell, "history", [])
    if not history:
        lines.append((prompt, PROMPT_COLOR))
        return lines

    # Última entrada del historial (la más relevante para v0).
    last = history[-1]
    # `history` en Shell es list[dict] con claves "line" y "result".
    line = str(last.get("line", "")) if isinstance(last, dict) else str(last)
    result = last.get("result", {}) if isinstance(last, dict) else {}
    stdout = str(result.get("stdout", "")) if isinstance(result, dict) else ""
    stderr = str(result.get("stderr", "")) if isinstance(result, dict) else ""

    # Prompt + comando en una línea (si cabe) o en dos.
    cmd_text = f"{prompt} {line}" if line else prompt
    # Si el comando desborda, lo partimos en dos líneas visuales.
    if len(cmd_text) > TERM_COLS:
        lines.append((prompt, PROMPT_COLOR))
        for w in wrap_lines(line, TERM_COLS - 2):
            lines.append((f"  {w}", OUTPUT_COLOR))
    else:
        lines.append((cmd_text, PROMPT_COLOR))

    # Salida del comando (stdout preferente, stderr si no hay stdout).
    output = stdout if stdout.strip() else stderr
    if output.strip():
        for w in wrap_lines(output.strip(), TERM_COLS):
            # Líneas de salida en color base; vacías se saltan.
            if w:
                lines.append((w, OUTPUT_COLOR))
    return lines
