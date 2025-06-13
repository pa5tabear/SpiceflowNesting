from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from prometheus_client import Counter

from config import settings
from models import Score

app = FastAPI()
engine = create_engine(settings.DATABASE_URL, future=True, echo=False)
Session = sessionmaker(engine)

FEEDBACK_COUNTER = Counter("feedback_total", "User feedback events")


class Feedback(BaseModel):
    listing_id: int
    feedback: int


@app.post("/feedback")
def submit_feedback(item: Feedback):
    db = Session()
    db.query(Score).filter_by(listing_id=item.listing_id).update(
        {"feedback": item.feedback}
    )
    db.commit()
    db.close()
    FEEDBACK_COUNTER.inc()
    logger.info("Feedback %s for listing %s", item.feedback, item.listing_id)
    return {"status": "ok"}
