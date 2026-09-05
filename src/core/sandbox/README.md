# sandbox/ — El Linux de mentira que dice verdades

> **Qué hace:** filesystem virtual + shell con semántica REAL de Linux
> (ARCHITECTURE §2.2), autónomo y reutilizable, sin I/O ni reloj real.<br>
> **Estado (05/09, Smough):** comandos del cap. 0 (`ls`, `cd`, `cat`,
> `cp`) + cap. 2 (`grep`, `wc`) y tubería `cmd1 | cmd2` + cap. 3 (`ps`, `env`
> — familia procesos; `sudo` GANADO + `kill` Señales v0) + familia conteo
> (`head`/`tail`/`sort`/`uniq`/`cut`, cap. 6 — lectura frugal, la Lista es tabla cortable).

## Piezas (v0)

| Fichero | Qué hay |
|---|---|
| `fs.py` | `FileNode`/`DirNode` (owner, group, mode, mtime SIMULADO), `FileSystem` (resolve/change_dir/read_file/list_dir/copy_file + `abspath` canónica pura S1 03/09), `FsError` con kinds estructurados, `to_dict`/`from_dict` ida-y-vuelta EXACTO + `snapshot()` |
| `shell.py` | Sesión serializable: parser `shlex` POSIX, registro de specs, cwd/tick/historial simulados, `DEFAULT_CAP0_COMMANDS` / `DEFAULT_CH2_COMMANDS` (+grep,wc) / `DEFAULT_CH3_COMMANDS` (+ps,env,sudo,kill S1 02/09) / `DEFAULT_CH6_COMMANDS` (+head,tail,sort,uniq,cut S2→S1 04/09), tubería `cmd1 | cmd2` (stdout→stdin), rechazo didáctico de sintaxis futura. **S1, 03/09** 🧭14b: `read_marks` (credenciales LEÍDAS con `cat`, viajan en `to_dict`) + bus de sesión (`event.credential.read` en la transición) + gate de lectura en `_exec_sudo` |
| `commands/base.py` | `CommandResult` (stdout/stderr byte a byte, exit, noise, new_cwd), `CommandSpec` (concepts → pools del generador §6.4.2), `CommandRegistry` |
| `commands/navigation.py` | `ls` (columna única, orden codepoint), `cd` (builtin: valida→normaliza, errores antes de tocar cwd) |
| `commands/files.py` | `cat` (bytes exactos, exit 1 si cualquier error), `cp` (sobrescribe, copia-DENTRO de dirs, `same_file`) |
| `commands/texto.py` | `grep` (patrón, fichero o stdin de tubería) y `wc` (`-l`/`-c`; **S1, 30/08** — cap. 2) |
| `commands/procesos.py` | `ps` (`ps aux` con columna USER) y `env` (solo-lectura, orden por clave; **S1, 31/08** — cap. 3) |
| `commands/senal.py` | `kill` (**S1, 02/09**): `kill [-9|-HUP] <pid>…` sobre `fs.processes` (par ceniza-521/censo-522). `-9`/`TERM` mata (elimina), `-HUP` reinicia (`--reloaded`, `HUP_<pid>=1`, visible en `ps`/`env`). Emite `sandbox.signal` + ruido 2. Golden GNU y gate 127 en cap. 0/2. |
| `commands/escalada.py` | `sudo` GANADO (**S1, 01/09** + gate de LECTURA **S1, 03/09** 🧭14b): wrapper de orquestación del shell que arbitra la CREDENCIAL narrativa (fichero del mundo, contrato O1↔S1); sin credencial → rechazo diegético accionable (ruido 0, exit 1); credencial SIN LEER → rechazo que NOMBRA la orden (`SUDO_UNREAD_MSG`, ruido 0, sin firma); credencial LEÍDA (`cat` en la sesión) → eleva + ruido premium + firma en `/var/log/auth.log`. Constantes del contrato (`SUDO_CREDENTIAL_PATH`, `AUTH_LOG_PATH`, `SUDO_AUTHZ_MARKER`, `SUDO_PREMIUM_NOISE`, `SUDO_READ_EVENT_TYPE`). |
| `commands/conteo.py` | Familia conteo (**S1, 05/09**: `sort -k`/`-t`/`-n` lectura VERTICAL — `sort -t'|' -k12 -n` ordena la Lista por puntuación; **S2, 01/09**: `head`/`tail`/`sort`/`uniq`) `head`/`tail` (`-n N` default 10), `sort` (`-u`/`-n`/`-t SEP`/`-k KEYDEF`/`-r`, delim `|` incluido, fallback vacío sin crashear), `uniq` (`-c` ancho 7). «Lectura frugal»: leen menos que un `cat` entero. GNU honesto contrastado (multi-char tab, `-k0`, sin `-k` byte-idéntico). Cap. 6. |
| `commands/cut.py` | `cut` (**S1, 04/09** — la Lista es tabla cortable): `cut -d DELIM -f LIST [FILE...]` GNU-honesto (`-d` delim single-char, `-f` rangos `N`, `N-M`, `N-`, `-M`, coma-separado, ordenado+deduplicado, línea sin delim imprime entera, sin `-f` → error GNU, stdin/tubería, multi-fichero). Ruido 1. Gate 127 en cap. 0/2/3. |
| `noise.py` | Perfil ⚠️ v1 `cd:0, ls:1, cat:1, cp:3, grep:2, wc:1, ps:1, env:1, sudo:3, head:1, tail:1, sort:2, uniq:1, kill:2, cut:1` + eventos `common.events.Event` REALES (`type="event.noise"`); el coste de detección lo decide el ENGINE |
| `__main__.py` | **REPL (S2, 29/08):** `PYTHONPATH=src python -m core.sandbox` abre una sesión real del cap. 0 con prompt diegético (`operador@oficina-vecinal:~$`, DESIGN §6.1); `run_repl` reutilizable y testeable programáticamente |
| `PLAN.md` | Decisiones de diseño e hitos del turno 27/08 |
| `PLAN-2026-08-30.md` | Plan de implementación S1+S2 del turno 30/08 (pipes+grep/wc, currículo cap. 2) |
| `PLAN-2026-08-31.md` | Plan de implementación S1+S2 del turno 31/08 (ps/env, currículo cap. 3) |
| `PLAN-2026-09-01.md` | Plan de implementación S1+S2 del turno 01/09 (sudo GANADO + familia conteo, currículo + contrato O1↔S1) |
| `PLAN-2026-09-02.md` | Plan de implementación S1+S2 del turno 02/09 (kill/señales v0 + quest ch6.e1 + DEFAULT_CH6_COMMANDS, contrato O3↔S2) |
| `PLAN-2026-09-04.md` | Plan de implementación S1 del turno 04/09 (cut S1 — la Lista es tabla cortable, gate 22/22) |
| `PLAN-2026-09-05.md` | Plan de implementación S1 del turno 05/09 (sort -k/-t/-n — lectura VERTICAL de la Lista, `sort -t'|' -k12 -n`) |

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
10. **`sudo` es un WRAPPER del shell, no una spec (S1, 01/09):** necesita el
    registry de la sesión para despachar el comando envuelto, igual que las
    tuberías se orquestan en `execute`. No está en `SPECS_ALL`; se intercepta
    en `_exec_argv` solo si `available_commands` lo expone (cap. 3 nada más).
    Su ruido es PREMIUM (extra sobre el base del envuelto). La credencial es
    un FICHERO del mundo (contrato O1↔S1), NO una contraseña; si las rutas
    `SUDO_CREDENTIAL_PATH`/`AUTH_LOG_PATH` cambian, cambian A LA VEZ en la
    rama de Ornstein (`feat/engine`, chapter3.py) y en la mía.
12. **`kill` v0 (S1, 02/09):** `kill [-9|-HUP] <pid>` sobre `fs.processes` (par 521/522). Default SIGTERM (15) mata; `-9` (KILL) mata; `-HUP` (1) reinicia: mantiene PID, `cmd += " --reloaded"` (stat S→R) y `env["HUP_<pid>"]="1"`. Señales vía `-s NAME` también. Múltiples pids en una línea (GNU: procesa todos, exit 1 si alguno falló). Evento `sandbox.signal` por cada pid exitoso (`{pid, signal, signal_num, amount:0}`) para karma/escenas. Golden: `kill: (PID) - No such process` exit 1; `kill: invalid signal` exit 1; sin args → not enough arguments exit 1; cap. 0/2 → exit 127 (no existe hasta cap. 3/6).

11. **Familia conteo (S2, 01/09):** `uniq -c` usa ancho 7 derecha-alineado
    (GNU real); `uniq` NO ordena (solo adyacentes); `sort` ordena por byte
    (LC_ALL=C, determinismo §5). Errores GNU honestos: `head`/`tail`/`uniq`
    fichero ausente → exit 1; `sort` → exit 2; `uniq` reporta DISTINTO que
    head/tail (sin «cannot open»).

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
- **Golden de `kill`** (`test_kill.py` + `test_session_kill.py`, S1 02/09): `kill` sin args / pid inexistente / señal inválida (golden GNU), `-9` vs `-HUP` observables en `ps`/`env` (mata vs reinicia), múltiples pids, evento `sandbox.signal`, ruido 2, gate 127 en cap. 0/2, roundtrip conserva mutación.
- **Golden de `ps`/`env`** (`test_procesos.py` + `test_session_ch3.py`, S1
  31/08): cabeceras GNU (`ps` → `    PID TTY          TIME CMD`; `ps aux` →
  cabecera completa con USER) verificadas contra coreutils real; `env` ordenado
  por clave (reproducibilidad §5); sesión end-to-end del cap. 3 donde `ps aux`
  DELATA al propietario compartido (prosa de Manus); roundtrip de la sesión
  conserva procesos+entorno byte a byte. Regresión explícita: cap. 0 y cap. 2
  NO exponen `ps`/`env` (exit 127).
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
