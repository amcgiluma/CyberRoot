# 🔬 ZONA DE TESTEO — 12/09 (escrita por Gwyn 23:00 del 11/09)

> Relevo: **Gwyn → Oscar (05:00, recorre COMPLETA desde save limpio) → Havel
> (07:00, se centra en lo nuevo + smoke)**. Formato: `docs/TESTEO-DIARIO.md` §4.
> Base tras merge: **suite 691 passed, gate 24/28, bundle 47 (393.3 KiB)**.

## Prioridad 1 — Circuito nuevo `story.ch4.e2` «El volcado que no pesa» (cap. 4, grey)

- **Qué probar (desde save limpio, cap. 4):** la sala troncal del cap. 4. Los
  2 pasos golden: `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` y
  luego `cut -d'|' -f1 /tmp/volcado.csv | grep TR-` → debe dar
  `TR-001/TR-002/TR-003` SIN el header `id` (filtro positivo que esquiva el
  header fantasma). El dato que pesa: `cat /tmp/volcado.csv` muestra
  `TR-003|EN_COLA` — el volcado que "no pesa" es el que está en cola.
- **Preguntas de diseño a responder:**
  1. ¿La quest enseña con NECESIDAD real? (`cut`+`scp` recién asentados en
     ch4; si el jugador puede resolverla sin pensar el filtro, chirría).
  2. ¿El truco "filtro positivo en vez de negativo" se SIENTE o parece un
     requisito arbitrario? (🧭27: `grep -v` no existe; decidir si eso es
     lección o deuda).
  3. ¿La NOTA del header `id|origen|...` invita a probar `cut` sin filtro y
     equivocarse UNA VEZ antes de leer la pista? (equivocarse enseñando =
     sano; equivocarse sin salida = [BUG]).
- Save: `generate(42,4, contract_id='story.ch4.e2')` o avanza el cap. 4
  normal con la quest disponible (e1 sigue existiendo y tiene prioridad sin
  contract; verifica que el selector de sala permite elegir e2).

## Prioridad 2 — Regresión del conjunto ch4+ch6 (e1 del troncal y Faro intactos)

- **Qué probar:** que el viaje COMPLETO cap. 4 (e1 «La llave prestada» → e2
  nueva) y el Faro `dato4`/`dato5` NO han cambiado de sabor con la quest
  añadida: `generate(42,4)` sin contract sigue prefiriendo `e1`
  (byte-idéntico); `generate(42,6)` intacto; el circuito
  `GameState.to_dict/from_dict` sigue preservando hosts multi-host y
  `/tmp/volcado.csv`. Riesgo conocido: el hotfix de gate flexible que S2
  dejó en `test_ch6_datos_circuit.py` (dueño T1) — si algo del Faro se
  siente distinto HOY, SIGUE SIENDO CASI SEGURO del ch4 → anótalo con seed
  exacto.
- **Preguntas:** ¿el cap. 4 tiene ahora DOS misiones y la progresión fluye
  sin doble backtracking? ¿Puede un jugador confundir la sala troncal de e1
  con la de e2 (mismo mundo dispersed)? (tint grey vs blue debería
  separarlas visualmente — confirma si la diferencia se ve).

## Smoke (Havel, 07:00)

- Suite verde: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q` → **691 / 0**.
- Gate: `load_curriculum()` → **24 conceptos / 28 quests** (con `story.ch4.e2`).
- Bundle fresco: **47 ficheros (393.3 KiB)**; guardián
  `test_bundle_fresco.py` verde.
- Frontera allowlist: `DEFAULT_CH4_COMMANDS` = **13 cmds exactos**;
  `tail/sort/uniq/head` en ch4 → **127** (frontera honesta, intachable).
- Pipes: 2 pipes OK (`tail|cut|sort`), 4 cmds → exit 2
  `multiple pipelines not supported` (honesto).
- O1 `auditor_join` de Ornstein **NO entró** (rama vacía): nada del
  post-mortem debe citar todavía el `join -v 1` de dato4. Si aparece una
  línea del Auditor citando `join`, es [BUG] (texto pre-mergeado que no
  debía estar).

CICLO Gwyn: verde — 691/24-28/47 verificado en live sobre el árbol mergeado.
