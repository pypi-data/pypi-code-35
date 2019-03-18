# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


from trytond.model import ModelView, ModelSQL, fields, Unique, Check
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval, Or, Id
from sql.conditionals import Coalesce, Case
from sql.functions import DateTrunc, DatePart, CurrentDate, Trunc, Extract
from sql import Cast
from datetime import datetime, timedelta, date
import icalendar


__all__ = ['Event']
__metaclass__ = PoolMeta


class Event(ModelSQL, ModelView):
    'Event'
    __name__ = 'pim_calendar.event'

    states_ro = {
        'readonly': ~Or(
                Eval('id', -1) < 0,
                Eval('owner', False) == True,
                Eval('permchange', False) == True,
                Id('pim_calendar', 'group_calendar_admin').in_(Eval('context', {}).get('groups', []))
            )
        }
    calendar = fields.Many2One(string=u'Calendar', required=True, select=True, 
        help=u'Calendar to which the event belongs', ondelete='CASCADE', 
        depends=['owner', 'permchange'],
        model_name='pim_calendar.calendar', states=states_ro)
    name = fields.Char(string='Title', required=True, select=True, states=states_ro,
        depends=['owner', 'permchange'])
    location = fields.Char(string='Location', states=states_ro,
        depends=['owner', 'permchange'])
    note = fields.Text(string='Note', states=states_ro,
        depends=['owner', 'permchange'])
    startpos = fields.DateTime(string=u'Begin', required=True, select=True, states=states_ro,
        depends=['owner', 'permchange'])
    endpos = fields.DateTime(string=u'End', required=True, select=True, states=states_ro,
        depends=['owner', 'permchange'])
    wholeday = fields.Boolean(string=u'Whole Day', states=states_ro)
    
    # permissions for visitors, owner has full access
    owner = fields.Function(fields.Boolean(string=u'Owner', 
        readonly=True, help=u'Permission: full access - for current user'), 
        'get_permissions', searcher='search_owner')
    permchange = fields.Function(fields.Boolean(string=u'Permission: Change', 
        readonly=True, help=u'Permission: change - for current visitor'), 
        'get_permissions', searcher='search_permchange')
    permcreate = fields.Function(fields.Boolean(string=u'Permission: Create', 
        readonly=True, help=u'Permission: create - for current visitor'), 
        'get_permissions', searcher='search_permcreate')
    permdelete = fields.Function(fields.Boolean(string=u'Permission: Delete', 
        readonly=True, help=u'Permission: delete - for current visitor'), 
        'get_permissions', searcher='search_permdelete')
    
    # views
    dayss = fields.Function(fields.Integer(string=u'Days start', readonly=True), 
        'get_days_data', searcher='search_dayss')
    dayse = fields.Function(fields.Integer(string=u'Days end', readonly=True), 
        'get_days_data', searcher='search_dayse')
    weeks = fields.Function(fields.Integer(string=u'Weeks', readonly=True), 
        'get_days_data', searcher='search_weeks')
    months = fields.Function(fields.Integer(string=u'Months', readonly=True), 
        'get_days_data', searcher='search_months')
    years = fields.Function(fields.Integer(string=u'Years', readonly=True), 
        'get_days_data', searcher='search_years')
    startday = fields.Function(fields.Date(string=u'Begin', readonly=True),
        'get_days_data', searcher='search_startday')
    endday = fields.Function(fields.Date(string=u'End', readonly=True), 
        'get_days_data', searcher='search_endday')

    # colors, texts
    bgcolor = fields.Function(fields.Char(string='Color', readonly=True), 
        'on_change_with_bgcolor')
    location_lim = fields.Function(fields.Char(string='Location', readonly=True), 
        'on_change_with_location_lim')
    name_lim = fields.Function(fields.Char(string='Name', readonly=True), 
        'on_change_with_name_lim')
    calendar_name = fields.Function(fields.Char(string='Calendar', readonly=True), 
        'on_change_with_calendar_name')
    
    @classmethod
    def __setup__(cls):
        super(Event, cls).__setup__()
        tab_event = cls.__table__()
        cls._order.insert(0, ('name', 'ASC'))
        cls._order.insert(0, ('startpos', 'DESC'))
        cls._sql_constraints.extend([
            ('order_time', 
            Check(tab_event, 
                ((tab_event.startpos < tab_event.endpos) & (tab_event.wholeday == False)) |\
                ((tab_event.startpos <= tab_event.endpos) & (tab_event.wholeday == True))), 
            u'The end must be after the beginning.'),
            ])
        cls._error_messages.update({
            'event_import_noend': (u"The event '%s' has no valid end time and was not imported."),
            })

    @classmethod
    def view_attributes(cls):
        return super(Event, cls).view_attributes() + [
                ('//group[@id="startpos1"]', 'states', {'invisible': Eval('wholeday', False),}),
                ('//group[@id="startpos2"]', 'states', {'invisible': ~Eval('wholeday', False),}),
                ('//group[@id="endpos1"]', 'states', {'invisible': Eval('wholeday', False),}),
                ('//group[@id="endpos2"]', 'states', {'invisible': ~Eval('wholeday', False),}),
            ]

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('name',) + tuple(clause[1:]),]

    def get_rec_name(self, name):
        """ create rec_name
        """
        t1 = '-'
        d1 = '-'
        d2 = '-'
        if not isinstance(self.name, type(None)):
            t1 = self.name
        if not isinstance(self.startpos, type(None)):
            d1 = self.startpos.strftime('%d.%m.%Y %H:%M')
        if not isinstance(self.endpos, type(None)):
            if (self.startpos.year == self.endpos.year) and \
                (self.startpos.month == self.endpos.month) and \
                (self.startpos.day == self.endpos.day):
                d2 = self.endpos.strftime('%H:%M')
            else :
                d2 = self.endpos.strftime('%d.%m.%Y %H:%M')
        c1 = '-/-'
        if not isinstance(self.calendar, type(None)):
            c1 = self.calendar.rec_name
        return '%s - %s - %s (%s)' % (t1, d1, d2, c1)

    @classmethod
    def get_calendarlst(cls):
        """ get default calendars
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        ModelData = pool.get('ir.model.data')
        trans1 = Transaction()
        
        id_user = trans1.user
        context = trans1.context
        
        id_grp = ModelData.get_id('pim_calendar', 'group_calendar_admin')
        
        if (id_grp in context.get('groups', [])) or \
            (len(context.get('groups', [])) == 0):
            # admin gets all calendars
            c_lst = Calendar.search([], order=[('name', 'ASC')])
        else :
            # find a calendar owned by current user
            c_lst = Calendar.search([
                        ('owner.id', '=', id_user),
                    ], order=[('name', 'ASC')])
            # add calendars with edit/create-permission of other users
            c_lst.extend(Calendar.search([
                        ('visitors.visitor.id', '=', id_user),
                        ['OR', 
                            ('visitors.acccreate', '=', True),
                            ('visitors.accchange', '=', True),
                            ('visitors.accdelete', '=', True),
                        ]
                    ], order=[('name', 'ASC')])
                )
        return [x.id for x in c_lst]

    @classmethod
    def default_startpos(cls):
        """ set to now
        """
        return datetime.now()

    @classmethod
    def default_endpos(cls):
        """ set to now + 30 min
        """
        return datetime.now() + timedelta(seconds=60 * 30)

    @classmethod
    def default_calendar(cls):
        """ get writable calendar
        """
        cal_lst = cls.get_calendarlst()

        if len(cal_lst) > 0:
            return cal_lst[0]
        else :
            return None

    def limit_textlength(self, text):
        if not isinstance(text, type(None)):
            if not isinstance(self.calendar, type(None)):
                if (self.calendar.cal_limittext == True) and \
                    (len(text) > self.calendar.cal_limitanz):
                        return text[:self.calendar.cal_limitanz - 1] + '*'

            return text
        else :
            return None

    @classmethod
    def default_wholeday(cls):
        return False

    @fields.depends('calendar')
    def on_change_with_calendar_name(self, name=None):
        if isinstance(self.calendar, type(None)):
            return None
        return self.calendar.name_lim

    @fields.depends('location', 'calendar')
    def on_change_with_location_lim(self, name=None):
        return self.limit_textlength(self.location)

    @fields.depends('name', 'calendar')
    def on_change_with_name_lim(self, name=None):
        return self.limit_textlength(self.name)

    @fields.depends('calendar')
    def on_change_with_bgcolor(self, name=None):
        Calendar = Pool().get('pim_calendar.calendar')
        if isinstance(self.calendar, type(None)):
            return Calendar.default_cal_color()
        else :
            if isinstance(self.calendar.cal_color, type(None)):
                return Calendar.default_cal_color()
            return self.calendar.cal_color

    @fields.depends('wholeday', 'startpos', 'endpos')
    def on_change_wholeday(self):
        """ at 'wholeday'=True - set time to 0
        """
        Event = Pool().get('pim_calendar.event')
        
        if (not isinstance(self.startpos, type(None))) and \
            (not isinstance(self.endpos, type(None))) and \
            (not isinstance(self.wholeday, type(None))):
            if self.wholeday == True:
                self.startpos = Event.setdate_wholeday(self.startpos)
                self.endpos = Event.setdate_wholeday(self.endpos)

    @fields.depends('startpos', 'endpos', 'wholeday')
    def on_change_startpos(self):
        """ update endpos
        """
        if (not isinstance(self.startpos, type(None))) and \
            (not isinstance(self.endpos, type(None))):
            if self.startpos >= self.endpos:
                self.endpos = self.startpos + timedelta(seconds=60)
            self.on_change_wholeday()

    @fields.depends('startpos', 'endpos', 'wholeday')
    def on_change_endpos(self):
        """ update startpos
        """
        if (not isinstance(self.startpos, type(None))) and \
            (not isinstance(self.endpos, type(None))):
            if self.startpos >= self.endpos:
                if self.wholeday == False:
                    self.startpos = self.endpos - timedelta(seconds=60)
                else :
                    self.startpos = self.endpos
            self.on_change_wholeday()

    @classmethod
    def setdate_wholeday(cls, dtime):
        """ set time of 'datetime' to '0:00:00'
        """
        if isinstance(dtime, type(None)):
            return None
        return datetime(dtime.year, dtime.month, dtime.day, 0, 0, 0)
        
    @classmethod
    def get_permissions_sql(cls):
        """ get sql code to search for write-users
        """
        pool = Pool()
        Visitor = pool.get('pim_calendar.visitor')
        Calendar = pool.get('pim_calendar.calendar')
        
        tab_vis = Visitor.__table__()
        tab_cal = Calendar.__table__()
        tab_event = cls.__table__()

        # get list of users and events, having change permission
        qu1 = tab_event.join(tab_cal, condition=tab_cal.id==tab_event.calendar
            ).join(tab_vis, 
                condition=tab_vis.calendar==tab_cal.id,
                type_ = 'LEFT OUTER'
            ).select(tab_event.id.as_('id_event'),
                tab_cal.owner.as_('id_owner'),
                Coalesce(tab_vis.visitor, None).as_('id_user'),
                Coalesce(tab_vis.accchange, False).as_('permchange'),
                Coalesce(tab_vis.accdelete, False).as_('permdelete'),
                Coalesce(tab_vis.acccreate, False).as_('permcreate'),
            )
        return qu1

    @classmethod
    def search_owner(cls, name, clause):
        """ get owner for current user
        """
        tab_evnt = cls.get_permissions_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]
        id_user = Transaction().user

        qu1 = tab_evnt.select(tab_evnt.id_event,
                Case (
                    (id_user == tab_evnt.id_owner, True),
                    else_ = False
                ).as_('is_owner'),
            )
        qu2 = qu1.select(qu1.id_event,
                where=Operator(qu1.is_owner, clause[2])
            )
        return [('id', 'in', qu2)]

    @classmethod
    def search_permchange(cls, name, clause):
        """ get change-permission for current user
        """
        tab_evnt = cls.get_permissions_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]
        id_user = Transaction().user

        qu1 = tab_evnt.select(tab_evnt.id_event,
                where=Operator(tab_evnt.permchange, clause[2]) & \
                       (tab_evnt.id_user == id_user)
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_permcreate(cls, name, clause):
        """ get create-permission for current user
        """
        tab_evnt = cls.get_permissions_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]
        id_user = Transaction().user

        qu1 = tab_evnt.select(tab_evnt.id_event,
                where=Operator(tab_evnt.permcreate, clause[2]) &\
                    (tab_evnt.id_user == id_user)
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_permdelete(cls, name, clause):
        """ get delete-permission for current user
        """
        tab_evnt = cls.get_permissions_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]
        id_user = Transaction().user

        qu1 = tab_evnt.select(tab_evnt.id_event,
                where=Operator(tab_evnt.permdelete, clause[2]) &\
                    (tab_evnt.id_user == id_user)
            )
        return [('id', 'in', qu1)]

    @classmethod
    def get_permissions(cls, events, names):
        """ get permissions of current user
        """
        res1 = {'permchange': {}, 'permcreate': {}, 'permdelete': {}, 'owner': {}}
        id_lst = [x.id for x in events]
        trans1 = Transaction()
        cursor = trans1.connection.cursor()
        tab_evnt = cls.get_permissions_sql()

        for i in id_lst:
            res1['permchange'][i] = False
            res1['permcreate'][i] = False
            res1['permdelete'][i] = False
            res1['owner'][i] = False
            
        if ('permchange' in names) or ('permcreate' in names) or \
            ('permdelete' in names):
            qu1 = tab_evnt.select(tab_evnt.id_event,
                    tab_evnt.permchange,
                    tab_evnt.permcreate,
                    tab_evnt.permdelete,
                    where=tab_evnt.id_event.in_(id_lst) & \
                        (tab_evnt.id_user == trans1.user)
                )
            cursor.execute(*qu1)
            l1 = cursor.fetchall()
    
            for i in l1:
                (id_evnt, permch, permcr, permdel) = i
                res1['permchange'][id_evnt] = permch
                res1['permcreate'][id_evnt] = permcr
                res1['permdelete'][id_evnt] = permdel

        # owner
        qu2 = tab_evnt.select(tab_evnt.id_event,
                Case (
                    (tab_evnt.id_owner == trans1.user, True),
                    else_ = False
                ).as_('owner'),
                where=tab_evnt.id_event.in_(id_lst),
                group_by=[tab_evnt.id_event, tab_evnt.id_owner]
            )
        cursor.execute(*qu2)
        l2 = cursor.fetchall()

        for i in l2:
            (id_evnt, owner) = i
            res1['owner'][id_evnt] = owner

        res2 = {}
        for i in names:
            res2[i] = res1[i]
        return res2

    @classmethod
    def get_days_data_sql(cls):
        """ sql-code
            days/weeks/month: current = 0, last = 1, ...
        """
        tab_event = cls.__table__()
        q1 = tab_event.select(tab_event.id.as_('id_event'),
            Cast(
                Extract('days',
                    DateTrunc('day', Coalesce(tab_event.startpos, CurrentDate())) -
                    CurrentDate()
                ),
                'integer'
            ).as_('dayss'), # days-start
            Cast(
                Extract('days',
                    DateTrunc('day', Coalesce(tab_event.endpos, CurrentDate())) -
                    CurrentDate()
                ),
                'integer'
            ).as_('dayse'), # days-end
            Cast(
                Trunc(
                    Extract('days', 
                        DateTrunc('day', Coalesce(tab_event.startpos, CurrentDate())) -
                        CurrentDate()
                    ) / 7.0
                ), 'integer'
            ).as_('weeks'),
            Cast(
                DatePart('year',  Coalesce(tab_event.startpos, CurrentDate())) -
                DatePart('year',  CurrentDate()),
                'integer').as_('years'),
            Cast(
                (DatePart('year', Coalesce(tab_event.startpos, CurrentDate())) - 
                 DatePart('year', CurrentDate())) * 12 + 
                (DatePart('month', Coalesce(tab_event.startpos, CurrentDate())) - 
                 DatePart('month', CurrentDate())),
                'integer').as_('months'),
            Cast(DateTrunc('day', tab_event.startpos), 'date').as_('startday'),
            Cast(DateTrunc('day', tab_event.endpos), 'date').as_('endday'),
            )
        return q1

    @classmethod
    def get_days_data(cls, events, names):
        """ get relative number of day/week/month/year
            cuttent = 0, last = 1, ...
        """
        r1 = {
                'dayss': {}, 'dayse': {},
                'weeks':{}, 'months':{}, 'years': {}, 
                'startday':{}, 'endday': {}
            }
        cursor = Transaction().connection.cursor()
        
        sql1 = cls.get_days_data_sql()
        qu2 = sql1.select(sql1.id_event, 
                    sql1.dayss,
                    sql1.dayse,
                    sql1.weeks,
                    sql1.months,
                    sql1.years,
                    sql1.startday, 
                    sql1.endday,
                    where=sql1.id_event.in_([x.id for x in events])
                )
        cursor.execute(*qu2)
        l2 = cursor.fetchall()
        
        for i in l2:
            (id1, ds1, de1, w1, m1, y1, sd1, ed1) = i
            r1['dayss'][id1] = ds1
            r1['dayse'][id1] = de1
            r1['weeks'][id1] = w1
            r1['months'][id1] = m1
            r1['years'][id1] = y1
            r1['startday'][id1] = sd1
            r1['endday'][id1] = ed1
        
        r2 = {}
        for i in names:
            r2[i] = r1[i]
        return r2

    @classmethod
    def search_startday(cls, name, clause):
        """ search in startday
        """
        sql1 = cls.get_days_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = sql1.select(sql1.id_event,
                where=Operator(sql1.startday, clause[2])
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_endday(cls, name, clause):
        """ search in endday
        """
        sql1 = cls.get_days_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = sql1.select(sql1.id_event,
                where=Operator(sql1.endday, clause[2])
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_dayss(cls, name, clause):
        """ search in days-start
        """
        sql1 = cls.get_days_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = sql1.select(sql1.id_event,
                where=Operator(sql1.dayss, clause[2])
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_dayse(cls, name, clause):
        """ search in days-end
        """
        sql1 = cls.get_days_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = sql1.select(sql1.id_event,
                where=Operator(sql1.dayse, clause[2])
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_weeks(cls, name, clause):
        """ search in weeks
        """
        sql1 = cls.get_days_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = sql1.select(sql1.id_event,
                where=Operator(sql1.weeks, clause[2])
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_months(cls, name, clause):
        """ search in months
        """
        sql1 = cls.get_days_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = sql1.select(sql1.id_event,
                where=Operator(sql1.months, clause[2])
            )
        return [('id', 'in', qu1)]

    @classmethod
    def search_years(cls, name, clause):
        """ search in years
        """
        sql1 = cls.get_days_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        qu1 = sql1.select(sql1.id_event,
                where=Operator(sql1.years, clause[2])
            )
        return [('id', 'in', qu1)]

    @classmethod
    def ical_add_event(cls, calendar, event):
        """ create event in selected calendar from icalendar.Event()
        """

        def get_datetime(dtval, fulld):
            if type(dtval) == type(date(2000, 1, 1)):
                dtval = datetime(dtval.year, dtval.month, dtval.day, 0, 0, 0)
                fulld = True
            return (dtval, fulld)

        Event = Pool().get('pim_calendar.event')

        if not type(event) == type(icalendar.Event()):
            raise ValueError("wrong type of event, expected 'icalendar.Event()', got '%s'" % \
                str(type(event)))

        fullday = False
        (dt_start, fullday) = get_datetime(event['DTSTART'].dt, fullday)
        if 'DTEND' in event.keys():
            (dt_end, fullday) = get_datetime(event['DTEND'].dt, fullday)
        elif 'DURATION' in event.keys():
            (dt_end, fullday) = get_datetime(event['DTSTART'].dt + event['DURATION'].dt, fullday)
        else :
            cls.raise_user_error('event_import_noend', (event['SUMMARY']))

        # if whole-day=true: endpos is at next day
        # we store this at same day and mark the event as 'wholeday=True'
        if (fullday == True) and (dt_end >= (dt_start + timedelta(days=1))):
            dt_end = dt_end - timedelta(days=1)

        ev1 = Event(
                calendar = calendar,
                name = event['SUMMARY'],
                startpos = dt_start,
                endpos = dt_end,
                note = event.get('DESCRIPTION', None),
                wholeday = fullday
            )
        ev1.save()
        return ev1

    @classmethod
    def create(cls, vlist):
        """ create item
        """
        vlist = [x.copy() for x in vlist]
        for values in vlist:

            if 'wholeday' in values:
                if values['wholeday'] == True:
                    if 'startpos' in values:
                        values['startpos'] = cls.setdate_wholeday(values['startpos'])
                    if 'endpos' in values:
                        values['endpos'] = cls.setdate_wholeday(values['endpos'])

        return super(Event, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        """ write item
        """
        actions = iter(args)
        for items, values in zip(actions, actions):

            if 'wholeday' in values:
                if values['wholeday'] == True:
                    if 'startpos' in values:
                        values['startpos'] = cls.setdate_wholeday(values['startpos'])
                    if 'endpos' in values:
                        values['endpos'] = cls.setdate_wholeday(values['endpos'])

        super(Event, cls).write(*args)

# end Event
