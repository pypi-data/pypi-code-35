# -*- coding: utf-8 -*-

from trytond.pool import Pool
from .calendar2 import Calendar, CalendarSettings
from .visitors import Visitor
from .events import Event
from .importwiz import EventImportWizardStart, EventImportWizard
from .exportcal import ExportCalendar

def register():
    Pool.register(
        Visitor,
        Calendar,
        CalendarSettings,
        Event,
        EventImportWizardStart,
        module='pim_calendar', type_='model')
    Pool.register(
        ExportCalendar,
        module='pim_calendar', type_='report')
    Pool.register(
        EventImportWizard,
        module='pim_calendar', type_='wizard')
