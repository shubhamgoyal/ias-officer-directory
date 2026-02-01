from bs4 import BeautifulSoup


def _normalize_header(value: str) -> str:
    return " ".join(value.lower().strip().split())


def parse_table_records(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return []

    header_row = table.find("tr")
    headers = []
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
        records.append(row_map)
    return records
