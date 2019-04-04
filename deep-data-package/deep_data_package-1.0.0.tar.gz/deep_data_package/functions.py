#########################################################################
#
# Copyright (C) 2019 Team Deep-Data, Colorado School of Mines
#
# Date created: 1/22/19
# Date last updated:
#
# Creators:
#   - Sean Smith            seansmith@mines.edu
#   - Tyler Murphy          tmurphy@mines.edu
#   - Tyler Blount          trblount@mines.edu
#   - Sydney Nelson         snelson1@mines.edu
#   - Josh Grego            jgrego@mines.edu
#   - Jake Steiner          msteiner@mines.edu
#   - Marcelo Gonzales      magonzal@mines.edu
#   - Daniel Hanuszczak     danielhanuszczak@mines.edu
#
#########################################################################

from .band_ratios import *

'''
Module for calculating band ratio results

Functions:
    load_Deep_Data
    load_HI_1453
    load_HI_1215
    load_HI_1732
    load_GM
    load_NDVI
    load_NDPI

'''


def load_Deep_Data(band_reader, band_1='1197', band_2='1216', band_3='1235', band_4='1373', band_5='1453', band_6='1503', adjust_for_calibration_gain=False):
    '''
        Function for loading Deep-Data hydrocarbon index map automatically

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            band_1 - L_1197 band in 1215 hydrocarbon index map (Default 1197)
            band_2 - L_1216 band in 1215 hydrocarbon index map (Default 1216)
            band_3 - L_1235 band in 1215 hydrocarbon index map (Default 1235)
            band_4 - L_1373 band in 1453 hydrocarbon index map (Default 1373)
            band_5 - L_1453 band in 1453 hydrocarbon index map (Default 1453)
            band_6 - L_1503 band in 1453 hydrocarbon index map (Default 1503)

        Returns ================================================================
            1453 Hydrocarbon Index Map

    '''

    result_Deep_Data = Deep_Data(
        band_reader.load_band(band_1, adjust_for_calibration_gain),
        band_reader.load_band(band_2, adjust_for_calibration_gain),
        band_reader.load_band(band_3, adjust_for_calibration_gain),
        band_reader.load_band(band_4, adjust_for_calibration_gain),
        band_reader.load_band(band_5, adjust_for_calibration_gain),
        band_reader.load_band(band_6, adjust_for_calibration_gain)
    )

    return result_Deep_Data


def load_HI_1453(band_reader, band_1='1373', band_2='1453', band_3='1503', adjust_for_calibration_gain=False):
    '''
        Function for loading 1215 hydrocarbon index map automatically

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            band_1 - L_1373 band in 1453 hydrocarbon index map (Default 1373)
            band_2 - L_1453 band in 1453 hydrocarbon index map (Default 1453)
            band_3 - L_1503 band in 1453 hydrocarbon index map (Default 1503)

        Returns ================================================================
            1453 Hydrocarbon Index Map

    '''

    result_HI_1453 = HI_1453(
        band_reader.load_band(band_1, adjust_for_calibration_gain),
        band_reader.load_band(band_2, adjust_for_calibration_gain),
        band_reader.load_band(band_3, adjust_for_calibration_gain)
    )

    return result_HI_1453




def load_HI_1215(band_reader, band_1='1197', band_2='1216', band_3='1235', adjust_for_calibration_gain=False):
    '''
        Function for loading 1215 hydrocarbon index map automatically

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            band_1 - L_1197 band in 1215 hydrocarbon index map (Default 1197)
            band_2 - L_1216 band in 1215 hydrocarbon index map (Default 1216)
            band_3 - L_1235 band in 1215 hydrocarbon index map (Default 1235)

        Returns ================================================================
            1215 Hydrocarbon Index Map

    '''

    result_HI_1215 = HI_1215(
        band_reader.load_band(band_1, adjust_for_calibration_gain),
        band_reader.load_band(band_2, adjust_for_calibration_gain),
        band_reader.load_band(band_3, adjust_for_calibration_gain)
    )

    return result_HI_1215


def load_HI_1732(band_reader, band_1='1705', band_2='1729', band_3='1741', adjust_for_calibration_gain=False):
    '''
        Function for loading 1732 hydrocarbon index map automatically

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            band_1 - L_1705 band in 1732 hydrocarbon index map (Default 1705)
            band_2 - L_1729 band in 1732 hydrocarbon index map (Default 1729)
            band_3 - L_1741 band in 1732 hydrocarbon index map (Default 1741)

        Returns ================================================================
            1732 Hydrocarbon Index Map

    '''

    result_HI_1732 = HI_1732(
        band_reader.load_band(band_1, adjust_for_calibration_gain),
        band_reader.load_band(band_2, adjust_for_calibration_gain),
        band_reader.load_band(band_3, adjust_for_calibration_gain)
    )

    return result_HI_1732


def load_GM(band_reader, band_1='850', band_2='1660', adjust_for_calibration_gain=False):
    '''
        Function for loading Goddijn-Murphy index map automatically

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            band_1 - L_850 band in GM index map (Default 850)
            band_2 - L_1729 band in GM index map (Default 1660)

        Returns ================================================================
            Goddijn-Murphy Index Map

    '''

    result_GM = GM(
        band_reader.load_band(band_1, adjust_for_calibration_gain),
        band_reader.load_band(band_2, adjust_for_calibration_gain)
    )

    return result_GM


def load_NDVI(band_reader, band_1='1006', band_2='675', adjust_for_calibration_gain=False):
    '''
        Function for loading NDVI index map automatically

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            band_1 - L_1006 band in GM index map (Default 1006)
            band_2 - L_675 band in GM index map (Default 675)

        Returns ================================================================
            NDVI Index Map

    '''

    result_NDVI = NDVI(
        band_reader.load_band(band_1, adjust_for_calibration_gain),
        band_reader.load_band(band_2, adjust_for_calibration_gain)
    )

    return result_NDVI


def load_NDPI(band_reader, band_1='1263', band_2='2417', adjust_for_calibration_gain=False):
    '''
        Function for loading NDVI index map automatically

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            band_1 - L_1263 band in GM index map (Default 1263)
            band_2 - L_2417 band in GM index map (Default 2417)

        Returns ================================================================
            NDVI Index Map

    '''

    result_NDPI = NDPI(
        band_reader.load_band(band_1, adjust_for_calibration_gain),
        band_reader.load_band(band_2, adjust_for_calibration_gain)
    )

    return result_NDPI
