import asyncio
from types import SimpleNamespace
from loguru import logger
import notifier


class FakeClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def post(self, *args, **kwargs):
        class R:
            def raise_for_status(self):
                pass

        return R()


def test_log_line(monkeypatch):
    out = []
    logger.add(out.append, format="{message}")
    monkeypatch.setattr(notifier.httpx, "AsyncClient", lambda *a, **k: FakeClient())
    monkeypatch.setattr(notifier.settings, "SENDGRID_API_KEY", "x")
    monkeypatch.setattr(notifier.settings, "SENDGRID_TO", "t@example.com")
    monkeypatch.setattr(notifier.settings, "SENDGRID_FROM", "noreply@example.com")
    listing = SimpleNamespace(url="u", title="t", price=1)
    asyncio.run(notifier.send_digest([listing]))
    assert any("Digest sent" in m for m in out)
