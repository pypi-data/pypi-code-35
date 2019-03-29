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
from decimal import Decimal
import datetime

db = Database()

class Meter(db.Entity):
    meters = Set('MeasurementBase')

class Linky(Meter):
    name = Required(str,unique=True)

class MeasurementBase(db.Entity):
    meter = Required(Meter)
    time = Optional(int,size=32,unsigned=True,unique=True)
    date = Optional(str,unique=True)

    def __init__(self,*args,**kwargs):
        super(MeasurementBase,self).__init__(*args,**kwargs)
        self._check_inputs()

    def _check_inputs(self):
        if self.time and self.date:
            raise ValueError('MeasurementBase : you must specify either time or date')

class LinkyMeasurementBase(MeasurementBase):
    value = Required(float)

class LinkyHourly(LinkyMeasurementBase):
    composite_index(MeasurementBase.time,MeasurementBase.meter)

    def _check_inputs(self):
        super(LinkyMeasurementBase,self)._check_inputs()
        if not self.time:
            raise ValueError('Attribute LinkyHourly.time is required')


class LinkyDaily(LinkyMeasurementBase):
    composite_index(MeasurementBase.date,MeasurementBase.meter)

    def _check_inputs(self):
        super(LinkyMeasurementBase,self)._check_inputs()
        if not self.date:
            raise ValueError('Attribute LinkyDaily.date is required')


class LinkyMonthly(LinkyMeasurementBase):
    composite_index(MeasurementBase.date,MeasurementBase.meter)

    def _check_inputs(self):
        super(LinkyMeasurementBase,self)._check_inputs()
        if not self.date:
            raise ValueError('Attribute LinkyMonthly.date is required')

class LinkyYearly(LinkyMeasurementBase):
    composite_index(MeasurementBase.date,MeasurementBase.meter)

    def _check_inputs(self):
        super(LinkyMeasurementBase,self)._check_inputs()
        if not self.date:
            raise ValueError('Attribute LinkyYear.date is required')


def open_db(filename='linky.sqlite',create=False):
    if create: 
        import os
        if os.path.isfile(filename):
            os.remove(filename)

    db.bind(provider='sqlite',filename=filename,create_db=create)
    #db.bind(provider='sqlite',filename=':memory:')
    db.generate_mapping(create_tables=create)

