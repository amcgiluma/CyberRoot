# 🔬 Zona de testeo — 25/09 (definida por Gwyn el 24/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base post-merge 24/09: suite **818 passed /
> 0 failed** (809+9+0+0, deltas verificados por Artorias + ensayo worktree,
> re-verificados por Gwyn tras los 3 merges), gate **25 conceptos / 31
> quests** intacto, bundle **50 ficheros (481.3 KiB)** regen canónico. PRs
> #78/#79/#80 MERGEADOS. NADA retenido.

## Prioridad 1 — E2 «grep del intruso» (NUEVO, PR #78): la LECTURA del díptico

- **Dónde:** `abrir_encargo(c,'story.ch5.e2',{'c.cat','c.grep','c.scp'},42)`
  abre E2 en la Subestación — ahora con `grep` permitido
  (`DEFAULT_CH5E2_COMMANDS = (cat,scp,ps,grep)`).
- **Qué verificar:**
  (a) e2 abrible SOLO con `c.grep` en knowledge; sin él → rechazo honesto
  `missing ['c.grep']` (Alumnos 24/09: NO es fricción, es pedagogía — el
  gate es la matricula del día).
  (b) `ps aux | grep censo` → exit 0, UNA línea
  (`censo --vigilar-censo START 03:14`) + ruido honesto (`grep:2`, `ps:1`).
  (c) `grep ceniza` → exit 1 (motivo correcto: ceniza no delata nada).
  (d) `grep -i censo` veterano → exit 0 (ataljo, no canon).
  (e) Frontera 127 honesta: `chmod` y `kill` en e2 → `command not found`.
- **Por qué importa:** la Subestación pasa de 4/4 huellas a 4 huellas + 1
  lectura forense. Pregunta de sabor (OSCAR): ¿delatar al vigilante con
  `grep` se SIENTE distinto a condenarlo con `kill` — inteligencia vs fuerza?

## Prioridad 2 — Lente web del propietario (NUEVO, PR #80): 5º estado del semáforo

- **Dónde:** web `?chapter=5`, insignia `#ch5-e4-owner` bajo la tabla
  custodia, con `get_ls_owner()`/`get_chown_history()` (leen FS, nunca
  ejecutan).
- **Qué verificar:**
  (a) Boot limpio → `operator:operator` neutro `#95a5a6`.
  (b) `chown gris:apagados pts0` → azul `#5dade2` (DUEÑO entregado).
  (c) `chown root:root pts0` (o post-azul) → rojo `#e74c3c` (RETOMA).
  (d) `restartSameSeed` limpia la insignia también.
  (e) Fuera de cap. 5 → insignia oculta; caps 1-4 sin ensuciar; consola
  limpia en los 3 estados + post-restart.
- **Por qué importa:** el tríptico web (intruso + veredicto + propietario)
  cierra con la misma regla: la lente MIRA, no toca. Pregunta de sabor:
  ¿-R azul (gris va a vivir) vs rojo (el Censo vuelve) pesa distinto de
  verlo en web que en post-mortem?

## Smoke sí o sí

- Suite completa: `PYTHONPATH=src .venv/bin/python -m pytest src/ -o addopts= -q`
  → **818 passed / 0 failed** (delta +9 del engine de ayer). Si NO da 818:
  circumstancia (re-correr desde la raíz del repo).
- Gate de datos: `load_curriculum` **25 conceptos / 31 quests** (e2
  `requires ['c.cat','c.grep','c.scp']` coherente — verificado por
  Gwyn 24/09 vía Python real).
- Bundle fresco: `test_bundle_fresco` verde; 50 ficheros, 481.3 KiB.
- Determinismo: `generate(42,5,volcado_rescatado=True)` byte-idéntico ×2.
- Web `node --check web/app.js` OK; `CUSTODIA/TRONCAL_STATIC` intactas.

## Recámara de la zona (solo si sobra turno)

- 🧭47: el stock de Gris sigue 0% contraste en el harness de Smough
  (estático) — si Seath trabaja en lógica kármica de stock, medir el
  contraste ANTES/AFTER con el mismo `--micro-karma` (no escribir prosa).
- 6º estado `grep censo` en `#custodia-intruso` (hueco honesto de Seath):
  SOLO si Gwyndolin lo planifica como tarea.

---
*(Gwyn 24/09: zone limpia — dos prioridades máximas (regla §4), smoke
canónico, sin deuda nueva que probar. Oscar empieza por P1: `grep` es el
primer verbo LECTOR de la Subestación — que se sienta forense, no táctico.)*
