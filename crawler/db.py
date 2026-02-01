from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, declarative_base, relationship

Base = declarative_base()


class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True)
    full_name = Column(Text, nullable=False)
    batch = Column(Integer)
    cadre = Column(Text)
    current_posting = Column(Text)
    education = Column(Text)
    source_url = Column(Text)
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    postings = relationship("Posting", back_populates="officer")


class Posting(Base):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True)
    officer_id = Column(Integer, ForeignKey("officers.id"), nullable=False)
    organization = Column(Text)
    role_title = Column(Text)
    location = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, nullable=False, default=True)
    source_url = Column(Text)
    observed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    officer = relationship("Officer", back_populates="postings")


class SourceIngest(Base):
    __tablename__ = "source_ingests"

    id = Column(Integer, primary_key=True)
    source_url = Column(Text, nullable=False)
    source_type = Column(String, nullable=False)
    crawled_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    payload_hash = Column(Text)


def get_engine(database_url: str):
    return create_engine(database_url, future=True)


def upsert_officer(session: Session, payload: dict) -> Officer:
    stmt = select(Officer).where(
        Officer.full_name == payload["full_name"],
        Officer.batch == payload.get("batch"),
        Officer.cadre == payload.get("cadre"),
    )
    officer = session.execute(stmt).scalars().first()
    if not officer:
        officer = Officer(**payload)
        session.add(officer)
        session.flush()
        return officer

    officer.current_posting = payload.get("current_posting")
    officer.education = payload.get("education")
    officer.source_url = payload.get("source_url")
    officer.last_updated = payload.get("last_updated", datetime.utcnow())
    return officer


def record_posting(session: Session, officer_id: int, payload: dict) -> None:
    if not payload:
        return

    stmt = select(Posting).where(
        Posting.officer_id == officer_id,
        Posting.is_current.is_(True),
    )
    current = session.execute(stmt).scalars().first()
    same_posting = (
        current
        and current.organization == payload.get("organization")
        and current.role_title == payload.get("role_title")
        and current.location == payload.get("location")
    )
    if same_posting:
        return

    if current:
        current.is_current = False
        current.end_date = current.end_date or datetime.utcnow().date()

    session.add(
        Posting(
            officer_id=officer_id,
            organization=payload.get("organization"),
            role_title=payload.get("role_title"),
            location=payload.get("location"),
            start_date=payload.get("start_date"),
            end_date=payload.get("end_date"),
            is_current=payload.get("is_current", True),
            source_url=payload.get("source_url"),
            observed_at=payload.get("observed_at", datetime.utcnow()),
        )
    )


def record_ingest(session: Session, source_url: str, source_type: str, payload_hash: str | None) -> None:
    session.add(
        SourceIngest(
            source_url=source_url,
            source_type=source_type,
            payload_hash=payload_hash,
            crawled_at=datetime.utcnow(),
        )
    )
