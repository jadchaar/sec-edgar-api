"""Unofficial SEC EDGAR API wrapper."""
from typing import Union

from ._BaseClient import BaseClient
from ._constants import (
    BASE_URL_SUBMISSIONS,
    BASE_URL_XBRL_COMPANY_CONCEPTS,
    BASE_URL_XBRL_COMPANY_FACTS,
    BASE_URL_XBRL_FRAMES,
)
from ._types import JSONType
from ._utils import merge_submission_dicts, validate_cik


class EdgarClient(BaseClient):
    """An :class:`EdgarClient` object."""

    def __init__(self, user_agent: str):
        """Constructor for the :class:`EdgarClient` class."""
        if not user_agent:
            raise ValueError(
                "Please enter a valid user-agent string of the form "
                "'<Sample Company Name> <Sample Company Email>'. "
                "This is required by the SEC to identify your requests "
                "for rate-limiting purposes."
            )
        super().__init__(user_agent)

    def get_submissions(self, cik: str, *, handle_pagination: bool = True) -> JSONType:
        """Get submissions for a specified CIK. Requests data from the
        data.sec.gov/submissions API endpoint. Full API documentation:
        https://www.sec.gov/edgar/sec-api-documentation.

        :param cik: CIK to obtain submissions for.
        :param handle_pagination: whether to automatically handle API pagination,
            defaults to True. By default, 1000 submissions are included and the
            response specified the next set of filenames to request to get the next
            batch of submissions (each page contains 1000 submissions). If this is
            set to True, requests to the paginated resources will be completed
            automatically and the results will be concatenated to the recent filings key.
            If a raw response is preferred for manual pagination handling, set this
            value to false.
        :return: JSON response from the data.sec.gov/submissions/ API endpoint
            for the specified CIK.
        """
        cik = validate_cik(cik)
        api_endpoint = f"{BASE_URL_SUBMISSIONS}/CIK{cik}.json"
        submissions = self._rate_limited_get(api_endpoint)

        filings = submissions["filings"]
        paginated_submissions = filings["files"]

        # Handle pagination for a large number of requests
        if handle_pagination and paginated_submissions:
            to_merge = [filings["recent"]]
            for submission in paginated_submissions:
                filename = submission["name"]
                api_endpoint = f"{BASE_URL_SUBMISSIONS}/{filename}"
                resp = self._rate_limited_get(api_endpoint)
                to_merge.append(resp)

            # Merge all paginated submissions from files key into recent
            # and clear files list.
            filings["recent"] = merge_submission_dicts(to_merge)
            filings["files"] = []

        return submissions

    def get_company_concept(
        self,
        cik: str,
        taxonomy: str,
        tag: str,
    ) -> JSONType:
        """Get company concepts for a specified CIK. Requests data from the
        data.sec.gov/api/xbrl/companyconcept/ API endpoint. Returns all
        the XBRL disclosures for a single company (CIK) and concept (taxonomy and
        tag), with a separate array of facts for each unit of measure that the
        company has chosen to disclose (e.g. net profits reported in U.S. dollars
        and in Canadian dollars). Full API documentation:
        https://www.sec.gov/edgar/sec-api-documentation.

        :param cik: CIK to obtain company concepts for.
        :param taxonomy: reporting taxonomy (e.g. us-gaap, ifrs-full, dei, srt).
            More info: https://www.sec.gov/info/edgar/edgartaxonomies.shtml.
        :param tag: reporting tag (e.g. AccountsPayableCurrent).
        :return: JSON response from the data.sec.gov/api/xbrl/companyconcept/
            API endpoint for the specified CIK.
        """
        cik = validate_cik(cik)
        api_endpoint = (
            f"{BASE_URL_XBRL_COMPANY_CONCEPTS}/CIK{cik}/{taxonomy}/{tag}.json"
        )
        return self._rate_limited_get(api_endpoint)

    def get_company_facts(self, cik: str) -> JSONType:
        """Get all company concepts for a specified CIK. Requests data from the
        data.sec.gov/api/xbrl/companyfacts/ API endpoint. Full API documentation:
        https://www.sec.gov/edgar/sec-api-documentation.

        :param cik: CIK to obtain company concepts for.
        :return: JSON response from the data.sec.gov/api/xbrl/companyfacts/
            API endpoint for the specified CIK.
        """
        cik = validate_cik(cik)
        api_endpoint = f"{BASE_URL_XBRL_COMPANY_FACTS}/CIK{cik}.json"
        return self._rate_limited_get(api_endpoint)

    def get_frames(
        self,
        taxonomy: str,
        tag: str,
        unit: str,
        year: str,
        quarter: Union[int, str, None] = None,
        instantaneous: bool = True,
    ) -> JSONType:
        """Get all aggregated company facts for a specified taxonomy and tag in the specified
        calendar period. Requests data from the data.sec.gov/api/xbrl/frames/ API endpoint.
        Supports for annual, quarterly and instantaneous data. Example:
        us-gaap / AccountsPayableCurrent / USD / CY2019Q1I.
        Full API documentation: https://www.sec.gov/edgar/sec-api-documentation.

        :param taxonomy: reporting taxonomy (e.g. us-gaap, ifrs-full, dei, srt).
            More info: https://www.sec.gov/info/edgar/edgartaxonomies.shtml.
        :param tag: reporting tag (e.g. AccountsPayableCurrent).
        :param unit: unit of measure specified in the XBRL (e.g. USD).
        :param year: calendar period year.
        :param quarter: calendar period quarter, optional. Defaults to whole year.
        :param instantaneous: whether to request instantaneous data, defaults to True.
        :return: JSON response from the data.sec.gov/api/xbrl/frames/ API endpoint.
        """
        _quarter = (
            f"Q{quarter}" if quarter is not None and 1 <= int(quarter) <= 4 else ""
        )
        _instantaneous = "I" if instantaneous else ""
        period = f"CY{year}{_quarter}{_instantaneous}"
        api_endpoint = f"{BASE_URL_XBRL_FRAMES}/{taxonomy}/{tag}/{unit}/{period}.json"
        return self._rate_limited_get(api_endpoint)
