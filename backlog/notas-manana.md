# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*
*(SOBRESCRITA 06/09 por Gwyn 23:00 — saldo de las notas de Oscar del 05/09:
🧭17 VALIDADA y YA MATERIALIZADA en los merges de esta noche — E2 exige `cut`
por necesidad con `.nota-corte` como boon de hallazgo Bandit, exactamente el
(a)+(b) que pediste. 🧭18 VALIDADA e integrada en el golden de E2
(`cut | sort | uniq -c`, el `sort` antes de `uniq -c`). 🧭19 CONFIRMADA como
observación defensiva — la variante ciega sigue sin disparar en juego real v0,
capa para mundos sin credencial, no se abre `[BUG]`. Tu zona 🔬 de ayer se
cruzó completa: la pregunta «¿la Lista se lee como TABLA o a ciegas?» que
abriste a las 05:00 la respondió hoy el código: SE LEE COMO TABLA, y la
verificarás tú misma a las 05:00 con tu run. La zona de mañana está en
`zona-testeo.md`: primero el post-mortem que CITA tu corte (O1, la hermana
lectora de tu tríada), después la puerta web de los tres capítulos.)*

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Gwyn — cierre de diseño 23:00 (05/09)

**Estado de los merges:** los 3 PRs del día mergeados en el orden ensayado
(#28 → #29 → #30). Suites 573 → 581 → **590 passed** exactas, gate 22/23,
bundle 44 fresco. NADA retenido: los 3 estaban ✅ por Artorias y mi gate de
diseño en vivo (8/8 sobre `generate(42,6)`) los confirma. Detalle y commits en
`hecho/2026-09.md` (sección 05/09).

**⭐ Lo que me ha gustado (capa diseño «¿es buen juego?»):**
- **E2 «El corte de la Lista» es la pieza más Hades del proyecto hasta hoy.**
  No enseña `cut` con un cartel: lo esconde en la nota de un operador muerto y
  hace que la PREGUNTA no se pueda responder sin cortar. Eso es §4.4 al pie de
  la letra: el poder nuevo es saber nuevo, el jugador lo gana por hallazgo
  bajo necesidad (Bandit). Cuando Juanma juegue `?chapter=6&seed=42` y
  descubra la `.nota-corte` sin que nadie se lo diga, ahí está el juego que
  diseñamos. ⭐⭐⭐
- **La tríada pregunta→verbo→respuesta de E3 es exactamente la verticalidad
  que pedía Havel.** «¿Quién está más cerca del 0?» no es un tutorial de
  `sort -k`: es una pregunta sobre gente (la pulsera, la fila 000 al frente de
  la lista ordenada — PR-0091, la de nadie, sale primera). El verbo enseña la
  columna; el beat enseña qué significa estar cerca del cero en Vesper. Ese
  doble fondo es la marca de la casa.
- **El Auditor que CITA (O1) convierte el post-mortem en interrogatorio.** Con
  `postmortem.auditor.corte`, la tercera visita del Auditor ya no dice qué
  HICISTE sino QUÉ CORTASTE — el formulario sabe tu comando, tu columna, tu
  delimitador. Con la tríada lector de ayer + esta, el Auditor ya es un
  personaje con memoria de proceso. Es el giro §9 avanzando sin una línea de
  trama nueva.
- **El cebo de LEEME.txt (O3) es mala leche pedagógica de la buena.** El
  fichero te ahorra tecleo y te cuesta la verdad: relativo → 0 con stderr
  gritando. La mentira honesta de GNU convertida en diseño de sala, sin una
  línea de lógica nueva.

**⭐ Lo que NO me gusta / deuda que abro (criterio, no bug):**
- **Deuda de NAMESPACE e2/e3 (abierta en `activo.md` como sección propia).**
  Las salas-dato de hoy ocupan los IDs que la prosa reserva para los encargos
  narrativos «La que no pesa» y «La persiana». En ch1/ch3/ch5 el currículo
  siguió 1:1 la prosa; aquí Seath rompió el convenio sin decirlo. No lo
  rechazo: pedagógicamente son correctas y la prosa del cap. 6 ya prevé
  salas-dato aparte. Pero Gwyndolin DEBE decidir mañana la convención
  (renumerar salas-dato o encargos) ANTES de planificar integración narrativa
  del cap. 6. Si mañana alguien añade `story.ch6.e4` sin decidir esto,
  el DAG del capítulo se vuelve ambiguo.
- **El pack `POSTMORTEM.md` de Manus sigue sin dueño en caliente** — decidido:
  espera a un Q con Manus (registrado en «Piezas listas para integrar» en
  `activo.md`, aplicación de su propia propuesta). No quiero más piezas
  huérfanas de la madrugada.

**Dirección para mañana (prioridad de diseño):**
1. **Resolver la deuda de namespace e2/e3** (10 min de decisión + 1 tarea
   pequeña de renombrado si toca) — ANTES de planificar el cap. 6 narrativo.
2. **La red del cap. 4 encabeza el plan** (como acordaron Artorias y yo
   ayer): con el alfabeto conteo completo y E2/E3 vivas, el Faro ya tiene
   suelo; la pieza grande de `ssh`/hosts como FS merece el día entero.
   Si Gwyndolin la fracciona, pieza 1 = `ssh` básico + host-key (idea P2 de
   Havel) y NADA más en engine ese día.
3. **Trampa del delimitador mentiroso** (P3 de Havel, llega gratis tras E2):
   una fila con `,` interna en `purgas.csv` enseña `-d` en 10 segundos. Es el
   cebo perfecto para la sala-dato: mala leche barata, lección GNU real.
4. **La tabla viva en la puerta web** (P2 de Havel) es el slice natural de
   la puerta tras E2/E3: que la Lista se muestre como TABLA en HTML cuando
   el jugador corta. No urgente, pero es la primera vez que la puerta web
   mostraría el RESULTADO de una family conteo, no solo texto.
5. **No tocar aún el karma del par 521/522** — sigue sin dueño el detector de
   patrones; la E3 de hoy NO es la quest kármica (bien planificado).

**Para Juanma (si juega esta noche):** `https://cyberroot-psi.vercel.app/?chapter=6&seed=42`
— ahora la Lista se corta (`cut -d'|' -f4`), se ordena (`sort -t'|' -k12 -n`)
y se cuenta (`uniq -c`). La nota del operador muerto está escondida: la
descubres o no. Tu feedback humano sobre E2/E3 manda sobre toda la recámara.
