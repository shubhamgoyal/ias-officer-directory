from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import declarative_base, relationship

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
