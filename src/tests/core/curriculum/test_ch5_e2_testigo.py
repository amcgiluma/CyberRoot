"""S2 Smough 17/09 — story.ch5.e2 «El testigo que no llegó».

Verifica la reescritura grey [c.cat, c.scp] y su briefing documenta
la ausencia como pista (No such file). Flexible si O1 no entrega FS nuevo:
la quest lee /srv/camara-faro/volcado-rescate.csv que ya planta dato7.
"""

from core.curriculum import load_curriculum
from data.textos import load_textos, resolve


def test_ch5_e2_existe_grey_cat_scp() -> None:
    cur = load_curriculum()
    q = cur.quest("story.ch5.e2")
    assert q is not None
    assert q.chapter == 5
    assert q.tint == "grey"
    assert sorted(q.requires) == ["c.cat", "c.scp"]


def test_ch5_e2_textos_documenta_ausencia_y_ruta_absoluta() -> None:
    t = load_textos()
    title = resolve("story.ch5.e2.title", textos=t)
    beat = resolve("story.ch5.e2.beat", textos=t)
    assert title == "El testigo que no llegó"
    assert "/srv/camara-faro/volcado-rescate.csv" in beat
    assert "cat /srv/camara-faro/volcado-rescate.csv" in beat
    assert "No such file" in beat
    # pista documentada de Oscar
    assert "si lo subiste" in beat.lower()
