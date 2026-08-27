# common/ — Cimientos del core (dueño: Ornstein)

> Normativa: `../ARCHITECTURE.md` §2.1 y §3. Este paquete es la base de la
> cadena de dependencias del core: **todo lo demás importa de aquí; aquí no
> se importa nada del core salvo stdlib.** Sin lógica de juego.
> Plan de implementación seguido: [`PLAN.md`](PLAN.md).

## Contenido

| Fichero | Qué aporta | API principal |
|---|---|---|
| `rng.py` | RNG determinista seedeada | `Rng(seed)` · `.uint64() .below(n) .integers(a,b) .float() .choice() .shuffle() .sample(seq,k) .fork(label)` · `.state` / `from_state()` · `mix_seeds(a, b)` |
| `events.py` | Bus de eventos pub/sub síncrono | `Event(type, data, tick)` frozen + `to_dict/from_dict` · `EventBus(record_history)` · `.subscribe/.unsubscribe/.publish/.history` · `EventTypes` (catálogo v0 ABIERTO) |
| `types.py` | Tipos base e invariantes | `Command(cmd, args)` frozen + `to_dict/from_dict` · `SeedLike` · `TextKey` · `ensure_plain(obj)` |
| `errors.py` | Jerarquía de errores de dominio | `CyberRootError` → `InvalidCommandError`, `NotPlainDataError` |

## Decisiones de diseño (y por qué)

1. **splitmix64 propio en vez de `random.Random`**: aritmética entera exacta ⇒
   secuencia idéntica ante la misma seed entre procesos, plataformas y
   versiones de CPython (verificado: mismo output con `PYTHONHASHSEED=1`,
   `999999` y `random`, sobre Python 3.11 y 3.12). Estado serializable como
   UN entero (`Rng.state` ↔ `Rng.from_state`): save/load trivial para `state/`.
2. **Semillas no-enteras vía `sha256`**, jamás vía builtin `hash()`:
   `hash(str)` varía entre procesos (PYTHONHASHSEED).
3. **Sin sesgo**: `below()/integers()/sample()` usan rechazo/partial-Fisher-Yates,
   no módulos directos sobre la palabra completa.
4. **`Event` frozen con snapshot de datos**: mutar el dict original tras
   publicar no altera el evento ya publicado ni su historial.
5. **Bus síncrono FIFO, fail-fast**: las excepciones de handlers propagan
   (fase dev); sin hilos. El comodín (`subscribe(None, h)`) es un registro
   separado del específico. Suscribir el mismo handler dos veces dispara DOS
   veces (intencional, documentado).
6. **`Command` plano `{"cmd": ..., ...}`** (contrato §1.2 ARCHITECTURE):
   `"cmd"` es clave reservada — prohibida como arg — para que
   `from_dict(to_dict(c)) == c` sin ambigüedad.
7. **`ensure_plain`** valida JSON-plano estricto (sin tuples/sets/bytes/NaN/
   claves no-str, profundidad ≤ 64 anti-ciclos) informando la RUTA exacta del
   fallo. Reutilizable por `state/` (Seath) antes de serializar saves.
8. **Catálogo de tipos de evento v0 abierto** (§5.2 ARCHITECTURE): la decisión
   final se cierra cuando render y harness lo consuman por primera vez.

## Cómo correr los tests

```bash
# desde la raíz del repo
./.venv/bin/python -m pytest                 # suite completa (~105 tests, <1 s)
./.venv/bin/python -m pytest src/tests/core/common/test_rng.py -q   # solo RNG

# reproducibilidad cross-proceso a mano (debe imprimir lo mismo siempre):
PYTHONPATH=src PYTHONHASHSEED=cualquier-cosa ./.venv/bin/python -c \
  "from core.common.rng import Rng; print([Rng('cap-0').uint64() for _ in range(3)])"
```

Los tests estadísticos (sesgo, media) usan seeds FIJAS ⇒ deterministas; sus
márgenes medidos corren holgados (p. ej. desvío máx. 1,8% vs tolerancia 5%).

## Qué NO vive aquí

Nada de salas, runs, economía o conceptos de juego (eso es `generator/engine`);
nada de serialización de partida (`state/`); nada de texto visible — el core
solo maneja claves (`TextKey`), el render las resuelve contra `data/`.

## Guardianes de arquitectura que me protegen

`src/tests/architecture/`: core sin `pyxel` (AST), core stdlib-only (AST),
core sin `random` global (AST). Todos verificados en negativo: detectan
violaciones reales apuntando fichero:línea. Cambiarlos exige propuesta en
`backlog/mejoras/pendiente/`.
