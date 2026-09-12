# web/ — T2-web slice 2: cap. 0 y 3 jugables + bucle de muerte (Seath, 04/09)

Página estática lista para Vercel que da **juego REAL** en el navegador:
carga el **core Python de verdad** (`src/core/` + `src/data/`, stdlib puro y headless) dentro
de **Pyodide** y monta un REPL jugable con semilla y capítulo por URL
(`?seed=`/`?chapter=` → `generate(seed, chapter)` + `new_session(inc)` + `shell.execute(...)`).

Este directorio NO toca `src/core`, `src/data`, `src/render` ni `src/tests`:
solo **lee** sus fuentes vía `build_bundle.py` y escribe debajo de `web/`.

## Ficheros

| Fichero | Qué es |
|---|---|
| `index.html` | página (terminal + panel de incursión con seed/cap/budget + overlay post-mortem + evidencia golden) |
| `app.js` | bootstrap Pyodide, instala el core en el FS virtual, puente `cmd()`/`postmortem()`, parseo `?seed=`/`?chapter=`, bucle de muerte con `build_postmortem` |
| `style.css` | tema de terminal + overlay post-mortem |
| `bundle/core.json` | **artefacto generado**: manifest `{ruta_virtual → contenido}` de los `.py` de `src/core/` + `src/data/` (43 ficheros, 272 KiB) + `curriculum.json`/`textos.json` |
| `assets/golden/*.png` | evidencia jugable: render v0 (cap0-room.png, sha `c84450443e835609`) y su zoom 3× |
| `build_bundle.py` (`tools/web/`) | regenera `bundle/core.json` y copia los PNG golden |

`vercel.json` (en `web/`) sirve estático puro sin build (`outputDirectory:
"."`) : el bundle va pre-generado y commiteado (`bundle/core.json`), porque
Vercel detecta proyecto Python si hay un `.py` bajo la raíz de deploy.

## Probar local

```bash
cd /home/juanma/CyberRoot
.venv/bin/python tools/web/build_bundle.py          # solo si cambiaste src/core o src/data
python3 -m http.server 8000 --directory web
# abre http://localhost:8000
# cap. 0: http://localhost:8000/?seed=42&chapter=0
# cap. 3 (lección completa): http://localhost:8000/?chapter=3&seed=42
```

Deberías ver «Listo — REPL del core real en el navegador», el panel de la
incursión y poder teclear, p.ej.:

```
ls
cat /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt
cp /srv/oficina-vecinal-muelle-norte/nombre_de_proveedor.txt /usb/
ls /usb
```

`cmd("ls")` llama a la función Python `cmd()` definida en `app.js`, que invoca
`new_session(generate(42, 0)).execute("ls")` — el mismo core que corre offline. Para cap. 3:

```
cat /srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt
sudo cat /etc/hosts
ps aux
kill -9 522
```

## Deploy (HECHO por Seath, hito C, 03/09)

```bash
cd web && vercel --prod --yes --name cyberroot
```

- URL pública: **https://cyberroot-psi.vercel.app** (produce juego REAL: REPL
  Pyodide con el core del cap. 0, seed 42; verificado en Chromium + curl 200).
- Proyecto Vercel `cyberroot` (estático puro, sin build: el bundle va
  pre-generado con `.venv/bin/python tools/web/build_bundle.py` y commiteado;
  Vercel detecta proyecto Python si hay un `.py` bajo la raíz de deploy, por
  eso el script vive en `tools/web/` y el primer proyecto hubo que borrarlo
  y recrearlo).
- Si cambia `src/core/`: regenerar el bundle, commit, y la URL sigue valiendo
  (re-deploy manual de momento; el auto-deploy por git push queda como
  siguiente paso).

- Ruta publicada: la anota Seath en `docs/ESTADO-JUGADOR.md` + worklog.
- CDN del core: Pyodide viene de jsDelivr (sin build propio); el core entra por
  `bundle/core.json` (256 KiB, una petición).
- Suite local intacta: este HITO B no toca ningún `.py` de `src/`.

## Verificación `?seed=`/`?chapter=` (T1 08/09 — Seath, completa T3 07/09)

Implementación en `app.js` desde 06/09 (`_parse_seed` + `parseParams` L10-15/L47,
`BOOTSTRAP.init(seed,chapter)` + `generate(s,ch)`, capítulos `[0,2,3,6]` con
fallback 0). El cron 19:00 del 07/09 murió (`Interrupted by shutdown`) antes de
documentar — T1 08/09 cierra el hueco verificando en **Chromium real**.

### Cómo reproducir

```bash
python3 -m http.server 8765 --directory web
# caso 1: Faro cap.6 seed 42
http://localhost:8765/?chapter=6&seed=42
# caso 2: seed distinto, determinista (cap.0 fallback)
http://localhost:8765/?seed=1337
```

### Resultado Chromium 08/09 (playwright 1.63, headless shell 153)

| URL | `#hint-cap6` | `#header-chapter` / `#header-seed` | `#md-chapter`/`#md-seed` (tras Pyodide) | `#md-pool` | `#status` |
|---|---|---|---|---|---|
| `?chapter=6&seed=42` | `display:block` (visible) | `cap. 6` / `42` | `6` / `42` | `c.cut, c.head, c.sort, c.tail, c.uniq` | `Listo — cap. 6 · seed 42 · presupuesto 12 — REPL del core real.` |
| `?seed=1337` | `display:none` | `cap. 0` / `1337` | `0` / `1337` (fallback) | `c.ls`… (cap.0) | `Listo — cap. 0 · seed 1337…` |
| `?seed=1337` (reload) | `display:none` | `cap. 0` / `1337` | idéntico | byte-idéntico | determinista |

* Hint solo con `chapter=6` (`c==='6'` en `app.js` L131-132); sin `chapter`
  o con valor no soportado → fallback `0` (`hint-cap0` block, `hint-cap6` none).
* `parseParams` acepta `seed` numérica (`_parse_seed` convierte `"1337"`→`1337`,
  `"42"`→`42`) y `chapter` en `[0,2,3,6]`; fuera de lista → `0`.
* Determinismo Python verificado: `generate(42,6)` byte-idéntico en recarga
  (`fs.to_dict` igual), `generate(1337,0)` recarga idéntica; `?seed=1337`
  regenera determinista y muestra `header-seed` `1337` (la FS de cap.0/6 es
  estable en esta versión, la semilla viaja en `header-seed`/`md-seed` y en
  `generate(_parse_seed(seed))`).
* Verificación ejecutada con `node /tmp/pw-test/verify.js` sobre
  `python3 -m http.server 8765 --directory web` (Chromium headless, sin
  pyproject mock). Sin Delta de suite (+0): solo doc.

## Tabla viva del Troncal (T1 12/09 — Seath, hermana del Faro)

Panel lateral «Volcado del Troncal» en `index.html`+`app.js`, espejo del
`#faro-tabla` pero para el cap. 4:

| Pieza | Detalle |
|---|---|
| Panel | `#troncal-tabla` con `#troncal-tabla-meta`/`#troncal-tabla-content`, tras `#faro-tabla` |
| Hint | `#hint-cap4` con `cat /etc/hosts → scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/ → cut -d'\|' -f1 /tmp/volcado.csv | grep TR-` |
| JS | `parseCut` acepta `volcado.csv`, `parseTroncalCut/hideTroncalTabla/renderTroncalTabla/updateTroncalTabla/previewTroncalTabla` (patrón Faro, acento verde), `parseParams` capítulos `[0,2,3,4,6]`, `dispatch` dual, `preview` estático pre-scp (`TRONCAL_STATIC` 3 filas id\|origen\|destino\|bytes\|estado TR-001/002 OK 1024/2048 + TR-003 EN_COLA 512) |
| Preview | `?chapter=4&seed=42` muestra tabla inmediata (col 1 `|` resaltada) sin necesidad de `cut`; el `cut -d'|' -f1` posterior solo mueve el highlight |
| Fallback | si `/tmp/volcado.csv`/`/srv/archivo-troncal/volcado.csv` no existen aún, render estático sin error ni consola |

Sin tocar `data/` ni core: reusa `get_csv` vía Pyodide. Faro intacto (`#faro-tabla` solo cap. 6). Suite 691 (+0).

Evidencia del run: `node` log completo en worklog `docs/worklog/2026/09/08.md`
(Seath).