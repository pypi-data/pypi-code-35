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
Parse energy consumption JSON files from Enedis (ERDF) consumption data
collected via their  website (API).
"""


import datetime
from dateutil.relativedelta import relativedelta

import logging
logger = logging.getLogger()

class LinkyWebDataShaper(object):
    '''
       Parse json data returned by Enedis API, and convert them
       to our format : a list of {'time':t,'conso':c} points where
       t is the time expressed in datetime type, and c is the consumption
       given at that time.

       json data contain a list of consumptions value ordered by time, but
       does not contain informations about the time unit, which depends
       on the query done.

       time_period_unit and time_period_values properties are used by the data() 
       parsing function to determine resp. the unit name and value of time unit.

    '''
    def __init__(self,data):
        self._data = data


    def data(self):
        # Extract start date and parse it
        start_date_queried_str = self._data['graphe']['periode']['dateDebut']
        start_date_queried = datetime.datetime.strptime(start_date_queried_str, "%d/%m/%Y").date()

        # Calculate final start date using the "offset" attribute returned by the API
        kwargs = {}
        kwargs[self.time_period_unit] = self._data['graphe']['decalage'] * self.time_period_value
        start_date = start_date_queried - relativedelta(**kwargs)
        logger.info("Start Date:%s" % start_date)

        logger.debug("delta unit:%s" % self.time_period_unit)

        for i,datapoint in enumerate(self._data['graphe']['data']):
            ordre = datapoint['ordre']  #TODO?: ordered by ordre
            value = datapoint['valeur'] * self.time_period_value
            logger.debug("%d %d %f" % (i,ordre,value))
            if value >= 0:
                kwargs[self.time_period_unit] = i * self.time_period_value
                t = start_date + relativedelta(**kwargs)
                yield {"time": t, "conso": value}

        
    @property
    def time_period_unit(self):
        return self._time_period_unit

    @property
    def time_period_value(self):
        return self._time_period_value



class LinkyWebHourlyDataShaper(LinkyWebDataShaper):
    """Parse JSON data containing half-hours power measure"""
    def __init__(self,data):
        self._time_period_unit = 'hours'
        self._time_period_value = 0.5
        super(LinkyWebHourlyDataShaper,self).__init__(data)



class LinkyWebDailyDataShaper(LinkyWebDataShaper):
    """Parse JSON data containing daily consumption"""
    def __init__(self,data):
        self._time_period_unit = 'days'
        self._time_period_value = 1
        super(LinkyWebDailyDataShaper,self).__init__(data)



class LinkyWebMonthlyDataShaper(LinkyWebDataShaper):
    """Parse JSON data containing monthly consumption"""
    def __init__(self,data):
        self._time_period_unit = 'months'
        self._time_period_value = 1
        super(LinkyWebMonthlyDataShaper,self).__init__(data)



class LinkyWebYearlyDataShaper(LinkyWebDataShaper):
    """Parse JSON data containing yearly consumption"""
    def __init__(self,data):
        self._time_period_unit = 'years'
        self._time_period_value = 1
        super(LinkyWebYearlyDataShaper,self).__init__(data)



def getDataShaper(data,data_period):
    if data_period == 'hours':
        return LinkyWebHourlyDataShaper(data)
    elif data_period == 'days':
        return LinkyWebDailyDataShaper(data)
    elif data_period == 'months':
        return LinkyWebMonthlyDataShaper(data)
    elif data_period == 'years':
        return LinkyWebYearlyDataShaper(data)

__all__ = ['LinkyWebHourlyDataShaper','LinkyWebDailyDataShaper','LinkyWebMonthlyDataShaper',
           'LinkyWebYearlyDataShaper']

