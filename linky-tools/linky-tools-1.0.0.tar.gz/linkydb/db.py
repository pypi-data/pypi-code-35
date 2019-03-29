#    linky-tools 
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
#
from pony.orm import *

from .models import *

import time

import logging

logger = logging.getLogger()


'''
The db_session() decorator performs the following actions on exiting function:

    Performs rollback of transaction if the function raises an exception
    Commits transaction if data was changed and no exceptions occurred
    Returns the database connection to the connection pool
    Clears the database session cache
'''

class LinkyDbException(Exception):
    pass

@db_session
def add_meter(metername):
    linky = Linky(name=metername)



class LinkyDbMeter(object):

    @db_session
    def __init__(self,metername,period,is_immutable=True):
        self.metername = metername
        self.period = period
        self.is_immutable = is_immutable
        linky = Linky.get(name=metername)
        if not linky:
            raise ValueError('Unkown meter name: %s' % (metername))

    def _add_data(self,t,value):
        raise NotImplemented

    def _get_data(self,t,value):
        raise NotImplemented

    def _update_data(self,t,value):
        raise NotImplemented

    def _query(self,from_date,to_date):
        raise NotImplemented

    def add_data(self,t,value):
        try:
            self._add_data(t,value)
        except pony.orm.core.TransactionIntegrityError:
            if self.is_immutable:
                m = self._get_data(t)
                if m.value != value:
                    logging.warning('*** %s:Data already in database with a different value' % (t))
            else:
                m = self._get_data(t)
                if m.value < value:
                    logger.warning('%s:%s:update value %f by %f' % (self.period,t,m.value,value))
                    self._update_data(t,value)
                elif m.value > value:
                    logging.warning('%s:%s:Data already in database with a greater value' % (self.period,t))


    def get_data(self,t):
        return self._get_data(t)

    def query(self,from_date,to_date):
        return self._query(from_date,to_date)



class LinkyDbHourlyData(LinkyDbMeter):

    def __init__(self,metername):
        super(LinkyDbHourlyData,self).__init__(metername,period='hours',is_immutable=True)

    @db_session
    def _add_data(self,t,value):
        linky = Linky.get(name=self.metername)
        _time = int(time.mktime(t.timetuple()))
        logger.debug('Add hourly:%d,%f' % (_time,value))
        LinkyHourly(time=_time, value=value,meter=linky)

    @db_session
    def _get_data(self,t):
        linky = Linky.get(name=self.metername)
        _time = int(time.mktime(t.timetuple()))
        logger.debug('Get hourly:%d' % (_time))
        m = LinkyHourly.get(time=_time, meter=linky)
        return m

    @db_session
    def _query(self,from_date,to_date):
        linky = Linky.get(name=self.metername)
        from_time = int(time.mktime(from_date.timetuple()))
        to_time = int(time.mktime(to_date.timetuple()))
        # need to do this rather than returning select result, to avoid db_session issue
        # probably because select function itself is not decorated by @db_session
        for x in select(m for m in LinkyHourly if m.meter == linky and m.time >= from_time and m.time <= to_time).order_by(lambda m: m.time): yield x



class LinkyDbDailyData(LinkyDbMeter):

    def __init__(self,metername):
        super(LinkyDbDailyData,self).__init__(metername,period='days',is_immutable=True)

    @db_session
    def _add_data(self,t,value):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y%b%d")
        logger.debug('Add daily:%s,%f' % (date,value))
        LinkyDaily(date=date,value=value,meter=linky)

    @db_session
    def _get_data(self,t):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y%b%d")
        logger.debug('Get daily:%s' % (date))
        m = LinkyDaily.get(date=date,meter=linky)
        return m



class LinkyDbMonthlyData(LinkyDbMeter):

    def __init__(self,metername):
        super(LinkyDbMonthlyData,self).__init__(metername,period='months',is_immutable=False)

    @db_session
    def _add_data(self,t,value):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y%m")
        logger.debug('Add monthly:%s,%f' % (date,value))
        LinkyMonthly(date=date, value=value,meter=linky)

    @db_session
    def _get_data(self,t):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y%m")
        logger.debug('Get monthly:%s' % (date))
        m = LinkyMonthly.get(date=date, meter=linky)
        return m

    @db_session
    def _update_data(self,t,value):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y%m")
        logger.debug('Update monthly:%s,%f' % (date,value))
        m = LinkyMonthly.get(date=date, meter=linky)
        m.value = value


class LinkyDbYearlyData(LinkyDbMeter):

    def __init__(self,metername):
        super(LinkyDbYearlyData,self).__init__(metername,period='years',is_immutable=False)

    @db_session
    def _add_data(self,t,value):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y")
        logger.debug('Add yearly:%s,%f' % (date,value))
        LinkyYearly(date=date, value=value,meter=linky)

    @db_session
    def _get_data(self,t):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y")
        logger.debug('Get yearly:%s' % (date))
        m = LinkyYearly.get(date=date, meter=linky)
        return m

    @db_session
    def _update_data(self,t,value):
        linky = Linky.get(name=self.metername)
        date = t.strftime("%Y")
        logger.debug('Update yearly:%s,%f' % (date,value))
        m = LinkyYearly.get(date=date, meter=linky)
        m.value = value



__all__ =['db_session', 'add_meter', 
        'LinkyDbHourlyData', 
        'LinkyDbDailyData', 
        'LinkyDbMonthlyData', 
        'LinkyDbYearlyData', 
        'LinkyDbException']

