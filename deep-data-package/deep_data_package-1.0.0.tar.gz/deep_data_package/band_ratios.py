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

'''
Module for calculating band ratios

Band ratios:
    Deep_Data
    HI_1453
    HI_1215
    HI_1732
    GM
    NDVI
    NDPI

'''
def Deep_Data(L_1197, L_1216, L_1235, L_1373, L_1453, L_1503):
    '''
        Deep-Data Hydrocarbon Index =============================================
            Convert numpy arrays of radiance data to a Deep-Data hydrocarbon
            index map

        Inputs ==================================================================
            L_1197 : At-sensor radiance at 1197 nm wavelength (numpy array)
            L_1216 : At-sensor radiance at 1216 nm wavelength (numpy array)
            L_1235 : At-sensor radiance at 1235 nm wavelength (numpy array)
            L_1373 : At-sensor radiance at 1373 nm wavelength (numpy array)
            L_1453 : At-sensor radiance at 1453 nm wavelength (numpy array)
            L_1503 : At-sensor radiance at 1503 nm wavelength (numpy array)

        Returns =================================================================
            Deep-Data Hydrocarbon Index Map

    '''
    return (1.2 * L_1197 - 1.1 * L_1216 + 0.5 * (1.2 * L_1235 - L_1197 * 1.1)) - (1.2 * L_1373 - 1.1 * L_1453 + 0.5 * (1.2 * L_1503 - L_1373 * 1.1))


def HI_1453(L_1373, L_1453, L_1503):
    '''
        1453 Hydrocarbon Index ==================================================
            Convert numpy arrays of radiance data to a 1453 hydrocarbon index map

        Inputs ==================================================================
            L_1373 : At-sensor radiance at 1373 nm wavelength (numpy array)
            L_1453 : At-sensor radiance at 1453 nm wavelength (numpy array)
            L_1503 : At-sensor radiance at 1503 nm wavelength (numpy array)

        Returns =================================================================
            1453 Hydrocarbon Index Map

    '''
    return 1.2 * L_1373 - 1.1 * L_1453 + 0.5 * (1.2 * L_1503 - L_1373 * 1.1)


def HI_1215(L_1197, L_1216, L_1235):
    '''
        1215 Hydrocarbon Index ==================================================
            Convert numpy arrays of radiance data to a 1215 hydrocarbon index map

        Inputs ==================================================================
            L_1197 : At-sensor radiance at 1197 nm wavelength (numpy array)
            L_1216 : At-sensor radiance at 1216 nm wavelength (numpy array)
            L_1235 : At-sensor radiance at 1235 nm wavelength (numpy array)

        Returns =================================================================
            1215 Hydrocarbon Index Map

    '''
    return 1.2 * L_1197 - 1.1 * L_1216 + 0.5 * (1.2 * L_1235 - L_1197 * 1.1)



def HI_1732(L_1705, L_1729, L_1741):
    '''
        1732 Hydrocarbon Index ==================================================
            Convert numpy arrays of radiance data to a 1732 hydrocarbon index map

        Inputs ==================================================================
            L_1705 : At-sensor radiance at 1705 nm wavelength (numpy array)
            L_1729 : At-sensor radiance at 1729 nm wavelength (numpy array)
            L_1741 : At-sensor radiance at 1741 nm wavelength (numpy array)

        Returns =================================================================
            1732 Hydrocarbon Index Map

    '''
    return (L_1705 - L_1729 + 0.667 * (L_1741 * 1.05 - L_1705 * 1.05)) * 1.2
    #return L_1705 - L_1729 + 0.667 * (L_1741 - L_1705)



def GM(L_850, L_1660):
    '''
        Goddijn-Murphy Index ====================================================
            From: "Proof of concept for a model of light reflectance of plastics
            floating on natural waters" by Lonneke Goddijn-Murphy and Juvenal
            Dufaur. - See Table 5

            Convert numpy arrays of radiance data to a Goddijn-Murphy map

        Inputs =================================================================
            L_850 : At-sensor radiance at 850 nm wavelength (numpy array)
            L_1660 : At-sensor radiance at 1660 nm wavelength (numpy array)

        Returns ================================================================
            Goddijn-Murphy Map
    '''

    return L_850 - L_1660


def NDVI(L_1006, L_675):
    '''
        NDVI ====================================================================
            Convert numpy arrays of radiance data to a NDVI map

        Inputs ==================================================================
            L_1006 : At-sensor radiance at 1006 nm wavelength (numpy array)
            L_675 : At-sensor radiance at 675 nm wavelength (numpy array)

        Returns =================================================================
            NDVI Map

    '''
    return (L_1006 - L_675) / (L_1006 + L_675)



def NDPI(L_1263, L_2417):
    '''
        NDPI ====================================================================
            Convert numpy arrays of radiance data to a NDPI map

        Inputs ==================================================================
            L_1263 : At-sensor radiance at 1263 nm wavelength (numpy array)
            L_2417 : At-sensor radiance at 2417 nm wavelength (numpy array)

        Returns =================================================================
            NDPI Map

    '''
    return (L_1263 - L_2417) / (L_1263 + L_2417)
