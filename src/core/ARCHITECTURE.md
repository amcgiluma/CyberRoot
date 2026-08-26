# ARCHITECTURE — core/ (decisiones normativas de Fase 0)

> Fuente: `docs/INVESTIGACION-STACK.md` («La decisión clave de arquitectura:
> separar core de render — CONFIRMADA») + reglas operativas de `docs/DESIGN.md`.
> Este documento define la frontera y los contratos internos. Los ejecutores
> implementan DENTRO de estas líneas; cambiarlas = propuesta en
> `backlog/mejoras/pendiente/propuestas.md` o ADR nuevo.

---

## 1. La frontera (regla nº 1 del proyecto)

```
        comandos (dicts planos)            eventos observables
render ───────────────────────────────► core ──────────────────┐
(harness usa la MISMA puerta)                                  │
       ◄───────────────────────────────────────────────────────┘
        lee GameState serializable
```

1. **`core/` NO importa `pyxel` jamás.** Vigilado por
   `src/tests/architecture/test_core_no_pyxel.py` (falla si aparece el import).
2. **Todo entra como comando** (`{"cmd": "exec", "argv": [...]}` o acción UI);
   el core responde con `Event`s observables. El render consulta estado, nunca
   lo muta directamente.
3. **RNG SIEMPRE seedeada** (`common/rng.Rng(seed)`): runs reproducibles,
   tests deterministas, bugs reproducibles por el harness. Prohibido `random`
   global; cada subsistema deriva sus sub-semillas de la semilla de run.
4. **Semántica determinista** (DESIGN §4.5): el RNG jamás decide si un comando
   funciona. La incertidumbre vive en el mapa y la vigilancia, nunca en la
   física del sandbox.
5. **Guardado como dato plano**: `GameState` ↔ JSON/dict, sin objetos opacos ni
   referencias vivas. Un save debe poder escribirse a disco a mano.

## 2. Paquetes (dependencias permitidas →)

```
state ──► karma, progression ──► engine ──► generator ──► curriculum ──► sandbox ──► common
```

- Las flechas son IMPORTS PERMITIDOS: `sandbox` no sabe que existe `engine`;
  `engine` no importa `render` ni `progression` directamente (los recibe como
  parámetros o los orquesta `game.py`).
- **`sandbox/` es autónomo y reutilizable**: FS virtual + shell sin concepto de
  partida. Si mañana hay otro modo (tutoriales sueltos), se usa solo.

### 2.1 `common/` — cimientos (dueño: Ornstein)
`rng.py` (RNG determinista), `events.py` (`Event(tipo, datos)` + tipos
compartidos), `types.py`, errores. Sin lógica de juego. Todo lo demás importa
de aquí; aquí no se importa nada del core salvo stdlib.

### 2.2 `sandbox/` — el Linux de mentira que dice verdades (dueño: Smough)
- `fs.py`: árbol de filesystem virtual serializable (nodos, permisos, dueños,
  tamaños, timestamps). Referencia conceptual: simuladores tipo KaliNexus
  (INVESTIGACION-STACK). El generador crea instancias; el sandbox las ejecuta.
- `shell.py`: parser argv + expansión básica (globs, pipes, redirección,
  variables) → operaciones sobre `fs.py`/procesos virtuales. Salida estilo
  terminal real (si el sistema real emite inglés, se emite inglés — DESIGN §2.6.8).
- `commands/<familia>.py`: un módulo por familia del currículo (§6.2 de
  DESIGN): navegación, permisos, texto/pipes, procesos, red, auditoría,
  escalada. Cada comando declara qué conceptos usa (para el pool del generador)
  y su coste de «ruido» (subida de detección).
- Red simulada mínima para cap. 4+ (`ssh`/`scp`/`ss` entre hosts virtuales):
  modelo de nodos alcanzables, sin sockets reales jamás.
- **Salidas:** resultado del comando (stdout-like, exit code) + efectos sobre
  el FS/procesos + ruido generado.
- **Tests:** golden tests de salida por comando; semántica contra casos reales
  documentados; determinismo ante misma seed.

### 2.3 `curriculum/` — el grafo de verdad único (dueño: Smough)
- Carga `src/data/curriculum.json` (~60 boons en 8 familias con prerrequisitos,
  DESIGN §6.2). UN solo DAG que alimenta currículo y generador (§6.4.1).
- Responde: ¿qué conceptos tiene desbloqueados este jugador? ¿qué pool de
  práctica corresponde a este capítulo (sesgo dominados:nuevo §6.4.2)?
- No conoce runs ni salas: es conocimiento puro.

### 2.4 `generator/` — generación procedural ENSEÑANTE (dueño: Ornstein)
- Contrato EXACTO (DESIGN §4.5): entrada `{capítulo, Pacto activo, karma,
  boons del jugador, seed}` → salida grafo de salas + instancias de piel.
  Determinista ante la misma seed.
- Muestreo pedagógico desde `curriculum/` (§6.4.2), plantillas de sala por
  familia (explorar/firewall/datos/elite/evento, §6.4.3).
- **Validación canónica obligatoria** (§6.4.4): toda sala se auto-resuelve con
  una secuencia canónica antes de ofrecerse; irresoluble = bug de generación.
  La solución canónica SOLO usa conceptos del pool permitido (test headless).
- Karma y Pacto no tocan el pool (modifican presión/botín/textos, §6.4.5).

### 2.5 `engine/` — el motor roguelite (dueño: Ornstein)
- Ciclo run: mapa de nodos → entrar sala → resolver → extraer/detectar.
- Detección/vigilancia: % sube por acciones ruidosas (regla de luz §6.0.2),
  nunca por relojes artificiales (§7.9).
- Economía DATOS×COMBO (§7.1), apuestas de run (§7.3), liquidación parcial al
  ser expulsado (§7.7).
- Cola de eventos post-run hacia el Hub: post-mortem siempre primero (§4.7).
- Los números ⚠️ v1 del diseño viven en constantes legibles/documentadas, para
  que Ornstein los calibre con el harness SIN tocar lógica.
- **El harness vive fuera del juego**: `tools/harness/` (mismo dueño) consume
  esta API: corre N runs headless con seeds fijas y saca métricas
  (resolubilidad, duración, contraste kármico §8.6).

### 2.6 `state/` — el estado agregador (dueña/o: Seath)
- `GameState`: partida completa (jugador, run actual si la hay, Hub, unlocks,
  historial kármico, récords). Serializable JSON ida y vuelta.
- Save/load atómico; versionado de saves desde el día 1 (`schema_version`) —
  migrar saves viejos será necesario y barato si se hace pronto.
- Único punto donde las piezas ensamblan; expone la fachada que consume
  `main.py`.

### 2.7 `progression/` — metaprogresión (dueña/o: Seath)
- Espejo de Gris (3 ramas: Hardware/Oficio/Red, §4.3), recuerdos equipables,
  tienda de objetos, economía de créditos/favores.
- Desbloqueos POR COMPETENCIA, nunca por grind (§7.5.3): registrar usos reales
  y disparar unlock cuando toca.
- Regla dura §4.2: nada de esto sustituye conocimiento; acelera/personaliza.
- Récords personales persistentes (§7.6), sin leaderboard.

### 2.8 `karma/` — contabilidad Blue/Red (dueña/o: Seath)
- Entradas `{momento, acción, peso, timestamp}`; valor K = suma ponderada de
  las últimas N=8 (§3.3); umbrales T_alto/T_bajo como constantes ⚠️ v1.
- Expone consultas: banda actual (azul/mixta/roja), requisitos de finales
  (§3.4.1), qué canal de feedback dispara cada cruce.
- Serializable y testeable; JAMÁS se dibuja como barra ética (eso es cosa del
  render, y ni siquiera entonces: el mundo reacciona, §3.2).

## 3. Convenciones

- Python ≥ 3.11 (requerido por Pyxel; la máquina local tiene 3.11.15 ✅).
- Tipos anotados en toda función pública; dataclasses para datos, no dicts
  anónimos dentro de core (en las FRONTERAS sí viajan dicts planos).
- Docstrings cortos con referencia al § de DESIGN.md que norma el comportamiento.
- Textos visibles del juego: NUNCA hardcodeados en core — viven en `data/`.
  Core carga y devuelve claves de texto; el render las resuelve.
- Sin I/O de red, sin reloj real (todo tiempo de juego es tiempo simulado),
  sin globals mutables. Dependencia externa de runtime objetivo: cero
  (stdlib only) para que instalar Pyxel sea opcional para testear core.

## 4. Tests (resumen — detalle por paquete en su README)

| Suite | Qué garantiza |
|---|---|
| `tests/architecture/` | core no importa pyxel; RNG inyectada; frontera de imports |
| `tests/core/sandbox/` | semántica de comandos (golden outputs) |
| `tests/core/generator/` | determinismo por seed; TODA sala resoluble con pool válido |
| `tests/core/engine/` | loop run completo headless: éxito y expulsión; combo/economía |
| `tests/core/state/` | save/load ida-y-vuelta idéntico |
| `tests/core/karma/` | N=8, bandas, condiciones de finales |

## 5. Decisiones abiertas (no bloqueantes, dueño Fase 1)

1. **Lista comando a comando de los ~60 boons**: validar contra lo soportado
   por el sandbox real (DESIGN §9). Dueño: Smough + Arquitecto. Bloquea
   contenido, no estructura.
2. **Formato exacto de `Event.ttipo`**: catálogo cerrado cuando render y
   harness lo consuman por primera vez (Seath/Ornstein acuerdan en el primer PR
   cruzado).
3. **import-linter formal** vs test tonto: empezar con test tonto (cero deps);
   migrar a import-linter si el grafo crece.
