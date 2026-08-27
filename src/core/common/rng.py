"""rng.py — RNG seedeada determinista (ARCHITECTURE §1.3, DESIGN §4.5).

PRNG splitmix64 propio: aritmética entera exacta ⇒ secuencia idéntica ante
la misma seed entre procesos, plataformas y versiones de CPython (el criterio
de aceptación del plan 27/08 exige reproducibilidad cross-proceso).

Reglas que este módulo hace cumplir:
- RNG SIEMPRE seedeada; prohibido `random` global (§1.3).
- Semillas no-enteras (`str`/`bytes`) via `sha256`, JAMÁS via `hash()`
  (PYTHONHASHSEED rompería la reproducibilidad entre procesos).
- El RNG jamás decide semántica: aquí solo hay números (DESIGN §4.5).
"""

from __future__ import annotations

import hashlib
from typing import Sequence, TypeVar

SeedSource = int | str | bytes

_T = TypeVar("_T")

_MASK64 = (1 << 64) - 1
_GOLDEN = 0x9E3779B97F4A7C15


def _seed_to_u64(seed: SeedSource) -> int:
    """Normaliza cualquier SeedSource a un entero de 64 bits determinista."""
    if isinstance(seed, bool):
        raise TypeError("seed bool no admitida (usa 0/1 explícitos)")
    if isinstance(seed, int):
        return seed & _MASK64
    if isinstance(seed, (str, bytes)):
        raw = seed.encode("utf-8") if isinstance(seed, str) else seed
        digest = hashlib.sha256(raw).digest()
        return int.from_bytes(digest[:8], "big")
    raise TypeError(f"seed debe ser int | str | bytes, no {type(seed).__name__}")


class Rng:
    """RNG determinista (splitmix64) con estado serializable como UN entero.

    Uso:
        rng = Rng("run-123")
        rng.below(10)              # int en [0, 10)
        sub = rng.fork("mapa")     # sub-RNG para un subsistema (§1.3)

    Garantías:
    - Misma seed ⇒ misma secuencia infinita de salidas, en cualquier proceso.
    - Todos los métodos avanzan exactamente el estado indicado en su docstring;
      nunca hay reintentos dependientes de contexto externo.
    """

    __slots__ = ("_state",)

    def __init__(self, seed: SeedSource) -> None:
        # Estado inicial ya "dorada": splitmix64 basta con estado != 0.
        self._state = (_seed_to_u64(seed) + _GOLDEN) & _MASK64
        if self._state == 0:
            self._state = _GOLDEN

    # -- primitiva ----------------------------------------------------------

    def uint64(self) -> int:
        """Siguiente palabra de 64 bits ([0, 2**64)). Avanza el estado 1 paso.

        Es splitmix64 (Steele et al. 2014): 3 rondas de mezcla por salida,
        periodo completo 2**64; un paso = una suma + mezcla.
        """
        self._state = (self._state + _GOLDEN) & _MASK64
        z = self._state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & _MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & _MASK64
        return (z ^ (z >> 31)) & _MASK64

    # -- enteros ------------------------------------------------------------

    def below(self, n: int) -> int:
        """Entero uniforme en [0, n). Lanza ValueError si n <= 0.

        Sin sesgo: rejection sampling sobre el rango [0, m*n) mayor múltiplo
        de n bajo 2**64 — no usa módulo directo sobre toda la palabra.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError(f"below espera int, no {type(n).__name__}")
        if n <= 0:
            raise ValueError(f"below requiere n >= 1, recibido {n}")
        if n == 1:
            return 0
        span = (1 << 64) // n * n  # múltiplo exacto de n bajo 2**64
        while True:
            x = self.uint64()
            if x < span:
                return x % n

    def integers(self, low: int, high: int) -> int:
        """Entero uniforme EN INCLUSIVO [low, high]. ValueError si low > high."""
        if low > high:
            raise ValueError(f"integers vacío: low {low} > high {high}")
        return low + self.below(high - low + 1)

    # -- flotantes ----------------------------------------------------------

    def float(self) -> float:
        """Flotante uniforme en [0.0, 1.0) con 53 bits de mantisa."""
        return (self.uint64() >> 11) * (2.0 ** -53)

    # -- utilidades estilo stdlib ---------------------------------------------

    def choice(self, population: Sequence[_T]) -> _T:
        """Un elemento de population (no vacía). IndexError si está vacía... no:
        lanza ValueError por coherencia con below/integers.
        """
        if len(population) == 0:
            raise ValueError("choice sobre secuencia vacía")
        return population[self.below(len(population))]

    def shuffle(self, population: Sequence[_T]) -> list[_T]:
        """Devuelve copia barajada (Fisher-Yates hacia abajo); NO muta entrada."""
        out = list(population)
        for i in reversed(range(1, len(out))):
            j = self.below(i + 1)
            out[i], out[j] = out[j], out[i]
        return out

    def sample(self, population: Sequence[_T], k: int) -> list[_T]:
        """K elementos DISTINCTOS (sin repetición), orden barajado.

        ValueError si k < 0 o k > len(population).
        """
        if k < 0:
            raise ValueError(f"sample k negativo: {k}")
        if k > len(population):
            raise ValueError(
                f"sample de {k} elementos sobre población de {len(population)}"
            )
        pool = list(population)
        result: list[_T] = []
        # selección parcial de Fisher-Yates O(k)
        for i in range(k):
            j = i + self.below(len(pool) - i)
            pool[i], pool[j] = pool[j], pool[i]
            result.append(pool[i])
        return result

    # -- derivación de subsistemas ----------------------------------------

    def fork(self, label: "str | int | bytes") -> "Rng":
        """Sub-RNG derivada del estado ACTUAL + label (no consume tiradas del padre).

        Contrato §1.3: cada subsistema deriva sus sub-semillas de la semilla
        de run; fork es ese mecanismo (p.ej. fork("mapa"), fork("vigilancia")).
        """
        basis = self._state.to_bytes(8, "big")
        tag = label.encode() if isinstance(label, str) else (
            label.to_bytes(((label.bit_length() + 7) // 8) or 1, "big")
            if isinstance(label, int)
            else label
        )
        child_seed_raw = hashlib.sha256(b"cyberroot.fork:" + tag + b":" + basis).digest()
        child = Rng.__new__(Rng)
        child_state = int.from_bytes(child_seed_raw[:8], "big")
        child._state = child_state
        if child._state == 0:
            child._state = _GOLDEN
        return child

    # -- serialización ----------------------------------------------------

    @property
    def state(self) -> int:
        """Estado interno como entero serializable (save/load ida-y-vuelta)."""
        return self._state

    @classmethod
    def from_state(cls, state: int) -> "Rng":
        """Reconstruye una Rng en el estado exacto dado."""
        if not isinstance(state, int) or isinstance(state, bool):
            raise TypeError(f"state debe ser int, no {type(state).__name__}")
        clone = cls.__new__(cls)
        clone._state = state & _MASK64
        if clone._state == 0:
            clone._state = _GOLDEN
        return clone


def mix_seeds(a: SeedSource, b: SeedSource) -> int:
    """Mezcla dos fuentes de semilla en una seed de 64 bits (ayudante opcional)."""
    digest = hashlib.sha256(
        _seed_to_u64(a).to_bytes(8, "big")
        + b":"
        + _seed_to_u64(b).to_bytes(8, "big")
    ).digest()
    return int.from_bytes(digest[:8], "big")
