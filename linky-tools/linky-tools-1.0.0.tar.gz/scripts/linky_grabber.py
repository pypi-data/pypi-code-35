#!/usr/bin/env python
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
import datetime
from dateutil.relativedelta import relativedelta

import linkymeter as linky
import linkydb


def add_data(meter_name,data,data_period):
        if data_period == 'hours':
           dbmeter = linkydb.LinkyDbHourlyData(metername=meter_name)
        elif data_period == 'days':
           dbmeter = linkydb.LinkyDbDailyData(metername=meter_name)
        elif data_period == 'months':
           dbmeter = linkydb.LinkyDbMonthlyData(metername=meter_name)
        elif data_period == 'years':
           dbmeter = linkydb.LinkyDbYearlyData(metername=meter_name)
        else:
            raise ValueError

        for v in data:
            dbmeter.add_data(v['time'],v['conso'])


def grab_from_cloud(args):
    if args.data_dir and not os.path.exists(args.data_dir):
        os.mkdir(args.data_dir)

    logger.info("logging in as %s...", args.username)
    session = linky.web.session.login(args.username,args.password)
    logger.info("logged in successfully!")

    today = datetime.date.today()


    # Years
    logger.info("retrieving yearly data...")
    res_year = session.get_yearly_consumption(data_dir=args.data_dir)
    logger.info('adding yearly data...')
    add_data(args.meter_name,res_year,"years")

    # 12 months ago - today
    logger.info("retrieving monthly data...")
    res_month = session.get_monthly_consumption((today - relativedelta(months=11)), today,
                                           data_dir=args.data_dir)
    logger.info('adding monthly data...')
    add_data(args.meter_name,res_month,"months")

    # One month ago - yesterday
    logger.info("retrieving daily data...")
    res_day = session.get_daily_consumption((today - relativedelta(days=1, months=1)),
                                       (today - relativedelta(days=1)),
                                           data_dir=args.data_dir)
    logger.info('adding daily data...')
    add_data(args.meter_name,res_day,"days")

    # One week ago 
    logger.info("retrieving hourly data...")
    res_hour = session.get_hourly_consumption((today - relativedelta(days=7)), today,
                                           data_dir=args.data_dir)
    logger.info('adding hourly data...')
    add_data(args.meter_name,res_hour,"hours")


def grab_from_files(args):
    from linkymeter.web.datashaper import getDataShaper
    import json
    for fname in args.files:
        logger.info('Extracting data from json file %s' % (fname))
        data = json.loads(open(fname).read())
        shaper = getDataShaper(data, data_period=args.files_period)
        add_data(args.meter_name,shaper.data(),args.files_period)


def main(args):
    if args.create:
        logger.info('Create database')
        linkydb.open_db(filename=os.path.abspath(args.sqlite3_db),create=True)
        linkydb.add_meter(metername=args.meter_name)
        exit(0)
    else:
        linkydb.open_db(filename=os.path.abspath(args.sqlite3_db))


    if not args.from_cloud and len(args.files) >= 1:
        grab_from_files(args)
    else:
        grab_from_cloud(args)




if __name__ == '__main__':

    logger = logging.getLogger()

    # --------------------------------------------------
    # Create argument parser
    # --------------------------------------------------
    parser = argparse.ArgumentParser(description='Enedies linky data grabber')
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

    flags.add_argument('--create', 
                       action='store_true', 
                       default=False, 
                       help='Create database.')

    flags.add_argument('--data-dir', 
                       action='store', 
                       default=None, 
                       help='Database folder.')

    flags.add_argument('--sqlite3-db', 
                       action='store', 
                       default='linky.sqlite', 
                       help='Sqlite3 database file.')

    flags.add_argument('--credentials',
                       required=False,
                       type=argparse.FileType('r'),
                       metavar='USERNAME:PASSWORD',
                       help='File containing credentials for Enedis account')

    flags.add_argument('--meter-name', 
                       action='store', 
                       required=False,
                       default='main',
                       metavar='NAME',
                       help='Name of linky meter (default:%(default)s).')

    flags.add_argument('--from-files',
                       action='store_false', 
                       dest='from_cloud',
                       default=True, 
                       help='Grab data from json files.')

    flags.add_argument('--from-cloud',
                       action='store_true', 
                       dest='from_cloud',
                       default=True, 
                       help='Grab data from ERDF cloud.')

    flags.add_argument('--files-period',
                       action='store', 
                       choices=['hours','days','months','years'],
                       help='Type of files.')

    parser.add_argument('files', nargs='*', help='bar help')

    # --------------------------------------------------
    # Parse arguments
    # --------------------------------------------------
    args = parser.parse_args()

    # --------------------------------------------------
    # Apply log arguments
    # --------------------------------------------------
    #  Set log output
    #  use default stream to stdout
    handler1 = logging.StreamHandler()
    handler2 = None
    if args.log:
        import logging.handlers
        # A log file was specified, use it to log
        handler2 = logging.handlers.RotatingFileHandler(args.log, mode="a", maxBytes= 1000000, backupCount= 1)

    #  Set log format
    if args.debug > 0:
        # -d was specified -> use a detailed format
        formatter = logging.Formatter('%(filename)s[%(lineno)d]:%(levelname)s> %(message)s')
        handler1.setFormatter(formatter)
        logger.addHandler(handler1) 
        if handler2:
            handler2.setFormatter(formatter)
            logger.addHandler(handler2) 
        logger.setLevel(logging.DEBUG)
    else:
        # -d not specified -> use a simpler format
        formatter = logging.Formatter('%(asctime)s %(levelname)s> %(message)s')
        handler1.setFormatter(formatter)
        logger.addHandler(handler1)
        if handler2:
            handler2.setFormatter(formatter)
            logger.addHandler(handler2) 

        if args.verbose:
            # -v :  output up to INFO level
            logger.setLevel(logging.INFO)
        else:
            # no -v :  output up to WARNING level (.i.e no INFO)
            logger.setLevel(logging.WARNING)

    if args.credentials:
        s = args.credentials.read().strip().split(':')
        username = s[0]
        password = ":".join(s[1:])
        args.credentials.close()

        args.username = username
        args.password = password


    try:
        logger.info('----------------------------------------')
        main(args)
    except:
        import traceback
        traceback.print_exc()
        exit(1)




