# 🔬 Zona de testeo — 15/09 (definida por Gwyn el 14/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base del estado actual: post-merge
> PRs #53/#54/#55, suite **714**, gate **24 conceptos / 29 quests**, bundle
> **47 ficheros (406.2 KiB)** regenerado canónicamente (guardián verde).
> ADR TR-003 FIRMADO por Gwyn esta noche: `story.ch4.e3` planificable
> mañana como quest con bifurcación karma — NADA de esa quest existe aún
> en main, no testearla hoy.

## Prioridad 1 — toggle del badge `EN_COLA` en la web (NUEVO, PR #55)

- **Dónde:** `?chapter=4&seed=42`, tras `scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/` +
  `cut -d'|' -f1 /tmp/volcado.csv | grep TR-`: click en el badge `EN_COLA · 512` de la fila
  `TR-003` → SOLO queda `TR-003` visible (como `grep EN_COLA` con los ojos); segundo click →
  vuelven las 3 filas.
- **Qué verificar:** (a) el toggle NO ejecuta nada por el jugador — es lente, no ejecutor;
  (b) `hideTroncalTabla` en `restartSameSeed` limpia AMBOS paneles (troncal + Faro) y el
  toggle no persiste tras restart; (c) Faro intacto (la tabla del Faro no cambia por el toggle
  del troncal); (d) consola limpia; (e) header `id` sigue tachado con tooltip y las
  tooltips intactas.
- **Por qué importa:** primer elemento Clicable del troncal — si un toggle «hace demasiado»
  mata la lección de `grep` que lo originó; si hace demasiado poco, es ruido.
- Pregunta de sabor: **¿el toggle añade control o resta descubrimiento?** (el jugador que
  nunca escribió `grep EN_COLA` ¿pierde algo al clickear?, ¿o el badge-clicable invita a
  probar el pipe real?)

## Prioridad 2 — dato6 con variante como REQUIREMENT (PR #54)

- **Dónde:** cap. 6 Faro, quest `story.ch6.dato6` «La segunda purga»: la golden sigue siendo
  `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep 000483` → 1 línea
  `000483|PR-0092|…|EN BLANCO, revisado`; PERO la variante
  `cut -d'|' -f3 purgas.csv | grep 000483` → `000483` ya NO es bonus, es segunda válida.
- **Qué verificar:** (a) ambas completan la quest (exit 0 con `000483`); (b) el briefing
  nombra las DOS válidas y la trampa `grep 000` (2 líneas) vs `grep 000483` (1 línea) que
  ilumina cuál de las dos huérfanas es la fantasma — «no toda huérfana es fantasma» —; (c) hint_2 la
  señaliza sin regalar la solución; (d) `cut -d','` sigue rompiendo la coma-trampa (lección
  del separador intacta); (e) determinismo 42×2 idéntico y gate 24/29 (sin quest nueva).
- **Por qué importa:** es la primera vez que una quest del juego acepta DOS rutas — si ambas
  se sienten de igual peso, la lección se multiplica; si una se siente «callejón real» y la
  otra «atajo», la honestidad del golden queda dañada.
- Pregunta de sabor: **¿las dos rutas pesan lo mismo, o el `join` se siente «el verdadero» y
  el `cut` «el truco»?** (la igualdad entre rutas es la cláusula de honestidad de
  `dato6`).

**Smoke:** suite completa (714/0), gate 24/29, bundle fresco (guardián verde, 47 ficheros),
`generate(42,6)` + `generate(42,6,'story.ch6.dato6')` intactos, `gris_eco` determinista
(con gesto → línea `hub.gris.volcado`, sin gesto → byte-idéntico) +
_toggle del troncal_ verde en `?chapter=4&seed=42`.
