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
import os, sys
import numpy as np
import glob
import logging
import math
import dateutil
from osgeo import gdal, ogr, osr
from datetime import datetime
#------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


"""
============================================================================================
Synthesize a list of input raster files to different csv files using a classification shapefile
The zonal statistics are calculated with the prorata of the pixels entering into each polygon

The process is separated into four parts:

0) Init
1) Spatial Cross Shapefile with Raster File
2) Synthesis of each input file according to the proratas computed in part2
3) Temporal Synthesis and writing of CSV files

synthesize_init(shp_fn, shp_attrib):
    Initialize all the tables for a particular shapefile and its attribute

    Params:
        shp_fn: (String) Filename of the input shapefile to process
        shp_attrib: (String) Name of the attribute to process

    Return:
        table_att: List of attributes. As they are used as identifier, so that they should be unique !!!!
        table_id: a pointer table to the pixels id
        table_prop: proportion of that pixel to this shape
        table_output : weighted sum
        table_date: the date of the input data are taken from the input filename
        table_ha


synthesize_init_part2(shp_fn, shp_attrib):
    Initialize only the tables table_output,table_date,table_ha


synthesize_part1(infiles, shp_fn, shp_attrib,table_att,table_id,table_prop):
    Calculates the proratas between raster and vector files

    infiles is the list of TIFF files. The tiff files must of the same dimensions.

    Output:
    tempdir="j:\\drought_index\\fishnet"
fishnet_fn=os.path.join(tempdir,"fishnet2.tif")
vectfile=os.path.join(tempdir,"fishnet2.shp")

synthesize_part2(infiles, weap_fn, prefix,table_att,table_id,table_prop,table_output,table_date,table_ha)
synthesize_part3(infiles, weap_fn, prefix,table_att,table_id,table_prop,table_output,table_date,table_ha)

Inputs:
	infiles: a repertory with GeoTif Files with the names having thuis syntax: yyyy.mm.dd.tif
	shp_fn: a shappefile

Params:

	timerange: DAY WEEK or MONTH is the duration of accumulation
	mode: MEAN or SUM is how the final calculation is done
	shp_attrib: it is the name of the attribute from the shapefile that will be used for spatial agregation


Output:
	weap: a csv file in Weap21 format

	Intermediary files
	fishnet.shp: the vectorized shapefile from fishnet.tif


	The proportion of each pixel belonging to a shape is calculated (fishnet + intersection) then each input data file is synthesize based on the proportion and the input data

Remark:
   For ET, sum by month is different : 9 first days a percent of ET is used, and 9 first days of next month too with a percent of ET

  Author: Michel Le Page - 04/03/2014
  MODIFICATION : Michel, 05/02/2016, separation in subprocess, optimize file crossing, reuse fichnets files, error on last date corrected
# =========================================================================
"""

#!--------------------------------------------------------------------------------------
def synthesize_init(shp_fn, shp_attrib, tempdir, fishnet_fn, vectfile):

    if os.path.exists(tempdir) is False:
        os.mkdir(tempdir)

    shp1 = ogr.Open(shp_fn)
    if shp1 is None:
        print('Unable to open %s' % shp_fn)
        sys.exit(1)

    layer1 = shp1.GetLayer()

    table_id = []
    table_prop = []

    table_att = []
    table_output = []
    table_date = []
    table_ha = []

    for feature1 in layer1:
        attribute1 = feature1.GetField(shp_attrib)
        if attribute1 not in table_att:
            table_att.append(attribute1)
            table_date.append([])
            table_ha.append([])
            table_output.append([])
            table_id.append([])
            table_prop.append([])

    shp1.Destroy()

    return(table_att, table_id, table_prop, table_output, table_date, table_ha, tempdir, fishnet_fn, vectfile)

#!--------------------------------------------------------------------------------------
def synthesize_init_part2(shp_fn, shp_attrib):
    shp1 = ogr.Open(shp_fn)
    if shp1 is None:
        print('Unable to open %s' % shp_fn)
        sys.exit(1)

    layer1 = shp1.GetLayer()

    table_att = []
    table_output = []
    table_date = []
    table_ha = []

    for feature1 in layer1:
        attribute1 = feature1.GetField(shp_attrib)
        if attribute1 not in table_att:
            table_att.append(attribute1)
            table_date.append([])
            table_ha.append([])
            table_output.append([])

    shp1.Destroy()

    return(table_output, table_date, table_ha)

#!--------------------------------------------------------------------------------------
def synthesize_part1(infiles, shp_fn, shp_attrib, table_att, table_id, table_prop, tempdir, fishnet_fn, vectfile):
    logging.basicConfig(format='[L:%(lineno)d] [%(asctime)s]  %(message)s', level=20, datefmt='%m-%d %H:%M')

    logging.info("==== INIT SYNTHESIS ====")

    infile = infiles[0] # premier fichier de la liste pour récupérer les coordonnées

    inDs = gdal.Open(infile)
    if inDs is None:
        print('Unable to open %s' % infile)
        sys.exit(1)

    pj = inDs.GetProjection()
    cols = inDs.RasterXSize
    rows = inDs.RasterYSize
    driver = inDs.GetDriver()
    geo_t = inDs.GetGeoTransform()
    pixel_spacing = geo_t[1]

    # --------- REPROJECTION DU SHAPEFILE dans la projection des images ----
    if os.path.isfile(os.path.join(tempdir, 'shp_proj.shp')) is True:
        logging.info("=> Projected shapefile already exists. Using it! ")
    else:

        kk = ogr.osr.SpatialReference(pj)
        epsg = kk.GetAttrValue("GEOGCS|AUTHORITY", 1)

        logging.info("=> Reprojecting shape to EPSG:%s" % epsg)

        ogr2ogr = os.path.join(path_to_osgeo, 'ogr2ogr')
        os.system(ogr2ogr+' -t_srs EPSG:'+epsg+' "'+os.path.join(tempdir, 'shp_proj.shp')+'" "'+shp_fn+'"')
        shp_fn = os.path.join(tempdir, 'shp_proj.shp')

    # --------- CREATION D'UNE GRILLE NUMEROTEE AUX MEMES DIMENSIONS QUE LE FICHIER D'eNTREE ----
    if os.path.isfile(fishnet_fn) is True:
        logging.info("=> Sequentially numbered grid already exists. Using it!")
    else:
        logging.info("=> Creation of a sequentially numbered grid")

        print("Cols:", cols, "Ligs:", rows)

        outDs = driver.Create(fishnet_fn, cols, rows, 1, gdal.GDT_UInt32)
        if outDs is None:
            print('Unable to create %s' % fishnet_fn)
            sys.exit(1)

        outDs.SetGeoTransform(inDs.GetGeoTransform())
        outDs.SetProjection(inDs.GetProjection())

        aa = np.arange(rows*cols)
        aa = aa.reshape((rows, cols))
        bando = outDs.GetRasterBand(1)
        bando.WriteArray(aa)

        aa = 0

        outDs = None

    # --------- CREATION DU FISHNET A PARTIR DU FICHIER GRILLE (repris de gdal_polygonize.py) ----
    if os.path.isfile(vectfile) is True:
        logging.info("=> Fishnet already exists. Using it! ")
    else:
        logging.info("=> Creation of a fishnet shapefile ")

        format = 'GML'
        options = []
        quiet_flag = 0
        src_filename = None
        src_band_n = 1

        dst_filename = None
        dst_layername = None
        dst_fieldname = None
        dst_field = -1

        mask = 'default'

        gdal.AllRegister()

        src_filename = fishnet_fn
        dst_filename = vectfile
        dst_layername = dst_fieldname = 'fishnet'
        format = "ESRI shapefile"

        #	Open source file
        src_ds = gdal.Open(src_filename)

        if src_ds is None:
            print('Unable to open %s' % src_filename)
            sys.exit(1)

        srcband = src_ds.GetRasterBand(src_band_n)

        if mask is 'default':
            maskband = srcband.GetMaskBand()
        elif mask is 'none':
            maskband = None
        else:
            mask_ds = gdal.Open(mask)
            maskband = mask_ds.GetRasterBand(1)

        #       Try opening the destination file as an existing file.

        try:
            gdal.PushErrorHandler('CPLQuietErrorHandler')
            dst_ds = ogr.Open(dst_filename, update=1)
            gdal.PopErrorHandler()
        except:
            dst_ds = None

        # 	Create output file.

        if dst_ds is None:
            drv = ogr.GetDriverByName(format)
            if os.path.exists(dst_filename):
                drv.DeleteDataSource(dst_filename)
            if not quiet_flag:
                print('Creating output %s of format %s.' % (dst_filename, format))
            dst_ds = drv.CreateDataSource(dst_filename)

        # Find or create destination layer.

        try:
            dst_layer = dst_ds.GetLayerByName(dst_layername)
        except:
            dst_layer = None

        if dst_layer is None:

            srs = None
            if src_ds.GetProjectionRef() != '':
                srs = osr.SpatialReference()
                srs.ImportFromWkt(src_ds.GetProjectionRef())

            dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)

            if dst_fieldname is None:
                dst_fieldname = 'DN'

            fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
            dst_layer.CreateField(fd)
            dst_field = 0
        else:
            if dst_fieldname is not None:
                dst_field = dst_layer.GetLayerDefn().GetFieldIndex(dst_fieldname)
                if dst_field < 0:
                    print("Warning: cannot find field '%s' in layer '%s'" % (dst_fieldname, dst_layername))

        #	Invoke algorithm.
        if quiet_flag:
            prog_func = None
        else:
            prog_func = gdal.TermProgress

        result = gdal.Polygonize(srcband, maskband, dst_layer, dst_field, options)

        srcband = None
        src_ds = None
        dst_ds = None
        mask_ds = None

    # ------- MERGE THE TWO FILES AND CREATE a pointer table to the pixels id (table_id), proportion of that pixel to this shape (table_prop) -----------
    # table_att is one dimensional, it stores the id of the shape
    # table_output and table_date are not used in this step but later in the synthesis

    fn_table_id = os.path.join(tempdir, 'table_id0.csv')
    fn_table_prop = os.path.join(tempdir, 'table_prop0.csv')

    if (os.path.isfile(fn_table_id) is True and os.path.isfile(fn_table_prop) is True):
        logging.info("=> Intersections already exist. Using it! ")

        table_id = []
        table_prop = []

        for i in range(len(table_att)):
            fn_table_id = os.path.join(tempdir, 'table_id'+str(i)+'.csv')
            fn_table_prop = os.path.join(tempdir, 'table_prop'+str(i)+'.csv')
            table_prop.append([])
            table_id.append([])

            kkk = np.loadtxt(fn_table_id, ndmin=1)
            kkk1 = np.loadtxt(fn_table_prop, ndmin=1)

            for j in range(kkk.size):
                table_id[i].append(int(kkk[j]))
                table_prop[i].append(kkk1[j])

            print('.', end='')
            sys.stdout.flush()

    else:

        logging.info("=> Intersecting the vectorized grid and the shapefile")

        shp1 = ogr.Open(shp_fn)
        if shp1 is None:
            print('Unable to open %s' % shp_fn)
            sys.exit(1)

        shp2 = ogr.Open(vectfile)
        if shp2 is None:
            print('Unable to open %s' % vectfile)
            sys.exit(1)

        layer1 = shp1.GetLayer()
        layer2 = shp2.GetLayer()
        att2 = 'fishnet'

        # fenetre de croisement
        ras_xmin, ras_xmax, ras_ymin, ras_ymax = layer2.GetExtent()
        shp_xmin, shp_xmax, shp_ymin, shp_ymax = layer1.GetExtent()

        layer1.ResetReading()
        n = 0
        for feature1 in layer1:
            n = n + 1
            geom1 = feature1.GetGeometryRef()
            attribute1 = feature1.GetField(shp_attrib)
            feat_xmin, feat_xmax, feat_ymin, feat_ymax = geom1.GetEnvelope()
            win1_xmin = max(ras_xmin, feat_xmin)
            win1_xmax = min(ras_xmax, feat_xmax)
            win1_ymin = max(ras_ymin, feat_ymin)
            win1_ymax = min(ras_ymax, feat_ymax)

            #premier et dernier pixel à tester (la fenetre est une bande)
#            feat_firstgrid=int(((ras_ymax-win1_ymax)/pixel_spacing*cols)+((win1_xmin-ras_xmin)/pixel_spacing))
#            feat_lastgrid=int(((ras_ymax-win1_ymin)/pixel_spacing*cols)+((win1_xmax-ras_xmin)/pixel_spacing))

            y0 = int((ras_ymax-win1_ymax)/pixel_spacing)
            y9 = int((ras_ymax-win1_ymin)/pixel_spacing)
            x0 = int((win1_xmin-ras_xmin)/pixel_spacing)
            x9 = int((win1_xmax-ras_xmin)/pixel_spacing)

            lili = []
            for yyy in range(y0, y9):
                for xxx in range(x0, x9):
                    lili.append((yyy*cols)+xxx)

            print(n, attribute1, len(lili))

            #for i in range(feat_firstgrid,feat_lastgrid):
            for i in lili:
                feature2 = layer2.GetFeature(i)
                geom2 = feature2.GetGeometryRef()

                if geom2.Intersects(geom1):
                    attribute2 = feature2.GetField(att2)
                    intersection = geom2.Intersection(geom1)
                    #if intersection.IsValid() and intersection.GetDimension()==2:
                    if intersection.GetDimension() == 2:

                        a1 = geom2.GetArea()
                        a2 = intersection.GetArea()
                        proportion = a2/a1

                        k = table_att.index(attribute1)	# id de la zone

                        table_id[k].append(attribute2)	# id du piwel

                        table_prop[k].append(proportion)	# proportion de la zone couverte par ce pixel

                layer2.ResetReading()

        shp1.Destroy()
        shp2.Destroy()

        # ---- Sauvegarde des croisements en CSV
        np_id = np.array(table_id)
        np_prop = np.array(table_prop)

        for i in range(len(table_att)):
            fn_table_id = os.path.join(tempdir, 'table_id'+str(i)+'.csv')
            fn_table_prop = os.path.join(tempdir, 'table_prop'+str(i)+'.csv')
            np.savetxt(fn_table_id, np_id[i], fmt='%d', delimiter=',')
            np.savetxt(fn_table_prop, np_prop[i], fmt='%.3f', delimiter=',')

    return(table_id, table_prop)

#!--------------------------------------------------------------------------------------
def synthesize_part2(infiles, weap_fn, prefix, table_att, table_id, table_prop, table_output, table_date, table_ha, do_cumul='no', sep='.'):

    # --------- TIME SYNTHESIS:  -----------------
    # in this step, table_output and table_date are populated : the second dimension stores the weighted sum and the date of the input data
    # the date is taken from the file name. It can be modified here.

    logging.info("=> Synthesis to the intersected shapes")

    cumul = np.zeros(table_att.__len__())

    for infile in sorted(glob.glob(infiles)):
        # on fait confiance à l'opérateur: tt les fichiers sont fonctionnels et de la bonne dimension
        inDs = gdal.Open(infile)
        cols = inDs.RasterXSize
        rows = inDs.RasterYSize
        data = inDs.ReadAsArray()
        geo_t = inDs.GetGeoTransform()

        inDs = None
        data = data.reshape(rows*cols)	# reshape en 1 vecteur qui va correspondre aux ids de la table_id

        ladate = os.path.basename(infile)

        ladate = ladate.split(prefix)[1].split(".tif")[0]
        ladate = dateutil.parser.parse(ladate)

        if ladate.month == cf['agroyear']["begin"]:
            cumul = np.zeros(table_att.__len__())

        print(ladate)
        #ladate=ladate.replace('.','/')[0:10]	# la date au format yyyy/mm/dd

        toto = data*np.nan

        for k in range(table_att.__len__()): # pour tous les polygones du fichier classé
            #print(k)
            #somme=0.
            #poids=0.

            #toto=data*0
            #toto[table_id[k][:]] = 1
            toto[table_id[k][:]] = table_prop[k][:]
            moyenne = np.nansum(data[table_id[k][:]]*toto[table_id[k][:]])/np.nansum(toto[table_id[k][:]])
            if do_cumul == 'yes':
                cumul[k] = cumul[k]+moyenne
                table_output[k].append(cumul[k])
            else:
                table_output[k].append(moyenne)

            table_date[k].append(ladate)
            toto[table_id[k][:]] = np.nan          # remise à nan des pixels qu'on a allumé

    return(table_date, table_output, table_ha)

#!--------------------------------------------------------------------------------------
def synthesize_part3(infiles, shp_fn, weap_fn, prefix, table_att, table_id, table_prop, table_output, table_date, table_ha):
    nbdays = [31, 27, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # --------- Output to a CSV file in Weap21 format -----------------
    # this step uses table_date and table_output to make a temporal synthesis and output it to a csv file

    logging.info("=> Output to a CSV File")

    fout = open(weap_fn, 'w')

    # Ecriture de l'entete WEAP

    print("sep=,", file=fout)
    print("$ListSeparator = , ", file=fout)
    print("$DecimalSymbol = .", file=fout)
    print("# ---- Synthesize, SAMIR-FAO56 Simple - CESBIO-IRD 2015 -----", file=fout)
    print("# Input Raster Data: %s" % prefix, file=fout)
    print("# Input Shapefile: %s" % shp_fn, file=fout)
    if prefix == 'Temp_':
        unit = "C°"
    elif prefix == "Kc_":
        unit = 'no unit'
    else:
        unit = 'mm/day'
    print("# Unit: %s" % unit, file=fout)
    print("# Processing Date: %s" % datetime.now().strftime("%Y/%m/%d %H:%M"), file=fout)

    print("\n", file=fout, end="")

    # Ecriture des données mensuelles

    print("$Columns = Year, Month", file=fout, end="")

    for k in range(table_att.__len__()):
        print(",%s"  % prefix+table_att[k], file=fout, end="")
    print("\n", file=fout, end="")

    zedate = zedate0 = table_date[0][0]
    zeze = zedate.month
    vals = np.zeros(table_att.__len__())

    i = 0
    n = 0

    for i in range(table_date[0].__len__()):
    #while zedate<=table_date[0][table_date[0].__len__()-1]:			# boucle sur les dates
        zedate = table_date[0][i]
        zizi = zedate.month

        if zizi == zeze:
            n = n+1
            for k in range(table_att.__len__()):
                if len(table_output[k]) > 0:
                    vals[k] += table_output[k][i]                                          #Possible de Décommenter
        else:	# fin de la semaine ou du mois, on écrit
            # ----- entete de la ligne de sortie
            print("%04d, %02d" % (zedate0.year, zedate0.month))
            print("%04d, %02d" % (zedate0.year, zedate0.month), file=fout, end="")

                # ----- synthese ---
            vals = vals/n
            if unit == 'mm/month':
                vals = vals * nbdays[zeze-1]

            for k in range(table_att.__len__()):
                print(", %.2f" % (vals[k]), file=fout, end="")
            print("\n", file=fout, end="")

            # on a terminé la séquence on enregistre ce jour, et on initialise le compteur zeze
            zizi = zedate.month
            zeze = zedate.month

            # premier jour de la semaine ou du mois
            zedate0 = zedate
            n = 1
            vals = np.zeros(table_att.__len__())

            for k in range(table_att.__len__()):
                if len(table_output[k]) > 0:
                    vals[k] += table_output[k][i]

    if n > 0:
        print("%04d, %02d" % (zedate0.year, zedate0.month), file=fout, end="")
        vals = vals/n

        for k in range(table_att.__len__()):
            print(", %.2f" % (vals[k]), file=fout, end="")
        print("\n", file=fout, end="")

    fout.close()

#!--------------------------------------------------------------------------------------
def synthesize_part2_areas(infiles, shp_fn, weap_fn, prefix, table_att, table_id, table_prop, table_output, table_date, table_ha, do_cumul='no', sep='.', idzone=[3, 4, 5]):

    # --------- TIME SYNTHESIS:  -----------------
    # in this step, table_output and table_date are populated : the second dimension stores the weighted sum and the date of the input data
    # the date is taken from the file name. It can be modified here.

    logging.info("=> Synthesis of yearly areas of "+prefix)
    fout = open(weap_fn, 'w')

    # Ecriture de l'entete WEAP

    print("sep=,", file=fout)
    print("# ---- Synthesize, SAMIR-FAO56 Simple - CESBIO-IRD 2015 -----", file=fout)
    print("# Input Raster Data: %s" % infiles, file=fout)
    print("# Input Shapefile: %s" % shp_fn, file=fout)
    print("# Processing Date: %s" % datetime.now().strftime("%Y/%m/%d %H:%M"), file=fout)
    print("# Areas in hectares", file=fout)
    print("$ListSeparator = ,", file=fout)
    print("$DecimalSymbol = .", file=fout)
    print("$Columns = Year", file=fout, end="")

    for k in range(table_att.__len__()):
        print(",%s"  % prefix+str(table_att[k]), file=fout, end="")
    print("\n", file=fout, end="")

    for infile in sorted(glob.glob(infiles)):
        # on fait confiance à l'opérateur: tt les fichiers sont fonctionnels et de la bonne dimension
        inDs = gdal.Open(infile)
        cols = inDs.RasterXSize
        rows = inDs.RasterYSize
        data = inDs.ReadAsArray()
        geo_t = inDs.GetGeoTransform()
        kmlon = 111412.84*math.cos(geo_t[3]*math.pi/180) - 93.5*math.cos(3*geo_t[3]*math.pi/180)
        kmlat = 111132.92 - 559.82*math.cos(2*geo_t[3]*math.pi/180) + 1.175*math.cos(4*geo_t[3]*math.pi/180)

        """
	  m1 = 111132.92    # latitude calculation term 1
	  m2 = -559.82        # latitude calculation term 2
	  m3 = 1.175      # latitude calculation term 3
	  m4 = -0.0023        # latitude calculation term 4
	  p1 = 111412.84    # longitude calculation term 1
	  p2 = -93.5      # longitude calculation term 2
	  p3 = 0.118      # longitude calculation term 3

        lonrad = geo_t[0]*math.pi/180
        latrad = geo_t[3]*math.pi/180

	  # Calculate the length of a degree of latitude and longitude in meters
	  metersPerLat = m1 + (m2 * math.cos(2 * latrad)) + (m3 * math.cos(4 * latrad)) + (m4 * math.cos(6 * latrad))
	  metersPerLon = (p1 * math.cos(latrad)) + (p2 * math.cos(3 * latrad)) + (p3 * math.cos(5 * latrad))
       """

        table_ha[k].append(sum(table_prop[k])*geo_t[1]*kmlon*(-geo_t[5])*kmlat/10000.)	 	#Approximation 1°D = 111 km

        inDs = None
        data = data.reshape(rows*cols)	# reshape en 1 vecteur qui va correspondre aux ids de la table_id

        year = infile.split(prefix)[1].split('.tif')[0]
        print("%s" % (year))
        print("%s" % (year), file=fout, end="")

        for k in range(table_att.__len__()): # pour tous les polygones du fichier classé
            total = 0
            for id1 in idzone:
                sel = np.where(data[table_id[k][:]] == id1)
                #print(k,id1,len(sel[0]),'/',len(table_id[k][:]))
                total = total + np.nansum(np.array(table_prop[k][:])[sel])
#                total = total + np.nansum(np.array(table_prop[k][:]))
            total = total*geo_t[1]*kmlon*(-geo_t[5])*kmlat/10000.
            print(", %.2f" % (total), file=fout, end="")
        print("\n", file=fout, end="")

    fout.close()

    return()
    
#!--------------------------------------------------------------------------------------

class Croisement():
    def __init__(self, table_att, table_id, table_prop, table_output, table_date, table_ha):
        self.table_att = table_att
        self.table_id = table_id
        self.table_prop = table_prop
        self.table_output = table_output
        self.table_date = table_date
        self.table_ha = table_ha

#!--------------------------------------------------------------------------------------

def do_croisement_shape(shp_file="", shp_att="", prefix="", path_in="", tempdir=""):

    infiles = glob.glob(os.path.join(path_in, prefix+"*.tif"))	# input repertory for raster files. The files must have this format yyyy.mm.dd.tif
    
    fishnet_fn = os.path.join(tempdir, "fishnet2.tif")
    vectfile = os.path.join(tempdir, "fishnet2.shp")

    table_att, table_id, table_prop, table_output, table_date, table_ha, tempdir, fishnet_fn, vectfile = synthesize_init(shp_file, shp_att, tempdir, fishnet_fn, vectfile)
    table_id, table_prop = synthesize_part1(infiles, shp_file, shp_att, table_att, table_id, table_prop, tempdir, fishnet_fn, vectfile)
    
    croisement = Croisement(table_att, table_id, table_prop, table_output, table_date, table_ha) 
    
    return(croisement)

#!--------------------------------------------------------------------------------------
    
def do_synthese_areas(croisement, shp_file="", prefix="", path_in="", path_out="",):
    
    auj = datetime.now()
    auj = auj.strftime('%Y.%m.%d')
    
    weap_fn = os.path.join(path_in, "Areas_"+auj+".csv")
    infiles = os.path.join(path_out, prefix+"*.tif")

    synthesize_part2_areas(infiles, shp_file, weap_fn, prefix, croisement.table_att, croisement.table_id, croisement.table_prop, croisement.table_output, croisement.table_date, croisement.table_ha, do_cumul='no', sep='.', idzone=[3, 4, 5])

    return(croisement)

#!--------------------------------------------------------------------------------------

def do_synthese_classes(croisement, shp_file="", prefix="", path_in="", path_out="", path_rel=""):
    
    auj = datetime.now()
    auj = auj.strftime('%Y.%m.%d')
    
    for key in path_rel:
                val = path_rel[key][0]
                weap_fn = os.path.join(path_in, "Areas_"+key+'_'+auj+".csv")
                infiles = os.path.join(path_out, prefix+"*.tif")
                mET_weap.synth.synthesize_part2_areas(infiles, shp_file, weap_fn, prefix, croisement.table_att, croisement.table_id, croisement.table_prop, croisement.table_output, croisement.table_date, croisement.table_ha, do_cumul='no', sep='.', idzone=[val])

    return(croisement)

#!--------------------------------------------------------------------------------------

def do_synthese(croisement, shp_file="", shp_att="", prefix="", path_in="", path_out=""):
    
    auj = datetime.now()
    auj = auj.strftime('%Y.%m.%d')
    
    infiles = os.path.join(os.path.join(path_in, prefix+"*.tif"))	# input repertory for raster files. The files must have this format yyyy.mm.dd.tif
    weap_fn = os.path.join(path_out, prefix+auj+".csv")

    croisement.table_output, croisement.table_date, croisement.table_ha = synthesize_init_part2(shp_file, shp_att)
    croisement.table_date, croisement.table_output, croisement.table_ha = synthesize_part2(infiles, weap_fn, prefix, croisement.table_att, croisement.table_id, croisement.table_prop, croisement.table_output, croisement.table_date, croisement.table_ha, sep='-')
    synthesize_part3(infiles, shp_file, weap_fn, prefix, croisement.table_att, croisement.table_id, croisement.table_prop, croisement.table_output, croisement.table_date, croisement.table_ha)

    return(croisement)

#!--------------------------------------------------------------------------------------
