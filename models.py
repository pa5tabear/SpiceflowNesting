"""Database models and base class definitions."""

from __future__ import annotations

import datetime as dt

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase

__all__ = ["Source", "Listing", "Score", "Base"]


class Base(DeclarativeBase):
    """Base declarative class for all models."""


class Source(Base):
    """A site or API providing rental listings."""

    __tablename__ = "sources"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    url: str = Column(String, nullable=False)


class Listing(Base):
    """A single rental listing scraped from a source."""

    __tablename__ = "listings"

    id: int = Column(Integer, primary_key=True)
    source_id: int = Column(Integer, ForeignKey("sources.id"))
    source_uid: str = Column(String, nullable=False)
    url: str = Column(String, nullable=False)
    title: str | None = Column(String)
    price: int | None = Column(Integer)
    beds: float | None = Column(Float)
    baths: float | None = Column(Float)
    sqft: int | None = Column(Integer, nullable=True)
    lat: float | None = Column(Float)
    lon: float | None = Column(Float)
    amenities: str | None = Column(String)
    first_seen: dt.datetime = Column(DateTime, default=dt.datetime.utcnow)
    last_seen: dt.datetime = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow
    )
    __table_args__ = (
        UniqueConstraint("source_id", "source_uid", name="uix_source_uid"),
    )


class Score(Base):
    """Aggregated score information for a Listing."""

    __tablename__ = "scores"

    listing_id: int = Column(Integer, ForeignKey("listings.id"), primary_key=True)
    score: float | None = Column(Float)
    subscores: str | None = Column(String)
    created_at: dt.datetime = Column(DateTime, default=dt.datetime.utcnow)
