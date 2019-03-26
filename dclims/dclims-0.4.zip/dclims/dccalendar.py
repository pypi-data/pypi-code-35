'''
This is the preliminary work for an API wrapper.  This API wrapper will call the
D.C. LIMS API system, streamlining the calls.

Dependencies: Requests;
API help from DC Council Website:http://lims.dccouncil.us/api/Help


|Signature-------------------------------------------|
|Written for DC Policy Center by Michael Watson; 2017|
|www.DCPolicyCenter.org / DC-Policy-Center.github.io |
|github:M-Watson & MW-DC-Policy-Center               |
|----------------------------------------------------|
'''

#Requests is used for all of the API calls.
import requests, json
from bs4 import BeautifulSoup as bs
def topLevelTest(toPrint):
    print(toPrint)
    return(toPrint)

class get:
#*****************************************************************************#

class calendar:
    page_number = 1
    url = "http://dccouncil.us/events/list/?tribe_paged=%s"%page_number

    re = requests.get(url)

    soup = bs(re.content,"lxml")

    calendar_date = soup.find("div",{'class':'listing-header__subhead'})
    articles = soup.find_all('article')
    ul_list = []
    for article in articles:
        ul_list.append(article.ul)
    print(ul_list)

'''  *****************        APPENDICES   *************************
                    I. Only pulls list 
                    II.
                    III.
                    IV.

*****************        END APPENDICES   *************************'''
