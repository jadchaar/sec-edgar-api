"""Unofficial SEC EDGAR API wrapper."""
from calendar import different_locale
from typing import Union
from zoneinfo import available_timezones

from ._BaseClient import BaseClient
from .EdgarApi import EdgarApi
from ._UserAgent import (
    BASE_USER_AGENT
)
from ._types import JSONType
from ._utils import merge_submission_dicts, validate_cik

from .termination.usGaap.IncomeStatement.TotalRevenue import TotalRevenue

import json
import pandas as pd
from datetime import datetime
from dateutil import relativedelta


class EdgarClient():
    """An :class:`EdgarClient` object."""

  

    def get_filling(cik: str, *, handle_pagination: bool = True) -> JSONType:
        """Random test.

        :param cik: CIK to obtain submissions for.
        :param handle_pagination: whether to automatically handle API pagination,
            defaults to True. By default, 1000 submissions are included and the
            response specified the next set of filenames to request to get the next
            batch of submissions (each page contains 1000 submissions). If this is
            set to True, requests to the paginated resources will be completed
            automatically and the results will be concatenated to the recent filings key.
            If a raw response is preferred for manual pagination handling, set this
            value to false.
        :return: JSON response from the data.sec.gov/submissions/ API endpoint
            for the specified CIK.
        """

        edgar = EdgarApi(user_agent=BASE_USER_AGENT)

        #get all the facts that we find for this company
        secGovFacts = edgar.get_company_facts(cik=cik)["facts"]["us-gaap"].keys()

        #overall data save array
        dataBlobArray = []

        #seach if we find the saved termination
        for secGovFact in secGovFacts:
            # for TotalRevenue
            for totalRevenueFact in TotalRevenue:
                if totalRevenueFact == secGovFact:
                    # find termination so get data
                    respones = edgar.get_company_concept(cik=cik, taxonomy="us-gaap", tag=totalRevenueFact)['units']["USD"]
                    #for every dataframe that we have
                    for factDataFrame in respones:

                        # make sure that we always target the correct data frame
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
                            dataBlobArray.append([
                                targetYear, #fy key is incorrect in dates before 2019
                                startDate,
                                endDate,
                                factDataFrame["fp"], #FY = full year & QX
                                'Income',
                                'TotalRevenue',
                                factDataFrame["val"],
                                factDataFrame["form"],
                                diff
                            ])

        # drop duplicates
        # clean data = make sure if there are doubles -> take one (this will have a small diff)
        dataBlob = pd.DataFrame(dataBlobArray, columns=['year', 'start', 'end', 'type', 'statement', 'tag', 'value', 'form', 'diff']).drop_duplicates()

        ## get all the years
        allYears = dataBlob["year"].drop_duplicates()
        allYearsArray = allYears.to_numpy()

        ## get all the time frames and make key to create dataframe
        allDataFrameKeys = []

        dataFrames = {}
        for year in allYearsArray:
            availableFrames = dataBlob.loc[dataBlob['year'] == year]['type'].drop_duplicates()
            for frame in availableFrames:
                key = str(year) + '_' + frame
                allDataFrameKeys.append(key)

                dataRow = dataBlob.loc[(dataBlob['year'] == year) & (dataBlob['type'] == frame)]

                dataFrames[key] = {
                    'Income': pd.DataFrame({
                        'tag': [dataRow['tag'].iloc[0]],
                        'value': [int(dataRow['value'].iloc[0])],
                        'year': [dataRow['year'].iloc[0]],
                        'frame': [dataRow['type'].iloc[0]],
                    }),
                    'Balance': pd.DataFrame({
                        'tag': [dataRow['tag'].iloc[0]],
                        'value': [int(dataRow['value'].iloc[0])],
                        'year': [dataRow['year'].iloc[0]],
                        'frame': [dataRow['type'].iloc[0]],
                    }),
                    'Cash': pd.DataFrame({
                        'tag': [dataRow['tag'].iloc[0]],
                        'value': [int(dataRow['value'].iloc[0])],
                        'year': [dataRow['year'].iloc[0]],
                        'frame': [dataRow['type'].iloc[0]],
                    })
                }
                



        ## create data frame and push in data for the data frame


        #print(dataBlob.to_string())
        #print(allYearsArray)
        print(allDataFrameKeys)
        #print([availableFrames[0]])

        #for dataFrameKey in allDataFrameKeys:
        #    print("*******************************")
        #    print("**********"+dataFrameKey+"**************")
        #    print("*******************************")
        #    print("\n")
        #    print(f"---- Income:")
        #    print(dataFrames[dataFrameKey]['Income'])
        #    print("\n")
        #    print(f"---- Balance:")
        #    print(dataFrames[dataFrameKey]['Balance'])
        #    print("\n")
        #    print(f"---- Cash:")
        #    print(dataFrames[dataFrameKey]['Cash'])
        #    print("\n")
        #    print("*******************************")






       