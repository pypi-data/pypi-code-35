#!/usr/bin/env python

__copyright__ = 'Copyright 2013-2016, http://radical.rutgers.edu'
__license__   = 'MIT'


import sys
import pprint

import matplotlib.pyplot as plt
import numpy             as np

import radical.utils     as ru
import radical.pilot     as rp
import radical.analytics as ra

from   radical.utils.profile import *
from   radical.pilot.states  import *

# ------------------------------------------------------------------------------
#
def main():

    events = [
            # 'schedule_ok',
            # 'cu_start',
              'cu_exec_start',
              'app_start',
             ]


    data    = dict()
    sizes   = dict()
    ws_path = 'data/weak_scaling_synapse_titan/optimized'
    ss_path = 'data/strong_scaling_synapse_titan'
    mb_path = 'data/micro_benchmarks_synapse_titan'
    t_path  = 'data/tests'
    sources = [
          # '%s/rp.session.thinkie.merzky.017494.0007'     % t_path,

          # '%s/ws_syn_titan_32_32_1024_60_1.0'            % ws_path,
          # '%s/ws_syn_titan_32_32_1024_60_1.1'            % ws_path,
          # '%s/ws_syn_titan_64_32_2048_60_2.0'            % ws_path,
          # '%s/ws_syn_titan_64_32_2048_60_2.1'            % ws_path,
          # '%s/ws_syn_titan_128_32_4096_60_3.0'           % ws_path,
          # '%s/ws_syn_titan_128_32_4096_60_3.1'           % ws_path,
          # '%s/ws_syn_titan_256_32_8192_60_4.0'           % ws_path,
          # '%s/ws_syn_titan_256_32_8192_60_4.1'           % ws_path,
        #   '%s/ws_syn_titan_512_32_16384_60_5.0'          % ws_path,
          # '%s/ws_syn_titan_512_32_16384_60_5.1'          % ws_path,
          # '%s/ws_syn_titan_1024_32_32768_60_6.0'         % ws_path,
          # '%s/ws_syn_titan_1024_32_32768_60_6.1'         % ws_path,
          # '%s/ws_syn_titan_2048_32_65536_60_7.0'         % ws_path,
          # '%s/ws_syn_titan_2048_32_65536_60_7.1'         % ws_path,
          # '%s/ws_syn_titan_4096_32_131072_60_8.0'        % ws_path,

          # '%s/rp.session.titan-ext1.itoman.017473.0000' % ss_path,
          # '%s/rp.session.titan-ext1.itoman.017491.0004' % ss_path,
          # '%s/rp.session.titan-ext1.itoman.017492.0001' % ss_path,
          # '%s/rp.session.titan-ext2.itoman.017467.0000' % ss_path,

            '%s/micro_syn_titan_512_32_16384_60_5.0'       % mb_path,
            '%s/micro_syn_titan_512_32_16384_60_5.1'       % mb_path,
            '%s/micro_syn_titan_1024_32_32768_60_6.0'      % mb_path,
            '%s/micro_syn_titan_1024_32_32768_60_6.1'      % mb_path,
            '%s/micro_syn_titan_2048_32_65536_60_7.0'      % mb_path,
            '%s/micro_syn_titan_2048_32_65536_60_7.1'      % mb_path,
            '%s/rp.session.titan-ext1.merzky1.017452.0003' % mb_path,
            '%s/rp.session.titan-ext1.merzky1.017453.0004' % mb_path,
            '%s/rp.session.titan-ext1.merzky1.017454.0000' % mb_path,
            '%s/rp.session.titan-ext1.merzky1.017454.0004' % mb_path,
            '%s/rp.session.titan-ext1.merzky1.017458.0002' % mb_path,
            '%s/rp.session.titan-ext1.merzky1.017458.0003' % mb_path,

               ]

    # get the numbers we actually want to plot
    for src in sources:

        # always point to the tarballs
        if src[-4:] != '.tbz':
            src += '.tbz'

        print
        print '-----------------------------------------------------------'
        print src

        session   = ra.Session(src, 'radical.pilot')
        pilots    = session.filter(etype='pilot', inplace=False)
        units     = session.filter(etype='unit',  inplace=True)
        sid       = session.uid

        sizes[sid] = pilots.get()[0].description['cores']
        data[sid]  = dict()

        for event in events:
            data[sid][event] = units.rate(event={ru.EVENT: event}, sampling=5, first=True)


  # print
  # pprint.pprint(data)
  # sys.exit()


    plt.figure(figsize=(20,14))
    labels = list()
    for sid in data:
        for event in events:
            x = [t[0] for t in data[sid][event]]
            y = [t[1] for t in data[sid][event]]

            if not x:
                print 'skip %s / %s' % (sid, event)
                continue
            print 'plot %s / %s' % (sid, event)

            # re-align timestamps to begin at zero
            t_min = x[0]
            for idx in range(len(x)):
                x[idx] -= t_min
            plt.plot(x, y)
            labels.append('%s %s %6d' % (sid, event, sizes[sid]))

  # plt.ylim([0,12])
  # plt.xscale('log')
  # plt.yscale('log')
    plt.xlabel('runtime [s]')
    plt.ylabel('event rate')
    plt.title ('time dependent event rates')
    plt.legend(labels, ncol=4, loc='upper left', bbox_to_anchor=(0,1.13))
    plt.savefig('11_event_rates.png')
    plt.show()


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    main()

# ------------------------------------------------------------------------------


