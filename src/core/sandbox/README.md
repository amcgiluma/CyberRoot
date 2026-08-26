# sandbox/ — El Linux virtual de CyberRoot

> **Qué hace:** implementa un filesystem Linux virtual y una shell con
> semántica REAL de comandos. Es el músculo del juego: todo lo que el jugador
> escribe pasa por aquí. No sabe que existe una partida, ni niveles, ni Pyxel.
>
> Diseño normativo: `../ARCHITECTURE.md` §2.2 · familias curriculares:
> `docs/DESIGN.md` §6.2.

## Responsabilidades
- `fs.py`: árbol de FS serializable (ficheros, permisos rwx, dueño/grupo,
  tamaños, timestamps, enlaces). Instanciable por el generador con piel
  aleatoria (nombres/IPs/puertos) y médula fija (conceptos).
- `shell.py`: parser de línea → argv/expansión (pipes, redirección, globs,
  variables) → ejecución contra `fs.py` y procesos virtuales.
- `commands/<familia>.py`: un módulo por familia — navegación (`ls/cd/cp/mv/
  find`), permisos (`chmod/chown/whoami`), texto-pipes (`grep/sort/uniq/wc/
  tee`), procesos (`ps/kill/systemctl/env`), red (`ssh/scp/ss`), auditoría
  (`journalctl/last/hashes`), escalada (SUID/cron/claves).
- Declaración por comando: conceptos que usa + ruido que genera (alimenta
  detección y pools del generador).

## Entradas / salidas
- ENTRADA: argv ya tokenizado + estado del nodo (FS, procesos, usuario
  virtual) + entorno (boons disponibles).
- SALIDA: stdout-like textual (formato real de Linux), exit code, efectos sobre
  el FS/procesos, ruido generado.

## Cómo se testea
- Golden tests por comando: entrada fija → salida byte a byte.
- Casos de semántica delicada: permisos numéricos vs simbólicos, `grep -i`,
  pipes encadenados, `sudo` con/sin credencial válida.
- Determinismo puro: sin RNG propia (el azar entra por la piel que instancia
  el generador, no aquí).
- Regla: si un comando no funciona como en Linux real, ES un bug (fantasía =
  competencia real, DESIGN §8.4).

## Dueño
Smough (`feat/sandbox`). Toques desde otras ramas = tarea para Smough.
