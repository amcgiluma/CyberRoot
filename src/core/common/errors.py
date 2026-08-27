"""errors.py — errores de dominio compartidos del core (ARCHITECTURE §2.1).

Tipos base de excepción reutilizados por todo `src/core`: `core/` lanza
errores de dominio (CyberRootError) en vez de `Exception` pelada, para que
render/harness filtren por jerarquía sin acoplarse a detalles internos.
Sin lógica de juego; solo stdlib.
"""


class CyberRootError(Exception):
    """Base de los errores de dominio del juego.

    Toda excepción que el core propaga hacia fuera debería derivar de aquí
    (ARCHITECTURE §1 y §2.1: la frontera core/render habla dicts planos, pero
    los fallos internos se señalizan con tipos de dominio reconocibles).
    """


class InvalidCommandError(CyberRootError):
    """Comando malformado (la usa `types.Command.from_dict`).

    Señala un dict de comando que no respeta el contrato plano §1.2
    (`{"cmd": str no vacío, ...}`): falta la clave canónica, es no-str/vacía,
    o la entrada ni siquiera es un Mapping.
    """


class NotPlainDataError(CyberRootError):
    """Dato no serializable a JSON plano (la usa `ensure_plain`).

    El core solo persiste/atraviesa JSON plano estricto (§3, §4.5): tuples,
    sets, bytes, floats no finitos, objetos arbitrarios, claves de dict no
    str y ciclos/estructuras demasiado profundas violan esa regla. El mensaje
    incluye la RUTA del fallo dentro de la estructura para facilitar el debug.
    """