import asyncio
from pathlib import Path
from types import SimpleNamespace
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


def test_snapshot_written(monkeypatch, tmp_path):
    monkeypatch.setattr(notifier.httpx, "AsyncClient", lambda *a, **k: FakeClient())
    monkeypatch.setattr(notifier.settings, "SENDGRID_API_KEY", "x")
    monkeypatch.setattr(notifier.settings, "SENDGRID_TO", "t@example.com")
    monkeypatch.setattr(notifier.settings, "SENDGRID_FROM", "noreply@example.com")
    monkeypatch.setattr(notifier, "REPO_ROOT", tmp_path)

    listing = SimpleNamespace(url="u", title="t", price=1)
    asyncio.run(notifier.send_digest([listing]))
    files = list((tmp_path / "docs" / "SampleOutputs").glob("*_digest.md"))
    assert len(files) == 1

