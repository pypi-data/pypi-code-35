# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from datetime import datetime, timedelta
from .testlib import create_calendar, create_user


class EventsTestCase(ModuleTestCase):
    'Test events module'
    module = 'pim_calendar'

    def prep_events_newuser(self, name, group):
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
        
    def prep_events_users_cal(self):
        """ create user, add group, create calendar
        """
        # user
        usr1 = self.prep_events_newuser('Frida', 'PIM Calendar - User')

        cal1 = create_calendar('Test 1', usr1)
        self.assertEqual(cal1.name, 'Test 1')
        self.assertEqual(cal1.owner.name, 'Frida')
        return cal1
        
    @with_transaction()
    def test_events_create_item(self):
        """ create event
        """
        Event = Pool().get('pim_calendar.event')
        cal1 = self.prep_events_users_cal()

        with Transaction().set_user(cal1.owner.id):
            cal1.events = [
                Event(name='Testevnt1',
                    startpos = datetime(2019, 2, 18, 10, 0, 0),
                    endpos = datetime(2019, 2, 18, 10, 30, 0),
                    )
                ]
            cal1.save()

        e_lst = Event.search([])
        self.assertEqual(len(e_lst), 1)
        self.assertEqual(e_lst[0].name, 'Testevnt1')
        self.assertEqual(str(e_lst[0].startpos), '2019-02-18 10:00:00')
        self.assertEqual(str(e_lst[0].endpos), '2019-02-18 10:30:00')
        self.assertEqual(str(e_lst[0].rec_name), 'Testevnt1 - 18.02.2019 10:00 - 10:30 (Test 1 (Frida))')

        # use defaults
        l1 = list(cal1.events)
        dt1 = datetime.now()
        l1.append(Event(name='Testevnt2'))
        cal1.events = l1
        cal1.save()
        dt2 = datetime.now()
        
        e2_lst = Event.search([('name', '=', 'Testevnt2')])
        self.assertEqual(len(e2_lst), 1)
        self.assertTrue(
            datetime(dt1.year, dt1.month, dt1.day, dt1.hour, dt1.minute, dt1.second) <= 
            e2_lst[0].startpos <= 
            datetime(dt2.year, dt2.month, dt2.day, dt2.hour, dt2.minute, dt2.second))

        self.assertTrue(
            (datetime(dt1.year, dt1.month, dt1.day, dt1.hour, dt1.minute, dt1.second) + timedelta(seconds=30*60)) <= 
            e2_lst[0].endpos <= 
            (datetime(dt2.year, dt2.month, dt2.day, dt2.hour, dt2.minute, dt2.second) + timedelta(seconds=30*60)))

    @with_transaction()
    def test_events_check_constraints(self):
        """ create event, check constraints
        """
        Event = Pool().get('pim_calendar.event')
        cal1 = self.prep_events_users_cal()

        ev1 = Event(name='End < Start',
            calendar=cal1,
            startpos = datetime(2019, 2, 18, 12, 0, 0),
            endpos = datetime(2019, 2, 18, 10, 0, 0),
            )
        self.assertRaisesRegex(UserError,
            "The end must be after the beginning.",
            ev1.save)

    @with_transaction()
    def test_events_check_location_textlimit(self):
        """ create event, check limiting text on location
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Calendar = pool.get('pim_calendar.calendar')
        cal1 = self.prep_events_users_cal()
        
        with Transaction().set_user(cal1.owner.id):
            cal2 = Calendar.search([()])
            self.assertEqual(len(cal2), 1)
            self.assertEqual(cal2[0].name, 'Test 1')
            
            cal2[0].cal_limittext = True
            cal2[0].cal_limitanz = 21
            cal2[0].save()
            
            cal2[0].events = [
                Event(name='Test evnt1234567890123',
                    location='abcdefghijklmnopqrstuvw',
                    startpos = datetime(2019, 2, 18, 10, 0, 0),
                    endpos = datetime(2019, 2, 18, 10, 30, 0),
                    )
                ]
            cal2[0].save()
            self.assertEqual(len(cal2[0].events), 1)
            self.assertEqual(cal2[0].events[0].location, 'abcdefghijklmnopqrstuvw')
            self.assertEqual(cal2[0].events[0].location_lim, 'abcdefghijklmnopqrst*')
            self.assertEqual(len(cal2[0].events[0].location_lim), 21)

            self.assertEqual(cal2[0].events[0].name, 'Test evnt1234567890123')
            self.assertEqual(cal2[0].events[0].name_lim, 'Test evnt12345678901*')
            self.assertEqual(len(cal2[0].events[0].name_lim), 21)

    @with_transaction()
    def test_events_perm_viewonly(self):
        """ create calendar, events, edit/delete/create in other users calendar
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')

        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')

        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=False,
                accdelete=False,
                acccreate=False,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        
        # frida creates a event
        with Transaction().set_user(cal1.owner.id):
            ev1 = Event(
                    name='Test 1',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            ev1.save()
            evlst = Event.search([])
            self.assertEqual(len(evlst), 1)
            self.assertEqual(evlst[0].name, 'Test 1')
            
        with Transaction().set_user(usr2.id):
            # diego tries to edit a event in fridas 'Test 1'-calendar
            # no permission - should fail
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertEqual(ev2lst[0].calendar.owner.name, 'Frida')
            ev2lst[0].name = 'Test 1a'
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2lst[0].save)

            # delete w/o permission
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                Event.delete,
                ev2lst)

            # create w/o permission
            ev2 = Event(
                    name='Test 2',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2.save)

    @with_transaction()
    def test_events_perm_allowview(self):
        """ create calendar, events, try to violate against permissions
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')

        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')

        # 2nd calendar, no visitors
        cal2 = create_calendar('Test 2', cal1.owner)
        self.assertEqual(cal2.name, 'Test 2')

        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=False,
                accdelete=False,
                acccreate=False,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        
        # frida creates a event
        with Transaction().set_user(cal1.owner.id):
            ev1 = Event(
                    name='Event 1',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            ev1.save()

            ev2 = Event(
                    name='Event 2',
                    startpos = datetime(2019, 2, 21, 10, 0, 0),
                    endpos = datetime(2019, 2, 21, 10, 30, 0),
                    calendar = cal2,
                )
            ev2.save()

            evlst = Event.search([], order=[('name', 'ASC')])
            self.assertEqual(len(evlst), 2)
            self.assertEqual(evlst[0].name, 'Event 1')
            self.assertEqual(evlst[0].calendar.name, 'Test 1')
            self.assertEqual(evlst[1].name, 'Event 2')
            self.assertEqual(evlst[1].calendar.name, 'Test 2')
            
        with Transaction().set_user(usr2.id):
            # diego read event 'Test 1'
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertEqual(ev2lst[0].name, 'Event 1')
            self.assertEqual(ev2lst[0].calendar.owner.name, 'Frida')

            # diego tries to edit a event in fridas 'Test 1'-calendar
            # no permission - should fail
            ev2lst[0].name = 'Test 1a'
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2lst[0].save)

            # delete w/o permission
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                Event.delete,
                ev2lst)

            # create - should fail
            ev2 = Event(
                    name='Test 2',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2.save)

    @with_transaction()
    def test_events_perm_allowcreate(self):
        """ create calendar, events, create in other users calendar
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')

        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')

        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=False,
                accdelete=False,
                acccreate=True,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        
        # frida creates a event
        with Transaction().set_user(cal1.owner.id):
            ev1 = Event(
                    name='Test 1',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            ev1.save()
            evlst = Event.search([])
            self.assertEqual(len(evlst), 1)
            self.assertEqual(evlst[0].name, 'Test 1')
            
        with Transaction().set_user(usr2.id):
            # diego tries to edit a event in fridas 'Test 1'-calendar
            # no permission - should fail
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertEqual(ev2lst[0].calendar.owner.name, 'Frida')
            ev2lst[0].name = 'Test 1a'
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2lst[0].save)

            # delete w/o permission
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                Event.delete,
                ev2lst)

            # create
            ev2 = Event(
                    name='Test 2',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            ev2.save()

    @with_transaction()
    def test_events_perm_allowdelete(self):
        """ create calendar, events, edit/delete/create in other users calendar
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')

        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')

        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=False,
                accdelete=True,
                acccreate=False,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        
        # frida creates a event
        with Transaction().set_user(cal1.owner.id):
            ev1 = Event(
                    name='Test 1',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            ev1.save()
            evlst = Event.search([])
            self.assertEqual(len(evlst), 1)
            self.assertEqual(evlst[0].name, 'Test 1')
            
        with Transaction().set_user(usr2.id):
            # diego tries to edit a event in fridas 'Test 1'-calendar
            # no permission - should fail
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertEqual(ev2lst[0].calendar.owner.name, 'Frida')
            ev2lst[0].name = 'Test 1a'
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2lst[0].save)

            # delete
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            Event.delete(ev2lst)

            # create w/o permission
            ev2 = Event(
                    name='Test 2',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2.save)

    @with_transaction()
    def test_events_perm_allowchange(self):
        """ create calendar, events, change in other users calendar
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')

        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')

        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=True,
                accdelete=False,
                acccreate=False,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        
        # frida creates a event
        with Transaction().set_user(cal1.owner.id):
            ev1 = Event(
                    name='Test 1',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            ev1.save()
            evlst = Event.search([])
            self.assertEqual(len(evlst), 1)
            self.assertEqual(evlst[0].name, 'Test 1')
            
        with Transaction().set_user(usr2.id):
            # diego tries to edit a event in fridas 'Test 1'-calendar
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertEqual(ev2lst[0].calendar.owner.name, 'Frida')
            ev2lst[0].name = 'Test 1a'
            ev2lst[0].save()

            # delete w/o permission
            ev2lst = Event.search([])
            self.assertEqual(len(ev2lst), 1)
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                Event.delete,
                ev2lst)

            # create w/o permission
            ev2 = Event(
                    name='Test 2',
                    startpos = datetime(2019, 2, 20, 10, 0, 0),
                    endpos = datetime(2019, 2, 20, 10, 30, 0),
                    calendar = cal1,
                )
            self.assertRaisesRegex(UserError, 
                "You try to bypass an access rule.*",
                ev2.save)

    @with_transaction()
    def test_events_permission_change(self):
        """ create event, calendar, visitors, check change permission
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')
        # calendar 1
        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        
        # calendar 2
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')
        cal2 = create_calendar('Test 2', usr2)
        self.assertEqual(cal2.name, 'Test 2')
        self.assertEqual(cal2.owner.name, 'Diego')

        usr3 = self.prep_events_newuser('John', 'PIM Calendar - User')
        
        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=True,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        self.assertEqual(cal1.visitors[0].accchange, True)
        self.assertEqual(cal1.visitors[0].accdelete, False)
        self.assertEqual(cal1.visitors[0].acccreate, False)

        # add event to calendar 1
        cal1.events = [
            Event(name='Testevnt1',
                startpos = datetime(2019, 2, 18, 10, 0, 0),
                endpos = datetime(2019, 2, 18, 10, 30, 0),
                )
            ]
        cal1.save()
        self.assertEqual(len(cal1.events), 1)
        self.assertEqual(cal1.events[0].name, 'Testevnt1')
        self.assertEqual(str(cal1.events[0].startpos), '2019-02-18 10:00:00')

        # add event to calendar 2
        cal2.events = [
            Event(name='Testevnt2',
                startpos = datetime(2019, 2, 18, 10, 0, 0),
                endpos = datetime(2019, 2, 18, 10, 30, 0),
                )
            ]
        cal2.save()
        self.assertEqual(len(cal2.events), 1)
        self.assertEqual(cal2.events[0].name, 'Testevnt2')
        self.assertEqual(str(cal2.events[0].startpos), '2019-02-18 10:00:00')
        
        # count all events
        e3 = Event.search([])
        self.assertEqual(len(e3), 2)
        
        # check 'change'
        # switch to 'Frida'
        with Transaction().set_user(cal1.owner.id):
            e1 = Event.search([])
            self.assertEqual(len(e1), 1)
            self.assertEqual(e1[0].name, 'Testevnt1')
            self.assertEqual(e1[0].permchange, False)
            self.assertEqual(e1[0].owner, True)
            
            e2 = Event.search([('permchange', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('permchange', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 0)

        # switch to 'Diego'
        with Transaction().set_user(usr2.id):
            e1 = Event.search([], order=[('name', 'ASC')])
            self.assertEqual(len(e1), 2)
            self.assertEqual(e1[0].name, 'Testevnt1')
            self.assertEqual(e1[0].permchange, True)
            self.assertEqual(e1[0].owner, False)
            self.assertEqual(e1[1].name, 'Testevnt2')
            self.assertEqual(e1[1].permchange, False)
            self.assertEqual(e1[1].owner, True)
            
            e2 = Event.search([('permchange', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')
            e2 = Event.search([('permchange', 'in', [True])])
            self.assertEqual(len(e2), 1)
            e2 = Event.search([('permchange', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt2')
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')
            
        # switch to 'John' - no access
        with Transaction().set_user(usr3.id):
            e1 = Event.search([], order=[('name', 'ASC')])
            self.assertEqual(len(e1), 0)
            
            e2 = Event.search([('permchange', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('permchange', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 0)

    @with_transaction()
    def test_events_permission_delete(self):
        """ create event, calendar, visitors, check delete permission
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')
        # calendar 1
        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        
        # calendar 2
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')
        cal2 = create_calendar('Test 2', usr2)
        self.assertEqual(cal2.name, 'Test 2')
        self.assertEqual(cal2.owner.name, 'Diego')

        usr3 = self.prep_events_newuser('John', 'PIM Calendar - User')
        
        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                accdelete=True,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        self.assertEqual(cal1.visitors[0].accchange, False)
        self.assertEqual(cal1.visitors[0].accdelete, True)
        self.assertEqual(cal1.visitors[0].acccreate, False)

        # add event to calendar 1
        cal1.events = [
            Event(name='Testevnt1',
                startpos = datetime(2019, 2, 18, 10, 0, 0),
                endpos = datetime(2019, 2, 18, 10, 30, 0),
                )
            ]
        cal1.save()
        self.assertEqual(len(cal1.events), 1)
        self.assertEqual(cal1.events[0].name, 'Testevnt1')
        self.assertEqual(str(cal1.events[0].startpos), '2019-02-18 10:00:00')

        # add event to calendar 2
        cal2.events = [
            Event(name='Testevnt2',
                startpos = datetime(2019, 2, 18, 10, 0, 0),
                endpos = datetime(2019, 2, 18, 10, 30, 0),
                )
            ]
        cal2.save()
        self.assertEqual(len(cal2.events), 1)
        self.assertEqual(cal2.events[0].name, 'Testevnt2')
        self.assertEqual(str(cal2.events[0].startpos), '2019-02-18 10:00:00')
        
        # count all events
        e3 = Event.search([])
        self.assertEqual(len(e3), 2)
        
        # check 'delete'
        # switch to 'Frida'
        with Transaction().set_user(cal1.owner.id):
            e1 = Event.search([])
            self.assertEqual(len(e1), 1)
            self.assertEqual(e1[0].name, 'Testevnt1')
            self.assertEqual(e1[0].permdelete, False)
            self.assertEqual(e1[0].owner, True)
            
            e2 = Event.search([('permdelete', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('permdelete', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 0)

        # switch to 'Diego'
        with Transaction().set_user(usr2.id):
            e1 = Event.search([], order=[('name', 'ASC')])
            self.assertEqual(len(e1), 2)
            self.assertEqual(e1[0].name, 'Testevnt1')
            self.assertEqual(e1[0].permdelete, True)
            self.assertEqual(e1[0].owner, False)
            self.assertEqual(e1[1].name, 'Testevnt2')
            self.assertEqual(e1[1].permdelete, False)
            self.assertEqual(e1[1].owner, True)
            
            e2 = Event.search([('permdelete', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')
            e2 = Event.search([('permdelete', 'in', [True])])
            self.assertEqual(len(e2), 1)
            e2 = Event.search([('permdelete', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt2')
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')

        # switch to 'John' - no access
        with Transaction().set_user(usr3.id):
            e1 = Event.search([], order=[('name', 'ASC')])
            self.assertEqual(len(e1), 0)
            
            e2 = Event.search([('permdelete', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('permdelete', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 0)

    @with_transaction()
    def test_events_permission_create(self):
        """ create event, calendar, visitors, check create permission
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')
        Visitor = pool.get('pim_calendar.visitor')
        # calendar 1
        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        
        # calendar 2
        usr2 = self.prep_events_newuser('Diego', 'PIM Calendar - User')
        cal2 = create_calendar('Test 2', usr2)
        self.assertEqual(cal2.name, 'Test 2')
        self.assertEqual(cal2.owner.name, 'Diego')

        usr3 = self.prep_events_newuser('John', 'PIM Calendar - User')
        
        # add visitor 'Diego' to calendar 1
        cal1.visitors = [
            Visitor(visitor=usr2,
                acccreate=True,
                )
            ]
        cal1.save()
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        self.assertEqual(cal1.visitors[0].accchange, False)
        self.assertEqual(cal1.visitors[0].accdelete, False)
        self.assertEqual(cal1.visitors[0].acccreate, True)

        # add event to calendar 1
        cal1.events = [
            Event(name='Testevnt1',
                startpos = datetime(2019, 2, 18, 10, 0, 0),
                endpos = datetime(2019, 2, 18, 10, 30, 0),
                )
            ]
        cal1.save()
        self.assertEqual(len(cal1.events), 1)
        self.assertEqual(cal1.events[0].name, 'Testevnt1')
        self.assertEqual(str(cal1.events[0].startpos), '2019-02-18 10:00:00')

        # add event to calendar 2
        cal2.events = [
            Event(name='Testevnt2',
                startpos = datetime(2019, 2, 18, 10, 0, 0),
                endpos = datetime(2019, 2, 18, 10, 30, 0),
                )
            ]
        cal2.save()
        self.assertEqual(len(cal2.events), 1)
        self.assertEqual(cal2.events[0].name, 'Testevnt2')
        self.assertEqual(str(cal2.events[0].startpos), '2019-02-18 10:00:00')
        
        # count all events
        e3 = Event.search([])
        self.assertEqual(len(e3), 2)
        
        # check 'create'
        # switch to 'Frida'
        with Transaction().set_user(cal1.owner.id):
            e1 = Event.search([])
            self.assertEqual(len(e1), 1)
            self.assertEqual(e1[0].name, 'Testevnt1')
            self.assertEqual(e1[0].permcreate, False)
            self.assertEqual(e1[0].owner, True)
            
            e2 = Event.search([('permcreate', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('permcreate', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 0)

        # switch to 'Diego'
        with Transaction().set_user(usr2.id):
            e1 = Event.search([], order=[('name', 'ASC')])
            self.assertEqual(len(e1), 2)
            self.assertEqual(e1[0].name, 'Testevnt1')
            self.assertEqual(e1[0].permcreate, True)
            self.assertEqual(e1[0].owner, False)
            self.assertEqual(e1[1].name, 'Testevnt2')
            self.assertEqual(e1[1].permcreate, False)
            self.assertEqual(e1[1].owner, True)
            
            e2 = Event.search([('permcreate', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')
            e2 = Event.search([('permcreate', 'in', [True])])
            self.assertEqual(len(e2), 1)
            e2 = Event.search([('permcreate', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt2')
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 1)
            self.assertEqual(e2[0].name, 'Testevnt1')

        # switch to 'John' - no access
        with Transaction().set_user(usr3.id):
            e1 = Event.search([], order=[('name', 'ASC')])
            self.assertEqual(len(e1), 0)
            
            e2 = Event.search([('permcreate', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('permcreate', '=', False)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', True)])
            self.assertEqual(len(e2), 0)
            e2 = Event.search([('owner', '=', False)])
            self.assertEqual(len(e2), 0)
    
    @with_transaction()
    def test_events_edit_startpos(self):
        """ check behavior of event if startpos is edited
        """
        Event = Pool().get('pim_calendar.event')
        
        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        
        dt1 = datetime(2019, 3, 15, 10, 0, 0)
        ev1 = Event(name='Ev1', 
            startpos=dt1, endpos=dt1 + timedelta(seconds=60), 
            calendar=cal1)
        ev1.save()
        
        ev_lst = Event.search([]) # get all
        self.assertEqual(len(ev_lst), 1)
        self.assertEqual(ev_lst[0].name, 'Ev1')
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 10:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 10:01:00')
        self.assertEqual(str(ev_lst[0].calendar.rec_name), 'Test 1 (Frida)')
        
        # move startpos forward, endpos should follow
        ev_lst[0].startpos = dt1 + timedelta(seconds=5 * 60)
        ev_lst[0].on_change_startpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 10:05:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 10:06:00')

        # move startpos backward, endpos should stay
        ev_lst[0].startpos = dt1 - timedelta(seconds=10 * 60)
        ev_lst[0].on_change_startpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 09:50:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 10:06:00')
        
    @with_transaction()
    def test_events_edit_endpos(self):
        """ check behavior of event if endpos is edited
        """
        Event = Pool().get('pim_calendar.event')
        
        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        
        dt1 = datetime(2019, 3, 15, 10, 0, 0)
        ev1 = Event(name='Ev1', 
            startpos=dt1, endpos=dt1 + timedelta(seconds=60), 
            calendar=cal1)
        ev1.save()
        
        ev_lst = Event.search([]) # get all
        self.assertEqual(len(ev_lst), 1)
        self.assertEqual(ev_lst[0].name, 'Ev1')
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 10:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 10:01:00')
        self.assertEqual(str(ev_lst[0].calendar.rec_name), 'Test 1 (Frida)')

        # move endpos forward, startpos should stay
        ev_lst[0].endpos = dt1 + timedelta(seconds=5 * 60)
        ev_lst[0].on_change_endpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 10:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 10:05:00')

        # move endpos backward, startpos should follow
        ev_lst[0].endpos = dt1 - timedelta(seconds=5 * 60)
        ev_lst[0].on_change_endpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 09:54:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 09:55:00')

    @with_transaction()
    def test_events_wholeday(self):
        """ check behavior of event in whole-day-mode
        """
        Event = Pool().get('pim_calendar.event')
        
        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        
        dt1 = datetime(2019, 3, 15, 10, 0, 0)
        ev1 = Event(name='Ev1', 
            startpos=dt1, endpos=dt1 + timedelta(seconds=60), 
            calendar=cal1,
            wholeday=True)
        ev1.save()
        
        ev_lst = Event.search([]) # get all
        self.assertEqual(len(ev_lst), 1)
        self.assertEqual(ev_lst[0].name, 'Ev1')
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 00:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 00:00:00')
        self.assertEqual(ev_lst[0].wholeday, True)
        self.assertEqual(str(ev_lst[0].calendar.rec_name), 'Test 1 (Frida)')

        # edit startpos, remains on same day, is moved back to '0:00:00'
        ev_lst[0].startpos = dt1 + timedelta(seconds=60 * 60)
        ev_lst[0].on_change_startpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-15 00:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-15 00:00:00')
        self.assertEqual(ev_lst[0].wholeday, True)

        # edit startpos, goto to next day
        ev_lst[0].startpos = dt1 + timedelta(seconds=18 * 60 * 60) # 4:00:00 at next day
        ev_lst[0].on_change_startpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-16 00:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-16 00:00:00')
        self.assertEqual(ev_lst[0].wholeday, True)

        # edit endpos 1
        ev_lst[0].endpos = ev_lst[0].endpos + timedelta(days=1)
        ev_lst[0].on_change_endpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-16 00:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-17 00:00:00')
        self.assertEqual(ev_lst[0].wholeday, True)

        # edit endpos 2
        ev_lst[0].endpos = ev_lst[0].endpos - timedelta(days=1)
        ev_lst[0].on_change_endpos()
        ev_lst[0].save()
        self.assertEqual(str(ev_lst[0].startpos), '2019-03-16 00:00:00')
        self.assertEqual(str(ev_lst[0].endpos), '2019-03-16 00:00:00')
        self.assertEqual(ev_lst[0].wholeday, True)

    @with_transaction()
    def test_events_days_data(self):
        """ check results of get_days_data
        """
        pool = Pool()
        Event = pool.get('pim_calendar.event')

        cal1 = self.prep_events_users_cal()
        self.assertEqual(cal1.owner.name, 'Frida')
        
        dt1 = datetime.now()
        ev1 = Event(name='Today', startpos=dt1, endpos=dt1 + timedelta(seconds=60), calendar=cal1)
        ev1.save()
        self.assertEqual(ev1.name, 'Today')
        self.assertEqual(ev1.dayss, 0)
        self.assertEqual(ev1.dayse, 0)
        self.assertEqual(ev1.weeks, 0)
        self.assertEqual(ev1.months, 0)
        self.assertEqual(ev1.years, 0)
        
        dt2 = datetime.now() - timedelta(seconds=60*60*24)
        ev2 = Event(name='yesterday', startpos=dt2, endpos=dt2 + timedelta(seconds=60), calendar=cal1)
        ev2.save()
        self.assertEqual(ev2.name, 'yesterday')
        self.assertEqual(ev2.dayss, -1)
        self.assertEqual(ev2.dayse, -1)
        self.assertEqual(ev2.weeks, 0)
        self.assertEqual(ev2.months, 0)
        self.assertEqual(ev2.years, 0)

        dt3 = datetime.now() - timedelta(seconds=60*60*24*35)
        ev3 = Event(name='35 days back', startpos=dt3, endpos=dt3 + timedelta(seconds=60), calendar=cal1)
        ev3.save()
        self.assertEqual(ev3.name, '35 days back')
        self.assertEqual(ev3.dayss, -35)
        self.assertEqual(ev3.dayse, -35)
        self.assertEqual(ev3.weeks, -5)
        self.assertTrue(ev3.months in [-1, -2])
        self.assertEqual(ev3.years, 0)

        dt4 = datetime.now() - timedelta(seconds=60*60*24*380)
        ev4 = Event(name='380 days back', startpos=dt4, endpos=dt4 + timedelta(seconds=60), calendar=cal1)
        ev4.save()
        self.assertEqual(ev4.name, '380 days back')
        self.assertEqual(ev4.dayss, -380)
        self.assertEqual(ev4.dayse, -380)
        self.assertEqual(ev4.weeks, -54)
        if dt4.month != datetime.now().month:
            self.assertEqual(ev4.months, -13)
        else :
            self.assertEqual(ev4.months, -12)
        self.assertEqual(ev4.years, -1)

        dt5 = datetime.now() + timedelta(seconds=60*60*24*6)
        ev5 = Event(name='6 days ahead', startpos=dt5, endpos=dt5 + timedelta(seconds=60), calendar=cal1)
        ev5.save()
        self.assertEqual(ev5.name, '6 days ahead')
        self.assertEqual(ev5.dayss, 6)
        self.assertEqual(ev5.dayse, 6)
        self.assertEqual(ev5.weeks, 0)
        if dt5.month != datetime.now().month:
            self.assertEqual(ev5.months, 1)
        else :
            self.assertEqual(ev5.months, 0)
        self.assertEqual(ev5.years, 0)

        dt6 = datetime.now() + timedelta(seconds=60*60*24*26)
        ev6 = Event(name='26 days ahead', startpos=dt6, endpos=dt6 + timedelta(seconds=60), calendar=cal1)
        ev6.save()
        self.assertEqual(ev6.name, '26 days ahead')
        self.assertEqual(ev6.dayss, 26)
        self.assertEqual(ev6.dayse, 26)
        self.assertEqual(ev6.weeks, 3)
        if dt6.month != datetime.now().month:
            self.assertEqual(ev6.months, 1)
        else :
            self.assertEqual(ev6.months, 0)
        self.assertEqual(ev6.years, 0)

        dt7 = datetime.now() + timedelta(seconds=60*60*24*370)
        ev7 = Event(name='370 days ahead', startpos=dt7, endpos=dt7 + timedelta(seconds=60), calendar=cal1)
        ev7.save()
        self.assertEqual(ev7.name, '370 days ahead')
        self.assertEqual(ev7.dayss, 370)
        self.assertEqual(ev7.dayse, 370)
        self.assertEqual(ev7.weeks, 52)
        if dt7.month != datetime.now().month:
            self.assertEqual(ev7.months, 13)
        else :
            self.assertEqual(ev7.months, 12)
        self.assertEqual(ev7.years, 1)
        
        s1 = Event.search([('dayss', '>=', 0), ('dayss', '<', 7)], order=[('startpos', 'DESC')])
        self.assertEqual(len(s1), 2)
        self.assertEqual(s1[0].name, '6 days ahead')
        self.assertEqual(s1[1].name, 'Today')

        s2 = Event.search([('weeks', '>', 1), ('weeks', '<', 6)], order=[('startpos', 'ASC')])
        self.assertEqual(len(s2), 1)
        self.assertEqual(s2[0].name, '26 days ahead')

        s3 = Event.search([('months', '>=', 0), ('months', '<', 2)], order=[('startpos', 'ASC')])
        self.assertEqual(len(s3), 4)
        self.assertEqual(s3[0].name, 'yesterday')   # current month
        self.assertEqual(s3[1].name, 'Today')
        self.assertEqual(s3[2].name, '6 days ahead')
        self.assertEqual(s3[3].name, '26 days ahead')

        s4 = Event.search([('years', '=', 1)], order=[('startpos', 'ASC')])
        self.assertEqual(len(s4), 1)
        self.assertEqual(s4[0].name, '370 days ahead')

        ev2 = Event(name='Ev2', 
                startpos=datetime(2019, 3, 15, 10, 0, 0, 0), 
                endpos=datetime(2019, 3, 15, 11, 45, 0), 
                calendar=cal1
            )
        ev2.save()
        self.assertEqual(str(ev2.startpos), '2019-03-15 10:00:00')
        self.assertEqual(str(ev2.endpos), '2019-03-15 11:45:00')
        self.assertEqual(str(ev2.startday), '2019-03-15')
        self.assertEqual(str(ev2.endday), '2019-03-15')

# end EventsTestCase
