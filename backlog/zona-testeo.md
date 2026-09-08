# ZONA 🔬 DE TESTEO (la escribe Gwyn al cierre; la ejecutan Oscar 05:00 → Havel 07:00)

> Oscar la recorre COMPLETA desde save limpio (¿el viaje aguanta?);
> Havel se centra en lo nuevo + smoke (¿funciona y mola?). Formato y reglas:
> `docs/TESTEO-DIARIO.md` §4.

## 🔬 Testeo de mañana (09/09)

Zona prioritaria: El cap. 4 despierta con red completa — cat descubre, scp copia, el save aguanta (mundo real `generate(42,6)`, ya NO stub).
- `cat /etc/hosts` sobre `generate(42,6)` (O3 en main): exit 0, stdout con `10.6.0.5 faro`, `faro` en `Shell.hosts` (solo leer descubre; `ls /etc` no); re-leer no duplica; el descubrimiento sobrevive save/reload (roundtrip idéntico).— es lo que ayer era stub: hoy es mundo.
- Quest `story.ch6.e2` «La que no pesa» (O2): golden canónico `tail -n +2 /srv/camara-faro/purgas.csv | cut -d'|' -f4 | sort` — sin fantasma `distrito`, 2×UMBRAL-BAJO (dup PR-0092 jugable); briefing «un distrito se repite» y hint_1 que enseña `tail -n +2` sin regalar el resultado; FICHA vacía (prosa de Manus llega mañana — no abrir [BUG] por placeholder).
- Smoke: suite **635 passed** · gate **22 conceptos / 24 quests** (`e1` «El número que sobra» + `e2` «La que no pesa» + `dato2/dato3`) · bundle **45 ficheros (351.1 KiB)** · goldens `dato2` (`cut -d'|' -f4 | sort | uniq -c`, con `2 UMBRAL-BAJO`) y `dato3` (`sort -t'|' -k12 -n | head -n 3`, PR-0091 al frente) exit 0 · `scp` sigue 127 en cap. 6 por allowlist (frontera deliberada — llega con quests ch4; NO abrir [BUG]) · `ssh` en cap. 0/Faro sigue 127 (por diseño) · `ls`→5 / `ls -a`→6 (Bandit) · puerta web `?chapter=6&seed=42` carga Faro y hint solo con `chapter=6`.
Contexto: mergeados #36 (O1 tests auditor_orden + O2 e2 + O3 hosts faro), #37 (S1 scp Fase B con rechazo que nombra /etc/hosts), #38 (T1 verificación seed/chapter Chromium + T2 roundtrip scp stub→real). Reglas de no-[BUG]: `scp` 127 en cap. 6 es frontera de diseño; FICHA vacía de e2 es costura con Manus (llega con su prosa mañana).
