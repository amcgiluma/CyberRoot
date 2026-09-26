/* app.js — CyberRoot T2-web slice 2: semilla por URL + capítulo elegible + bucle de muerte.
 *
 * Carga el core Python REAL (`src/core/`, stdlib puro y headless) dentro de
 * Pyodide y expone una shell jugable `cero@host:$` que ejecuta `shell.execute`
 * sobre la Incursión generada con la semilla y capítulo de la URL.
 * El core se instala en el FS virtual (`/lib/core`) desde el manifest
 * `bundle/core.json` (generado por `tools/web/build_bundle.py`).
 *
 * T2 añade:
 * - `?seed=` y `?chapter=` en la URL → `generate(seed, chapter)` + comandos del capítulo.
 *   Capítulos jugables: 0 (tutorial), 2, 3 (orden→sudo→ps/kill), 4 (Troncal: red + volcado) y 6 (Faro con familia conteo) — muerte con `auditor_text` en todos.
 * - Bucle de muerte: `total_noise > noise_budget` → pantalla post-mortem con
 *   `build_postmortem` (voz del Auditor en el navegador) + reiniciar.
 * - Status muestra seed y capítulo activos → cada bug reporta su reproducción en la URL.
 * - Sin query string = comportamiento de ayer byte-idéntico (cap. 0, seed 42).
 */

"use strict";

const VIRT_LIB = "/lib";

// Estado global de la run activa (para reiniciar y para el status)
let pyodide = null;
let currentSeed = "42";
let currentChapter = 0;
let currentNoiseBudget = 12;

// ---------------------------------------------------------------------------
// Bootstrap Python (se define una vez y se reutilizan init/cmd/postmortem).
// ---------------------------------------------------------------------------
const BOOTSTRAP = `
import sys
import json
sys.path.insert(0, ${JSON.stringify(VIRT_LIB)})

def install_from_json(payload):
    import os
    files = json.loads(payload)
    for path, content in files.items():
        d = os.path.dirname(path)
        os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

_lib = {}

def _parse_seed(s):
    # Numeric strings → int (generate(42) vs generate("42") difieren en Rng);
    # no-numéricas → str tal cual. Int directo también vale.
    if isinstance(s, int) and not isinstance(s, bool):
        return s
    t = str(s)
    try:
        # Soporta "42", "-7", etc. No convierte floats.
        if t.lstrip("-").isdigit():
            return int(t)
        return t
    except Exception:
        return t

def init(seed=42, chapter=0):
    from core.generator import generate, new_session
    s = _parse_seed(seed)
    ch = int(chapter)
    inc = generate(s, chapter=ch)
    _lib["inc"] = inc
    _lib["shell"] = new_session(inc)
    _lib["seed"] = s
    _lib["chapter"] = ch
    _lib["noise_budget"] = int(inc.room.noise_budget)
    return json.dumps(_describe())

def _describe():
    inc = _lib["inc"]
    shell = _lib["shell"]
    return {
        "host": inc.room.host,
        "objective": inc.room.objective.story_key,
        "concept_pool": list(inc.room.concept_pool),
        "canon_steps": [list(s.argv) for s in inc.room.canon.steps],
        "cwd": shell.cwd,
        "seed": _lib.get("seed", 42),
        "chapter": _lib.get("chapter", 0),
        "noise_budget": _lib.get("noise_budget", 12),
        "total_noise": int(getattr(shell, "total_noise", 0)),
    }

def cmd(line):
    shell = _lib["shell"]
    try:
        r = shell.execute(str(line))
    except Exception as e:
        return json.dumps({"ok": False, "error": repr(e)})
    d = r.to_dict() if hasattr(r, "to_dict") else {
        "stdout": getattr(r, "stdout", ""),
        "stderr": getattr(r, "stderr", ""),
        "exit_code": getattr(r, "exit_code", 0),
        "noise": [],
        "new_cwd": None,
    }
    d["ok"] = bool(r.exit_code == 0)
    d["cwd"] = getattr(shell, "cwd", "/")
    d["total_noise"] = int(getattr(shell, "total_noise", 0))
    d["noise_budget"] = int(_lib.get("noise_budget", 12))
    return json.dumps(d, ensure_ascii=False, default=str)

def postmortem():
    from core.engine.postmortem import build_postmortem
    shell = _lib["shell"]
    nb = int(_lib.get("noise_budget", 12))
    pm = build_postmortem(shell.to_dict(), {"noise_budget": nb})
    return json.dumps(pm, ensure_ascii=False, default=str)

def get_status():
    shell = _lib["shell"]
    return json.dumps({
        "total_noise": int(getattr(shell, "total_noise", 0)),
        "noise_budget": int(_lib.get("noise_budget", 12)),
        "cwd": getattr(shell, "cwd", "/"),
        "seed": _lib.get("seed", 42),
        "chapter": _lib.get("chapter", 0),
    }, ensure_ascii=False)

def get_csv(path):
    import json as _j
    shell = _lib.get("shell")
    if shell is None:
        return _j.dumps({"ok": False, "error": "no shell"})
    try:
        from core.sandbox.fs import DirNode
        node = None
        for base in ("/", getattr(shell, "cwd", "/")):
            try:
                n = shell.fs.resolve(str(path), base)
                if n is not None and not isinstance(n, DirNode):
                    node = n
                    break
            except Exception:
                continue
        if node is None or isinstance(node, DirNode):
            return _j.dumps({"ok": False, "error": f"no such file {path}"})
        content = getattr(node, "content", "")
        return _j.dumps({"ok": True, "content": content, "path": str(path)})
    except Exception as e:
        return _j.dumps({"ok": False, "error": repr(e)})

def get_tick():
    shell = _lib.get("shell")
    if shell is None:
        return 0
    return int(getattr(shell, "tick", 0))

def get_history():
    import json as _j
    shell = _lib.get("shell")
    if shell is None:
        return _j.dumps([])
    try:
        hist = getattr(shell, "history", [])
        lines = [h.get("line", "") for h in hist if isinstance(h, dict)]
        return _j.dumps(lines, ensure_ascii=False)
    except Exception as e:
        return _j.dumps([])

def get_ps():
    import json as _j
    shell = _lib.get("shell")
    if shell is None:
        return _j.dumps([])
    try:
        procs = getattr(shell.fs, "processes", [])
        out = []
        for p in procs:
            try:
                out.append(p.to_dict() if hasattr(p, "to_dict") else {"pid": getattr(p, "pid", 0), "user": getattr(p, "user", ""), "cmd": getattr(p, "cmd", ""), "start": getattr(p, "start", "")})
            except Exception:
                continue
        return _j.dumps(out, ensure_ascii=False)
    except Exception as e:
        return _j.dumps([])

def get_ls_owner(path=\"/srv/subestacion/sesiones/pts0\"):
    import json as _j
    shell = _lib.get(\"shell\")
    if shell is None:
        return _j.dumps({\"ok\": False, \"error\": \"no shell\"})
    try:
        target = str(path) if path else \"/srv/subestacion/sesiones/pts0\"
        from core.sandbox.fs import DirNode
        node = None
        for base in (\"/\", getattr(shell, \"cwd\", \"/\")):
            try:
                n = shell.fs.resolve(target, base)
                if n is not None:
                    node = n
                    break
            except Exception:
                continue
        if node is None:
            return _j.dumps({\"ok\": False, \"error\": f\"no such file {target}\"})
        if isinstance(node, DirNode):
            return _j.dumps({\"ok\": False, \"error\": f\"{target}: Is a directory\"})
        owner = getattr(node, \"owner\", \"operator\")
        group = getattr(node, \"group\", \"operator\")
        mode = int(getattr(node, \"mode\", 0))
        return _j.dumps({\"ok\": True, \"path\": target, \"owner\": str(owner), \"group\": str(group), \"mode\": mode, \"owner_group\": f\"{owner}:{group}\"}, ensure_ascii=False)
    except Exception as e:
        return _j.dumps({\"ok\": False, \"error\": repr(e)})

def get_chown_history():
    import json as _j
    shell = _lib.get(\"shell\")
    if shell is None:
        return _j.dumps([])
    try:
        hist = getattr(shell, \"history\", []) or []
        out = []
        for h in hist:
            line = h.get(\"line\", \"\") if isinstance(h, dict) else str(h)
            if \"chown\" in line and \"pts0\" in line:
                out.append(str(line))
        return _j.dumps(out, ensure_ascii=False)
    except Exception:
        return _j.dumps([])

def get_env():
    import json as _j
    shell = _lib.get("shell")
    if shell is None:
        return _j.dumps({})
    try:
        env = getattr(shell.fs, "environment", {}) or {}
        return _j.dumps(dict(env), ensure_ascii=False)
    except Exception:
        return _j.dumps({})
`;

// ---------------------------------------------------------------------------
// UI helpers (sin framework).
// ---------------------------------------------------------------------------
function $id(id) { return document.getElementById(id); }

function appendOut(text, cls) {
  const pre = $id("out");
  const div = document.createElement("div");
  if (cls) div.className = cls;
  div.textContent = text.length ? text : " ";
  pre.appendChild(div);
  pre.scrollTop = pre.scrollHeight;
}

function setStatus(msg) {
  $id("status").textContent = msg;
  $id("status").className = "status";
}

function _updateTitle(seed, chapter) {
  // T1 26/09 Seath: título dinámico para links compartibles ?seed=&chapter=
  // Formato exigido: 'CyberRoot — cap. N — seed M' (em dash)
  try {
    document.title = `CyberRoot \u2014 cap. ${chapter} \u2014 seed ${seed}`;
  } catch (e) {}
}

function setState(state) {
  $id("md-host").textContent = state.host;
  $id("md-quest").textContent = state.objective;
  $id("md-pool").textContent = state.concept_pool.join(", ");
  $id("md-cwd").textContent = state.cwd;
  $id("md-steps").textContent = state.canon_steps
    .map((s) => "$ " + s.join(" "))
    .join("  ·  ");
  $id("state-panel").style.display = "block";
  // Seed/capítulo visibles en el status + en la cabecera dinámica
  const seedEl = $id("md-seed");
  const chapEl = $id("md-chapter");
  const budgetEl = $id("md-budget");
  if (seedEl) seedEl.textContent = String(state.seed);
  if (chapEl) chapEl.textContent = String(state.chapter);
  if (budgetEl) budgetEl.textContent = String(state.noise_budget);
  _updateTitle(state.seed, state.chapter);
}

// ---------------------------------------------------------------------------
// Tabla del Faro — panel vivo que refleja el cut (T2, Seath 06/09, dirección #4)
// Sin cambios de core: lee el CSV del FS via get_csv y destaca la columna cortada.
// ---------------------------------------------------------------------------
function parseCut(line) {
  // Detecta cut con -d y -f en cualquier orden, delimiter con/without quotes
  const tokens = line.trim().split(/\s+/);
  if (!tokens.includes("cut")) return null;
  let delim = null, field = null, file = null;
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i] === "-d" && i + 1 < tokens.length) {
      let d = tokens[i + 1];
      d = d.replace(/^['\"]|['\"]$/g, "");
      delim = d;
    }
    if (tokens[i].startsWith("-d") && tokens[i].length > 2) {
      let d = tokens[i].slice(2);
      d = d.replace(/^['\"]|['\"]$/g, "");
      if (d) delim = d;
    }
    if (tokens[i] === "-f" && i + 1 < tokens.length) {
      const n = parseInt(tokens[i + 1], 10);
      if (!isNaN(n)) field = n;
    }
    if (tokens[i].startsWith("-f") && tokens[i].length > 2) {
      const n = parseInt(tokens[i].slice(2), 10);
      if (!isNaN(n)) field = n;
    }
  }
  // Fichero: último token que parezca .csv (absoluto o relativo)
  for (let i = tokens.length - 1; i >= 0; i--) {
    if (tokens[i].includes(".csv")) {
      file = tokens[i].replace(/^['\"]|['\"]$/g, "");
      break;
    }
  }
  if (field === null || !file) return null;
  if (!delim) delim = "|"; // default del Faro es | si no se especifica
  if (!file.includes("purgas.csv") && !file.includes("registro.csv") && !file.includes("volcado.csv")) return null;
  return { delim, field, file };
}

function hideFaroTabla() {
  const el = $id("faro-tabla");
  if (el) el.style.display = "none";
}

function renderFaroTabla(cutInfo, csvContent) {
  const panel = $id("faro-tabla");
  const metaEl = $id("faro-tabla-meta");
  const contentEl = $id("faro-tabla-content");
  if (!panel || !metaEl || !contentEl) return;
  const lines = csvContent.split("\n").filter(l => l.length > 0);
  if (lines.length === 0) { hideFaroTabla(); return; }
  const delim = cutInfo.delim;
  const colIdx = cutInfo.field - 1;
  const shortFile = cutInfo.file.split("/").pop();
  const _faroSuffix = _getFaroRescateSuffix();
  if (_faroSuffix) {
    const _faroTip = "El volcado rescatado en ch4.e3 viaj\u00f3 al Faro \u2014 TR-003|EN_COLA presente en /srv/camara-faro/volcado-rescate.csv (lente, no ejecuta el core)";
    metaEl.innerHTML = `${_escapeHtml(shortFile)} \u00b7 columna ${cutInfo.field} (${_escapeHtml(delim)})<span title="${_escapeHtml(_faroTip)}" style="cursor:help;color:var(--accent)"> \u00b7 TR-003 rescatado \u2014 volcado-rescate.csv</span>`;
  } else {
    metaEl.textContent = `${shortFile} \u00b7 columna ${cutInfo.field} (${delim})`;
  }
  // Construye tabla HTML
  let html = '<table style="width:100%;border-collapse:collapse;font-family:var(--mono);font-size:.82rem">';
  // header
  const headerCells = lines[0].split(delim);
  html += "<thead><tr>";
  for (let i = 0; i < headerCells.length; i++) {
    const cls = i === colIdx ? ' style="background:rgba(94,200,229,.25);color:var(--accent);font-weight:700;border:1px solid var(--border);padding:4px 6px"' : ' style="border:1px solid var(--border);padding:4px 6px;color:var(--muted)"';
    html += `<th${cls}>${headerCells[i] || "—"}</th>`;
  }
  html += "</tr></thead><tbody>";
  const maxRows = Math.min(lines.length, 16);
  for (let r = 1; r < maxRows; r++) {
    const cells = lines[r].split(delim);
    html += "<tr>";
    for (let c = 0; c < cells.length; c++) {
      const cls = c === colIdx ? ' style="background:rgba(94,200,229,.18);color:var(--fg);font-weight:600;border:1px solid var(--border);padding:3px 6px"' : ' style="border:1px solid var(--border);padding:3px 6px"';
      const val = cells[c] || "—";
      html += `<td${cls}>${val.length > 24 ? val.slice(0,24)+"…" : val}</td>`;
    }
    html += "</tr>";
  }
  if (lines.length > maxRows) html += `<tr><td colspan="${headerCells.length}" style="text-align:center;color:var(--muted);padding:6px">… ${lines.length - maxRows} filas más (usa cat/head en la terminal)</td></tr>`;
  html += "</tbody></table>";
  contentEl.innerHTML = html;
  panel.style.display = "block";
}

function updateFaroTabla(line) {
  const info = parseCut(line);
  if (!info) return; // sin cut → no toca el panel (no lo oculta para no parpadear)
  if (currentChapter !== 6) return; // solo en el Faro
  try {
    const raw = pyodide.globals.get("get_csv")(info.file);
    const data = JSON.parse(raw);
    if (!data.ok || !data.content) { hideFaroTabla(); return; }
    renderFaroTabla(info, data.content);
  } catch (e) {
    // no rompe la terminal si falla
  }
}

// ---------------------------------------------------------------------------
// Tabla del Troncal — panel vivo 'Volcado del Troncal' del cap. 4 (Hito 3, Seath 12/09)
// Mismo patrón que el Faro, pero para el volcado.csv del troncal (cut -d'|' -f1).
// Sin cambios de core: lee el CSV del FS via get_csv y destaca la columna cortada.
// ---------------------------------------------------------------------------
function parseTroncalCut(line) {
  // Reutiliza parseCut (ya detecta volcado.csv) y filtra al fichero del troncal.
  const info = parseCut(line);
  if (!info) return null;
  if (!info.file.includes("volcado.csv")) return null;
  return info;
}

// Estado toggle TR-003 EN_COLA (lente, no ejecutor — Seath 14/09 T1)
let _troncalEnColaOnly = false;
let _troncalLastCut = null;
let _troncalLastCsv = null;
let _troncalLastGrep = false;
function _toggleTroncalEnCola() {
  _troncalEnColaOnly = !_troncalEnColaOnly;
  if (_troncalLastCut && _troncalLastCsv !== null) {
    renderTroncalTabla(_troncalLastCut, _troncalLastCsv, { grepFiltered: _troncalLastGrep });
  }
}
// Exponer para onclick inline del badge
if (typeof window !== "undefined") window._toggleTroncalEnCola = _toggleTroncalEnCola;

function hideTroncalTabla() {
  const el = $id("troncal-tabla");
  if (el) el.style.display = "none";
  // Restart limpia paneles — resetea lente
  _troncalEnColaOnly = false;
}

// Helpers T1 15/09 — Seath: ticks del volcado + rótulo rescate/caducado (sin pulso, estático)
// Helper T1 16/09 — Seath: escape HTML mínimo para innerHTML seguro (lente, no ejecutor)
function _escapeHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}
// Faro — lente del rescate (solo web/app.js, consume get_history/get_csv ya expuestos)
function _isFaroRescatePresent() {
  try {
    if (!pyodide || !pyodide.globals) return false;
    // 1) history: scp + volcado-rescate.csv (señal del gesto e3 azul)
    try {
      const hraw = pyodide.globals.get("get_history")();
      const lines = JSON.parse(hraw);
      if (Array.isArray(lines)) {
        for (const ln of lines) {
          const s = String(ln);
          if (s.includes("volcado-rescate.csv") && s.includes("scp")) return true;
        }
      }
    } catch(e) {}
    // 2) file: /srv/camara-faro/volcado-rescate.csv existe y contiene TR-003
    try {
      const raw = pyodide.globals.get("get_csv")("/srv/camara-faro/volcado-rescate.csv");
      const data = JSON.parse(raw);
      if (data.ok && data.content && String(data.content).includes("TR-003")) return true;
    } catch(e) {}
    return false;
  } catch(e) { return false; }
}
function _getFaroRescateSuffix() {
  if (currentChapter !== 6) return "";
  if (_isFaroRescatePresent()) return " \u00b7 TR-003 rescatado \u2014 volcado-rescate.csv";
  return "";
}
function _getVolcadoTick() {
  try {
    if (!pyodide || !pyodide.globals) return 0;
    const fn = pyodide.globals.get("get_tick");
    if (!fn) return 0;
    const v = fn();
    const n = parseInt(v, 10);
    return isNaN(n) ? 0 : n;
  } catch (e) { return 0; }
}
function _getVolcadoStatus(tick) {
  // Lee history y decide rótulo: rescate > disuelto > caducado > null
  try {
    if (!pyodide || !pyodide.globals) return null;
    const fn = pyodide.globals.get("get_history");
    if (!fn) return null;
    const raw = fn();
    const lines = JSON.parse(raw);
    if (!Array.isArray(lines)) return null;
    let hasRescate = false, hasDisuelto = false;
    for (const ln of lines) {
      const s = String(ln);
      if (s.includes("volcado-rescate.csv") && s.includes("scp")) hasRescate = true;
      if (s.includes("rm") && s.includes("/tmp/volcado.csv")) hasDisuelto = true;
    }
    if (hasRescate) return "testigo entregado al Faro";
    if (hasDisuelto) return "testigo disuelto";
    if (tick >= 30) return "volcado caducado (30 ticks)";
    return null;
  } catch (e) { return null; }
}

function renderTroncalTabla(cutInfo, csvContent, opts) {
  const panel = $id("troncal-tabla");
  const metaEl = $id("troncal-tabla-meta");
  const contentEl = $id("troncal-tabla-content");
  if (!panel || !metaEl || !contentEl) return;
  const grepFiltered = !!(opts && opts.grepFiltered);
  // Guarda último estado para toggle (lente EN_COLA)
  _troncalLastCut = cutInfo;
  _troncalLastCsv = csvContent;
  _troncalLastGrep = grepFiltered;
  const allLines = csvContent.split("\n").filter(l => l.length > 0);
  if (allLines.length === 0) { hideTroncalTabla(); return; }
  const delim = cutInfo.delim;
  const colIdx = cutInfo.field - 1;
  const shortFile = cutInfo.file.split("/").pop();
  // Toggle EN_COLA: filtra filas (como grep EN_COLA), reusa grepFiltered como base
  const enColaActive = _troncalEnColaOnly;
  const lines = enColaActive
    ? [allLines[0]].concat(allLines.slice(1).filter(l => l.split(delim).includes("EN_COLA")))
    : allLines;
  if (lines.length === 0) { hideTroncalTabla(); return; }
  const metaSuffix = enColaActive ? " · EN_COLA solo" : (grepFiltered ? " · grep TR-" : "");
  const _tick = _getVolcadoTick();
  const _status = _getVolcadoStatus(_tick);
  const _tickTip = "Ticks desde que apareció el volcado. A los 30 caduca si no lo rescatas (scp a faro:/srv/camara-faro/volcado-rescate.csv) o lo disuelves (rm /tmp/volcado.csv) \u2014 lectura estática, sin pulso (\u00b734)";
  const _tickSpan = `<span title="${_escapeHtml(_tickTip)}" style="cursor:help;text-decoration:underline dotted 1px rgba(140,220,150,.55);text-underline-offset:2px"> \u00b7 ticks del volcado: ${_tick}/30</span>`;
  const _rotulo = _status ? ` \u00b7 ${_escapeHtml(_status)}` : "";
  metaEl.innerHTML = `${_escapeHtml(shortFile)} \u00b7 columna ${cutInfo.field} (${_escapeHtml(delim)})${_escapeHtml(metaSuffix)}${_tickSpan}${_rotulo}`;
  let html = '<table style="width:100%;border-collapse:collapse;font-family:var(--mono);font-size:.82rem">';
  const headerCells = lines[0].split(delim);
  html += "<thead><tr>";
  for (let i = 0; i < headerCells.length; i++) {
    const headerVal = headerCells[i] || "\u2014";
    const isIdHeader = headerVal === "id" && i === 0;
    if (grepFiltered && isIdHeader) {
      const tip = "filtrado por grep TR- \u2014 el header miente, \u2018-\u2019 dice la verdad";
      html += `<th title="${tip}" style="border:1px solid var(--border);padding:4px 6px;color:var(--muted);text-decoration:line-through;opacity:.65;cursor:help;text-decoration-thickness:1.5px">${headerVal}</th>`;
    } else {
      const cls = i === colIdx ? ' style="background:rgba(140,220,150,.25);color:var(--accent);font-weight:700;border:1px solid var(--border);padding:4px 6px"' : ' style="border:1px solid var(--border);padding:4px 6px;color:var(--muted)"';
      html += `<th${cls}>${headerVal}</th>`;
    }
  }
  html += "</tr></thead><tbody>";
  const maxRows = Math.min(lines.length, 16);
  for (let r = 1; r < maxRows; r++) {
    const cells = lines[r].split(delim);
    const isEnColaRow = cells.includes("TR-003") && cells.includes("EN_COLA");
    const rowStyle = ((grepFiltered || enColaActive) && isEnColaRow) ? ' style="background:rgba(255,193,7,.07)"' : "";
    html += `<tr${rowStyle}>`;
    for (let c = 0; c < cells.length; c++) {
      const isCol = c === colIdx;
      const baseStyle = isCol ? "background:rgba(140,220,150,.18);color:var(--fg);font-weight:600;border:1px solid var(--border);padding:3px 6px" : "border:1px solid var(--border);padding:3px 6px";
      const val = cells[c] || "\u2014";
      const displayVal = val.length > 24 ? val.slice(0,24)+"\u2026" : val;
      if ((grepFiltered || enColaActive) && isEnColaRow && val === "EN_COLA") {
        const tip = enColaActive ? "filtrando EN_COLA — click para ver las 3 filas" : "512 bytes, 03:14 \u2014 el que no pesa a\u00fan pesa (click para filtrar solo TR-003)";
        const bg = enColaActive ? "rgba(255,193,7,.35);border:1px solid rgba(255,193,7,.9)" : "rgba(255,193,7,.22);border:1px solid rgba(255,193,7,.55)";
        const badge = `<span role="button" tabindex="0" title="${tip}" onclick="window._toggleTroncalEnCola()" onkeydown="if(event.key==='Enter'||event.key===' ') {event.preventDefault();window._toggleTroncalEnCola()}" style="display:inline-block;margin-left:6px;padding:1px 6px;border-radius:999px;background:${bg};color:#ffcf4a;font-size:.68rem;font-weight:700;vertical-align:middle;cursor:pointer">EN_COLA \u00b7 512</span>`;
        html += `<td style="${baseStyle}" title="${tip}">${displayVal} ${badge}</td>`;
      } else {
        html += `<td style="${baseStyle}">${displayVal}</td>`;
      }
    }
    html += "</tr>";
  }
  if (lines.length > maxRows) html += `<tr><td colspan="${headerCells.length}" style="text-align:center;color:var(--muted);padding:6px">\u2026 ${lines.length - maxRows} filas m\u00e1s (usa cat/head en la terminal)</td></tr>`;
  html += "</tbody></table>";
  contentEl.innerHTML = html;
  panel.style.display = "block";
}

function updateTroncalTabla(line) {
  const info = parseTroncalCut(line);
  if (!info) return;
  if (currentChapter !== 4) return;
  const isGrepTR = line.includes("grep") && line.includes("TR-");
  const grepFiltered = !!(isGrepTR && info.delim === "|" && info.field === 1);
  try {
    const raw = pyodide.globals.get("get_csv")(info.file);
    const data = JSON.parse(raw);
    if (!data.ok || !data.content) { hideTroncalTabla(); return; }
    renderTroncalTabla(info, data.content, { grepFiltered });
  } catch (e) {
  }
}

// Preview automático del volcado en boot (cap. 4): antes del scp aún no hay
// /tmp/volcado.csv → muestra el volcado del bundle (fallback estático) para
// que ?chapter=4&seed=42 tenga preview inmediato; tras el scp re-renderiza con col 1.
const TRONCAL_STATIC = "id|origen|destino|bytes|estado\nTR-001|faro|troncal-01|1024|OK\nTR-002|troncal-01|nodo-02|2048|OK\nTR-003|faro|troncal-01|512|EN_COLA\n";
function previewTroncalTabla() {
  if (currentChapter !== 4) return;
  try {
    const candidates = ["/tmp/volcado.csv", "/srv/archivo-troncal/volcado.csv"];
    for (const p of candidates) {
      const raw = pyodide.globals.get("get_csv")(p);
      const data = JSON.parse(raw);
      if (data.ok && data.content) {
        renderTroncalTabla({ delim: "|", field: 1, file: p }, data.content);
        return;
      }
    }
    // Fallback estático pre-scp: tabla viva inmediata (mismo contenido que TRONCAL_CONTENT)
    renderTroncalTabla({ delim: "|", field: 1, file: "/srv/archivo-troncal/volcado.csv" }, TRONCAL_STATIC);
  } catch (e) {
    // último recurso: estática
    try { renderTroncalTabla({ delim: "|", field: 1, file: "volcado.csv" }, TRONCAL_STATIC); } catch(_){}
  }
}

// ---------------------------------------------------------------------------
// Tabla de la Subestación — custodia (lente custodia, Seath 19/09 T1)
// Hermana de Faro/Troncal: renderiza /tmp/volcado-custodia.csv SOLO si
// volcado_rescatado=True (fs condicional). Ausencia honesta → No such file.
// ---------------------------------------------------------------------------
const CUSTODIA_STATIC = "id|origen|destino|bytes|estado\nTR-003|faro|troncal-01|512|EN_COLA\n";
function _isCustodiaPresent() {
  try {
    if (!pyodide || !pyodide.globals) return false;
    try {
      const raw = pyodide.globals.get("get_csv")("/tmp/volcado-custodia.csv");
      const data = JSON.parse(raw);
      if (data.ok && data.content && String(data.content).includes("TR-003")) return true;
    } catch(e) {}
    return false;
  } catch(e) { return false; }
}
function _getCustodiaSuffix() {
  if (currentChapter !== 5) return "";
  if (_isCustodiaPresent()) return " \u00b7 TR-003 custodiado \u2014 volcado-custodia.csv";
  return "";
}
function hideCustodiaTabla() {
  const el = $id("custodia-tabla");
  if (el) el.style.display = "none";
}
function parseCustodiaCut(line) {
  // cut sobre volcado-custodia.csv → reusa parseCut + filtro custodia
  if (line.includes("volcado-custodia.csv") || line.includes("volcado-custodia")) {
    const info = parseCut(line);
    if (info) return info;
    // cat sin cut: fallback columna 1
    if (line.includes("cat") && line.includes("volcado-custodia")) {
      return { delim: "|", field: 1, file: "/tmp/volcado-custodia.csv" };
    }
    // cut no parseable pero menciona custodia → asumimos cut estándar
    if (line.includes("cut")) return { delim: "|", field: 1, file: "/tmp/volcado-custodia.csv" };
    // genérico: cat/otros sobre custodia
    return { delim: "|", field: 1, file: "/tmp/volcado-custodia.csv" };
  }
  return null;
}
function renderCustodiaTabla(cutInfo, csvContent) {
  const panel = $id("custodia-tabla");
  const metaEl = $id("custodia-tabla-meta");
  const contentEl = $id("custodia-tabla-content");
  if (!panel || !metaEl || !contentEl) return;
  const lines = csvContent.split("\n").filter(l => l.length > 0);
  if (lines.length === 0) { hideCustodiaTabla(); try { _updateIntrusoUI(); } catch(e){} return; }
  const delim = cutInfo.delim || "|";
  const colIdx = (cutInfo.field || 1) - 1;
  const shortFile = (cutInfo.file || "/tmp/volcado-custodia.csv").split("/").pop();
  const _custSuf = _getCustodiaSuffix();
  const _tick = _getVolcadoTick();
  const _status = _getVolcadoStatus(_tick);
  const _tickTip = "Ticks desde que apareció el volcado. A los 30 caduca si no lo rescatas (scp a faro:/srv/camara-faro/volcado-rescate.csv) o lo disuelves (rm /tmp/volcado.csv) \u2014 lectura estática, sin pulso (\u00b734)";
  const _tickSpan = `<span title="${_escapeHtml(_tickTip)}" style="cursor:help;text-decoration:underline dotted 1px rgba(140,220,150,.55);text-underline-offset:2px"> \u00b7 ticks del volcado: ${_tick}/30</span>`;
  const _rotulo = _status ? ` \u00b7 ${_escapeHtml(_status)}` : "";
  const _custTip = "El testigo custodiado en la Subestación \u2014 /tmp/volcado-custodia.csv existe solo si rescataste en ch4.e3 (scp a faro) y no expiró (lente, no ejecuta el core)";
  const _custSpan = _custSuf ? `<span title="${_escapeHtml(_custTip)}" style="cursor:help;color:var(--accent)"> \u00b7 TR-003 custodiado \u2014 volcado-custodia.csv</span>` : "";
  metaEl.innerHTML = `${_escapeHtml(shortFile)} \u00b7 columna ${cutInfo.field || 1} (${_escapeHtml(delim)})${_tickSpan}${_rotulo}${_custSpan}`;
  let html = '<table style="width:100%;border-collapse:collapse;font-family:var(--mono);font-size:.82rem">';
  const headerCells = lines[0].split(delim);
  html += "<thead><tr>";
  for (let i = 0; i < headerCells.length; i++) {
    const cls = i === colIdx ? ' style="background:rgba(140,220,150,.25);color:var(--accent);font-weight:700;border:1px solid var(--border);padding:4px 6px"' : ' style="border:1px solid var(--border);padding:4px 6px;color:var(--muted)"';
    html += `<th${cls}>${_escapeHtml(headerCells[i] || "\u2014")}</th>`;
  }
  html += "</tr></thead><tbody>";
  const maxRows = Math.min(lines.length, 16);
  for (let r = 1; r < maxRows; r++) {
    const cells = lines[r].split(delim);
    html += "<tr>";
    for (let c = 0; c < cells.length; c++) {
      const baseStyle = c === colIdx ? "background:rgba(140,220,150,.18);color:var(--fg);font-weight:600;border:1px solid var(--border);padding:3px 6px" : "border:1px solid var(--border);padding:3px 6px";
      const val = cells[c] || "\u2014";
      const disp = val.length > 24 ? val.slice(0,24)+"\u2026" : val;
      html += `<td style="${baseStyle}">${_escapeHtml(disp)}</td>`;
    }
    html += "</tr>";
  }
  if (lines.length > maxRows) html += `<tr><td colspan="${headerCells.length}" style="text-align:center;color:var(--muted);padding:6px">\u2026 ${lines.length - maxRows} filas m\u00e1s (usa cat/head en la terminal)</td></tr>`;
  html += "</tbody></table>";
  contentEl.innerHTML = html;
  panel.style.display = "block";
  try { _updateIntrusoUI(); } catch(e){}
}
function updateCustodiaTabla(line) {
  const info = parseCustodiaCut(line);
  if (!info) return;
  if (currentChapter !== 5) return;
  try {
    const raw = pyodide.globals.get("get_csv")(info.file);
    const data = JSON.parse(raw);
    if (!data.ok || !data.content) {
      // Ausencia honesta: oculta tabla (no error consola) — el briefing la nombra como pista
      hideCustodiaTabla();
      return;
    }
    renderCustodiaTabla(info, data.content);
  } catch(e) {}
}
// ---------------------------------------------------------------------------
// Insignia del vigilante — Seath 21/09 T1 (junto a la tabla custodia)
// Lee get_ps()/get_env() ya expuestos: 3 estados sin consola roja.
// Verde: censo N intruso --vigilar-censo START 03:14
// Ámbar: silenciado (-9, sin HUP, sin intruso)
// Azul: reconfigurado (HUP_* → --reloaded)
// 25/09 T1 6º estado: grep-verde lectura forense (ps aux | grep censo)
// ---------------------------------------------------------------------------
function _hasGrepCensoInHistory() {
  try {
    if (!pyodide || !pyodide.globals) return false;
    let lines = [];
    try { lines = JSON.parse(pyodide.globals.get("get_history")()); } catch(e) { lines = []; }
    if (!Array.isArray(lines)) return false;
    for (const raw of lines) {
      const l = String(raw || "").toLowerCase();
      // debe contener grep y censo (no ceniza) — lectura forense e2
      if (l.includes("grep") && l.includes("censo")) return true;
    }
    return false;
  } catch(e) { return false; }
}
function _getIntrusoStatus() {
  try {
    if (!pyodide || !pyodide.globals) return null;
    let ps = [], env = {};
    try { ps = JSON.parse(pyodide.globals.get("get_ps")()); } catch(e){ ps = []; }
    try { env = JSON.parse(pyodide.globals.get("get_env")()); } catch(e){ env = {}; }
    if (!Array.isArray(ps)) ps = [];
    if (typeof env !== "object" || env === null) env = {};
    let hupKey = null;
    for (const k in env) { if (k.startsWith("HUP_") && String(env[k]) === "1") { hupKey = k; break; } }
    let intruso = null;
    for (const p of ps) {
      const cmd = String(p.cmd || "");
      const user = String(p.user || "");
      if (cmd.includes("intruso") && cmd.includes("--vigilar-censo")) { intruso = p; break; }
      if (cmd.includes("intruso") && cmd.includes("vigilar-censo")) { intruso = p; break; }
      // fallback estricto user censo
      if (user === "censo" && cmd.includes("intruso")) { intruso = p; break; }
    }
    if (hupKey) {
      const pidFromHup = hupKey.slice(4);
      const pid = intruso ? String(intruso.pid) : pidFromHup;
      const hasReloaded = intruso && String(intruso.cmd).includes("--reloaded");
      // HUP presente → azul reconfigurado (aunque intruso aún con --reloaded)
      return { state: "azul", kind: "reconfigurado", pid, cmd: intruso ? String(intruso.cmd) : "intruso --vigilar-censo --reloaded", hupKey, intruso, hasReloaded };
    }
    if (intruso) {
      // 25/09 T1: si hay lectura forense en el historial, el verde pasa a grep-verde (lectura > vigilante base, pero < HUP/ambar)
      if (_hasGrepCensoInHistory()) {
        return { state: "grep-verde", kind: "lectura", pid: String(intruso.pid), cmd: String(intruso.cmd), start: String(intruso.start || "03:14"), intruso, hasGrep: true };
      }
      return { state: "verde", kind: "vigilante", pid: String(intruso.pid), cmd: String(intruso.cmd), start: String(intruso.start || "03:14"), intruso };
    }
    // sin intruso -> silenciado prefiere sobre grep-verde (escribir > leer)
    return { state: "ambar", kind: "silenciado", pid: null, cmd: null, hupKey: null, intruso: null };
  } catch(e) { return null; }
}
function _intrusoBadgeHtml(s) {
  if (!s) return "";
  if (s.state === "grep-verde") {
    const cmdEsc = _escapeHtml(s.cmd || `censo ${s.pid} intruso --vigilar-censo`);
    const start = _escapeHtml(s.start || "03:14");
    return `<span title="${_escapeHtml("lectura forense: ps aux | grep censo — has leído al vigilante")}" style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(46,204,113,.10);border:1px solid rgba(46,204,113,.45);color:#2ecc71;font-weight:700;font-size:.78rem;cursor:help">⌕ censo ${ _escapeHtml(s.pid)} — lectura forense</span> <span style="color:var(--muted);font-size:.75rem">grep censo registrado</span>`;
  }
  if (s.state === "verde") {
    const cmdEsc = _escapeHtml(s.cmd || `censo ${s.pid} intruso --vigilar-censo`);
    const start = _escapeHtml(s.start || "03:14");
    return `<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(46,204,113,.18);border:1px solid rgba(46,204,113,.45);color:#2ecc71;font-weight:700;font-size:.78rem">● censo ${ _escapeHtml(s.pid)} intruso --vigilar-censo START ${start}</span> <span style="color:var(--muted);font-size:.75rem">vigilante activo</span>`;
  }
  if (s.state === "azul") {
    const pid = _escapeHtml(s.pid || "?");
    const tip = _escapeHtml(`HUP_${pid}=1 → --reloaded`);
    return `<span title="${tip}" style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(52,152,219,.18);border:1px solid rgba(52,152,219,.55);color:#5dade2;font-weight:700;font-size:.78rem;cursor:help">◆ reconfigurado — HUP_${pid} → --reloaded</span> <span style="color:var(--muted);font-size:.75rem">señal de reconfiguración</span>`;
  }
  // ámbar
  return `<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(243,156,18,.18);border:1px solid rgba(243,156,18,.45);color:#f39c12;font-weight:700;font-size:.78rem">■ silenciado</span> <span style="color:var(--muted);font-size:.75rem">proceso de vigilancia eliminado</span>`;
}
function _updateIntrusoUI() {
  const el = $id("custodia-intruso");
  if (!el) return;
  if (currentChapter !== 5) { el.style.display = "none"; el.innerHTML = ""; try { _updateCustodiaPostmortem(); } catch(e){} return; }
  try {
    const st = _getIntrusoStatus();
    if (!st) { el.style.display = "none"; el.innerHTML = ""; try { _updateCustodiaPostmortem(); } catch(e){} return; }
    el.innerHTML = _intrusoBadgeHtml(st);
    el.style.display = "block";
    try { _updateCustodiaPostmortem(); } catch(e){}
  } catch(e) { el.style.display = "none"; try { _updateCustodiaPostmortem(); } catch(_){} }
}
function hideIntrusoBadge() {
  const el = $id("custodia-intruso");
  if (el) { el.style.display = "none"; el.innerHTML = ""; }
  const pm = $id("custodia-postmortem");
  if (pm) { pm.style.display = "none"; pm.innerHTML = ""; }
}
// ---------------------------------------------------------------------------
// Lente propietario — Seath 24/09 T1 (#ch5-e4-owner, 5º estado del semáforo)
// Lee get_ls_owner()/get_chown_history() sin ejecutar (lente, no ejecuta).
// 3 estados: operator:operator neutro / gris:apagados azul / root:root rojo.
// Hermana de _getIntrusoStatus/_updateCustodiaPostmortem.
// ---------------------------------------------------------------------------
function _getOwnerStatus() {
  try {
    if (!pyodide || !pyodide.globals) return null;
    let info = null;
    try { info = JSON.parse(pyodide.globals.get("get_ls_owner")("/srv/subestacion/sesiones/pts0")); } catch(e) { info = null; }
    if (!info || !info.ok) {
      return { state: "neutro", owner: "operator", group: "operator", owner_group: "operator:operator", mode: 644, raw: info };
    }
    const owner = String(info.owner || "operator");
    const group = String(info.group || "operator");
    const og = owner + ":" + group;
    let history = [];
    try { history = JSON.parse(pyodide.globals.get("get_chown_history")()); } catch(e) { history = []; }
    const last = Array.isArray(history) && history.length ? history[history.length-1] : null;
    if (og === "gris:apagados") return { state: "azul", owner, group, owner_group: og, mode: info.mode, last, raw: info };
    if (og === "root:root") return { state: "rojo", owner, group, owner_group: og, mode: info.mode, last, raw: info };
    if (og === "operator:operator") return { state: "neutro", owner, group, owner_group: og, mode: info.mode, last, raw: info };
    return { state: "neutro", owner, group, owner_group: og, mode: info.mode, last, raw: info, variant: true };
  } catch(e) { return null; }
}
function _ownerBadgeHtml(s) {
  if (!s) return "";
  const og = _escapeHtml(s.owner_group || "operator:operator");
  const tipMode = s.mode !== undefined ? "mode " + (s.mode.toString(8) || s.mode) : "";
  const tipLast = s.last ? " · " + _escapeHtml(String(s.last)) : "";
  const tip = _escapeHtml(tipMode + tipLast + " — propietario de pts0 (ls -l, chown)");
  if (s.state === "azul") {
    return `<span title="${tip}" style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(52,152,219,.18);border:1px solid rgba(52,152,219,.55);color:#5dade2;font-weight:700;font-size:.78rem;cursor:help">◆ gris:apagados</span> <span style="color:var(--muted);font-size:.75rem">custodia transferida a Gris</span>`;
  }
  if (s.state === "rojo") {
    return `<span title="${tip}" style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(231,76,60,.18);border:1px solid rgba(231,76,60,.55);color:#e74c3c;font-weight:700;font-size:.78rem;cursor:help">● root:root</span> <span style="color:var(--muted);font-size:.75rem">casa retomada por Lumen</span>`;
  }
  const neutroExtra = s.variant ? ` <span style="color:#95a5a6;font-size:.70rem">(${og})</span>` : "";
  return `<span title="${tip}" style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(149,165,166,.14);border:1px solid rgba(149,165,166,.35);color:#95a5a6;font-weight:700;font-size:.78rem;cursor:help">○ operator:operator</span><span style="color:var(--muted);font-size:.75rem"> propietario neutro</span>${neutroExtra}`;
}
function _updateOwnerUI() {
  const el = $id("ch5-e4-owner");
  if (!el) return;
  if (currentChapter !== 5) { el.style.display = "none"; el.innerHTML = ""; return; }
  try {
    const st = _getOwnerStatus();
    if (!st) { el.style.display = "none"; el.innerHTML = ""; return; }
    el.innerHTML = _ownerBadgeHtml(st);
    el.style.display = "block";
  } catch(e) { el.style.display = "none"; }
}
function hideOwnerBadge() {
  const el = $id("ch5-e4-owner");
  if (el) { el.style.display = "none"; el.innerHTML = ""; }
}
// ---------------------------------------------------------------------------
// Lente del veredicto — Seath 22/09 T1 (#custodia-postmortem)
// Pinta bajo #custodia-intruso la frase del Expediente 000 con el color
// de la insignia (verde vivo / azul --reloaded / ámbar silenciado).
// Fuente primaria: postmortem() del core (auditor_hup_text / auditor_kill_text);
// fallback estático idéntico a textos.json si el bundle no trae el dato
// (hueco honesto delta 0, sin tocar src/core/).
// ---------------------------------------------------------------------------
function _updateCustodiaPostmortem() {
  const el = $id("custodia-postmortem");
  if (!el) return;
  if (currentChapter !== 5) { el.style.display = "none"; el.innerHTML = ""; return; }
  try {
    const st = _getIntrusoStatus();
    if (!st) { el.style.display = "none"; el.innerHTML = ""; return; }
    let text = null;
    let color = "#2ecc71";
    if (st.state === "azul") color = "#5dade2";
    else if (st.state === "ambar") color = "#f39c12";
    else if (st.state === "grep-verde") color = "#2ecc71";
    else color = "#2ecc71";
    // Intenta leer la frase real del postmortem (datos ya serializados)
    try {
      if (pyodide && pyodide.globals) {
        const pm = JSON.parse(pyodide.globals.get("postmortem")());
        if (st.state === "azul" && pm.auditor_hup_text) text = pm.auditor_hup_text;
        else if (st.state === "ambar" && pm.auditor_kill_text) text = pm.auditor_kill_text;
        else if (st.state === "verde" && pm.auditor_custodia_text) text = pm.auditor_custodia_text;
        else if (st.state === "grep-verde" && pm.auditor_custodia_text) text = pm.auditor_custodia_text;
      }
    } catch(e) {}
    if (!text) {
      if (st.state === "azul") text = "Expediente 000: señal de reconfiguración registrada — proceso de vigilancia reconfigurado. Continuidad del ensayo: estable.";
      else if (st.state === "ambar") text = "Expediente 000: proceso de vigilancia eliminado — el testigo queda sin ojos. Continuidad del ensayo: estable.";
      else if (st.state === "grep-verde") text = "Expediente 000: lectura forense registrada — grep censo. El testigo mantiene ojos en la Subestación. Continuidad del ensayo: estable.";
      else text = "Expediente 000: vigilancia activa — el testigo mantiene ojos en la Subestación. Continuidad del ensayo: estable.";
    }
    el.innerHTML = `<span style="color:${color};font-weight:700">⬥ Veredicto:</span> <span style="color:${color}">${_escapeHtml(text)}</span>`;
    el.style.display = "block";
    el.style.borderColor = color + "55";
  } catch(e) { el.style.display = "none"; }
}
function hideCustodiaPostmortem() {
  const el = $id("custodia-postmortem");
  if (el) { el.style.display = "none"; el.innerHTML = ""; }
}
function previewCustodiaTabla() {
  if (currentChapter !== 5) { hideIntrusoBadge(); hideOwnerBadge(); return; }
  // Insignia siempre visible en cap. 5 (lente, no ejecuta)
  try { _updateIntrusoUI(); } catch(e) {}
  try { _updateOwnerUI(); } catch(e) {}
  try {
    const raw = pyodide.globals.get("get_csv")("/tmp/volcado-custodia.csv");
    const data = JSON.parse(raw);
    if (data.ok && data.content) {
      renderCustodiaTabla({ delim: "|", field: 1, file: "/tmp/volcado-custodia.csv" }, data.content);
      return;
    }
    // Miss honesto: panel oculto (no error) — tooltip No such file documentado en meta si luego hay cut
    hideCustodiaTabla();
  } catch(e) {
    hideCustodiaTabla();
  }
}

function parseParams() {
  const p = new URLSearchParams(window.location.search);
  const seedRaw = p.get("seed");
  const chapterRaw = p.get("chapter");
  const seed = seedRaw !== null && seedRaw !== "" ? seedRaw : "42";
  let chapter = 0;
  if (chapterRaw !== null && chapterRaw !== "") {
    const n = parseInt(chapterRaw, 10);
    if (!isNaN(n) && [0,2,3,4,5,6].includes(n)) chapter = n;
    else if (!isNaN(n)) chapter = 0; // capítulo no soportado → fallback 0 (no-regresión)
    else chapter = 0;
  }
  return { seed, chapter };
}

// ---------------------------------------------------------------------------
// Post-mortem overlay (bucle de muerte)
// ---------------------------------------------------------------------------
function showPostmortem(pm) {
  const overlay = $id("postmortem");
  const textEl = $id("pm-text");
  const facturaEl = $id("pm-factura");
  const metaEl = $id("pm-meta");
  // Auditor text ya resuelto por build_postmortem (nunca clave cruda)
  const auditorText = pm.auditor_text || pm.auditor?.line_key || "(sin texto)";
  textEl.textContent = auditorText;
  // Factura y meta
  const factura = pm.factura || {};
  facturaEl.textContent = Object.entries(factura).map(([k,v]) => `${k}: ${v}`).join(" · ");
  metaEl.textContent = `Ruido ${pm.total_noise} / ${pm.noise_budget} · ${pm.dentro_presupuesto ? "dentro" : "EXCEDIDO"} — seed ${currentSeed} · cap. ${currentChapter}`;
  overlay.style.display = "flex";
  $id("cmd").disabled = true;
}

function hidePostmortem() {
  $id("postmortem").style.display = "none";
  $id("cmd").disabled = false;
  $id("cmd").focus();
}

async function restartSameSeed() {
  hidePostmortem();
  hideFaroTabla();
  hideTroncalTabla();
  hideCustodiaTabla();
  hideIntrusoBadge();
  hideOwnerBadge();
  $id("out").innerHTML = "";
  setStatus(`Reiniciando cap. ${currentChapter} (seed ${currentSeed})…`);
  _updateTitle(currentSeed, currentChapter);
  try {
    const state = JSON.parse(pyodide.globals.get("init")(currentSeed, currentChapter));
    currentNoiseBudget = state.noise_budget;
    setState(state);
    // Resetea el contador de ruido visible
    const nsEl = $id("noise-status");
    if (nsEl) nsEl.textContent = `ruido 0/${currentNoiseBudget}`;
    const pmUrl = $id("pm-url");
    if (pmUrl) pmUrl.textContent = window.location.href;
    setStatus(`Listo — cap. ${currentChapter} · seed ${currentSeed} · presupuesto ${currentNoiseBudget} — REPL del core real.`);
    renderPrompt(state.cwd);
    try { previewTroncalTabla(); } catch(e){}
    try { previewCustodiaTabla(); } catch(e){}
    try { _updateIntrusoUI(); } catch(e){}
    try { _updateOwnerUI(); } catch(e){}
  } catch (e) {
    setStatus("Error reiniciando: " + e);
  }
}

async function restartNewSeed() {
  const newSeed = String(Math.floor(Math.random() * 100000));
  // Actualiza la URL sin recargar, para que el bug report siga siendo copiable
  const url = new URL(window.location.href);
  url.searchParams.set("seed", newSeed);
  // Mantén el capítulo actual
  url.searchParams.set("chapter", String(currentChapter));
  window.history.replaceState({}, "", url.toString());
  currentSeed = newSeed;
  await restartSameSeed();
}

// ---------------------------------------------------------------------------
// Boot (sin librería: loadPyodide global desde el CDN).
// ---------------------------------------------------------------------------
async function boot() {
  setStatus("Cargando Pyodide…");
  try {
    pyodide = await loadPyodide();
  } catch (e) {
    setStatus("Error cargando Pyodide: " + e);
    return;
  }

  setStatus("Instalando core Python real (src/core)…");
  try {
    pyodide.runPython(BOOTSTRAP);
    const res = await fetch("bundle/core.json");
    const manifest = JSON.stringify(await res.json());
    pyodide.globals.get("install_from_json")(manifest);
  } catch (e) {
    setStatus("Error instalando core: " + e);
    return;
  }

  const { seed, chapter } = parseParams();
  currentSeed = seed;
  currentChapter = chapter;
  _updateTitle(seed, chapter);

  setStatus(`Generando cap. ${chapter} (seed ${seed}) y arrancando sesión…`);
  let state;
  try {
    state = JSON.parse(pyodide.globals.get("init")(seed, chapter));
  } catch (e) {
    setStatus("Error generando la incursión: " + e);
    // Fallback a cap. 0 si el capítulo pedido no genera (p. ej. capítulo inválido)
    try {
      currentChapter = 0;
      _updateTitle(seed, 0);
      state = JSON.parse(pyodide.globals.get("init")(seed, 0));
      setStatus(`Capítulo ${chapter} no disponible — fallback a cap. 0.`);
    } catch (e2) {
      setStatus("Error en fallback: " + e2);
      return;
    }
  }

  currentNoiseBudget = state.noise_budget;
  setState(state);
  // Preview del volcado del troncal (cap. 4): oculta sin error si aún no hay fichero
  previewTroncalTabla();
  previewCustodiaTabla();
  try { _updateIntrusoUI(); } catch(e){}
  try { _updateOwnerUI(); } catch(e){}
  const ns0 = $id("noise-status");
  if (ns0) ns0.textContent = `ruido 0/${currentNoiseBudget}`;
  setStatus(`Listo — cap. ${chapter} · seed ${seed} · presupuesto ${currentNoiseBudget} — REPL del core real.`);
  $id("cmd").disabled = false;
  $id("cmd").placeholder = "escribe un comando (ls, cat, cd, cp…)";
  renderPrompt(state.cwd);
  $id("cmd").focus();
}

function renderPrompt(cwd) {
  const p = $id("prompt");
  p.textContent = "cero@" + $id("md-host").textContent + ":" + (cwd || "/") + "$ ";
}

async function dispatch() {
  const input = $id("cmd");
  const line = input.value;
  if (line.trim() === "") return;
  input.value = "";
  appendOut(renderCursor() + line, "cmdline");
  let res;
  try {
    res = JSON.parse(pyodide.globals.get("cmd")(line));
  } catch (e) {
    appendOut("ERROR en el puente JS↔Python: " + e, "err");
    renderPrompt("/");
    return;
  }
  if (res.error !== undefined && res.error !== null && res.error !== "") {
    appendOut("python: " + res.error, "err");
    renderPrompt("/");
    return;
  }
  if (res.stdout) appendOut(res.stdout, "out");
  if (res.stderr) appendOut(res.stderr, "err");
  if (res.exit_code !== 0 && !res.stderr) appendOut("[exit " + res.exit_code + "]", "exitcode");
  renderPrompt(res.cwd);
  // Actualiza cwd visible en el panel
  const cwdEl = $id("md-cwd");
  if (cwdEl) cwdEl.textContent = res.cwd;
  // Bucle de muerte: total_noise > noise_budget → post-mortem del Auditor
  const total = res.total_noise !== undefined ? res.total_noise : 0;
  const budget = res.noise_budget !== undefined ? res.noise_budget : currentNoiseBudget;
  // También actualiza status con ruido si quieres feedback continuo
  const statusEl = $id("noise-status");
  if (statusEl) statusEl.textContent = `ruido ${total}/${budget}`;
  // Tabla del Faro: refleja el cut sin sustituir la terminal
  try { updateFaroTabla(line); } catch(e) {}
  // Tabla del Troncal (cap. 4): mismo reflejo del cut sobre volcado.csv
  try { updateTroncalTabla(line); } catch(e) {}
  // Tabla de la Subestación — custodia (cap. 5)
  try { updateCustodiaTabla(line); } catch(e) {}
  // Insignia del vigilante — actualiza tras cada comando en cap.5 (kill/ps)
  try { if (currentChapter === 5) _updateIntrusoUI(); } catch(e) {}
  // Insignia propietario — actualiza tras cada comando en cap.5 (chown/ls)
  try { if (currentChapter === 5) _updateOwnerUI(); } catch(e) {}
  if (total > budget) {
    try {
      const pm = JSON.parse(pyodide.globals.get("postmortem")());
      // Nunca clave cruda: auditor_text ya resuelto; si falla, usa line_key
      if (!pm.auditor_text || pm.auditor_text === pm.auditor?.line_key) {
        // Fallback honesto ya está en pm, pero aseguramos que no es clave cruda vacía
        pm.auditor_text = pm.auditor_text || "Expediente 000: presupuesto excedido.";
      }
      showPostmortem(pm);
    } catch (e) {
      appendOut("postmortem error: " + e, "err");
      showPostmortem({ auditor_text: "Expediente 000: presupuesto excedido (postmortem no disponible).", factura: {}, total_noise: total, noise_budget: budget, dentro_presupuesto: false });
    }
  }
}

function renderCursor() {
  return "cero@" + $id("md-host").textContent + ":" + ($id("md-cwd").textContent || "/") + "$ ";
}

// Exponer para tests / consola
if (typeof window !== "undefined") { window._getIntrusoStatus = _getIntrusoStatus; window._hasGrepCensoInHistory = _hasGrepCensoInHistory; window._updateIntrusoUI = _updateIntrusoUI; window._updateCustodiaPostmortem = _updateCustodiaPostmortem; window._getOwnerStatus = _getOwnerStatus; window._updateOwnerUI = _updateOwnerUI; }

// ---------------------------------------------------------------------------
// Wire-up.
// ---------------------------------------------------------------------------
window.addEventListener("DOMContentLoaded", () => {
  $id("cmd").addEventListener("keydown", (ev) => {
    if (ev.key === "Enter") {
      ev.preventDefault();
      dispatch();
    }
  });
  const btnSame = $id("pm-restart-same");
  const btnNew = $id("pm-restart-new");
  if (btnSame) btnSame.addEventListener("click", restartSameSeed);
  if (btnNew) btnNew.addEventListener("click", restartNewSeed);
  boot();
});
