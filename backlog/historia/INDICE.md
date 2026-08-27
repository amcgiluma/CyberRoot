# historia/ — La narrativa de CyberRoot (carpeta de trabajo de Manus)

> ✍️ **Manus** (03:00) escribe aquí la historia del juego, contra la espina
> fija de `docs/DESIGN.md` §2 (12 beats) y las reglas operativas §2.6.
> Estructura definida en AGENTS-PLAN §6.1 — este índice la materializa.

## Mapa

```
historia/
  INDICE.md        ← ESTE fichero: estado del arco narrativo
  PERSONAJES.md    → fichas de voz ANTES de dar diálogo a nadie (regla §2.6.5)
  ESCENARIOS.md    → lugares: Subestación, tres anillos, nodos tipo del Grid
  CAPITULOS/       → un fichero por capítulo-campaña (0–6), esquema → texto
  FRAGMENTOS.md    → botín narrativo H1/H2 con orden fijo por capítulo (§9 P5)
```

## Flujo de entrega
Manus escribe AQUÍ. Para entrar al juego, sus textos viajan a `src/data/story/`
con claves JSON — lo hace el ejecutor integrador (no Manus), para no romper
formato. Piezas listas para integrar se marcan `[LISTA]` en INDICE.md.

## Reglas de oro (resumen — el detalle manda en DESIGN)
1. Cada encargo = objetivo técnico + beat narrativo + decisión de karma +
   gancho post-mortem (§2.6.1). Sin barrera técnica no hay avance de trama.
2. Morir SIEMPRE avanza: cola de eventos con líneas nuevas por caso (§2.6.2).
3. Ficha de voz obligatoria antes de escribir cualquier personaje (§2.6.5),
   con fila «nunca diría». Test del nombre tapado.
4. Objetos de lore: dato técnico arriba, grieta humana abajo, un número
   concreto por descripción. Cero adjetivos atmosféricos.
5. Todo en español de España; comandos/salidas técnicas en forma real.

## Estado — FUNDACIÓN (27/08, primer turno de Manus)
- Beats 1–12 definidos (DESIGN §2.5). Capítulos 0–6 con necesidad narrativa
  propia (§6.1).
- ✅ Fichas de voz completas (6/6, `PERSONAJES.md`) — desbloquea todo diálogo.
- ✅ Escenarios con datos base (6/6, `ESCENARIOS.md`).
- ✅ Fragmento 1 `[LISTA]` (`FRAGMENTOS.md`). Fragmentos 2–6 pendientes.
- ✅ Capítulo 0 abierto (`CAPITULOS/00-la-firma.md`, beats 1–3).
- PENDIENTE bloqueante para cap. 6: worldbuilding del censo (§9, dueño Manus
  en Fase 1). No bloquea capítulos 0–4.