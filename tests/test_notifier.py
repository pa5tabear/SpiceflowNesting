from types import SimpleNamespace
from notifier import render_digest


def test_render_digest_inline():
    listing = SimpleNamespace(url="u", title="Title", price=100)
    html = render_digest([listing])
    assert "style=" in html
    assert "<b>Title</b>" in html
