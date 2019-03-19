
import numpy as np
import datetime as dt
from pyspedas.utilities.time_string import time_string
from pyspedas.utilities.time_double import time_double

def mms_feeps_remove_bad_data(probe = '1', data_rate = 'srvy', datatype = 'electron', level = 'l2', suffix = ''):
    data_rate_level = data_rate + '_' + level

    # electrons first, remove bad eyes
    #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; 1. BAD EYES ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    #  First, here is a list of the EYES that are bad, we need to make sure these 
    #  data are not usable (i.e., make all of the counts/rate/flux data from these eyes NAN). 
    #  These are for all modes, burst and survey:
bad_data_table = {}
bad_data_table['2017-10-01'] = {}
bad_data_table['2017-10-01']['mms1'] = {'top': [1], 'bottom': [1, 11]}
bad_data_table['2017-10-01']['mms2'] = {'top': [5, 7, 12], 'bottom': [7]}
bad_data_table['2017-10-01']['mms3'] = {'top': [2, 12], 'bottom': [2, 5, 11]}
bad_data_table['2017-10-01']['mms4'] = {'top': [1, 2, 7], 'bottom': [2, 4, 5, 10, 11]}

bad_data_table['2018-10-01'] = {}
bad_data_table['2018-10-01']['mms1'] = {'top': [1], 'bottom': [1, 11]}
bad_data_table['2018-10-01']['mms2'] = {'top': [7, 12], 'bottom': [2, 12]}
bad_data_table['2018-10-01']['mms3'] = {'top': [1, 2], 'bottom': [5, 11]}
bad_data_table['2018-10-01']['mms4'] = {'top': [1, 7], 'bottom': [4, 11]}

dates = np.asarray(time_double(list(bad_data_table.keys())))
closest_table_tm = (np.abs(dates - dt.datetime.now().timestamp())).argmin()

closest_table = time_string(dates[closest_table_tm], '%Y-%m-%d')
bad_data = bad_data_table[closest_table]['mms'+probe]



