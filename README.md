# secEdgarApi -> Forked from sec-edgar-api

<!---
[![Tests](https://github.com/jadchaar/sec-edgar-api/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/jadchaar/sec-edgar-api/actions/workflows/continuous_integration.yml)
[![Documentation Status](https://readthedocs.org/projects/sec-edgar-api/badge/?version=latest)](https://sec-edgar-api.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/jadchaar/sec-edgar-api/branch/main/graph/badge.svg?token=0WLWU3SZKE)](https://codecov.io/gh/jadchaar/sec-edgar-api)
[![PyPI Version](https://img.shields.io/pypi/v/sec-edgar-api.svg)](https://pypi.org/project/sec-edgar-api/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/sec-edgar-api.svg)](https://pypi.org/project/sec-edgar-api/)
[![License](https://img.shields.io/pypi/l/sec-edgar-api.svg)](https://pypi.org/project/sec-edgar-api/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
-->

**secEdgarApi** is an unofficial Python API wrapper for the [SEC EDGAR REST API](https://www.sec.gov/edgar/sec-api-documentation). that will format facts into json file, sorted by submission 

## Features above the feature that [sec-edgar-api](https://github.com/jadchaar/sec-edgar-api) gives:

- giving a formatted json sorted by submission

<!---
## Quick Start

### Installation

not there yet -> but you can install the one before the fork

-->
### Usage

```python
>>> from secEdgarApi import EdgarClient

# Get the fillings **all** submissions for apple
>>> EdgarClient.get_filling(cik="320193")


```


## Contributing

If you encounter a bug or would like to see a new company filing or feature added to **sec-edgar-api**, please [file an issue](https://github.com/jadchaar/sec-edgar-api/issues) or [submit a pull request](https://help.github.com/en/articles/creating-a-pull-request).

### This is still a alpha version
 things that need to happen before we consider a BETA release
- [ ] cover the most used facts
- [ ] detailed way to targeting data
- [ ] cover 75% of all facts names
- [ ] testing frame work

## Documentation

- Good to know that you can use all the functionality that you get from [sec-edgar-api](https://github.com/jadchaar/sec-edgar-api), be we do recommend to use [sec-edgar-api](https://github.com/jadchaar/sec-edgar-api) if you only need this to talk to the API end point of SEC EDGAR
