# PLAN.md — Sandbox mínimo cap. 0 (Smough, 27/08)

> Mi plan de implementación para la Tarea B de Gwyndolin
> (`backlog/planes/2026/08/27.md` §3-B). El QUÉ lo da ella; el CÓMO en detalle
> es este documento. Normativa dura: `src/core/ARCHITECTURE.md` §2.2,
> `docs/DESIGN.md` §2.6.8 (salidas técnicas en inglés real), §4.5 (RNG jamás
> decide la semántica), README del módulo.

## Decisiones previas (mías, con motivo)

1. **`cp` implementado y testeado, NO registrado en el set del cap. 0.**
   🧭1 (cp como 4.º concepto) la decide Gwyn esta noche. Implementarlo cuesta
   poco y deja la aprobación como cambio de UNA línea. Si Gwyn rechaza, no
   estorba: es código del módulo navega/ficheros con tests, reusable en cap. 1
   (§6.2 lo asigna ahí de todos modos).
2. **`ls` imprime una columna (estilo `ls -1` real, orden codepoint).** En
   Linux real `ls` imprime una columna cuando su salida no es un TTY (pipe);
   la nuestra va a string → contexto pipe. La escena de Manus en
   `CAPITULOS/00-la-firma.md` es prosa narrativa, no contrato de bytes.
3. **Códigos de salida y stderr REALES (GNU/coreutils), en inglés** (§2.6.8):
   - `ls` fallo → `ls: cannot access 'x': No such file or directory`, exit 2.
   - `cat` fallo → `cat: x: No such file or directory`, exit 1.
   - `cd` fallo → `cd: x: No such file or directory`, exit 1 (builtin).
   - comando desconocido → `sh: command not found: X`, exit 127.
   - pipes/globs/redirección → `sh: syntax not supported in this session`
     (salen en caps. 1–2), exit 2.
4. **Ruido por acción con forma de `common.events.Event`** (dict
   `{type, data, tick}` con `type="event.noise"`): Ornstein lo definió así en
   `feat/engine` (PR #1, aún no mergeada). Viajo con dicts planos y el canje
   tras merge es una importación. El coste de detección lo decide el ENGINE:
   yo solo emito cantidad (constantes ⚠️ v1 en `noise.py`, calibrables).
5. **Cero RNG en sandbox** (determinismo puro §2.2). La piel aleatoria la
   instancia el generador; el sandbox solo ejecuta. Prohibido `random`,
   `pyxel`, subprocesos, reloj real. Iteraciones SIEMPRE sobre secuencias
   ordenadas (nada de iterar sets: orden no determinista entre procesos).

## Estructura de datos (contratos)

- `fs.FileNode`: dataclass — `name, content: str, owner="root", group="root",
  mode="644", mtime: int=0` (mtime = tiempo SIMULADO).
- `fs.DirNode`: dataclass — `name, children: dict[str, Node], owner, group,
  mode="755", mtime`.
- `fs.FsError(Exception)`: `.kind ∈ {not_found, not_a_directory,
  is_a_directory, permission_denied, not_empty}` + `.path`. Los comandos mapean
  kind → mensaje GNU + exit code (no hay jerarquía de clases: un tipo de error,
  datos estructurados).
- `fs.FileSystem`: `resolve(path, cwd) -> Node`, `list_dir`, `read_file`,
  `change_dir(path, cwd) -> str`, `copy_file(src, dst, cwd)` (resuelto `..`,
  `.`, `//`, barra final; rutas absolutas y relativas), `to_dict()/from_dict()`
  ida-y-vuelta EXACTO (ARCHITECTURE §1.5), `snapshot()` (copia profunda vía
  dict). La raíz es un `DirNode(name="/")`. Sin symlinks v0.
- `noise.NoiseProfile`: constantes ⚠️ v1 — `cd: 0, ls: 1, cat: 1, cp: 3`.
- `noise.NoiseMeter`: acumulador + `emit(command, argv, tick) -> dict` con
  forma Event (`type="event.noise"`, `data={command, amount, argv}`).
- `commands.base.CommandResult`: dataclass frozen — `stdout: str, stderr: str,
  exit_code: int, noise: tuple[dict, ...]`. `stdout` lleva EXACTAMENTE los
  bytes impresos (newlines incluidos) → reproducibilidad byte a byte.
- `commands.base.CommandSpec`: dataclass frozen — `name, handler, concepts:
  frozenset[str], noise: int`. Los `concepts` alimentarán los pools del
  generador (§6.4.2); se declaran, no se usan aquí.
- `shell.Shell(fs, *, user="operator", host, cwd, tick=0, commands=DEFAULT)`:
  `execute(line) -> CommandResult`; parser `shlex.split(posix=True)`; registra
  historial; avanza `tick` simulado; muta cwd/FS. `to_dict()/from_dict()`
  completa la sesión (fs + cwd + user + tick + historial).
  `DEFAULT_CAP0_COMMANDS = ("cat", "cd", "ls")` — `cp` queda fuera hasta
  decisión 🧭1.

## Hitos (cada uno con su "hecho")

- **H0 — Esqueleto (yo):** PLAN.md (esto), `pyproject.toml` raíz copiado
  BYTE A BYTE de `feat/engine` (evita conflicto add/add con Ornstein en
  merge), `__init__.py` de paquete y tests, smoke test.
  ✓ = `.venv/bin/python -m pytest` verde desde raíz.
- **H1 — `fs.py` + tests (SUB-AGENTE A):** nodos, FileSystem completo,
  errores, roundtrip dict, snapshot. Tests: resolución (absoluta/relativa/`..`/
  `.`//colapsada/trailing slash), errores (not_found/not_a_directory/
  is_a_directory), permisos (`permission_denied` ante `r--` ajeno),
  copy_file (destino existente dir → error; dentro de sí mismo → error),
  to_dict→from_dict→to_dict idéntico.
  ✓ = `pytest src/tests/core/sandbox/test_fs.py` verde. **VERIFICO leyendo el
  fichero y corriendo los tests yo mismo.**
- **H1b — `noise.py` + tests (YO, en paralelo con A):** perfil de constantes,
  meter, forma Event.
  ✓ = `pytest src/tests/core/sandbox/test_noise.py` verde.
- **H2 — comandos (SUB-AGENTE B, tras verificar H1):** `commands/base.py`,
  `commands/navigation.py` (`ls`, `cd`), `commands/files.py` (`cat`, `cp`).
  Golden tests por comando (stdout/stderr/exit byte a byte) contra un FS
  fixture. `cp` testeado igual que los demás aunque no esté en el set del
  cap. 0.
  ✓ = `pytest src/tests/core/sandbox/` verde entero. **VERIFICO yo.**
- **H3 — `shell.py` + tests (YO):** parser shlex, registro por nombre, 127,
  rechazo de pipes/globs/redirección, historial, tick, to_dict/from_dict.
  ✓ = `test_shell.py` verde (incluye quoting: `cat "mi fichero.txt"`).
- **H4 — sesión end-to-end cap. 0 (YO):** fixture del FS de la escena
  (oficina-vecinal-muelle-norte: `nombre_de_proveedor.txt`, `log.txt`,
  `README`) + secuencia de la escena (`ls` → `cat` → `cd ..`) → dump byte a
  byte; mismo script en DOS procesos con PYTHONHASHSEED distintos → idéntico;
  sesión con `cp` disponible → extracción del fichero (gancho 🧭1).
  ✓ = `test_session_cap0.py` verde, reproducibilidad demostrada por mí.
- **H5 — README del módulo (YO):** decisiones 1–5, códigos exit, formato
  `ls`, estado 🧭1, cómo instanciará salas el generador.
- **H6 — huella (YO):** `[HECHO]`+PR en `activo.md`, worklog, commit como
  Smough, push, `gh pr create`.

## Qué NO toco (anti-colisión)

- `src/core/common/` (Ornstein, PR #1 abierta), `src/tests/architecture/`
  (sus guardianes ya cubren todo `core/`; no duplico ficheros homónimos),
  `src/core/{generator,engine}`, `src/assets`, docs de historia.
- `pyproject.toml` raíz: SOLO copia exacta de la de Ornstein (mismo contenido
  = merge limpio).

## Delegación

Sub-agentes flash: A (H1-fs) y B (H2-comandos), SERIALES (B programa contra
la API real de H1, no contra mi spec). Verificación de cada uno: leo el
código completo + corro los tests yo mismo (regla de la casa: no fiarse del
resumen). H1b/H3/H4/H5/H6 son mías (transversales o pequeñas).
