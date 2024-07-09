# sec-edgar-api

[![Tests](https://github.com/jadchaar/sec-edgar-api/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/jadchaar/sec-edgar-api/actions/workflows/continuous_integration.yml)
[![Documentation Status](https://readthedocs.org/projects/sec-edgar-api/badge/?version=latest)](https://sec-edgar-api.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/jadchaar/sec-edgar-api/branch/main/graph/badge.svg?token=0WLWU3SZKE)](https://codecov.io/gh/jadchaar/sec-edgar-api)
[![PyPI Version](https://img.shields.io/pypi/v/sec-edgar-api.svg)](https://pypi.org/project/sec-edgar-api/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/sec-edgar-api.svg)](https://pypi.org/project/sec-edgar-api/)
[![License](https://img.shields.io/pypi/l/sec-edgar-api.svg)](https://pypi.org/project/sec-edgar-api/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

**sec-edgar-api** is a lightweight, unofficial Python API wrapper for the [SEC EDGAR REST API](https://www.sec.gov/edgar/sec-api-documentation).

## Features

- Full support for [all SEC EDGAR REST API endpoints](#wrapper-functions-and-corresponding-api-endpoints)
- Automatic pagination handling for filing submissions data
- Automatic rate-limiting to 10 requests per second to conform with [SEC fair access rules](https://www.sec.gov/developer)
- Full support for PEP 484-style type hints and the [mypy type checker](https://mypy.readthedocs.io/en/stable/)
- Support for Python 3.6+

## Quick Start

### Installation

Install and update this package using [pip](https://pip.pypa.io/en/stable/getting-started/):

```console
$ pip install -U sec-edgar-api
```

### Usage

```python
>>> from sec_edgar_api import EdgarClient

# Specify user-agent string to pass to SEC to identify
# requests for rate-limiting purposes
>>> edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")

# Get submissions for Apple with the additional paginated files
# appended to the recent filings to prevent the need for extra
# manual pagination handling
>>> edgar.get_submissions(cik="320193")
{
    "cik": "320193",
    "entityType": "operating",
    "sic": "3571",
    "sicDescription": "Electronic Computers",
    "insiderTransactionForOwnerExists": 0,
    "insiderTransactionForIssuerExists": 1,
    "name": "Apple Inc.",
    "tickers": [
        "AAPL"
    ],
    "exchanges": [
        "Nasdaq"
    ],
    ...
    "filings": {
        "recent": {
            "accessionNumber": [...],
            "filingDate": [...],
            "reportDate": [...],
            "acceptanceDateTime": [...],
            "act": [...],
            "form": [...],
            "fileNumber": [...],
            "filmNumber": [...],
            "items": [...],
            "size": [...],
            "isXBRL": [...],
            "isInlineXBRL": [...],
            "primaryDocument": [...],
            "primaryDocDescription": [...]
        },
        # The extra paginated submission data has already been
        # appended to the lists in the above "recent" key entries
        "files": []
    }
}

# Get submissions for Apple without automatic pagination handling,
# which requires manual handling of the paginated files (not recommended)
>>> edgar.get_submissions(cik="320193", handle_pagination=False)
{
    "cik": "320193",
    "entityType": "operating",
    "sic": "3571",
    "sicDescription": "Electronic Computers",
    "insiderTransactionForOwnerExists": 0,
    "insiderTransactionForIssuerExists": 1,
    "name": "Apple Inc.",
    "tickers": [
        "AAPL"
    ],
    "exchanges": [
        "Nasdaq"
    ],
    ...
    "filings": {
        "recent": {
            "accessionNumber": [...],
            "filingDate": [...],
            "reportDate": [...],
            "acceptanceDateTime": [...],
            "act": [...],
            "form": [...],
            "fileNumber": [...],
            "filmNumber": [...],
            "items": [...],
            "size": [...],
            "isXBRL": [...],
            "isInlineXBRL": [...],
            "primaryDocument": [...],
            "primaryDocDescription": [...]
        },
        # Requires manual pagination handling
        "files": [
            {
                "name": "CIK0000320193-submissions-001.json",
                "filingCount": ...,
                "filingFrom": ...,
                "filingTo": ...
            }
        ]
    }
}

# Get company concept for Apple
>>> edgar.get_company_concept(cik="320193", taxonomy="us-gaap", tag="AccountsPayableCurrent")
{
    "cik": 320193,
    "taxonomy": "us-gaap",
    "tag": "AccountsPayableCurrent",
    "label": "Accounts Payable, Current",
    "description": ...,
    "entityName": "Apple Inc.",
    "units": {
        "USD": [...]
    }
}

# Get company facts for Apple
>>> edgar.get_company_facts(cik="320193")
{
    "cik": 320193,
    "entityName": "Apple Inc.",
    "facts": {
        "dei": {
            "EntityCommonStockSharesOutstanding": {
                "label": "Entity Common Stock, Shares Outstanding",
                "description": ...,
                "units": {
                    "shares": [...]
                }
            },
            "EntityPublicFloat": {
                "label": "Entity Public Float",
                "description": ...,
                "units": {
                    "USD": [...]
                }
            }
        },
        "us-gaap": {
            "AccountsPayable": {
                "label": "Accounts Payable (Deprecated 2009-01-31)",
                "description": ...,
                "units": {
                    "USD": [...]
                }
            },
            "AccountsPayableCurrent": {
                "label": "Accounts Payable, Current",
                "description": ...,
                "units": {
                    "USD": [...]
                }
            },
            ...
        }
    }
}

# Get one fact for each reporting entity in specified
# calendar period (Q1 2019)
>>> edgar.get_frames(taxonomy="us-gaap", tag="AccountsPayableCurrent", unit="USD", year="2019", quarter=1)
{
    "taxonomy": "us-gaap",
    "tag": "AccountsPayableCurrent",
    "ccp": "CY2019Q1I",
    "uom": "USD",
    "label": "Accounts Payable, Current",
    "description": ...,
    "pts": 3388,
    "data": [
        {
            "accn": "0001555538-19-000006",
            "cik": 1555538,
            "entityName": "SUNCOKE ENERGY PARTNERS, L.P.",
            "loc": "US-IL",
            "end": "2019-03-31",
            "val": 78300000
        },
        {
            "accn": "0000011199-19-000012",
            "cik": 11199,
            "entityName": "BEMIS CO INC",
            "loc": "US-WI",
            "end": "2019-03-31",
            "val": 465700000
        },
        ...
    ]
}
```

## Wrapper Functions and Corresponding API Endpoints

|                        Wrapper Function                         |          API Route          |                                         Full API URI                                         |
| --------------------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------- |
| `get_submissions(cik)`                                          | `/submissions/`             | `data.sec.gov/submissions/CIK{cik}.json`                                                     |
| `get_company_concept(cik, taxonomy, tag)`                       | `/api/xbrl/companyconcept/` | `data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{taxonomy}/{tag}.json`                        |
| `get_company_facts(cik)`                                        | `/api/xbrl/companyfacts/`   | `data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`                                           |
| `get_frames(taxonomy, tag, unit, year, quarter, instantaneous)` | `/api/xbrl/frames/`         | `data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{unit}/CY{year}{quarter}{instantaneous}.json` |

More details on each endpoint can be found on the official SEC API documentation: [sec.gov/edgar/sec-api-documentation](https://www.sec.gov/edgar/sec-api-documentation).

## Contributing

If you encounter a bug or would like to see a new company filing or feature added to **sec-edgar-api**, please [file an issue](https://github.com/jadchaar/sec-edgar-api/issues) or [submit a pull request](https://help.github.com/en/articles/creating-a-pull-request).

## Documentation

For full documentation, please visit [sec-edgar-api.readthedocs.io](https://sec-edgar-api.readthedocs.io).
