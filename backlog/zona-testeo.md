# 🔬 Zona de testeo — 18/09 (definida por Gwyn el 17/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge: suite **749 passed**,
> gate **24 conceptos / 31 quests**, bundle **48 ficheros (441.4 KiB)**
> regenerado canónicamente (guardián verde).

## Prioridad 1 — cap. 5 «Subestación»: el testigo condicional (NUEVO, PRs #62+#63)

- **Dónde:** `build_chapter5_fs(42, volcado_rescatado=True/False)` + quest `story.ch5.e2`
  (grey, `['c.cat','c.scp']`). Rescate (vía e3 `scp` a `faro:`) → `/srv/camara-faro/volcado-rescate.csv`
  existe con `TR-003` y `/tmp/volcado-custodia.csv` presente en el FS del asalto;
  caducado → `cat` → `No such file` y el proceso `intruso --vigilar-censo` (USER censo, `START 03:14`)
  patrulla igual.
- **Qué verificar:** (a) determinismo ×2 seeds byte-idéntico en AMBAS variantes;
  (b) `No such file` es trayectoria válida, no error — el briefing lo dice como pista
  («si lo subiste, la prueba viaja; si lo borraste o tardaste, la hora amanece sin papel»);
  (c) NOTA: `session.py` aún NO expone cap. 5 (fuera de `SUPPORTED_CHAPTERS`) — probar por
  `generate(42,5,volcado_rescatado=…)` + Shell directo, no por `abrir_encargo` (llega mañana);
  (d) capítulos 0/2/3/4/6 byte-idénticos (no-regresión 7 goldens).
- **Por qué importa:** primera vez que una decisión de hace 2 capítulos cambia la GEOGRAFÍA
  de otro capítulo — si el jugador no siente que la ausencia «le habla», la bifurcación pierde peso.
- Pregunta de sabor: ¿el testigo ausente se siente vacío (bug) o ausencia elocuente (drama)?

## Prioridad 2 — web: tooltip N/30 + lente rescate Faro (PR #61)

- **Dónde:** `?chapter=4&seed=42` hover sobre `· ticks del volcado: N/30` → tooltip
  descriptivo (30 ticks, rescate `scp` vs disolución `rm`, sin pulso). `?chapter=6&seed=42`
  tras rescate → meta del panel anota `TR-003 rescatado — volcado-rescate.csv` (lente pura).
- **Qué verificar:** (a) tooltip es `title=` nativo, sin `setInterval` (🧭34); (b) la lente
  del Faro NO ejecuta nada del core — solo refleja history; (c) `TRONCAL_STATIC` intacta,
  toggle EN_COLA y `hideTroncalTabla` restart intactos; (d) con save caducado, la lente NO
  aparece (falso positivo); (e) consola limpia en ambas tarjetas.
- **Por qué importa:** la cadena TR-003 ya es visible en el panel — si la web la cuenta
  entera sin que el jugador la haya vivido, se la cuele antes de tiempo; si no la cuenta, lente muerta.
- Pregunta de sabor: ¿la web anticipa la historia o la acompaña?

**Smoke:** suite completa (749/0), gate 24/31, bundle fresco (guardián verde, 48 ficheros),
`generate(42,6)` + dato7 condicional (`volcado_rescatado=True/False`) intactos,
e3 allowlist 14 con `rm` en session intacto, badge toggle + Gris + espejo byte-idénticos.
