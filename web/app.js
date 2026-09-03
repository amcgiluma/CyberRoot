/* app.js — CyberRoot T1-deploy HITO B: REPL cap. 0 en navegador vía Pyodide.
 *
 * Carga el core Python REAL (`src/core/`, stdlib puro y headless) dentro de
 * Pyodide y expone una shell jugable `cero@cap0:$` que ejecuta `shell.execute`
 * sobre la Incursión real generada con seed 42.  El core se instala en el FS
 * virtual (`/lib/core`) desde el manifest `bundle/core.json` (generado por
 * `web/build_bundle.py`).
 */
"use strict";

const VIRT_LIB = "/lib";

// Estado de la shell en Python; aquí guardamos refs para la UI.
let pyodide = null;

// ---------------------------------------------------------------------------
// Bootstrap Python (se define una vez y se reutilizan init/cmd/_describe).
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

def init(seed=42):
    from core.generator import generate, new_session
    inc = generate(int(seed), chapter=0)
    _lib["inc"] = inc
    _lib["shell"] = new_session(inc)
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
    return json.dumps(d, ensure_ascii=False, default=str)
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

function setState(state) {
  $id("md-host").textContent = state.host;
  $id("md-quest").textContent = state.objective;
  $id("md-pool").textContent = state.concept_pool.join(", ");
  $id("md-cwd").textContent = state.cwd;
  $id("md-steps").textContent = state.canon_steps
    .map((s) => "$ " + s.join(" "))
    .join("  ·  ");
  $id("state-panel").style.display = "block";
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

  setStatus("Generando cap. 0 (seed 42) y arrancando sesión…");
  let state;
  try {
    // init llama a generate(42, chapter=0) + new_session(inc) en el core real.
    state = JSON.parse(pyodide.globals.get("init")(42));
  } catch (e) {
    setStatus("Error generando la incursión: " + e);
    return;
  }

  setState(state);
  setStatus("Listo — REPL del core real en el navegador.");
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
}

function renderCursor() {
  return "cero@" + $id("md-host").textContent + ":" + ($id("md-cwd").textContent || "/") + "$ ";
}

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
  boot();
});