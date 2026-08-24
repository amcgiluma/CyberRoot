# INVESTIGACIÓN — Stack técnico y referencias (CyberRoot)

> Fecha: 24/08/2026 · Estado: **DEFINITIVO para Fase 0** (investigación profunda completada).
> Sustituye al borrador preliminar del 23/08. Todas las afirmaciones clave han sido
> verificadas contra fuentes primarias (repo oficial Pyxel vía GitHub API/raw,
> PyPI, repos oficiales de Textual y pygame-ce) el 24/08/2026.
> Pendiente de decisión final por Juanma (gate de Fase 0), pero la recomendación
> es sólida y argumentada. Lo no verificable está marcado con ⚠️.

## Objetivo de la investigación
Elegir el motor y la arquitectura de forma informada para un juego de
**aprendizaje de Linux + seguridad (Blue/Red Team)** con estética hacker
de terminal y pixel-art, de **10–15 horas de juego**, roguelite estilo Hades
(run → base → run) con dopamina tipo Balatro, que además un sistema de
agentes autónomos pueda **testear a sí mismo sin pantalla (headless)**.

**Regla de oro que condiciona todo:** el comité de IAs debe poder ejecutar y
validar el juego autónomamente en cada turno. Cualquier stack que exija
interacción gráfica humana para verificar lógica queda descartado.

---

## Motor recomendado: Pyxel — verificado a fondo

- **Qué es:** motor retro de pixel-art para Python (núcleo en Rust), inspirado
  en consolas retro: **16 colores**, 4 canales de sonido, resolución definida
  por el desarrollador (p. ej. 160×120 escalada).
- **Licencia:** MIT (verificado en repo y LICENSE). Gratis, sin royalties.
- **Salud del proyecto:** 17.758★ · última release **2.9.9** en PyPI · último
  push 12/08/2026 (mantenimiento activo, ritmo de releases mensual).
  Requiere **Python ≥ 3.11** — la máquina local tiene 3.11.15 ✅.
- **Web/wasm CONFIRMADO:** el repo incluye ~148 ficheros bajo `wasm/`+`web/`
  (runtime Pyodide, showcase, editor, code-maker). Los ejemplos corren en el
  navegador desde el propio README. La FAQ advierte que **Code Maker no soporta
  proyectos multi-fichero** → para CyberRoot la web sirve como *demo jugable*
  embebible, no como entorno de desarrollo. Desarrollo local normal.
- **Paleta:** los 16 colores se pueden **redefinir en runtime** vía
  `pyxel.colors` (lista Python, ops nativas) y `load_pal()/save_pal()` +
  ficheros `.pyxpal` para el editor. La limitación es estética, no técnica:
  podremos tener una paleta "fósforo verde/ámbar CRT" propia coherente.
- **Input:** teclado + ratón (`mouse_x/mouse_y`, botones) + gamepad. El ratón
  cubre el mapa de nodos clicables; el teclado, la terminal.

### ⚠️ Riesgos conocidos (no invalidan la elección, hay que gestionarlos)
1. **⚠️ Bus factor = 1.** El propio README lo dice: *"this project is developed
   by one person"* (kitao). Si el proyecto se abandona, quedamos atados a un
   motor congelado. Mitigación: el núcleo del juego vivirá en `core/` Python
   puro; portar el render a pygame-ce sería factible si algún día hiciera falta.
2. **⚠️ Texto pixelado a resoluciones bajas:** Pyxel no trae tipografías TTF;
   su fuente builtin es limitada (la v2.9.x añadió custom fonts, pero dibujar
   texto legible tipo consola requiere una fuente bitmap propia bien elegida).
   Es EL riesgo visual del proyecto: la terminal in-game ES texto. Plan: font
   bitmap 5×7 o similar desde el día 1, validada con capturas.
3. **⚠️ Rendimiento de draw calls por frame:** para HUD/mapa/terminal está de
   sobra (juegos más complejos corren bien), pero no hay que animar cientos de
   sprites simultáneos. No aplica a nuestro género.

## Alternativas evaluadas (comparativa verificada)

| Opción | Veredicto | Razón (datos) |
|---|---|---|
| **Pyxel** | ✅ **ELEGIDO** | Pixel-art real, MIT, wasm para demo web, `init(headless=True)` oficial, un solo lenguaje (Python) |
| **Textual/rich (TUI)** | ❌ descartado para el look | Excelente framework (37k★, MIT, apps en navegador vía `textual serve`, también MIT): PERO es dashboard de texto, NO pixel-art. Se descarta como motor principal… |
| ↳ Textual como herramienta auxiliar | 💡 uso puntual permitido | …pero puede usarse fuera del juego (p. ej. visores del harness de testing) sin comprometer nada. No es parte del stack del juego. |
| **Godot 4** | ❌ descartado | Potente, y el testing headless existe (gdUnit4/GUT con CLI + GitHub Actions documentados), PERO: GDScript/escenas = otro ecosistema para el comité, tests headless con known issues de flakiness en CI (issues abiertos sobre ejecución fiable headless), y sobre-ingeniería para un juego 2D UI-driven. El coste de testeo autónomo sube mucho. |
| **pygame-ce** | 🥈 plan B serio | Fork comunitario activo (último push 23/08/2026, SDL2, MIT/LGPL según componentes). Más flexible que Pyxel (colores ilimitados, TTF fácil) pero MUCHO más trabajo manual para lograr el look retro (paleta, escalado integer, chiptune). Es la ruta de escape documentada si Pyxel falla. |
| **Motores "hacking simulator" open source** | ❌ no como base | Ver abajo: son referencias estéticas, superficies de animación sin motor educativo. |

## La decisión clave de arquitectura: separar core de render — CONFIRMADA

El borrador proponía separar `core/` (lógica pura testeable) de `render/`
(Pyxel). **Veredicto: CONFIRMADA, y reforzada con dos hallazgos nuevos:**

1. **Pyxel soporta modo headless OFICIALMENTE**: `pyxel.init(..., headless=True)`
   — *"Run without a window"* (api-reference.md oficial, línea 27). Esto significa
   que incluso el bucle de render puede correr sin pantalla en CI/agentes, y que
   `render/` nunca será un obstáculo para el testing autónomo.
2. **Patrón command explícito**: toda acción del jugador entra al core como un
   comando (`{"cmd": "exec", "argv": ["ls", "-la"]}` o pulsación mapeada), y el
   core devuelve eventos observables. Así:
   - `pytest tests/core/` verifica niveles resolviéndolos como un jugador
     (secuencias de comandos → estado final esperado). SIN ventana, SIN Pyxel
     importado siquiera: `core/` no depende del motor.
   - El harness de playtesting (Ornstein) puede lanzar cientos de runs headless
     midiendo resolubilidad/duración/balance con datos.
   - Un mismo core podría montarse luego sobre otro render (pygame-ce) sin
     tocar la lógica.

```
src/
  core/   → estado, niveles, parser de comandos, RNG seedeada, progreso/meta (Python puro, 0 deps de motor)
  render/ → adaptador fino de Pyxel: dibuja estado + traduce input→comandos
  tests/  → pytest sobre core (headless) + smoke tests de render (opcional, headless=True)
```

Reglas de la frontera (para el Arquitecto del 27/08):
- `core/` NO importa pyxel jamás (test de arquitectura: import-linter o test tonto).
- RNG **siempre seedeada** → runs reproducibles = tests deterministas = el agente
  puede reproducir un bug exacto.
- Guardado/carga de partida como dato plano serializable (JSON/dict), no objetos opacos.
- El render consulta el estado; nunca lo muta directamente (todo pasa por comandos).

## Referencias de mecánicas de "aprender sin deberes" (fuentes)
- **Terminus (MIT)**: RPG de terminal con hint inicial; el jugador explora
  y aprende comandos por uso. Referencia directa de "aprender jugando".
- **OverTheWire / Bandit**: misiones de shell reales, dificultad sin
  "hand-holding". Bueno para retos avanzados.
- **CodeCombat**: gamifica programación; aprende resolviendo puzzles.
- **Root Me**: plataforma de retos de seguridad (tras dominar lo básico).
- **Conclusión transversal (se mantiene, sigue siendo válida):** los que
  FUNCIONAN dan el objetivo por delante y enseñan el skill por necesidad;
  los que fallan son "cuestionarios con skin".

## Arquitectura de referencia (hacking-simulator open source)
- Los proyectos "HACKNET-like" (JS/HTML) muestran: terminal con efecto máquina
  de escribir, barras de progreso falsas, scrolling de datos, prompt de comandos.
  Solo referencia estética, no de arquitectura (su core es superficial).
- ⚠️ Matiz nuevo (24/08): en el topic `hacking-simulator` de GitHub abundan
  simuladores tipo **KaliNexus** (FS virtual + terminal en navegador). Su FS/
  parser de comandos SÍ es útil como referencia *conceptual* de modelado de un
  filesystem virtual mínimo (cd/ls/cat/grep...), aunque estén en JS. Para
  CyberRoot: modelar el FS virtual dentro de `core/fs.py` como árbol serializable.

## Dopamina tipo Balatro — qué copiar (fuente: análisis de diseño 2025)
Del análisis de diseño de Balatro (Apple Design Award 2025, LocalThunk solo-dev):
- **El juice ES el juego, no decoración**: quita animaciones y sonidos a Balatro
  y queda una calculadora. Cada evento de puntuación apila canales simultáneos:
  shake de pantalla + partículas + números rodantes + SFX.
- **Feedback como canal de datos**: la intensidad del shake comunica magnitud
  ANTES de leer el número. En CyberRoot: combos de comandos, rachas sin pistas,
  escaneos exitosos → escala visual/sonora proporcional a la hazaña.
- **Enseñar mostrando el PORQUÉ**: cada bonus se activa secuencialmente con
  callout visual (qué carta/joker disparó qué). En CyberRoot: cuando un comando
  encadena efectos, mostrar la cadena paso a paso (¡esto también ENSEÑA Linux!).
- **Estética nacida de la restricción**: el look CRT de Balatro nace de una
  limitación, no de un pipeline de arte. Nuestra restricción (16 colores Pyxel +
  scanlines) es la MISMA oportunidad de identidad visual. Coherencia total: hasta
  los menús viven en la ficción CRT.
- Traducción concreta para Pyxel: paleta CRT propia, overlay de scanlines
  (dibujable cada N líneas), screen-shake barato (offset aleatorio decayente),
  números flotantes con easing, SFX chiptune de 4 canales para aciertos.

## Implicaciones para el sistema de agentes
- Tests de core = el "verificador" autónomo de cada nivel (el agente ejecuta
  `pytest`, comprueba que el nivel es resoluble, y así cada PR queda validado).
- **Headless doble**: `core/` ni siquiera necesita Pyxel instalado; y si se quiere
  probar el render en CI, `pyxel.init(headless=True)` lo permite oficialmente.
- El render se desarrolla después/paralelo, con pautas visuales claras.
- Cada ejecutor puede tocar `core/` o `render/` por separado (sin colisión).
- Harness de balance (Ornstein): runs headless con seeds fijas → métricas de
  duración/dificultad por nivel. Posible gracias a RNG seedeada del core.

## Rol en el documento de diseño
Este research alimenta el **DESIGN.md** (historia, capítulos, niveles, stack,
mapa) que se escribirá en la fase de planning. Decisiones que quedan para el
gate de Juanma:
1. Aprobar **Pyxel como stack definitivo** (recomendación: SÍ, con los riesgos
   ⚠️ aceptados y plan B pygame-ce documentado).
2. Nombre del juego.
3. (Nuevo) Confirmar la paleta CRT como identidad visual desde el día 1.
