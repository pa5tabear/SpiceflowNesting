from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Source, Listing, Score


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(bind=engine)


def test_crud_and_constraints():
    db = setup_db()
    src = Source(name="zillow", url="https://zillow.com")
    db.add(src)
    db.commit()
    lst = Listing(source_id=src.id, source_uid="1", url="url")
    db.add(lst)
    db.commit()

    # unique constraint
    dup = Listing(source_id=src.id, source_uid="1", url="u")
    db.add(dup)
    try:
        db.commit()
        raise AssertionError("unique constraint not enforced")
    except Exception:
        db.rollback()

    sc = Score(listing_id=lst.id, score=50)
    db.add(sc)
    db.commit()
    assert db.query(Score).count() == 1

    db.close()
