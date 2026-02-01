from .parser_table import parse_table_records


def parse_dopt_list(html: str, source_url: str) -> list[dict]:
    records: list[dict] = []
    for row_map in parse_table_records(html):
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
