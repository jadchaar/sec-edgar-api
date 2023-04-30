from secEdgarApi.EdgarApi import EdgarApi
from .CashFlowStatement.CashFlowStatement import CashFlowStatement
from .BalanceSheetStatement.BalanceSheetStatement import BalanceSheetStatement
from .IncomeStatement.IncomeStatement import IncomeStatement

from secEdgarApi._UserAgent import (
    BASE_USER_AGENT
)

class UsGaapHandler:
    
    def getUsGaapFacts(self, cik: str):
        api = EdgarApi(user_agent=BASE_USER_AGENT)
        
        secGovFacts = api.get_company_facts(cik=cik)["facts"]["us-gaap"].keys()
        incomeStatement =  IncomeStatement.getIncomeStatement(secGovFacts, cik)
        balanceSheetStatement =  BalanceSheetStatement.getBalanceSheetStatement(secGovFacts, cik)
        cashFlowStatement =  CashFlowStatement.getCashStatement(secGovFacts, cik)

        ### get all the years 
        # possible errors we take only the years that have incomeStatement - it possible to lose data
        # point is, this is data that is not complete and we probably not need it anyways.
        allYears = incomeStatement["year"].drop_duplicates()
        allYearsArray = allYears.to_numpy()

        ### get all the time frames and make key to create dataframe
        allDataFrameKeys = []

        dataFrames = {}
        for year in allYearsArray:
            availableFrames = incomeStatement.loc[incomeStatement['year'] == year]['type'].drop_duplicates()
            for frame in availableFrames:
                key = str(year) + '_' + frame
                allDataFrameKeys.append(key)

                incomeStatementDataRows = incomeStatement.loc[(incomeStatement['year'] == year) & (incomeStatement['type'] == frame)].drop_duplicates(subset=['tag'])
                balanceSheetStatementDataRows = balanceSheetStatement.loc[(balanceSheetStatement['year'] == year) & (balanceSheetStatement['type'] == frame)]                
                cashFlowStatementDataRows = cashFlowStatement.loc[(cashFlowStatement['year'] == year) & (cashFlowStatement['type'] == frame)]

                #turn into Json
                dataFrames[key] = {
                    'IncomeStatement': self.formatToStatment(incomeStatementDataRows),
                    'BalanceSheetStatement': self.formatToStatment(balanceSheetStatementDataRows),
                    'CashFlowStatement': self.formatToStatment(cashFlowStatementDataRows),
                }
        return dataFrames

    def formatToStatment(self, dataRows):
        # Create an empty dictionary to store the results
        result = {}

        # Get a list of all the unique tags
        unique_tags = dataRows['tag'].unique()

        # Loop through each tag and create the dictionary for that tag
        for tag in unique_tags:
            # Get the rows for the current tag
            tag_rows = dataRows[dataRows['tag'] == tag]

            # Check if there are any rows for this tag
            if not tag_rows.empty:
                # Create the dictionary for this tag
                result[tag] = int(tag_rows['value'].iloc[0]) if len(tag_rows['value'] != 0 ) else "XXX"
            else:
                # If there are no rows for this tag, set the values to "XXX"
                result[tag] = "XXX"
            
        return [result] 