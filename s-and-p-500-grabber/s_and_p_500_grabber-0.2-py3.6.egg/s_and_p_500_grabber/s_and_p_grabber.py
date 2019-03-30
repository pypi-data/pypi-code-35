# Copyright (c) <2019> <Zachariah Eastman>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bs4 import BeautifulSoup
import requests
from datetime import date
import os

def _output_csv(constituents):
    output_directory = os.path.join('..','output')
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    filename = os.path.join(output_directory,'S&P_Consituents_' + date.today().isoformat() + '.csv')
    with open(filename,'w') as csv:
        for row in constituents:
            for value in row:
                csv.write(str(value).replace(',','').strip() + ',')
            csv.write('\n')



#currently uses wikipedia as the source. There is no other updated, 
#free source for s_and_p listings that I am aware of.
def grab_s_and_p_list():
    constituents = []
    r = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(r.text,'html.parser')
    
    table = soup.find('table',{'id':'constituents'})
    if table:
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if cells:
                company = []
                company.append(cells[0].a.string.strip())
                company.append(str(cells[1].a['href']).strip())
                company.append(cells[7].string.strip())
                constituents.append(company)
        
    return constituents
    


if __name__ == '__main__':
    constituents = grab_s_and_p_list()
    #print(constituents)
    _output_csv(constituents)