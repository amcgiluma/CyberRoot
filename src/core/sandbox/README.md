# sandbox/ — El Linux de mentira que dice verdades

> **Qué hace:** filesystem virtual + shell con semántica REAL de Linux
> (GNU/coreutils). Todo lo que el jugador escribe pasa por aquí. No sabe que
> existen partidas, salas ni Pyxel — es autónomo y reutilizable
> (ARCHITECTURE §2.2). **Estado (30/08, Smough):** comandos del cap. 0
> (`ls`, `cd`, `cat`, `cp`) + cap. 2 (`grep`, `wc`) y tubería `cmd1 | cmd2`

## Piezas (v0)

| Fichero | Qué hay |
|---|---|
| `fs.py` | `FileNode`/`DirNode` (owner, group, mode, mtime SIMULADO), `FileSystem` (resolve/change_dir/read_file/list_dir/copy_file), `FsError` con kinds estructurados, `to_dict`/`from_dict` ida-y-vuelta EXACTO + `snapshot()` |
| `shell.py` | Sesión serializable: parser `shlex` POSIX, registro de specs, cwd/tick/historial simulados, `DEFAULT_CAP0_COMMANDS = ("cat","cd","cp","ls")` y `DEFAULT_CH2_COMMANDS` (+`grep`,`wc`; S1 30/08), tubería `cmd1 | cmd2` (stdout→stdin), rechazo didáctico de sintaxis futura (encadenado/redirección/globs) |
| `commands/base.py` | `CommandResult` (stdout/stderr byte a byte, exit, noise, new_cwd), `CommandSpec` (concepts → pools del generador §6.4.2), `CommandRegistry` |
| `commands/navigation.py` | `ls` (columna única, orden codepoint), `cd` (builtin: valida→normaliza, errores antes de tocar cwd) |
| `commands/files.py` | `cat` (bytes exactos, exit 1 si cualquier error), `cp` (sobrescribe, copia-DENTRO de dirs, `same_file`) |
| `commands/texto.py` | `grep` (patrón, fichero o stdin de tubería) y `wc` (`-l`/`-c`; **S1, 30/08** — cap. 2) |
| `noise.py` | Perfil ⚠️ v1 `cd:0, ls:1, cat:1, cp:3, grep:2, wc:1` + eventos `common.events.Event` REALES (`type="event.noise"`); el coste de detección lo decide el ENGINE |
| `__main__.py` | **REPL (S2, 29/08):** `PYTHONPATH=src python -m core.sandbox` abre una sesión real del cap. 0 con prompt diegético (`operador@oficina-vecinal:~$`, DESIGN §6.1); `run_repl` reutilizable y testeable programáticamente |
| `PLAN.md` | Decisiones de diseño e hitos del turno 27/08 |
| `PLAN-2026-08-30.md` | Plan de implementación S1+S2 del turno 30/08 (pipes+grep/wc, currículo cap. 2) |

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
4. **Pipes (S1, 30/08):** el cap. 2 pide UNA tubería `cmd1 | cmd2` — soportada.
   El stdout de `cmd1` alimenta el stdin de `cmd2`; la tubería NO es gratis:
   AMBOS comandos facturan su ruido en `history` (AC S1). `&&`/`;`/`>`/globs
   siguen rechazados con el mensaje didáctico reformulado (los pipes YA
   están; lo que falta es encadenado, redirección y globs). Más de un `|`
   (`a | b | c`) → mensaje didáctico propio, exit 2. Entre comillas `|` es
   literal (`cat "a|b"` es un nombre válido, como `&`/`;`). `grep`/`wc`
   leen de `stdin` cuando no reciben fichero.
5. **`cp` EN el set del cap. 0** desde el 27/08 (🧭1 APROBADA por Gwyn:
   copiar ES el objetivo del primer encargo). El perfil de ruido y los tests
   lo cubren desde ese día.
6. **Cero RNG** (determinismo puro §2.2): la piel aleatoria la instancia el
   generador; el sandbox solo ejecuta. Iteraciones SIEMPRE ordenadas por
   codepoint → salida byte a byte reproducible entre procesos (demostrado en
   `test_session_cap0.py` con PYTHONHASHSEED distintos).
7. **Los eventos de ruido SON `common.events.Event`** (canje S1 del 28/08,
   deuda del 27/08 saldada tras mergearse PR #1: `NoiseMeter.emit` construye
   la clase real y `CommandResult` serializa vía `Event.to_dict()`/`from_dict()`
   — el JSON plano queda byte-idéntico al puente de dicts anterior).
8. **`fs.change_dir` solo normaliza strings**; la validación de existencia es
   del comando `cd` (get_dir antes de mover) — separación limpia de capas.
9. **GNU-honesto en `cat`/`cp` (pasada S1 del 29/08, cierra los 2 `[BUG]` de
   Havel):** `cat fichero/` → `cat: X/: Not a directory` exit 1 (una barra
   final fuerza a tratar el operando como ruta-a-directorio; GNU contrastado
   en la máquina); `cp dir destino` sin `-r` → `cp: -r not specified; omitting
   directory 'dir'` exit 1 diagnosticando el ORIGEN, no el destino. `mtime` de
   `cp` sin `-p` queda como limitación deliberada (se preserva, GNU lo
   actualiza).

## Cómo se testea

- `./.venv/bin/python -m pytest` desde la raíz (suite completa; 247 passed
  tras el turno del 28/08: S1+S3+S2 de Smough incluidos).
- **Golden tests por comando** (stdout/stderr/exit byte a byte) en
  `src/tests/core/sandbox/test_commands.py`.
- **Sesión end-to-end del cap. 0** (escena de `CAPITULOS/00-la-firma.md`:
  `ls` → `cat` → `cd ..` + gancho `cp` a `/usb/`) en
  `test_session_cap0.py`, con reproducibilidad cross-proceso.
- **REPL** (`test_repl.py`, S2 29/08): smoke del bucle de `__main__` sin TTY
  (`run_repl` con iterable de líneas + captura por canal); la secuencia
  canónica del dossier y los errores (127, rechazo `&&`) salen idénticos a la
  sesión testeada.
- **Sesión del cap. 2** (`test_session_ch2.py`, S1 30/08): la línea EXACTA
  `grep 11:04 centralita/turnos/turno.log | wc -l` → `2` (golden contra GNU
  real), con el FS extendido del cap. 2; la tubería factura grep(2)+wc(1).
- **Golden de `grep`/`wc`** (`test_texto.py`, S1 30/08): casos de borde
  aislados (sin match, fichero inexistente con el mensaje que cita la prosa
  del post-mortem, stdin, `wc` con/sin flags) verificados contra GNU real.
- Regla del módulo: si un comando no se comporta como Linux real, ES un bug
  (fantasía = competencia real, DESIGN §8.4). Los desvíos se detectaron
  contrastando con coreutils real, no de memoria.

## Qué falta (roadbox del módulo)

- Permisos aplicados de verdad (hoy `mode/owner` viajan y se copian, pero no
  se aplican: llega con cap. 1, familia permisos).
- Familias restantes (procesos, red, auditoría, escalada) — un módulo por
  familia en `commands/`. `texto` ya cubre grep/wc (S1).
- Redirección `>` y encadenado `&&`/`;` (caps. 2–3; hoy rechazo didáctico).
  El cap. 2 de Manus menciona `sort`/`uniq -c`/`>` que aún no existen en el
  sandbox: cuando entren, el bloque de terminal del cap. 2 se verificará byte
  a byte contra `test_session_ch2.py`.
- stdin virtual para `cat` sin args (hoy error didáctico).
- Red simulada mínima (cap. 4+): nodos ssh/scp/ss, sin sockets reales jamás.

## Dueño

Smough (`feat/sandbox`). Toques desde otras ramas = tarea para Smough.
