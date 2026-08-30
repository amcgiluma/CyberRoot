# ESCENARIOS — Lugares del Grid (Manus)

> Los lugares se describen con datos concretos (regla §2.6.6: un número por
> descripción), nunca con adjetivos atmosféricos. Cada escenario debe poder
> volverse mecánica o piel de sala del generador.

## Base fija

## La Subestación — el Hub
- Central eléctrica de la subcuenca 4, desconectada en el mes 18 de los
  Apagones (hace 19 años). Dos transformadores de 20 kV vacíos de aceite; el
  tablero de control conserva la luz de «CORTE MANUAL» encendida desde
  entonces.
- No hay factura porque no hay medidor vivo: la línea entró en «desafectada»
  en los libros de Lumen y nadie la reabrió. Ese es todo el secreto del
  lugar: no es escondida, es contable como muerta.
- Zonas jugables (mecánicas, §4.7):
  - **Terminal de informes post-mortem**: un rack rescatado del hospital del
    Muelle (placa `HOSP-47-C`), vuelto vertical. Aquí habla el Auditor y
    comenta Ceniza.
  - **Espejo de Gris**: un tablero magnético que fue de redes, con tres
    columnas de paneles (Hardware / Oficio / Red, §4.3). Gris lo toca como
    quien frota un amuleto.
  - **Mesa de encargos**: la tapa de un condensador, con papeles clavados con
    cinta. Es la única luz fija de la sala (una tira de LED robada).
  - **Rincón de Zeta**: una esquina limpia contra la que apoyan su silla
    basculante. No hay carteles; hay un contador de propias.
  - **Archivo de fragmentos**: cajones de un armario de fichas, numerados a
    mano (27–31 están vacíos).
- Luz: una línea principal de LED que Gris mantiene con las 08:00 de
  encendido; fuera de ella, oscuridad hasta los indicadores verdes de los
  equipos.

## Geografía (tres anillos — regla de mundo: más luz = más vigilancia)

## Anillo Faro
- Centro corporativo. Luz continua de sodio, sin noche: las luminarias no se
  apagan nunca, ni en avería (redundan en batería).
- Cobertura de sensores 100 % (dato diegético: más de 3 cámaras por cruce
  en vía principal). Es la sede del censo y de la Oficina de Continuidad.
- Alcanzarlo jugable significa cruzar el Umbral alto: la luz ES la dificultad
  (§6.0.2). Nodos: cámara del Programa de Continuidad, nodo maestro del censo.

## Anillo Umbral (bajo y alto)
- Residencial y oficinas de planta baja. Luz por sectores y horario: el bajo
  apaga a las 23:20, el alto mantiene dos avenidas encendidas toda la noche.
- Capítulos 1–3: facturas, registros civiles, centralita de facturación, nodos
  protegidos por permisos. La vigilancia crece con la luz: en el alto, la
  patrulla de auditoría pasa cada 22 minutos (dato de ritmo para retos).
- Capítulo 3 (Procesos y sistema): es el territorio del demonio del censo
  (E1), el bucle de reinicio (E2) y la subestación secundaria en servicio.
  Hora muerta característica en el canon: la 03:00 (turno sin registro).
- Cobertura del anillo (para el generador): los nodos del Alto asumen la
  factura de E3/E4, cuando la segunda mirada de la luz ya cobra en alertas.

## Los Muelles
- Afueras medio apagadas; base de Los Apagados. Docks con francesas de red
  robadas, grúas paradas desde el año 2 de los Apagones (nº 9 tiene el cable
  de izado enmohecido soldado a la pista).
- Capítulo 1 y capítulo 5 (asalto invertido a la Subestación). Luz escasa:
  aquí la vigilancia de Lumen no llega salvo en redadas puntuales, y eso lo
  convierte en refugio y en peligro a la vez (cuando Lumen entra, entra con
  hombres, no con sensores).
- Desde el cap. 1: un repeater vecinal cuelga de la grúa nº 9 y da red a
  media docena de casas fuera del censo (nodo de cierre del capítulo,
  `story.ch1.e5`). El buzón muerto del técnico filtrador es la lavandería
  «Ciclón», Calle del Estío (encargo `story.ch1.e2`).

## Nodos tipo (piel del generador — §6.4.3)
- **Oficina vecinal** (Umbral bajo): una línea telefónica, un cajero roto,
  carpetas de papel digitalizadas en un NAS sin cifrar.
- **Centralita de facturación** (Umbral bajo): pool de facturas, entrada con
  cols directorio; sube alerta si lo tocas fuera de horario.
- **Subestación secundaria** (Umbral alto): réplica en miniatura de la
  Subestación, en servicio y con mantenimiento remoto activo. Puerta a los
  procesos (cap. 3).
- **Nodo troncal** (frontera Umbral/Faro): concentra el tráfico de un anillo
  entero; exige red real (ssh, túneles) y credenciales (cap. 4).
- **Cámara del Programa de Continuidad** (Faro): el armario del censo con los
  expedientes cerrados; escenario de los beats 7 y del hallazgo del propio
  número vacío.
- **Nodo maestro del censo** (Faro): el núcleo contable. Quemarlo es abrir
  NOCHE LARGA; extraerlo en limpio, la palanca de LUZ PLENA.

## Estado
Escenarios con datos base: 6/6 (Subestación, Faro, Umbral bajo/alto, Muelles,
nodos tipo). ✅
Pendiente: el worldbuilding fino del censo (qué se puntúa exactamente) — dueño
Manus/Fase 1, bloquea las salas-dato del cap. 6 (§9, §6.6.4), no los cap. 0–4.