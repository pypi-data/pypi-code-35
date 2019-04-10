#!/usr/bin/env python

__copyright__ = 'Copyright 2013-2016, http://radical.rutgers.edu'
__license__   = 'MIT'


import sys

import radical.utils     as ru
import radical.pilot     as rp
import radical.analytics as ra

import matplotlib.pyplot as plt
import numpy             as np


# create several plots wiwth shared X-Axis (time):
#  - a state transition plot for each stateful entity type
#  - for entity type with most members:
#    - concurrent entities under changing ownership

state_vals = 

# ---------------------------------------------------------------------------     ---
#
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "\n\tusage: %s <dir|tarball>\n" % sys.argv[0]
        sys.exit(1)

    src     = sys.argv[1]
    session = ra.Session(src, 'radical.pilot')

    # A formatting helper before starting...
    def ppheader(message):
        separator = '\n' + 78 * '-' + '\n'
        print separator + message + separator

    session.filter(etype=event_entity, inplace=True)
    print '#entities: %d' % len(session.get())

    data = dict()
    for thing in session.get():

        tstamps = list()

        for event in event_list:
            times = thing.timestamps(event=event)
            if times: tstamps.append(times[0])
            else    : tstamps.append(None)

        data[thing.uid] = tstamps

  # diffs = list()
  # for uid in data:
  #     diffs.append(data[uid][-1] - data[uid][0])
  # print sorted(diffs)


    sorted_things = sorted(data.items(), key=lambda e: e[1][0])
    sorted_data   = list()
    index         = 0
  # for thing in sorted_things[150:170]:
    for thing in sorted_things:
        sorted_data.append([index] + thing[1])
        index += 1


    np_data = np.array(sorted_data)
  # print np_data

    plt.figure(figsize=(20,14))
    for e_idx in range(len(event_list)):
        plt.plot(np_data[:,0], np_data[:,(1+e_idx)], label=event_list[e_idx])

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
          ncol=2, fancybox=True, shadow=True)
    plt.savefig('07_event_timeline.svg')
    plt.show()


# ------------------------------------------------------------------------------

