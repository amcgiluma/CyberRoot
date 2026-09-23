"""permisos.py — `chmod` y `chown` (familia permisos, cap. 1/5).

S1 19/09 (Smough): física mínima de auditoría y defensa para la Subestación
(05-subestacion.md). Cap. 5 es la ÚNICA incursión invertida: defender la
casa cerrando permisos (E1/E4). Semántica GNU-honesta (DESIGN §2.6.8) en v0
minimalista: solo lo que exige CH5-E1/E3/E4, sin modos simbólicos
complejos. Sin RNG (§2.2).
S1 23/09 (Smough): soporte `-R`/`--recursive` honesto — sobre fichero es
no-op válido (exit 0, mismo karma que sin -R); sobre dir recorre children
en orden determinista (sorted codepoint), sin RNG.

- `chmod [-R] MODE FILE...` — MODE octal 0-777 / 0-7777 (3-4 dígitos 0-7) o
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


def _is_recursive_flag(tok: str) -> bool:
    """True si tok es un flag de recursividad (-R / --recursive / combinados tipo -Rv)."""
    if tok in ("-R", "--recursive"):
        return True
    if tok.startswith("-") and not tok.startswith("--") and "R" in tok:
        # -Rv, -vR, -Rcf etc — cualquier combinado que contenga R
        return True
    return False


def _chmod_recursive(node: DirNode | FileNode, mode: str) -> None:
    """Aplica mode recursivamente en orden determinista (sorted por codepoint)."""
    effective = mode if _OCTAL_RE.match(mode) else "755" if "+x" in mode else "644"
    node.mode = effective
    node.mtime += 1
    if isinstance(node, DirNode):
        for name in sorted(node.children):
            _chmod_recursive(node.children[name], mode)


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
    # --- parse flags leading (-R / --recursive / -v etc) antes del modo ---
    recursive = False
    idx = 0
    # flags válidos que preceden al modo (GNU: -R --recursive -v --verbose -c -f etc)
    known_flags = {
        "-R", "--recursive", "-v", "--verbose", "-c", "--changes",
        "-f", "--silent", "--quiet",
    }
    while idx < len(argv):
        tok = argv[idx]
        if tok == "--":
            idx += 1
            break
        if tok in known_flags or _is_recursive_flag(tok):
            if _is_recursive_flag(tok):
                recursive = True
            idx += 1
            continue
        if tok.startswith("-") and not tok.startswith("--") and len(tok) > 1:
            # flags combinados tipo -Rv, -cf etc
            # si contiene R → recursive; si todos son v/c/f/R → flag válido
            chars = set(tok[1:])
            if chars <= {"R", "v", "c", "f"}:
                if "R" in chars:
                    recursive = True
                idx += 1
                continue
            # flag desconocido con R? ya tratado arriba; resto → invalid option más tarde
            # si es combinación desconocida, dejar que el parsing de modo lo detecte
            # pero no avanzar como flag: romper y tratar como posible modo inválido
            if any(ch in chars for ch in "Rvcf"):
                # tratar como flag igualmente (GNU ignora orden)
                if "R" in chars:
                    recursive = True
                idx += 1
                continue
        break
    remaining = argv[idx:]
    if not remaining:
        return CommandResult(
            stderr="chmod: missing operand\nTry 'chmod --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    if len(remaining) < 2:
        # falta file operand
        mode = remaining[0]
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
    mode, *files = remaining
    if not _chmod_mode_valid(mode):
        return CommandResult(
            stderr=f"chmod: invalid mode: ‘{mode}’\nTry 'chmod --help' for more information.",
            exit_code=1,
            noise=noise,
        )
    # Manejar -- separador como modo
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
        # Cambia mode — con -R recursivo sobre dir
        if recursive and isinstance(node, DirNode):
            _chmod_recursive(node, mode)
        else:
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
