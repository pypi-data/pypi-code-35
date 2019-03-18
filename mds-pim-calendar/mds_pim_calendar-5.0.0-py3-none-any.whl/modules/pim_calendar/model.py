# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import MultiValueMixin, ValueMixin, fields, Unique
from trytond.transaction import Transaction

__all__ = ['CalendarMultiValueMixin', 'CalendarValueMixin']


class CalendarMultiValueMixin(MultiValueMixin):

    def updt_multivalue_pattern(self, pattern):
        """ add values to pattern
        """
        pattern.setdefault('calendar', self.id)
        pattern.setdefault('iduser', Transaction().user)
        return pattern

    def get_multivalue(self, name, **pattern):
        Value = self.multivalue_model(name)
        if issubclass(Value, CalendarValueMixin):
            pattern = self.updt_multivalue_pattern(pattern)
        return super(CalendarMultiValueMixin, self).get_multivalue(name, **pattern)

    def set_multivalue(self, name, value, **pattern):
        Value = self.multivalue_model(name)
        if issubclass(Value, CalendarValueMixin):
            pattern = self.updt_multivalue_pattern(pattern)
        return super(CalendarMultiValueMixin, self).set_multivalue(name, value, **pattern)

# end CalendarMultiValueMixin


class CalendarValueMixin(ValueMixin):
    iduser = fields.Many2One(model_name='res.user', string="User", 
        select=True, ondelete='CASCADE', required=True)
    calendar = fields.Many2One(model_name='pim_calendar.calendar', string="Calendar", 
        select=True, ondelete='CASCADE', required=True)

    @classmethod
    def __setup__(cls):
        super(CalendarValueMixin, cls).__setup__()
        tab_calval = cls.__table__()
        cls._sql_constraints.extend([
            ('calval_uniq', 
            Unique(tab_calval, tab_calval.iduser, tab_calval.calendar), 
            u'Calendar settings are already exists for this user and calendar'),
            ])

# end CalendarValueMixin

