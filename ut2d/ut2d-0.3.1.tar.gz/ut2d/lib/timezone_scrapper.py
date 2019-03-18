import re
from typing import Optional

import requests
from bs4 import BeautifulSoup as BS

from .message import throw_msg

SEARCH_ENGINES = {
    'google': 'https://www.google.com',
    'bing': 'https://www.bing.com',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

TZ_INFO = {
    'AST': 'UTC-4',
    'EDT': 'UTC-4',
    'EST': 'UTC-5',
    'CDT': 'UTC-5',
    'CST': 'UTC-6',
    'MDT': 'UTC-6',
    'MST': 'UTC-7',
    'PDT': 'UTC-7',
    'PST': 'UTC-8',
    'AKDT': 'UTC-8',
    'AKST': 'UTC-9',
    'HADT': 'UTC-9',
    'SDT': 'UTC-10',
    'HST': 'UTC-10',
    'HAST': 'UTC-10',
    'SST': 'UTC-11',
    'CHST': 'UTC+10',
}


class TimezoneScrapper:
    """
    Scrap the city's timezone from search engines, then conver to UTC format.
    
    Some popular search engines like Google or Bing supports getting the
    time and timezone info of a given place with one simple query "xx time".

    Pre-selected search engines will be tested for availability, and then
    scrapped to collect the timezone information.
    """

    def __init__(self, city: str):
        self.city = city
        self.search_engines = []
        self.timezone = None
        
        self._find_search_engines()
        self._find_timezone()
    
    def _locate_tz(self, tz_text: str) -> str:
        """locate timezone in raw text"""
        return re.search('\(.*\)', tz_text).group()[1:-1]

    def _to_utc_fmt(self, timezone: str) -> Optional[str]:
        """
        GMT-4 -> UTC-4
        UTC-4 -> UTC-4
        AST   -> UTC-4
        """
        if timezone[:3].upper() in ['UTC', 'GMT']:
            if len(timezone) == 3:
                return 'UTC+0'
            else:
                return timezone
        else:
            time_in_utc = TZ_INFO.get(timezone.upper())
            if time_in_utc is None:
                return None
            else:
                return time_in_utc

    def _find_search_engines(self):
        for se, se_url in SEARCH_ENGINES.items():
            try:
                r = requests.get(se_url, headers=HEADERS)
                if r.status_code == 200:
                    self.search_engines.append(se)
            except:
                pass

        if not self.search_engines:
            throw_msg(0, 'search_conn_failed', True)
    
    def _find_timezone(self):
        for se in self.search_engines:
            if (se == 'google') and (not self.timezone):
                self._scrap_google()
            if (se == 'bing') and (not self.timezone):
                self._scrap_bing()

    def _scrap_google(self):
        city_fmt = self.city.lstrip().rstrip().replace(' ', '+')

        base_url = 'https://www.google.com/search?q='
        full_url = base_url + city_fmt + '+' + 'time'

        try:
            r = requests.get(full_url, headers=HEADERS)
            soup = BS(r.content, 'html.parser')
            tz_text = soup.select('span[class="KfQeJ"]')[1].text
            
            tz = self._locate_tz(tz_text)
            self.timezone = self._to_utc_fmt(tz)
        except:
            pass

    def _scrap_bing(self):
        city_fmt = self.city.lstrip().rstrip().replace(' ', '%20')

        base_url = 'https://www.bing.com/search?q='
        full_url = base_url + city_fmt + '%20' + 'time'

        try:
            r = requests.get(full_url, headers=HEADERS)
            soup = BS(r.content, 'html.parser')
            tz_text = soup.select_one('div[class="baselClock"] div[class="b_focusLabel"]').text

            tz_fmt = self._locate_tz(tz_text)
            self.timezone = self._to_utc_fmt(tz_fmt)
        except:
            pass
