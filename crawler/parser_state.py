from parser_table import parse_table_records


def _split_postings(value: str) -> list[str]:
    if not value:
        return []
    for separator in [";", "|", "\n"]:
        if separator in value:
            return [item.strip() for item in value.split(separator) if item.strip()]
    return [value.strip()]


def parse_state_list(html: str, source_url: str) -> list[dict]:
    records: list[dict] = []
    for row_map in parse_table_records(html):
        posting_history_raw = (
            row_map.get("posting history")
            or row_map.get("postings")
            or row_map.get("previous postings")
        )
        postings = [
            {"organization": item, "source_url": source_url, "is_current": False}
            for item in _split_postings(posting_history_raw or "")
        ]

        record = {
            "full_name": row_map.get("name") or row_map.get("officer name") or row_map.get("col_1"),
            "batch": row_map.get("batch") or row_map.get("year"),
            "cadre": row_map.get("cadre") or row_map.get("state"),
            "current_posting": row_map.get("present posting") or row_map.get("current posting"),
            "education": row_map.get("education") or row_map.get("qualification"),
            "source_url": source_url,
            "postings": postings,
        }
        if record["full_name"]:
            records.append(record)
    return records
