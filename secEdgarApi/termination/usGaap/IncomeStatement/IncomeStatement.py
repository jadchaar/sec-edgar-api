import string
from array import array

import pandas as pd
from .TotalRevenue import TotalRevenue, TOTAL_REVENUE
from .NetIncome import NetIncome, NET_INCOME
from .OperatingExpenses import OperatingExpenses, OPERATING_EXPENSES
from .GrossProfit import GrossProfit, GROSS_PROFIT
from .CostOfRevenue import CostOfRevenue, COST_OF_REVENUE

from secEdgarApi.EdgarHelper import EdgarHelper

class IncomeStatement:
    def getIncomeStatement(secGovFacts: array, cik: string):
        IncomeBlobArray = []
        try:
            IncomeBlobArray = EdgarHelper.getIncomeFact(secGovFacts, cik, NetIncome, IncomeBlobArray, NET_INCOME)
            IncomeBlobArray = EdgarHelper.getIncomeFact(secGovFacts, cik, TotalRevenue, IncomeBlobArray, TOTAL_REVENUE)
            IncomeBlobArray = EdgarHelper.getIncomeFact(secGovFacts, cik, OperatingExpenses, IncomeBlobArray, OPERATING_EXPENSES)
            IncomeBlobArray = EdgarHelper.getIncomeFact(secGovFacts, cik, GrossProfit, IncomeBlobArray, GROSS_PROFIT)
            IncomeBlobArray = EdgarHelper.getIncomeFact(secGovFacts, cik, CostOfRevenue, IncomeBlobArray, COST_OF_REVENUE)
        
            IncomeBlobArray = pd.DataFrame(IncomeBlobArray, columns=['year', 'start', 'end', 'type', 'statement', 'tag', 'value', 'form', 'diff', 'filed']).drop_duplicates()
        except KeyError:
                print("Income sheet statement is empty - please log a bug")

        return IncomeBlobArray