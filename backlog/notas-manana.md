# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*

*(Vacío esta noche — la última dirección de Oscar (12/09, 🧭20–28) fue
VALIDADA e integrada por Gwyn el 12/09 por la noche: 🧭20/21/22/23/28
CERRADAS archivadas, 🧭24 cerrada con matiz PRE-PUEBLA resuelto (Gwyn
decide MANTENER la pre-puebla de `shell.hosts` como comodidad — la
redundancia didáctica del briefing «léelo en /etc/hosts» es un recuerdo
de la frontera, no un bug; ajustar el briefing es deuda P3 si algún día
confunde a un jugador real), 🧭25/26/27 PERSISTEN sin cambio. Ver
`../planes/2026/09/12.md` y worklog 12/09 para el detalle.)*

## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

### 🎯 Gwyn — cierre de diseño 23:00 (12/09)

**Estado de los merges:** los 3 PRs mergeados en el orden ensayado por
Artorias — **#47 (engine O1 `auditor_join`) → #48 (sandbox S2 127 que
enseña) → #49 (meta-ui T1 tabla viva del troncal)**. Suite **698 passed
exactos** (691+3+4+0, deltas declarados verificados por aritmética), gate
**24/28**, bundle **47 ficheros (396.7 KiB)** regenerado canónicamente
(guardián verde). **NADA retenido.** Las 3 ramas borradas tras confirmar
MERGED en GitHub. O1 entregó A LA TERCERA: la antigua deuda nocturna
cierra sin cicatrices — el diagnóstico de Gwyndolin (fallo de arranque,
no de spec) fue el correcto.

**Validación del 🧭 de Oscar (12/09):** 🧭20/21/22/23 re-verificadas
ARCHIVADAS. **🧭24 (pre-puebla `hosts` vuelve redundante el rechazo
`scp` sin `cat`): mi decisión es MANTENER la pre-puebla como comodidad y
NO tocar el briefing hoy** — el texto describe la frontera conceptual
(«el host se conoce leyendo, no adivinando») que sigue siendo la
lección, y el jugador que salta `cat` gana tiempo sin perder nada de
conocimiento. Doc drift P3 en recámara: si un playtest real muestra
confusión, se reescribe el briefing, no el código. 🧭25 (pipes) y
🧭26 (`cut` en ch4) siguen en recámara sin cambio. 🧭28 (FICHA e2 con
alma) verificada positiva — CERRADA.

**⭐ Lo que me ha gustado (capa diseño, del 12/09):**
- **El Auditor ya tiene TRÍLOGÍA completa: corte, orden y cruce.**
  `auditor_join` aterriza con el mismo formulario y la misma voz — y lo
  mejor: la huella NUEVA solo aparece cuando usaste anti-join (`-v`);
  una noche sin cruce deja el informe byte-idéntico. El post-mortem no
  es un checklist, es un TESTIGO: solo declara lo que viste. ⭐⭐⭐
- **El 127 que nombra el Faro es la fricción convertida en mapa.** La
  frontera del capítulo ya no es un muro mudo (`command not found`) sino
  un cartelesito que dice «aquí no, pero existe un sitio donde sí». Y lo
  hizo Smough SIN tocar la allowlist — 7 líneas + 4 tests de frontera. La
  elegancia de siempre: enseñar el mundo a través del error. ⭐⭐⭐
- **La tabla del troncal hermana de la del Faro es la PRIMERA pieza que
  reusa un patrón web en vez de inventar otro.** `parseTroncalCut` con
  filtro fino propio y **fallback estático honesto pre-scp**: la web
  muestra TR-001/002/003 aunque no hayas bajado el volcado — y cambia a
  LIVE tras el `scp`. Consistencia de mundo: el jugador que aprendió a
  leer la tabla del Faro RECONOCE el instrumento en el troncal. ⭐⭐⭐
- **Los cap. 4 y cap. 6 se respiran mutuamente sin tocarse:** O1 tocó
  postmortem+textos, S2 sandbox/shell, T1 web — cero cruces de rutas,
  ownership respetado al 100 %. Tres semanas de avances para llegar a un
  día en que nadie pisa el fichero del otro. ⭐⭐

**⭐ Lo que NO me gusta / deuda que dejo:**
- **Dos ramas regeneraron el bundle en paralelo (O1 y S2, 394.0 KiB cada
  una).** No rompió hoy (auto-merge trivial), pero es la segunda noche
  con doble regen del mismo artefacto. Criterio que FIRMARÉ como regla
  si vuelve a pasar: **solo el ejecutor que toca `src/data/` regenera el
  bundle en su rama; el resto lo deja al build canónico post-merge de
  Gwyn.** Gwyndolin, apúntalo en el plan si los deltas vuelven a
  solaparse en data/.
- **El fallback estático de T1 duplica TRONCAL_CONTENT en `web/app.js`.**
  Es intencional (Artorias lo verificó byte-idéntico), pero significa que
  si el volcado cambia mañana, hay DOS sitios que actualizar. mientras
  el volcado sea un glob mutable, riesgo bajo; se hace deuda el
  día que Manus toque el volcado para narrativa. Alerta en el plan de
  ese día.
- **🧭24 deja la vieja red de «`scp` sin `cat` rechaza» muerta en el
  briefing** — decisión arriba: mantengo, P3, no urgente.

**Dirección para mañana (prioridad de diseño):**
1. **Zona 🔬 13/09 está CARGADA para las 4 patas (ver
   `zona-testeo.md`):** prioridad 1 = se SIENTE el `auditor_join` (el
   titular de la jornada: ¿el testigo nuevo confiesa con la misma voz?);
   prioridad 2 = glosa 127 + tabla troncal (¿enseña o marea? ¿da que
   hacer o solo muestra?). El relevo OSCAR (completa desde save limpio)
   → HAVEL (lo nuevo + smoke) queda como protocolo.
2. **Dato6 «La segunda purga» PR-0092 coma-trampa** (Havel 12/09,
   persigue): la idea tiene ALMA — «la purga que no pesa» vs la que sí,
   y la coma-trampa es la lección de separador que el Faro aún no
   cobra. Si Gwyndolin la asigna, la spec debe decidir pronto la
   ALLOWLIST (¿`sort -k4 -n`? ¿nuevo `tr`?), no dejarla para el turno.
3. **TR-003 EN_COLA como bifurcación karma** (Havel, P2): el volcado
   que espera puede ser rescate O ceniza. Es la primera bifurcación
   narrativa REAL del juego. No la muerdan sin ADR — es una decisión de
   DESIGN, mía final.
4. **No tocar:** karma 521/522 (sin dueño), pack `POSTMORTEM.md` (la
   voz del interrogatorio ya está CUBIERTA por la tríada corte/orden/
   join — el pack de SEÑAL queda aún más en recámara), 🧭25/26/27 en
   recámara.

**Para Juanma (si juega esta noche):** `?chapter=4&seed=42` y cap. 4
ahora tiene TABLA VIVA en la web: baja el volcado con
`scp troncal-01:/srv/archivo-troncal/volcado.csv /tmp/`, pásalo por
`cut -d'|' -f1 /tmp/volcado.csv | grep TR-` y mira la tabla nacer en el
panel del lateral. TR-003 sigue EN_COLA desde las 03:14 — alguien sabe
qué es eso. Y si juegas el cap. 0, teclea `join`: hasta los errores
ahora saben dónde vive el futuro.

### 🎯 Artorias — filtro técnico 21:00 (12/09) — histórico, ya AUDITADO por Gwyn

*(Los 3 PRs ✅ y mergeados esta noche por Gwyn 23:00 — 698/24-28/47, NADA
retenido. Ver su cierre de arriba.)*

<!-- La entrada completa de Artorias del 12/09 se archiva con la jornada;
     el relevo a Gwyndolin ya está cubierto arriba. -->
