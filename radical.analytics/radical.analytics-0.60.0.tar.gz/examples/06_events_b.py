#!/usr/bin/env python

__copyright__ = 'Copyright 2013-2016, http://radical.rutgers.edu'
__license__   = 'MIT'


import sys
import pprint

import numpy             as np
import matplotlib.pyplot as plt

import radical.utils     as ru
import radical.analytics as ra

"""
This example illustrates hoq to obtain durations for arbitrary (non-state)
profile events.
"""


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "\n\tusage: %s <dir|tarball>\n" % sys.argv[0]
        sys.exit(1)

    src = sys.argv[1]

    if len(sys.argv) == 2: stype = 'radical.pilot'
    else                 : stype = sys.argv[2]

    session = ra.Session(src, stype)

    print ("Time spent by the units in execution") 
    units = session.filter(etype='unit', inplace=False)
    print '#units   : %d' % len(units.get())

    ranges = units.ranges(event=[{ru.EVENT: 'date_submit'},
                                 {ru.EVENT: 'date_finish'}],
                          collapse=False)
    print 'ranges   :'
    for r in ranges:
        print '  [%7.2f, %7.2f] = %7.2f' % (r[0], r[1], r[1] - r[0])

    duration = units.duration(ranges=ranges)
    print 'duration : %.2f' % duration


    print "concurrent units in between date_submit and date_finish events"
  # concurrency = units.concurrency(event=[{ru.EVENT: 'date_submit'},
  #                                        {ru.EVENT: 'date_finish' }],
  #                                 sampling=10)
    concurrency = units.concurrency(event=[{ru.EVENT: 'exec_start'},
                                           {ru.EVENT: 'exec_stop' }],
                                    sampling=10)
    pprint.pprint(concurrency)

    plt.figure(figsize=(20,14))
    plt.plot([x[0] for x in concurrency], 
             [x[1] for x in concurrency],
             label='execution concurrency')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
          ncol=2, fancybox=True, shadow=True)
    plt.savefig('06_concurrency.png')
    plt.show()


# ------------------------------------------------------------------------------

