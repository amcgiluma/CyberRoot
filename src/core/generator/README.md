# generator/ — Generación procedural ENSEÑANTE

> **Qué hace:** convierte `{capítulo, Pacto activo, karma, boons del jugador,
> seed}` en una incursión jugable: grafo de salas + piel instanciada (FS,
> nombres, IPs, puertos, topología). Determinista ante la misma seed.
>
> Contrato normativo: `docs/DESIGN.md` §4.5 · muestreo pedagógico §6.4 ·
> arquitectura: `../ARCHITECTURE.md` §2.4.

## Reglas duras que implementa
1. **Un solo grafo de verdad**: lee pools de `curriculum/`; comprueba el pool
   DESBLOQUEADO del jugador, nunca la etiqueta del capítulo (§6.4.1) — nadie
   recibe un reto sin sus herramientas.
2. **Sesgo pedagógico**: conceptos dominados + EXACTAMENTE 1 nuevo/en práctica;
   proporción dominados:nuevo ≈ 1:1 (cap. 1) → 4:1 (cap. 6) (§6.4.2).
3. **Salas tipo**: explorar / firewall / datos / elite / evento (§6.4.3). La
   PLANTILLA la fija el capítulo; la INSTANCIA la seed.
4. **Validación canónica OBLIGATORIA** (§6.4.4): toda sala se auto-resuelve con
   una secuencia canónica antes de ofrecerse; la secuencia SOLO usa conceptos
   del pool permitido. Sala irresoluble = bug de generación, no reto.
5. **Karma y Pacto NO tocan el pool** (§6.4.5): modifican presión (ruido base,
   rotación de logs), botín y textos — jamás los conceptos exigidos.
6. El RNG jamás decide si un comando funciona (semántica determinista §4.5).

## Entradas / salidas
- ENTRADA: dict `{chapter_id, pacto, karma_value, unlocked_boons, seed}` +
  plantillas de campaña (`src/data/chapters/`).
- SALIDA: `IncursionInstance` serializable — grafo de salas tipadas con su FS
  virtual instanciado, solución canónica adjunta (para validación/harness),
  parámetros de vigilancia inicial.

## Cómo se testea
- Misma seed + mismos inputs → instancia IDÉNTICA (test de determinismo).
- Barrido de N seeds × 7 capítulos: TODA sala generada pasa validación
  canónica (test masivo headless — el favorito del harness).
- La solución canónica nunca exige conceptos fuera del pool (test automático).

## Dueño
Ornstein (`feat/engine`, junto a `engine/`). Es el corazón del harness de
playtest: `tools/harness/` barrerá este módulo con miles de seeds.
