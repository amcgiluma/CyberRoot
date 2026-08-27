"""Sistema de ficheros virtual serializable (ARCHITECTURE §2.2, §2.1.5).

Árbol de nodos (ficheros y directorios) con dueño, grupo, permisos y mtime
SIMULADO, sin reloj real ni `random`. Las iteraciones caminan SIEMPRE listas
ordenadas (PLAN.md §5) para reproducibilidad byte a byte entre procesos, y
`to_dict` recorre los hijos por codepoint por la misma razón.

Los errores son DATOS estructurados (kind + path): los COMANDOS mapean kind
a texto y exit code GNU/coreutils en inglés (DESIGN §2.6.8); aquí no hay texto
"* No such file", solo códigos. `invalid_argument` cubre `cp` sobre sí mismo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypeAlias

Node: TypeAlias = "FileNode | DirNode"
DictData: TypeAlias = dict[str, Any]

ErrorKind: TypeAlias = Literal[
    "not_found",
    "not_a_directory",
    "is_a_directory",
    "permission_denied",
    "not_empty",
    "invalid_argument",
    "same_file",
]


class FsError(Exception):
    """Error de filesystem como datos: `kind` (código) + `path` (blanco)."""

    def __init__(self, kind: ErrorKind, path: str) -> None:
        super().__init__(kind, path)
        self.kind = kind
        self.path = path

    def __str__(self) -> str:
        """Representación legible usada en logs/tests (no en salida de comando)."""
        return f"{self.kind}: {self.path}"


@dataclass
class FileNode:
    """Fichero: contenido de texto + metadatos (ARCHITECTURE §2.2)."""

    name: str
    content: str = ""
    owner: str = "root"
    group: str = "root"
    mode: str = "644"
    mtime: int = 0

    def to_dict(self) -> DictData:
        """Serialize a dict plano y etiquetado, ida y vuelta EXACTO (§1.5)."""
        return {
            "type": "file",
            "name": self.name,
            "content": self.content,
            "owner": self.owner,
            "group": self.group,
            "mode": self.mode,
            "mtime": self.mtime,
        }

    @classmethod
    def from_dict(cls, d: DictData) -> "FileNode":
        """Deserializa (cuyo inverso exacto es `to_dict`)."""
        return cls(
            name=str(d["name"]),
            content=str(d["content"]),
            owner=str(d["owner"]),
            group=str(d["group"]),
            mode=str(d["mode"]),
            mtime=int(d["mtime"]),
        )


@dataclass
class DirNode:
    """Directorio: mapa nombre->nodo + metadatos (ARCHITECTURE §2.2)."""

    name: str
    children: dict[str, Node] = field(default_factory=dict)
    owner: str = "root"
    group: str = "root"
    mode: str = "755"
    mtime: int = 0

    def to_dict(self) -> DictData:
        """Serializa recursivo; hijos recorridos por codepoint (determinismo)."""
        children: DictData = {
            name: self.children[name].to_dict() for name in sorted(self.children)
        }
        return {
            "type": "dir",
            "name": self.name,
            "children": children,
            "owner": self.owner,
            "group": self.group,
            "mode": self.mode,
            "mtime": self.mtime,
        }

    @classmethod
    def from_dict(cls, d: DictData) -> "DirNode":
        """Deserializa recursivo; inverso exacto de `to_dict`."""
        children: dict[str, Node] = {}
        raw_children = d["children"]
        assert isinstance(raw_children, dict)
        # Recorre los hijos en el orden serializado para mantener el orden.
        for name, raw in raw_children.items():
            assert isinstance(raw, dict)
            if raw["type"] == "dir":
                children[str(name)] = DirNode.from_dict(raw)
            else:
                children[str(name)] = FileNode.from_dict(raw)
        return cls(
            name=str(d["name"]),
            children=children,
            owner=str(d["owner"]),
            group=str(d["group"]),
            mode=str(d["mode"]),
            mtime=int(d["mtime"]),
        )


class FileSystem:
    """FS virtual con rutas absolutas/relativas y cwd (ARCHITECTURE §2.2)."""

    def __init__(self, root: DirNode | None = None) -> None:
        """Crea un FS; sin argumento parte de la raíz `/` vacía."""
        self.root = root if root is not None else DirNode(name="/")

    # ---- serialización / copia (ARCHITECTURE §1.5) ---------------------

    def to_dict(self) -> DictData:
        """Serializa el árbol completo a dict plano."""
        return {"root": self.root.to_dict()}

    @classmethod
    def from_dict(cls, d: DictData) -> "FileSystem":
        """Reconstruye un FS desde dict; copia profunda, independiente."""
        root = d["root"]
        assert isinstance(root, dict)
        return cls(root=DirNode.from_dict(root))

    def snapshot(self) -> "FileSystem":
        """Copia profunda e independiente vía roundtrip de dict."""
        return FileSystem.from_dict(self.to_dict())

    # ---- normalización de rutas (PLAN.md §estructura) ------------------

    @staticmethod
    def _segments(cwd: str) -> list[str]:
        """Trocea una cwd ya normalizada en sus segmentos no vacíos."""
        return [p for p in cwd.split("/") if p not in ("", ".")]

    @staticmethod
    def _normalize(parts: list[str]) -> list[str]:
        """Colapsa `.`, `//` y `..` (este último clampa en la raíz)."""
        out: list[str] = []
        for p in parts:
            if p in ("", "."):
                continue
            if p == "..":
                if out:
                    out.pop()
            else:
                out.append(p)
        return out

    def _join(self, cwd: str, path: str) -> str:
        """Resuelve `path` (abs. o relativo a `cwd`) a una ruta normalizada.

        El resultado SIEMPRE empieza por `/` y no tiene barra final salvo la
        raíz (cuyo valor canónico es `/`).
        """
        raw = path.split("/") if path.startswith("/") else self._segments(cwd) + path.split("/")
        segs = self._normalize(raw)
        if not segs:
            return "/"
        return "/" + "/".join(segs)

    # ---- resolución / consultas ----------------------------------------

    def resolve(self, path: str, cwd: str = "/") -> Node:
        """Devuelve el nodo destino, absoluto o relativo a `cwd`.

        Errores: `not_found` si no existe (incl. ruta vacía); `not_a_directory`
        si un componente intermedio es un fichero.
        """
        if path == "":
            raise FsError("not_found", path)
        raw = path.split("/") if path.startswith("/") else self._segments(cwd) + path.split("/")
        segs = self._normalize(raw)
        node: Node = self.root
        for seg in segs:
            if isinstance(node, FileNode):
                raise FsError("not_a_directory", path)
            assert isinstance(node, DirNode)
            if seg not in node.children:
                raise FsError("not_found", path)
            node = node.children[seg]
        return node

    def get_dir(self, path: str, cwd: str = "/") -> DirNode:
        """Devuelve el directorio; `not_a_directory` si el nodo es fichero."""
        node = self.resolve(path, cwd)
        if isinstance(node, FileNode):
            raise FsError("not_a_directory", path)
        return node

    def read_file(self, path: str, cwd: str = "/") -> str:
        """Devuelve el contenido; `is_a_directory` si el nodo es directorio."""
        node = self.resolve(path, cwd)
        if isinstance(node, DirNode):
            raise FsError("is_a_directory", path)
        return node.content

    def list_dir(self, path: str, cwd: str = "/") -> list[str]:
        """Nombres de hijos ORDENADOS por codepoint (determinismo §5)."""
        node = self.get_dir(path, cwd)
        return sorted(node.children)

    def change_dir(self, path: str, cwd: str = "/") -> str:
        """Nueva cwd NORMALIZADA (siempre `/...`); `..` clampa en la raíz.

        Normalización PURA de cadena sobre la cwd del shell: con cwds
        ilustrativas tipo `/a/b` (PLAN.md/exigencias de test) el resultado
        debe ser `/a`, no un error. La existencia/validez del destino la
        valida el shell cuando un comando accede de verdad al FS.
        """
        if path == "":
            raise FsError("not_found", path)
        return self._join(cwd, path)

    # ---- copia (PLAN.md decisión 1: cp fuera del set del cap. 0) --------

    def copy_file(self, src: str, dst: str, cwd: str = "/") -> None:
        """Copia un fichero con sus metadatos; mtime_dst = mtime_src (§decisión).

        Sobrescribe si el destino ya es fichero. Errores: `not_found` (fuente
        o padre del destino ausentes), `not_a_directory` (fuente es dir),
        `is_a_directory` (destino es un dir existente), `invalid_argument`
        (destino dentro del propio fuente, p.ej. `cp /a /a/b`).
        """
        src_node = self.resolve(src, cwd)
        if isinstance(src_node, DirNode):
            raise FsError("not_a_directory", src)
        dst_abs = self._join(cwd, dst)
        dst_segs = self._normalize(dst_abs.split("/"))
        src_segs = self._normalize(self._join(cwd, src).split("/"))
        # `cp /a /a/b`: el destino queda bajo el propio fuente.
        if len(dst_segs) > len(src_segs) and dst_segs[: len(src_segs)] == src_segs:
            raise FsError("invalid_argument", dst)
        if not dst_segs:
            raise FsError("not_found", dst)
        parent: Node = self.root
        for seg in dst_segs[:-1]:
            if isinstance(parent, FileNode):
                raise FsError("not_a_directory", dst)
            assert isinstance(parent, DirNode)
            if seg not in parent.children:
                raise FsError("not_found", dst)
            parent = parent.children[seg]
        dst_name = dst_segs[-1]
        if dst_name in parent.children:
            existing = parent.children[dst_name]
            if isinstance(existing, DirNode):
                # GNU real: `cp fichero dir/` copia DENTRO del directorio
                # (dst pasa a ser dir/<base>); error solo si colisiona.
                base = src_segs[-1]
                if base in existing.children:
                    clash = existing.children[base]
                    if isinstance(clash, DirNode):
                        # GNU: «cannot overwrite directory with non-directory».
                        raise FsError("is_a_directory", dst)
                    if dst_segs + [base] == src_segs:
                        raise FsError("same_file", dst)
                    clash.content = src_node.content
                    clash.owner = src_node.owner
                    clash.group = src_node.group
                    clash.mode = src_node.mode
                    clash.mtime = src_node.mtime
                else:
                    existing.children[base] = FileNode(
                        name=base,
                        content=src_node.content,
                        owner=src_node.owner,
                        group=src_node.group,
                        mode=src_node.mode,
                        mtime=src_node.mtime,
                    )
                return
            if dst_segs == src_segs:
                # GNU real: `cp f f` → «'f' and 'f' are the same file».
                raise FsError("same_file", dst)
            existing.content = src_node.content
            existing.owner = src_node.owner
            existing.group = src_node.group
            existing.mode = src_node.mode
            existing.mtime = src_node.mtime
        else:
            assert isinstance(parent, DirNode)
            parent.children[dst_name] = FileNode(
                name=dst_name,
                content=src_node.content,
                owner=src_node.owner,
                group=src_node.group,
                mode=src_node.mode,
                mtime=src_node.mtime,
            )