# Copyright (C) 2014-2018 Michel Le Page
#
# mET_weap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mET_weap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#--- external imports ---
import os
import glob
from datetime import datetime
#------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


def select_files_agroyear_16j(path, prefix, from_year, to_year):

    list_fnames = []

    for year in range(from_year, to_year+1):

        for month in range(cf['agroyear']["begin"], 13):
            fname = os.path.join(path, prefix+'_'+str(year)+'.'+str("%02d"%month)+'.01.tif')
            if os.path.exists(fname):
                list_fnames.append(fname)
            fname = os.path.join(path, prefix+'_'+str(year)+'.'+str("%02d"%month)+'.16.tif')
            if os.path.exists(fname):
                list_fnames.append(fname)

        for month in range(1, cf['agroyear']["end"]+1):
            fname = os.path.join(path, prefix+'_'+str(year+1)+'.'+str("%02d"%month)+'.01.tif')
            if os.path.exists(fname):
                list_fnames.append(fname)
            fname = os.path.join(path, prefix+'_'+str(year+1)+'.'+str("%02d"%month)+'.16.tif')
            if os.path.exists(fname):
                list_fnames.append(fname)

        month = cf['agroyear']["end"]+2
        day = 1
        lll = sorted(glob.glob(os.path.join(path, prefix+'_'+str(year+1)+'.'+str("%02d"%month)+'.'+str("%02d"%day)+'*.tif')))
        for fname in lll:
            list_fnames.append(fname)

    return list_fnames

def select_files_agroyear_all(path, prefix, from_year, to_year, sep='.'):

    list_fnames = []
    for year in range(from_year, to_year+1):
        for month in range(cf['agroyear']["begin"], 13):
            #print(os.path.join(path,prefix+'_'+str(year)+sep+str("%02d"%month)+'*.tif'))
            lll = sorted(glob.glob(os.path.join(path, prefix+'_'+str(year)+sep+str("%02d"%month)+'*.tif')))
            for fname in lll:
                list_fnames.append(fname)

        for month in range(1, cf['agroyear']["end"]+1):
            #print(os.path.join(path,prefix+'_'+str(year+1)+sep+str("%02d"%month)+'*.tif'))
            lll = sorted(glob.glob(os.path.join(path, prefix+'_'+str(year+1)+sep+str("%02d"%month)+'*.tif')))
            for fname in lll:
                list_fnames.append(fname)

    month = cf['agroyear']["end"]+1
    lll = sorted(glob.glob(os.path.join(path, prefix+'_'+str(year+1)+sep+str("%02d"%month)+'*.tif')))
    if len(lll) > 0:
        list_fnames.append(lll[0])

    return list_fnames

def get_date_ecmwf(fname):

    ladate = fname.split(os.sep)[-1].split('erainterim_sfc_fc_')[-1].split('_to_')[0]
    ladate = ladate.replace('-', '.')
    datetime_date = datetime.strptime(str(ladate), '%Y.%m.%d')
    return(ladate, datetime_date)

def get_date_modis(fname, prefix, frmt='%Y.%m.%d'):

    if str(fname.__class__) == "<class 'str'>":
        ladate = fname.split(os.sep)[-1]                   # decoupe de expression par \\
        ladate = ladate.split(prefix+'_')[1].split('.tif')[0]       # decoupe de date et .tif
        datetime_date = datetime.strptime(str(ladate), frmt)
        return(ladate, datetime_date)
    elif str(fname.__class__) == "<class 'list'>":
        ladate = []
        datetime_date = []
        for ff in fname:
            ll = ff.split(os.sep)[-1]                   # decoupe de expression par \\
            ll2 = ll.split(prefix+'_')[1].split('.tif')[0]
            ladate.append(ll2)       # decoupe de date et .tif
            datetime_date.append(datetime.strptime(str(ll2), frmt))
        return(ladate, datetime_date)
