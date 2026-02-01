import hashlib
import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from .config import DOPT_LIST_URL, STATE_SOURCE_URLS
from .db import get_engine, record_ingest, record_posting, upsert_officer
from .fetcher import fetch_url
from .normalize import normalize_officer
from .parser_dopt import parse_dopt_list
from .parser_state import parse_state_list


def crawl_dopt_list(session: Session) -> int:
    html = fetch_url(DOPT_LIST_URL)
    payload_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()
    record_ingest(session, DOPT_LIST_URL, "dopt_list", payload_hash)

    raw_records = parse_dopt_list(html, DOPT_LIST_URL)
    count = 0
    for raw in raw_records:
        normalized = normalize_officer(raw)
        if not normalized["full_name"]:
            continue
        officer = upsert_officer(session, normalized)

        if normalized.get("current_posting"):
            record_posting(
                session,
                officer.id,
                {
                    "organization": normalized.get("current_posting"),
                    "role_title": None,
                    "location": None,
                    "source_url": normalized.get("source_url"),
                    "is_current": True,
                },
            )
        count += 1
    return count


def crawl_state_sources(session: Session, urls: list[str]) -> int:
    count = 0
    for url in urls:
        html = fetch_url(url)
        payload_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()
        record_ingest(session, url, "state_list", payload_hash)
        raw_records = parse_state_list(html, url)
        for raw in raw_records:
            normalized = normalize_officer(raw)
            if not normalized["full_name"]:
                continue
            officer = upsert_officer(session, normalized)
            for posting in normalized.get("postings", []):
                record_posting(
                    session,
                    officer.id,
                    {
                        "organization": posting.get("organization"),
                        "role_title": posting.get("role_title"),
                        "location": posting.get("location"),
                        "start_date": posting.get("start_date"),
                        "end_date": posting.get("end_date"),
                        "is_current": posting.get("is_current", False),
                        "source_url": posting.get("source_url", url),
                    },
                )
            count += 1
    return count


def main() -> None:
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required")

    engine = get_engine(database_url)
    with Session(engine) as session:
        count = crawl_dopt_list(session)
        if STATE_SOURCE_URLS:
            count += crawl_state_sources(session, STATE_SOURCE_URLS)
        session.commit()
    print(f"Ingested {count} officers")


if __name__ == "__main__":
    main()
