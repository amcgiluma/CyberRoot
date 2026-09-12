"""shell.py — la sesión interactiva del sandbox (ARCHITECTURE §2.2).

parser shlex POSIX + registro de comandos + cwd/tick/historial
SIMULADOS. El shell NO sabe qué comandos existen: recibe specs registradas;
v0 expone `DEFAULT_CAP0_COMMANDS = ("cat", "cd", "cp", "ls")` — `cp` entra en
el set por decisión 🧭1 de Gwyn (27/08): copiar ES el objetivo del tutorial.
Sintaxis NO soportada v0 (pipes, globs, redirección — caps. 1–2): se detecta
FUERA de comillas (GNU real: `cat "a*b.txt"` es literal y válido) y se
rechaza con error didáctico + exit 2 (PLAN decisión 3). Sin RNG, sin reloj
real, sin globals mutables; `to_dict`/`from_dict` de la sesión es ida y
vuelta exacta (§1.5).
"""

from __future__ import annotations

import shlex
from typing import Any

from core.sandbox.commands.base import CommandResult, build_registry
from core.sandbox.commands.conteo import SPECS as CONTEO_SPECS
from core.sandbox.commands.cut import SPECS as CUT_SPECS
from core.sandbox.commands.join import JOIN_NAME, SPECS as JOIN_SPECS
from core.sandbox.commands.red import (
    EXIT_NAME,
    LOGOUT_NAME,
    SCP_NAME,
    SSH_NAME,
    SPECS as RED_SPECS,
    fingerprint_for_host,
    host_key_prompt,
)
from core.sandbox.commands.senal import SPECS as SENAL_SPECS
from core.sandbox.commands.escalada import (
    AUTH_LOG_PATH,
    SUDO_AUTHZ_MARKER,
    SUDO_CREDENTIAL_PATH,
    SUDO_NAME,
    SUDO_NO_CRED_MSG,
    SUDO_READ_EVENT_TYPE,
    SUDO_UNREAD_MSG,
    check_credential,
    signature_line,
)
from core.sandbox.commands.files import CAT_NAME, SPECS as FILE_SPECS
from core.sandbox.commands.navigation import SPECS as NAVIGATION_SPECS
from core.sandbox.commands.procesos import SPECS as PROCESOS_SPECS
from core.sandbox.commands.texto import SPECS as TEXT_SPECS
from core.common.events import Event, EventBus
from core.sandbox.fs import DirNode, FileSystem
from core.sandbox.noise import NoiseMeter

#: Comandos del set del cap. 0 (tutorial). 🧭1 APROBADA por Gwyn (27/08):
#: `cp` es el 4.º concepto del cap. 0 — copiar ES el objetivo del primer
#: encargo (aprender-por-necesidad, DESIGN §6.1).
DEFAULT_CAP0_COMMANDS: tuple[str, ...] = ("cat", "cd", "cp", "ls")

#: Comandos del set del cap. 2 (S1, 30/08): añade las tuberías (`grep`, `wc`)
#: al set base. `DEFAULT_CAP0_COMMANDS` sigue intacto (cap. 0 es escenario sin
#: pipes — 🧭8=(b): evalúan los prereqs al abrir, no lo genera el capítulo).
DEFAULT_CH2_COMMANDS: tuple[str, ...] = ("cat", "cd", "cp", "grep", "ls", "wc")

#: Comandos del set del cap. 3 (S1, 31/08): añade la familia procesos (`ps`,
#: `env`) al set del cap. 2. Cap. 0 y cap. 2 quedan INTACTOS (el proceso solo
#: existe cuando el currículo lo presenta — regresión explícita en tests).
#: S1 (01/09): `sudo` entra en el cap. 3 — es donde se GANA la credencial
#: narrativa (DESIGN §6.1). NO existe en cap. 0/2 (exit 127, como `ps`/`env`).
#: S1 (02/09): `kill` entra en el cap. 3 — operar sobre el par ceniza/censo
#: (ps 521/522). Sin `kill` no hay bisturí para la persiana del Faro.
DEFAULT_CH3_COMMANDS: tuple[str, ...] = (
    "cat", "cd", "cp", "env", "grep", "kill", "ls", "ps", "sudo", "wc",
)

#: Comandos del set del cap. 4 (O1, 09/09): red del cap. 4 — añade `cut`+`ssh`/`scp`
#: al set del cap. 3. `cut` es prereq de `scp` (DAG `c.cut→c.scp`, Havel 07/09);
#: `ssh`/`scp` son la red simulada (DESIGN §6.1). Cap. 0/2/3 quedan INTACTOS
#: (regresión 127 en tests). Cap. 6 sigue 127 para ssh/scp por frontera deliberada
#: (ch4 nace CON red, ch6 sin red — 🧭24 resuelta por diseño).
DEFAULT_CH4_COMMANDS: tuple[str, ...] = (
    "cat", "cd", "cp", "cut", "env", "grep", "kill", "ls", "ps", "scp", "ssh", "sudo", "wc",
)

#: Comandos del set del cap. 6 (S2, 02/09): desbloquea la familia conteo
#: (head/tail/sort/uniq) sobre la base del cap. 3. El cap. 6 «Faro» lee la
#: Lista de Lumen con grep/wc/pipe + conteo; necesita TODO lo anterior
#: (ps/env/sudo/kill para la persiana) más la lectura frugal. Cap. 0/2/3
#: quedan INTACTOS (regresión 127 en tests).
DEFAULT_CH6_COMMANDS: tuple[str, ...] = (
    "cat", "cd", "cp", "cut", "env", "grep", "head", "join", "kill", "ls", "ps", "sort",
    "sudo", "tail", "uniq", "wc",
)

#: Todas las specs implementadas (registro completo del módulo v0 → S2; conteo
#: añadido en S2 01/09, kill en S1 02/09). `sudo` NO es una spec: es un wrapper del shell.
#: `ssh`/`exit`/`logout` NO van aquí: son wrappers del shell (como `sudo`/`cd`), no specs puras.
#: Van en RED_SPECS para registro manual si se piden, pero no en el pool del generator.
#: `join` (S3 10/09) NO está en este pool AÚN: es spec pura (JOIN_SPECS, cap. 6 quest dato4)
#: que el shell registra OPcionalmente por el set del cap. 6; no alimenta el pool del generator.
SPECS_ALL = (
    NAVIGATION_SPECS + FILE_SPECS + TEXT_SPECS + PROCESOS_SPECS + CONTEO_SPECS + SENAL_SPECS + CUT_SPECS
)

#: Caracteres de sintaxis NO soportada todavía (fuera de comillas). `*?<` =
#: globs, `>` = redirección, `&`/`;` = encadenado. `|` (tubería) SÍ entra en
#: S1 (30/08): los pipes llegan en el cap. 2. Entre comillas SON literales
#: reales (`cat "a&b.txt"` es un nombre válido).
_UNSUPPORTED_SYNTAX = frozenset("*?<>&;")

#: Mensaje didáctico de sintaxis futura (caps. 2+; PLAN §3 + 🧭3 de Oscar:
#: la terminal también ENSEÑA qué no sabe hacer AÚN — nunca culpar al comando
#: equivocado). Reformulado en S1 (30/08): las tuberías YA están; lo que
#: queda pendiente es encadenado, redirección y globs.
_SYNTAX_MSG = (
    "sh: syntax not supported in this session: it runs one pipeline at a time "
    "(chaining, redirection and globbing arrive later)"
)

#: Mensaje didáctico para >1 pipe (`a | b | c`): el cap. 2 pide UNA tubería.
_PIPE_MSG = (
    "sh: multiple pipelines not supported in this session: chain them one "
    "at a time"
)


def _has_unsupported_syntax(line: str) -> bool:
    """True si hay `*?<>&;` FUERA de comillas (entre comillas son literales).

    `|` (tubería) ya NO está en el set desde S1 (30/08): los pipes llegan en
    el cap. 2 y se parsean aparte en `_split_pipeline`.
    """
    quote: str | None = None
    for ch in line:
        if quote is not None:
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch in _UNSUPPORTED_SYNTAX:
            return True
    return False


def _split_pipeline(line: str) -> list[str]:
    """Trocea `line` por `|` FUERA de comillas (una tubería de N comandos).

    Los pipes entre comillas son literales (`cat "a|b"` no es una tubería).
    Devuelve los trozos tal cual (sin strip interior); el shell valida que
    el cap. 2 solo necesite UNA tubería (2 comandos).
    """
    parts: list[str] = []
    cur: list[str] = []
    quote: str | None = None
    for ch in line:
        if quote is not None:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            cur.append(ch)
        elif ch == "|":
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _join_err(*stderrs: str) -> str:
    """Concatena los stderr de los comandos de una tubería (orden, `\\n`).

    GNU escribe cada stderr a su salida; aquí los juntamos en el orden de
    ejecución para que el post-mortem/o el jugador lea ambos diagnósticos.
    Evita líneas en blanco y vacíos.
    """
    non_empty = [s for s in stderrs if s]
    return "\n".join(non_empty)


#: Ruta canónica del fichero de hosts del sistema (red simulada cap.4, S1
#: 07/09). `cat` EXITOSO sobre esta ruta DES-CUBRE hostnames en `self.hosts`.
HOSTS_PATH = "/etc/hosts"

#: Hostnames que NO son destinos de red (se filtran al descubrir). `ip6-*`
#: se excluye además por prefijo (ip6-localnet, ip6-mcastprefix, ...).
_HOSTS_SKIP: frozenset[str] = frozenset(
    {
        "localhost",
        "localhost.localdomain",
        "broadcasthost",
        "ip6-localhost",
        "ip6-loopback",
    }
)


def _parse_hosts_content(text: str) -> list[str]:
    """Extrae hostnames no-locales del contenido de un fichero `/etc/hosts`.

    Formato GNU: líneas `IP hostname [alias...]`; se ignoran comentarios
    (`#`) y vacías. El primer token es la IP, el resto son hostnames. Filtra
    `localhost`/`localhost.localdomain`/`broadcasthost` y todo `ip6-*`.
    Devuelve lista ÚNICA y ordenada (determinismo, ARCHITECTURE §1.5).
    """
    found: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tokens = line.split()
        if len(tokens) < 2:
            continue
        for name in tokens[1:]:
            if name in _HOSTS_SKIP or name.startswith("ip6-"):
                continue
            found.add(name)
    return sorted(found)


class Shell:
    """Una sesión de terminal virtual sobre un FileSystem (serializable)."""

    def __init__(
        self,
        fs: FileSystem,
        *,
        user: str = "operator",
        host: str = "node",
        cwd: str = "/",
        tick: int = 0,
        commands: tuple[str, ...] = DEFAULT_CAP0_COMMANDS,
        bus: EventBus | None = None,
        hosts: dict[str, FileSystem] | None = None,
        known_hosts: dict[str, str] | None = None,
    ) -> None:
        self.fs = fs
        self.user = user
        self.host = host
        self.cwd = cwd
        self.tick = tick
        self.total_noise = 0
        self.history: list[dict[str, Any]] = []
        #: Credenciales narrativas LEÍDAS en la sesión (rutas canónicas). S1
        #: (03/09, 🧭14b): el `sudo` se GANA LEYENDO la orden con `cat` — la
        #: marca la pone `_note_credential_read` y viaja en `to_dict`.
        self.read_marks: set[str] = set()
        #: Bus de sesión (runtime, NO serializado): publica
        #: `event.credential.read` al ganar cada marca. El llamador puede
        #: inyectar el suyo (tests, engine futuro); por defecto uno propio.
        self.bus = bus if bus is not None else EventBus()
        wanted = set(commands)
        self.available_commands = wanted.copy()
        self.registry = build_registry(
            tuple(
                spec
                for spec in (SPECS_ALL + JOIN_SPECS)
                if spec.name in wanted
            )
        )
        # ---- Red simulada cap.4 pieza1 (S1 06/09, hosts como FS simultáneos) ----
        #: Registro de hosts conocidos (nombre → FS). El generator o el test
        #: inyecta los FS remotos; el Shell solo los conmuta.
        self.hosts: dict[str, FileSystem] = dict(hosts) if hosts is not None else {}
        #: Pila de conexión: cada entrada guarda host/cwd/fs del nivel anterior
        self.host_stack: list[dict[str, Any]] = []
        #: Caché de huellas verificadas (known_hosts en sesión, sin disco)
        self.known_hosts: dict[str, str] = dict(known_hosts) if known_hosts is not None else {}
        #: Conexión pendiente de host-key (None o {"host","user","fingerprint"})
        self.pending_ssh: dict[str, str] | None = None
        #: Decisiones ssh registradas (yes/no por host, tick, fingerprint)
        self.ssh_decisions: list[dict[str, Any]] = []

    # ---- helpers de red ---------------------------------------------------

    def register_host(self, host: str, fs: FileSystem) -> None:
        """Registra un host remoto (FS simultáneo, DESIGN §6.1)."""
        self.hosts[host] = fs

    def _fingerprint(self, host: str) -> str:
        return fingerprint_for_host(host)

    # ---- ejecución -------------------------------------------------------

    def _note_credential_read(
        self, cmd: str, argv: tuple[str, ...], stdout: str
    ) -> None:
        """Marca la credencial narrativa como LEÍDA si este `cat` la leyó.

        S1 (03/09, 🧭14b): el `sudo` se GANA LEYENDO. Regla: comando `cat`
        cuyo stdout trae el marcador Y uno de sus operandos resuelve a
        `SUDO_CREDENTIAL_PATH` (relativa o absoluta — `abspath` canoniza).
        Solo la TRANSICIÓN publica `event.credential.read` en el bus
        (releer no re-emite). No exige exit 0: `cat falta orden` (exit 1)
        también entrega el texto al jugador — leer es leer.
        """
        if cmd != CAT_NAME or SUDO_AUTHZ_MARKER not in stdout:
            return
        for arg in argv:
            if self.fs.abspath(arg, self.cwd) == SUDO_CREDENTIAL_PATH:
                if SUDO_CREDENTIAL_PATH not in self.read_marks:
                    self.read_marks.add(SUDO_CREDENTIAL_PATH)
                    self.bus.publish(
                        Event(
                            type=SUDO_READ_EVENT_TYPE,
                            data={"path": SUDO_CREDENTIAL_PATH},
                            tick=self.tick,
                        )
                    )
                return

    def _note_hosts_discovery(
        self, cmd: str, argv: tuple[str, ...], stdout: str, exit_code: int
    ) -> None:
        """Descubre hostnames LEÍDOS de `/etc/hosts` (red simulada cap.4, S1 07/09).

        Solo la LECTURA descubre: un `cat` EXITOSO (exit 0) con un operando
        que resuelve a `HOSTS_PATH` registra cada hostname no-local en
        `self.hosts` como un FS stub (raíz `/` vacía). No toca `known_hosts`
        (eso es del ssh). `ls /etc` no pasa por aquí; un `cat` sin fichero
        falla exit 1 y tampoco descubre. Releer/doble operando no duplica:
        solo se crea el host si no existía.
        """
        if cmd != CAT_NAME or exit_code != 0:
            return
        for arg in argv:
            if self.fs.abspath(arg, self.cwd) != HOSTS_PATH:
                continue
            for host in _parse_hosts_content(stdout):
                if host not in self.hosts:
                    self.hosts[host] = FileSystem(root=DirNode(name="/", children={}))
            return

    def _exec_argv(
        self, argv: tuple[str, ...], stdin: str = ""
    ) -> CommandResult:
        """Ejecuta UN comando (argv ya parseado) con su stdin virtual.

        Resuelve la spec, invoca `spec.run(fs, cwd, argv, tick, stdin)` y
        aplica `new_cwd` si el comando cambió de directorio. NO registra en
        el historial ni suma ruido: eso lo hace `execute`/`_record` una vez
        por LÍNEA (para que una tubería quede como UNA entrada con el ruido
        de AMBOS comandos).

        `sudo` (S1, 01/09) es un WRAPPER de orquestación, no una spec: se
        despacha aquí SI la sesión lo expone (`available_commands`). Si la
        sesión no lo expone (cap. 0/2), `SUDO_NAME` no está en el registry y
        cae al `command not found` de abajo (exit 127), igual que `ps`/`env`.
        """
        # exit/logout son builtins siempre (des-apilan si hay stack)
        if argv[0] in (EXIT_NAME, LOGOUT_NAME):
            return self._exec_exit(argv, stdin)
        if argv[0] == SSH_NAME and SSH_NAME in self.available_commands:
            return self._exec_ssh(argv, stdin)
        if argv[0] == SCP_NAME and SCP_NAME in self.available_commands:
            return self._exec_scp(argv, stdin)
        if argv[0] == SUDO_NAME and SUDO_NAME in self.available_commands:
            return self._exec_sudo(argv, stdin)
        spec = self.registry.get(argv[0])
        if spec is None:
            if argv[0] == JOIN_NAME:
                return CommandResult(
                    stderr=f"sh: command not found: {argv[0]}\nTry 'join --help' \u2014 tables cross there (chapter 6).",
                    exit_code=127,
                )
            return CommandResult(
                stderr=f"sh: command not found: {argv[0]}", exit_code=127
            )
        result = spec.run(self.fs, self.cwd, argv[1:], self.tick, stdin)
        if result.new_cwd is not None:
            self.cwd = result.new_cwd
        # S1 (03/09): `cat` de la orden GANA la marca (vale en tuberías:
        # cada lado pasa por aquí).
        self._note_credential_read(argv[0], argv[1:], result.stdout)
        # S1 (07/09): `cat /etc/hosts` EXITOSO descubre hostnames (solo lectura).
        self._note_hosts_discovery(argv[0], argv[1:], result.stdout, result.exit_code)
        return result

    def _exec_ssh(
        self, argv: tuple[str, ...], stdin: str = ""
    ) -> CommandResult:
        """`ssh [user@]host` — red simulada cap.4 pieza1 (DESIGN §6.1).

        - Sin args → usage error.
        - Host no registrado → `Could not resolve hostname` (sin conectar).
        - Host no cacheado → prompt host-key (pending), sin conectar.
        - Host cacheado → push stack, switch FS/host/cwd, conectar.
        """
        if len(argv) < 2:
            return CommandResult(
                stderr="usage: ssh [user@]hostname",
                exit_code=255,
            )
        target_spec = argv[1]
        # Soportar múltiples args? Solo el primero es host; el resto se ignora v0
        if "@" in target_spec:
            user, host = target_spec.split("@", 1)
            if not host:
                return CommandResult(
                    stderr=f"ssh: Could not resolve hostname {target_spec}: Name or service not known",
                    exit_code=255,
                )
        else:
            user = self.user
            host = target_spec
        if host not in self.hosts:
            noise = NoiseMeter().emit(SSH_NAME, tuple(argv[1:]), self.tick)
            return CommandResult(
                stderr=f"ssh: Could not resolve hostname {host}: Name or service not known",
                exit_code=255,
                noise=(noise,),
            )
        fingerprint = self._fingerprint(host)
        # Si ya está en este host, no hace falta apilar
        if host == self.host and not self.host_stack:
            # Ya estás ahí — mensaje honesto
            noise = NoiseMeter().emit(SSH_NAME, tuple(argv[1:]), self.tick)
            return CommandResult(
                stdout=f"Connected to {host}.\n",
                exit_code=0,
                noise=(noise,),
            )
        if host not in self.known_hosts:
            # Primera vez → prompt host-key, sin conectar, guarda pending
            self.pending_ssh = {"host": host, "user": user, "fingerprint": fingerprint}
            msg = host_key_prompt(host, fingerprint)
            noise = NoiseMeter().emit(SSH_NAME, tuple(argv[1:]), self.tick)
            return CommandResult(stdout=msg, exit_code=0, noise=(noise,))
        # Cacheado → conecta directamente
        self.host_stack.append({"host": self.host, "cwd": self.cwd, "fs": self.fs})
        self.host = host
        self.fs = self.hosts[host]
        self.cwd = "/"
        noise = NoiseMeter().emit(SSH_NAME, tuple(argv[1:]), self.tick)
        return CommandResult(
            stdout=f"Connected to {host}.\n",
            exit_code=0,
            noise=(noise,),
        )

    def _exec_scp(
        self, argv: tuple[str, ...], stdin: str = ""
    ) -> CommandResult:
        """`scp [user@]host:path path` — copia entre FS del stack (Fase B, 08/09).

        - Requiere exactamente 2 operandos; sin host remoto -> error sin ruido 0? Con ruido scp.
        - Host no descubierto -> rechazo didáctico exit 1 ruido 0 que NOMBRA qué falta y dónde (/etc/hosts).
        - Ruta remota inexistente -> GNU-honesto No such file, exit 1 ruido scp.
        - Destino inválido (parent no existe, is_a_directory) -> GNU-honesto exit 1 ruido scp.
        - Éxito -> fichero real en FS destino con metadatos copiados, exit 0 ruido 3.
        """
        from core.sandbox.commands.base import CommandResult
        from core.sandbox.fs import DirNode, FileNode, FsError
        from core.sandbox.noise import NoiseMeter

        # argv incluye "scp" como argv[0]
        raw_args = list(argv[1:])
        # Opciones no soportadas v0: cualquier -opt -> invalid
        for a in raw_args:
            if a.startswith("-") and a != "-":
                noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
                return CommandResult(
                    stderr=f"scp: invalid option -- '{a.lstrip('-')}'",
                    exit_code=1,
                    noise=(noise,),
                )
        if len(raw_args) < 2:
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr="scp: missing file operand",
                exit_code=1,
                noise=(noise,),
            )
        if len(raw_args) > 2:
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr="scp: too many arguments",
                exit_code=1,
                noise=(noise,),
            )
        src_spec, dst_spec = raw_args[0], raw_args[1]

        def _parse_target(spec: str) -> tuple[str | None, str]:
            if ":" in spec:
                host_part, path = spec.split(":", 1)
                # host_part puede ser user@host
                if "@" in host_part:
                    host = host_part.rsplit("@", 1)[1]
                else:
                    host = host_part
                if host == "":
                    return None, path  # host vacío -> se tratará como error
                return host, path
            return None, spec

        src_host, src_path = _parse_target(src_spec)
        dst_host, dst_path = _parse_target(dst_spec)

        # Detectar ":" con host vacío (ej: ": /path" o "user@:...")
        if (":" in src_spec and src_host is None) or (":" in dst_spec and dst_host is None):
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr="scp: invalid hostname",
                exit_code=1,
                noise=(noise,),
            )

        # Debe haber al menos un host remoto
        if src_host is None and dst_host is None:
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr="scp: no remote host specified",
                exit_code=1,
                noise=(noise,),
            )

        # Hosts no descubiertos -> rechazo didáctico ruido 0 que nombra dónde leer
        if src_host is not None and src_host not in self.hosts:
            return CommandResult(
                stderr=f"scp: host '{src_host}' no descubierto \u2014 l\u00e9elo en /etc/hosts",
                exit_code=1,
                noise=(),
            )
        if dst_host is not None and dst_host not in self.hosts:
            return CommandResult(
                stderr=f"scp: host '{dst_host}' no descubierto \u2014 l\u00e9elo en /etc/hosts",
                exit_code=1,
                noise=(),
            )

        # Resolver FS
        src_fs = self.hosts[src_host] if src_host is not None else self.fs
        dst_fs = self.hosts[dst_host] if dst_host is not None else self.fs
        # cwd para cada FS
        src_cwd = "/" if src_host is not None else self.cwd
        dst_cwd = "/" if dst_host is not None else self.cwd

        # Validar src_path no vacío
        if src_path == "":
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr=f"scp: {src_spec}: No such file or directory",
                exit_code=1,
                noise=(noise,),
            )

        # Leer fuente
        try:
            src_node = src_fs.resolve(src_path, src_cwd)
        except FsError as e:
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            # Mensaje GNU-honesto: scp: <spec>: No such file or Is a directory etc
            kind_map = {
                "not_found": "No such file or directory",
                "not_a_directory": "Not a directory",
                "is_a_directory": "Is a directory",
                "permission_denied": "Permission denied",
            }
            msg = kind_map.get(e.kind, e.kind)
            return CommandResult(
                stderr=f"scp: {src_spec}: {msg}",
                exit_code=1,
                noise=(noise,),
            )
        if isinstance(src_node, DirNode):
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr=f"scp: {src_spec}: Is a directory",
                exit_code=1,
                noise=(noise,),
            )

        # Determinar destino final: si dst es directorio existente, copiar dentro
        # dst_path puede ser vacío? (ej: "faro:" -> path vacío) ya validado? dst_path vacío significa error
        if dst_path == "":
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr=f"scp: {dst_spec}: No such file or directory",
                exit_code=1,
                noise=(noise,),
            )

        # Comprobar si dst es directorio
        try:
            dst_node = dst_fs.resolve(dst_path, dst_cwd)
            is_dir = isinstance(dst_node, DirNode)
        except FsError:
            is_dir = False

        if is_dir:
            base = src_path.rsplit("/", 1)[-1] if "/" in src_path else src_path
            # dst_path tal cual + "/" + base
            final_spec = dst_path.rstrip("/") + "/" + base if dst_path != "/" else "/" + base
            final_path = final_spec
        else:
            final_path = dst_path

        # Resolver parent de final_path en dst_fs
        # final_path puede ser relativo para local; para remoto cwd="/"
        # abspath normaliza
        final_abs = dst_fs.abspath(final_path, dst_cwd)
        # segments
        segs = [s for s in final_abs.split("/") if s not in ("", ".")]
        # handle .. already normalized by abspath, but keep as is
        # Use _normalize via fs? abspath ya normaliza, so segs are clean
        if not segs:
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            return CommandResult(
                stderr=f"scp: {dst_spec}: Invalid argument",
                exit_code=1,
                noise=(noise,),
            )
        file_name = segs[-1]
        parent_abs = "/" + "/".join(segs[:-1]) if len(segs) > 1 else "/"
        try:
            parent_node = dst_fs.get_dir(parent_abs, "/")
        except FsError as e:
            noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
            kind_map2 = {
                "not_found": "No such file or directory",
                "not_a_directory": "Not a directory",
                "is_a_directory": "Is a directory",
            }
            msg = kind_map2.get(e.kind, e.kind)
            return CommandResult(
                stderr=f"scp: {dst_spec}: {msg}",
                exit_code=1,
                noise=(noise,),
            )

        # Comprobar colisiones same_file y is_a_directory
        if file_name in parent_node.children:
            existing = parent_node.children[file_name]
            if isinstance(existing, DirNode):
                noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
                return CommandResult(
                    stderr=f"scp: {dst_spec}: Is a directory",
                    exit_code=1,
                    noise=(noise,),
                )
            # same_file si mismo FS y misma ruta absoluta que origen
            if dst_fs is src_fs:
                try:
                    src_abs = src_fs.abspath(src_path, src_cwd)
                    if src_abs == final_abs:
                        noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
                        return CommandResult(
                            stderr=f"scp: '{src_spec}' and '{dst_spec}' are the same file",
                            exit_code=1,
                            noise=(noise,),
                        )
                except Exception:
                    pass

        # Crear / sobrescribir fichero destino con metadatos de origen
        # src_node es FileNode
        new_node = FileNode(
            name=file_name,
            content=src_node.content,
            owner=src_node.owner,
            group=src_node.group,
            mode=src_node.mode,
            mtime=src_node.mtime,
        )
        parent_node.children[file_name] = new_node

        noise = NoiseMeter().emit(SCP_NAME, tuple(raw_args), self.tick)
        return CommandResult(
            stdout="",
            stderr="",
            exit_code=0,
            noise=(noise,),
        )

    def _exec_exit(
        self, argv: tuple[str, ...], stdin: str = ""
    ) -> CommandResult:
        """`exit`/`logout` — des-apila host anterior (stack de conexión)."""
        cmd = argv[0]
        noise = NoiseMeter().emit(cmd, tuple(argv[1:]), self.tick)
        if not self.host_stack:
            # Sin stack: logout simple (no hay a dónde volver)
            return CommandResult(stdout="logout\n", exit_code=0, noise=(noise,))
        prev = self.host_stack.pop()
        # Restaurar host/cwd/fs anterior
        self.host = prev["host"]
        self.fs = prev["fs"]
        self.cwd = prev["cwd"]
        return CommandResult(stdout="logout\n", exit_code=0, noise=(noise,))

    def _exec_sudo(
        self, argv: tuple[str, ...], stdin: str = ""
    ) -> CommandResult:
        """`sudo <cmd> [args...]` — elevación con credencial narrativa (cap. 3).

        Forma firma DESIGN §6.1 (S1, 01/09; gate de LECTURA S1, 03/09 🧭14b):
          - sin credencial en el mundo → rechazo diegético accionable, exit 1,
            ruido 0.
          - credencial SIN LEER (`cat` previo en la sesión) → rechazo
            diegético que NOMBRA la orden, exit 1, ruido 0, SIN firma.
          - credencial LEÍDA → ejecuta el comando envuelto (registry),
            factura ruido PREMIUM (extra sobre el base del comando) y deja
            firma en `AUTH_LOG_PATH` (usuario, comando, tick) via
            `fs.append_file`.

        Si el comando envuelto no existe → `sh: command not found: cmd`
        (exit 127), igual que el shell sin sudo. La credencial vive en el FS de
        la sala (contrato O1↔S1); NO es una contraseña tecleada.
        """
        if len(argv) < 2:
            return CommandResult(
                stderr="sudo: no command given\n", exit_code=1
            )
        # Sin credencial en el mundo: intentar no es delinquir.
        if not check_credential(self.fs, self.cwd):
            return CommandResult(stderr=SUDO_NO_CRED_MSG + "\n", exit_code=1)
        # Con credencial pero SIN LEER: la llave se gana, no se adivina.
        if SUDO_CREDENTIAL_PATH not in self.read_marks:
            return CommandResult(stderr=SUDO_UNREAD_MSG + "\n", exit_code=1)

        wrapped = argv[1:]
        spec = self.registry.get(wrapped[0])
        if spec is None:
            return CommandResult(
                stderr=f"sh: command not found: {wrapped[0]}", exit_code=127
            )
        result = spec.run(self.fs, self.cwd, wrapped[1:], self.tick, stdin)
        if result.new_cwd is not None:
            self.cwd = result.new_cwd
        # Leer es leer también bajo sudo (no cambia el gate: sin marca previa
        # ni se llega aquí).
        self._note_credential_read(wrapped[0], wrapped[1:], result.stdout)

        # Ruido PREMIUM: el wrapper emite el extra (base + premium = factura)
        # y deja firma en el auth.log — el poder deja factura (§6.1).
        premium = NoiseMeter().emit(SUDO_NAME, tuple(wrapped), self.tick)
        noise = result.noise + (premium,)
        self.fs.append_file(
            AUTH_LOG_PATH,
            signature_line(self.user, wrapped[0], tuple(wrapped[1:]), self.tick),
        )
        return CommandResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            noise=noise,
            new_cwd=result.new_cwd,
        )

    def _handle_pending_ssh(self, line: str) -> CommandResult | None:
        """Si hay pending host-key, interpreta yes/no/fingerprint como respuesta.

        Devuelve CommandResult si la línea era una respuesta al prompt;
        None si no hay pending o la línea no es respuesta (deja que execute
        normal siga).
        """
        if self.pending_ssh is None:
            return None
        stripped = line.strip()
        pending = self.pending_ssh
        host = pending["host"]
        fingerprint = pending["fingerprint"]
        if stripped in ("yes", fingerprint):
            # Aceptar y conectar
            self.known_hosts[host] = fingerprint
            self.ssh_decisions.append(
                {"host": host, "answer": "yes", "fingerprint": fingerprint, "tick": self.tick}
            )
            self.host_stack.append({"host": self.host, "cwd": self.cwd, "fs": self.fs})
            self.host = host
            self.fs = self.hosts[host]
            self.cwd = "/"
            self.pending_ssh = None
            noise = NoiseMeter().emit(SSH_NAME, (host,), self.tick)
            msg = (
                f"Warning: Permanently added '{host}' (ED25519) to the list of known hosts.\n"
                f"Connected to {host}.\n"
            )
            return self._record(line, CommandResult(stdout=msg, exit_code=0, noise=(noise,)))
        if stripped == "no":
            self.ssh_decisions.append(
                {"host": host, "answer": "no", "fingerprint": fingerprint, "tick": self.tick}
            )
            self.pending_ssh = None
            # Sin ruido de sesión establecida (plan)
            return self._record(line, CommandResult(stdout="Host key verification failed.\n", exit_code=1))
        # Si pending y la línea no es yes/no/fingerprint → mantener pending pero
        # informar que debe responder yes/no
        if stripped in ("y", "n"):
            # OpenSSH acepta y/n como abreviación, pero nuestro prompt dice yes/no;
            # lo tratamos como inválido para no romper determinismo
            pass
        # No es respuesta al prompt → no consumir, pero si hay pending, cualquier
        # otro comando mientras pending debería recordarle que responda
        # Para no bloquear, si el usuario teclea otro comando distinto a yes/no,
        # lo tratamos como que cancela? El plan dice prompt host-key y yes/no;
        # para simplificar, si no es yes/no, mantenemos pending y dejamos que el
        # comando se ejecute normal tras limpiar? Mejor mantener pending y exigir
        # yes/no: devolvemos recordatorio sin avanzar.
        # Sin embargo, esto bloquearía `ls` mientras pending. Decisión: si no es
        # yes/no, no consumir como respuesta → retorna None y deja que execute
        # normal siga, pero pending sigue vivo (el usuario puede seguir intentando).
        return None

    def execute(self, line: str) -> CommandResult:
        """Ejecuta una línea; muta cwd/tick/historial y devuelve el resultado.

        Línea vacía → éxito sin efecto (como pulsar Enter en una terminal
        real). Comandos desconocidos → exit 127 con stderr de `sh` real.
        Una tubería `cmd1 | cmd2` (S1, 30/08) ejecuta `cmd1` con stdin vacío,
        captura su stdout y lo alimenta como stdin de `cmd2`; el resultado se
        registra como UNA línea con el ruido de ambos comandos.
        """
        stripped = line.strip()
        if not stripped:
            return CommandResult()

        # Pending host-key: yes/no tiene prioridad sobre parsing normal
        if self.pending_ssh is not None and stripped in ("yes", "no", self.pending_ssh["fingerprint"]):
            handled = self._handle_pending_ssh(line)
            if handled is not None:
                return handled

        if _has_unsupported_syntax(stripped):
            return self._record(line, CommandResult(stderr=_SYNTAX_MSG, exit_code=2))

        pipeline = _split_pipeline(stripped)
        if len(pipeline) > 3:
            # Cap. 6 E2 pide DOS tuberías (cut|sort|uniq -c); hasta 2 pipes permitidos.
            return self._record(line, CommandResult(stderr=_PIPE_MSG, exit_code=2))

        try:
            argv = tuple(shlex.split(pipeline[-1], posix=True))
        except ValueError:
            # Comillas sin cerrar u otros errores léxicos de shell real.
            return self._record(
                line,
                CommandResult(
                    stderr="sh: syntax error: unexpected end of file", exit_code=2
                ),
            )

        if not argv:
            return self._record(line, CommandResult())

        if len(pipeline) == 1:
            return self._record(line, self._exec_argv(argv))

        # Tubería: `cmd1 | cmd2 [| cmd3]` — cap. 6 E2 pide cut|sort|uniq
        # Encadena stdin: stdout del anterior es stdin del siguiente.
        argvs: list[tuple[str, ...]] = []
        for segment in pipeline[:-1]:
            try:
                av = tuple(shlex.split(segment, posix=True))
            except ValueError:
                return self._record(
                    line,
                    CommandResult(
                        stderr="sh: syntax error: unexpected end of file", exit_code=2
                    ),
                )
            if not av:
                return self._record(line, CommandResult(stderr=_PIPE_MSG, exit_code=2))
            argvs.append(av)
        argvs.append(argv)
        # Ejecuta encadenado
        prev_stdout = None
        results: list = []
        for idx, av in enumerate(argvs):
            stdin = prev_stdout if idx > 0 else ""
            res = self._exec_argv(av, stdin=stdin)
            results.append(res)
            prev_stdout = res.stdout
        # Último resultado manda stdout/exit/new_cwd; stderr y ruido se combinan
        last = results[-1]
        combined_stderr = _join_err(*(r.stderr for r in results))
        combined_noise = []
        for r in results:
            combined_noise.extend(r.noise)
        combined = CommandResult(
            stdout=last.stdout,
            stderr=combined_stderr,
            exit_code=last.exit_code,
            noise=combined_noise,
            new_cwd=last.new_cwd,
        )
        return self._record(line, combined)

    def _record(self, line: str, result: CommandResult) -> CommandResult:
        """Anota historial, suma el ruido del resultado y avanza el tick.

        El ruido total suma los eventos que YA viajan en `result.noise`
        (única fuente de verdad: cada comando emite el suyo). Comandos
        desconocidos y errores de sintaxis no suman ruido (perfil 0), pero
        sí consumen un tick: el tiempo simulado corre igual.
        """
        self.history.append({"line": line, "result": result.to_dict()})
        self.total_noise += sum(int(ev.data.get("amount", 0)) for ev in result.noise)
        self.tick += 1
        return result

    # ---- serialización (ARCHITECTURE §1.5) -------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Sesión completa a dict plano (fs, cwd, tick, historial, marcas)."""
        return {
            "fs": self.fs.to_dict(),
            "user": self.user,
            "host": self.host,
            "cwd": self.cwd,
            "tick": self.tick,
            "total_noise": self.total_noise,
            "history": [
                {"line": h["line"], "result": h["result"]} for h in self.history
            ],
            # S1 (03/09): credenciales LEÍDAS (rutas canónicas, ordenadas
            # por codepoint para bytes reproducibles).
            "read_marks": sorted(self.read_marks),
            # S1 (06/09): red simulada — hosts simultáneos + known_hosts + decisiones
            "hosts": {h: fs.to_dict() for h, fs in self.hosts.items()},
            "host_stack": [
                {"host": e["host"], "cwd": e["cwd"], "fs": e["fs"].to_dict()}
                for e in self.host_stack
            ],
            "known_hosts": dict(self.known_hosts),
            "ssh_decisions": list(self.ssh_decisions),
            "pending_ssh": dict(self.pending_ssh) if self.pending_ssh is not None else None,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Shell":
        """Reconstruye la sesión; copia independiente del original.

        `read_marks` es opcional (saves v1 previos a S1-03/09 cargan con
        el set vacío: sesión sin lecturas). El bus NO viaja (runtime):
        la restaurada trae uno propio y vacío.
        """
        shell = cls(
            FileSystem.from_dict(d["fs"]),
            user=str(d["user"]),
            host=str(d["host"]),
            cwd=str(d["cwd"]),
            tick=int(d["tick"]),
        )
        shell.total_noise = int(d["total_noise"])
        shell.history = [dict(h) for h in d["history"]]
        shell.read_marks = set(str(p) for p in (d.get("read_marks") or []))
        # Red: hosts
        raw_hosts = d.get("hosts") or {}
        shell.hosts = {
            str(h): FileSystem.from_dict(fs_d)
            for h, fs_d in raw_hosts.items()
            if isinstance(fs_d, dict)
        }
        raw_stack = d.get("host_stack") or []
        shell.host_stack = []
        for e in raw_stack:
            if isinstance(e, dict) and "host" in e and "fs" in e:
                shell.host_stack.append(
                    {
                        "host": str(e["host"]),
                        "cwd": str(e["cwd"]),
                        "fs": FileSystem.from_dict(e["fs"]),
                    }
                )
        shell.known_hosts = {str(k): str(v) for k, v in (d.get("known_hosts") or {}).items()}
        shell.ssh_decisions = [dict(x) for x in (d.get("ssh_decisions") or [])]
        pending = d.get("pending_ssh")
        shell.pending_ssh = dict(pending) if isinstance(pending, dict) else None
        return shell
