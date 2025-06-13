from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl | str = (
        "postgresql+psycopg://ai_bot:ai_bot@localhost:5432/ai_bot"
    )
    GEOCODER_API_KEY: str | None = None
    OPENAI_API_KEY: str = ""
    SENDGRID_API_KEY: str | None = None
    SENDGRID_TO: str | None = None
    SENDGRID_FROM: str = "noreply@example.com"
    SLACK_WEBHOOK_URL: str | None = None
    DOWNTOWN_LAT: float = 42.2808
    DOWNTOWN_LON: float = -83.7480
    MAX_DISTANCE_MILES: float = 1.0
    RUN_INTERVAL_HOURS: int = 6

    class Config:
        env_file = Path(__file__).with_suffix(".env")


settings = Settings()
