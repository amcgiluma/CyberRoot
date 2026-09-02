"""senal.py — `kill` / señales v0 sobre el par ceniza/censo (familia procesos, cap. 3).

S1 (02/09) del plan Gwyndolin: kill v0 sobre el par ceniza-521/censo-522 que
delata `ps aux` (test_session_ch3). La física es matar/reiniciar procesos
virtuales que viven en `fs.processes` (piel del generador); la bifurcación
kármica (matar=rojo / reconfigurar=azul) queda para karma después — v0 = física
+ evento al bus para que escenas lo consuman después (payload pid/señal).

Semántica GNU honesta (DESIGN §2.6.8): mensajes y exits reales (1 = error de
usuario, 0 = éxito). Sin RNG (§2.2): la mutación es determinista y persistente
vía `Shell.to_dict`.

Señales soportadas v0:
- default (sin flag) → SIGTERM (15, mata)
- `-9` / `-SIGKILL` / `-KILL` → SIGKILL (9, mata)
- `-HUP` / `-SIGHUP` / `-1` → SIGHUP (1, reinicia con config distinta)
Otras señales → `kill: invalid signal`.

Efectos observables en `ps`/`env` (AC):
- `-9` / TERM: elimina el Proceso del FS (desaparece de `ps`).
- `-HUP`: mantiene PID pero muta `cmd` (añade ` --reloaded` si no está) y
  setea `fs.environment[f"HUP_{pid}"]=1` (visible en `env`). Así `-9` vs
  `-HUP` son distinguibles sin tocar karma.
"""

from __future__ import annotations

from core.common.events import Event
from core.sandbox.commands.base import CommandResult, CommandSpec, noise_event
from core.sandbox.fs import FileSystem, Proceso
from core.sandbox.noise import NOISE_PROFILE

KILL_NAME = "kill"

# Señales v0 normalizadas: nombre canónico → (num, mata?)
# mata=True → elimina proceso; False → reinicia (HUP)
_SIGNALS: dict[str, tuple[int, bool]] = {
    "TERM": (15, True),
    "KILL": (9, True),
    "HUP": (1, False),
}

# Alias de CLI → canónico. Se normaliza: strip `-`, upper, strip `SIG` prefix,
# luego mapear número → canónico.
_NUM_TO_CANON: dict[str, str] = {"9": "KILL", "15": "TERM", "1": "HUP"}


def _normalize_signal(token: str) -> str | None:
    """`token` sin `-` inicial → canónico `TERM`/`KILL`/`HUP` o None si inválido."""
    t = token.upper()
    if t.startswith("SIG"):
        t = t[3:]
    if t in _SIGNALS:
        return t
    if t in _NUM_TO_CANON:
        return _NUM_TO_CANON[t]
    return None


def _run_kill(
    fs: FileSystem,
    cwd: str,
    argv: tuple[str, ...],
    tick: int,
    stdin: str = "",
) -> CommandResult:
    """`kill [-9|-HUP|-TERM] <pid>...` — envía señal a procesos virtuales."""
    _ = cwd
    _ = stdin
    noise = noise_event(KILL_NAME, argv, tick)

    if not argv:
        return CommandResult(
            stderr="kill: not enough arguments",
            exit_code=1,
            noise=noise,
        )

    # Parse señal opcional: primer arg que empieza por `-`
    signal_canon = "TERM"  # default
    pids_start = 0

    first = argv[0]
    if first.startswith("-"):
        # Soporta `-s HUP` (dos tokens)
        if first == "-s":
            if len(argv) < 2:
                return CommandResult(
                    stderr="kill: option requires an argument -- 's'",
                    exit_code=1,
                    noise=noise,
                )
            cand = _normalize_signal(argv[1])
            if cand is None:
                return CommandResult(
                    stderr=f"kill: invalid signal '{argv[1]}'",
                    exit_code=1,
                    noise=noise,
                )
            signal_canon = cand
            pids_start = 2
        else:
            # `-9`, `-HUP`, `-SIGTERM`, etc. en un token
            sig_token = first[1:]  # sin `-`
            # `-n` con `l` (list) no está en contrato v0
            if sig_token == "l":
                return CommandResult(
                    stderr="kill: list signal names is not supported in this session yet",
                    exit_code=1,
                    noise=noise,
                )
            cand = _normalize_signal(sig_token)
            if cand is None:
                return CommandResult(
                    stderr=f"kill: invalid signal '{sig_token}'",
                    exit_code=1,
                    noise=noise,
                )
            signal_canon = cand
            pids_start = 1
        # Tras consumir señal, debe quedar al menos un pid
        if pids_start >= len(argv):
            return CommandResult(
                stderr="kill: not enough arguments",
                exit_code=1,
                noise=noise,
            )

    pids_tokens = argv[pids_start:]
    signal_num, should_kill = _SIGNALS[signal_canon]

    errors: list[str] = []
    signal_events: list[Event] = []
    exit_code = 0

    for token in pids_tokens:
        # Validación pid numérico
        try:
            pid = int(token)
        except ValueError:
            errors.append(f"kill: {token}: arguments must be process or job IDs")
            exit_code = 1
            continue

        # Buscar proceso
        idx = next((i for i, p in enumerate(fs.processes) if p.pid == pid), None)
        if idx is None:
            errors.append(f"kill: ({pid}) - No such process")
            exit_code = 1
            continue

        # Efecto
        if should_kill:
            # Elimina proceso
            fs.processes = tuple(p for p in fs.processes if p.pid != pid)
        else:
            # SIGHUP: reinicia con config distinta
            old = fs.processes[idx]
            new_cmd = old.cmd if " --reloaded" in old.cmd else old.cmd + " --reloaded"
            # Reconstruir proceso con cmd mutado; stat pasa a R si era S (señal de reload)
            new_stat = "R" if old.stat == "S" else old.stat
            new_proc = Proceso(
                pid=old.pid,
                user=old.user,
                cmd=new_cmd,
                tty=old.tty,
                cpu=old.cpu,
                mem=old.mem,
                vsz=old.vsz,
                rss=old.rss,
                stat=new_stat,
                start=old.start,
                time=old.time,
            )
            lst = list(fs.processes)
            lst[idx] = new_proc
            fs.processes = tuple(lst)
            # Env visible
            fs.environment[f"HUP_{pid}"] = "1"

        # Evento al bus (futura karma/escenas)
        signal_events.append(
            Event(
                type="sandbox.signal",
                data={"pid": pid, "signal": signal_canon, "signal_num": signal_num, "amount": 0},
                tick=tick,
            )
        )

    stderr = "\n".join(errors)
    # Ruido + eventos de señal (estos últimos con amount 0, no alteran total_noise)
    all_events = tuple(noise) + tuple(signal_events)
    # También emitimos un evento noise para kill ya está en noise; signal_events son extra
    return CommandResult(
        stderr=stderr,
        exit_code=exit_code,
        noise=all_events,
    )


KILL_SPEC = CommandSpec(
    name=KILL_NAME,
    concepts=frozenset({"kill"}),
    noise=NOISE_PROFILE[KILL_NAME],
    run=_run_kill,
)

SPECS: tuple[CommandSpec, ...] = (KILL_SPEC,)
