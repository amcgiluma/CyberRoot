# 🔬 Zona de testeo — 13/09 (definida por Gwyn el 12/09, 23:00)

> Formato `docs/TESTEO-DIARIO.md` §4. Relevo: **OSCAR (05:00) recorre la
> zona COMPLETA desde save limpio (MODO B) → HAVEL (07:00) se centra en lo
> nuevo + smoke del conjunto.** Base del estado ain: post-merge
> PRs #47/#48/#49, suite 698, gate 24/28, bundle 47 (396.7 KiB).

## Prioridad 1 — `auditor_join`: el post-mortem cita el anti-join (NUEVO, PR #47)

- **Dónde:** juega `story.ch6.dato4` (Faro) resolviéndolo con
  `join -t'|' -1 3 -2 1 -v 1 purgas.csv registro.csv` y abre la ficha.
  El **post-mortem del Auditor** debería ahora incluir una línea nueva
  «cruce registrado — join anti-join (-v): huérfanas de la primera tabla».
- **Qué verificar:** (a) la línea aparece SOLO cuando el history contiene
  un `join` **con `-v`/`-v1`/`-v 1`/pipe+join**; (b) una sesión sin join
  produce el post-mortem **byte-idéntico** a antes (sin ruido); (c) una
  sesión con `join` **sin `-v`** NO dispara la línea nueva (el join
  normal ya lo cubre el informe de hoy); (d) la línea no filtra datos de
  fila del mundo (formulario, no contador de datos).
- **Por qué importa:** es la CUARTA huella del Auditor (corte→orden→join):
  si esta no se siente como las otras (testigos que confiesan), el
  post-mortem pierde la retícula.
- Pregunta de sabor: **¿feels like the Auditor "saw" your cross?** ¿o
  parece un tachuelo de formulario más?

## Prioridad 2 — 127 que enseña + tabla viva del troncal (PRs #48/#49)

- **Dónde:** en un cap. 0 o cap. 4 (tras e1), teclea
  `join`, y la shell responderá el error 127 con la glosa que nombra el
  Faro: `Try 'join --help' — tables cross there (chapter 6).`. Luego, en
  cap. 4, abre la **web** (`?chapter=4&seed=42`).
- **Qué verificar:** (a) la glosa SOLO aparece con `join` (el resto de
  comandos que no existen mantienen el error 127 seco, sin glosa); (b) en
  el cap. 6,  `join a b` funciona y NO da 127; (c) en la web, el panel
  **«Volcado del Troncal»** hermana del Faro: preview estático
  (TR-001/002/003) ANTES del `scp`, y **tabla viva-live** DESPUÉS del
  `scp /tmp/`, con el reflejo de `cut -d'|' -f1` sin la fila `id`; (d)
  cambia de capítulo y el panel desaparece (cap. 4 only); (e) **restart
  limpia ambos paneles** (el del Faro intacto siempre).
- **Por qué importa:** dos superficies nuevas (glosa didáctica + panel
  web) que NACEN de la frontera: si la glosa choca con el sabor («te
  dice dónde ir») o x (`id` fantasma vs
  TR-…), es señal de diseño, no de bug.
- Pregunta de sabor: **¿la glosa del 127 enseña o marea?** ¿La tabla del
  troncal «da que hacer» y no solo «muestra»?

**Smoke:** suite completa (698/0), gate 24/28, bundle fresco (guardián
verde), `generate(42,6)` intacto, golden `cut -d'|' -f1 /tmp/volcado.csv
| grep TR-` → 3 líneas sin `id` + TR-003 EN_COLA visible.
