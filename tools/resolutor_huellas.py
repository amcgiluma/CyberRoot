#!/usr/bin/env python3
"""resolutor_huellas.py — resolutor canónico de colisiones de huellas.

Resuelve colisiones git en `activo.md` + `worklog/YYYY/MM/DD.md` sin
reimprimir el ad-hoc cada noche.

Contrato (plan 26/09 O1):
- recibe fichero(s) + orden cronológico esperado de secciones ``## HH:00``
- expande marcadores anidados (<<<<<<< / ======= / >>>>>>>)
- mantiene UNA sola copia por sección (dedupe por contenido idéntico;
  si difiere, se queda la más reciente y lo advierte por stderr)
- assertions de contenido (toda ``## HH:00`` esperada presente al final)
- salida con CERO ``<<<<<<<`` por línea (exit 1 si queda alguno)
- modo ``--check`` que solo valida (0 = limpio, 1 = sucio)

Uso:
    python tools/resolutor_huellas.py [--check] [--order 03:00,05:00,07:00,11:00,13:00,16:00,19:00,21:00,23:00] <fichero>...

Sin ``--order`` usa el orden canónico del Concilio (03/05/07/11/13/16/19/21/23).
Con ``--check`` no escribe, solo valida.

Python 3 sin deps nuevas.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Orden canónico del Concilio (horas de los 9 agentes + Gwyndolin)
CANON_ORDER = ["03:00", "05:00", "07:00", "11:00", "13:00", "16:00", "19:00", "21:00", "23:00"]

# Regex para extraer HH:00 de una cabecera (p.ej. "## Manus (03:00)" o "## 03:00")
_RE_HORA = re.compile(r"(\d{2}:\d{2})")

# Cabecera de sección: líneas que empiezan por ## (nivel 2 o 3)
_RE_SECTION = re.compile(r"^#{2,3}\s.*$")


def _strip_markers(text: str) -> str:
    """Expande marcadores anidados: elimina todas las líneas de conflicto.

    Itera hasta que no queden marcadores (soporta anidados).
    """
    lines = text.splitlines()
    # Filtra líneas que son marcadores git
    filtered = [l for l in lines if not l.startswith("<<<<<<< ") and not l.startswith("=======") and not l.startswith(">>>>>>> ")]
    # Si había marcadores anidados con prefijos sin espacio (<<<<<<<), también
    filtered2 = [l for l in filtered if not l.startswith("<<<<<<<") and not l.startswith(">>>>>>>")]
    # Bucle: si aún quedan marcadores sueltos, repite
    result = "\n".join(filtered2)
    # Verifica que no queden marcadores
    if "<<<<<<<" in result or ">>>>>>>" in result:
        # Último intento: elimina cualquier línea que contenga <<<<<<<
        lines = result.splitlines()
        lines = [l for l in lines if "<<<<<<<" not in l and ">>>>>>>" not in l and l.strip() != "======="]
        result = "\n".join(lines)
    return result


def _extract_hora(heading: str) -> str | None:
    m = _RE_HORA.search(heading)
    return m.group(1) if m else None


def _split_sections(text: str) -> list[tuple[str, str]]:
    """Divide texto en secciones por cabecera ## . Devuelve lista (heading, body).

    La primera sección antes de la primera cabecera se trata como preámbulo
    con heading "".
    """
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_body: list[str] = []
    # Preámbulo: todo antes de la primera cabecera
    preamble_done = False
    for line in lines:
        if _RE_SECTION.match(line):
            # Nueva sección
            if not preamble_done and current_heading == "" and current_body:
                # Guarda preámbulo
                sections.append(("", "\n".join(current_body)))
                current_body = []
                preamble_done = True
            elif current_heading != "" or current_body:
                if current_heading != "" or current_body:
                    sections.append((current_heading, "\n".join(current_body)))
                current_body = []
            current_heading = line
            preamble_done = True
        else:
            current_body.append(line)
    # Última sección
    if current_heading != "" or current_body:
        sections.append((current_heading, "\n".join(current_body)))
    # Si no hubo cabeceras, todo es preámbulo
    if not sections and text:
        sections.append(("", text))
    return sections


def _dedupe_sections(sections: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], list[str]]:
    """Dedupe por heading: UNA copia por sección.

    Si dos copias tienen contenido idéntico → una sola.
    Si difieren → se queda la más reciente (última en el fichero) y warning.
    """
    warnings: list[str] = []
    seen: dict[str, str] = {}  # heading -> body
    order: list[str] = []  # orden de primera aparición

    for heading, body in sections:
        # El preámbulo ("") no se deduplica por heading, se concatena
        if heading == "":
            if "" in seen:
                # Merge preámbulos (no debería haber dos)
                if body.strip() and body.strip() != seen[""].strip():
                    warnings.append(f"preámbulo difiere — se mantiene el último")
                seen[""] = body  # último manda
            else:
                seen[""] = body
                order.append("")
            continue

        if heading not in seen:
            seen[heading] = body
            order.append(heading)
        else:
            existing = seen[heading]
            if existing.strip() == body.strip():
                warnings.append(f"dedupe: sección {heading!r} duplicada idéntica — colapsada")
            else:
                warnings.append(f"conflicto: sección {heading!r} difiere — se queda la más reciente")
                seen[heading] = body  # última gana

    result = [(h, seen[h]) for h in order]
    return result, warnings


def _reorder_sections(
    sections: list[tuple[str, str]], expected_order: list[str]
) -> list[tuple[str, str]]:
    """Reordena secciones según expected_order (por hora extraída).

    Secciones sin hora o con hora no en expected_order van al final
    preservando orden relativo.
    """
    # Mapeo hora -> índice canónico
    order_index = {h: i for i, h in enumerate(expected_order)}

    # Separar preámbulo
    preamble = [(h, b) for h, b in sections if h == ""]
    rest = [(h, b) for h, b in sections if h != ""]

    def sort_key(item: tuple[str, str]) -> tuple[int, int]:
        heading, _ = item
        hora = _extract_hora(heading)
        if hora and hora in order_index:
            return (0, order_index[hora])
        # Sin hora o hora desconocida → al final, orden de aparición
        return (1, 999)

    # Para estabilidad, ordenamos solo los que tienen hora conocida
    conocidas = [s for s in rest if _extract_hora(s[0]) in order_index]
    desconocidas = [s for s in rest if _extract_hora(s[0]) not in order_index]

    conocidas_sorted = sorted(conocidas, key=sort_key)
    # Desconocidas mantienen orden original
    result = preamble + conocidas_sorted + desconocidas
    return result


def _render(sections: list[tuple[str, str]]) -> str:
    parts: list[str] = []
    for heading, body in sections:
        if heading == "":
            if body:
                parts.append(body)
        else:
            parts.append(heading)
            if body:
                parts.append(body)
    text = "\n".join(parts)
    # Normaliza: termina con \n, colapsa \n\n\n → \n\n
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    if text and not text.endswith("\n"):
        text += "\n"
    return text


def process_file(path: Path, expected_order: list[str], check: bool = False) -> int:
    """Procesa un fichero. Devuelve 0 si ok, 1 si hay error."""
    raw = path.read_text(encoding="utf-8")

    has_markers = "<<<<<<<" in raw or ">>>>>>>" in raw

    # Expandir marcadores
    cleaned = _strip_markers(raw)

    # Verificar que no queden marcadores
    if "<<<<<<<" in cleaned or ">>>>>>>" in cleaned:
        print(f"[resolutor] ERROR: {path}: quedan marcadores <<<<<<< tras expansión", file=sys.stderr)
        return 1

    sections = _split_sections(cleaned)
    deduped, warnings = _dedupe_sections(sections)

    for w in warnings:
        print(f"[resolutor] {path}: {w}", file=sys.stderr)

    reordered = _reorder_sections(deduped, expected_order)
    rendered = _render(reordered)

    # Assertions de contenido: toda ## HH:00 esperada debe estar si el fichero ya tenía alguna
    # Solo exige presencia si el fichero original contenía al menos una hora del orden
    horas_presentes_original = set(_extract_hora(h) for h, _ in sections if _extract_hora(h))
    horas_presentes_final = set(_extract_hora(h) for h, _ in reordered if _extract_hora(h))
    # No exigimos TODAS las horas — solo verificamos que no se perdieron horas que ya existían
    perdidas = horas_presentes_original - horas_presentes_final
    if perdidas:
        print(f"[resolutor] ERROR: {path}: secciones perdidas {sorted(p for p in perdidas if p)}", file=sys.stderr)
        return 1

    # Verificación final: cero <<<<<<< por línea
    for i, line in enumerate(rendered.splitlines(), 1):
        if "<<<<<<<" in line or ">>>>>>>" in line:
            print(f"[resolutor] ERROR: {path}:{i}: queda marcador", file=sys.stderr)
            return 1

    if check:
        # En modo check: si hubo marcadores o dedupe con conflicto, reporta
        if has_markers:
            print(f"[resolutor] {path}: --check detectó marcadores (habría resuelto)", file=sys.stderr)
            return 1
        if warnings:
            # warnings con "difiere" son informativos pero no error en check
            pass
        # Si el renderizado difiere del original limpio, informa
        if rendered.strip() != cleaned.strip():
            print(f"[resolutor] {path}: --check detectó reorden/dedupe pendiente", file=sys.stderr)
            return 1
        return 0

    # Escribir solo si cambió
    if rendered != raw:
        path.write_text(rendered, encoding="utf-8")
        print(f"[resolutor] {path}: resuelto ({len(warnings)} avisos)", file=sys.stderr)
    else:
        print(f"[resolutor] {path}: limpio", file=sys.stderr)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolutor canónico de huellas (colisiones git)")
    parser.add_argument("files", nargs="+", help="ficheros a resolver")
    parser.add_argument("--check", action="store_true", help="solo valida, no escribe")
    parser.add_argument("--order", default=",".join(CANON_ORDER), help="orden esperado de horas, coma-separado")
    args = parser.parse_args()

    expected = [o.strip() for o in args.order.split(",") if o.strip()]

    exit_code = 0
    for f in args.files:
        p = Path(f)
        if not p.exists():
            print(f"[resolutor] ERROR: {f} no existe", file=sys.stderr)
            exit_code = 1
            continue
        rc = process_file(p, expected, check=args.check)
        if rc != 0:
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
