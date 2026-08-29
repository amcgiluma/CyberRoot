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
- ✅ Fragmento 1 `[LISTA]` (`FRAGMENTOS.md`). Quedan 3–6 por escribir.
- ✅ Capítulo 0 (`CAPITULOS/00-la-firma.md`, beats 1–3) — prosa RETOCADA el
  28/08 según decisión D1 de Gwyn: `cp` enseñado en la escena técnica (🧭1,
  alineado con la sesión canónica del sandbox) y run 0 falible en prosa (🧭2:
  el bloque del post-mortem de la primera run ya no es rama muerta).
- ✅ Capítulo 1 «Los Muelles» (`CAPITULOS/01-los-muelles.md`, beats 3–4,
  28/08) — pacto, 5 encargos con karma, regla de la luz diegética (🧭3),
  cola de post-mortem de Ceniza, escenas de Zeta, gancho hacia el cap. 2.
- ✅ Capítulo 0 prosa↔FS REALINEADA (29/08, tarea M1): el listado tras
  `cd /srv` muestra UNA entrada (`oficina-vecinal-muelle-norte`); `/usb`
  permanece en la RAÍZ (opción B de Gwyn, 🧭2). Verificado byte a byte contra
  `src/tests/core/sandbox/test_session_cap0.py` (3/3 passed).
- ✅ Fragmento 2 «La pulsera» `[LISTA]` (`FRAGMENTOS.md`, 29/08) — piel
  HOSP-47-C propuesta por Havel; NHC 47-C-0191, fecha de admisión = día de
  la firma; sostiene H1 y H2 a la vez.
- ✅ Capítulo 2 «Facturas» (`CAPITULOS/02-facturas.md`, beats 5,
  29/08) — 5 encargos (`story.ch2.e1`–`e5`: 2 azules, 1 gris, 1 rojo, 1 de
  cierre), pipes como primera sinergia, escenas de Ceniza/Zeta, cola de
  post-mortem con líneas de Auditor por perfil kármico, la Lista nombrada
  por Ceniza y gancho al cap. 3 (el proceso vivo en la subestación
  secundaria). Bloque de terminal con pipes: contrato pedagógico pendiente
  de verificación hasta que el sandbox soporte tuberías (nota del
  integrador).
- PENDIENTE bloqueante para cap. 6: worldbuilding del censo (§9, dueño Manus
  en Fase 1). No bloquea capítulos 0–4.
- SIGUIENTE (dirección Gwyn, 28/08): fragmento 3 (contrato de alquiler a
  nombre de nadie) con el cap. 3 «Bombas» cuando toque colchón del Acto 2.
- DECISIÓN Gwyn (27/08, 🧭5): el ÚLTIMO fragmento de la cadena está
  GARANTIZADO al completar la cadena final del cap. 6 (ver DESIGN §6.1).
  Materializarlo en `FRAGMENTOS.md` cuando se escriba la cadena.