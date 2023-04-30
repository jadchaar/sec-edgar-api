import string
from array import array

import pandas as pd
from .TotalAssets import TotalAssets, TOTAL_ASSETS
from secEdgarApi.EdgarHelper import EdgarHelper

class BalanceSheetStatement:
    def getBalanceSheetStatement(secGovFacts: array, cik: string):
        BalanceBlobArray = []
        try:
            BalanceBlobArray = EdgarHelper.getBalanceFact(secGovFacts, cik, TotalAssets, BalanceBlobArray, TOTAL_ASSETS)
            BalanceBlobArray = pd.DataFrame(BalanceBlobArray, columns=['year', 'end', 'type', 'statement', 'tag', 'value', 'form', 'filled', 'diff']).drop_duplicates()
        except KeyError:
                print("Balance sheet statement is empty - please log a bug")

        return BalanceBlobArray