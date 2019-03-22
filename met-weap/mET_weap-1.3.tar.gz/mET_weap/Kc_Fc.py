# Copyright (C) 2014-2018 Michel Le Page, Cindy Gosset
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
import gdal
import xlrd
import numpy as np
from datetime import timedelta
from math import factorial
from scipy.interpolate import InterpolatedUnivariateSpline
from mET_weap import utils
#---------------------------------------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


"""
Created on Mon Mar 16 12:47:56 2015

@author: gossetc

Script de calcul des paramètres Fc et Kc pour chaque dates de NDVI
Entrée :
tableaux de paramètres ndvi_kckcb et NDVI-FC
Os tif calculé à partir des NDVI
les NDVI qu'il faut penser à diviser par 10 000

Sortie :
Kc pour chaque date NDVI en tif sur la zone
Fc
"""


##############################################################################################
#                                       DEFINITION FONCTION LISSAGE                          #
##############################################################################################
def savitzky_golay(y, window_size, order, deriv=0, rate=1):                                  #
                                                                                             #
    try:                                                                                     #
        window_size = np.abs(np.int(window_size))                                            #
        order = np.abs(np.int(order))                                                        #
    except ValueError:                                                                      #
        raise ValueError("window_size and order have to be of type int")                     #
    if window_size % 2 != 1 or window_size < 1:                                              #
        raise TypeError("window_size size must be a positive odd number")                    #
    if window_size < order + 2:                                                              #
        raise TypeError("window_size is too small for the polynomials order")                #
    order_range = range(order+1)                                                             #
    half_window = (window_size -1) // 2                                                      #
    # precompute coefficients                                                                #
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])    #
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)                          #
    # pad the signal at the extremes with                                                    #
    # values taken from the signal itself                                                    #
    firstvals = y[0]-np.abs(y[1:half_window+1][::-1]-y[0])                                   #
    lastvals = y[-1]+np.abs(y[-half_window-1:-1][::-1]-y[-1])                                #
    y = np.concatenate((firstvals, y, lastvals))                                             #
    return np.convolve(m[::-1], y, mode='valid')                                             #
##############################################################################################

#parcourir le Fc_i et kc_i première dimension (temps) sur chaque pixel (une colonne et une ligne à la fois)
#####################################################################################################
#                                 definition de la fonction de localisation des extrèmes            #
#####################################################################################################
def local_min_max(datafc, datakcmid):                                                               #
                                                                                                    #
    metrics_local_max = []                                                                          #
    metrics_local_min = []                                                                          #
    kmid_prec = 0                                                                                   #
    sous_vecteur = list()                                                                           #
    Vecteur = list()                                                                                #
    for i in range(len(datakcmid)):                                                                 #
        if datakcmid[i] == kmid_prec:                                                               #
            if datakcmid[i] > 0:                                                                    #
                sous_vecteur.append(i)                                                              #
        else:                                                                                       #
            if len(sous_vecteur) > 0:                                                               #
                Vecteur.extend([sous_vecteur])                                                      #
            sous_vecteur = list()                                                                   #
            kmid_prec = datakcmid[i]                                                                #
            if datakcmid[i] > 0:                                                                    #
                sous_vecteur.append(i)                                                              #
        if i == range(len(datakcmid))[-1]:                                                          #
            if len(sous_vecteur) > 0:                                                               #
                if len(Vecteur) == 0 or Vecteur[-1][-1] != sous_vecteur[-1]:                        #
                    Vecteur.extend([sous_vecteur])                                                  #
    for n in range(len(Vecteur)):                                                                   #
        m_l_max = list()                                                                            #
        m_l_min = list()                                                                            #
        if n == 0:                                                                                  #
            local_max = (np.diff(np.sign(np.diff(datafc[Vecteur[n]]))) < 0).nonzero()[0] + 1        #
            local_min = (np.diff(np.sign(np.diff(datafc[Vecteur[n]]))) > 0).nonzero()[0] + 1        #
            for l in local_max:                                                                     #
                m_l_max.append(Vecteur[n][l])                                                       #
            metrics_local_max = np.array(m_l_max)                                                   #
            for l in local_min:                                                                     #
                m_l_min.append(Vecteur[n][l])                                                       #
            metrics_local_min = np.array(m_l_min)                                                   #
        else:                                                                                       #
            local_max = (np.diff(np.sign(np.diff(datafc[Vecteur[n]]))) < 0).nonzero()[0] + 1        #
            local_min = (np.diff(np.sign(np.diff(datafc[Vecteur[n]]))) > 0).nonzero()[0] + 1        #
            for l in local_max:                                                                     #
                m_l_max.append(Vecteur[n][l])                                                       #
            metrics_local_max = np.r_[metrics_local_max, np.array(m_l_max)]                         #
            for l in local_min:                                                                     #
                m_l_min.append(Vecteur[n][l])                                                       #
            metrics_local_min = np.r_[metrics_local_min, np.array(m_l_min)]                         #
    return metrics_local_min, metrics_local_max                                                     #
#####################################################################################################


def KC_FC_calc(prefix, from_year, to_year):

    # ------- Loading Tables KC and FC -------

    print("importation des tables de paramètre Kc et Fc et des valeurs OS")
    #table de KcKcb excel
    Ndvi_KcKcb = xlrd.open_workbook(cf['Relation_NDVI']['Ndvi_KcKcb'])
    feuille = Ndvi_KcKcb.sheet_names()
    excel_Kc = Ndvi_KcKcb.sheet_by_name(feuille[0])
    head_Kc = excel_Kc.row_values(0)[2:] #noms des colonnes conservées
    for i in range(len(head_Kc)):
        if i == 0:
            rel_Kc = np.array(excel_Kc.col_values(i+2)[1:])
        else:
            rel_Kc = np.c_[rel_Kc, np.array(excel_Kc.col_values(i+2)[1:])]
    #table de Fc excel
    Ndvi_Fc = xlrd.open_workbook(cf['Relation_NDVI']['Ndvi_Fc'])
    feuille = Ndvi_Fc.sheet_names()
    excel_Fc = Ndvi_Fc.sheet_by_name(feuille[0])
    head_Fc = excel_Fc.row_values(0)[2:-1] #noms des colonnes conservées
    for i in range(len(head_Fc)):
        if i == 0:
            rel_Fc = np.array(excel_Fc.col_values(i+2)[1:])
        else:
            rel_Fc = np.c_[rel_Fc, np.array(excel_Fc.col_values(i+2)[1:])]

    # ----- Loading Yearly LandCover --------

    #rel_Os = colonne 1:Val_os , colonne 2:Val_line_Kc, colonne 3: Val_line_Fc
    nb_class = len(cf['Relation_NDVI']['rel_OS'])
    rel_Os = np.zeros((nb_class, 3))

    i = 0
    for key in cf['Relation_NDVI']['rel_OS'].keys():
        print(key, cf['Relation_NDVI']['rel_OS'][key])
        rel_Os[i, 0] = cf['Relation_NDVI']['rel_OS'][key][0]
        rel_Os[i, 1] = cf['Relation_NDVI']['rel_OS'][key][1]
        rel_Os[i, 2] = cf['Relation_NDVI']['rel_OS'][key][2]
        i = i+1

    print(rel_Os)

    for year in range(from_year, to_year+1):

        print(" ======== YEAR ", year, " ==========")
        
        # ------ Land Cover ERA5 file ------

        Os = gdal.Open(os.path.join(cf['path']["outputs_ERA5"], 'class_'+str(year)+'.tif'))
        cols = Os.RasterXSize
        rows = Os.RasterYSize
        GT = Os.GetGeoTransform()
        PJ = Os.GetProjection()
        np_os = Os.ReadAsArray()
        Os = None

        # ----- Loading Linear relations --------

        print('Preparing linear relations')

        np_akc = np.zeros((rows, cols))
        np_bkc = np.zeros((rows, cols))
        np_afc = np.zeros((rows, cols))
        np_bfc = np.zeros((rows, cols))
        np_mask_calc_ndvi = np.zeros((rows, cols))
        np_mask_calc_fc = np.zeros((rows, cols))

        np_mask_calc_Kc = np.zeros((rows, cols))
        np_mask_calc_Kcb = np.zeros((rows, cols))

        np_ke = np.zeros((rows, cols))
        np_fc_prolong = np.zeros((rows, cols))
        for line in range(rows): #parcours des lignes
        #listes des Kcmid Kcb et Ke par ligne pour une date
            for col in range(cols): #parcours par colonne
                #kc = np_kc = np_fc = fc = None
                #np_akc = np_bkc = np_afc = np_bfc = None #remise à zeros a chaque nouveau pixel
                #recuperation indices de ligne des tableau NDVi_Fc et KcKcb pour chaque valuer de OS des pixel

                aaa = np.where(rel_Os[:, 0] == np_os[line, col])

                if len(aaa[0]) == 0:
                    ind_k = ind_f = float('NaN')

                else:
                    ind_k = rel_Os[aaa, 1][0][0]
                    ind_f = rel_Os[aaa, 2][0][0]

                #si il n'ya pas de ligne on assigne a kc et fc la valeur 0 (depend de la classe OS)
                if ind_k != ind_k: # if ind_k is nan
                    np_akc[line, col] = 0
                    np_akc[line, col] = 0
                    np_ke[line, col] = 0
                    np_mask_calc_ndvi[line, col] = 0
                    np_mask_calc_fc[line, col] = 0
                    np_mask_calc_Kc[line, col] = 0
                    np_mask_calc_Kcb[line, col] = 0

                else: #sinon calcul
                    ind_k = int(ind_k)
                    np_akc[line, col] = rel_Kc[ind_k, 0]
                    np_bkc[line, col] = rel_Kc[ind_k, 1]

                    if rel_Kc[ind_k, 2] == 2:
                        np_mask_calc_ndvi[line, col] = 0
                        np_mask_calc_fc[line, col] = 1
                    else:
                        np_mask_calc_ndvi[line, col] = 1
                        np_mask_calc_fc[line, col] = 0

                    if rel_Kc[ind_k, -1] == 1:
                        np_mask_calc_Kc[line, col] = 1
                        np_mask_calc_Kcb[line, col] = 0
                    else:
                        np_mask_calc_Kc[line, col] = 0
                        np_mask_calc_Kcb[line, col] = 1

                    np_ke[line, col] = rel_Kc[ind_k, 3]

                if ind_f != ind_f:  # if ind_f is nan
                    np_afc[line, col] = 0
                    np_bfc[line, col] = 0
                    np_fc_prolong[line, col] = 0
                else: #sinon calcul
                    ind_f = int(ind_f)
                    np_afc[line, col] = rel_Fc[ind_f, 0]
                    np_bfc[line, col] = rel_Fc[ind_f, 1]
                    np_fc_prolong[line, col] = rel_Fc[ind_f, 2]

        # ----- Loading NDVIS --------

        print('Loading NDVIs')

        Noms_ndvi = utils.select_files_agroyear_all(cf['path']["MOD13Q1_tif"], prefix, year, year)

        Dates_ndvi = list()
        short_ndvi = list()

        NDVI1 = gdal.Open(Noms_ndvi[0])
        NDVI = NDVI1.ReadAsArray() * cf['Relation_NDVI']['scale_factor']
        cols = NDVI1.RasterXSize
        rows = NDVI1.RasterYSize
        driver = NDVI1.GetDriver()
        GT = NDVI1.GetGeoTransform()
        PJ = NDVI1.GetProjection()
        ladate, ladate_datetime = utils.get_date_modis(Noms_ndvi[0], prefix)
        print("NDVI ", ladate)
        short_ndvi.append(ladate)
        Dates_ndvi.append(ladate_datetime)

        NDVI = np.append([NDVI], [gdal.Open(Noms_ndvi[1]).ReadAsArray() * cf['Relation_NDVI']['scale_factor']], axis=0)
        ladate, ladate_datetime = utils.get_date_modis(Noms_ndvi[1], prefix)
        print("NDVI ", ladate)
        short_ndvi.append(ladate)
        Dates_ndvi.append(ladate_datetime)

        for fname in Noms_ndvi[1:]:
            ladate, ladate_datetime = utils.get_date_modis(fname, prefix)
            print("NDVI ", ladate)
            short_ndvi.append(ladate)
            Dates_ndvi.append(ladate_datetime)

            NDVI = np.append(NDVI, [gdal.Open(fname).ReadAsArray() * cf['Relation_NDVI']['scale_factor']], axis=0)

        # set NDVI<0 to zero
        NDVI[NDVI < 0] = 0

        # -----  Compute Linear Relations ------

        print('Fraction Cover')

        np_fc = np.minimum(np.maximum(np_afc*NDVI + np_bfc, 0), 1)

        if cf['Relation_NDVI']['do_senescence']:
            np_fc = np_fc.reshape(NDVI.shape[0], np_os.size)	# redimensionnement np_os.size=dimensions en X*Y, NDVI.shape[0] = nombre de jours
            np_fc_prolong = np_fc_prolong.reshape(np_os.size)	# redimensionnement np_os.size=dimensions en X*Y, NDVI.shape[0] = nombre de jours
            compteur = np_os.size/100
            window_size = NDVI.shape[0] - 3
            order = 4
            if window_size%2 == 0: window_size = window_size - 1
            if window_size < 6: order = 3
            print("window_size:", window_size)

            for k in range(np_os.size):
                if k % compteur == 0:
                    print('.', end='', flush=True)

                if np_fc_prolong[k] > 0:

                    np_fc[:, k] = savitzky_golay(np_fc[:, k], window_size, order, deriv=0, rate=1)
                    np_fc[:, k] = np.maximum(np_fc[:, k], 0)

                    l_max = ((np.diff(np.sign(np.diff(np_fc[:, k]))) < 0).nonzero()[0] + 1)
                    l_min = ((np.diff(np.sign(np.diff(np_fc[:, k]))) > 0).nonzero()[0] + 1)

                    for l0 in l_max:
                        aa = np.where(np.array(l_min) > l0)[0]
                        if np.size(aa) > 0:
                            l1 = l_min[np.min(aa)]
                            if np_fc[l0, k]-np_fc[l1, k] > 0.2:
                                #duree = Dates_ndvi[long[l1]]-Dates_ndvi[long[l0]]
                                #duree = duree.days
                                #duree = min(duree, np_fc_prolong[k])
                                duree = min(l1-l0, np_fc_prolong[k])  # ndvi au pdt journalier

                                fin = min(duree+l0, np_fc[:, k].size)
                                list_duree = np.arange(l0, int(fin))
                                np_fc[list_duree, k] = np_fc[l0, k]

            np_fc = np_fc.reshape(NDVI.shape[0], NDVI.shape[1], NDVI.shape[2])	# redimensionnement np_os.size = dimensions en X*Y, NDVI.shape[0] = nombre de jours

        print('\n  Crop Coefficient')
        # somme de deux equations: (a*NDVI+b) + (a*fc+b). Chaque équation est masquée en fonction de l'OS par np_mask_calc_ndvi et np_mask_calc_fc
        np_kc = np.maximum((np_akc*NDVI + np_bkc), 0)*np_mask_calc_ndvi + np.maximum((np_akc*np_fc + np_bkc), 0)*np_mask_calc_fc

        # on libère de la mémoire
        NDVI = 0
        # calcul supplémentaire si on on calculé un Kcb et non un Kc

        np_kc = np.maximum((np_mask_calc_Kcb * (np_kc + ((np_fc > 0.05) * (1-np_fc) * np_ke))) + (np_mask_calc_Kc * np_kc), 0)

        # -----  Write outputs ------

        print("  Ecriture des KC et FC.tif")
        i = 0
        for ladate in short_ndvi:            
            outDs = driver.Create(os.path.join(cf['path']["outputs_ERA5"], 'Kc_'+ladate+'.tif'), cols, rows, 1, gdal.GDT_Float32)
            outDs.SetGeoTransform(GT)
            outDs.SetProjection(PJ)
            bando = outDs.GetRasterBand(1)
            bando.WriteArray(np_kc[i, :, :])
            del outDs

            outDs = driver.Create(os.path.join(cf['path']["outputs_ERA5"], 'Fc_'+ladate+'.tif'), cols, rows, 1, gdal.GDT_Float32)
            outDs.SetGeoTransform(GT)
            outDs.SetProjection(PJ)
            bando = outDs.GetRasterBand(1)
            bando.WriteArray(np_fc[i, :, :])
            del outDs
            i = i+1
            
            #----------------------------------------------------------------------------
            
        if cf['Relation_NDVI']['do_stack']:
            print("Ecriture des stacks.tif")
            outDs = driver.Create(os.path.join(cf['path']["outputs_ERA5"], 'Stack_Kc_'+short_ndvi[0]+'-'+short_ndvi[-1]+'.tif'), cols, rows, len(short_ndvi), gdal.GDT_Float32)
            outDs.SetGeoTransform(GT)
            outDs.SetProjection(PJ)
            for bande in range(len(short_ndvi)):
                bando = outDs.GetRasterBand(bande+1)
                bando.WriteArray(np_kc[bande, :, :])
            del outDs

            outDs = driver.Create(os.path.join(cf['path']["outputs_ERA5"], 'Stack_Fc_'+short_ndvi[0]+'-'+short_ndvi[-1]+'.tif'), cols, rows, len(short_ndvi), gdal.GDT_Float32)
            outDs.SetGeoTransform(GT)
            outDs.SetProjection(PJ)
            for bande in range(len(short_ndvi)):
                bando = outDs.GetRasterBand(bande+1)
                bando.WriteArray(np_fc[bande, :, :])
            del outDs

        # -----  end of for(year) ------

    # -----  Finished ------

import PIL

def PIL_resize(img, shape):
    PILshape = (shape[1], shape[0])
    pix = PIL.Image.fromarray(img)
    pix = pix.resize(PILshape, PIL.Image.BICUBIC)
    #pix=pix.rotate(90)
    return np.array(pix)


def ET_actual_ERA5(from_year, to_year, Kc_path, ET0_path, out_path, prefix_Kc, prefix_ET0, prefix_ETa, echelle):

    for year in range(from_year, to_year+1):
        print(" ======== YEAR ", year, " ==========")

        Noms_Kc = utils.select_files_agroyear_all(cf['path']["outputs_ERA5"], "Kc", year, year)
        Noms_ET0 = utils.select_files_agroyear_all(cf['path']["outputs_ERA5"], "ET0", year, year)

        short_ndvi, Dates_ndvi = utils.get_date_modis(Noms_Kc, "Kc")
        short_ET0, Dates_ET0 = utils.get_date_modis(Noms_ET0, "ET0")

        #import des ndvi pour chaque dates mod13Q1
        print(" Reading data...")
        for j in range(len(short_ndvi)):
            if j == 0:
                NDVI1 = gdal.Open(os.path.join(Kc_path, prefix_Kc+'_'+short_ndvi[j]+'.tif'))
                NDVI = NDVI1.ReadAsArray()
                cols = NDVI1.RasterXSize
                rows = NDVI1.RasterYSize
                driver = NDVI1.GetDriver()
                GT = NDVI1.GetGeoTransform()
                PJ = NDVI1.GetProjection()
                NDVI1 = None
            elif j == 1:
                NDVI = np.append([NDVI], [gdal.Open(os.path.join(Kc_path, prefix_Kc+'_'+short_ndvi[j]+'.tif')).ReadAsArray()], axis=0)
            else:
                NDVI = np.append(NDVI, [gdal.Open(os.path.join(Kc_path, prefix_Kc+'_'+short_ndvi[j]+'.tif')).ReadAsArray()], axis=0)

        delta = (Dates_ndvi[len(Dates_ndvi)-1]-Dates_ndvi[0]).days
        nb_files = len(Noms_Kc)
        Das = np.arange(0, delta)

        if delta != nb_files:
            print(" Temporal interpolation...", delta, rows, cols)
            new_NDVI = np.zeros((delta, rows, cols)) #contiendra 16 dates

            xi = np.zeros(len(Dates_ndvi))

            for i in range(len(Dates_ndvi)):
                xi[i] = (Dates_ndvi[i]-Dates_ndvi[0]).days

            for r in range(rows):
                for c in range(cols):
                    #yi = NDVI[:,r,c]
                    s = InterpolatedUnivariateSpline(xi, NDVI[:, r, c], k=1)
                    new_NDVI[:, r, c] = s(Das)

            #sortir new_NDVI avec Dates correspondant à idas
            print(" Writing output...")
            for d in Das:
                day = Dates_ndvi[0]+timedelta(float(d))
                print(day.strftime('%Y-%m-%d'))
                fname_ET0 = os.path.join(ET0_path, prefix_ET0+'_'+day.strftime('%Y-%m-%d')+'.tif')

                if os.path.exists(fname_ET0):
                    ds = gdal.Open(fname_ET0)
                    ET0 = ds.ReadAsArray()
                    if echelle != 1:
                        ET0 = PIL_resize(ET0, (new_NDVI.shape[1], new_NDVI.shape[2]))
                    ds = None

                    fname_out = os.path.join(out_path, prefix_ETa+'_'+day.strftime('%Y.%m.%d')+'.tif')
                    if os.path.exists(fname_out):
                        os.remove(fname_out)
                    outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Float32)
                    outDs.SetGeoTransform(GT)
                    outDs.SetProjection(PJ)
                    bando = outDs.GetRasterBand(1)
                    bando.WriteArray(new_NDVI[d, :, :]*ET0)
                    outDs = None
        else:
            for d in Das:
                day = Dates_ndvi[0]+timedelta(float(d))
                fname_ET0 = os.path.join(ET0_path, prefix_ET0+'_'+day.strftime('%Y-%m-%d')+'.tif')

                if os.path.exists(fname_ET0):
                    ds = gdal.Open(fname_ET0)
                    ET0 = ds.ReadAsArray()
                    ds = None

                    fname_out = os.path.join(out_path, prefix_ETa+'_'+day.strftime('%Y.%m.%d')+'.tif')
                    if os.path.exists(fname_out):
                        os.remove(fname_out)
                    outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Float32)
                    outDs.SetGeoTransform(GT)
                    outDs.SetProjection(PJ)
                    bando = outDs.GetRasterBand(1)
                    bando.WriteArray(new_NDVI[d, :, :]*ET0)
                    outDs = None


        # -----  end of for(year) ------

    # -----  Finished ------
