from typing import List

from fastapi import Depends, FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import OfficerBase, OfficerDetail, PostingOut

app = FastAPI(title="IAS Officer Directory API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
handler = Mangum(app)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/officers", response_model=List[OfficerBase])
def search_officers(
    name: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    query = text(
        """
        SELECT id, full_name, batch, cadre, current_posting, education, source_url, last_updated
        FROM officers
        WHERE full_name ILIKE :pattern
        ORDER BY similarity(full_name, :name) DESC, full_name
        LIMIT 50
        """
    )
    pattern = f"%{name}%"
    rows = db.execute(query, {"pattern": pattern, "name": name}).mappings().all()
    return [OfficerBase(**row) for row in rows]


@app.get("/officers/{officer_id}", response_model=OfficerDetail)
def get_officer(officer_id: int, db: Session = Depends(get_db)):
    officer_query = text(
        """
        SELECT id, full_name, batch, cadre, current_posting, education, source_url, last_updated
        FROM officers
        WHERE id = :officer_id
        """
    )
    officer_row = db.execute(officer_query, {"officer_id": officer_id}).mappings().first()
    if not officer_row:
        raise HTTPException(status_code=404, detail="Officer not found")

    postings_query = text(
        """
        SELECT id, officer_id, organization, role_title, location, start_date, end_date,
               is_current, source_url, observed_at
        FROM postings
        WHERE officer_id = :officer_id
        ORDER BY COALESCE(start_date, observed_at) DESC
        """
    )
    postings_rows = db.execute(postings_query, {"officer_id": officer_id}).mappings().all()
    postings = [PostingOut(**row) for row in postings_rows]
    return OfficerDetail(**officer_row, postings=postings)
