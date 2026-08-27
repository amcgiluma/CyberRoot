# ESTADO-JUGADOR — qué se puede jugar hoy (documento vivo de Oscar)

> 📌 **Documento vivo, mantenido a diario por Oscar de Astora (05:00).** Es el
> puente entre el `docs/DESIGN.md` (lo que el juego *será*) y el código en `src/`
> (lo que el juego *es hoy*). Cualquier agente o Juanma puede leerlo para saber
> en qué punto está la experiencia jugable de verdad.

---

## 🎮 Estado global jugable de HOY

**¿Hay algo que jugar de principio a fin?** *(27/08 — MODO A)*
**SIN BUILD AÚN.** No existe un punto de entrada ejecutable que arranque una run
de principio a fin. Verificado 27/08 05:00:
- `src/` contiene SOLO los README de los 11 módulos (Fase 0 del Arquitecto) y la
  doc `core/ARCHITECTURE.md` — cero `.py` de juego.
- No hay harness (`tools/harness/` ni `tools/playtest/` no existen físicamente;
  están por crear en Fase 1 por Ornstein).
- El único `.py` raíz es `tools/cyberroot_usage.py` (panel de uso/coste), no el juego.
- No hay `python -m core` ni equivalente. → **No se puede jugar ni headless.**
- Revisión hecha en MODO A (test de diseño en papel), ver sección «📝 Revisión de
  diseño (papel)» abajo.

## 🏃 Run de referencia (save limpio)

**Pregunta de Oscar cada día:** ¿un jugador que empieza de cero puede avanzar por
el camino real (capítulo 1 en adelante) hasta donde toque, sin que se rompa el
viaje?

- Resultado de la run de hoy: **no ejecutable** (sin build). Run MENTAL sobre el
  diseño, cap. 0 → 6 + 4 finales (§3.4).
- Dónde se rompe el camino (si se rompe): *(aún sin código — ver riesgos en la
  revisión de papel, sobre todo el tutorial del cap. 0)*
- Estado del save al terminar: **no existe save** (ni estado, ni harness que lo
  genere).

## 👴 Progreso de veterano (save 20+ horas)

**Pregunta de Oscar cada día:** ¿el juego sigue enganchando y siendo coherente
cuando ya llevas 20+ horas (loop a largo plazo, base/Hub, karma, dificultad,
textos de reacción)?

- Evaluación (en papel): el diseño prevé 3 fases de rejugabilidad (§5.4) con
  Pactos de Vela (§4.6), caza de sinergias (§5.2/§7.8) y récords personales
  (§7.6). Sin save real, la validación de largo plazo la hará el harness de
  Ornstein en cuanto haya build.
- Señales de cansancio o rotura del ciclo: ver hallazgo sobre el **techo
  post-finales** en la sección de papel (y en `notas-manana.md` 🧭).

## 📝 Revisión de diseño — camino del novato en el papel (MODO A, 27/08)

**Veredicto general:** el esqueleto del viaje (cap. 0 → 6, 4 finales en §3.4)
TIENE SENTIDO de principio a fin para un jugador de cero: el aprendizaje por
necesidad está bien secuenciado a grandes rasgos (navegar antes que permisos, la
luz como curva de dificultad, el cap. 5 como práctica obligatoria de defensa).
El camino NO está roto sobre el papel, pero tiene **un agujero serio en el
tutorial del capítulo 0** y varios puntos a afinar. Detalle abajo.

**HALLAZGOS (HECHO vs OPINIÓN):**

1. **[SERIO — camino de cero] El cap. 0 no enseña a COPIAR, pero pide copiar.**
   - HECHO: `docs/DESIGN.md` §6.1 dice cap. 0 = «Tutorial sin teoría: `ls`/`cd`/`cat`
     aparecen POR NECESIDAD; 1 sala, 1 run guiada». §6.3 le asigna 3 conceptos.
   - HECHO: la escena técnica de `backlog/historia/CAPITULOS/00-la-firma.md`
     (Manus, 27/08) muestra `ls`, `cat`, `cd ..` — y solo esos. El dossier pide
     «objetivo: copiar, no borrar», y el texto afirma «Copia el fichero» pero
     NUNCA muestra `cp`.
   - OPINIÓN/RIESGO: un jugador de cero que hace su primera run recibe el objetivo
     «copia el fichero» sin haber visto ningún comando de copia. O bien `cp` debe
     entrar en el cap. 0 (cuarto concepto, y el `datos×combo` del hallazgo §7.1 de
     extracción depende de copiar), o el tutorial debe rediseñarse para que el
     objetivo inicial no exija copiar. Es la primera impresión del juego y hoy
     exige un comando no enseñado. → Nota 🧭 a Gwyn + `[PENDIENTE][P1]`.
2. **[MEDIO] Cap. 0: run guiada «que sale bien» vs. texto de post-mortem si mueres.**
   - HECHO: §6.1 dice cap. 0 «Todo sale bien. La firma ya está puesta» (beat 1).
   - HECHO: el capítulo materializado incluye «Si mueres en la primera run, no es
     game over: post-mortem» con líneas de expulsión al 40 %.
   - OPINIÓN: si la run 0 es tutorial guiado que no puede fallar, ese bloque es
     rama muerta; si puede fallar, contradice «todo sale bien». Gwyn debe decidir
     si la run 0 puede fallar o no (y, si puede, `cp` es OBLIGATORIO en el cap. 0,
     ver hallazgo 1). → Nota 🧭 a Gwyn.
3. **[MEDIO] La regla «más luz = más vigilancia» debe señalizarse antes del Umbral.**
   - HECHO: §6.0.2 «la luz es la curva de dificultad»; cap. 1 = Muelles (apagado),
     cap. 2 = Umbral bajo.
   - OPINIÓN: el jugador debería descubrir/verbalizar la regla en el cap. 1 (un
     diálogo, un titular, el mercado de Gris) ANTES de cruzar al Umbral en el
     cap. 2, o entrará en la primera zona brillante sin saber que subió la apuesta.
   → Nota 🧭 a Gwyn.
4. **[MEDIO — ritmo] Cap. 4 (red) es el más largo (9–10 encargos, 2,5 h) y cierra
   el acto 2.** §6.3 lo define deliberadamente así (skill firma, §6.6.3).
   - OPINIÓN: es el valle de riesgo del mid-game: justo cuando el jugador lleva
     ~8 h, 10 encargos de red seguidos pueden cansar. La repetición espaciada
     (§6.0.4) y las salas elite multi-familia (§5.2) alivian, pero conviene
     vigilar el ritmo; quizá airear el cap. 4 con más variedad de familia. →
     Nota 🧭 a Gwyn (no es decisión mía).
5. **[MEDIO — finales] APAGÓN PROPIO (secreto) depende del último fragmento, cuyo
   drop es «probabilidad baja fija» (§6.1).**
   - HECHO: §9 «orden fijo por capítulo; la seed solo decide la piel» → el último
     fragmento cae solo en cap. 6.
   - OPINIÓN: si el drop final es RNG puro, un jugador que ha completado TODOS los
     arcos + banda mixta podría no ver APAGÓN PROPIO y frustrarse en el final
     secreto. Recomendar drop garantizado del último fragmento en la cadena final
     del cap. 6 (no dejar el final de dominio total al azar). → Nota 🧭 a Gwyn.
6. **[MENOR — redacción] Condición de LUZ PLENA ambigua en §3.4.1.**
   - HECHO: «ningún dato de la cadena vendido o destruido **durante el acto 3**».
   - OPINIÓN: la integridad de la cadena se compromete si vendes en CUALQUIER
     momento, no solo en el acto 3; la condición debería leer «en ningún momento».
     Dejar claro qué ventas cierran LUZ PLENA para no sorprender al jugador. →
     `[PENDIENTE][P2]` de coherencia (Gwyndolin) + nota 🧭.
7. **[VETERANO — techo] Sin NG+ (§9), el contenido post-4-finales queda en Pactos
   duros + récords personales.** Es suficiente para 20 h (objetivo 10–15 h), pero
   el techo existe y conviene declararlo para alinear expectativas del veterano.
   → Nota 🧭.

**Señalización de los 4 finales:** §3.4 y §3.4.1 son coherentes entre sí y con los
beats del acto 3 (§2.5); los cuatro finales son alcanzables de forma lógica con el
karma K ya definido (§3.3). No hay final incoherente sobre el papel, salvo el
matiz del punto 5 (RNG del fragmento) y el 6 (redacción de LUZ PLENA).

**Secuenciación curricular:** correcta a grandes rasgos. No se exige un comando de
escalada antes de enseñarlo; los prerrequisitos = llaves diegéticas
(§6.0.3) son una herramienta de diseño muy buena (la puerta se ve antes de tener
la llave). Cap. 5 obliga a defensa a todo perfil (coherente con §3.1: misma
materia, lentes distintas).

## 🧭 Notas de dirección (para Gwyn)

*(Oscar puede dejar aquí también un apunte breve; las notas formales van en
`backlog/notas-manana.md`, sección 🧭, para que Gwyn las valide a las 23:00.)*

**Resumen (detalle en `backlog/notas-manana.md`):** el mayor riesgo del camino de
cero hoy es el tutorial del cap. 0 (objetivo «copiar» sin enseñar `cp`). Le sigo
el cap. 4 como valle de ritmo, la señalización de la regla luz=vigilancia antes
del Umbral, el drop del fragmento final para APAGÓN PROPIO, y el techo veterano
post-finales. Nada bloqueante de Fase 1; todo son decisiones de Gwyn.
CICLO: verde.

---
*Mantenido por **Oscar de Astora** · Firmado con su nombre en el historial git.*