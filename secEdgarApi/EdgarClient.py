"""Unofficial SEC EDGAR API wrapper."""
from ._types import JSONType
from typing import Union

from secEdgarApi.EdgarApi import EdgarApi
from .termination.TerminationHandler import TerminationHandler

from secEdgarApi._UserAgent import (
    BASE_USER_AGENT
)

class EdgarClient():
    """An :class:`EdgarClient` object."""

    def get_filling(cik: str) -> JSONType:
        """
        :param cik: CIK to obtain submissions for.
        :return: JSON response from an sec.gov API endpoint
            for the specified CIK, including everthing we
            can find about this the specified CIK that is in
            the param
        """

        #get all the USGaap facts that we find for this company
        dataFrames = TerminationHandler.get_usGaap(cik=cik)

        return dataFrames
    
    ####
        ## Support for sec-edgar-api https://github.com/jadchaar/sec-edgar-api
    ####
    def get_submissions(cik: str, handle_pagination: bool = True) -> JSONType:
        api = EdgarApi(user_agent=BASE_USER_AGENT)

        return api.get_submissions(cik=cik, handle_pagination=handle_pagination)

    def get_company_concept(cik: str, taxonomy: str, tag: str ) -> JSONType:
        api = EdgarApi(user_agent=BASE_USER_AGENT)

        return api.get_company_concept(cik=cik, taxonomy=taxonomy, tag=tag)

    def get_company_facts(cik: str) -> JSONType:
        api = EdgarApi(user_agent=BASE_USER_AGENT)

        return api.get_company_facts(cik=cik)

    def get_frames(taxonomy: str, tag: str, unit: str, year: str, quarter: Union[int, str, None] = None, instantaneous: bool = True ) -> JSONType:
        api = EdgarApi(user_agent=BASE_USER_AGENT)

        return api.get_frames(taxonomy=taxonomy, tag=tag, unit=unit, year=year, quarter=quarter, instantaneous=instantaneous)
