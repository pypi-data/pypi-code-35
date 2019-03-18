# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from .testlib import create_calendar, create_user


class VisitorsTestCase(ModuleTestCase):
    'Test visitors module'
    module = 'pim_calendar'

    def prep_visitor_newuser(self, name, group):
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
    def test_visitors_create_item(self):
        """ create visitor object
        """
        Visitor = Pool().get('pim_calendar.visitor')
        
        usr1 = self.prep_visitor_newuser('Frida', 'PIM Calendar - User')
        usr2 = self.prep_visitor_newuser('Diego', 'PIM Calendar - User')
        self.assertEqual(usr2.name, 'Diego')
        
        cal1 = create_calendar('Test 1', usr1)
        self.assertEqual(cal1.name, 'Test 1')
        self.assertEqual(cal1.owner.name, 'Frida')

        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=True,
                )
            ]
        cal1.save()

        v_lst = Visitor.search([])
        self.assertEqual(len(v_lst), 1)
        self.assertEqual(v_lst[0].calendar.name, 'Test 1')
        self.assertEqual(v_lst[0].visitor.name, 'Diego')

    @with_transaction()
    def test_visitors_same_visitor(self):
        """ create visitor object, add same user twice, check contrains
        """
        Visitor = Pool().get('pim_calendar.visitor')
        
        usr1 = self.prep_visitor_newuser('Frida', 'PIM Calendar - User')
        usr2 = self.prep_visitor_newuser('Diego', 'PIM Calendar - User')
        self.assertEqual(usr2.name, 'Diego')
        
        cal1 = create_calendar('Test 1', usr1)
        self.assertEqual(cal1.name, 'Test 1')
        self.assertEqual(cal1.owner.name, 'Frida')

        cal1.visitors = [
            Visitor(visitor=usr2,
                accchange=True,
                )
            ]
        cal1.save()
        self.assertEqual(len(cal1.visitors), 1)
        self.assertEqual(cal1.visitors[0].calendar.name, 'Test 1')
        self.assertEqual(cal1.visitors[0].visitor.name, 'Diego')
        self.assertEqual(cal1.visitors[0].accchange, True)
        self.assertEqual(cal1.visitors[0].acccreate, False)
        self.assertEqual(cal1.visitors[0].accdelete, False)

        v_lst = list(cal1.visitors)
        v_lst.append(Visitor(visitor=usr2, accchange=True))
        cal1.visitors = v_lst
        self.assertRaisesRegex(UserError,
            "This visitor in already on this calendar.",
            cal1.save)

    @with_transaction()
    def test_visitors_add_owner(self):
        """ create visitor object, add owner, check contrains
        """
        Visitor = Pool().get('pim_calendar.visitor')
        
        usr1 = create_user('Frida', 'frida', 'Test.1234')
        self.assertEqual(usr1.name, 'Frida')
        
        cal1 = create_calendar('Test 1', usr1)
        self.assertEqual(cal1.name, 'Test 1')
        self.assertEqual(cal1.owner.name, 'Frida')

        cal1.visitors = [
            Visitor(visitor=usr1,
                accchange=True,
                )
            ]
        self.assertRaisesRegex(UserError,
            'The value of the field "Visitor" on "Visitor" is not valid according to its domain.',
            cal1.save)

# end VisitorsTestCase
