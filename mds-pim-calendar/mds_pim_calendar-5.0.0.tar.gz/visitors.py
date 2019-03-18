# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

# one or more calendar per Tryton user
# contains events
# can be visible/editable to owner/selected user/group/world (by permission)


from trytond.model import ModelView, ModelSQL, fields, Unique, Check
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval, Id


__all__ = ['Visitor']
__metaclass__ = PoolMeta


class Visitor(ModelSQL, ModelView):
    'Visitor'
    __name__ = 'pim_calendar.visitor'

    calendar = fields.Many2One(string=u'Calendar', 
        help=u'Calendar to which the visitor have permissions',
        required=True, select=True, ondelete='CASCADE',
        model_name='pim_calendar.calendar')
    visitor = fields.Many2One(string=u'Visitor', 
        help=u'User, who can see or edit the calendar',
        required=True, select=True, ondelete='CASCADE',
        model_name='res.user', depends=['visitors'],
        domain=[
                ('id', 'in', Eval('visitors', [])),
                ['OR',
                    ('groups', '=', Id('pim_calendar', 'group_calendar_admin')),
                    ('groups', '=', Id('pim_calendar', 'group_calendar_user')),
                ],
            ])
    accchange = fields.Boolean(string=u'Change', help=u'The user can change existing appointments.')
    acccreate = fields.Boolean(string=u'Create', help=u'The user can create appointments.')
    accdelete = fields.Boolean(string=u'Delete', help=u'The user can delete appointments.')
    
    # views
    visitors = fields.Function(fields.One2Many(string=u'Visitors', readonly=True, field=None,
        model_name='res.user', states={'invisible': True}), 'on_change_with_visitors')

    @classmethod
    def __setup__(cls):
        super(Visitor, cls).__setup__()
        tab_vis = cls.__table__()
        cls._sql_constraints.extend([
            ('uniq_visit', 
            Unique(tab_vis, tab_vis.calendar, tab_vis.visitor), 
            u'This visitor in already on this calendar.'),
            ])

    @classmethod
    def default_accchange(cls):
        return False
        
    @classmethod
    def default_acccreate(cls):
        return False

    @classmethod
    def default_accdelete(cls):
        return False

    @fields.depends('calendar')
    def on_change_with_visitors(self, name=None):
        """ get list of allowed visitors
        """
        User = Pool().get('res.user')
        
        if isinstance(self.calendar, type(None)):
            u_lst = User.search([
                ('id', '!=', Transaction().user)
                ])
        else :
            u_lst = User.search([
                ('id', '!=', self.calendar.owner.id),
                ])
        return [x.id for x in u_lst]

    @classmethod
    def create(cls, vlist):
        CalendarSettings = Pool().get('pim_calendar.calendar_setting')
        
        r1 = super(Visitor, cls).create(vlist)

        # add calendar-settings
        for i in r1:
            CalendarSettings.add_cal_settings(i.visitor.id, i.calendar.id)
        return r1

# end Visitor
