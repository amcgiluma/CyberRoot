"""core.sandbox — el Linux de mentira que dice verdades (ARCHITECTURE §2.2).

FS virtual + shell con semántica REAL de Linux. Autónomo y reutilizable:
no sabe que existen runs, salas ni partidas. Determinismo puro: sin RNG
(el azar entra por la piel que instancia el generador, no aquí), sin reloj
real (tick simulado), sin `pyxel`, sin `random`, stdlib only.

Estado v0 (27/08): comandos del tutorial del cap. 0 (`ls`, `cd`, `cat`)
+ `cp` implementado a la espera de la decisión 🧭1 de Gwyn. Ver PLAN.md
para decisiones de diseño y hitos. Dueño: Smough (`feat/sandbox`).
"""

__version__ = "0.1.0"
