# ZONA 🔬 DE TESTEO (la escribe Gwyn al cierre; la ejecutan Oscar 05:00 → Havel 07:00)

> Oscar la recorre COMPLETA desde save limpio (¿el viaje aguanta?);
> Havel se centra en lo nuevo + smoke (¿funciona y mola?). Formato y reglas:
> `docs/TESTEO-DIARIO.md` §4.

## 🔬 Testeo de mañana (10/09)

Zona prioritaria: **El cap. 4 ES jugable por primera vez** — quest `story.ch4.e1` «La llave prestada» + red propia (`chapter4.py`, hosts 2-3/seed, `ssh`+`scp` en allowlist desde el nacimiento).

- **Primera prioridad — el viaje completo hasta el cap. 4 desde save limpio:** `?chapter=4&seed=42` → `cat /etc/hosts` descubre `faro`+`troncal-01` (y `troncal-02` en seed 1; `ls /etc` NO descubre) → `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` copia con metadatos (TR-001) → completar `story.ch4.e1` y que el gate suba a `c.scp`. OJO: `c.cut` ahora vive en cap. 4 (prereq `wc`) — el Faro (cap. 6) deja de ser el primer sitio donde se aprende `cut`: probar jugando el Faro ANTES del troncal a ver si la progresión sigue enseñando `cut` con necesidad real (dato de diseño para la decisión del límite de pipes).
- **Segunda prioridad — el límite de 2 pipes (🧭25, [P1]):** en el cap. 4/6 la quest e2 valida con `tail -n +2 ... | cut ... | sort` (2 pipes) — probar que el golden sale verde, que `uniq -c` encadenado en segundo paso también, y anotar si ALGÚN beat natural pide 3 pipes (decisión mañana: ampliar el shell a 3 pipes vs enseñar a encadenar con `> /tmp/x`).
- **Smoke:** suite **648 passed** · gate **23 conceptos / 25 quests** (`c.scp` + `story.ch4.e1` nuevas; `e1/e2` cap. 6 + `dato2/dato3` intactas) · bundle **46 ficheros (370.4 KiB)** · `generate(42,4)` determinista byte-idéntico · `generate(42,6)` intacto (cap. 6 con Faro como ayer) · `scp` sigue 127 en cap. 6 por allowlist (frontera deliberada, NO abrir [BUG]) · red del Faro: `cat /etc/hosts` descubre `faro` 10.6.0.5 y el save aguanta roundtrip.

Contexto: mergeados hoy #39 (engine — `chapter4.py` + `DEFAULT_CH4_COMMANDS` con ssh/scp, 🧭24 resuelta por diseño), #40 (sandbox — quest ch4.e1 + `c.scp` prereq `c.cut`; `c.cut` movido 6→4 con prereq `wc`, DAG válido) y #41 (meta-ui — circuito ch4 multi-host verificado + dato exacto `3 pipes → multiple pipelines not supported`). Reglas de no-[BUG]: `scp`/`ssh` 127 en cap. 6 es frontera deliberada; FICHA de ch4.e1 vacía honesta (prosa de Manus llega mañana).
