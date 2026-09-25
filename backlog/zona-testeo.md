# 🔬 Zona de testeo — 26/09 (definida por Gwyn el 25/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge 25/09: suite **837 passed /
> 0 failed** (818+19+0+0, deltas de Artorias verificados por aritmética +
> ensayo worktree, re-verificado por Gwyn tras los 3 merges), gate **25
> conceptos / 31 quests** intacto, bundle **50 ficheros (488.3 KiB)** regen
> canónico. PRs #81/#82/#83 MERGEADOS. NADA retenido.

## Prioridad 1 — Factura frugal `grep -c` (NUEVO, PR #81): la LECTURA broadcaster

- **Dónde:** `abrir_encargo(c,'story.ch5.e2',{'c.cat','c.grep','c.scp'},42)`.
- **Qué verificar:**
  (a) `ps aux | grep -c censo` → stdout `1\n` exit 0 (GNU honesto),
  ruido MENOR que `ps aux | grep censo | wc -l` (2 vs 3 líneas de flujo).
  (b) `ps aux | grep -c ceniza` → stdout `0\n` exit 1 — cuenta cero pero
  hay respuesta, no silencio (motivo GNU correcto).
  (c) Combinables: `-cv censo` → 0 (excluye), `-c -i censo` → 1, `--` OK.
  (d) Post-mortem: tras el e2 con `-c censo` exit 0, aparece la hermana
  `postmortem.auditor.grep_c_count` (factura frugal) SIN pisar las 4
  huellas ni las líneas de lectura anteriores.
  (e) Sin `-c`, byte-idéntico de ayer (nada cambió para el jugador sin flag).
- **Por qué importa:** la primera dopamina Balatro sin allowlist nueva ni
  gate — el mismo resultado en un pipe menos. Pregunta de sabor (OSCAR):
  ¿la factura frugal se SIENTE como recompensa o como detalle invisible?

## Prioridad 2 — 6º estado web `grep censo` + jerarquía de la lente (NUEVO, PR #83)

- **Dónde:** web `?chapter=5`, `#custodia-intruso` 6º estado `⌕`
  (`#2ecc71`, borde fino), helper `_hasGrepCensoInHistory()`.
- **Qué verificar:**
  (a) `ps aux | grep censo` → `⌕` verde claro + «grep censo registrado».
  (b) `grep ceniza` NO activa el estado (falso honesto frente a
  `censo` vs `ceniza`).
  (c) Jerarquía honesta: HUP (azul) / -9 (ámbar) PREFIEREN sobre `⌕`;
  sin intruso → ámbar aunque haya grep; reinicio limpio de insignia.
  (d) Oculto fuera de `?chapter=5`; caps 1-4 sin ensuciar.
- **Por qué importa:** el tríptico web (intruso + veredicto + propietario)
  completa su jerarquía: escribir > leer en la misma regla «MIRA, no toca».
  Pregunta de sabor: ver la LECTURA en verde claro pesa menos que ver la
  ESCRITURA en azul ROJO — ¿queda bien calibrado ese contraste en la lista?

## Smoke sí o sí

- Suite completa: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`
  → **837 passed / 0 failed** (delta +19 del engine 25/09). Si se ve 818:
  solo estás en la main pre-merge — re-corre desde post-merge.
- Gate de datos: `load_curriculum` **25 conceptos / 31 quests** (la `-c`
  NO añade concepto/quest — flag, no comando).
- Bundle fresco: `test_bundle_fresco` verde; 50 ficheros, 488.3 KiB.
- Determinismo: `generate(42,5,volcado_rescatado=True)` byte-idéntico ×2.
- Web `node --check web/app.js` OK; `CUSTODIA/TRONCAL_STATIC` intactas.

## Recámara de la zona (solo si sobra turno)

- 🧭47 CERRADA como medida: el stock de Gris 0% + lectura intercalada 0% delta
  (PR #82, medido con N=20/500 + README 25/09). NO repetir el harness — la
  recámara ahora es la DECISIÓN de Gwyn (+0.3 tenue a la lectura si acaso).
- `tail`/`stat` del `pts0` custodia (recámara desde 23/09, sin tarea viva).

---
*(Gwyn 25/09: la Subestación 4/4 huellas + lectura + 6º estado queda
COMPLETA — no proponer verbos nuevos sobre ch5. Que la zona teste el
PESO de la lectura (factura frugal + jerarquía lente), no la mecánica
que ya está en verde casi 40 tests.)*
