import string
from array import array

import pandas as pd
from .TotalRevenue import TotalRevenue, TOTAL_REVENUE
from .NetIncome import NetIncome, NET_INCOME

from secEdgarApi.EdgarHelper import EdgarHelper

class IncomeStatement:
    def getIncomeStatement(secGovFacts: array, cik: string):
        IncomeBlobArray = []
        try:
            IncomeBlobArray = EdgarHelper.getIncomeFact(secGovFacts, cik, TotalRevenue, IncomeBlobArray, NET_INCOME)
            IncomeBlobArray = EdgarHelper.getIncomeFact(secGovFacts, cik, NetIncome, IncomeBlobArray, TOTAL_REVENUE)
        
            IncomeBlobArray = pd.DataFrame(IncomeBlobArray, columns=['year', 'start', 'end', 'type', 'statement', 'tag', 'value', 'form', 'diff', 'filed']).drop_duplicates()
        except KeyError:
                print("Income sheet statement is empty - please log a bug")

        return IncomeBlobArray