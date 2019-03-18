# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval

__all__ = ['EventImportWizardStart', 'EventImportWizard']


class EventImportWizardStart(ModelView):
    'Import events from ics - start'
    __name__ = 'pim_calendar.wiz_import_event.start'

    icsfile = fields.Binary(string="*.ics-File", required=True,
        help='The iCalendar-records in this *.ics-file are imported into the current calendar.')
    calendar = fields.Many2One(string="Calendar", readonly=True,
        help="The events are imported into this calendar.", 
        model_name='pim_calendar.calendar')
    
# end EventImportWizardStart


class EventImportWizard(Wizard):
    'Import events from ics'
    __name__ = 'pim_calendar.wiz_import_event'
    
    start_state = 'start'
    start = StateView(model_name='pim_calendar.wiz_import_event.start', \
            view='pim_calendar.import_wizard_start_form', \
            buttons=[
                Button(string=u'Cancel', state='end', icon='tryton-cancel'), 
                Button(string=u'Import', state='importevents', icon='tryton-save',
                    states={
                        'readonly': Eval('icsfile', '').in_([None, '']),
                    }),
                ])
    importevents = StateTransition()

    @classmethod
    def __setup__(cls):
        super(EventImportWizard, cls).__setup__()
        cls._error_messages.update({
            'wizimp_wrongmodel': (u"Please use the ics-import with a calendar."),
            'wizimp_selectcal': (u"Please select (only) a calendar."),
            'wizimp_nofile': (u"Please select a file to import."),
            })

    def transition_importevents(self):
        """ import from ics-file
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')
        Event = pool.get('pim_calendar.event')
        
        if isinstance(self.start.icsfile, type(None)):
            self.raise_user_error('wizimp_nofile')
        elif len(self.start.icsfile) == 0:
            self.raise_user_error('wizimp_nofile')
            
        ical1 = Calendar.ical_data_read(self.start.icsfile)
        for i in ical1.walk('VEVENT'):
            Event.ical_add_event(self.start.calendar, i)
        return 'end'

    def default_start(self, fields):
        """ fill form
        """
        Calendar = Pool().get('pim_calendar.calendar')
        context = Transaction().context
        
        if context['active_model'] != 'pim_calendar.calendar':
            self.raise_user_error('wizimp_wrongmodel')

        cal1 = Calendar.browse(context['active_ids'])
        if len(cal1) != 1:
            self.raise_user_error('wizimp_selectcal')

        r1 = {}
        tr1 = Transaction()
        r1['icsfile'] = ''
        r1['calendar'] = cal1[0].id
        return r1

# end EventImportWizard
