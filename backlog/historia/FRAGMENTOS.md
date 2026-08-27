# FRAGMENTOS — El pasado de Cero (botín narrativo H1/H2)

> Botín raro repartido en capítulos 1–6 con probabilidad baja fija (§2.2,
> §6.1-notas). ORDEN FIJO POR CAPÍTULO decidido en P5 (§9): la seed solo
> decide la piel del objeto, no cuál toca — controla el ritmo del misterio.
>
> Cada fragmento sostiene DOS hipótesis a la vez:
> **H1** — borraste tu pasado tú · **H2** — te lo borraron como ensayo.
>
> Formato (regla §2.6.6): dato técnico arriba, grieta humana abajo, UN número
> concreto por descripción. Cero adjetivos atmosféricos.

## Orden canónico (por cerrar con contenido)

| # | Capítulo | Fragmento (idea de DESIGN) | Estado |
|---|---|---|---|
| 1 | 1 | foto con los metadatos raspados | [LISTA] |
| 2 | 2 | pulsera de hospital con fecha | [PENDIENTE] |
| 3 | 3 | contrato de alquiler a nombre de nadie | [PENDIENTE] |
| 4 | 4 | cuenta que recibió pagos mensuales de una filial de Lumen hasta hace 3 años | [PENDIENTE] |
| 5 | 5 | expediente médico del hospital del Muelle (el de Vela existe — ¿y este?) | [PENDIENTE] |
| 6 | 6 | hoja de cierre del Programa de Continuidad: sujeto 000, fecha en blanco | [PENDIENTE] |

## Fragmento 1 — La foto (cap. 1, botín raro)

> **Formato**: sabes cómo llega al inventario (integrador → `src/data/story/`),
> no qué significa. Está escrito para leerse plausible en H1 y en H2 a la vez.

Imagen JPEG, 640×480, 214 KB, código `IMG_0000007.JPG`. Los metadatos EXIF
borrados con herramienta de sobreescritura: campo de fecha vacío, modelo de
cámara tachado, coordenadas raspadas hasta el byte. Quien lo limpió conocía
la utilidad que deja la cabecera intacta.

En el encuadre, dos personas delante de un edificio con letrero de fachada en
neón: «FACTURACIÓN 24H — MUELLE NORTE». La del fondo tiene el brazo levantado,
saludando o tapando la cara. La de primer plano no se ve: un dedo cubre el
objetivo. Se distingue, entre el pulgar y el índice, un fragmento de la manga:
tela azul de uniforme con un borde blanco.

Detrás del dedo, la puerta del edificio está entreabierta. Nadie se acuerda de
haber tenido este día.

## Reglas para escribirlos
- Nunca resuelven H1 vs H2: cada uno debe leerse plausible en ambas.
- El último (nº 6) solo aparece si el jugador llega al Faro; alimenta
  APAGÓN PROPIO (requisito «último fragmento», §3.4.1).
- No puntúan: son botín narrativo puro (§7.1).

## Estado
0/6 escritos. Dueño: Manus. Integración a `src/data/story/` la hace el
ejecutor integrador cuando estén `[LISTA]`.
