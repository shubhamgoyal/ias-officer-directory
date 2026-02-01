from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class OfficerBase(BaseModel):
    id: int
    full_name: str
    batch: Optional[int] = None
    cadre: Optional[str] = None
    current_posting: Optional[str] = None
    education: Optional[str] = None
    source_url: Optional[str] = None
    last_updated: datetime


class PostingOut(BaseModel):
    id: int
    officer_id: int
    organization: Optional[str] = None
    role_title: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool
    source_url: Optional[str] = None
    observed_at: datetime


class OfficerDetail(OfficerBase):
    postings: list[PostingOut] = []
