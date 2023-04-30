import string
from array import array

import pandas as pd
from .OperatingCashFlow import OperatingCashFlow, FACT_NAME
from secEdgarApi.EdgarHelper import EdgarHelper

class CashFlowStatement:
    def getCashStatement(secGovFacts: array, cik: string):
        CashBlobArray = []
        try:
            CashBlobArray = EdgarHelper.getCashFact(secGovFacts, cik, OperatingCashFlow, CashBlobArray, FACT_NAME)
            CashBlobArray = pd.DataFrame(CashBlobArray, columns=['year', 'start', 'end', 'type', 'statement', 'tag', 'value', 'form', 'diff', 'filed']).drop_duplicates()
        except KeyError:
                print("Cash sheet statement is empty - please log a bug")

        return CashBlobArray