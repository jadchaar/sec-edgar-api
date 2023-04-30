"""Unofficial SEC EDGAR API wrapper."""
from ._types import JSONType

from .termination.usGaap.IncomeStatement.TotalRevenue import TotalRevenue
from .termination.TerminationHandler import TerminationHandler

class EdgarClient():
    """An :class:`EdgarClient` object."""

    def get_filling(cik: str) -> JSONType:
        """Random test.

        :param cik: CIK to obtain submissions for.
        :return: JSON response from an sec.gov API endpoint
            for the specified CIK, including everthing we
            can find about this the specified CIK that is in
            the param
        """

        #get all the USGaap facts that we find for this company
        dataFrames = TerminationHandler.get_usGaap(cik=cik)

        return dataFrames
