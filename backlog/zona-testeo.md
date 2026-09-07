# ZONA 🔬 DE TESTEO (la escribe Gwyn al cierre; la ejecutan Oscar 05:00 → Havel 07:00)

> Oscar la recorre COMPLETA desde save limpio (¿el viaje aguanta?);
> Havel se centra en lo nuevo + smoke (¿funciona y mola?). Formato y reglas:
> `docs/TESTEO-DIARIO.md` §4.

## 🔬 Testeo de mañana (08/09)

Zona prioritaria: La red Fase A — descubrimiento de hosts por lectura (`cat /etc/hosts` → `Shell.hosts` → roundtrip en el save).
- `cat /etc/hosts` sobre el mundo real de `generate(42,6)` (O3 aún SIN entregar): exit 1 GNU-honesto (`No such file or directory`), `hosts` vacío, y `ls /etc` TAMBIÉN sin descubrir; con FS handmade (`127.0.0.1 localhost` + `faro`): `cat` exit 0 descubre 1 host, el pipeline `cat | grep` también descubre, re-leer no duplica, `to_dict/from_dict` idéntico. — es lo nuevo de hoy (S1/PR #34) y el estado base que mañana O3 conectará al generator.
- Puerta web cap. 6 (T1): `?chapter=6&seed=42` muestra el hint Faro NUEVO (solo con `chapter=6`; con `?seed=42` a secas → cap. 0 y sin hint-6); la muerte en cap. 6 sigue mostrando `auditor_text`; el hint orienta pero NO ejecuta nada por el jugador (tú escribes los comandos). — verificar que orienta sin regalar la solución.
- Smoke: suite **617 passed** · gate **22 conceptos / 23 quests** · bundle **45 ficheros** · goldens `dato2` (`cut -d'|' -f4 purgas.csv | sort | uniq -c`) y `dato3` (`sort -t'|' -k12 -n … | head -n 3`) exit 0 con PR-0091 al frente · `ls`→5 / `ls -a`→6 (Bandit) · `ssh` en cap. 0/Faro sigue 127 (por diseño). Si O3 y O2 entran durante el día: repetir `cat /etc/hosts` sobre `generate(42,6)` — debe descubrir `faro` — y validar el golden de e1 con `tail -n +2` (sin el fantasma `distrito`) y el briefing «un distrito se repite».
Contexto: mergeados #34/#35 (S1 hosts descubribles por lectura + S2 `sort --help` + T1 hint cap. 6 + T2 roundtrip red); O1/O2/O3 SIN RAMA — reposición prioridad 1 de mañana; no abrir [BUG] por el 127 ni por la ausencia de `/etc/hosts` en el mundo: ambos son estado conocido.
