# Estructura del repo y de los agentes — CyberRoot

> Fecha: 23/08/2026 · Estado: propuesta

## Estructura de carpetas (propuesta para el repo del juego)

```
CyberRoot/
├── README.md                 # Identidad, estado, cómo contribuye el sistema
├── LICENSE                   # (decidir: MIT, etc.)
├── .gitignore
├── docs/
│   ├── DESIGN.md             # Documento de diseño del juego (historia, niveles)
│   ├── BRAINSTORM.md         # Ideas y exploración
│   ├── ADR/                  # Decisiones de arquitectura (fecha + razón)
│   └── WORKLOG.md            # Registro diario del desarrollo
├── agents/
│   ├── planificador.prompt   # Prompt/cron del planificador (Grok 4.6)
│   ├── ejecutor-A.prompt     # Ejecutor de módulo A (DeepSeek)
│   ├── ejecutor-B.prompt
│   ├── ejecutor-C.prompt
│   ├── revisor-filtro.prompt # (DeepSeek)
│   └── revisor-diseno.prompt # (modelo fuerte)
├── backlog/
│   └── TODO.md               # La "libreta": tareas con estado
└── src/                      # Código del juego
    ├── (módulos asignados: A, B, C…)
    └── tests/
```

## Asignación de módulos a ejecutores
(Se define en la fase de diseño técnico. Ideal: cada ejecutor toca un
subconjunto de `src/` cuasi-disjunto para no pisarse en git.)

## Zonas privadas vs públicas
- TODO, agentes y diseño también se suben (transparencia decidida por Juanma),
  pero jamas credenciales ni tokens (ver `.gitignore`).

## Proceso diario (resumen)
1. Idees cron recoge dirección.
2. Planificador convierte en plan ordenado dividido por módulos.
3. Ejecutores implementan cada uno en su franja y zona.
4. Revisores (2 modelos) validan y cierran el PR.
5. Todo queda reflejado en `WORKLOG.md` y `TODO.md`.