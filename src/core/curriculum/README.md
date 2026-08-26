# curriculum/ — El grafo de conocimiento único

> **Qué hace:** mantiene el DAG de conceptos Linux (~60 boons en 8 familias)
> que alimenta A LA VEZ el currículo de capítulos y el generador procedural.
> Una sola fuente de verdad: si un concepto se enseña en el capítulo 3, ninguna
> sala del capítulo 1 puede exigirlo.
>
> Normativa: `docs/DESIGN.md` §4.4 (fuentes de boons), §6.2 (reparto
> curricular), §6.4.1 · datos: `src/data/curriculum.json`.

## Responsabilidades
- Cargar y validar `src/data/curriculum.json`: familias, comandos,
  prerrequisitos (DAG sin ciclos), capítulo de ENSEÑANZA, capítulos de
  MANTENIMIENTO.
- Consultas: pool desbloqueado de un jugador (desde boons/usos registrados),
  pool de práctica de un capítulo con sesgo pedagógico (dominados:nuevo,
  repetición espaciada §6.0.4), prerrequisitos faltantes de un concepto.
- Marcar dominio: registrar usos exitosos en contexto (alimenta unlocks por
  competencia §7.5 y la tarjeta «dominio 1»).

## Familias (§6.2)
navegación (~8) · permisos (~7) · texto/pipes (~9) · procesos (~8) · red (~9) ·
auditoría/defensa (~7) · escalada/persistencia (~8) · hallazgo (~4).

## Entradas / salidas
- ENTRADA: JSON curricular + registro de usos del jugador.
- SALIDA: pools de conceptos, grafos de prerequisitos, estados de dominio.
- NO conoce salas, runs ni renders.

## Cómo se testea
- Integridad del DAG: sin ciclos, sin huérfanos, cada familia con dueño
  (capítulo de enseñanza único — cobertura verificada de §6.2).
- Sesgos: proporciones dominados:nuevo por capítulo dentro de margen.
- Un jugador SIN boon X jamás recibe un pool que exija X.

## Nota abierta (DESIGN §9)
La lista comando a comando (~60) queda validada contra lo soportado por el
sandbox real antes de congelar contenido. Dueño: Smough + Arquitecto (Fase 1).
La ESTRUCTURA del módulo no depende de esa lista.

## Dueño
Smough (`feat/sandbox`), junto a `sandbox/`: comparten la verdad de qué
comandos existen y qué semántica tienen.
