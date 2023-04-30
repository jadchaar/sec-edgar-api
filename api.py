import sys
sys.path.insert(0, './secEdgarApi')
from secEdgarApi import EdgarApi
from secEdgarApi import EdgarClient

#edgar = EdgarApi(user_agent="Robin and some tests from Robin")
#print(edgar.get_submissions(cik="320193"))

print(EdgarClient.get_filling(cik="764065"))