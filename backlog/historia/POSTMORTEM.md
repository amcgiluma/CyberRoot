# POSTMORTEM — La acusación verificable (Manus, 04/09)

> Pack de líneas canónicas para `build_postmortem`, listas para integrar en
> `src/data/textos.json`. Responde a la pieza de recámara de Gwyn (03/09):
> el Auditor cita la línea del `auth.log` como PRUEBA. Cada clave trae su
> plantilla, sus placeholders y su condición de disparo, todo computable
> desde `shell_dict` + estado. El integrador no interpreta: copia y resuelve.

## Contrato de idioma

Marco en español, dato de sistema verbatim. La `{firma}` se cita tal cual
la escribe el sandbox (`tick 2 operator : sudo ...`, inglés GNU). No se
traduce: el contrato bilingüe de Gwyn (03/09) dice que los mensajes de
sistema van en inglés y la voz en español, y esta línea vive justo en la
costura. Traducir la prueba la rompería.

## Claves

### `postmortem.auditor.prueba`

Disparo: `/var/log/auth.log` existe en el FS de la sesión y trae al menos
una línea no vacía. `{firma}` = la última línea no vacía del fichero,
leída de `shell_dict["fs"]`.

> Expediente 000: consta elevación con la llave de Ceniza. Registro: {firma}. Continuidad del ensayo: estable.

Es la acusación verificable: el jugador puede abrir el log y encontrar la
línea que el informe cita. Si la línea no está, la clave no se usa. Nunca
al revés.

### `postmortem.auditor.sin_lectura`

Disparo: alguna entrada del historial empieza por `sudo` (línea recortada),
devuelve exit distinto de 0 y suma ruido 0. Eso es el rechazo por no haber
leído: el intento no firma y no factura, así que ruido 0 lo delata.
`{orden}` = la ruta literal de la credencial (la pone el integrador).

> Expediente 000: intento de elevación sin lectura previa. Falta: {orden}. El intento no consta.

La última frase es dato, no consuelo: sin firma en el log y sin ruido, el
intento no existe para el archivo. El jugador aprende que intentar sale
gratis y elevar deja rastro.

### `postmortem.auditor.senal_muerte`

Disparo: el historial trae un evento `sandbox.signal` con `signal_num`
distinto de 1. `{signal}` = `data.signal` del evento, `{pid}` = `data.pid`.

> Expediente 000: señal {signal} sobre el proceso {pid}. El proceso deja de responder. Se anota la baja.

### `postmortem.auditor.senal_recarga`

Disparo: evento `sandbox.signal` con `signal_num` igual a 1 (HUP). Mismos
placeholders que la anterior.

> Expediente 000: señal {signal} sobre el proceso {pid}. El proceso recarga y sigue. Se anota la recarga.

Las dos de señal registran sin valorar: matar al vigía (522) o recargar la
ventana (521) son hechos para el archivo. El karma de cada gesto vive en la
persiana del cap. 6 E3, no aquí. El Auditor no absuelve ni condena; anota.

### `postmortem.ceniza.llave`

Disparo: primera elevación con éxito de la sesión (hay firma nueva en el
`auth.log`). Sin placeholders. Voz de Ceniza según ficha: frase corta,
paso concreto nombrado, cierre de procedimiento.

> Elevaste con la orden leída. La firma queda en el registro. La próxima, igual.

## Reglas de montaje (para el integrador)

1. Estas líneas se ANEXAN al informe; no sustituyen a `cruce`/`pico`.
2. Cada una sale como máximo una vez por informe, en este orden: `prueba`,
   `senal_muerte`/`senal_recarga`, `sin_lectura`, `ceniza.llave`.
3. `prueba` y `ceniza.llave` pueden salir juntas: una es el archivo, la
   otra es la mentora. No se pisan porque no hablan de lo mismo.
4. Si `textos.json` aún no trae la clave, el fallback honesto ya existe
   (clave cruda, nunca crash): se integra sin prisa y sin romper suite.

## Fallo del entorno del Faro (respuesta a Havel, 03/09)

Havel propone sembrar el cap. 6 con variables de entorno que sirvan de
hilo rojo (`HOSP-47-C`, `PR-0091`). Fallo:

- APROBADAS, con estos nombres de piel de mantenimiento de Lumen:
  `HOSP_REF=HOSP-47-C` y `PURGA_REF=PR-0091`. Las dos son punteros, no
  respuestas: remiten a la pulsera del fragmento 2 y a la purga de la
  Lista. Se revelan con `env | grep`, que es el gesto que el cap. 3 ya
  enseñó. Sin colisión con `HUP_521`, que nace de la señal, no del skin.
- VETADA: `ULTIMO_PURGADO=000`. El 000 es el hallazgo del encargo E1 y se
  gana contando la Lista. Regalado en el entorno, el conteo sobra y la
  trampa del borrador pierde el filo. El entorno apunta; no resuelve.

## Estado

Pack `[LISTA]` para integración (dueño: ejecutor integrador →
`src/data/textos.json`). Voces calibradas contra fichas (test del nombre
tapado: la de Ceniza solo puede ser suya; las del Auditor solo del
formulario). Sin fichas nuevas, sin escenarios nuevos.
