"""state.py — GameState: el estado agregador + save/load versionado (§2.6).

El PRIMER save del juego (T1, plan 28/08): `GameState` envuelve la Shell del
cap. 0 como dato plano (ARCHITECTURE §1.5: sin objetos opacos ni referencias
vivas — un save se puede escribir a mano a disco). La clase NO hace I/O: el
guardado atómico vive en las funciones de módulo `save()`/`load()`, testeable
headless con tmp_path.

Decisiones v1 (racional en una línea):
- `SAVE_VERSION` int monotónico desde 1 (no semver: solo lo lee `from_dict`,
  comparable con `<`); migrar barato = cableado desde el día 1 (§2.6).
- Sin reloj real: `saved_at` es el tick SIMULADO de la Shell en el momento del
  save (§3: core sin reloj real; el save es reproducible a tiempo de juego).
- Migraciones: `_MIGRATIONS` {versión origen → callable(dict)->dict}, nace
  VACÍO (v1 es la primera versión real); `from_dict`/`load` aplican la cadena
  v_origen → … → SAVE_VERSION. Un save sin `"version"` se rechaza salvo que
  haya migración v0 registrada.
- Igualdad a nivel de DICTS serializados: Shell no define `__eq__`; la
  identidad de estados se ejercita con `to_dict()`.
- JSON determinista: `sort_keys=True` + `ensure_ascii=False` (bytes
  reproducibles y legible a mano).
- Límite v1 declarado: el set de comandos NO viaja en el save (contrato de
  `Shell.to_dict`; `Shell.from_dict` reconstruye con el default). Viajará por
  migración v2 cuando exista selección de set por capítulo.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable

from core.sandbox.shell import Shell

#: Versión del formato de save (schema_version, §2.6). Int monotónico.
SAVE_VERSION = 1

#: Registro de migraciones PRIVADO: {versión origen: callable(dict)->dict}.
#: Vacío en v1 (no hay versiones anteriores reales); el mecanismo queda
#: probado con la migración sintética v0→v1 de los tests (white-box).
_MIGRATIONS: dict[int, Callable[[dict[str, Any]], dict[str, Any]]] = {}


class SaveError(Exception):
    """Base de todos los errores de save/load."""


class SaveVersionError(SaveError):
    """Versión de save desconocida o save sin cabecera de versión."""


class SaveIntegrityError(SaveError):
    """Save dañado: JSON inválido, claves ausentes o estado no serializable."""


@dataclass
class GameState:
    """Partida completa serializable ida y vuelta (§2.6, §1.5).

    v0 envuelve SOLO la Shell del cap. 0: los futuros hub/unlocks/karma/
    récords entrarán como sub-dicts hermanos de `"shell"` vía migración —
    GameState AGREGA, no aplana la sesión.
    """

    shell: Shell
    version: int = SAVE_VERSION
    #: Inventario de conocimientos dominados por competencia (§2.7/§7.5.3):
    #: {id_boon: True}. Opcional en el formato v1 (sub-dict hermano de "shell").
    knowledge: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Estado completo a dict plano JSON-safe (ida y vuelta con from_dict)."""
        return {
            "version": self.version,
            "saved_at": self.shell.tick,  # tick SIMULADO, no reloj real (§3)
            "shell": self.shell.to_dict(),
            "knowledge": dict(self.knowledge),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "GameState":
        """Reconstruye desde dict plano; aplica migraciones si hace falta.

        SaveVersionError si la versión es desconocida o falta la cabecera
        (salvo migración v0 registrada); SaveIntegrityError si falta la
        sección `"shell"` o es inválida.
        """
        d = _migrate(d)
        try:
            raw_shell = d["shell"]
        except KeyError:
            raise SaveIntegrityError("save sin la sección 'shell'") from None
        try:
            shell = Shell.from_dict(raw_shell)
        except (KeyError, TypeError, ValueError) as exc:
            raise SaveIntegrityError(f"sección 'shell' inválida: {exc!r}") from exc
        return cls(
            shell=shell,
            version=int(d["version"]),
            knowledge=dict(d.get("knowledge") or {}),
        )


def _migrate(d: dict[str, Any]) -> dict[str, Any]:
    """Cadena de migraciones v_origen → … → SAVE_VERSION (§2.6).

    Lanza SaveVersionError con mensaje claro (qué recibió, qué soporta)
    cuando la versión es mayor que la actual o no tiene migración registrada.
    """
    if "version" not in d:
        if 0 in _MIGRATIONS:  # save pre-v1: solo con migración v0 registrada
            d = _MIGRATIONS[0](dict(d))
        else:
            raise SaveVersionError("save sin cabecera de versión")
    try:
        version = int(d["version"])
    except (KeyError, TypeError, ValueError):
        raise SaveVersionError(f"versión ilegible: {d.get('version')!r}") from None
    if version > SAVE_VERSION:
        raise SaveVersionError(
            f"save de versión {version} no soportada "
            f"(este juego soporta hasta {SAVE_VERSION})"
        )
    while version < SAVE_VERSION:
        step = _MIGRATIONS.get(version)
        if step is None:
            raise SaveVersionError(
                f"sin migración registrada de versión {version} "
                f"(soportadas: hasta {SAVE_VERSION})"
            )
        d = step(dict(d))
        version = int(d["version"])
    return d


def save(state: GameState, path: str | os.PathLike[str]) -> None:
    """Guarda ATÓMICAMENTE: `<path>.tmp` + `os.replace` (§2.6).

    Si la serialización falla (estado con valores no JSON-safe), lanza
    SaveIntegrityError, limpia el .tmp si puede y deja CUALQUIER save
    anterior intacto (el replace nunca llegó a ocurrir).
    """
    data = state.to_dict()
    tmp = f"{path}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, sort_keys=True)
    except TypeError as exc:
        try:
            os.unlink(tmp)
        except OSError:
            pass  # mejor esfuerzo: el próximo save reutiliza el nombre
        raise SaveIntegrityError(f"estado no serializable a JSON: {exc}") from exc
    os.replace(tmp, path)


def load(path: str | os.PathLike[str]) -> GameState:
    """Carga un save de disco: valida versión, migra y reconstruye.

    Un JSON escrito A MANO (sin pasar por save()) carga igual (§1.5).
    FileNotFoundError/PermissionError se propagan tal cual: el llamador
    decide qué hacer con un save ausente o ilegible.
    """
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    try:
        d = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SaveIntegrityError(f"save con JSON inválido: {exc}") from exc
    if not isinstance(d, dict):
        raise SaveIntegrityError("save inválido: el JSON raíz no es un objeto")
    return GameState.from_dict(d)
