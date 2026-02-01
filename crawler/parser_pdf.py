import io
import re
from pypdf import PdfReader


def _split_columns(line: str) -> list[str]:
    parts = re.split(r"\s{2,}", line.strip())
    return [part.strip() for part in parts if part.strip()]


def parse_dopt_pdf(pdf_bytes: bytes, source_url: str) -> list[dict]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    records: list[dict] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or len(line) < 6:
                continue
            if line.lower().startswith(("name", "s.no", "sl.no")):
                continue

            columns = _split_columns(line)
            if len(columns) < 3:
                continue

            # Heuristic: name + batch + cadre + optional posting/education
            batch = None
            name = columns[0]
            if len(columns) > 1 and columns[1].isdigit() and len(columns[1]) == 4:
                batch = columns[1]
                cadre = columns[2] if len(columns) > 2 else None
                remainder = columns[3:] if len(columns) > 3 else []
            else:
                cadre = columns[1] if len(columns) > 1 else None
                remainder = columns[2:] if len(columns) > 2 else []

            current_posting = remainder[0] if remainder else None
            education = remainder[1] if len(remainder) > 1 else None

            record = {
                "full_name": name,
                "batch": batch,
                "cadre": cadre,
                "current_posting": current_posting,
                "education": education,
                "source_url": source_url,
                "postings": [],
            }
            if record["full_name"]:
                records.append(record)
    return records
