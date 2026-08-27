# PLAN DE IMPLEMENTACIÓN — Módulo `common` (Ornstein, 27/08)

> Desarrollo del detalle que el plan de Gwyndolin (tarea A) no fijó.
> Fuente normativa: `docs/planes/2026/08/27.md` (QUÉ + criterio de aceptación)
> y `src/core/ARCHITECTURE.md` §2.1 + §3 (frontera y convenciones).
> Rama: `feat/engine`. Todo commit firmado como Ornstein. PR → main (mergea Gwyn).

## 0. Decisiones de diseño previas (el PORQUÉ antes del código)

1. **PRNG propio (splitmix64) en vez de `random.Random`**: `random.Random(int)`
   es bastante estable, pero su doc NO garantiza estabilidad absoluta entre
   versiones/algoritmo interno. splitmix64 son ~20 líneas de aritmética entera
   exacta: determinista entre procesos, plataformas y versiones de CPython,
   trivialmente serializable (UN entero de estado — crítico para save/load de
   Seath §2.6), y elimina toda duda para el test cross-proceso del criterio.
2. **Seeds `str`/`bytes` vía `sha256`, jamás vía `hash()`**: el builtin `hash()`
   de `str` varia entre procesos (PYTHONHASHSEED). Prohibido usarlo.
3. **API de RNG con inglés técnico** (`below/integers/choice/shuffle/sample/fork`)
   siguiendo el estilo stdlib; textos de juego nunca aquí (§3: texto vive en
   `data/`).
4. **`Event` inmutable + datos copiados** al construir (`dict(data)`): publica
   snapshots, evita Aliasing sorpresas; dataclass frozen.
5. **Bus síncrono FIFO**: handlers se ejecutan en orden de suscripción;
   excepciones de handlers PROPAGAN (fail-fast en dev). Sin hilos. Historial
   opcional (`deque(maxlen=k)`) para debug/post-mortem posterior.
6. **Catálogo de tipos de evento: mínimo v0** (prefijo `event.` + constantes
   obvias), marcado abierto — decisión §5.2 de ARCHITECTURE queda abierta hasta
   primer consumo real de render/harness.
7. **`Command` plano ida-y-vuelta** según contrato §1.2
   (`{"cmd": "exec", "argv": [...]}` estilo) + utilidad `ensure_plain()`
   recursiva con profundidad máxima (anti-ciclos), reusable por `state/`.
8. **Solo stdlib, tipado completo, dataclasses, docstrings citando § de DESIGN**
   — convenciones §3 de ARCHITECTURE, verificadas por tests de arquitectura.

## 1. Hitos (secuenciales y verificables)

### H0 — MÍO: Andamiaje e infraestructura de tests raíz (~30 min)
- Crear `.venv` con `~/.local/bin/python3.11` (runtime objetivo ≥3.11, Pyxel)
  + `pip install pytest`.
- `pyproject.toml` raíz con SOLO `[tool.pytest.ini_options]`:
  `testpaths=["src/tests"]`, `pythonpath=["src"]`, `addopts="-q"`.
  (Sin sección `[project]`: aún no es distribución, solo tooling.)
- Esqueleto: `src/core/__init__.py`, `src/core/common/{__init__,rng,events,types,errors}.py`
  (docstrings de placeholder), smoke test `src/tests/smoke/test_package.py`.
- **Hecho si:** `/home/juanma/CyberRoot/.venv/bin/python -m pytest` corre VERDE
  desde la raíz (aunque sea 1 test humo). Commit.

### H1 — SUB-AGENTE A: `rng.py` + sus tests
- **Interfaz exacta a crear en `src/core/common/rng.py`:**
  ```python
  class Rng:
      def __init__(self, seed: int | str | bytes) -> None
      def uint64(self) -> int                       # siguiente palabra 64 bits
      def below(self, n: int) -> int                # [0, n), sin sesgo (rejection sampling)
      def integers(self, a: int, b: int) -> int     # [a, b] INCLUSIVE, sin sesgo
      def float(self) -> float                      # [0.0, 1.0), 53 bits de mantisa
      def choice(self, population: Sequence[T]) -> T
      def shuffle(self, population: Sequence[T]) -> list[T]   # PURA: devuelve copia barajada
      def sample(self, population: Sequence[T], k: int) -> list[T]
      def fork(self, label: str | int | bytes) -> Rng          # sub-RNG derivada (sha256 estado||label)
      @property state -> int                        # estado interno serializable
      @classmethod from_state(cls, state: int) -> Rng
  ```
  Interno: splitmix64 puro (`& 0xFFFFFFFFFFFFFFFF`), `float()` vía
  `(uint64() >> 11) * 2.0**-53`. Errores: `ValueError` en `below(n≤0)`,
  `integers(a>b)`, `sample(k > len)`, `choice(vacío)`. Prohibido `import random`,
  prohibido `hash()`.
- **Tests `src/tests/core/common/test_rng.py`:**
  1. Determinismo in-proceso: misma seed → mismas 100 primeras salidas.
  2. **Cross-proceso (CRITERIO DURO)**: lanza 2 subprocess con `PYTHONHASHSEED`
     DISTINTO (aleatorio explícito) + script `-c` que imprime primeros K valores
     para seed fija; ambos coinciden entre sí y con golden literals congelados.
  3. Estadístico ligero: `float()` ∈ [0,1) en 10k tiradas, media cercana a 0.5;
     `integers(1,6)` cubre todo el dominio en barrido de semillas.
  4. Sesgo: `below(n)` distribución aproximada (chi-cuadrado laxo o frecs.
     min/max) sobre 50k tiradas.
  5. `shuffle` pura (entrada no mutada) + permutación determinista.
  6. `fork("x")` ≠ padre pero reproducible; `fork` no depende del nº de tiradas
     previas del padre tras igualar estado (usando `from_state`).
  7. `state`/`from_state` ida-y-vuelta: secuencia continúa idéntica.
  8. Seeds `0`, negativas, `""` vacía, unicode: todas válidas y deterministas.
- **Hecho si:** esos tests pasan con `.venv/bin/python -m pytest
  src/tests/core/common/test_rng.py -q` desde `/home/juanma/CyberRoot`.

### H2 — SUB-AGENTE B: `events.py` + sus tests
- **Interfaz exacta en `src/core/common/events.py`:**
  ```python
  @dataclass(frozen=True)
  class Event:
      type: str            # contrato: NUNCA dicts opacos; type canónico str
      data: Mapping[str, Any] = field(default_factory=dict)   # snapshot dict(data)
      tick: int | None = None                                 # tiempo SIMULADO (§3: sin reloj real)

      def to_dict(self) -> dict        # ida-y-vuelta JSON-plano
      @classmethod from_dict(cls, d: Mapping) -> "Event"

  class EventBus:
      def subscribe(self, event_type: str | None, handler: Callable[[Event], None]) -> Callable[..., None]
          # event_type None = comodín (todos). Devuelve el handler (decorador usable).
      def unsubscribe(self, event_type: str | None, handler) -> bool  # idempotente (False si no estaba)
      def publish(self, event_or_type: Event | str, *, data: Mapping|None = None,
                  tick: int | None = None) -> Event
          # SINCRONO, FIFO por orden de suscripción; excepciones PROPAGAN;
          # devuelve el Event publicado. Guarda en history si está activada.
      def history(self, limit: int | None = None) -> tuple[Event, ...]
      def clear_history(self) -> None
  ```
  Constructor del bus: `EventBus(record_history: int | None = None)`.
  Constantes v0: clase `EventTypes` con `EXEC="event.exec"`,
  `NOISE="event.noise"`, `TEXT="event.text"` ⚠️ v0 — catálogo abierto (§5.2).
- **Tests `src/tests/core/common/test_events.py`:** FIFO estricto, comodín,
  desuscripción idempotente, excepción de handler propaga y NO rompe el bus,
  snapshot de `data` (mutar el dict original tras publish no altera el Event),
  roundtrip `to_dict/from_dict`, error `ValueError` si `type` vacío/no-str,
  determinismo de orden con múltiples subscriptores, history con maxlen recorta.
- **Hecho si:** tests verdes; cero dependencias de rng/types/errors internas
  (autonomía de fichero).

### H3 — SUB-AGENTE C: `types.py` + `errors.py` + tests
- **`src/core/common/errors.py`:** `CyberRootError(Exception)` base; hijas
  `InvalidCommandError`, `NotPlainDataError` (mensajes accionables).
- **`src/core/common/types.py`:**
  ```python
  SeedLike = int | str | bytes          # type alias documentado
  TextKey = str                          # claves de texto que core entrega (§3), doc-only alias
  
  @dataclass(frozen=True)
  class Command:
      cmd: str
      args: Mapping[str, Any] = field(default_factory=dict)
      # validate en __post_init__: cmd str no vacío; keys str
      def to_dict(self) -> dict          # {"cmd": ..., **args}  (contrato plano §1.2)
      @classmethod from_dict(cls, d: Mapping) -> "Command"   # InvalidCommandError ante basura
  
  def ensure_plain(obj: Any, *, _depth: int = 0) -> None    # lanza NotPlainDataError si no es JSON-plano
      # permitido: None|bool|int|float|str|list|tuple→lista? NO: tuple NO permitido (JSON plano estricto)
      # dict con keys str; recursión máx. profundidad 64; anti-ciclos por profundidad.
  ```
- **Tests `src/tests/core/common/test_types.py`:** roundtrip Command
  idéntico byte-a-byte (json.dumps comparado), errores de from_dict (no-dict,
  sin "cmd", cmd no-str/vacío, keys no-str), ensure_plain acepta
  scalars/list/dict anidado y rechaza tuple/set/object()/ciclo profundo,
  mensaje de error contiene la ruta del fallo (p.ej. `args.argv[2]`).
- **Hecho si:** tests verdes; sin imports fuera de stdlib.

### H4 — MÍO: Tests de arquitectura + integración final (~45 min)
- `src/tests/architecture/test_core_no_pyxel.py`: escanea `*.py` bajo
  `src/core/`; falla si aparece `import pyxel` / `from pyxel` (comentarios
  excluidos con heurística de strip simple).
- `src/tests/architecture/test_core_stdlib_only.py`: `src/core/**` no debe
  importar paquetes externos (whitelist stdlib — dumb scanner con `ast`).
- `src/tests/architecture/test_random_global_prohibido.py`: ningún fichero de
  `src/core/` usa `import random`/`from random` (ni siquiera `common/rng.py` —
  ahí lo escaneamos igual: splitmix64 no lo necesita).
- Export público limpio en `src/core/common/__init__.py` (re-export API + `__all__`).
- Suite COMPLETA desde raíz verde, medir tiempo (< 5 s objetivo Fase 1).
- Repaso anti-colisión: nada tocado fuera de `src/core/common/`, `src/core/__init__.py`,
  `src/tests/`, `pyproject.toml`.

### H5 — MÍO: Documentación + huella + PR (~30 min)
- `src/core/common/README.md`: API, decisiones (splitmix64, sha256-seeds,
  bus síncrono), cómo correr tests, qué NO vive aquí.
- Worklog del día (QUÉ/POR QUÉ/ENTREGABLE/RELEVO + este plan resumido).
- Marcar `[HECHO]` + nº PR en mi línea de `activo.md` (en ESTA rama).
- Commit final + push + `gh pr create` → main (mergea Gwyn; revisa Artorias).

## 2. Edge cases recogidos (checklist transversal)
- RNG: seed `0`/negativa/vacía/unicode/bytes; `below(1)`; `integers(x,x)`;
  secuencias vacías en choice/sample → error claro; sesión larga sin drift.
- Events: datos mutados después de publicar; orden FIFO; doble subscribe igual
  handler (dispara DOS veces — documentado); publish de Event vs (str,data).
- Types: `to_dict` con args colisionando con clave `"cmd"` → se sobreescribe y
  from_dict lo respalda como arg? DECISIÓN: `Command.to_dict` pone args DESPUÉS
  (args mandan); from_dict rechaza `{"cmd": ..., "cmd"}` duplicados (json ya lo
  impide). Documentado en docstring.
- Cross-process: hacerlo con `PYTHONHASHSEED=random` explícito para demostrar
  que no dependemos del hash aleatorizado.

## 3. Fuera de alcance HOY (explícito)
- Aserciones de rendimiento; persistencia real (eso es `state/`, Seath);
  tipos de dominio (salas, nodos) — viven en `generator/engine`;
  cualquier fichero de Smough o Seath. NADA en `src/data/`.
