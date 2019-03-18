# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from .testlib import create_calendar, create_user
from .ical_data import ical_data


class ImportWizardTestCase(ModuleTestCase):
    'Test import wizard module'
    module = 'pim_calendar'

    def prep_importwizard_calendar(self):
        """ create user, calendar
        """
        pool = Pool()
        Group = pool.get('res.group')
        Calendar = pool.get('pim_calendar.calendar')
        
        # group
        grp1 = Group.search([('name', '=', 'PIM Calendar - User')])
        self.assertEqual(len(grp1), 1)
        grp1 = grp1[0]
        self.assertEqual(grp1.name, 'PIM Calendar - User')

        usr1 = create_user('Frida', 'Frida'.lower(), 'Test.1234')
        l1 = list(usr1.groups)
        l1.append(grp1)
        usr1.groups = l1
        usr1.save()
        self.assertEqual(usr1.name, 'Frida')
        self.assertEqual(len(usr1.groups), 1)
        self.assertEqual(usr1.groups[0].name, 'PIM Calendar - User')

        c1 = None
        with Transaction().set_user(usr1.id):
            cal1 = create_calendar('Holiday', Calendar.default_owner())
            
            c1 = Calendar.search([])    # find all
            self.assertEqual(len(c1), 1)
            self.assertEqual(c1[0].name, 'Holiday')
            self.assertEqual(c1[0].owner.name, 'Frida')
        return c1[0]

    @with_transaction()
    def test_importwizard_check_default(self):
        """ start wizard, check defaults
        """
        pool = Pool()
        ImportWizard = pool.get('pim_calendar.wiz_import_event', type='wizard')
        
        cal1 = self.prep_importwizard_calendar()
        self.assertEqual(cal1.name, 'Holiday')

        # no valid model
        with Transaction().set_context(active_model='err1'):
            (sess_id, start_state, end_state) = ImportWizard.create()
            self.assertEqual(start_state, 'start')
            self.assertEqual(end_state, 'end')

            w_obj = ImportWizard(sess_id)
            self.assertTrue(w_obj)
            
            self.assertRaisesRegex(UserError,
                "Please use the ics-import with a calendar.",
                ImportWizard.execute,
                sess_id, {}, start_state)

        # no active-ids
        with Transaction().set_context(active_model='pim_calendar.calendar', active_ids=[]):
            (sess_id, start_state, end_state) = ImportWizard.create()
            w_obj = ImportWizard(sess_id)
            self.assertTrue(w_obj)
            
            self.assertRaisesRegex(UserError,
                "Please select \(only\) a calendar.",
                ImportWizard.execute,
                sess_id, {}, start_state)

        with Transaction().set_context(
                active_model='pim_calendar.calendar', 
                active_ids=[cal1.id]
            ):
            (sess_id, start_state, end_state) = ImportWizard.create()
            w_obj = ImportWizard(sess_id)
            self.assertTrue(w_obj)
            
            res1 = ImportWizard.execute(sess_id, {}, start_state)
            self.assertEqual(list(res1.keys()), ['view'])
            self.assertEqual(res1['view']['defaults']['calendar'], cal1.id)
            self.assertEqual(res1['view']['defaults']['icsfile'], '')

            for i in res1['view']['defaults']:
                setattr(w_obj.start, i, res1['view']['defaults'][i])

            self.assertRaisesRegex(
                UserError, 
                "Please select a file to import.", 
                w_obj.transition_importevents)
            
    @with_transaction()
    def test2_importwizard_store_icsfile(self):
        """ import ics-data, check results
        """
        pool = Pool()
        ImportWizard = pool.get('pim_calendar.wiz_import_event', type='wizard')
        Event = pool.get('pim_calendar.event')
        
        cal1 = self.prep_importwizard_calendar()
        self.assertEqual(cal1.name, 'Holiday')

        with Transaction().set_context(
                active_model='pim_calendar.calendar', 
                active_ids=[cal1.id]
            ):
            (sess_id, start_state, end_state) = ImportWizard.create()
            w_obj = ImportWizard(sess_id)
            self.assertTrue(w_obj)
            
            res1 = ImportWizard.execute(sess_id, {}, start_state)
            self.assertEqual(list(res1.keys()), ['view'])
            self.assertEqual(res1['view']['defaults']['calendar'], cal1.id)
            self.assertEqual(res1['view']['defaults']['icsfile'], '')

            for i in res1['view']['defaults']:
                setattr(w_obj.start, i, res1['view']['defaults'][i])
            
            # load file in wizard
            w_obj.start.icsfile = ical_data
            self.assertEqual(w_obj.transition_importevents(), 'end')
            
            ev1 = Event.search([])  # select all events
            ev2 = Event.search([('calendar', '=', cal1.id)], order=[('name', 'ASC')])  # select events in cal1
            self.assertEqual(len(ev1), 7)
            self.assertEqual(len(ev2), 7)

# end ImportWizardTestCase
