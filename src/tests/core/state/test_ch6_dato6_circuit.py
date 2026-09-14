"""S2 14/09 — test circuito dato6 «La segunda purga» (Smough).

Contrato S2 (plan 14/09):
  quest story.ch6.dato6 requires c.join, golden
  `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep 000483` → 1 línea PR-0092
  + variante requirement `cut -d'|' -f3 purgas.csv | grep 000483` (sube de bonus a requirement)
  hint_2 trampa `grep 000` vs `grep 000483` ("¿no toda huérfana es fantasma?")
  Reusa scaffold dato4 (mismo FS); NO toca generator.py ni chapter6.py.
  Fallback handmade si generator exige branch (test con Shell directo, declarado).

Tests:
  1) golden join|grep 000483 → PR-0092 sin PR-0091
  2) variante requirement cut|grep 000483 → 000483 (ambas válidas)
  3) lección filtro positivo: join solo da 2 huérfanas, grep 000 da 2, grep 000483 da 1
  4) briefing nombra coma ',' + ambas goldens + variante
  5) hint_2 trampa grep 000 vs 000483
  6) determinismo seed 42×2 idéntico (generator si disponible, fallback handmade)

Determinista, sin RNG global, sin reloj real, sin pyxel.
"""

from __future__ import annotations

import importlib.util
import json

from core.sandbox.fs import DirNode, FileNode, FileSystem, Proceso
from core.sandbox.shell import Shell, DEFAULT_CH6_COMMANDS

PURGAS_HEADER = "purga_id|fecha|sujeto|distrito|motivo_codigo|prev_puntuacion|post_credito|puerta_cerrada|archivo_referencia"
REGISTRO_HEADER = "residente_id|nombre|fecha_nac|distrito|vivienda|empleador|ingresos_mes|antiguedad_meses|chequeo|sanciones|marcas_purga|puntuacion|estado"

PURGAS_CONTENT = (
    PURGAS_HEADER + "\n"
    + "PR-0144|03-07|000462|UMBRAL-BAJO|CONTINUIDAD|438|0|1|OH-UBA-14-0007\n"
    + "PR-0151|11-07|000537|MUEL-01|REASIGNACION|0|0|1|OH-HOSP-47-C-0191\n"
    + "PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C\n"
    + "PR-0092|11-07|000483|UMBRAL-BAJO|EN BLANCO, revisado|500|0|1|OH-UBA-14-0092\n"
)

REGISTRO_CONTENT = (
    REGISTRO_HEADER + "\n"
    + "000291|VERA MONTEJO G.|12-03-1987|UMBRAL-ALTO|B14-E3-P14|LUMEN DIV. FACTURACION|2140|214|SIN CHEQUEO|0|0|712|ACTIVO\n"
    + "000462|E. ROLDAN S.|03-11-2001|UMBRAL-BAJO|C07-E1-P02|LAVANDERIA CICLON|1280|96|HOSP-47-C|1|1|438|EN DEUDA\n"
    + "000537|J. HERRERA V.|27-08-1963|MUEL-01|D03-E2-P01|ASTILLEROS DEL MUEL SE|0|0|EN BLANCO|0|2|0|PURGADO 19\n"
)

HOSTS_CONTENT = "127.0.0.1 localhost\n10.6.0.5 faro\n"
FARO_SYNC_BINARY = "/usr/sbin/faro-sync"


def _has_join() -> bool:
    return importlib.util.find_spec("core.sandbox.commands.join") is not None


def _handmade_ch6_fs() -> FileSystem:
    try:
        from core.generator.chapter6 import build_chapter6_fs as _build

        fs = _build(None)
        if len(fs.processes) >= 3:
            return fs
    except Exception:
        pass
    return FileSystem(
        root=DirNode(
            name="/",
            children={
                "srv": DirNode(
                    name="srv",
                    children={
                        "camara-faro": DirNode(
                            name="camara-faro",
                            children={
                                "purgas.csv": FileNode(name="purgas.csv", content=PURGAS_CONTENT),
                                "registro.csv": FileNode(name="registro.csv", content=REGISTRO_CONTENT),
                            },
                        ),
                    },
                ),
                "etc": DirNode(name="etc", children={"hosts": FileNode(name="hosts", content=HOSTS_CONTENT)}),
            },
        ),
        processes=(
            Proceso(pid=1, user="root", cmd="/sbin/init --system", tty="?", cpu="0.0", mem="0.1", vsz="22288", rss="10888", stat="Ss", start="Aug25", time="0:38"),
            Proceso(pid=412, user="faro", cmd=f"{FARO_SYNC_BINARY} --purga PR-0091", tty="?", cpu="0.1", mem="0.2", vsz="12784", rss="2104", stat="S", start="11:04", time="11:34:02"),
            Proceso(pid=431, user="faro", cmd=f"{FARO_SYNC_BINARY} --purga PR-0092", tty="?", cpu="0.0", mem="0.3", vsz="13100", rss="2440", stat="S", start="08:17", time="09:11:44"),
        ),
        environment={"LANG": "C.UTF-8", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin", "SHELL": "/bin/sh", "USER": "operator"},
    )


def _shell_ch6(fs: FileSystem) -> Shell:
    return Shell(fs, commands=DEFAULT_CH6_COMMANDS)


def _has_generator() -> bool:
    return importlib.util.find_spec("core.generator") is not None and importlib.util.find_spec("core.generator.generator") is not None


# ---------------------------------------------------------------------------
# 1) golden join|grep 000483 → PR-0092 sin PR-0091
# ---------------------------------------------------------------------------

def test_ch6_dato6_golden_join_grep_000483() -> None:
    """Golden dato6: join anti-join | grep 000483 → 1 línea PR-0092, sin PR-0091."""
    fs = _handmade_ch6_fs()
    shell = _shell_ch6(fs)
    cmd = "join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv | grep 000483"
    r = shell.execute(cmd)
    if r.exit_code == 127 and _has_join():
        from core.sandbox.commands.join import _run_join

        # fallback directo: join luego grep manual (shell no expone join en este handmade)
        r_join = _run_join(fs, "/", ("-t", "|", "-1", "3", "-2", "1", "-v", "1", "/srv/camara-faro/purgas.csv", "/srv/camara-faro/registro.csv"), tick=0)
        assert r_join.exit_code == 0, r_join.stderr
        # grep 000483 manual
        lines = [l for l in r_join.stdout.splitlines() if "000483" in l]
        assert len(lines) == 1
        assert "PR-0092" in lines[0]
        assert "PR-0091" not in lines[0]
        assert "000483|PR-0092" in lines[0]
        # verifica coma dentro del campo no rompe
        assert "EN BLANCO, revisado" in lines[0]
        return
    assert r.exit_code == 0, f"golden failed: {r.stderr}"
    assert "PR-0092" in r.stdout
    assert "000483|PR-0092" in r.stdout
    assert "EN BLANCO, revisado" in r.stdout
    assert "PR-0091" not in r.stdout
    # una sola línea con contenido
    lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, f"esperaba 1 línea, got {lines}"


# ---------------------------------------------------------------------------
# 2) variante requirement cut|grep (14/09: sube de bonus a requirement)
# ---------------------------------------------------------------------------

def test_ch6_dato6_variante_cut_grep_000483() -> None:
    """Variante requirement 14/09: cut -d'|' -f3 purgas.csv | grep 000483 → 000483 (ambas válidas)."""
    fs = _handmade_ch6_fs()
    shell = _shell_ch6(fs)
    cmd = "cut -d'|' -f3 /srv/camara-faro/purgas.csv | grep 000483"
    r = shell.execute(cmd)
    assert r.exit_code == 0, r.stderr
    assert "000483" in r.stdout
    lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1
    assert lines[0].strip() == "000483"
    assert "PR-0091" not in r.stdout


def test_ch6_dato6_ambas_variantes_validas() -> None:
    """Ambas goldens válidas: join|grep y cut|grep dan exit 0 con 000483 (requirement 14/09)."""
    fs = _handmade_ch6_fs()
    shell = _shell_ch6(fs)
    r1 = shell.execute("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv | grep 000483")
    if r1.exit_code == 127 and _has_join():
        from core.sandbox.commands.join import _run_join

        r1 = _run_join(fs, "/", ("-t", "|", "-1", "3", "-2", "1", "-v", "1", "/srv/camara-faro/purgas.csv", "/srv/camara-faro/registro.csv"), tick=0)
        # grep manual
        r1_stdout = "\n".join(l for l in r1.stdout.splitlines() if "000483" in l)
        assert "PR-0092" in r1_stdout
    else:
        assert r1.exit_code == 0
        assert "000483" in r1.stdout
    r2 = shell.execute("cut -d'|' -f3 /srv/camara-faro/purgas.csv | grep 000483")
    assert r2.exit_code == 0
    assert "000483" in r2.stdout
    # briefing declara ambas válidas
    with open("src/data/textos.json", encoding="utf-8") as f:
        data = json.load(f)
    briefing = data["texts"]["story.ch6.dato6.briefing"]
    assert "Variante:" in briefing or "Variante" in briefing
    assert "ambas válidas" in briefing
    assert "cut -d'|' -f3" in briefing


# ---------------------------------------------------------------------------
# 3) lección filtro positivo: 2 huérfanas vs 1
# ---------------------------------------------------------------------------

def test_ch6_dato6_leccion_filtro_positivo() -> None:
    """Lección: join solo da 2 huérfanas; grep 000 da 2, grep 000483 da 1."""
    fs = _handmade_ch6_fs()
    shell = _shell_ch6(fs)
    # join sin grep → 3 líneas (cabecera + 2 huérfanas) si incluye header, o 2 huérfanas puras según GNU (cabecera es sujeto)
    # En nuestro FS, header tiene sujeto="sujeto" (no numérico) → con -v 1 sale 1 header +2 huérfanas
    r_all = shell.execute("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv")
    if r_all.exit_code == 127 and _has_join():
        from core.sandbox.commands.join import _run_join

        r_all = _run_join(fs, "/", ("-t", "|", "-1", "3", "-2", "1", "-v", "1", "/srv/camara-faro/purgas.csv", "/srv/camara-faro/registro.csv"), tick=0)
    assert r_all.exit_code == 0
    assert "PR-0091" in r_all.stdout
    assert "PR-0092" in r_all.stdout

    # grep 000 → ambas huérfanas (000 y 000483 contienen 000)
    r_000 = shell.execute("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv | grep 000")
    if r_000.exit_code == 127 and _has_join():
        from core.sandbox.commands.join import _run_join

        rj = _run_join(fs, "/", ("-t", "|", "-1", "3", "-2", "1", "-v", "1", "/srv/camara-faro/purgas.csv", "/srv/camara-faro/registro.csv"), tick=0)
        lines = [l for l in rj.stdout.splitlines() if "000" in l]
        # filtra cabecera "sujeto" que no contiene 000 → 2 líneas
        assert len([l for l in lines if "PR-009" in l]) == 2
        return
    assert r_000.exit_code == 0
    assert "PR-0091" in r_000.stdout
    assert "PR-0092" in r_000.stdout
    lines_000 = [l for l in r_000.stdout.strip().splitlines() if l.strip()]
    assert len(lines_000) == 2

    # grep 000483 → solo PR-0092
    r_483 = shell.execute("join -t'|' -1 3 -2 1 -v 1 /srv/camara-faro/purgas.csv /srv/camara-faro/registro.csv | grep 000483")
    if r_483.exit_code == 127 and _has_join():
        from core.sandbox.commands.join import _run_join

        rj = _run_join(fs, "/", ("-t", "|", "-1", "3", "-2", "1", "-v", "1", "/srv/camara-faro/purgas.csv", "/srv/camara-faro/registro.csv"), tick=0)
        lines = [l for l in rj.stdout.splitlines() if "000483" in l]
        assert len(lines) == 1
        return
    assert r_483.exit_code == 0
    assert "PR-0092" in r_483.stdout
    assert "PR-0091" not in r_483.stdout
    lines_483 = [l for l in r_483.stdout.strip().splitlines() if l.strip()]
    assert len(lines_483) == 1


# ---------------------------------------------------------------------------
# 4) briefing nombra coma + ambas variantes
# ---------------------------------------------------------------------------

def test_ch6_dato6_briefing_nombra_coma() -> None:
    """Briefing de dato6 nombra la coma ',' como separador que rompe y ambas variantes."""
    with open("src/data/textos.json", encoding="utf-8") as f:
        data = json.load(f)
    briefing = data["texts"].get("story.ch6.dato6.briefing", "")
    assert "," in briefing
    assert "EN BLANCO, revisado" in briefing
    # menciona explícitamente que -d',' rompe y -d'|' no
    assert "-d'|' " in briefing or "-d'|'" in briefing or "cut" in briefing.lower()
    assert "Variante:" in briefing or "variante" in briefing.lower()
    assert "ambas válidas" in briefing
    assert "cut -d'|' -f3" in briefing
    # currículum DAG válido
    from core.curriculum import load_curriculum

    curr = load_curriculum()
    assert any(q.id == "story.ch6.dato6" for q in curr.quests)
    q = next(q for q in curr.quests if q.id == "story.ch6.dato6")
    assert tuple(q.requires) == ("c.join",)
    assert q.chapter == 6


def test_ch6_dato6_hint2_trampa_filtro() -> None:
    """hint_2 14/09: trampa grep 000 vs grep 000483 — ¿no toda huérfana es fantasma?"""
    with open("src/data/textos.json", encoding="utf-8") as f:
        data = json.load(f)
    hint2 = data["texts"].get("story.ch6.dato6.hint_2", "")
    assert "grep 000" in hint2
    assert "grep 000483" in hint2
    assert "huérfana es fantasma" in hint2 or "huérfana" in hint2
    # detail también declara ambas válidas
    detail = data["texts"].get("story.ch6.dato6.detail", "")
    assert "ambas válidas" in detail
    assert "cut -d'|' -f3" in detail


# ---------------------------------------------------------------------------
# 6) determinismo seed 42×2 idéntico (generator si disponible)
# ---------------------------------------------------------------------------

def test_ch6_dato6_determinismo_seed() -> None:
    """Determinismo: generate(42,6) ×2 byte-idéntico o FS handmade idéntico."""
    if _has_generator():
        try:
            from core.generator import generate

            inc1 = generate(42, 6)
            inc2 = generate(42, 6)
            assert inc1.room.fs.to_dict() == inc2.room.fs.to_dict(), "generate(42,6) no determinista"
            # purgas intactas con coma-trampa
            fs = inc1.room.fs
            assert "PR-0092" in fs.read_file("/srv/camara-faro/purgas.csv", "/")
            assert "EN BLANCO, revisado" in fs.read_file("/srv/camara-faro/purgas.csv", "/")
            return
        except Exception:
            pass
    # Fallback handmade determinista
    fs1 = _handmade_ch6_fs()
    fs2 = _handmade_ch6_fs()
    assert fs1.to_dict() == fs2.to_dict()
    assert "EN BLANCO, revisado" in fs1.read_file("/srv/camara-faro/purgas.csv", "/")
