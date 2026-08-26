# karma.py — Contabilidad Blue/Red

> **Qué hace:** registra cada decisión kármica `{momento, acción, peso,
> timestamp}` y calcula el valor K = suma ponderada de las últimas N=8
> entradas. Expone bandas y condiciones de finales. Es contabilidad invisible:
> aquí no hay UI y jamás la habrá.
>
> Normativa: `docs/DESIGN.md` §3.1–3.5 · `../ARCHITECTURE.md` §2.8.

## API conceptual
- `registrar(momento, accion, peso)` — micro (dentro de run: datos civiles,
  credenciales, puertas traseras, logs §3.3) o macro (Hub: encargos, grieta de
  Ceniza, ventas a Gris).
- `valor()` → K actual · `banda()` → azul / mixta / roja.
- `cumple(final)` → requisitos de LUZ PLENA / NOCHE LARGA / EL TRATO /
  APAGÓN PROPIO según §3.4.1 (los otros sistemas aportan lo suyo: prueba
  íntegra, palanca del Auditor, arcos, fragmentos).
- Deriva: pesan las últimas 8 — redimirse cuesta, traicionar es rápido (§3.2).

## Reglas duras
- **El karma NUNCA modifica currículo ni dificultad técnica** (§3.1): toca
  textos, encargos ofrecidos, stock y finales — nada de pools del generador.
- Umbrales T_alto/T_bajo y N=8: constantes ⚠️ v1 documentadas; los calibra el
  harness midiendo cuántas runs limpias rehabilitan a un operador sangriento.
- Serializable y testeable: es UNA variable con historial, nada opaco.

## Cómo se testea
- Secuencias de decisiones → K exacto tras cada una; ventana N=8 correcta.
- Bandas excluyentes y HERENCIA superpuesta (§3.4.1).
- Contraste headless mínimo: perfiles azul/rojo forzados con mismas seeds →
  lecturas distintas de stock/encargos (protocolo completo: §8.6, harness).

## Dueño
Seath (`feat/meta-ui`).
