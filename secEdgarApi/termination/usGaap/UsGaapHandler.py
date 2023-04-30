from secEdgarApi.EdgarApi import EdgarApi
from .CashFlowStatement.CashFlowStatement import CashFlowStatement
from .BalanceSheetStatement.BalanceSheetStatement import BalanceSheetStatement
from .IncomeStatement.IncomeStatement import IncomeStatement


from secEdgarApi._UserAgent import (
    BASE_USER_AGENT
)

class UsGaapHandler:
    
    def getUsGaapFacts(cik: str):
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

                incomeStatementDataRows = incomeStatement.loc[(incomeStatement['year'] == year) & (incomeStatement['type'] == frame)]
                balanceSheetStatementDataRows = balanceSheetStatement.loc[(balanceSheetStatement['year'] == year) & (balanceSheetStatement['type'] == frame)]                
                cashFlowStatementDataRows = cashFlowStatement.loc[(cashFlowStatement['year'] == year) & (cashFlowStatement['type'] == frame)]

                #turn into Json
                dataFrames[key] = {
                    'IncomeStatement': {
                        'tag': incomeStatementDataRows['tag'].iloc[0] if len(incomeStatementDataRows['tag'] != 0 ) else "XXX",
                        'value': int(incomeStatementDataRows['value'].iloc[0]) if len(incomeStatementDataRows['tag'] != 0 ) else "XXX",
                        'year': incomeStatementDataRows['year'].iloc[0] if len(incomeStatementDataRows['tag'] != 0 ) else "XXX",
                        'frame': incomeStatementDataRows['type'].iloc[0] if len(incomeStatementDataRows['tag'] != 0 ) else "XXX",
                    },
                    'BalanceSheetStatement': {
                        'tag': balanceSheetStatementDataRows['tag'].iloc[0] if len(balanceSheetStatementDataRows['tag'] != 0 ) else "XXX",
                        'value': int(balanceSheetStatementDataRows['value'].iloc[0]) if len(balanceSheetStatementDataRows['value'] != 0 ) else "XXX",
                        'year': balanceSheetStatementDataRows['year'].iloc[0] if len(balanceSheetStatementDataRows['year'] != 0 ) else "XXX",
                        'frame': balanceSheetStatementDataRows['type'].iloc[0] if len(balanceSheetStatementDataRows['type'] != 0 ) else "XXX",
                    },
                    'CashFlowStatement': {
                        'tag': cashFlowStatementDataRows['tag'].iloc[0] if len(cashFlowStatementDataRows['tag'] != 0 ) else "XXX",
                        'value': int(cashFlowStatementDataRows['value'].iloc[0]) if len(cashFlowStatementDataRows['tag'] != 0 ) else "XXX",
                        'year': cashFlowStatementDataRows['year'].iloc[0] if len(cashFlowStatementDataRows['tag'] != 0 ) else "XXX",
                        'frame': cashFlowStatementDataRows['type'].iloc[0] if len(cashFlowStatementDataRows['tag'] != 0 ) else "XXX",
                    }
                }
        return dataFrames        