import string
from array import array

from datetime import datetime
from dateutil import relativedelta
from .EdgarApi import EdgarApi
from ._UserAgent import (
    BASE_USER_AGENT
)

class EdgarHelper():

  def getIncomeFact(secGovFacts: array, cik: string, FactArray: array, blob: array, naming: str):
    edgar = EdgarApi(user_agent=BASE_USER_AGENT)

    #seach if we find the saved termination
    for secGovFact in secGovFacts:
        # for TotalRevenue
        for Fact in FactArray:
            if Fact == secGovFact:
                # find termination so get data
                respones = edgar.get_company_concept(cik=cik, taxonomy="us-gaap", tag=Fact)['units']["USD"]
                #for every dataframe that we have
                for factDataFrame in respones:

                    # make sure that we always target the correct data frame
                    try:
                        startDate = datetime.strptime(factDataFrame["start"], '%Y-%m-%d')
                        endDate = datetime.strptime(factDataFrame["end"], '%Y-%m-%d')
                        diff = relativedelta.relativedelta(endDate, startDate)
                        diffYears = diff.years,
                        diffMonths = diff.months,
                        targetYear = int(datetime.strptime(factDataFrame["end"], '%Y-%m-%d').strftime("%Y"))

                        # if full year data is a year or 11 to 12 months difference
                        # if quarter is 2 to 3 months difference
                        if(
                            #targetYear > 2009 and
                            (factDataFrame["fp"] == "FY" and (diffYears[0] == 1 or diffMonths[0] >= 11) or
                            factDataFrame["fp"] != "FY" and (diffMonths[0] == 2 or diffMonths[0] == 3))
                        ):
                            blob.append([
                                targetYear, #fy key is incorrect in dates before 2019
                                startDate,
                                endDate,
                                factDataFrame["fp"], #FY = full year & QX
                                'Income',
                                naming,
                                factDataFrame["val"],
                                factDataFrame["form"],
                                diff,
                                factDataFrame["filed"],
                            ]) 
                    except KeyError:
                        print("secgov respone structure for income  not correct - please log a bug")
    return blob
  

  def getBalanceFact(secGovFacts: array, cik: string, FactArray: array, blob: array, naming: str):
    edgar = EdgarApi(user_agent=BASE_USER_AGENT)

    #seach if we find the saved termination
    for secGovFact in secGovFacts:
        # for TotalRevenue
        for Fact in FactArray:
            if Fact == secGovFact:
                # find termination so get data
                respones = edgar.get_company_concept(cik=cik, taxonomy="us-gaap", tag=Fact)['units']["USD"]
                #for every dataframe that we have
                for factDataFrame in respones:

                    try:
                        endDate = datetime.strptime(factDataFrame["end"], '%Y-%m-%d')
                        filledDate = datetime.strptime(factDataFrame["filed"], '%Y-%m-%d')
                        diff = relativedelta.relativedelta(filledDate, endDate)

                        targetYear = int(datetime.strptime(factDataFrame["end"], '%Y-%m-%d').strftime("%Y"))
                        filledYear = int(datetime.strptime(factDataFrame["filed"], '%Y-%m-%d').strftime("%Y"))

                        # if the fact is filled in the same year that it is present, we take that one
                        # sometimes there will be a an 10-Q filling in the next year also take that in account
                        # line above can give more then one record, so we check if this filling is with in 1 mouth after end is reported (don't think this is really stable thought)
                        if(
                            targetYear == filledYear or
                            ((factDataFrame["form"] == "10-Q" and filledYear - targetYear == 1) and
                            (diff.months <= 1))
                        ):
                            blob.append([
                                targetYear, #fy key is incorrect in dates before 2019
                                endDate,
                                factDataFrame["fp"], #FY = full year & QX
                                'Balance ',
                                naming,
                                factDataFrame["val"],
                                factDataFrame["form"],
                                filledYear,
                                diff,
                            ])

                    except KeyError:
                        print("secgov respone structure for balance not correct - please log a bug")
                        
    return blob
  
  def getCashFact(secGovFacts: array, cik: string, FactArray: array, blob: array, naming: str):
    edgar = EdgarApi(user_agent=BASE_USER_AGENT)

    #seach if we find the saved termination
    for secGovFact in secGovFacts:
        # for TotalRevenue
        for Fact in FactArray:
            if Fact == secGovFact:
                # find termination so get data
                respones = edgar.get_company_concept(cik=cik, taxonomy="us-gaap", tag=Fact)['units']["USD"]
                #for every dataframe that we have
                for factDataFrame in respones:
                    try:
                        startDate = datetime.strptime(factDataFrame["start"], '%Y-%m-%d')
                        endDate = datetime.strptime(factDataFrame["end"], '%Y-%m-%d')
                        diff = relativedelta.relativedelta(endDate, startDate)
                        diffYears = diff.years,
                        diffMonths = diff.months,
                        targetYear = int(datetime.strptime(factDataFrame["end"], '%Y-%m-%d').strftime("%Y"))

                        # if full year data is a year or 11 to 12 months difference
                        # if quarter is 2 to 3 months difference
                        if(
                            #targetYear > 2009 and
                            (factDataFrame["fp"] == "FY" and (diffYears[0] == 1 or diffMonths[0] >= 11) or
                            factDataFrame["fp"] != "FY" and (diffMonths[0] == 2 or diffMonths[0] == 3))
                        ):
                            blob.append([
                                targetYear, #fy key is incorrect in dates before 2019
                                startDate,
                                endDate,
                                factDataFrame["fp"], #FY = full year & QX
                                'Cash',
                                naming,
                                factDataFrame["val"],
                                factDataFrame["form"],
                                diff,
                                factDataFrame["filed"],
                            ]) 
                    except KeyError:
                        print("secgov respone structure for balance not correct - please log a bug")
                        
    return blob