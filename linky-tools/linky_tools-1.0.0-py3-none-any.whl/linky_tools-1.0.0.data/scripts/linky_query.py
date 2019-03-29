#!python
#    linky-tools 
#
#    Copyright (C) 2019  ermitz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>
#
import os
import argparse
import logging
import linkydb
import datetime



def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1,day=1) - datetime.timedelta(days=1)

def month_periods(from_date,to_date):
    first_day = from_date
    while first_day < to_date:
        last_day =  last_day_of_month(first_day).replace(hour=23,minute=59,second=59)
        if last_day >= to_date:
           last_day = to_date
        yield (first_day,last_day)
        first_day = (last_day + datetime.timedelta(days=1)).replace(hour=0,minute=0,second=0)

if __name__ == '__main__':

    logger = logging.getLogger()

    def valid_date(s):
        if s in ['now']:
            return datetime.datetime.now()

        if s in ['today']:
            t = datetime.date.today()
            return datetime.datetime(t.year, t.month, t.day)

        try:
            return datetime.datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            try:
                return datetime.datetime.strptime(s, "%Y-%m-%d,%H:%M")
            except ValueError:
                msg = "Not a valid date: '{0}'.".format(s)
                raise argparse.ArgumentTypeError(msg)

    # --------------------------------------------------
    # Create argument parser
    # --------------------------------------------------
    parser = argparse.ArgumentParser(description='ERDF linky data query')
    flags = parser.add_argument_group('Flag arguments')


    flags.add_argument('-d', '--debug', 
                       dest='debug', 
                       action='store_const', 
                       const=1, 
                       default=0, 
                       help='Enable the debug prints.')
    
    flags.add_argument('-v', '--verbose', 
                       action='store_true', 
                       default=False, 
                       help='Enable verbose mode.')

    flags.add_argument('-l', '--log', 
                       default=None, 
                       metavar="FILE", 
                       help='File name where to store logs an error messages (default:use stdout/stderr)')

    flags.add_argument('--sqlite3-db', 
                       action='store', 
                       default='linky.sqlite', 
                       help='Sqlite3 database file (default:%(default)s).')

    flags.add_argument('--meter-name', 
                       action='store', 
                       required=False,
                       default='main',
                       metavar='NAME',
                       help='Name of linky meter (default:%(default)s).')

    flags.add_argument('--from-date', 
                       action='store', 
                       required=True,
                       metavar='DATE',
                       type=valid_date,
                       help='Date of begin of query.')

    flags.add_argument('--to-date', 
                       action='store', 
                       required=True,
                       metavar='DATE',
                       type=valid_date,
                       help='Date of end of query.')



    # --------------------------------------------------
    # Parse arguments
    # --------------------------------------------------
    args = parser.parse_args()

    # --------------------------------------------------
    # Apply log arguments
    # --------------------------------------------------
    #  Set log output
    if args.log:
        # A log file was specified, use it to log
        handler = logging.FileHandler(args.log, mode='w')
    else:
        # No log file was specified, use default stream to stdout
        handler = logging.StreamHandler()

    #  Set log format
    if args.debug > 0:
        # -d was specified -> use a detailed format
        handler.setFormatter(logging.Formatter('%(filename)s[%(lineno)d]:%(levelname)s> %(message)s'))
        logger.addHandler(handler) 
        logger.setLevel(logging.DEBUG)
    else:
        # -d not specified -> use a simpler format
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s> %(message)s'))
        logger.addHandler(handler)

        if args.verbose:
            # -v :  output up to INFO level
            logger.setLevel(logging.INFO)
        else:
            # no -v :  output up to WARNING level (.i.e no INFO)
            logger.setLevel(logging.WARNING)


    #print (args)

    args.to_date = args.to_date.replace(hour=23,minute=59,second=59)

    linkydb.open_db(filename=os.path.abspath(args.sqlite3_db))

    hourly = linkydb.LinkyDbHourlyData(metername=args.meter_name)
    monthly = linkydb.LinkyDbMonthlyData(metername=args.meter_name)
    for (f,l) in month_periods(args.from_date,args.to_date):
        total_month = 0
        for m in hourly.query(f,l):
            print (datetime.datetime.fromtimestamp(m.time),m.value)
            total_month += m.value

        m = monthly.get_data(f)
        if m:
          total_from_db = m.value
        else:
          total_from_db = 'unknown'
        print ('----- total: %f (%s)' % (total_month,total_from_db))
    
    

    exit(0)


