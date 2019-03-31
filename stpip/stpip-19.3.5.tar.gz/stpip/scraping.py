'''
---stpip---
This file contains the code that go scrap the website

@R. Thomas
@Santiago, Chile
@2019
'''


##standard library
import requests

#local import
from bs4 import BeautifulSoup

def scrap(package):
    '''
    This function go scrap pepy.tech

    Parameters
    -----------
    package
            str, name of the pypi package

    Returns
    -------
    total
            int, total number of downloads, all time
    month
            int, number of downloads in last month
    day
            int, number of downloads in the last week
    last_date
            str, date of the last day the stat was computed
    last_date_down, 
            int, number of downloads during last_date day
    '''

    url = 'https://pepy.tech/project/' + package

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    name_box = soup.find_all('table', attrs={'class': 'table'})

    a = [my_tag.text for my_tag in soup.find_all('table', attrs={'class':'table'})]
    counts = a[0].split()
    
    if counts[0] == 'Total':
        total = int(counts[2].replace(',', ''))
        month = int(counts[8].replace(',', ''))
        day = int(counts[14].replace(',', ''))

        last_days = a[1].split()
        last_date_down = last_days[3]
        last_date = last_days[2]

    else:
        total = 0
        month = 0
        day = 0

        last_days = 0
        last_date_down = '0 0 0'
        last_date = 0

    return total, month, day, last_date, last_date_down



