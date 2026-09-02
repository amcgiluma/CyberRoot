# CENSO-LISTA — El mecanismo de la Lista de Lumen (worldbuilding consultable)

> Worldbuilding del censo — M1 de Manus (02/09). Doc de CONSULTA para los
> ejecutores (Smough/Ornstein): define qué se puntúa exactamente y el formato
> real de los ficheros que las salas-dato del cap. 6 van a cruzar con
> `grep`/`sort`/`uniq`/`cut` (la familia conteo de Havel, S2, como
> alfabeto). Fuente de verdad narrativa: DESIGN §2.4 (el censo y la Lista),
> §2.5 beats 10–12, §3.4 (finales), §9 (arco del Auditor). Cero adjetivos.
>
> La Lista (§2.4) es el volcado íntegro del censo CON las marcas de cada purga.
> No es un documento público: es el fichero que guarda la cámara del Programa
> de Continuidad, y el que alguien quiso sacar a la luz el día de la firma.

## Qué es la Lista, físicamente

Dos ficheros lógicos en la cámara del Faro (el «volcado» es leer los dos):

1. **`registro.csv`** — una línea por habitante. Es el censo de vivos (y de
   dados de baja que se conservan). Delimitador `|` (tubería), elegido para que
   nombres y direcciones con coma no rompan el parseo. Sin cabecera de línea
   más arriba del fichero de ejemplo: la salas-dato pueden depender de que la
   columna 1 sea el `residente_id`.
2. **`purgas.csv`** — el libro de purgas. Una línea por ejecución de purga,
   con el motivo del formulario. Es el registro que nace cuando la Oficina
   «da de baja» a alguien.

La Lista como volcado integrable en la cámara es la suma lógica de ambos.

## Qué se puntúa exactamente (los campos de `registro.csv`)

Columna por columna (orden fijo; el generador puede variar la piel, nunca el orden):

```
residente_id | nombre | fecha_nac | distrito | vivienda | empleador | ingresos_mes | antiguedad_meses | chequeo | sanciones | marcas_purga | puntuacion | estado
```

El valor `puntuacion` (0–1000) se compone de cinco familias de campos, cada una
con su suma. Pesos ⚠️ v1, a calibrar; lo que importa para las salas es QUÉ
cuenta, no la fórmula final:

1. **Vivienda (0–200).** Distrito (Faro > Alto > Bajo > Muelles), bloque y la
   línea del medidor (pago al día, `0`/`1`). Puntúa el bloque, no solo a la
   persona: el par «hogar/censo» del §2.6.4.
2. **Trabajo (0–250).** Empleador validado en el registro de empleadores,
   antigüedad, sector. Un empleador que NO figura en el registro (caso
   `VESPER DE GESTIÓN S.L.`, fragmentos 4 y 5) resta en vez de sumar.
3. **Continuidad (0–300).** Años seguidos censado sin huecos, sin sanciones,
   asistencia a chequeos. Un «sin registro» nace con CERO aquí.
4. **Servicios (0–150).** Transporte, dependientes declarados y la última
   revisión sanitaria (columna `chequeo`, código de la sucursal del Muelle,
   `HOSP-47-C`).
5. **Novedad (0–100, sustractiva).** Actividad no atribuida en el trimestre:
   cruces de puertas, intentos de voto, peticiones al regulador, un perfil
   reactivado sin registro. Resta de la suma, sostiene la luz del Anillo Faro
   como regla de mundo (más actividad = más que mirar).

El umbral por debajo del cual se degrada vivienda/transporte/trabajo es un dato
que la sala muestra en números. El jugador lo ve, nunca lee el umbral como lore.

## Cómo se registra una purga (`purgas.csv`)

```
purga_id | fecha | sujeto | distrito | motivo_codigo | prev_puntuacion | post_credito | puerta_cerrada | archivo_referencia
```

- `post_credito` siempre `0` (la purga lleva crédito a cero).
- `puerta_cerrada` `1` (la puerta de la cámara de Lumen que quedó abierta el
  día de la firma se cierra al purgar; ver cap. 0).
- `archivo_referencia` enlaza con el folio (los mismos folios que perforan la
  Subestación y los fragmentos: `OH-HOSP-47-C-0191`, `OH-UBA-14-0007`).
- `motivo_codigo` viene del formulario del Auditor, campo cerrado:
  `CONTINUIDAD`, `REASIGNACION`, `ENSAYO`, `MANTENIMIENTO`, `VACIO`.

## El hueco que deja Cero («sin registro»)

El jugador es el sujeto 000 del Programa de Continuidad (§2.2, §2.4). En la
cámara eso se lee como dos faltas simétricas:

- En `registro.csv` NO hay fila con `residente_id = 000`. No existe como
  habitante.
- En `purgas.csv` SÍ hay una purga `sujeto=000`, `motivo_codigo=ENSAYO`, con la
  `fecha` en blanco (la fecha de cierre, como el alta de la pulsera, la fila 000
  del expediente y la hoja de cierre del fragmento 6), `prev_puntuacion` vacía
  (no hay registro que puntuar), `post_credito=0`, `puerta_cerrada=1`.

**DATO para salas-dato.** La anomalía que la sala debe poder encontrar con la
familia conteo: una purga cuyo sujeto NO tiene fila hermana en `registro.csv`.
El juego no lo dice: `grep 000 purgas.csv` o cruzar las dos listas lo deja
caer. Es exactamente la huella que la cadena final del cap. 6 premia.

## Ejemplo de filas (AC — un ejemplo de fila de la Lista)

`registro.csv` (tres vecinos reales, separador `|`):

```
$ cat registro.csv
residente_id|nombre|fecha_nac|distrito|vivienda|empleador|ingresos_mes|antiguedad_meses|chequeo|sanciones|marcas_purga|puntuacion|estado
000291|VERA MONTEJO G.|12-03-1987|UMBRAL-ALTO|B14-E3-P14|LUMEN DIV. FACTURACION|2140|214|SIN CHEQUEO|0|0|712|ACTIVO
000462|E. ROLDAN S.|03-11-2001|UMBRAL-BAJO|C07-E1-P02|LAVANDERIA CICLON|1280|96|HOSP-47-C|1|1|438|EN DEUDA
000537|J. HERRERA V.|27-08-1963|MUEL-01|D03-E2-P01|ASTILLEROS DEL MUEL SE|0|0|EN BLANCO|0|2|0|PURGADO 19
```

`purgas.csv` (el libro, con la purga de 000):

```
$ cat purgas.csv
purga_id|fecha|sujeto|distrito|motivo_codigo|prev_puntuacion|post_credito|puerta_cerrada|archivo_referencia
PR-0144|03-07|000462|UMBRAL-BAJO|CONTINUIDAD|438|0|1|OH-UBA-14-0007
PR-0151|11-07|000537|MUEL-01|REASIGNACION|0|0|1|OH-HOSP-47-C-0191
PR-0091|EN BLANCO|000|--|ENSAYO|--|0|1|HOSP-47-C
```

Ejemplo de operación-pista para una sala-dato: `grep -i "ENSAYO" purgas.csv`
devuelve la fila `PR-0091` con fecha en blanco y sujeto sin hermana. `sort -t'|'
-k12 -n registro.csv | tail -5` da a los cinco con peor `puntuacion`. `cut
-d'|' -f4,12 registro.csv | sort | uniq -c` separa por distrito y cuenta.

## Qué sirve a las salas-dato del cap. 6

- Sink de `grep` por `motivo_codigo` (muestra que las purgas no son un único
  acto: hay categorías) y por `id`.
- Sink de `sort`/`uniq` por `puntuacion` (el corte de la degradación) y por
  distrito.
- Sink de `cut`: separar columnas para quedarse con las que cuentan.
- La doble lectura H1/H2 intacta: la purga `ENSAYO` de 000 se lee como
  «borraste tu pasado tú» (H1) o «te lo borraron como ensayo piloto» (H2); el
  formulario solo registra el dato, no el motivo.

## Coherencia

- Cruza con fragmentos 2–5 (HOSP-47-C, VESPER DE GESTIÓN S.L., OH-UBA-14-0007,
  el 44-0191-7 como cuenta) sin forzar: el `archivo_referencia` de purgas es
  la misma numeración que perfora los fragmentos.
- Cruza con la ficha del Auditor: `motivo_codigo` y `fecha` son campos de su
  formulario; la purga de 000 con fecha en blanco es el dato que su Ensayo
  «completó» y cuyo cierre nunca escribió (§2.4: «ensayo completado», fecha en
  blanco).
- Ceniza conoce estos campos (los firmó del núcleo de auditoría, DESIGN §2.3)
  y puede mostrar a Cero cómo se lee una fila sin soltar el secreto de la
  Oficina; la muestra propiamente dicha la dan las salas-dato.