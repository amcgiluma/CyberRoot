/* verificar_repl.js — arranca Chromium local (playwright-core), carga la
 * página web/, espera a que Pyodide arranque el core real y ejecuta comandos
 * en el REPL del cap. 0 (seed 42). Evidencia en stdout + /tmp/shot.png.     */
const { chromium } = require("/home/juanma/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");

const URL = process.env.REPL_URL || "http://localhost:8000/";
const OUT = process.env.REPL_SHOT || "/tmp/cyberroot-repl.png";

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1100, height: 1400 } });

  const logs = [];
  page.on("console", (m) => logs.push(`[console.${m.type()}] ${m.text()}`));
  page.on("pageerror", (e) => logs.push(`[pageerror] ${e.message}`));
  page.on("requestfailed", (r) => logs.push(`[requestfailed] ${r.url()} :: ${r.failure()?.errorText}`));

  await page.goto(URL, { waitUntil: "load", timeout: 60000 });

  // Esperar a que el boot termine (Pyodide carga wasm; puede tardar 10-30s).
  let ready = false;
  try {
    await page.waitForSelector('#status:has-text("Listo")', { timeout: 120000 });
    ready = true;
  } catch (e) {
    const status = await page.$eval("#status", (el) => el.textContent).catch(() => "?");
    console.log("STATUS after wait:", JSON.stringify(status));
  }

  const cmds = [
    "ls",
    "cat /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt",
    "cp /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt /usb/",
    "ls /usb",
    "cd /srv",
    "ls",
    "hack visualiza_red_admin",
  ];

  if (ready) {
    for (const c of cmds) {
      await page.fill("#cmd", c);
      await page.press("#cmd", "Enter");
      await page.waitForTimeout(250);
    }
    await page.waitForTimeout(300);
  }

  const outText = await page.$eval("#out", (el) => el.textContent).catch(() => "");
  const statusText = await page.$eval("#status", (el) => el.textContent).catch(() => "");
  const state = {};
  for (const id of ["md-host", "md-quest", "md-pool", "md-cwd", "md-steps"]) {
    state[id] = await page.$eval("#" + id, (el) => el.textContent).catch(() => "");
  }

  await page.screenshot({ path: OUT, fullPage: true });

  console.log("=== READY:", ready, "===");
  console.log("STATUS:", statusText);
  console.log("STATE:", JSON.stringify(state));
  console.log("--- TERMINAL OUTPUT ---");
  console.log(outText);
  console.log("--- CONSOLE/ERROR (filtrado) ---");
  for (const l of logs) if (l.includes("error") || l.includes("failed") || l.includes("Traceback")) console.log(l);
  console.log("--- SHOT saved:", OUT, "---");

  await browser.close();
  process.exit(ready ? 0 : 1);
}

main().catch((e) => { console.error("FATAL:", e); process.exit(2); });