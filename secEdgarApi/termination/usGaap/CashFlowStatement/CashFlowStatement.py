import string
from array import array

import pandas as pd
from .OperatingCashFlow import OperatingCashFlow, OPERATING_CASHFLOW
from secEdgarApi.EdgarHelper import EdgarHelper

class CashFlowStatement:
    def getCashStatement(secGovFacts: array, cik: string):
        CashBlobArray = []
        try:
            CashBlobArray = EdgarHelper.getCashFact(secGovFacts, cik, OperatingCashFlow, CashBlobArray, OPERATING_CASHFLOW)
            CashBlobArray = pd.DataFrame(CashBlobArray, columns=['year', 'start', 'end', 'type', 'statement', 'tag', 'value', 'form', 'diff', 'filed']).drop_duplicates()
        except KeyError:
                print("Cash sheet statement is empty - please log a bug")

        return CashBlobArray