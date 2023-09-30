from weakref import finalize

import requests
from pyrate_limiter import Duration, Limiter, Rate
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ._constants import BACKOFF_FACTOR, MAX_REQUESTS_PER_SECOND, MAX_RETRIES
from ._types import JSONType
from .EdgarAPIError import EdgarAPIError

# 10 requests per second rate limit set by SEC:
# https://www.sec.gov/os/webmaster-faq#developers
SEC_THROTTLE_LIMIT_RATE = Rate(MAX_REQUESTS_PER_SECOND, Duration.SECOND)

# Wait up to 60 seconds for the rate-limiter bucket to refill.
# If the bucket does NOT refill, an exception will be raised.
limiter = Limiter(
    SEC_THROTTLE_LIMIT_RATE, raise_when_fail=True, max_delay=60_000
).as_decorator()


def limiter_mapping(*args):
    return "sec_edgar_api_rate_limit", 1


# Specify max number of request retries
# https://stackoverflow.com/a/35504626/3820660
retries = Retry(
    total=MAX_RETRIES,
    backoff_factor=BACKOFF_FACTOR,
    status_forcelist=[408, 425, 429, 500, 502, 503, 504],
)


class BaseClient:
    def __init__(self, user_agent: str):
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept-Encoding": "gzip, deflate",
                "Host": "data.sec.gov",
            }
        )
        self._session.mount("http://", HTTPAdapter(max_retries=retries))
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        # Close the session when this object is garbage collected
        # or the program exits.
        # Source: https://stackoverflow.com/a/67312839/3820660
        finalize(self, self._session.close)

    @limiter(limiter_mapping)
    def _rate_limited_get(self, url: str) -> JSONType:
        """Make a rate-limited GET request.

        SEC limits users to a maximum of 10 requests per second.
        Source: https://www.sec.gov/developer
        """
        resp = self._session.get(url)
        try:
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise EdgarAPIError(
                f"An error occurred with the SEC EDGAR API: {e}"
            ) from None
        return resp.json()
