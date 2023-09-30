_BASE_URL_SEC_API = "https://data.sec.gov"
_BASE_URL_XBRL = f"{_BASE_URL_SEC_API}/api/xbrl"

# SEC API endpoints as documented here:
# https://www.sec.gov/edgar/sec-api-documentation
BASE_URL_SUBMISSIONS = f"{_BASE_URL_SEC_API}/submissions"
BASE_URL_XBRL_COMPANY_CONCEPTS = f"{_BASE_URL_XBRL}/companyconcept"
BASE_URL_XBRL_COMPANY_FACTS = f"{_BASE_URL_XBRL}/companyfacts"
BASE_URL_XBRL_FRAMES = f"{_BASE_URL_XBRL}/frames"

MAX_REQUESTS_PER_SECOND = 10
MAX_RETRIES = 3
BACKOFF_FACTOR = 1 / MAX_REQUESTS_PER_SECOND
