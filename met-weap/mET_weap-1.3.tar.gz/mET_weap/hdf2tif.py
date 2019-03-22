# Copyright (C) 2014-2018 Michel Le Page
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#--- external imports ---
import os
import subprocess
import glob
from datetime import datetime
#----------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


def hdf2tif(List_Fich_name, outputdir, path_to_osgeo, win_xleft, win_xright, win_ybottom, win_ytop, variable):
    """
    extract one subdataset, project it to WGS84 and convert it from HDF to TIF
    subset the image to the given window
    You must take care of double quotes in the variable name (the subdataset) : variable=':MODIS_Grid_Daily_1km_LST:"LST_Day_1km"'
    """    
    gdalwarp = os.path.join(path_to_osgeo, "gdalwarp")
    gdaltranslate = os.path.join(path_to_osgeo, "gdal_translate")
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    for fname in List_Fich_name:

        nomfic = os.path.basename(fname)
        new_date = datetime.strptime(str(nomfic[9:16]), '%Y%j')
        new_name_output = str(new_date.strftime('%Y.%m.%d')) + ".tif"
        new_name_output = variable.split(':')[-1].split('"')[1].replace(' ', '')+'_'+str(new_date.strftime('%Y.%m.%d')) + ".tif"

        print(new_name_output)

        new_name_output = os.path.join(outputdir, new_name_output)
        new_name_tmp = os.path.join(outputdir, "tmp.tif")

        if os.path.exists(new_name_tmp) is True:
            os.remove(new_name_tmp)

        if os.path.isfile(new_name_output) is False:
            print(gdalwarp + ' -t_srs EPSG:4326 -of GTiff HDF4_EOS:EOS_GRID:"' + fname + '"'+ variable+' "'+  new_name_tmp+'"')
            #os.system(gdalwarp + ' -t_srs EPSG:4326 -of GTiff HDF4_EOS:EOS_GRID:"' + fname + '"'+ variable+' "'+  new_name_tmp+'"')
            subprocess.call(gdalwarp + ' -t_srs EPSG:4326 -of GTiff HDF4_EOS:EOS_GRID:"' + fname + '"'+ variable+' "'+  new_name_tmp+'"', shell=False, startupinfo=startupinfo)

            print(gdaltranslate + ' -projwin '+str(win_xleft)+' '+str(win_ytop)+' '+str(win_xright)+' '+str(win_ybottom)+' "'+ new_name_tmp +'" "'+ new_name_output+'"')
            subprocess.call(gdaltranslate + ' -projwin '+str(win_xleft)+' '+str(win_ytop)+' '+str(win_xright)+' '+str(win_ybottom)+' "'+ new_name_tmp +'" "'+ new_name_output+'"', shell=False, startupinfo=startupinfo)

            os.remove(new_name_tmp)
