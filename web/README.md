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