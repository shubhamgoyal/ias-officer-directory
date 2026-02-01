from bs4 import BeautifulSoup


def _normalize_header(value: str) -> str:
    return " ".join(value.lower().strip().split())


def parse_dopt_list(html: str, source_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return []

    headers = []
    header_row = table.find("tr")
    if header_row:
        headers = [_normalize_header(th.get_text(" ", strip=True)) for th in header_row.find_all(["th", "td"])]

    records: list[dict] = []
    for row in table.find_all("tr")[1:]:
        cols = [col.get_text(" ", strip=True) for col in row.find_all(["td", "th"])]
        if not cols:
            continue

        row_map = {}
        for idx, value in enumerate(cols):
            key = headers[idx] if idx < len(headers) else f"col_{idx}"
            row_map[key] = value

        record = {
            "full_name": row_map.get("name") or row_map.get("officer name") or row_map.get("col_1"),
            "batch": row_map.get("batch") or row_map.get("year"),
            "cadre": row_map.get("cadre"),
            "current_posting": row_map.get("present posting") or row_map.get("current posting"),
            "education": row_map.get("education") or row_map.get("qualification"),
            "source_url": source_url,
            "postings": [],
        }
        if record["full_name"]:
            records.append(record)

    return records
