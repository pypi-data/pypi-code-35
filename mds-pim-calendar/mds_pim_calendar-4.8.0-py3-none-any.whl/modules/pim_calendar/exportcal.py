# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.report import Report
from datetime import date
import zipfile
from io import BytesIO


__all__ = ['ExportCalendar']


class ExportCalendar(Report):
    __name__ = 'pim_calendar.export_calendar'

    @classmethod
    def cleanuptags(cls, text):
        """ delete critical chars
        """
        t1 = ''
        for i in text:
            if i in '0123456789abcdefghijklmnopqrstuvwxyz.ABCDEFGHIJKLMNOPQRSTUVWXYZ-':
                t1 += i
            else :
                t1 += u'-'
        return t1

    @classmethod
    def execute(cls, ids, data):
        """ create file name
        """
        pool = Pool()
        Calendar = pool.get('pim_calendar.calendar')

        # compress file
        content = BytesIO()
        with zipfile.ZipFile(content, 'w') as content_zip:
            for i in ids:
                cal1 = Calendar(i)
                fname = '%s-calendar-%s.ics' % \
                    (
                        date.today().strftime('%Y%m%d'), 
                        cls.cleanuptags(cal1.rec_name)
                    )
                # get ical
                ical_txt = Calendar.ical_data_write(cal1)
                content_zip.writestr(fname, ical_txt)
        content = content.getvalue()

        title = '%s-calendar' % date.today().strftime('%Y%m%d')
        return ('zip', content, False, title)
# ende ExportCalendar
