# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from datetime import datetime
import icalendar, copy
from .testlib import create_user, create_calendar
from .ical_data import ical_data


class CalendarTestCase(ModuleTestCase):
    'Test calendar module'
    module = 'pim_calendar'

    def prep_calendar_newuser(self, name, group):
        """ create user, add to group
        """
        pool = Pool()
        Group = pool.get('res.group')
        
        # group
        grp1 = Group.search([('name', '=', group)])
        self.assertEqual(len(grp1), 1)
        grp1 = grp1[0]
        self.assertEqual(grp1.name, group)

        usr1 = create_user(name, name.lower(), 'Test.1234')
        l1 = list(usr1.groups)
        l1.append(grp1)
        usr1.groups = l1
        usr1.save()
        self.assertEqual(usr1.name, name)
        self.assertEqual(len(usr1.groups), 1)
        self.assertEqual(usr1.groups[0].name, group)
        return usr1

    @with_transaction()
    def test_calendar_create_item(self):
        """ create valid item
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        User = pool.get('res.user')
        
        us1 = User(name='Frida', login='frida', password='test.1234')
        us1.save()
        us1_lst = User.search([])    # find all
        self.assertEqual(len(us1_lst), 2)    # admin + frida
        
        us2_lst = User.search([('login', '=', 'frida')])
        self.assertEqual(len(us2_lst), 1)
        self.assertEqual(us2_lst[0].name, 'Frida')
        
        with Transaction().set_user(us2_lst[0].id):
            cal1 = Calendar(
                    name = 'Holiday',
                    owner = Calendar.default_owner(),
                )
            cal1.save()
            self.assertEqual(cal1.name, 'Holiday')
            self.assertEqual(cal1.owner.name, 'Frida')
            self.assertEqual(cal1.cal_color, '#5e8ac7')
            self.assertEqual(cal1.cal_visible, True)

    @with_transaction()
    def test_calendar_add_visitors(self):
        """ create item, add visitors
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        User = pool.get('res.user')
        Visitor = pool.get('pim_calendar.visitor')

        us1 = self.prep_calendar_newuser('Frida', 'PIM Calendar - User')
        us2 = self.prep_calendar_newuser('Diego', 'PIM Calendar - User')
        us1_lst = User.search([], order=[('login', 'ASC')])    # find all
        self.assertEqual(len(us1_lst), 3)    # admin + frida + diego
        self.assertEqual(us1_lst[0].name, 'Administrator')
        self.assertEqual(us1_lst[1].name, 'Diego')
        self.assertEqual(us1_lst[2].name, 'Frida')

        with Transaction().set_user(us1_lst[2].id):
            cal1 = Calendar(
                    name = 'Holiday',
                    owner = Calendar.default_owner(),
                )
            cal1.save()
            
            c1 = Calendar.search([])    # find all
            self.assertEqual(len(c1), 1)
            self.assertEqual(c1[0].name, 'Holiday')
            self.assertEqual(c1[0].owner.name, 'Frida')
            
            c1[0].visitors = [
                    Visitor(
                        visitor=us1_lst[1],
                        accchange=True,
                        )
                ]
            c1[0].save()
            self.assertEqual(len(c1[0].visitors), 1)
            self.assertEqual(c1[0].visitors[0].visitor.name, 'Diego')
            self.assertEqual(c1[0].visitors[0].accchange, True)
            self.assertEqual(c1[0].visitors[0].acccreate, False)
            self.assertEqual(c1[0].visitors[0].accdelete, False)

            v1 = Visitor.search([])
            self.assertEqual(len(v1), 1)
            self.assertEqual(v1[0].visitor.name, 'Diego')
            
            # delete calendar
            Calendar.delete(c1)
            c1 = Calendar.search([])    # find all
            self.assertEqual(len(c1), 0)
            v1 = Visitor.search([])
            self.assertEqual(len(v1), 0)

    @with_transaction()
    def test_calendar_isowner(self):
        """ create calendar, check 'isowner'
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        Visitor = pool.get('pim_calendar.visitor')
        
        usr1 = self.prep_calendar_newuser('Frida', 'PIM Calendar - User')
        usr2 = self.prep_calendar_newuser('Diego', 'PIM Calendar - User')
        cal1 = create_calendar('Cal1', usr1)
        
        clst = Calendar.search([('name', '=', 'Cal1')])
        self.assertEqual(len(clst), 1)
        self.assertEqual(clst[0].name, 'Cal1')
        self.assertEqual(clst[0].owner.name, 'Frida')
        self.assertEqual(clst[0].owner.id, usr1.id)
        
        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].isowner, True)

            o_lst = Calendar.search([('isowner', '=', True)])
            self.assertEqual(len(o_lst), 1)
            self.assertEqual(o_lst[0].name, 'Cal1')

            o_lst = Calendar.search([('isowner', '=', False)])
            self.assertEqual(len(o_lst), 0)

            o_lst = Calendar.search([('isowner', '=', 1)])
            self.assertEqual(len(o_lst), 1)
            o_lst = Calendar.search([('isowner', '=', 0)])
            self.assertEqual(len(o_lst), 0)

            o_lst = Calendar.search([('isowner', '!=', True)])
            self.assertEqual(len(o_lst), 0)

            o_lst = Calendar.search([('isowner', '!=', False)])
            self.assertEqual(len(o_lst), 1)

            self.assertRaisesRegex(ValueError, "query invalid", Calendar.search, [('isowner', 'in', [False])])
            self.assertRaisesRegex(ValueError, "query invalid", Calendar.search, [('isowner', '=', 2)])
            self.assertRaisesRegex(ValueError, "query invalid", Calendar.search, [('isowner', '=', 'yes')])
            self.assertRaisesRegex(ValueError, "query invalid", Calendar.search, [('isowner', '!=', 'no')])

            # add visitor 'diego' to fridas calendar
            c2lst[0].visitors = [Visitor(visitor=usr2)]
            c2lst[0].save()
            self.assertEqual(len(c2lst[0].visitors), 1)
            self.assertEqual(c2lst[0].visitors[0].visitor.name, 'Diego')

        with Transaction().set_user(usr2.id):
            c3lst = Calendar.search([()])
            self.assertEqual(len(c3lst), 1)
            self.assertEqual(c3lst[0].isowner, False)

    @with_transaction()
    def test_calendar_limittext(self):
        """ create calendar (long name), test rec_name
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        Visitor = pool.get('pim_calendar.visitor')
        
        usr1 = self.prep_calendar_newuser('Frida', 'PIM Calendar - User')
        usr2 = self.prep_calendar_newuser('Diego', 'PIM Calendar - User')
        cal1 = create_calendar('Cal1', usr1)
        cal1.visitors = [Visitor(visitor=usr2)]
        cal1.save()
        self.assertEqual(len(cal1.visitors), 1)
        self.assertEqual(cal1.visitors[0].visitor.rec_name, 'Diego')

        # check as Frida
        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].name, 'Cal1')
            
            c2lst[0].cal_limittext = True
            c2lst[0].cal_limitanz = 21
            c2lst[0].name = '0123456789'
            c2lst[0].save()
            
            self.assertEqual(c2lst[0].name_lim, '0123456789')
            self.assertEqual(len(c2lst[0].name_lim), 10)

            c2lst[0].name = '01234567890123456789012345'
            c2lst[0].save()
            self.assertEqual(c2lst[0].name_lim, '01234567890123456789*')
            self.assertEqual(len(c2lst[0].name_lim), 21)

            c2lst[0].name = 'Cal1'
            c2lst[0].save()
        
        # check as Diego
        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].name, 'Cal1')
            
            # enable limiter
            c2lst[0].cal_limittext = True
            c2lst[0].cal_limitanz = 21
            c2lst[0].save()
            
            c2lst[0].name = '0123456789'
            self.assertRaisesRegex(UserError, 
                "Changing the field 'name' is not allowed.",
                c2lst[0].save)

        # edit as Frida
        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].cal_limittext = True
            c2lst[0].cal_limitanz = 21
            c2lst[0].name = '0123456789'
            c2lst[0].save()
        
        # diego
        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].cal_limittext, True)
            self.assertEqual(c2lst[0].name_lim, '0123456789 (Frida)')
            self.assertEqual(len(c2lst[0].name_lim), 18)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].name = '0123456789012'
            c2lst[0].save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].cal_limittext, True)
            self.assertEqual(c2lst[0].name_lim, '0123456789012 (Frida)')
            self.assertEqual(len(c2lst[0].name_lim), 21)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].name = '01234567890123'
            c2lst[0].save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].cal_limitanz, 21)
            self.assertEqual(c2lst[0].cal_limittext, True)
            self.assertEqual(c2lst[0].name_lim, '012345678901* (Frida)')
            self.assertEqual(len(c2lst[0].name_lim), 21)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].cal_limittext = False
            c2lst[0].name = '01234567890123'
            c2lst[0].save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].cal_limittext = False
            c2lst[0].save()
            self.assertEqual(c2lst[0].name_lim, '01234567890123 (Frida)')
            self.assertEqual(len(c2lst[0].name_lim), 22)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].name = '01234567890123'
            c2lst[0].save()
            usr1.name = 'Frida12'
            usr1.save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].cal_limittext, False)
            self.assertEqual(c2lst[0].name_lim, '01234567890123 (Frida12)')
            self.assertEqual(len(c2lst[0].name_lim), 24)

            c2lst[0].cal_limittext = True
            c2lst[0].save()
            self.assertEqual(c2lst[0].name_lim, '0123456789* (Frida12)')
            self.assertEqual(len(c2lst[0].name_lim), 21)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            usr1.name = 'Frida123'
            usr1.save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(c2lst[0].cal_limittext, True)
            self.assertEqual(c2lst[0].cal_limitanz, 21)
            self.assertEqual(c2lst[0].name_lim, '0123456789* (Frida1*)')
            self.assertEqual(len(c2lst[0].name_lim), 21)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].name = '0123456789'
            c2lst[0].save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(c2lst[0].cal_limittext, True)
            self.assertEqual(c2lst[0].cal_limitanz, 21)
            self.assertEqual(c2lst[0].name_lim, '0123456789 (Frida123)')
            self.assertEqual(len(c2lst[0].name_lim), 21)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            usr1.name = 'Frida1234'
            usr1.save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            self.assertEqual(c2lst[0].cal_limittext, True)
            self.assertEqual(c2lst[0].cal_limitanz, 21)
            self.assertEqual(c2lst[0].name_lim, '0123456789 (Frida1*)')
            self.assertEqual(len(c2lst[0].name_lim), 20)

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].cal_limitanz = 18
            c2lst[0].name = '0123456789'
            c2lst[0].save()
            usr1.name = 'Frida1234'
            usr1.save()

        with Transaction().set_user(usr2.id):
            c2lst = Calendar.search([()])
            c2lst[0].cal_limitanz = 18
            c2lst[0].save()
            self.assertEqual(c2lst[0].name_lim, '0123456* (Frida1*)')
            self.assertEqual(len(c2lst[0].name_lim), 18)

    @with_transaction()
    def test_calendar_color(self):
        """ create calendar, set color, check with different users
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        Visitor = pool.get('pim_calendar.visitor')
        
        usr1 = self.prep_calendar_newuser('Frida', 'PIM Calendar - User')
        usr2 = self.prep_calendar_newuser('Diego', 'PIM Calendar - User')
        cal1 = create_calendar('Cal1', usr1)
        
        clst = Calendar.search([('name', '=', 'Cal1')])
        self.assertEqual(len(clst), 1)
        self.assertEqual(clst[0].name, 'Cal1')
        self.assertEqual(clst[0].owner.name, 'Frida')

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].name, 'Cal1')

            # add visitor 'diego' to fridas calendar
            c2lst[0].visitors = [Visitor(visitor=usr2)]
            c2lst[0].save()
            self.assertEqual(len(c2lst[0].visitors), 1)
            self.assertEqual(c2lst[0].visitors[0].visitor.name, 'Diego')

            self.assertEqual(c2lst[0].cal_color, '#5e8ac7')
            self.assertEqual(c2lst[0].cal_visible, True)
            
            # frida edits color
            c2lst[0].cal_color = '#ed1c24'  # red
            c2lst[0].save()
            self.assertEqual(c2lst[0].cal_color, '#ed1c24')
            
        with Transaction().set_user(usr2.id):
            c3lst = Calendar.search([('name', '=', 'Cal1')])
            self.assertEqual(len(c3lst), 1)
            self.assertEqual(c3lst[0].name, 'Cal1')
            self.assertEqual(c3lst[0].owner.name, 'Frida')

            # diego has still default color on same calendar
            self.assertEqual(c3lst[0].cal_color, '#5e8ac7')
            self.assertEqual(c3lst[0].cal_visible, True)

            # diego edits color of frida's 'Cal1' for his own view
            c3lst[0].cal_color = '#00a65d'  # green
            c3lst[0].save()
            c3lsta = Calendar.search([('name', '=', 'Cal1')])
            self.assertEqual(c3lsta[0].cal_color, '#00a65d')

        with Transaction().set_user(usr1.id):
            c4lst = Calendar.search([('name', '=', 'Cal1')])
            self.assertEqual(len(c4lst), 1)
            self.assertEqual(c4lst[0].cal_color, '#ed1c24') # still red

    @with_transaction()
    def test_calendar_edit_by_multiuser(self):
        """ create calendar, check permissions
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        Visitor = pool.get('pim_calendar.visitor')
        
        usr1 = self.prep_calendar_newuser('Frida', 'PIM Calendar - User')
        usr2 = self.prep_calendar_newuser('Diego', 'PIM Calendar - User')
        cal1 = create_calendar('Cal1', usr1)
        
        clst = Calendar.search([('name', '=', 'Cal1')])
        self.assertEqual(len(clst), 1)
        self.assertEqual(clst[0].name, 'Cal1')
        self.assertEqual(clst[0].owner.name, 'Frida')

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([()])
            self.assertEqual(len(c2lst), 1)
            self.assertEqual(c2lst[0].name, 'Cal1')
            self.assertEqual(c2lst[0].isowner, True)
            
            # add visitor 'diego' to fridas calendar
            c2lst[0].visitors = [Visitor(visitor=usr2)]
            c2lst[0].save()
            self.assertEqual(len(c2lst[0].visitors), 1)
            self.assertEqual(c2lst[0].visitors[0].visitor.name, 'Diego')
            
            # frida edits the name
            c2lst[0].name = 'Cal2'
            c2lst[0].save()
            self.assertEqual(c2lst[0].name, 'Cal2')

        with Transaction().set_user(usr2.id):
            c3lst = Calendar.search([('name', '=', 'Cal2')])
            self.assertEqual(len(c3lst), 1)
            self.assertEqual(c3lst[0].isowner, False)
            
            # diego edits the name - should fail
            c3lst[0].name = 'Cal3'
            self.assertRaisesRegex(UserError,
                "Changing the field 'name' is not allowed.",
                c3lst[0].save)

            l1a = Calendar.search([('name', '=', 'Cal2')])
            self.assertEqual(len(l1a), 1)
            l1a[0].note = 'add a note'
            self.assertRaisesRegex(UserError,
                "Changing the field 'note' is not allowed.",
                l1a[0].save)
                
            l1b = Calendar.search([('name', '=', 'Cal2')])
            self.assertEqual(len(l1b), 1)
            l1b[0].owner = usr2
            self.assertRaisesRegex(UserError,
                "Changing the field 'owner' is not allowed.",
                l1b[0].save)

            l1c = Calendar.search([('name', '=', 'Cal2')])
            self.assertEqual(len(l1c), 1)
            l1c[0].visitors = []
            self.assertRaisesRegex(UserError,
                "Changing the field 'visitors' is not allowed.",
                l1c[0].save)

            l1d = Calendar.search([('name', '=', 'Cal2')])
            self.assertEqual(len(l1d), 1)
            l1d[0].events = []
            self.assertRaisesRegex(UserError,
                "Changing the field 'events' is not allowed.",
                l1d[0].save)

    @with_transaction()
    def test_calendar_search_by_visibility(self):
        """ create calendar, set visibility, search
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        Event = pool.get('pim_calendar.event')
        
        usr1 = self.prep_calendar_newuser('Frida', 'PIM Calendar - User')
        cal1 = create_calendar('Cal1', usr1)
        
        clst = Calendar.search([('name', '=', 'Cal1')])
        self.assertEqual(len(clst), 1)
        self.assertEqual(clst[0].name, 'Cal1')
        self.assertEqual(clst[0].owner.name, 'Frida')

        with Transaction().set_user(usr1.id):
            c2lst = Calendar.search([('name', '=', 'Cal1')])
            self.assertEqual(len(c2lst), 1)
            c2lst[0].cal_visible = True
            c2lst[0].save()
            
            c3lst = Calendar.search([('name', '=', 'Cal1')])
            self.assertEqual(len(c3lst), 1)
            self.assertEqual(c3lst[0].cal_visible, True)

            c1lst = Calendar.search([('cal_visible', '=', True)])
            self.assertEqual(len(c1lst), 1)
            
            c2lst[0].cal_visible = False
            c2lst[0].save()

            c3lst = Calendar.search([('name', '=', 'Cal1')])
            self.assertEqual(len(c3lst), 1)
            self.assertEqual(c3lst[0].cal_visible, False)

            c1lst = Calendar.search([('cal_visible', '=', True)])
            self.assertEqual(len(c1lst), 0)

            # add events
            c3lst[0].events = [
                Event(
                    name='Evnt1', 
                    startpos=datetime(2019, 2, 26, 12, 0, 0),
                    endpos=datetime(2019, 2, 26, 14, 30, 0)
                )]
            c3lst[0].cal_visible = True
            c3lst[0].save()
            ev1 = Event.search([])
            self.assertEqual(len(ev1), 1)
            
            # find events by visibility of calendar
            ev2 = Event.search([('calendar.cal_visible', '=', True)])
            self.assertEqual(len(ev2), 1)
            self.assertEqual(ev2[0].name, 'Evnt1')
            self.assertEqual(ev2[0].calendar.rec_name, 'Cal1')

    @with_transaction()
    def test_calendar_ical_read_ics(self):
        """ read ical-data 
        """
        Calendar = Pool().get('pim_calendar.calendar')
        
        self.assertRaisesRegex(UserError,
            "Error during import \(Content line could not be parsed into parts: 'nope': Invalid content line\)",
            Calendar.ical_data_read,
            'nope')

        r1 = Calendar.ical_data_read(ical_data)
        self.assertEqual(type(r1), type(icalendar.Calendar()))
        
        event = r1.walk('VEVENT')[0]
        self.assertEqual(type(event), type(icalendar.Event()))
        self.assertEqual(str(event['DTSTART'].dt), '2008-06-21 09:00:00+02:00')
        self.assertEqual(str(event['DTEND'].dt), '2008-06-21 09:15:00+02:00')
        self.assertEqual(event['SUMMARY'], 'Ventile bewegen')

    @with_transaction()
    def test_calendar_ical_addevent(self):
        """ add event from ical-data 
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        Event = pool.get('pim_calendar.event')

        ical1 = Calendar.ical_data_read(ical_data)
        self.assertEqual(type(ical1), type(icalendar.Calendar()))

        usr1 = self.prep_calendar_newuser('Frida', 'PIM Calendar - User')
        cal1 = create_calendar('Cal1', usr1)
        
        clst = Calendar.search([('name', '=', 'Cal1')])
        self.assertEqual(len(clst), 1)
        
        # add simple item, no repeat, no description, datetime()
        event1 = ical1.walk('VEVENT')[0]
        self.assertEqual(type(event1), type(icalendar.Event()))
        self.assertEqual(str(event1['DTSTART'].dt), '2008-06-21 09:00:00+02:00')
        self.assertEqual(str(event1['DTEND'].dt), '2008-06-21 09:15:00+02:00')
        self.assertEqual(event1['SUMMARY'], 'Ventile bewegen')
        event1a = copy.deepcopy(event1)
        del event1a['RRULE']

        ev1 = Event.ical_add_event(clst[0], event1a)
        
        ev2 = Event.search([])
        self.assertEqual(len(ev2), 1)
        # events are stored in UTC
        self.assertEqual(str(ev2[0].startpos), '2008-06-21 07:00:00')
        self.assertEqual(str(ev2[0].endpos), '2008-06-21 07:15:00')
        self.assertEqual(ev2[0].name, 'Ventile bewegen')
        self.assertEqual(ev2[0].note, None)
        self.assertEqual(ev2[0].wholeday, False)
        self.assertEqual(ev2[0].calendar.name, 'Cal1')

        # add item with description, no repeat, date()
        event2 = ical1.walk('VEVENT')[6]
        self.assertEqual(type(event2), type(icalendar.Event()))
        self.assertEqual(event2['SUMMARY'], 'Sommerferien Brandenburg')
        self.assertEqual(event2['DESCRIPTION'], 'Alle Termine auf www.schulferien.org')
        self.assertEqual(str(event2['DTSTART'].dt), '2014-07-10')
        # allday-event, ends at next day HH:MM=00:00
        self.assertEqual(str(event2['DTEND'].dt), '2014-08-23')

        ev3 = Event.ical_add_event(clst[0], event2)

        ev4 = Event.search([('name', '!=', 'Ventile bewegen')])
        self.assertEqual(len(ev4), 1)
        self.assertEqual(str(ev4[0].startpos), '2014-07-10 00:00:00')
        self.assertEqual(str(ev4[0].endpos), '2014-08-22 00:00:00')
        self.assertEqual(ev4[0].wholeday, True)
        self.assertEqual(ev4[0].name, 'Sommerferien Brandenburg')
        self.assertEqual(ev4[0].note, 'Alle Termine auf www.schulferien.org')
        self.assertEqual(ev4[0].calendar.name, 'Cal1')

# end CalendarTestCase
