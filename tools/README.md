# tools — utilidades raíz

## resolutor_huellas.py

Resolutor canónico de colisiones de huellas (`activo.md` + `worklog`).

Cuando dos turnos del Concilio escriben el mismo fichero (p.ej. Ornstein y
Smough tocan `activo.md` a la vez, o Manus/Oscar/Havel/Gwyndolin tocan
`worklog/2026/09/26.md`), el merge deja marcadores `<<<<<<<`/`=======`/`>>>>>>>`.
Antes cada noche se reimprimía un script ad-hoc; desde 26/09 hay uno canónico.

### Uso

```bash
# Resolver ficheros (expande marcadores, deduplica por sección, reordena cronológico, verifica cero <<<<<<<)
python tools/resolutor_huellas.py backlog/tareas/en-curso/activo.md docs/worklog/2026/09/26.md

# Solo validar (usado por Artorias/Gwyn en el gate)
python tools/resolutor_huellas.py --check backlog/tareas/en-curso/activo.md docs/worklog/2026/09/26.md
# exit 0 = limpio, exit 1 = quedan marcadores o reorden pendiente

# Orden explícito (por defecto el canónico del Concilio: 03,05,07,11,13,16,19,21,23)
python tools/resolutor_huellas.py --order 03:00,05:00,07:00,11:00,13:00,16:00,19:00,21:00,23:00 activo.md
```

### Qué hace

1. **Expande marcadores anidados** — elimina todas las líneas `<<<<<<<`, `=======`, `>>>>>>>` (iterativo, soporta anidados).
2. **Dedupe por sección `## HH:00`** — mantiene UNA copia por cabecera. Si dos copias son idénticas, colapsa silencioso; si difieren, se queda la más reciente y avisa por `stderr`.
3. **Reordena cronológico** — ordena secciones por hora (`03:00`→`23:00`) según el orden esperado; preámbulo y secciones sin hora van donde tocan.
4. **Assertions** — ninguna sección con hora se pierde; salida con CERO `<<<<<<<` por línea (si queda, `exit 1`).
5. **Modo `--check`** — valida sin escribir (para CI/gate).

### Fixtures de prueba

Los tests en `tests/tools/test_resolutor_huellas.py` usan ejemplos sintéticos
inspirados en las colisiones reales de 24/09 y 25/09 (activo.md + worklog con
marcadores anidados y secciones duplicadas).

Python 3 sin deps nuevas.
