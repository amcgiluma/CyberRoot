"""core.state — el estado agregador y el guardado (ARCHITECTURE §2.6).

GameState serializable JSON ida-y-vuelta + save/load ATÓMICO versionado
desde el día 1. Único punto donde las piezas ensamblan; fachada que
consumirá `main.py`. v0 envuelve la Shell del cap. 0. Sin RNG, sin reloj
real, sin pyxel, stdlib only. Ver PLAN.md (decisiones e hitos de la T1).
Dueño: Seath (`feat/meta-ui`).
"""

__version__ = "0.1.0"
