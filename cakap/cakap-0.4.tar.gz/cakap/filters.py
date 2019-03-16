__author__ = ('Imam Omar Mochtar', ('iomarmochtar@gmail.com',))

import re
from datetime import datetime

class FilterNotFound(Exception):
    pass

class FilterNotMatch(Exception):
    pass


def filter_wrapper(wfilter):
    """
    agar filter bisa mempunyai argumen/parameter
    """
    def callme(**params):
        def injector(*args, **kwargs):
            kwargs['params'] = params
            return wfilter(*args, **kwargs)
        return injector 
    return callme


class Filters(object):

    __register = [
        'NUMBER',
        'DB_DATE',
        'TEXT'
    ]

    def f_number(self, argnum, args, params):
        txt = args[argnum]
        prefix = params.get('prefix', None)
        if prefix:
            ptrn = re.search(r'^\d+(\w)$', txt)

            if ptrn and ptrn.group(1) in prefix:
                txt = txt.replace( ptrn.group(1),  prefix[ptrn.group(1)] )

        if not txt.isdigit():
            raise FilterNotMatch('{} is not a number'.format(txt)) 
        return txt

    def f_text(self, argnum, args, params):
        """
        Join all arguments to the rest of line
        """
        return ' '.join(args[argnum:])

    def f_db_date(self, argnum, args, params):
        tgl = args[argnum]
        date_format = params.get('format', '%Y-%m-%d')

        if params.get('allow_now') and tgl == 'now':
            tgl = datetime.now() 
        else:
            try:
                tgl = datetime.strptime(tgl, date_format)
            except ValueError:
                raise FilterNotMatch('{} is not a valid date'.format(tgl)) 

        return tgl if params.get('convert') else tgl.strftime(date_format)


    def __getattr__(self, attr):
        if attr not in self.__register:
            raise FilterNotFound('Filter with name {} is not found'.format(attr))
        name = attr.lower()
        convert = 'f_{}'.format(name)
        return filter_wrapper( getattr(self, convert) )

filters = Filters()
