# engine/ — El motor roguelite

> **Qué hace:** dirige el ciclo completo de una incursión y su vuelta al Hub:
> mapa de nodos → salas → extracción/detección → liquidación → post-mortem.
> Orquesta `sandbox/` (ejecuta comandos) y `generator/` (crea la incursión);
> aplica las reglas de números del diseño.
>
> Normativa: `docs/DESIGN.md` §4.1 (loop), §7 (dopamina/números), §4.7 (Hub) ·
> arquitectura: `../ARCHITECTURE.md` §2.5.

## Responsabilidades
- **Run**: estado de la incursión, sala actual, rutas, entradas/salidas de
  sala; modos mapa↔terminal como ESTADOS del core (el render solo los pinta).
- **Vigilancia/detección**: % sube por ruido de acciones (regla de luz §6.0.2:
  más luz = más vigilancia base por anillo). NUNCA sube por reloj artificial
  (§7.9). Al llegar al umbral → expulsión.
- **Economía DATOS×COMBO** (§7.1): base por tipo de dato; combo por escalones
  (+0,1 por cadena limpia, baja UN escalón por fallo, DOS por tramo de
  detección); liquidación total al extraer, parcial (50 % ⚠️ v1 de lo ya
  extraído, sin combo) al ser expulsado + bonus de profundidad (§7.7).
- **Apuestas de run** (§7.3): deep scan, ruta ruidosa, «una sala más».
- **Sinergias** (§5.2, catálogo v1 en §7.8): detección de disparadores
  pipeline/recon→ejecución/estado persistente/etc., leyendo el historial de
  comandos de la run. Los efectos son numéricos/eventos — el juice lo añade el
  render con los mismos eventos.
- **Cierre de run**: informe post-mortem (siempre, §4.7) + cola de eventos
  hacia el Hub (historia avance SIEMPRE — el contenido vive en `data/story/`).
- Números calibrables: constantes documentadas en un solo sitio para que el
  harness las ajuste sin reescribir lógica.

## Entradas / salidas
- ENTRADA: comandos de jugador (`exec`, `ui.*`) + `IncursionInstance` del
  generador + perfil del jugador (boons, karma).
- SALIDA: mutaciones de estado de run + `Event`s (combo, alerta, hallazgo,
  expulsión, liquidación…).

## Cómo se testea
- Run completa headless: resolver una incursión sembrada ejecutando su
  secuencia canónica → éxito esperado, métricas exactas.
- Expulsión forzada (ruido máximo) → parcial cobrado correcto, lección en cola,
  avance narrativo presente.
- Combo: cadenas limpias/fallidas/tramos de alerta → escalones exactos.
- Determinismo: misma seed + mismos comandos → misma partida entera.

## Dueño
Ornstein (`feat/engine`). También construye `tools/harness/` sobre esta API.
