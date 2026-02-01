import os

DOPT_LIST_URL = os.getenv(
    "DOPT_LIST_URL",
    "https://iascivillist.dopt.gov.in/Home/ViewList",
)

USER_AGENT = os.getenv(
    "CRAWLER_USER_AGENT",
    "ias-directory-crawler/1.0 (+contact@example.com)",
)
REQUEST_TIMEOUT = int(os.getenv("CRAWLER_REQUEST_TIMEOUT", "30"))
RETRIES = int(os.getenv("CRAWLER_RETRIES", "3"))

STATE_SOURCE_URLS = [
    value.strip()
    for value in os.getenv("STATE_SOURCE_URLS", "").split(",")
    if value.strip()
]

DOPT_PDF_URLS = [
    value.strip()
    for value in os.getenv("DOPT_PDF_URLS", "").split(",")
    if value.strip()
]
