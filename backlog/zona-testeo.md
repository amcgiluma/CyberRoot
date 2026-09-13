# 🔬 Zona de testeo — 14/09 (definida por Gwyn el 13/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base del estado actual: post-merge
> PRs #50/#51/#52, suite **708**, gate **24 conceptos / 29 quests**, bundle
> **47 ficheros (402.3 KiB)** regenerado canónicamente (guardián verde).

## Prioridad 1 — quest `story.ch6.dato6` «La segunda purga» (NUEVA, PR #51)

- **Dónde:** juega la quest nueva del Faro: golden
  `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv | grep 000483` →
  debe devolver **1 línea: `000483|PR-0092|...|EN BLANCO, revisado`**.
  La coma-trampa: `EN BLANCO, revisado` es UN campo — un `join -t','`
  partiéndolo es la lección del separador.
- **Qué verificar:** (a) el golden mental con `join` (cruce) — no se
  resuelve con `cut` ni `grep` a secas; (b) la variante bonus
  `cut -d'|' -f3 purgas.csv | grep 000483` —alumbra la huérfana que SÍ está
  en la segunda tabla (000 vs 000483: no toda huérfana es fantasma);
  (c) el filtro es POSITIVO `grep 000483`; (d) determinismo: repetir la
  golden dos veces → misma fila; (e) la quest exige `c.join` (no
  accesible sin la del dato4 de ayer).
- **Por qué importa:** PRIMERA quest que enseña mintiendo con la verdad:
  el dato trap está DENTRO del campo que `join` ya devolvía — si la
  lección no se siente, coma-trampa pierde cap.
- Pregunta de sabor: **¿la coma-trampa se nota sin señal roja, o el
  jugador la tropezará sin entender por qué?**

## Prioridad 2 — eco del espejo + huella visible del troncal (PRs #50/#52)

- **Eco del espejo (cap. 6):** termina una sesión de la tríada completa
  (ch4.e2 scp→cut|grep + dato4 join -v + dato5 ps aux|grep hora) y lee el
  post-mortem: una sola línea `postmortem.espejo.*` enumerando las 3
  firmas («,  y »), determinista ①→②→③; con CERO firmas → post-mortem
  byte-idéntico; con UNA sola → línea con esa firma sola. ¿Suenan las
  3 firmas juntas como un testigo que recuerda, o como una lista?
- **Huella del troncal en web (cap. 4):** en `?chapter=4&seed=42`, tras
  `scp` + `cut -d'|' -f1 /tmp/volcado.csv | grep TR-`: (a) fila
  `TR-003` lleva badge ámbar **`EN_COLA · 512`**; (b) header `id`
  aparece TACHADO con tooltip; (c) SIN esa pipeline → sin badge ni
  header tachado (fallback estático honesto intacto); (d) restart limpia
  ambos paneles (Faro + troncal), funciona, consola limpia.
- Pregunta de sabor: **¿el badge EN_COLA mete presión de timeline
  genuina o es solo ruido visual?** (TR-003 es la bifurcación kármica
  futura: el badge es su PRIMER aviso diegético.)

**Smoke:** suite completa (708/0), gate 24/29, bundle fresco (guardián
verde, 47 ficheros), `generate(42,6)` + `generate(42,6,'story.ch6.dato6')`
intactos, replay MODO B del eco del espejo con las 3 firmas + golden
dato6 exit 0.
