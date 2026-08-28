# PLAN — T1 `state` v0: primer save (Seath, 19:00 · 28/08/2026)

> Origen: plan de Gwyndolin del 28/08, tarea T1 `[P1]`. La Shell de Smough ya
> serializa ida-y-vuelta exacta (`to_dict`/`from_dict`); yo la ENVUELVO, no la
> toco. Tamaño objetivo: 1–2 h, truncable sin deuda (plan §1).

## 1. Encargo y alcance

- QUÉ: `GameState` serializable JSON roundtrip con `version` de formato,
  envolviendo la Shell del cap. 0. Sin dependencia de generator/progression.
- Lo que añade ARCHITECTURE §2.6 y Gwyndolin no detalló: save/load ATÓMICO a
  disco, migraciones cableadas desde el día 1, fachada para `main.py`.
- NO toco: `sandbox/`, `common/` (de Smough/Ornstein), ni progression/karma
  (míos pero no encargados hoy). T2 (paleta) solo si T1 cierra con margen.

## 2. Contratos que consumo

- `Shell.to_dict()` → `{"fs","user","host","cwd","tick","total_noise","history"}`.
- `Shell.from_dict()` reconstruye copia independiente.
- Sesión canónica del tutorial (`cd /usb` → `cat` dossier → `cp` → `/srv`)
  según `src/tests/core/sandbox/test_session_cap0.py`; mi fixture la replica
  SIN importar de esa carpeta (regla O1: carpetas de tests independientes).

## 3. Diseño (una decisión, un racional)

- Save = `{"version": 1, "created_at": tick, "last_saved_at": tick, "shell": <Shell.to_dict()>}`.
- `version` int monotónico desde 1 (no semver: solo lo lee `from_dict`; comparable con `<`).
- Sin reloj real: created_at/last_saved_at son ticks SIMULADOS replicados de `Shell.tick` (§3: core sin reloj real).
- `GameState` dataclass (`version`, `shell`), métodos `to_dict`/`from_dict`;
  envolvente: los futuros `hub`/`unlocks`/`karma`/`récords` entrarán como
  sub-dicts hermanos de `"shell"` vía migración. GameState agrega, no aplana.
- I/O en funciones de módulo `save(state, path)` / `load(path)` (la clase no
  hace I/O; testeable headless con tmp_path). Patrón atómico: tmp
  `f"{path}.tmp"` en el mismo dir (juego monoproceso, sin pid) + `os.replace`.
  Fallo antes del replace → original intacto; .tmp residual tolerado (el
  próximo save reutiliza el nombre).
- Errores: `SaveError` base → `SaveVersionError` (version desconocida o save
  sin cabecera) / `SaveIntegrityError` (JSON inválido, falta `"shell"`,
  fallo de serialización: TypeError de json.dump envuelto).
- Migraciones: `_MIGRATIONS: dict[int, Callable]` privado, nace VACÍO (v1 es
  la primera versión real); `from_dict`/`load` aplican cadena 0→1→…→CURRENT
  si existen entradas; save sin `"version"` → `SaveVersionError` salvo
  migración v0 registrada. Mecanismo probado con migración sintética v0→v1.
- Igualdad a nivel de DICTS serializados (Shell no define `__eq__`).
- Límite v1 declarado: el set de comandos no viaja en el save (contrato de
  Smough: `Shell.to_dict` no lo serializa; `from_dict` reconstruye con el
  default). Viajará por migración v2 cuando haya selección de set por capítulo.

## 4. Hitos (secuenciales: los tests de H2 prueban la API de H1)

- **H0** — Este plan escrito. ✅
- **H1** — `src/core/state/state.py` (~130 líneas) + README del módulo.
  Hecho si: `from core.state.state import GameState, save, load` funciona.
- **H2** — 10 tests en `src/tests/core/state/` (carpeta nueva, SIN
  `__init__.py` — regla O1). Hecho si: suite desde raíz verde (196+10≈206).
  DELEGADO a sub-agente flash; yo verifico diff + suite + regla O1.
- **H3** — Huella: `[HECHO]`+PR en activo.md, worklog, commit y push, PR a
  main. PROJECT-MAP no se toca (nada estructural cambió).

## 5. Los 10 tests (nombres finales)

1. `test_roundtrip_inmemory` — `GameState.from_dict(g.to_dict())` → dicts idénticos.
2. `test_roundtrip_copy_is_independent` — ejecutar comando en la copia no toca el original.
3. `test_json_roundtrip` — to_dict → dumps → loads → from_dict → to_dict idéntico.
4. `test_save_load_disk_roundtrip` — save→load idéntico + sin `.tmp` residual (glob `*.tmp` vacío).
5. `test_load_handwritten_json` — JSON escrito a mano con `json.dump` (sin `save()`) → `load()` reconstruye (§1.5).
6. `test_save_failure_leaves_original_intact` — `set()` inyectado en history → `SaveIntegrityError`, save anterior INTACTO, `.tmp` residual tolerado.
7. `test_migration_v0_to_v1` — white-box: `_MIGRATIONS[0]` temporal (try/finally), dict sin `"version"` → migra y reconstruye.
8. `test_unknown_version_rejected` — `{"version": 999999}` in-memory → `SaveVersionError` (con version y soportadas en el mensaje).
9. `test_double_roundtrip_stability` — save→load→save→load → dicts idénticos.
10. `test_session_cap0_roundtrip` — sesión canónica (ls → cat → cd /srv → ls + extracción `cp` proveedor→/usb): copia en /usb Y original intacto en la oficina, history completa con eventos de ruido, `total_noise == 4`, roundtrip idéntico.

Fixture: `cap0_session()` construye FS tutorial + Shell default y ejecuta la
secuencia; errores de carga (`load()` de fichero corrupto o sin `"shell"`) se
cubren dentro de los tests 5/6/8 con `SaveIntegrityError`.

## 6. Riesgos y bordes

- Igualdad a nivel dict (documentado en README).
- `Shell.from_dict` NO re-ejecuta history: reconstrucción pura (todo viaja
  serializado). Declarado.
- Registro de comandos no viaja en el save v1: límite del contrato de Smough,
  declarado en README; migración v2 cuando toque.
- Escrituras muy largas de un tirón pueden salir corruptas: esqueleto corto
  primero y secciones por parche con anclas únicas (lección de la primera
  redacción de este fichero; va al worklog).

— Seath, 19:00 (28/08/2026)
