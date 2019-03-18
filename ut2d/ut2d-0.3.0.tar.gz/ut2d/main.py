from __future__ import absolute_import

import argparse
import time

from ut2d.lib import EMOJI, throw_msg, TimezoneScrapper, Time


def main():
    parser = argparse.ArgumentParser(description='a command-line utility to convert unitx timestamp into human readable datetime.')
    parser.add_argument('ut_or_now', help='input now or a unix timestamp')
    parser.add_argument('--diff', '-d', action='store_true', help='time difference between input time and current time')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--timezone', '-tz', type=str, required=False, help='timezone info formatted as: GMT+8, or UTC+8')
    group.add_argument('--city', '-c', type=str, required=False, help='search local time of named city of input time')
    args = parser.parse_args()

    if args.ut_or_now == 'now':
        ut = time.time()
    else:
        if Time.is_valid(args.ut_or_now):
            ut = args.ut_or_now
        else:
            throw_msg(1, 'arg_invalid', True)
        
    dt = Time(ut)

    print(f'Unix Timestamp: {ut}')
    print(f'Local: {Time.fmt(dt.local)}')
    print(f'GMT  : {Time.fmt(dt.utc)}')

    if args.diff:
        print(dt.from_now)
    
    if args.timezone:
        if args.timezone[:3].upper() not in ['GMT', 'UTC']:
            throw_msg(1, 'tz_fmt_invalid', True)
        else:
            dt_tz = dt.in_timezone(args.timezone)
            print(EMOJI['smiling_face_with_sunglasses'] + ' '
                  f' The given time in {args.timezone} is: {Time.fmt(dt_tz)}.')

    if args.city:
        throw_msg(0, 'search_tz_begin')
        
        dt_city = dt.in_city(args.city)
        print(EMOJI['smiling_face_with_sunglasses'] + ' '
              f' I suppose the given time in {args.city} is: {Time.fmt(dt_city)}.'
              ' I have 88% confidence with this result from search engines!')


if __name__ == '__main__':
     main()
