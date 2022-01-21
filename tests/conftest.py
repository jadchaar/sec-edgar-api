import time
from typing import Dict

import pytest

from sec_edgar_api import EdgarClient


def generate_user_agent() -> str:
    curr_time = time.time()
    return f"{curr_time} {curr_time}@gmail.com"


@pytest.fixture(scope="session")
def apple_stock() -> Dict[str, str]:
    return {"cik": "0000320193", "name": "Apple Inc."}


@pytest.fixture(scope="session")
def base_concept_data() -> Dict[str, str]:
    return {
        "taxonomy": "us-gaap",
        "unit": "USD",
        "year": "2019",
        "quarter": "1",
    }


@pytest.fixture(scope="session")
def concept_data_accounts_payable_current(
    base_concept_data: Dict[str, str]
) -> Dict[str, str]:
    return {
        "tag": "AccountsPayableCurrent",
        **base_concept_data,
    }


@pytest.fixture(scope="session")
def concept_data_gross_profit(base_concept_data: Dict[str, str]) -> Dict[str, str]:
    return {
        "tag": "GrossProfit",
        **base_concept_data,
    }


@pytest.fixture(scope="session")
def edgar_client() -> EdgarClient:
    return EdgarClient(user_agent=generate_user_agent())
