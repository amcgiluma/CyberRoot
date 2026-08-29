# CAPÍTULO 2 — Facturas

> Acto 1→2, beat 5 (DESIGN §2.5). El rastro de la segunda ventana de las
> 11:04 lleva al Umbral bajo: turnos, facturas de acceso y la primera vez que
> el juego enseña a encadenar comandos. Enseñanza técnica del capítulo:
> texto y pipes (`grep`, `sort`, `uniq -c`, `wc`, redirección — §6.2); las
> primeras sinergias pipeline (§5.2). 5 encargos sobre el distrito de los
> ~7–8 del capítulo (§6.3); aquí solo el material narrativo: escenas,
> diálogos reactivos, karma y ganchos post-mortem. Fragmento 2 (la pulsera)
> disponible como botín (ver `FRAGMENTOS.md`). Estado: `[LISTA]` para
> integración → `src/data/story/`.

---

## ESCENA DE APERTURA — El turno partido

El papel nuevo lleva la caligrafía de siempre:

```
La ventana de las 11:04 se abrió dos veces esa mañana.
La primera fuiste tú. La segunda también.
Los turnos de la centralita no mienten: cuentan.
Vuelve al 12B. Cuenta.
```

La oficina del 12B sigue igual: cajero roto, NAS sin cifrar, y la
centralita facturando a CANDELAS. El papel del turno de aquella mañana, el
que colgaba de la puerta, lo dejó escrito a su manera: `11:04 SIN
REGISTRO`. La oficina sabía que a esa hora pasó algo que no podía
registrar. La centralita del turno sí que lo podía: en sus libros, la
ventana se abrió dos veces.

Ceniza lo había leído antes que tú. Lo dice sin levantar la vista del
informe:

> — La línea de un turno lleva tres cosas: quién, cuándo y cuánto ruido.
> Tu sesión de la firma queda en los libros con ruido 6. Hay otra apertura
> a la misma hora con ruido 1. Quien abrió esa sesión no trabajó ahí: pasó
> de largo, hizo una petición y salió. Las sesiones que pasan de largo
> dejan factura de acceso. Tráeme la serie entera. Y sales con la copia en
> tu unidad.

Primera vez que encadenas comandos. Nadie te lo explica: el carácter de
tubería aparece, y lo que un comando suelta lo recibe el siguiente. El
turno completo cabe en dos líneas:

```
conectando → oficina-vecinal-muelle-norte...
$ cd /srv/oficina-vecinal-muelle-norte
$ grep 11:04 centralita/turnos/turno.log | wc -l
2
$ grep 11:04 centralita/turnos/turno.log
11:04 sesion 000 ruido 6 objetivo nombre_de_proveedor.txt
11:04 sesion 000 ruido 1 objetivo -
$
```

Dos aperturas con la misma firma, a la misma hora. La diferencia cabe en un
campo: la tuya tenía objetivo; la otra lo dejó en blanco. Quien fue a por
el proveedor tocó el proveedor. La segunda sesión no tocó nada de esta
sala. Todo lo que hizo, lo hizo en otro sitio. Y ese otro sitio también
factura.

---

## ENCARGOS — La mesa (muestra integrable)

*Formato por encargo: objetivo técnico + beat + decisión kármica + gancho
post-mortem (§2.6.1). Los textos entran como claves; el generador pone la
piel procedural encima (nombres, rutas, horas).*

### E1 — «La serie fantasma» (azul, `story.ch2.e1`)

La centralita guarda la factura de acceso de cada sesión: qué ficheros
consultó, cuánto duró, cuánto ruido hizo. La sesión fantasma dejó la suya.
Los Apagados quieren la serie completa: qué pidió, en qué orden, hasta
dónde llegó.

- Técnico: `grep` sobre los logs de acceso del turno; `sort` y `uniq -c`
  para quedarte con lo que se repite; `wc -l` para el tamaño. La serie se
  guarda fuera del nodo por redirección: `grep ... > /usb/serie.txt`.
- Beat: la serie termina en una petición que no pide ficheros del distrito.
  Pide un volcado del censo por sectores. El campo de motivo dice una sola
  palabra: continuidad.
- Karma: los logs que te nombran a ti —la doble ventana lleva tu firma— se
  corrigen dejando rastro mínimo (azul) o se queman enteros (rojo: el fuego
  también borra lo que la oficina sabía del fantasma, y la pista pierde la
  mitad).
- Gancho post-mortem: el Auditor anota «acceso reiterado a registros del
  turno 11:04» y, por primera vez, pregunta algo que no está en el
  formulario: «¿el Expediente 000 audita su propio expediente?». No espera
  respuesta.

### E2 — «Puertas muertas» (azul, `story.ch2.e2`)

Una asociación de vecinos del bajo arrastra la misma sospecha desde el
invierno: hay pisos vacíos que Lumen factura como servicio prestado.
Quieren el recuento, con fechas, para reclamar. La lista es fácil de hacer
y difícil de sostener.

- Técnico: filtrar las facturas por póliza de suministro con `grep`,
  contar con `uniq -c` las pólizas sin lectura de contador, ordenar el
  importe con `sort -n`.
- Beat: hay pólizas que llevan cuarenta y un meses facturando a puertas con
  candado. El censo las tiene como viviendas en uso. Las dos
  contabilidades no pueden ser verdad a la vez.
- Karma: entregar la lista completa a la asociación (azul) o quedarte el
  total y vendérselo a quien paga por saber qué puertas nadie mira (rojo;
  Gris tiene comprador antes de que llegues a casa).
- Gancho: el Auditor registra «extracción de datos de terceros» y añade la
  frase que eligió él: «valoración, pendiente».

### E3 — «El proveedor nº 47» (gris, `story.ch2.e3`)

CANDELAS, el proveedor que copiaste el primer día, tiene una serie de
facturas cuyos pagos entran y salen por la misma cuenta sin titular claro.
Gris quiere saber si la serie es falsificable. Lo pregunta como quien
pregunta por el tiempo.

- Técnico: `sort` y `uniq -c` sobre los códigos de factura para encontrar
  la repetición que no cuadra; `wc -c` para el tamaño exacto de cada
  registro.
- Beat: la serie lleva once meses pagándose sola. Alguien mantiene la línea
  viva a propósito, y quien la mantiene no es CANDELAS.
- Karma: gris. Aquí el karma lo pone cómo sales, no qué haces. Si vuelves
  con las manos vacías, Gris te recibe con la cifra ya movida: «Te lo dejé
  en 260 y me escuchaste la mitad. Son 320. No es por el retraso: es por la
  prisa que llevas tú, que también se factura».
- Gancho: si sales limpio, Gris pregunta por el titular de la cuenta. No
  por el nombre: por el número.

### E4 — «La parada del 12» (rojo, `story.ch2.e4`)

La empresa de autobuses del 12 quiebra despacio. Sus horarios reales se los
queda una app del Faro; lo que la app cobra por líneas que ya no corren no
lo ve el sindicato. Dos compradores quieren la prueba del desfase: el
sindicato para denunciar, el del Faro para tasar la compra barata. Que el
que pague más sea el bueno no lo garantiza nadie.

- Técnico: extraer dos series (facturadas y prestadas) con `grep`,
  alinearlas con `sort`, contar las líneas muertas con `uniq -c` y el
  total con `wc`.
- Beat: la empresa lleva dos años facturando quince líneas que ya no
  existen. La app del Faro cobra cada viaje inventado a 0,40 créditos.
- Karma: la prueba para el sindicato (azul) o para el comprador del Faro
  (rojo). Es el mismo papel; cambia quién puede usarlo.
- Gancho: el que paga en silencio paga el doble y no deja buzón.

### E5 — «La ventana que cierra» (cierre del capítulo, `story.ch2.e5`)

Volver a la oficina del 12B con los ojos del oficio. Reconstruir la sesión
fantasma minuto a minuto y cerrarle la puerta: el canal de auditoría remota
por el que entró sigue abierto, y por ahí se entra también a mirarte.

- Técnico: la secuencia completa del capítulo sobre el turno real: acotar
  con `grep`, alinear con `sort`, contar con `uniq -c`, medir con `wc`, y
  la copia de la serie a `/usb` por redirección antes de tocar nada.
- Beat: la sesión fantasma entró por el mismo canal de auditoría que ahora
  te lee a ti. Cerrar ese canal es cerrarle la puerta a tu cazador. También
  es decirle, con un parche, que sabes que estuvo ahí.
- Karma: parchear y registrar el cierre (azul: la Oficina lo atribuirá a
  mantenimiento de rutina) o dejarlo abierto y clonar la llave de acceso
  para volver cuando quieras (rojo: una puerta de Lumen en tu bolsillo, con
  caducidad desconocida).
- Cierre de capítulo: el fragmento 2 puede caer aquí (ver `FRAGMENTOS.md`,
  fragmento 2 — la pulsera).

---

## ESCENA DE HUB — Ceniza cierra el turno (`story.ch2.ceniza`)

Tras el encargo de cierre, Ceniza lee la serie en su terminal de mano y no
dice nada mientras la impresora del rack escupe el papel. El informe que
dicta después dura menos que el silencio:

> — La segunda sesión no era una copia de la tuya. Difería en una línea: no
> ejecutó el `cp`. Lo demás era tu manera de trabajar: mirar, contar,
> salir. Alguien había visto cómo trabajas, y lo trabajó igual con la mitad
> de ruido.
>
> — Eso tiene dos lecturas. La buena: querían pasar sin estorbo. La mala:
> estaban ensayando contigo. No sé cuál es. Sé cuál no: la del error.
> Sigue. Estás más limpia que hace dos semanas. Lo digo por el ruido, no
> por ti.

---

## ESCENA DE HUB — Zeta pone precio a la cadena (`story.ch2.zeta1`)

La primera vez que encadenas cinco comandos sin susto, Zeta deja de darle
vueltas a la silla:

> — Cinco eslabones. Los he contado en el espejo; no hace falta que lo
> confirmes. Mi mejor cadena también es cinco, y la mía la pagué con una
> expulsión y media. Apuesto mi récord del distrito a que no repites la de
> hoy con el turno entero por delante. ¿Entras o mides?
>
> — El atasco de las once, el que te dejaste el martes: ya tiene nombre en
> mi mapa. Lo puse yo. «Cero», a secas. El día que dejes de ser un atasco,
> te aviso.

---

## COLA DE POST-MORTEM — Ceniza y el Auditor (cap. 2)

*Extracto integrable: líneas por clase de evento (§2.6.2/§2.6.3), nunca
repetición literal.*

Primera expulsión del capítulo, en voz de quien firma informes:

> — El log dice `grep: centralita/facturas: No such file or directory`. El
> comando funcionó; la ruta no existía. Antes de encadenar, mira dónde
> estás. Una tubería no arregla un camino malo: lo recorre más rápido.

Repetición ante el mismo obstáculo:

> — Segunda vez con el mismo atasco. El filtro no era el problema: el
> orden. Primero acota, después cuentas: `grep` antes de `uniq -c`, nunca
> al revés. Cada pasada que sobra es ruido, y el ruido aquí lleva tu
> número.

Y la del turno en que el jugador sobreescribe su propia serie:

> — Tu serie de las 13:00 y tu serie de las 13:20 son la misma: la misma
> redirección la vació antes de escribirla. Un `>` vacía primero y escribe
> después. Lo vaciado no vuelve. Copia antes de tapar.

Líneas del Auditor (canal kármico §3.3, canal 2). Perfil azul:

> Expediente 000: acceso reiterado a registros de facturación con
> conservación de copias. Clasificación: acumulación. Continuidad del
> ensayo: estable.

Perfil rojo:

> Expediente 000: acceso reiterado a registros de facturación con
> destrucción de originales. Clasificación: acumulación con pérdida.
> Continuidad del ensayo: estable.

---

## GANCHO DE CIERRE — La palabra

El informe del Auditor del encargo de cierre incluye, por fin, el destino
de la sesión fantasma. La petición salió de la centralita del 12B, cruzó
dos nodos y murió en el Umbral alto, en una subestación secundaria en
servicio. Lo que pedía no era una factura:

```
solicitud de volcado: censo · sector 12 · marcas incluidas
estado: DENEGADA — permisos de oficina requeridos
reintento programado: sí
```

Ceniza lee la línea dos veces y aparta la terminal:

> — Volcado del censo con marcas. Cada vecino es una línea; cada purga, una
> marca encima. Lumen lo llama continuidad. Los que firmamos partes de esa
> máquina lo llamamos de otro modo: la Lista. No la nombres fuera de esta
> sala.

El boletín de las 07:00, la voz calmada de siempre:

> ...el incidente de facturación del sector 12 se considera resuelto. Los
> protocolos de continuidad han restablecido el servicio con garantías. La
> confianza de los vecinos sigue siendo nuestro mejor activo. Gracias por
> su colaboración.

En los días siguientes, la ventana de las 11:04 se volvió a abrir tres
veces. Ninguna lleva tu firma. El parte de la oficina no distingue entre
auditoría y visita. Uno de los dos papeles miente.

Y queda lo último. La petición denegada no nació en la centralita: solo
pasó por ella. Nació en el Umbral alto, en esa subestación secundaria que
es la copia en miniatura de la que te hace de casa, y ahí sigue: un proceso
corriendo, con tu número en la línea de argumentos. Ceniza lo pone en la
mesa con la misma voz con la que reparte turnos de guardia:

> — El proceso sigue vivo. Encuéntralo. Y esta vez no sales sin verlo.

*Fin del capítulo 2. Sigue en el capítulo 3 «Bombas»: cruzar el Umbral alto
buscando qué proceso abre ventanas con tu nombre.*

---

### Notas para el integrador

- Claves sugeridas: `story.ch2.apertura`, `story.ch2.e1`–`story.ch2.e5`,
  `story.ch2.ceniza`, `story.ch2.zeta1`, `story.ch2.postmortem_ceniza`,
  `story.ch2.auditor_azul`, `story.ch2.auditor_rojo`, `story.ch2.lista`.
- Voz verificada contra PERSONAJES.md (Ceniza, Gris, Zeta, Auditor, Vela).
  Test del nombre tapado: cada línea reconocible por su dueño.
- Karma de cap. 2: E1/E2 azules, E3 gris, E4 rojo, E5 de cierre con ambas
  salidas. Aceptar suma poco; lo que manda es cómo se resuelve cada run
  (DESIGN §3.3).
- ⚠️ El bloque de terminal de la apertura usa PIPES: el sandbox aún no los
  soporta (rechazo didáctico de S3, PR #5). Cuando el cap. 2 entre en el
  currículo y el sandbox gane tuberías, verificar el bloque byte a byte
  contra el test canónico de la sesión ch2, igual que el cap. 0 se verifica
  contra `test_session_cap0.py` (cierre del bucle que pidió Oscar, 🧭5 del
  28/08: prosa que describe salida de pantalla se contrasta con el FS).
  Hasta entonces, el bloque es contrato pedagógico, no salida reproducible.
- El FS de cap. 2 extiende el fixture del cap. 0 (misma oficina, ahora con
  `centralita/turnos/` y `centralita/facturas/`). La línea `11:04 SIN
  REGISTRO` de `log.txt` ya existe en el test del cap. 0: es canon, no la
  toqué.
- El ruido 6 de la sesión canónica es el gasto real de la secuencia del
  cap. 0 (ls 1 + cat 1 + cp 3 + cd 0 + ls 1). La sesión fantasma gasta 1
  (una petición denegada). No cambiar ninguna de las dos cifras sin tocar
  el canon del cap. 0 y el informe del Auditor.
- Continuidad de 47: el proveedor CANDELAS nº 47 (cap. 0), la placa
  `HOSP-47-C` del rack del Hub y la NHC 47-C-0191 de la pulsera comparten
  el 47. No se explica en el juego; quien lo note, nota.
