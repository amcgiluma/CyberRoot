"""test_types.py — especificación determinista de Command + ensure_plain
(DESIGN §1.2 contrato plano, §4.5 determinismo, §3 textos; ARCHITECTURE §2.1).

Garantías bajo test:
- Command ida-y-vuelta: `to_dict`/`from_dict` son inversas exactas.
- El "cmd" canónico gana: `args` NO puede colisionar con la clave `"cmd"`
  (prohibido en `__post_init__`), luego `to_dict` es seguro y sin ambigüedad.
- `from_dict` rechaza basura con `InvalidCommandError` (no ValueError).
- `__post_init__` valida: cmd no vacío, claves args str, sin "cmd" en args.
- `ensure_plain` acepta JSON plano ESTRICTO y rechaza todo lo demás,
  incl. ciclos y profundidad >64, con mensajes que incluyen la RUTA del fallo.
- `SeedLike` / `TextKey` son alias documentados (isinstance vs su real).

Solo stdlib + pytest; sin `import random`.
"""

from __future__ import annotations

import pytest

from core.common.errors import CyberRootError, InvalidCommandError, NotPlainDataError
from core.common.types import Command, SeedLike, TextKey, ensure_plain


# ----------------------------------------------------------------------------
# Command: roundtrip to_dict / from_dict
# ----------------------------------------------------------------------------
def test_command_roundtrip_to_dict() -> None:
    c = Command("exec", {"argv": ["ls", "-la"], "cwd": "/root"})
    assert c.to_dict() == {"cmd": "exec", "argv": ["ls", "-la"], "cwd": "/root"}


def test_command_roundtrip_from_dict_igual_al_original() -> None:
    c = Command("exec", {"argv": ["ls", "-la"], "cwd": "/root"})
    assert Command.from_dict(c.to_dict()) == c  # frozen dataclass eq total


def test_command_json_roundtrip_byte_a_byte() -> None:
    import json

    c = Command("move", {"dx": 1, "dy": -2, "flags": [True, None, 3.5]})
    assert json.dumps(c.to_dict(), sort_keys=True) == json.dumps(
        Command.from_dict(c.to_dict()).to_dict(), sort_keys=True
    )


def test_command_sin_args_defaults_a_dict_vacio() -> None:
    c = Command("rest")
    assert c.args == {}
    assert c.to_dict() == {"cmd": "rest"}
    assert Command.from_dict(c.to_dict()) == c


def test_to_dict_devuelve_dict_nuevo_por_cada_llamada() -> None:
    c = Command("exec")
    d1 = c.to_dict()
    d2 = c.to_dict()
    assert d1 == d2
    assert d1 is not d2
    d1["extra"] = 1  # mutar la salida no afecta al Command ni a otras salidas
    assert "extra" not in c.to_dict()


# ----------------------------------------------------------------------------
# Command: "cmd" reservado en args está PROHIBIDO (el canónico manda)
# ----------------------------------------------------------------------------
def test_args_con_clave_cmd_lanza_valueerror_al_crear() -> None:
    with pytest.raises(ValueError, match="cmd"):
        Command("exec", {"cmd": "mover"})


# ----------------------------------------------------------------------------
# Command: post_init validación
# ----------------------------------------------------------------------------
def test_post_init_cmd_vacio_o_no_str_lanza_valueerror() -> None:
    with pytest.raises(ValueError, match="vac"):
        Command("")
    with pytest.raises(ValueError, match="str"):
        Command(42)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="str"):
        Command(None)  # type: ignore[arg-type]


def test_post_init_args_no_str_key_lanza_typeerror() -> None:
    with pytest.raises(TypeError, match="claves str"):
        Command("exec", {1: "x"})  # type: ignore[dict-item]
    with pytest.raises(TypeError, match="claves str"):
        Command("exec", {("a",): 1})  # type: ignore[dict-item]


def test_post_init_args_no_mapping_lanza_valueerror() -> None:
    with pytest.raises(ValueError, match="Mapping"):
        Command("exec", "no-soy-mapping")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Mapping"):
        Command("exec", [1, 2])  # type: ignore[arg-type]


def test_post_init_args_none_es_dict_vacio() -> None:
    assert Command("exec", None).args == {}  # type: ignore[arg-type]


# ----------------------------------------------------------------------------
# Command: from_dict errores → InvalidCommandError
# ----------------------------------------------------------------------------
def test_from_dict_no_mapping_lanza_invalid_command() -> None:
    for bad in ([1, 2], "exec", None, 42, 3.5, object(), (1, 2)):
        with pytest.raises(InvalidCommandError):
            Command.from_dict(bad)  # type: ignore[arg-type]


def test_from_dict_sin_cmd_lanza_invalid_command() -> None:
    for bad in ({}, {"argv": []}, {"cualquier": 1}):
        with pytest.raises(InvalidCommandError, match="cmd"):
            Command.from_dict(bad)


def test_from_dict_cmd_no_str_o_vacio_lanza_invalid_command() -> None:
    for bad in ({"cmd": ""}, {"cmd": None}, {"cmd": 42}, {"cmd": []}):
        with pytest.raises(InvalidCommandError, match="cmd"):
            Command.from_dict(bad)  # type: ignore[dict-item]


def test_from_dict_cmd_extra_no_se_toca_de_args() -> None:
    c = Command.from_dict({"cmd": "exec", "argv": [1], "meta": {"a": 1}})
    assert c.cmd == "exec"
    assert c.args == {"argv": [1], "meta": {"a": 1}}
    assert "cmd" not in c.args


def test_errores_son_del_dominio_cyberroot() -> None:
    # Jerarquía de dominio: ambas hijas son CyberRootError, que es Exception.
    assert issubclass(InvalidCommandError, CyberRootError)
    assert issubclass(NotPlainDataError, CyberRootError)
    assert issubclass(CyberRootError, Exception)
    with pytest.raises(CyberRootError):
        Command.from_dict("basura")  # type: ignore[arg-type]


# ----------------------------------------------------------------------------
# ensure_plain: acepta JSON plano ESTRICTO
# ----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "ok",
    [
        None,
        True,
        False,
        0,
        -17,
        3_000_000_000_000_000_000,
        3.5,
        -0.0,
        "texto",
        "",
        [],
        {},
        [1, 2, 3],
        {"a": 1, "b": [True, None, {"c": "x"}]},
        {"anidado": {"listas": [[], [{}], [None]]}},
    ],
)
def test_ensure_plain_acepta_valores_planos(ok: object) -> None:
    ensure_plain(ok)  # no debe lanzar


def test_ensure_plain_acepta_scalares_mixtos_profundos() -> None:
    ensure_plain({"run": {"seed": 123, "karma": 4.5, "flags": [True, "x", None]}})


def test_ensure_plain_acepta_dicts_y_listas_vacias() -> None:
    ensure_plain({})
    ensure_plain([])
    ensure_plain({"a": [], "b": {}})


# ----------------------------------------------------------------------------
# ensure_plain: rechaza todo lo NO plano
# ----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "bad",
    [
        (1, 2),                          # tuple
        {1, 2},                          # set
        frozenset(),                     # frozenset
        b"bytes",                        # bytes
        object(),                        # objeto arbitrario
        float("nan"),                    # float no finito
        float("inf"),
        float("-inf"),
        complex(1, 2),                   # complex no es float finito
        {1: "x"},                        # dict con clave no-str
    ],
)
def test_ensure_plain_rechaza_no_plano(bad: object) -> None:
    with pytest.raises(NotPlainDataError):
        ensure_plain(bad)  # type: ignore[arg-type]


def test_ensure_plain_rechaza_tuple_y_set_dentro_de_estructuras() -> None:
    with pytest.raises(NotPlainDataError):
        ensure_plain({"argv": ["a", ("b", "c")]})


def test_ensure_plain_rechaza_bytes_dentro_de_lista() -> None:
    with pytest.raises(NotPlainDataError):
        ensure_plain(["ok", b"\x00\xff"])


# ----------------------------------------------------------------------------
# ensure_plain: profundidad máx (64) y ciclos
# ----------------------------------------------------------------------------
def test_ensure_plain_profundidad_64_ok_y_65_rechazada() -> None:
    deep_64: object = 1
    for _ in range(64):
        deep_64 = [deep_64]
    ensure_plain(deep_64)  # 64 niveles de listas: válido

    deep_65: object = 1
    for _ in range(65):
        deep_65 = [deep_65]
    with pytest.raises(NotPlainDataError, match="profundidad"):
        ensure_plain(deep_65)


def test_ensure_plain_rechaza_ciclo_autorreferenciado() -> None:
    cyc: list[object] = []
    cyc.append(cyc)
    with pytest.raises(NotPlainDataError, match="ciclo"):
        ensure_plain(cyc)


def test_ensure_plain_rechaza_ciclo_en_dict() -> None:
    d: dict[str, object] = {"a": 1}
    d["self"] = d
    with pytest.raises(NotPlainDataError, match="profundidad"):
        ensure_plain(d)


# ----------------------------------------------------------------------------
# ensure_plain: mensajes con ruta del fallo
# ----------------------------------------------------------------------------
def test_mensaje_contiene_ruta_punto() -> None:
    with pytest.raises(NotPlainDataError) as ei:
        ensure_plain({"a": {"b": (1, 2)}})
    assert ".a.b" in str(ei.value)


def test_mensaje_contiene_ruta_corchete() -> None:
    with pytest.raises(NotPlainDataError) as ei:
        ensure_plain({"argv": ["ok", object()]})
    assert "argv[1]" in str(ei.value)


def test_mensaje_ruta_anidada_mixta_punto_y_corchete() -> None:
    with pytest.raises(NotPlainDataError) as ei:
        ensure_plain({"a": {"b": [["x"], ["y", object()]]}})
    # fallo en b[1][1].object() → ruta a.b[1][1] (objeto arbitrario, sin hijos)
    assert "a.b[1][1]" in str(ei.value)


def test_mensaje_raiz_personalizada() -> None:
    with pytest.raises(NotPlainDataError) as ei:
        ensure_plain({"x": {"y": object()}}, _root="run")
    assert "run.x.y" in str(ei.value)


def test_mensaje_rechazo_clave_no_str_menciona_la_raiz() -> None:
    with pytest.raises(NotPlainDataError) as ei:
        ensure_plain({1: "un"}, _root="raiz")
    assert "raiz" in str(ei.value)


def test_mensaje_rechazo_float_no_finito_menciona_el_valor() -> None:
    with pytest.raises(NotPlainDataError) as ei:
        ensure_plain(float("nan"))
    assert "nan" in str(ei.value).lower()


# ----------------------------------------------------------------------------
# Aliases documentados
# ----------------------------------------------------------------------------
def test_seedlike_es_union_de_int_str_bytes() -> None:
    for v in (0, "semilla", b"seed"):
        assert isinstance(v, SeedLike)
    for v in (None, 3.5, [1], object()):
        assert not isinstance(v, SeedLike)


def test_textkey_es_str() -> None:
    assert TextKey is str
    assert isinstance("text.key", TextKey)
    assert not isinstance(1, TextKey)