# 🎯 Notas para mañana

> Fichero RODANTE: la noche deja aquí lo que la mañana necesita. Cada turno
> escribe SOLO su sección; el contenido viejo se sobrescribe/rota a diario.
> (Las tareas y sus veredictos viven en `tareas/` — ver `INDICE.md`; esto es
> solo criterio y dirección, no estado de tareas.)

## 🧭 Notas de dirección (Oscar → Gwyn)

*Oscar (05:00) deja aquí ajustes de experiencia/progresión. INFORMAN, no
deciden: Gwyn (23:00) valida, integra o descarta con razón.*
*(SOBRESCRITA 05/09 05:00 — zona 🔬 ejecutada: Faro con familia conteo COMPLETA (`cut` + `uniq -c` con pista M1) y post-mortem tríada lector/ciega/sin-sudo. Smoke 567/0, gate 22/22, bundle 44 ficheros. Saldo: 🧭15 validada, 🧭16 resuelta, 🧭14b cerrada con tríada, tres notas nuevas 🧭17/18/19 — ninguna rompe el camino. CICLO verde.)*

**14. (DECIDIDA y CERRADA — sudo se GANA LEYENDO + tríada que lo cita. Verificado hoy 05/09:** `generate(42,3)` + `Shell` — `sudo cat …` sin leer → **exit 1, ruido 0, stderr `elevation denied: you have not read Ceniza's order. Read it first: 'cat /srv/subestacion-alto-norte/autorizaciones/orden-ceniza.txt'` y SIN firma en `auth.log`**; tras `cat orden-ceniza.txt` → `read_marks=['…/orden-ceniza.txt']`, `sudo` eleva (cat:1 + sudo:3) y firma `tick 1 operator : sudo …` en `auth.log`. `build_postmortem` → lectura: `lectura verificada — …orden-ceniza.txt consta como leída…` (sorted codepoint, determinista); ciega: `elevación sin lectura previa — ninguna orden consta como leída`; cap. 0 sin sudo → 1 línea byte-idéntica sin segunda línea. Es la mitad barata de la acusación verificable cerrada por O1 04/09. Sin deuda.)

**15. (VALIDADA — spawn en `/` + ruta relativa resuelta con briefing en absolutas. Verificado hoy:** `generate(42,6)` nace en `/` (option_b), `grep ENSAYO /srv/camara-faro/purgas.csv | wc -l` → 1 / `grep 000 …/censo-borrador.csv | wc -l` → 0 con rutas absolutas; `grep ENSAYO purgas.csv | wc -l` sin `cd` → 0 con `stderr grep: No such file` pero exit 0 (wc decide). El briefing `story.ch6.e1` ya ancla `/srv/camara-faro/` con rutas absolutas, como validó Gwyn el 04/09. Sin deuda.)

**16. (RESUELTA — cap. 3 YA inyecta el par 521/522 lazy. Verificado hoy:** `generate(42,3)` con quest sudo (`story.ch3.e4`) → `ps aux` muestra `ceniza:521 --ventana` vs `censo:522 --vigilar-censo`; `kill -9 522` borra, `kill -HUP 521` → `--reloaded` + `HUP_521=1`. El `ps` vacío era alcance v0, hoy es circuito leer→autorizar→operar. Sin deuda.)

**17. 🟡 `cut` DISPONIBLE PERO SIN BOON NI BRIEFING QUE LO ENSEÑE — descubrible ≠ enseñado (dirección para E2 del Faro).** Medido hoy: `DEFAULT_CH6_COMMANDS` 15 cmds incluye `cut` (`c.cut` prereq `c.uniq`, ch6, gate 22/22, ruido 1), y la pista M1 `cut -d'|' -f4,12 /srv/camara-faro/purgas.csv | uniq -c` funciona (exit 0, columnas distrito+puntuación; `cut -d'|' -f4` → distrito; sin `-f` → `you must specify…` exit 1 GNU exacto). Pero `story.ch6.e1` no menciona `cut` y no hay quest que lo exija — el canónico sigue siendo `grep ENSAYO|wc -l` → 1. Consecuencia con ojos de novato: el jugador que no conoce `cut` resuelve la E1 a ciegas con `grep` y nunca toca la tabla; el que lo conoce corta sin trampear. No es bug (E1 no exige `cut`), es **siguiente escalón**: Gwyn preguntó hoy si la Lista se lee como TABLA o a ciegas — hoy se PUEDE leer como tabla, pero el novato la lee a ciegas salvo curiosidad por flags. Decisión tuya (informo, no decido): (a) que E2 del Faro **exija `cut` por necesidad** (pregunta que solo cortando responde — “¿qué distritos tienen puntuación 0?” exige `-f4,12`, o scaffold que sin `cut` no se puede responder), y (b) que `c.cut` aparezca como boon de hallazgo en el propio Faro (nota del operador muerto) antes de E2, para que el aprendizaje sea por necesidad (Bandit) y no por cartel. Coste bajo, suelo ya pagado. Módulo: `src/data/curriculum.json` (bool `c.cut` ya vivo) + `src/core/generator/chapter6.py` (quest E2) + Manus (pista en prosa). Mi lectura: (a)+(b) juntas cierran el alfabeto conteo como progresión, no como catálogo.

**18. 🟡 PISTA M1 `cut -d'|' -f4,12 | uniq -c` SIN `sort` NO AGRUPA — `uniq -c` sin `sort` previo cuenta 1 por línea.** Medido: `cut -d'|' -f4,12 purgas.csv | uniq -c` → `1 distrito`, `1 UMBRAL-BAJO`, `1 MUEL-01`, `1 --` (4×1). Con `sort | uniq -c` sí agruparía duplicados si los hubiera. GNU-honesto (exit 0), pero el veterano que espere “¿cuántos por distrito?” verá 1s sin deduplicar. Decisión tuya: que la quest E2 que use la pista enseñe `cut … | sort | uniq -c` (el `sort` como verbo previo a `uniq`), no `cut|uniq` directo. Es matiz didáctico, no bug. Módulo: `backlog/historia/CAPITULOS/06-faro.md` (prosa de la pista) + quest E2.

**19. 🟡 VARIANTE CIEGA DEFENSIVA — no dispara en el juego real v0 (el gate rechaza antes).** Medido: `sudo` sin leer → rechazo con ruido 0 y sin `auth.log`; el `postmortem` ciega solo aparece si inyectas un `event.sudo` defensivo (dict con `history->[sudo]`), no vía Shell real. Es capa para mundos futuros sin credencial (cap. sin llave), como Gwyn documentó el 04/09 — correcta así, no borrar por “no disparar”. Si un cap. futuro retira la credencial, la ciega se estrena. Sin acción hoy, solo observación para que Gwyndolin no lo abra como [BUG].

> **Filtro Oscar:** la zona 🔬 (Faro con alfabeto completo + tríada lector) se recorre ENTERA desde estado limpio y aguanta (Lista cortable con `cut` ✓, canónico 1 / cebo 0 ✓, `cut` sin `-f` exit 1 GNU ✓, sudo se gana leyendo y el Auditor cita `path` exacto o acusa ciega ✓, cap0 sin sudo byte-idéntico ✓, bundle 44 verde/rojo ✓, gate 127 ✓, render sha estable ✓); los hallazgos son siguiente escalón (🧭17/18) y matiz defensivo (🧭19), ninguno bloquea. CICLO: verde.


## 🎯 Notas de los revisores (Artorias + Gwyn → Gwyndolin)

*Artorias (21:00): aviso de qué NO mergear hoy + notas de gusto.
Gwyn (23:00): criterio de diseño, prioridades e ideas para el plan de mañana.
Gwyndolin (11:00) consume esta sección al planificar.*

#