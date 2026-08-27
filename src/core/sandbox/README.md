# sandbox/ — El Linux de mentira que dice verdades

> **Qué hace:** filesystem virtual + shell con semántica REAL de Linux
> (GNU/coreutils). Todo lo que el jugador escribe pasa por aquí. No sabe que
> existen partidas, salas ni Pyxel — es autónomo y reutilizable
> (ARCHITECTURE §2.2). **Estado v0 (27/08, Smough):** comandos del cap. 0
> (`ls`, `cd`, `cat`) + `cp` implementado a la espera de 🧭1.

## Piezas (v0)

| Fichero | Qué hay |
|---|---|
| `fs.py` | `FileNode`/`DirNode` (owner, group, mode, mtime SIMULADO), `FileSystem` (resolve/change_dir/read_file/list_dir/copy_file), `FsError` con kinds estructurados, `to_dict`/`from_dict` ida-y-vuelta EXACTO + `snapshot()` |
| `shell.py` | Sesión serializable: parser `shlex` POSIX, registro de specs, cwd/tick/historial simulados, `DEFAULT_CAP0_COMMANDS = ("cat","cd","ls")` |
| `commands/base.py` | `CommandResult` (stdout/stderr byte a byte, exit, noise, new_cwd), `CommandSpec` (concepts → pools del generador §6.4.2), `CommandRegistry` |
| `commands/navigation.py` | `ls` (columna única, orden codepoint), `cd` (builtin: valida→normaliza, errores antes de tocar cwd) |
| `commands/files.py` | `cat` (bytes exactos, exit 1 si cualquier error), `cp` (sobrescribe, copia-DENTRO de dirs, `same_file`) |
| `noise.py` | Perfil ⚠️ v1 `cd:0, ls:1, cat:1, cp:3` + eventos forma `Event` (`type="event.noise"`); el coste de detección lo decide el ENGINE |
| `PLAN.md` | Decisiones de diseño e hitos del turno 27/08 |

## Decisiones que un revisor debe conocer

1. **`ls` estilo `ls -1` (columna, orden codepoint):** es lo que imprime GNU
   `ls` a un pipe, y nuestra salida va a string. Verificado contra
   coreutils real (Ubuntu 24.08, 27/08): sin cabecera con UN operando;
   multi-operando = ficheros primero + bloques `dir:` con UNA línea en
   blanco entre grupos; errores `ls: cannot access 'x': ...` (exit 2);
   `ls fichero/` → «Not a directory»; operando-fichero se imprime TAL CUAL.
2. **Mensajes GNU en inglés** (DESIGN §2.6.8: si el sistema real emite
   inglés, se emite inglés) con exit codes reales: ls=2, cat=1, cd=1,
   desconocido=127 (`sh: command not found:`), sintaxis futura=2.
3. **`cp fichero dir_existente/` copia DENTRO** (GNU real), no error. Colisión
   dir→`is_a_directory`; `cp f f`→`same_file` («are the same file»); `cp /a
   /a/b`→`invalid_argument`. mtime_dst = mtime_src (no hay reloj real).
4. **Pipes/globs/redirección RECHAZADOS v0** con `sh: syntax not supported in
   this session` (exit 2) — salen en caps. 1–2. Entre comillas son
   literales reales (`cat "a*b.txt"` funciona como nombre literal).
5. **`cp` FUERA del set del cap. 0** hasta que Gwyn decida 🧭1. La spec y sus
   tests ya existen: activarlo = añadir `"cp"` a `DEFAULT_CAP0_COMMANDS`.
6. **Cero RNG** (determinismo puro §2.2): la piel aleatoria la instancia el
   generador; el sandbox solo ejecuta. Iteraciones SIEMPRE ordenadas por
   codepoint → salida byte a byte reproducible entre procesos (demostrado en
   `test_session_cap0.py` con PYTHONHASHSEED distintos).
7. **Eventos de ruido con forma de `common.events.Event`** (dicts planos
   mientras PR #1 de Ornstein no esté mergeada; canje = importación).
8. **`fs.change_dir` solo normaliza strings**; la validación de existencia es
   del comando `cd` (get_dir antes de mover) — separación limpia de capas.

## Cómo se testea

- `./.venv/bin/python -m pytest` desde la raíz (suite completa, 91+ tests).
- **Golden tests por comando** (stdout/stderr/exit byte a byte) en
  `src/tests/core/sandbox/test_commands.py`.
- **Sesión end-to-end del cap. 0** (escena de `CAPITULOS/00-la-firma.md`:
  `ls` → `cat` → `cd ..` + gancho `cp` a `/usb/`) en
  `test_session_cap0.py`, con reproducibilidad cross-proceso.
- Regla del módulo: si un comando no se comporta como Linux real, ES un bug
  (fantasía = competencia real, DESIGN §8.4). Los desvíos se detectaron
  contrastando con coreutils real, no de memoria.

## Qué falta (roadbox del módulo)

- Permisos aplicados de verdad (hoy `mode/owner` viajan y se copian, pero no
  se aplican: llega con cap. 1, familia permisos).
- Familias restantes (texto/pipes, procesos, red, auditoría, escalada) — un
  módulo por familia en `commands/`.
- Globbing/pipes/redirección (caps. 1–2), stdin virtual para `cat` sin args.
- Red simulada mínima (cap. 4+): nodos ssh/scp/ss, sin sockets reales jamás.

## Dueño

Smough (`feat/sandbox`). Toques desde otras ramas = tarea para Smough.
