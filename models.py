from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base
import datetime as dt

Base = declarative_base()


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)


class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    source_uid = Column(String, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String)
    price = Column(Integer)
    beds = Column(Float)
    baths = Column(Float)
    sqft = Column(Integer, nullable=True)
    lat = Column(Float)
    lon = Column(Float)
    amenities = Column(String)
    first_seen = Column(DateTime, default=dt.datetime.utcnow)
    last_seen = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow
    )
    __table_args__ = (
        UniqueConstraint("source_id", "source_uid", name="uix_source_uid"),
    )


class Score(Base):
    __tablename__ = "scores"
    listing_id = Column(Integer, ForeignKey("listings.id"), primary_key=True)
    score = Column(Float)
    subscores = Column(String)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
