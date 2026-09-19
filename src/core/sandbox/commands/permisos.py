"""permisos.py — `chmod` y `chown` (familia permisos, cap. 1/5).

S1 19/09 (Smough): física mínima de auditoría y defensa para la Subestación
(05-subestacion.md). Cap. 5 es la ÚNICA incursión invertida: defender la
casa cerrando permisos (E1/E4). Semántica GNU-honesta (DESIGN §2.6.8) en v0
minimalista: solo lo que exige CH5-E1/E3/E4, sin -R ni modos simbólicos
complejos. Sin RNG (§2.2).

- `chmod MODE FILE...` — MODE octal 0-777 / 0-7777 (3-4 dígitos 0-7) o
  simple `+x`/`-x`/`+w`/`-r` como alias honesto para E1/E4 (Gwyndolin 19/09:
  `chmod 600` es el caso canónico de CH5). Cambia `node.mode` (str) y deja
  mtime+1. Errores GNU: missing operand, invalid mode, No such file, Is a
  directory? (no, chmod sobre dir es válido en GNU — cambiamos mode del dir
  también). Exit 1 en error, 0 si alguno ok (GNU mixto). Ruido 1.
- `chown OWNER[:GROUP] FILE...` — cambia `node.owner` (+ group si se da
  `:`). OWNER no vacío alfanumérico/._- (v0). Misma semántica de errores
  que chmod (missing, invalid owner, No such file). Exit 1/0. Ruido 1.

Ambos operan sobre FileNode y DirNode (cambian metadatos, no contenido).
No hay verificación de permisos reales: la fantasía es competencia técnica,
no ACL (DESIGN §6.2). Test frontera: 127 fuera de allowlist (shell filtra).
"""

from __future__ import annotations

import re

from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import DirNode, FileNode, FileSystem, FsError

CHMOD_NAME = "chmod"
CHOWN_NAME = "chown"

# Octal 3-4 dígitos 0-7, o symbolic simple +x -x +w etc (v0)
_OCTAL_RE = re.compile(r"^[0-7]{3,4}$")
_SIMPLE_SYMBOLIC = {"+x", "-x", "+w", "-w", "+r", "-r", "a+x", "a-x", "u+x", "g+x"}
_OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]{1,32}$")


def _chmod_mode_valid(mode: str) -> bool:
    return bool(_OCTAL_RE.match(mode)) or mode in _SIMPLE_SYMBOLIC


def _run_chmod(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    _ = stdin
    noise = noise_event(CHMOD_NAME, argv, tick)
    if not argv:
        return CommandResult(
            stderr="chmod: missing operand\nTry 'chmod --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    if len(argv) < 2:
        # falta file operand
        mode = argv[0]
        if not _chmod_mode_valid(mode):
            return CommandResult(
                stderr=f"chmod: invalid mode: ‘{mode}’\nTry 'chmod --help' for more information.",
                exit_code=1,
                noise=noise,
            )
        return CommandResult(
            stderr="chmod: missing operand after ‘{}’\nTry 'chmod --help' for more information.".format(mode),
            exit_code=1,
            noise=noise,
        )
    mode, *files = argv
    if not _chmod_mode_valid(mode):
        return CommandResult(
            stderr=f"chmod: invalid mode: ‘{mode}’\nTry 'chmod --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    # Manejar -- separador
    if mode == "--":
        return CommandResult(
            stderr="chmod: missing operand\nTry 'chmod --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    errs = []
    any_ok = False
    for f in files:
        if f.startswith("-") and f != "-":
            errs.append(f"chmod: invalid option -- '{f.lstrip(chr(45))}'\nTry 'chmod --help' for more information.")
            continue
        try:
            node = fs.resolve(f, cwd)
        except FsError as e:
            if e.kind == "not_found":
                errs.append(f"chmod: cannot access '{f}': No such file or directory")
            elif e.kind == "not_a_directory":
                errs.append(f"chmod: cannot access '{f}': Not a directory")
            else:
                errs.append(f"chmod: cannot access '{f}': {e.kind}")
            continue
        # Cambia mode
        node.mode = mode if _OCTAL_RE.match(mode) else "755" if "+x" in mode else "644"
        node.mtime += 1
        any_ok = True
    if errs:
        return CommandResult(
            stderr="\n".join(errs),
            exit_code=1,
            noise=noise,
        )
    return CommandResult(stdout="", stderr="", exit_code=0, noise=noise)


def _parse_chown_owner(spec: str) -> tuple[str, str | None] | None:
    """Parsea OWNER[:GROUP] → (owner, group|None) o None si inválido."""
    if ":" in spec:
        owner, group = spec.split(":", 1)
        if not owner or not _OWNER_RE.match(owner):
            return None
        if group == "":
            # `chown owner:` → owner, group vacío (GNU lo acepta como owner: → owner con grupo vacío)
            return (owner, None)
        if not _OWNER_RE.match(group):
            return None
        return (owner, group)
    if not _OWNER_RE.match(spec):
        return None
    return (spec, None)


def _run_chown(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    _ = stdin
    noise = noise_event(CHOWN_NAME, argv, tick)
    if not argv:
        return CommandResult(
            stderr="chown: missing operand\nTry 'chown --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    if len(argv) < 2:
        owner_spec = argv[0]
        if _parse_chown_owner(owner_spec) is None:
            return CommandResult(
                stderr=f"chown: invalid user: ‘{owner_spec}’",
                exit_code=1,
                noise=noise,
            )
        return CommandResult(
            stderr=f"chown: missing operand after ‘{owner_spec}’\nTry 'chown --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    owner_spec, *files = argv
    parsed = _parse_chown_owner(owner_spec)
    if parsed is None:
        return CommandResult(
            stderr=f"chown: invalid user: ‘{owner_spec}’",
            exit_code=1,
            noise=noise,
        )
    owner, group = parsed
    if owner_spec == "--":
        return CommandResult(
            stderr="chown: missing operand\nTry 'chown --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    errs = []
    for f in files:
        if f.startswith("-") and f != "-":
            errs.append(f"chown: invalid option -- '{f.lstrip(chr(45))}'\nTry 'chown --help' for more information.")
            continue
        try:
            node = fs.resolve(f, cwd)
        except FsError as e:
            if e.kind == "not_found":
                errs.append(f"chown: cannot access '{f}': No such file or directory")
            elif e.kind == "not_a_directory":
                errs.append(f"chown: cannot access '{f}': Not a directory")
            else:
                errs.append(f"chown: cannot access '{f}': {e.kind}")
            continue
        node.owner = owner
        if group is not None:
            node.group = group
        node.mtime += 1
    if errs:
        return CommandResult(stderr="\n".join(errs), exit_code=1, noise=noise)
    return CommandResult(stdout="", stderr="", exit_code=0, noise=noise)


CHMOD_SPEC = CommandSpec(
    name=CHMOD_NAME, concepts=frozenset({"chmod"}), noise=1, run=_run_chmod,
)
CHOWN_SPEC = CommandSpec(
    name=CHOWN_NAME, concepts=frozenset({"chown"}), noise=1, run=_run_chown,
)
SPECS: tuple[CommandSpec, ...] = (CHMOD_SPEC, CHOWN_SPEC)
