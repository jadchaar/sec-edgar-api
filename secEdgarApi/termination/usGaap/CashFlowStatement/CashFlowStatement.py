import string
from array import array

import pandas as pd
from .FinancingActivitiesCashFlow import FinancingActivitiesCashFlow, FINANCING_ACTIVITIES_CASHFLOW
from .InvestingActivitiesCashFlow import InvestingActivitiesCashFlow, INVESTING_ACTIVITIES_CASHFLOW
from .OperatingCashFlow import OperatingCashFlow, OPERATING_CASHFLOW
from .RepurchaseOfStock import RepurchaseOfStock, REPURCHASE_OF_STOCK

from secEdgarApi.EdgarHelper import EdgarHelper

class CashFlowStatement:
    def getCashStatement(secGovFacts: array, cik: string):
        CashBlobArray = []
        try:
            CashBlobArray = EdgarHelper.getCashFact(secGovFacts, cik, FinancingActivitiesCashFlow, CashBlobArray, FINANCING_ACTIVITIES_CASHFLOW)
            CashBlobArray = EdgarHelper.getCashFact(secGovFacts, cik, InvestingActivitiesCashFlow, CashBlobArray, INVESTING_ACTIVITIES_CASHFLOW)
            CashBlobArray = EdgarHelper.getCashFact(secGovFacts, cik, OperatingCashFlow, CashBlobArray, OPERATING_CASHFLOW)
            CashBlobArray = EdgarHelper.getCashFact(secGovFacts, cik, RepurchaseOfStock, CashBlobArray, REPURCHASE_OF_STOCK)

            CashBlobArray = pd.DataFrame(CashBlobArray, columns=['year', 'start', 'end', 'type', 'statement', 'tag', 'value', 'form', 'diff', 'filed']).drop_duplicates()
        except KeyError:
                print("Cash sheet statement is empty - please log a bug")

        return CashBlobArray