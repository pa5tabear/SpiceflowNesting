import scheduler


def test_cli_exit(monkeypatch):
    called = {}

    async def fake_run_once():
        called["x"] = True

    monkeypatch.setattr(scheduler, "run_once", fake_run_once)
    scheduler.cli(["run-once"])
    assert called.get("x")
