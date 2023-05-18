import string
from array import array

import pandas as pd

from .Cash import Cash, CASH
from .CurrentAssets import CurrentAssets, CURRENT_ASSETS
from .CurrentLiabilties import CurrentLiabilties, CURRENT_LIABILTIES
from .LongTermDebt import LongTermDebt, LONG_TERM_DEBT
from .ShortTermDebt import ShortTermDebt, SHORT_TERM_DEBT
from .TotalAssets import TotalAssets, TOTAL_ASSETS
from .TotalStockholderEquity import TotalStockholderEquity, TOTAL_STOCKHOLDER_EQUITY

from secEdgarApi.EdgarHelper import EdgarHelper

class BalanceSheetStatement:
    def getBalanceSheetStatement(secGovFacts: array, cik: string):
        BalanceBlobArray = []
        try:
            BalanceBlobArray = EdgarHelper.getBalanceFact(secGovFacts, cik, CurrentAssets, BalanceBlobArray, CURRENT_ASSETS)
            BalanceBlobArray = EdgarHelper.getBalanceFact(secGovFacts, cik, CurrentLiabilties, BalanceBlobArray, CURRENT_LIABILTIES)
            BalanceBlobArray = EdgarHelper.getBalanceFact(secGovFacts, cik, LongTermDebt, BalanceBlobArray, LONG_TERM_DEBT)
            BalanceBlobArray = EdgarHelper.getBalanceFact(secGovFacts, cik, ShortTermDebt, BalanceBlobArray, SHORT_TERM_DEBT)
            BalanceBlobArray = EdgarHelper.getBalanceFact(secGovFacts, cik, TotalAssets, BalanceBlobArray, TOTAL_ASSETS)
            BalanceBlobArray = EdgarHelper.getBalanceFact(secGovFacts, cik, TotalStockholderEquity, BalanceBlobArray, TOTAL_STOCKHOLDER_EQUITY)

            BalanceBlobArray = pd.DataFrame(BalanceBlobArray, columns=['year', 'end', 'type', 'statement', 'tag', 'value', 'form', 'filled', 'diff']).drop_duplicates()
        except KeyError:
                print("Balance sheet statement is empty - please log a bug")

        return BalanceBlobArray