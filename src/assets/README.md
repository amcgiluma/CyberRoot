# assets/ — Arte binario consumido por render/

> **Qué hay:** recursos NO serializables que Pyxel carga directamente.
> Nada de lógica, nada de datos de juego (eso va a `data/`).

## Previsto

| Carpeta | Contenido | Notas |
|---|---|---|
| `fonts/` | fuente bitmap 5×7 estilo consola (el riesgo nº 1 del stack — validarla con capturas ANTES de construir UI encima) | INVESTIGACION-STACK ⚠️ |
| `palette/` | paleta CRT propia `.pyxpal` (fósforo verde/ámbar, rojo Lumen, dorado hallazgo) | §8.5; se redefine en runtime vía `pyxel.colors` |
| `sprites/` | nodos del mapa (conectado/comprometido/quemado), iconos de boon por familia, retratos pixel-art del Hub | §8.5: cada sprite comunica estado |
| `sfx/` | chiptune 4 canales: acierto, pipeline, hallazgo crítico, alerta, expulsión sobria | §7.4 |

## Reglas
1. Solo lo toca **Seath** (`feat/meta-ui`) — mismo dueño que `render/`.
2. Formato nativo de Pyxel (.pyxres/.pyxpal) o PNG fuente; nombres estables:
   renombrar un asset rompe referencias silenciosamente.
3. Los 4 colores SEMÁNTICOS (§8.5) se respetan en TODO asset nuevo.
4. Arte «bonito suelto» prohibido: pixel-art funcional que comunica estado.
