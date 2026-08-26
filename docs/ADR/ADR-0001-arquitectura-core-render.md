# ADR-0001 — Frontera core/render y mapa de módulos de CyberRoot

- **Fecha:** 26/08/2026 (Arquitecto, Fase 0)
- **Estado:** PROPUESTA para el gate de Juanma (coherente con diseño cerrado;
  nada nuevo: materializa INVESTIGACION-STACK «decisión clave CONFIRMADA»).

## Contexto
El comité debe verificar el juego de forma autónoma (regla de oro del stack):
todo testeo headless, todo determinista por seed, todo el contenido separado
del código. DESIGN.md (Pases 1–5) define sistemas con números calibrables; el
stack eligió Pyxel con core Python puro.

## Decisión
1. **`src/core/` = Python puro sin Pyxel, testeable headless.** Paquetes:
   `common`, `sandbox`, `curriculum`, `generator`, `engine`, `state`,
   `progression`, `karma`. Grafo de dependencias estricto
   (state→…→sandbox→common); `sandbox` autónomo y reutilizable.
2. **Contrato único de interacción**: comandos dict-planos entran → eventos
   observables + estado serializable salen. Render y harness consumen LO MISMO.
3. **`src/render/` = capa delgada de Pyxel**: dibuja estado, traduce input a
   comandos, cero lógica. Único paquete que importa pyxel. Riesgo nº 1 del
   stack (fuente bitmap) se ataca el día 1.
4. **Contenido en `src/data/` (JSON)**: currículo, campañas, catálogos,
   textos. Los números ⚠️ v1 del diseño son datos, no código — el harness
   calibra sin PRs de lógica.
5. **Vigilancia automática de la frontera**: `tests/architecture/` (core no
   importa pyxel; RNG siempre inyectada; render no muta estado).
6. **Reparto anti-colisión por rama**: Smough=`feat/sandbox`
   (sandbox+curriculum), Ornstein=`feat/engine` (generator+engine+common+
   tools/harness), Seath=`feat/meta-ui` (state+progression+karma+render+
   assets). Una rama nunca toca rutas de otro dueño.

## Consecuencias
- Tests = especificación ejecutable; el harness extiende pytest a escala
  (miles de seeds). Sala irresoluble = rojo automático (§6.4.4).
- Portar a pygame-ce si Pyxel falla (plan B del stack) = reescribir SOLO
  `render/` + `assets/`.
- Coste: una capa más de indirección (comandos/eventos). Aceptado: es el precio
  de la verificabilidad autónoma, requisito duro del proyecto.

## Referencias
`docs/INVESTIGACION-STACK.md` · `docs/DESIGN.md` §§3–8 · `src/core/ARCHITECTURE.md`
(normativa operativa) · `docs/PROJECT-MAP.md` §3 (dueños).
