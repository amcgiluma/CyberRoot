# progression/ — Metaprogresión: el Espejo de Gris

> **Qué hace:** todo lo que persiste entre runs: ramas del espejo (Hardware /
> Oficio / Red), recuerdos equipables, tienda de objetos de Gris, economía
> (créditos + favores narrativos), desbloqueos por competencia y récords
> personales.
>
> Normativa: `docs/DESIGN.md` §4.2–4.3 (regla dura y espejo), §7.5–7.6
> (unlocks/récords) · `../ARCHITECTURE.md` §2.7.

## La regla dura que este módulo custodia
**El espejo da conveniencia e identidad de build, nunca conocimiento**
(§4.2): ninguna compra sustituye a un comando que el jugador no sabe usar.
Si una mejora propuesta rompe esto, se corta en diseño, no en código.

## Responsabilidades
- Compras y equipamiento (objetos ~12, perks ~8, recuerdos por NPC).
- Desbloqueos POR COMPETENCIA (§7.5.3): usa bien X en contexto → siguiente
  tarjeta de la familia; JAMÁS por grind de créditos.
- Récords personales persistentes (mejor combo, pipeline más largo, sala más
  valiosa — §7.6). Sin leaderboard, nunca.
- Señales kármicas de stock (§3.3 canal 1): el inventario ofertado por Gris
  depende del perfil — la lógica lee `karma.py`; los textos viven en `data/`.

## Cómo se testea
- Unlock por competencia: sin uso real NO hay unlock aunque sobren créditos.
- Economía: comprar/equipar/cobrar — aritmética exacta y persistente.
- Stock contrastado: perfil azul vs rojo forzados → ofertas distintas
  (semilla del protocolo §8.6; la medición fina es del harness).

## Dueño
Seath (`feat/meta-ui`).
