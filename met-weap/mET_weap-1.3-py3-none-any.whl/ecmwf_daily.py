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
import numpy as np
import os
import PIL
from ecmwfapi import ECMWFDataServer
from osgeo import gdal, osr
gdal.UseExceptions()
from datetime import datetime, timedelta
from math import exp, pi, cos, sin, acos, tan
from  scipy.interpolate import InterpolatedUnivariateSpline
from scipy.misc import imresize
from skimage.transform import resize
#------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


def gradient(img, shape, operation, Dz, gradientT):

    if operation == "mean":
        imgmean = img.mean(axis=2)
    elif operation == "min":
        imgmean = img.min(axis=2)
    elif operation == "max":
        imgmean = img.max(axis=2)

    pix_resize = PIL_resize(imgmean, shape)
    
#    Dz0 = np.matrix('0,0;0,0;0,0')
#    Dz0 = np.zeros(shape=(103,51))
#    pix_resize = imgmean - Dz0
#    pix_resize = imgmean - Dz * gradientT
    pix_resize = pix_resize - Dz * gradientT

    return pix_resize

def PIL_resize(img, shape):
    PILshape = (shape[1], shape[0])
    pix = PIL.Image.fromarray(img)
    pix = pix.resize(PILshape, PIL.Image.BICUBIC)
    #pix = pix.rotate(90)
    return np.array(pix)

"""
erainterim_to_tif(fname,dims,window): 
  Convert ECMWF Erainterim Netcdf File to SPARSE input data in Gtif Format with WGS84 projection and the desired output resolution and window
  The times 9h, 12h and 15h are converted and stacked into three bands

Parameters: 
  (char*) fname: the name of the Netcdf input file
  (int[2]) dims: the dimension in pixels of the output file: [width, height]
  (float[4]) window: the geographic window of the output file with  [xmin,ymin,xmax,ymax]

Dependencies:
  os
  datetime
  gdal + binary gdalwarp
  numpy
  
"""


def era5_daily(fname, dims, GT, window, Lat, Dz, DEM_cdsapi):

    # seasonal correction of Tair according to dz
    # http://www.hydrol-earth-syst-sci.net/16/4661/2012/hess-16-4661-2012.pdf

#    monthly_tair_correction_km = np.array([-4.7, -4.4, -5.9, -7.1, -7.8, -8.1, -8.2, -8.1, -8.1, -7.7, -6.8, -5.5, -4.7, -4.4])
    monthly_tair_correction_km = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    monthly_tair_correction_m = monthly_tair_correction_km/1000.
    monthly_x = np.arange(-15.5, 400, 30.416)
    s = InterpolatedUnivariateSpline(monthly_x, monthly_tair_correction_m)
    daily_tair_correction_m = s(np.array(np.arange(1, 368, 1)))

    try:
        gdalwarp = os.path.join(path_to_osgeo, "gdalwarp")
        fname_tmp = os.path.join(cf['path']["ERA5_tif"], "tmp.tif")

        print("\n--->%s\n"%fname)
        inDs = gdal.Open('NETCDF:"'+fname)

#        lejour = fname.split(os.sep)[-1].split('era5_sfc_fc_')[-1].split('_to_')[0]
        lejour = fname.split(os.sep)[-1].split('era5_')[-1].split('.nc')[0]

        date = datetime.strptime(str(lejour), '%Y-%m-%d')
        jday = date.timetuple().tm_yday

        subds = inDs.GetSubDatasets()
        nbands = len(subds)
        # on utilise les dimensions du premier subdataset
        sds = gdal.Open(subds[0][0])
        cols = sds.RasterXSize
        rows = sds.RasterYSize
        hours = sds.RasterCount
        sds = None

        data_all = np.zeros((nbands, rows, cols, hours))
        varnames = []
        dates = []

        sd = subds[0]

        do_dates = True

        # boucle sur les subdatasets
        bandsERA = 0

        i = 0
        for sd in subds:
            var = sd[0].split(':')
            var.reverse()
            var = var[0]

            varnames.append(var)

            sds = gdal.Open(sd[0])
            PJ = osr.SpatialReference()
            PJ.SetWellKnownGeogCS("EPSG:4326")
            MD = sds.GetMetadata_Dict()
            add_offset = float(MD.get(var+'#add_offset'))
            scale_factor = float(MD.get(var+'#scale_factor'))
            nodata = float(MD.get(var+'#_FillValue'))
            long_name = MD.get(var+'#long_name')
            units = MD.get(var+'#units')
            units = MD.get(var+'#units')

            print("----------------------------------------------------------")
            print(var, " : ", long_name, " (", units, ")")
            print("----------------------------------------------------------")

            date0 = datetime.strptime("1900-01-01", "%Y-%m-%d")
            time_values = MD.get('NETCDF_DIM_time_VALUES').split('{')[1].split('}')[0].split(',')

            n1 = 0
            for n in range(hours):
                ladate = date0+timedelta(int(time_values[n])/24)
                lheure = ladate.hour
                #if (lheure==9 or lheure==12 or lheure==15) and n1<3:       # on écrit uniquement les heures 9,12,15 du premier jour
                if n < 9:       # les 8 premieres heures = 0, 3, 6...
                    n1 = n1+1
                    if do_dates:
                        dates.append(ladate)

                    # If step 0 is chosen, then only analysed fields, which are produced for 0000, 0600, 1200 and 1800 UTC, are available.
                    # If step 3, 6, 9 or 12 is selected then only forecast fields which are produced from forecasts beginning at 0000 and 1200 UTC, are available.
                    # Table 9 lists the accumulated (from the beginning of the) forecast.

                    # ssrd et tisr font partie des variables cumulatives
                    #Comme j'ai choisis l'option "forecast à 0h et 12h, et ls timesteps 3,6,9,12, les cumuls commencent à 0h puis à 12h
                    # 3h =  cumul 0-3h
                    # 6h = cumul 0-6h
                    # 9h = cumul 0-9h
                    # 12h = cumul 0-12h
                    # 15h =  cumul 12-15h
                    # 18h = cumul 12-18h
                    # 21h = cumul 12-21h
                    # 0h = cumul 12-24h

                    if (var == 'ssrd' or var == 'tisr' or var == 'tp') and lheure != 0 and lheure != 15:
                        if n > 1:
                            data_before = add_offset + sds.GetRasterBand(n).ReadAsArray()*scale_factor
                            data_after = add_offset + sds.GetRasterBand(n+1).ReadAsArray()*scale_factor
                            data = data_after-data_before
                        else:
                            data = add_offset + sds.GetRasterBand(n+1).ReadAsArray()*scale_factor
                    else:
                        data = add_offset + sds.GetRasterBand(n+1).ReadAsArray()*scale_factor

                    if (var == 'ssrd' or var == 'tisr') and lheure == 0 and n == 7:
                        data = data-(data_all[5, :, :, 4]+data_all[5, :, :, 5]+data_all[5, :, :, 6])

                    print(n1, ladate, time_values[n], data[0, 0])
#                        outDs.GetRasterBand(n1).WriteArray(data)
                    data_all[i, :, :, n] = data

            bandsERA = n1
            i = i+1
            sds = None

        # passage du 3h vers journalier
        gradientT = daily_tair_correction_m[jday]

        # wind speed
        index_u10 = varnames.index('u10')
        index_v10 = varnames.index('v10')
        data_u10 = data_all[index_u10, :, :, :]
        data_v10 = data_all[index_v10, :, :, :]

#        data_u10=data_u10.reshape(cols*rows,bandsERA)
#        data_v10=data_v10.reshape(cols*rows,bandsERA)

        data_u10 = data_u10.mean(axis=2)
        data_v10 = data_v10.mean(axis=2)

        U2 = np.sqrt(data_u10*data_u10 + data_v10*data_v10)

#        U2=imresize(U2,Dz.shape,interp='cubic')
#        U2 = resize(U2, Dz.shape, mode = None, order=2)
#        U2 = resize(U2, Dz.shape, mode = 'edge')
        U2 = PIL_resize(U2, Dz.shape)

        #  FAO eq. 47
        #U2= U2 * 4.87 / np.log(67.8*Dz-5.42)

        # Tair
        index = varnames.index('t2m')
        TairK = data_all[index, :, :, :]
#        TairK = TairK.reshape(cols*rows,bandsERA)
#        TairK = resize(TairK, Dz.shape, mode = 'edge')
#        TairK = resize(TairK, Dz.shape, mode = 'edge', order=2)
        TairC = TairK-273.15
        TairCmean_z1 = gradient(TairC, Dz.shape, "mean", Dz, 0.)

        # correction DEM_cdsapi avec gradient de -0.6° tous les 100 metres
        #TairK = TairK (DEM_cdsapi-DEM_ERA_cdsapi) * -0.0006

        # correction DEM_cdsapi avec gradient variable suivant les mois tous les 100 metres
        TairCmean = gradient(TairC, Dz.shape, "mean", Dz, gradientT)
        TairCmin = gradient(TairC, Dz.shape, "min", Dz, gradientT)
        TairCmax = gradient(TairC, Dz.shape, "max", Dz, gradientT)

        """
        TairCmean = TairC.mean(axis = 2)
        TairCmin = TairC.min(axis = 2)
        TairCmax = TairC.max(axis = 2)

        pix = PIL.Image.fromarray(TairCmean)
        toto = pix.resize(Dz.shape,PIL.Image.BICUBIC)
        toto2 = np.array(toto)

        TairCmean = imresize(TairCmean,Dz.shape,interp = 'cubic')
        TairCmin = imresize(TairCmin,Dz.shape,interp = 'cubic')
        TairCmax = imresize(TairCmax,Dz.shape,interp = 'cubic')

        TairCmean = TairCmean - Dz * gradientT
        TairCmin = TairCmin - Dz * gradientT
        TairCmax = TairCmax - Dz * gradientT
        """

        # Relative Humidity
        # es = 611.21 * exp(17.502*(Tair-273.16)/(Tair-32.19))
        # ea = 611.21 * exp(17.502*(Tdew-273.16)/(Tdew-32.19))
        # rh = (ea / es)*100

        index = varnames.index('d2m')
        Tdew = data_all[index, :, :, :]
#        Tdew=Tdew.reshape(cols*rows,bandsERA)

        # correction DEM_cdsapi avec gradient de -0.6° tous les 100 metres
        #TairK = TairK (DEM_cdsapi-DEM_ERA_cdsapi) * -0.0006

        # correction DEM_cdsapi avec gradient variable suivant les mois tous les 100 metres
        esMean = np.zeros(Dz.shape)
        eaMean = np.zeros(Dz.shape)

        for i in range(Tdew.shape[-1]):
            Tdew1 = PIL_resize(Tdew[:, :, i], Dz.shape)
#            Tdew1 = imresize(Tdew[:, :, i], Dz.shape, interp='cubic')
#            Tdew1 = resize(Tdew[:, :, i], Dz.shape, mode = None, order=2)
#            Tdew1 = resize(Tdew[:, :, i], Dz.shape, mode = 'edge')
            Tdew1 = Tdew1 - Dz * gradientT

            TairK1 = PIL_resize(TairK[:, :, i], Dz.shape)
#            TairK1 = imresize(TairK[:, :, i], Dz.shape, interp = 'cubic')
#            TairK1 = resize(TairK[:, :, i], Dz.shape, mode = None, order=2)
#            TairK1 = resize(TairK[:, :, i], Dz.shape, mode = 'edge')
            TairK1 = TairK1 - Dz * gradientT

            es = 611.21 * np.exp(17.502*(TairK1-273.16)/(TairK1-32.19)) / 1000.
            ea = 611.21 * np.exp(17.502*(Tdew1-273.16)/(Tdew1-32.19))  / 1000.

            esMean = esMean + es
            eaMean = eaMean + ea

            # http://andrew.rsmas.miami.edu/bmcnoldy/Humidity.html
            # * Values are calculated using the August-Roche-Magnus approximation.
            #TairK1 = TairK1 + 273.16
            #Tdew1 = Tdew1 + 273.16
            #RH = 100*(np.exp((17.625*Tdew1)/(243.04+Tdew1))/np.exp((17.625*TairK1)/(243.04+Tdew1)))

            # https://www.vaisala.com/sites/default/files/documents/Humidity_Conversion_Formulas_B210973EN-F.pdf
            #TairK1 = TairK1 + 273.16
            #Tdew1 = Tdew1 + 273.16
            #A = 6.116441
            #m = 7.591386
            #Tn = 240.7263
            #PwsTd = A*np.exp((m*Tdew1)/(Tdew1+Tn))     #hPa
            #PwsTa = A*np.exp((m*TairK1)/(TairK1+Tn))   #hPa
            #HR = PwsTd/PwsTa

        # moyenne sur le nombre de mesures (8 normalement)
        esMean = esMean / Tdew.shape[-1]
        eaMean = esMean / Tdew.shape[-1]

        # Rayonnement solaire incident

        index = varnames.index('ssrd')
        Rs_jm2 = data_all[index, :, :, :]
#        Rs_jm2 = Rs_jm2.reshape(cols*rows, bandsERA)

        Rs_jm2 = Rs_jm2.sum(axis=2)
        Rs_jm2 = Rs_jm2 / 1000000. # on passe en MJ.m-2 pour FAO Daily

#        Rs_jm2 = imresize(Rs_jm2, Dz.shape, interp='cubic')
#        Rs_jm2 = resize(Rs_jm2, Dz.shape, mode = None, order=2)
#        Rs_jm2 = resize(Rs_jm2, Dz.shape, mode = 'edge')
        Rs_jm2 = PIL_resize(Rs_jm2, Dz.shape)

        # Pression Pa -> kPa
        index = varnames.index('sp')
        Pressure = data_all[index, :, :, :]
#        Pressure = Pressure.reshape(cols*rows, bandsERA)

        Pressure = Pressure.mean(axis=2) # on passe de Pascal à KiloPascal

#        Pressure = imresize(Pressure, Dz.shape, interp='cubic')
#        Pressure = resize(Pressure, Dz.shape, mode = None, order=2)
#        Pressure = resize(Pressure, Dz.shape, 'edge')
        Pressure = PIL_resize(Pressure, Dz.shape)
        #Pressure = (Pressure * 100 * np.power(1 - ((0.0065 * Dz)/(Tair_C_mean_PIL_z1 + 0.0065*Dz + 273.15)), -5.257))/1000.  # http://keisan.casio.com/exec/system/1224575267
        Pressure = Pressure * np.exp(Dz*9.81/(287.*((TairCmean+TairCmean_z1)/2 + 273.15)))/1000.

        # Total Precipitation m/3h -> mm/day
        index = varnames.index('tp')
        Rain = data_all[index, :, :, :]
#        Rain = Rain.reshape(cols*rows,bandsERA)
        Rain = Rain.sum(axis=2)*1000.

#        Rain = imresize(Rain, Dz.shape, interp='cubic')
#        Rain = resize(Rain, Dz.shape, mode = None, order=2)
#        Rain = resize(Rain, Dz.shape, mode = 'edge')
        Rain = PIL_resize(Rain, Dz.shape)

        # ET0
        albedo = 0.23
        ET0 = et0_pm2(Pressure, TairCmean, TairCmin, TairCmax, esMean, eaMean, Lat, jday, albedo, Rs_jm2, U2, DEM_cdsapi)

#            # ---- finalisation ----
#            output = np.zeros((cols, rows, 8))
#            output[0,:,:] = Pressure.reshape((cols, rows))
#            output[1,:,:] = Rain.reshape((cols, rows))
#            output[2,:,:] = Rs_jm2.reshape((cols, rows))
#            output[3,:,:] = es.reshape((cols, rows))
#            output[4,:,:] = ea.reshape((cols, rows))
#            output[5,:,:] = TairCmin.reshape((cols, rows))
#            output[6,:,:] = TairCmax.reshape((cols, rows))
#            output[7,:,:] = Uv.reshape((cols, rows))

        # ---- Ecriture Temp ----

        fname_out = os.path.join(cf['path']["ERA5_tif"], "Temp"+"_"+lejour+".tif")
        if os.path.exists(fname_out):
            os.remove(fname_out)
        driver = gdal.GetDriverByName("GTiff")
        outDs = driver.Create(fname_out, dims[0], dims[1], 1, gdal.GDT_Float32)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ.ExportToWkt())
        outDs.GetRasterBand(1).WriteArray(TairCmean)
        outDs = None

        # ---- Ecriture Rain ----

        fname_out = os.path.join(cf['path']["ERA5_tif"], "Rain"+"_"+lejour+".tif")
        if os.path.exists(fname_out):
            os.remove(fname_out)
        driver = gdal.GetDriverByName("GTiff")
        outDs = driver.Create(fname_out, dims[0], dims[1], 1, gdal.GDT_Float32)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ.ExportToWkt())
        outDs.GetRasterBand(1).WriteArray(Rain)
        outDs = None

        # ---- Ecriture ET0 ----

        fname_out = os.path.join(cf['path']["ERA5_tif"], "ET0"+"_"+lejour+".tif")
        if os.path.exists(fname_out):
            os.remove(fname_out)
        driver = gdal.GetDriverByName("GTiff")
        outDs = driver.Create(fname_out, dims[0], dims[1], 1, gdal.GDT_Float32)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ.ExportToWkt())
        outDs.GetRasterBand(1).WriteArray(ET0)
        outDs = None

        # ---- Ecriture Wind ----

        fname_out = os.path.join(cf['path']["ERA5_tif"], "Wind"+"_"+lejour+".tif")
        if os.path.exists(fname_out):
            os.remove(fname_out)
        driver = gdal.GetDriverByName("GTiff")
        outDs = driver.Create(fname_out, dims[0], dims[1], 1, gdal.GDT_Float32)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ.ExportToWkt())
        outDs.GetRasterBand(1).WriteArray(U2)
        outDs = None

    except:
        varnames = None
        pass

    return varnames


def Atm_Press(z):
    P = 101.3 * np.power(((293 - 0.0065*z)/293), 5.26)
    #if config.debug == 2 : print("Atm_Press", z, P)
    return P

def psychrometric_const(P):
    lb = 2.45
    cp = 1.013*0.001
    epsilon = 0.622
    gamma = (cp*P)/(epsilon*lb)
    gamma = 0.664742*0.001*P

    #if config.debug == 2 : print("psychrometric_const", P, gamma)
    return gamma

def e0t_from_tair(T):
	e0t = 0.6108*np.exp(17.27*T/(T+237.3))

	#if config.debug == 2 : print("e0t_from_tair", Tmean, e0t)
	return e0t

def msvp_day(Tmin, Tmax):
    es = (e0t_from_tair(Tmax)+e0t_from_tair(Tmin))/2.

    #if config.debug==2 : print("msvp_day", Tmin, Tmax, es)
    return es

def ssvp(T):
    delta = 4098 * 0.6108 * np.exp((17.27*T)/(T+237.3)) / np.power(237.3+T, 2)

    #if config.debug == 2 : print("ssvp", Tmean, delta)
    return delta

def ea_from_rhmean(T, rhmean):
    ea = e0t_from_tair(T)*rhmean/100.

    #if config.debug == 2 : print("ea_from_rhmean", Tmean, rhmean, ea)
    return ea

def Extraterrestrial_radiation(lat, jday):
    lat_rad = lat*pi/180.
    dr = 1 + 0.033 * cos(2*pi/365*jday)
    soldecl = 0.409*sin((2*pi/365*jday) - 1.39)
    sunset_angle = np.arccos(-np.tan(lat_rad)*tan(soldecl))

    ra = (24*60/pi)* 0.082 * dr * (sunset_angle * np.sin(lat_rad) * sin(soldecl) + np.cos(lat_rad) * cos(soldecl) * np.sin(sunset_angle))

    #if config.debug == 2 : print("Extraterrestrial_radiation", lat, jday, ra)
    return ra

def Clearsky_radiation_z(ra, z):
    rso = (0.75+0.00002*z)*ra

    #if config.debug == 2 : print("Clearsky_radiation_z:", ra, z, rso)
    return rso

def Net_shortwave_radiation(albedo, rs):
    rns = (1-albedo)*rs

    #if config.debug == 2 : print("Net_shortwave_radiation:", albedo, rs, rns)
    return rns

def Net_longwave_radiation(Tmin, Tmax, ea, rs, rso):
    stef_boltz = 4.903*pow(10, -9)

    Tmink = Tmin+273.16
    Tmaxk = Tmax+273.16

    rnl = stef_boltz * .5 * (np.power(Tmink, 4)+np.power(Tmaxk, 4)) * (0.34 -0.14*np.sqrt(ea)) * (1.35*(rs/rso)-0.35)

    #if config.debug==2 : print("Net_longwave_radiation:", Tmin, Tmax, ea, rs, rso, rnl)
    return rnl

def Net_Radiation(rns, rnl):
    rn = rns-rnl

    #if config.debug == 2 : print("Net_longwave_radiation:", rns, rnl, rn)
    return rn

def et0_pm2(P, T, Tmin, Tmax, es, ea, lat, jday, albedo, rs, u2, z):
    G = 0
    psy_const = psychrometric_const(P)
    #es = msvp_day(Tmin,Tmax)
    delta = ssvp(T)
    #ea = ea_from_rhmean(T,rhmean)
    ra = Extraterrestrial_radiation(lat, jday)
    rso = Clearsky_radiation_z(ra, z)
    rns = Net_shortwave_radiation(albedo, rs)
    rnl = Net_longwave_radiation(Tmin, Tmax, ea, rs, rso)
    rn = Net_Radiation(rns, rnl)
    et0 = (0.408*delta*(rn-G)+psy_const*(900./(T+273.))*u2*(es-ea))/(delta+psy_const*(1.+0.34*u2))

    #if config.debug == 2 : print("et0_pm2:", et0)
    return et0
