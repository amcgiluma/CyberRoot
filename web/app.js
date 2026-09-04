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
 *   Mínimo cap. 0 (tutorial) y cap. 3 (leer orden → sudo → ps/kill) — la lección completa.
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
  // Seed/capítulo visibles en el status + en la cabecera dinámica
  const seedEl = $id("md-seed");
  const chapEl = $id("md-chapter");
  const budgetEl = $id("md-budget");
  if (seedEl) seedEl.textContent = String(state.seed);
  if (chapEl) chapEl.textContent = String(state.chapter);
  if (budgetEl) budgetEl.textContent = String(state.noise_budget);
}

function parseParams() {
  const p = new URLSearchParams(window.location.search);
  const seedRaw = p.get("seed");
  const chapterRaw = p.get("chapter");
  const seed = seedRaw !== null && seedRaw !== "" ? seedRaw : "42";
  let chapter = 0;
  if (chapterRaw !== null && chapterRaw !== "") {
    const n = parseInt(chapterRaw, 10);
    if (!isNaN(n) && [0,2,3,6].includes(n)) chapter = n;
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
  $id("out").innerHTML = "";
  setStatus(`Reiniciando cap. ${currentChapter} (seed ${currentSeed})…`);
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

  setStatus(`Generando cap. ${chapter} (seed ${seed}) y arrancando sesión…`);
  let state;
  try {
    state = JSON.parse(pyodide.globals.get("init")(seed, chapter));
  } catch (e) {
    setStatus("Error generando la incursión: " + e);
    // Fallback a cap. 0 si el capítulo pedido no genera (p. ej. capítulo inválido)
    try {
      currentChapter = 0;
      state = JSON.parse(pyodide.globals.get("init")(seed, 0));
      setStatus(`Capítulo ${chapter} no disponible — fallback a cap. 0.`);
    } catch (e2) {
      setStatus("Error en fallback: " + e2);
      return;
    }
  }

  currentNoiseBudget = state.noise_budget;
  setState(state);
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
