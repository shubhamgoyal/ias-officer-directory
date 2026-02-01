import os

DOPT_LIST_URL = "https://iascivillist.dopt.gov.in/Home/ViewList"

USER_AGENT = os.getenv(
    "CRAWLER_USER_AGENT",
    "ias-directory-crawler/1.0 (+contact@example.com)",
)
REQUEST_TIMEOUT = int(os.getenv("CRAWLER_REQUEST_TIMEOUT", "30"))
RETRIES = int(os.getenv("CRAWLER_RETRIES", "3"))
