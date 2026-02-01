from datetime import datetime


def normalize_batch(value: str | None) -> int | None:
    if not value:
        return None
    digits = "".join(ch for ch in value if ch.isdigit())
    return int(digits) if digits else None


def normalize_officer(record: dict) -> dict:
    return {
        "full_name": record.get("full_name", "").strip(),
        "batch": normalize_batch(record.get("batch")),
        "cadre": record.get("cadre"),
        "current_posting": record.get("current_posting"),
        "education": record.get("education"),
        "source_url": record.get("source_url"),
        "last_updated": datetime.utcnow(),
        "postings": record.get("postings", []),
    }
