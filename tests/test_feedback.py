from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import feedback
from models import Base, Score


def setup_app(monkeypatch):
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    monkeypatch.setattr(feedback, "Session", Session)
    return TestClient(feedback.app), Session


def test_feedback_updates_score(monkeypatch):
    client, Session = setup_app(monkeypatch)
    db = Session()
    db.add(Score(listing_id=1, score=50))
    db.commit()
    db.close()
    resp = client.post("/feedback", json={"listing_id": 1, "feedback": 1})
    assert resp.status_code == 200
    db = Session()
    row = db.query(Score).filter_by(listing_id=1).first()
    assert row.feedback == 1
