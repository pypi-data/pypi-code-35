#    linkymeter : Get Linky smart meter data from Enedis webserver
#
#    Copyright (C) 2019  ermitz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>

"""
    Retrieves energy consumption data from Enedis account.
"""

import base64
import requests
import html
import sys
import os
import logging
import json
from . import datashaper

logger = logging.getLogger()


LOGIN_URL = 'https://espace-client-connexion.enedis.fr/auth/UI/Login'

DATA_URL = 'https://espace-client-particuliers.enedis.fr/group/espace-particuliers/suivi-de-consommation'


class LinkyWebLoginException(Exception):
    """Thrown if an error occured while connecting to webservice."""
    pass


class LinkyWebSessionException(Exception):
    """Thrown when the webservice threw an exception."""
    pass



def login(username, password, timeout=60.0):
    """
        Open a user session into the Linky web service.
    """
    session = requests.Session()

    payload = {
            'IDToken1': username,
            'IDToken2': password,
            'encoded': 'true',
            'gx_charset': 'UTF-8',
            'SunQueryParamsString': base64.b64encode(b'realm=particuliers')
    }

    session.headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept-Language': 'fr,fr-FR;q=0.8,en;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }

    #res = session.get(LOGIN_URL, allow_redirects=False, timeout=timeout)
    #if res.status_code not in [200]:
    #    print (res.text)
    #    print (res.headers)
    #    raise LinkyWebLoginException("Login service not accessible (err:%d)." % (res.status_code))

    res = session.post(LOGIN_URL, data=payload, allow_redirects=False, timeout=timeout)
    print (res.text)
    print (res.headers)
    #if res.status_code not in [200]:
    #    raise LinkyWebLoginException("Login service not accessible (err:%d)." % (res.status_code))

    # Sessions are identified using a unique token called SSOTokenID. 
    # The entire value of the iPlanetDirectoryPro cookie is the SSOTokenID
    session_cookie = res.cookies.get('iPlanetDirectoryPro')

    if not 'iPlanetDirectoryPro' in session.cookies:
        raise LinkyWebLoginException("Login failed. Check your credentials.")

    return LinkyWebSession(session)


def dtostr(date):
    """Format date accordingly to linky API"""
    return date.strftime("%d/%m/%Y")


class LinkyWebSession(object):
    def __init__(self,session):
        self.session = session

    def _dump_data(self,res,data_dir,filename):
        with open(os.path.join(data_dir,filename), 'w+') as outfile:
            json.dump(res, outfile)


    def get_hourly_consumption(self, start_date, end_date,data_dir=None):
        """Retreives hourly energy consumption data."""
        data = self._get_consumption('urlCdcHeure', dtostr(start_date), dtostr(end_date))
        if data_dir:
            self._dump_data(data,data_dir,"json_hours_values.txt")
        return datashaper.LinkyWebHourlyDataShaper(data).data()



    def get_daily_consumption(self, start_date, end_date,data_dir=None):
        """Retreives daily energy consumption data."""
        data = self._get_consumption('urlCdcJour', dtostr(start_date), dtostr(end_date))
        if data_dir:
            self._dump_data(data,data_dir,"json_days_values.txt")
        return datashaper.LinkyWebDailyDataShaper(data).data()


    def get_monthly_consumption(self, start_date, end_date, data_dir=None):
        """Retreives monthly energy consumption data."""
        data = self._get_consumption('urlCdcMois', dtostr(start_date), dtostr(end_date))
        if data_dir:
            self._dump_data(data,data_dir,"json_month_values.txt")
        return datashaper.LinkyWebMonthlyDataShaper(data).data()


    def get_yearly_consumption(self, data_dir=None):
        """Retreives yearly energy consumption data."""
        data = self._get_consumption('urlCdcAn')
        if data_dir:
            self._dump_data(data,data_dir,"json_years_values.txt")
        return datashaper.LinkyWebYearlyDataShaper(data).data()


    def _get_consumption(self, resource_id, start_date=None, end_date=None):

        #TODO:requests.exceptions.RequestException

        # First, get the page
        res = self.session.get(DATA_URL, allow_redirects=False,timeout=60.0)
        if res.status_code not in [200,302]:
            raise LinkyWebSessionException("Data query request page is unreachable. (err:%d)" % (res.status_code))

        req_part = 'lincspartdisplaycdc_WAR_lincspartcdcportlet'

        datas = {
            '_' + req_part + '_dateDebut': start_date,
            '_' + req_part + '_dateFin': end_date
        }

        params = {
            'p_p_cacheability': 'cacheLevelPage',
            'p_p_col_id': 'column-1',
            'p_p_col_pos': 1,
            'p_p_col_count': 3,
            'p_p_id': req_part,
            'p_p_lifecycle': 2,
            'p_p_mode': 'view',
            'p_p_resource_id': resource_id,
            'p_p_state': 'normal'
        }

        # Post data query request
        res = self.session.post(DATA_URL, allow_redirects=False, data=datas, params=params, timeout=60.0)

        if not res:
            raise LinkyWebSessionException("Data query request failed, no data received.")

        if res.status_code != 200:
            raise LinkyWebSessionException("Data query request failed, error <%d>." % (res.status_code))

        try:
            res_json = json.loads(res.text)
        except:
            logger.info ("%d : %s" % (res.status_code, res.text))
            raise LinkyWebSessionException('Received invalid data')

        if res_json['etat'] and res_json['etat']['valeur'] == 'erreur':
            logger.info ("%d : %s" % (res.status_code, res.text))
            raise LinkyWebSessionException(html.unescape(res_json['etat']))

        return res_json

    def close(self):
        self.session.close()

__all__ = ['login', 'LinkyWebLoginException', 'LinkyWebSessionException']
