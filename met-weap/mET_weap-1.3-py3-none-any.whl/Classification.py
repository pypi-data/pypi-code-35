# Copyright (C) 2014-2018 Michel Le Page, Oulad Sayad Younes, Cindy Gosset
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
from __future__ import division
from osgeo import gdal
import os
import numpy as np
#------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------

"""
Script de determination d'occupation du sol d'une zone specifier

Syntaxe : Python Classification.py [nom_dossier]

-------------------------------------------------------------------------"

ce script sert a determiner l'occupation du sol d'une zone precise en utilisant l'ensemble des images de cette zone dans une année precise
pour lancer le script veuillez utiliser la commande suivante : python Classification.py [2013.09.01 2014.08.31]
le dossier doit contenir les images de la zone a determiner l'occupation du sol

Realiser par : Michel Le Page/ Oulad Sayad Younes
Date Debut : 01/12/2014
Modifié par Gosset Cindy (05/03/2015)
Entrée
Image tif MODIS du ndvi
Paramètres des seuil SN, ANU et DEV
Sortie image tif d'os par an à la taille des image MODIS (Etendue et pixel)
--------------------------------------------------------------------------
"""


def classif_ijrs1997(list_fnames, fname_out, valsn=0.22, valanu=0.38, valdev=0.32):

    do_stack = True
    #Faire des seuils des paramètres pour la table de contingence
    seuil_sn = float(valsn)
    seuil_anu = float(valanu)
    seuil_dev = float(valdev)

    Images = []
    bands = 0

    for myfile in list_fnames: # on liste les fichiers HDF du dossier n un par un

        #decouper le chemin pour recuperer la date de l'image TIF
        #date=myfile.split('\\')
        #dateimage=date[len(date)-1].split('.tif')[0].split('_')[-1]
        if os.path.exists(myfile):
            bands += 1
            Images.append(myfile)

    if len(Images) > 0:
        #lecture des dimensions de la première image
        raster = gdal.Open(Images[0])
        cols = raster.RasterXSize
        rows = raster.RasterYSize
        driver = raster.GetDriver()
        GT = raster.GetGeoTransform()
        PJ = raster.GetProjection()
        raster = None

        #initialisation de la matrice tri-dimensionelle
        ndvis = np.zeros((bands, rows, cols)) # ndvis=np.zeros((nb_matrice,lignes,colonnes))
        print("Dates=", bands, "Rows=", rows, "Cols=", cols, "seuil_sn=", seuil_sn, "seuil_anu=", seuil_anu, "seuil_dev=", seuil_dev)

        bande = 0
        for myfile in Images:
            print(myfile)

            #lecture de l'image avec GDAL
            raster = gdal.Open(myfile)
            imarray = np.array(raster.ReadAsArray())

            # Calcul du NDVI de chaque Image
            imarray[imarray < 0] = 0
            ndvis[bande, :, :] = imarray * cf['Relation_NDVI']['scale_factor']
            bande += 1

            # fermeture de l'image
            raster = None

        code_NC = 1
        code_ASN = 4
        code_AVG = 3
        code_SN = 8
        code_ADV = 2
        code_CA = 5

        minndvi = np.min(ndvis, 0)
        maxndvi = np.max(ndvis, 0)

       #***** DEBUT DE CLASSIFICATION
        print("Classification : ")

        classif = np.zeros((rows, cols), np.byte)

        NT = 0  #Vide
        CA = 0  #Culture Annuelle
        ADV = 0 #Adventice
        SN = 0  #Sol Nu
        ASN = 0 #Arbre sur Sol Nu
        AVG = 0 #Arbre sur Vegetation
        NC = 0  #Non Classé
        classes = []

        ligne = 0
        for colonne in range(cols-1):
            for ligne in range(rows-1):

                maxmin = maxndvi[ligne, colonne]-minndvi[ligne, colonne]
                min_ndvi = minndvi[ligne, colonne]
                max_ndvi = maxndvi[ligne, colonne]
                NTi = CAi = ADVi = SNi = ASNi = AVGi = 0

                if max_ndvi == 0:
                    classes.append(' 000 ')
                    classif[ligne, colonne] = code_NC
                    NT += 1
                    NTi = 1

                else:
                    if min_ndvi <= seuil_sn: # if min_ndvi <= seuil_sn: ANNUELLES
                    # ***** CULTURE ANNUELLE : min_ndvi <= seuil_sn && max_ndvi > seuil_anu
                        if max_ndvi > seuil_anu:
                            classes.append(' C_A ')
                            classif[ligne, colonne] = code_CA
                            CA += 1
                            CAi = 1

                            # ***** ADVENTICE : min_ndvi < seuil_sn && max_ndvi < seuil_anu
                        elif ((max_ndvi > seuil_sn) and (max_ndvi <= seuil_anu)):
                            classes.append(' ADV ')
                            classif[ligne, colonne] = code_ADV
                            ADV += 1
                            ADVi = 1

                            # ***** SOL NU: min_ndvi < seuil_sn && max_ndvi < seuil_ssn
                        elif max_ndvi <= seuil_sn:
                            classes.append(' S_N ')
                            classif[ligne, colonne] = code_SN
                            SN += 1
                            SNi = 1

                    else:	# if min_ndvi > seuil_sn: ARBRES
                    #***** ARBRE SUR SOL NU : min_ndvi > seuil_sn && max_ndvi- min_ndvi < seuil_dev
                        if  maxmin <= seuil_dev:
                            classes.append(' ASN ')
                            classif[ligne, colonne] = code_ASN
                            ASN += 1
                            ASNi = 1

                            # ***** ARBRE SUR VEGETATION : min_ndvi > seuil_sn && max_ndvi- min_ndvi > seuil_dev
                        elif maxmin > seuil_dev:
                            classes.append(' AVG ')
                            classif[ligne, colonne] = code_AVG
                            AVG += 1
                            AVGi = 1

                    if (NTi+CAi+ADVi+SNi+ASNi+AVGi) == 0:
                        classes.append(' XXX ')
                        NC += 1

                    # FIN DE CLASSIFICATION
        print("VIDE = " + str(NT) + " 5-CA = " + str(CA) + " 2-ADVs = " + str(ADV) + " 8-SN =" + str(SN) + " 4-ASN =" + str(ASN) + " 3-AVG = " + str(AVG))

        outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Byte)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ)
        bando = outDs.GetRasterBand(1)
        bando.WriteArray(classif)
        ct = gdal.ColorTable()
        for i in range(255):
            ct.SetColorEntry(i, (255, 255, 255, 255))
        ct.SetColorEntry(4, (75, 150, 0, 0))
        ct.SetColorEntry(3, (75, 230, 0, 0))
        ct.SetColorEntry(8, (170, 110, 0, 0))
        ct.SetColorEntry(2, (255, 235, 175, 0))
        ct.SetColorEntry(5, (230, 255, 0, 0))
        ct.SetColorEntry(1, (255, 255, 255, 255))
        bando.SetRasterColorTable(ct)

        outDs = None

        if do_stack == True:
            fname_out = fname_out.replace('class', 'stack')
            outDs = driver.Create(fname_out, cols, rows, bands, gdal.GDT_Float32)
            outDs.SetGeoTransform(GT)
            outDs.SetProjection(PJ)
            for bande in range(bands):
                bando = outDs.GetRasterBand(bande+1)
                bando.WriteArray(ndvis[bande, :, :])
            outDs = None

    else:
        print("no image to class")
