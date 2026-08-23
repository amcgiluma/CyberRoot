# INVESTIGACIÓN — Stack técnico y referencias (CyberRoot)

> Fecha: 23/08/2026 · Estado: **PRELIMINAR — primeras ideas rápidas.**
> ⚠️ Esto NO es la investigación definitiva. Son hipótesis iniciales para orientar
> el arranque. La investigación profunda y completa la realizarán los agentes
> durante los primeros 3–4 días del proyecto (ver AGENTS-PLAN). Cualquier
> conclusión aquí puede ser revisada/ampliada por ese research.
> Fuentes consultadas en vivo (web). Decisión de stack indicativa, no cerrada.

## Objetivo de la investigación
Elegir el motor y la arquitectura de forma informada para un juego de
**aprendizaje de Linux + seguridad (Blue/Red Team)** con estética hacker
de terminal y pixel-art, de **10–15 horas de juego**, que además un sistema
de agentes autónomos pueda **testear a sí mismo**.

## Motor: Pyxel (recomendado) — verificado en repo oficial
- **Qué es:** motor retro de pixel-art para Python, inspirado en consolas
  retro: 16 colores, 4 canales de sonido, paleta de 256×256.
- **Licencia:** MIT, open source, gratis. 17.8k★, mantenimiento activo
  (última release 2.9.9 con soporte wasm).
- **Web:** la versión web corre por WASM **sin instalar Python ni Pyxel**,
  en PC, móvil y tablet (confirmado en repo: carpetas `wasm/` + `web/`).
  → Juanma podrá jugar la demo en el navegador sin config nada.
- **Alternativas descartadas por contraste:**
  - **Godot**: potente pero GDScript + escena/árbol, cara de testear de
    forma headless por el sistema autónomo, y sobre-ingeniería para esto.
  - **Textual / rich / blessed (TUI)**: gran estética de terminal pero NO
    pixel-art ("dashboard", no juego pixel). Descartado para el look pedido.
  - **pygame**: más bajo nivel, más trabajo para el mismo resultado retro.

## La decisión clave de arquitectura: separar motor de render
El problema real del testing autónomo: un juego de ventana gráfica es
**difícil de "jugar" sin pantalla por un agente**. Solución profesional
(no una trampa): **separar el núcleo jugable del render**:

```
src/
  core/   → estado del juego, niveles, parser de comandos, lógica (puro Python)
  render/ → adaptador de Pyxel (dibuja en pantalla, input) — capa fina
  tests/  → pytest sobre core, SIN abrir ventana
```

El agente ejecuta y valida con los **tests de core** (puede "resolver" cada
nivel como un jugador y comprobar que pasa). El render es una capa delgada.
Así se consigue el pixel-art chulo Y la testabilidad autónoma. Un solo
lenguaje (Python) y un alcance manejable: coherente para un sistema
autónomo a largo plazo.

## Referencias de mecánicas de "aprender sin deberes" (fuentes)
- **Terminus (MIT)**: RPG de terminal con hint inicial; el jugador explora
  y aprende comandos por uso. Referencia directa de "aprender jugando".
- **OverTheWire / Bandit**: misiones de shell reales, dificultad sin
  "hand-holding". Bueno para retos avanzados.
- **CodeCombat**: gamifica programación; aprende resolviendo puzzles.
- **Root Me**: plataforma de retos de seguridad (tras dominar lo básico).
- **Conclusión transversal de las fuentes:** los que FUNCIONAN dan el
  objetivo por delante y enseñan el skill por necesidad; los que fallan
  son "cuestionarios con skin". Refuerza el principio rector del brainstorm.

## Arquitectura de referencia (hacking-simulator open source)
- Los proyectos "HACKNET-like" (JS/HTML) muestran: terminal con efecto
  máquina de escribir, barras de progreso falsas, scrolling de datos,
  prompt de entrada de comandos. Sirven de referencia visual/CSS, pero
  su core es superficial (animación), NO motor de juego educativo real.
  → No usarlos como base de arquitectura, solo de estética.

## Implicaciones para el sistema de agentes
- Tests de core = el "verificador" autónomo de cada nivel (el agente ejecuta
  `pytest`, comprueba que el nivel es resoluble, y así cada PR queda validado).
- El render se desarrolla después/paralelo, con pautas visuales claras.
- Cada ejecutor puede tocar `core/` o `render/` por separado (sin colisión).

## Rol en el documento de diseño
Este research alimenta el futuro **DESIGN.md** (historia, capítulos, niveles,
stack, mapa) que se escribirá en la fase de planning. Pendiente de decisión
final por Juanma sobre: Pyxel como stack definitivo + nombre del juego.