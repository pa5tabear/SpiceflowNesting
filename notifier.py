from pathlib import Path
from datetime import date
import httpx
from loguru import logger
from prometheus_client import Counter
from config import settings

TEMPLATE = Path(__file__).parent / "templates" / "digest.html"

# Repository root used for storing digest snapshots
REPO_ROOT = Path(__file__).resolve().parent

EMAIL_COUNTER = Counter("emails_sent_total", "Digest emails sent")


def _save_snapshot(html: str) -> None:
    """Write a copy of the latest digest to docs/SampleOutputs."""
    out_dir = REPO_ROOT / "docs" / "SampleOutputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{date.today()}_digest.md"
    (out_dir / fname).write_text(html)


def render_digest(listings):
    base = TEMPLATE.read_text()
    cards = []
    for item in listings:
        cards.append(
            f'<div style="border:1px solid #ddd;padding:8px;margin:4px">'
            f'<a href="{getattr(item, "url", "")}"><b>{getattr(item, "title", "")}</b></a>'
            f' ${getattr(item, "price", "")}</div>'
        )
    return base.replace("{{cards}}", "\n".join(cards))


async def send_digest(listings):
    if not settings.SENDGRID_API_KEY or not listings:
        return
    html = render_digest(listings)
    payload = {
        "personalizations": [
            {"to": [{"email": settings.SENDGRID_TO or "test@example.com"}]}
        ],
        "from": {"email": settings.SENDGRID_FROM or "noreply@example.com"},
        "subject": "Daily digest",
        "content": [{"type": "text/html", "value": html}],
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=payload,
            headers={"Authorization": f"Bearer {settings.SENDGRID_API_KEY}"},
        )
        resp.raise_for_status()
    _save_snapshot(html)
    EMAIL_COUNTER.inc()
    logger.info("Digest sent with %d listings", len(listings))
