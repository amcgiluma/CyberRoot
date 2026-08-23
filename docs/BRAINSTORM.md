# BRAINSTORM — CyberRoot (nombre de trabajo)

> Fecha: 23/08/2026
> Sesión de ideas con Juanma. En crudo y desarrolladas. Se irán aplicando
> poco a poco y el resultado quedará aquí documentado.

## El principio rector
**Aprender Linux sin que parezca aprender.**
El jugador nunca lee "TEMA 3: permisos". El jugador persigue un objetivo
(colarse, escapar, defender, sobrevivir) y descubre el comando porque le
hace falta *ya*. Si aprender se siente como necesidad → es juego.
Si se siente como lección → es deberes. Nunca deberes.

## 1. Concepto central
Un RPG de terminal / pixel-art cyberpunk que enseña Linux y seguridad
de forma orgánica. El jugador vive una historia de hackeo con dos grandes
caminos morales: Blue Team (defensa) y Red Team (ofensa). Estética CRT,
vibe a Hacknet + RPG de terminal. Chulo, denso, adrenalínico.

## 2. Historia (esqueleto)
- **Premisa:** el jugador es un operador sin pasado reclutado por una red
  clandestina en una ciudad distópica dominada por una megacorp (el "Grid").
  Un primer trabajo sale mal y pasa a ser perseguido.
- **Antagonista:** una megacorp y su IA corporativa.
- **La trama se cose con las misiones**, no con pantallas de texto. Cada
  misión avanza historia Y enseña un concepto técnico.

## 3. Karma con dos carreras — Blue Team vs Red Team
No una barra "bueno/malo" binaria, sino **dos ejes**:
- **Defensa (Azul):** hardening, logs, monitoreo, firewalls, permisos,
  gestión de usuarios, ssh seguro, contenedores.
- **Ofensa (Roja):** escaneo, enumeración, exploits, nmap, escalada de
  privilegios, backdoors.

Cada misión ofrece elecciones que inclinan el karma y desbloquean
habilidades/exclusiones distintas. El karma decide el final: en el cisma
central el juego se bifurca en arcos separados. Enseña el mismo Linux con
lentes distintas — con un motivo moral para elegir el camino.

## 4. "De verdad pareces un hacker"
- Interfaz CRT con scanlines, pixel-art 16-bit en ANSI, verde/ámbar.
- Feedback: animaciones de acceso, barras de progreso falsas, lluvia de
  datos, `root@` al escalar.
- Sensación de sistema real sin ser deberes.

## 5. La trampa a evitar (documentada)
El gameplay no se come la historia, y la historia no se come el gameplay.
Cada **nivel = una misión** con un **reto técnico real** que se debe
superar con comandos/técnicas. La narrativa avanza DESPUÉS de pasar la
barrera técnica. Así la historia premia, no sustituye, el resolver.

## 6. Arco progresivo
Origen (shell) → navegación y ficheros → permisos/usuarios → procesos/red
→ **el cisma azul/rojo** → arc ramificada → final según karma.
De cero absoluto hasta hardening/exploit avanzado, dificultad creciente.

## 7. Ideas abiertas / pendientes de decidir
- Nombre definitivo del juego (candidatos: CyberRoot, sudo: Ghost Protocol,
  NEON//cron, BlackShell).
- Stack técnico (¿Python + curses/rich? ¿JS? ¿terminal simulado web?).
- Motor de nivel: sandbox de comandos reales vs simulador.
- Sistema de logros/reputación/ganancias in-game.
- Grado de detalle del pixel-art.

## Notas de decisión (ADR)
(Se irán añadiendo aquí las decisiones, con fecha y razón — para documentar
el proceso igual que la eficiencia de tokens.)