from weakref import finalize

import requests
from pyrate_limiter import Duration, Limiter, RequestRate
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ._constants import BACKOFF_FACTOR, MAX_REQUESTS_PER_SECOND, MAX_RETRIES
from ._types import JSONType
from .EdgarAPIError import EdgarAPIError

# Rate limiter
rate = RequestRate(MAX_REQUESTS_PER_SECOND, Duration.SECOND)
limiter = Limiter(rate)

# Specify max number of request retries
# https://stackoverflow.com/a/35504626/3820660
retries = Retry(
    total=MAX_RETRIES,
    backoff_factor=BACKOFF_FACTOR,
    status_forcelist=[403, 500, 502, 503, 504],
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

    @limiter.ratelimit(delay=True)
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
