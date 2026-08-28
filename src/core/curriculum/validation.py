"""validation.py — validador del DAG de currículo (S2, criterio de Gwyndolin).

Rechaza: ciclos, prereqs/hosts inexistentes, duplicados, capítulos fuera de
rango, quests con tint desconocido, quests con `requires` no enseñado aún
(invariante pedagógico §6.4.1) y claves de texto vacías. Todo en negativo con
tests (`test_validation.py`).

Estrategia anti-ciclo: DFS por color (blanco/gris/negro) con raíz de error
reproducible («a → b → c → a»), determinista ordenando por id. Cero RNG.
"""

from __future__ import annotations

from core.curriculum.model import CHAPTERS, FAMILIES, TINTS, Curriculum, CurriculumError

_WHITE = 0  # sin visitar
_GRAY = 1  # en la pila de la DFS actual
_BLACK = 2  # cerrado, sin ciclo por aquí


def validate(cur: Curriculum) -> None:
    """Levanta `CurriculumError` si el currículo es inválido; None si es sano.

    En negativo (tests): ciclo, prereq inexistente, prereq de capítulo futuro
    (§6.4.1), quest duplicada, concept duplicado, capítulo fuera de rango,
    familia desconocida, tint desconocido, `requires` no enseñado aún, claves
    de texto vacías, versión incorrecta.

    NOTA: no hay chequeo separado de «alcanzabilidad» porque es matemáticamente
    redundante — prereqs todos existentes + grafo acíclico garantizan que toda
    cadena de prereqs desciende hasta una raíz (concepto sin prereqs).
    """
    _validate_version(cur)
    _validate_concepts(cur)
    _validate_quest_entries(cur)
    _validate_acyclic(cur)


def _validate_version(cur: Curriculum) -> None:
    if cur.version != 1:
        raise CurriculumError(
            f"version de curriculum no soportada: {cur.version!r} (esperada 1)"
        )


def _validate_concepts(cur: Curriculum) -> None:
    seen: set[str] = set()
    for c in cur.concepts:
        if not c.id or not c.id.strip():
            raise CurriculumError("concept con id vacío")
        if c.id in seen:
            raise CurriculumError(f"concept duplicado: {c.id!r}")
        seen.add(c.id)
        if c.family not in FAMILIES:
            raise CurriculumError(
                f"concept {c.id!r}: familia desconocida {c.family!r}"
            )
        if c.chapter not in CHAPTERS:
            raise CurriculumError(
                f"concept {c.id!r}: capítulo fuera de rango {c.chapter!r}"
            )
        if not c.summary_key or not c.summary_key.strip():
            raise CurriculumError(f"concept {c.id!r}: summary_key vacía")
        # Prereqs existentes + regla pedagógica dura (§6.4.1): un concepto se
        # enseña DESPUÉS o EN el mismo capítulo que sus prereqs — jamás antes.
        for p in c.prerequisites:
            if p == c.id:
                raise CurriculumError(f"concept {c.id!r}: no puede ser prereq de sí mismo")
    ids = {c.id for c in cur.concepts}
    for c in cur.concepts:
        for p in c.prerequisites:
            if p not in ids:
                raise CurriculumError(
                    f"concept {c.id!r}: prereq inexistente {p!r}"
                )
    by_id = {c.id: c for c in cur.concepts}
    for c in cur.concepts:
        for p in c.prerequisites:
            if by_id[p].chapter > c.chapter:
                raise CurriculumError(
                    f"concept {c.id!r}: prereq {p!r} se enseña en el capítulo "
                    f"{by_id[p].chapter} (posterior a {c.chapter}) — viola §6.4.1"
                )


def _validate_quest_entries(cur: Curriculum) -> None:
    seen_q: set[str] = set()
    by_id = {c.id: c for c in cur.concepts}
    for q in cur.quests:
        if not q.id or not q.id.strip():
            raise CurriculumError("quest con id vacío")
        if q.id in seen_q:
            raise CurriculumError(f"quest duplicada: {q.id!r}")
        seen_q.add(q.id)
        if q.chapter not in CHAPTERS:
            raise CurriculumError(
                f"quest {q.id!r}: capítulo fuera de rango {q.chapter!r}"
            )
        if q.tint not in TINTS:
            raise CurriculumError(f"quest {q.id!r}: tint desconocido {q.tint!r}")
        if not q.title_key or not q.title_key.strip():
            raise CurriculumError(f"quest {q.id!r}: title_key vacía")
        for r in q.requires:
            c = by_id.get(r)
            if c is None:
                raise CurriculumError(
                    f"quest {q.id!r}: requiere concepto inexistente {r!r}"
                )
            if c.chapter > q.chapter:
                raise CurriculumError(
                    f"quest {q.id!r}: requiere {r!r} que se enseña en el "
                    f"capítulo {c.chapter} (posterior a {q.chapter}) — el "
                    f"encargo sería irresoluble cuando llega (§6.4.1)"
                )


def _validate_acyclic(cur: Curriculum) -> None:
    """DFS por color; el ciclo se reporta como camino «a → b → … → a».

    Reconstrucción del camino: en el back-edge (u→v con v GRIS), v es
    ancestro de u — se camina de u hacia arriba por `parent` hasta v.
    PROHIBIDO mutar `parent` en la detección: cerraría la cadena sobre sí
    misma y el recorrido no terminaría nunca (bug cazado y testeado).
    """
    color = {c.id: _WHITE for c in cur.concepts}
    parent: dict[str, str | None] = {}

    def cycle_path(u: str, v: str) -> str:
        path = [u]
        node: str = u
        while node != v:
            nxt = parent[node]
            # v es ancestro GRIS de u: el camino por padres llega a v ANTES
            # que a la raíz — nxt nunca es None aquí (invariante testeado).
            assert nxt is not None, f"camino roto hacia {v!r} desde {u!r}"
            node = nxt
            path.append(node)
        path.reverse()
        return " → ".join(path) + f" → {v}"

    def dfs(u: str) -> None:
        color[u] = _GRAY
        for v in sorted(_prereqs(cur, u)):
            if color[v] == _GRAY:
                raise CurriculumError(
                    f"ciclo en el DAG de conceptos: {cycle_path(u, v)}"
                )
            if color[v] == _WHITE:
                parent[v] = u
                dfs(v)
        color[u] = _BLACK

    for c in sorted(cur.concepts, key=lambda c: c.id):
        if color[c.id] == _WHITE:
            parent[c.id] = None
            dfs(c.id)


def _prereqs(cur: Curriculum, concept_id: str) -> tuple[str, ...]:
    for c in cur.concepts:
        if c.id == concept_id:
            return c.prerequisites
    return ()
