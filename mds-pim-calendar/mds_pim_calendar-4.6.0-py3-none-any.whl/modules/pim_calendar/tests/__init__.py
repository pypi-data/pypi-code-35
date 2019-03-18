# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

try:
    from trytond.modules.calendar.tests.test_calendar import CalendarTestCase
    from trytond.modules.calendar.tests.test_visitor import VisitorsTestCase
    from trytond.modules.calendar.tests.test_events import EventsTestCase
    from trytond.modules.calendar.tests.test_importwiz import  ImportWizardTestCase
except ImportError:
    from .test_calendar import CalendarTestCase
    from .test_visitor import VisitorsTestCase
    from .test_events import EventsTestCase
    from .test_importwiz import ImportWizardTestCase

__all__ = ['suite']



class CalendarModuleTestCase(\
            CalendarTestCase, \
            EventsTestCase, \
            VisitorsTestCase,\
            ImportWizardTestCase):
    'Test calendar module'
    module = 'pim_calendar'

#end CalendarModuleTestCase


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CalendarModuleTestCase))
    return suite
