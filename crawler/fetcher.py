import time
import requests

from config import REQUEST_TIMEOUT, RETRIES, USER_AGENT


def fetch_url(url: str) -> str:
    headers = {"User-Agent": USER_AGENT}
    last_err = None
    for attempt in range(RETRIES):
        try:
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.text
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"Failed to fetch {url}") from last_err
