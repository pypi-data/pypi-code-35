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
Module for reading AVIRIS and Hyperion flight data and mapping

Classes:
    hyperion_band_reader
    aviris_band_reader
    aviris_pickled_aviris_band_reader

Methods:
    select_closest_band
    create_pickled_aviris_flight
    get_available_aviris_flights
    get_available_pickled_aviris_flights
    get_available_hyperion_passes

'''

import os
import sys
import errno
import numpy as np
import builtins
import pickle
import glob
from bisect import bisect_left
from scipy import ndimage
import rasterio
import logging


################################################################################
###                                CLASSES                                   ###
################################################################################

class hyperion_band_reader(object):
    '''
        Class for reading Hyperion data from GEOtiff L1 files

        NOTE: bands 1-70 and VNIR, bands 71-242 are SWIR

        Reference ==============================================================
            https://archive.usgs.gov/archive/sites/eo1.usgs.gov/EO1userguidev2pt320030715UC.pdf
            https://crisp.nus.edu.sg/~research/tutorial/eo1.htm
            https://crisp.nus.edu.sg/~research/tutorial/eo1.htm

        Inputs =================================================================
            Optional:
                hyperion_pass - name of Hyperion pass to load (Default EO1H0410362008289110KF)
                scale_factor - number to divide bands by (Defaul 80 to get radiance values)

        Returns ================================================================
            class to load radiance bands as np arrays

        class Attributes =======================================================
            band_reader.hyperion_pass - Hyperion flight loaded
            band_reader.scale_factor - number to divide bands by (Defaul 80 to get radiance values)
            band_reader.mode - self identified mode for reference ('hyperion')
            band_reader.approx_band_centers - string refence to what band centers correspond to what files in Hyperion GEOtif files
            self.swir_actual_band_centers - caluclated band centers for SWIR bands (for reference)

    '''
    def __init__(self, hyperion_pass='EO1H0410362008289110KF', scale_factor=80):

        super(hyperion_band_reader, self).__init__()

        self.hyperion_pass = hyperion_pass
        self.scale_factor = scale_factor
        self.mode = 'hyperion'

        # HYPERION APPROX. BAND CENTERS
        # 852 nm - 2577 nm over 170 channels
        # therefore 10.02906977 spacing between centers
        # https://crisp.nus.edu.sg/~research/tutorial/eo1.htm

        # red 652, green 542, blue 471
        self.approx_band_centers = {
            '361': '1', '371': '2', '381': '3', '391': '4', '401': '5', '411': '6', '421': '7',
            '431': '8', '441': '9', '451': '10', '461': '11', '471': '12', '481': '13', '491': '14',
            '501': '15', '511': '16', '521': '17', '532': '18', '542': '19', '552': '20', '562': '21',
            '572': '22', '582': '23', '592': '24', '602': '25', '612': '26', '622': '27', '632': '28',
            '642': '29', '652': '30', '662': '31', '672': '32', '682': '33', '692': '34', '702': '35',
            '712': '36', '722': '37', '732': '38', '742': '39', '752': '40', '762': '41', '772': '42',
            '782': '43', '792': '44', '802': '45', '812': '46', '822': '47', '832': '48', '842': '49',
            '852': '50', '862': '51', '872': '52', '883': '53', '893': '54', '903': '55', '913': '56',
            '923': '57', '933': '58', '943': '59', '953': '60', '963': '61', '973': '62', '983': '63',
            '993': '64', '1003': '65', '1013': '66', '1023': '67', '1033': '68', '1043': '69', '1053': '70',
            '857': '71', '867': '72',  '877': '73',  '887': '74',  '897': '75',  '907': '76',  '917': '77',
            '927': '78',  '937': '79',  '947': '80',  '957': '81',  '967': '82',  '977': '83',  '987': '84',
            '997': '85',  '1007': '86', '1017': '87', '1028': '88', '1038': '89', '1048': '90', '1058': '91',
            '1068': '92', '1078': '93', '1088': '94', '1098': '95', '1108': '96', '1118': '97', '1128': '98',
            '1138': '99', '1148': '100', '1158': '101', '1168': '102', '1178': '103', '1188': '104', '1198': '105',
            '1208': '106', '1218': '107', '1228': '108', '1238': '109', '1248': '110', '1258': '111', '1268': '112',
            '1278': '113', '1288': '114', '1298': '115', '1308': '116', '1318': '117', '1328': '118', '1338': '119',
            '1348': '120', '1358': '121', '1368': '122', '1379': '123', '1389': '124', '1399': '125', '1409': '126',
            '1419': '127', '1429': '128', '1439': '129', '1449': '130', '1459': '131', '1469': '132', '1479': '133',
            '1489': '134', '1499': '135', '1509': '136', '1519': '137', '1529': '138', '1539': '139', '1549': '140',
            '1559': '141', '1569': '142', '1579': '143', '1589': '144', '1599': '145', '1609': '146', '1619': '147',
            '1629': '148', '1639': '149', '1649': '150', '1659': '151', '1669': '152', '1679': '153', '1689': '154',
            '1699': '155', '1709': '156', '1720': '157', '1730': '158', '1740': '159', '1750': '160', '1760': '161',
            '1770': '162', '1780': '163', '1790': '164', '1800': '165', '1810': '166', '1820': '167', '1830': '168',
            '1840': '169', '1850': '170', '1860': '171', '1870': '172', '1880': '173', '1890': '174', '1900': '175',
            '1910': '176', '1920': '177', '1930': '178', '1940': '179', '1950': '180', '1960': '181', '1970': '182',
            '1980': '183', '1990': '184', '2000': '185', '2010': '186', '2020': '187', '2030': '188', '2040': '189',
            '2050': '190', '2061': '191', '2071': '192', '2081': '193', '2091': '194', '2101': '195', '2111': '196',
            '2121': '197', '2131': '198', '2141': '199', '2151': '200', '2161': '201', '2171': '202', '2181': '203',
            '2191': '204', '2201': '205', '2211': '206', '2221': '207', '2231': '208', '2241': '209', '2251': '210',
            '2261': '211', '2271': '212', '2281': '213', '2291': '214', '2301': '215', '2311': '216', '2321': '217',
            '2331': '218', '2341': '219', '2351': '220', '2361': '221', '2371': '222', '2381': '223', '2391': '224',
            '2401': '225', '2412': '226', '2422': '227', '2432': '228', '2442': '229', '2452': '230', '2462': '231',
            '2472': '232', '2482': '233', '2492': '234', '2502': '235', '2512': '236', '2522': '237', '2532': '238',
            '2542': '239', '2552': '240', '2562': '241', '2572': '242'
        }

        self.swir_actual_band_centers = {
            '71': 857.01453490, '72': 867.04360470, '73': 877.07267440, '74': 887.10174420, '75': 897.13081400,
            '76': 907.15988370, '77': 917.18895350, '78': 927.21802330, '79': 937.24709300, '80': 947.27616280,
            '81': 957.30523260, '82': 967.33430230, '83': 977.36337210, '84': 987.39244190, '85': 997.42151160,
            '86': 1007.4505810, '87': 1017.4796510, '88': 1027.5087210, '89': 1037.5377910, '90': 1047.5668600,
            '91': 1057.5959300, '92': 1067.6250000, '93': 1077.6540700, '94': 1087.6831400, '95': 1097.7122090,
            '96': 1107.7412790, '97': 1117.7703490, '98': 1127.7994190, '99': 1137.8284880, '100': 1147.857558,
            '101': 1157.886628, '102': 1167.915698, '103': 1177.944767, '104': 1187.973837, '105': 1198.002907,
            '106': 1208.031977, '107': 1218.061047, '108': 1228.090116, '109': 1238.119186, '110': 1248.148256,
            '111': 1258.177326, '112': 1268.206395, '113': 1278.235465, '114': 1288.264535, '115': 1298.293605,
            '116': 1308.322674, '117': 1318.351744, '118': 1328.380814, '119': 1338.409884, '120': 1348.438953,
            '121': 1358.468023, '122': 1368.497093, '123': 1378.526163, '124': 1388.555233, '125': 1398.584302,
            '126': 1408.613372, '127': 1418.642442, '128': 1428.671512, '129': 1438.700581, '130': 1448.729651,
            '131': 1458.758721, '132': 1468.787791, '133': 1478.816860, '134': 1488.845930, '135': 1498.875000,
            '136': 1508.904070, '137': 1518.933140, '138': 1528.962209, '139': 1538.991279, '140': 1549.020349,
            '141': 1559.049419, '142': 1569.078488, '143': 1579.107558, '144': 1589.136628, '145': 1599.165698,
            '146': 1609.194767, '147': 1619.223837, '148': 1629.252907, '149': 1639.281977, '150': 1649.311047,
            '151': 1659.340116, '152': 1669.369186, '153': 1679.398256, '154': 1689.427326, '155': 1699.456395,
            '156': 1709.485465, '157': 1719.514535, '158': 1729.543605, '159': 1739.572674, '160': 1749.601744,
            '161': 1759.630814, '162': 1769.659884, '163': 1779.688953, '164': 1789.718023, '165': 1799.747093,
            '166': 1809.776163, '167': 1819.805233, '168': 1829.834302, '169': 1839.863372, '170': 1849.892442,
            '171': 1859.921512, '172': 1869.950581, '173': 1879.979651, '174': 1890.008721, '175': 1900.037791,
            '176': 1910.066860, '177': 1920.095930, '178': 1930.125000, '179': 1940.154070, '180': 1950.183140,
            '181': 1960.212209, '182': 1970.241279, '183': 1980.270349, '184': 1990.299419, '185': 2000.328488,
            '186': 2010.357558, '187': 2020.386628, '188': 2030.415698, '189': 2040.444767, '190': 2050.473837,
            '191': 2060.502907, '192': 2070.531977, '193': 2080.561047, '194': 2090.590116, '195': 2100.619186,
            '196': 2110.648256, '197': 2120.677326, '198': 2130.706395, '199': 2140.735465, '200': 2150.764535,
            '201': 2160.793605, '202': 2170.822674, '203': 2180.851744, '204': 2190.880814, '205': 2200.909884,
            '206': 2210.938953, '207': 2220.968023, '208': 2230.997093, '209': 2241.026163, '210': 2251.055233,
            '211': 2261.084302, '212': 2271.113372, '213': 2281.142442, '214': 2291.171512, '215': 2301.200581,
            '216': 2311.229651, '217': 2321.258721, '218': 2331.287791, '219': 2341.316860, '220': 2351.345930,
            '221': 2361.375000, '222': 2371.404070, '223': 2381.433140, '224': 2391.462209, '225': 2401.491279,
            '226': 2411.520349, '227': 2421.549419, '228': 2431.578488, '229': 2441.607558, '230': 2451.636628,
            '231': 2461.665698, '232': 2471.694767, '233': 2481.723837, '234': 2491.752907, '235': 2501.781977,
            '236': 2511.811047, '237': 2521.840116, '238': 2531.869186, '239': 2541.898256, '240': 2551.927326,
            '241': 2561.956395, '242': 2571.985465
        }

        # self.n_cols = samples
        # self.n_rows = lines
        # self.n_bands = bands
        # self.scale_factor = scale_factor

        # Check if aviris flight dir exists
        if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'HYPERION_data', self.hyperion_pass)):
            self.hyperion_folder_filepath = os.path.join(os.path.dirname(os.getcwd()), 'HYPERION_data', self.hyperion_pass)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'HYPERION_data', self.hyperion_pass))

    def load_band(self, band_req, adjust_for_gain=False):
        '''
            Function for reading Hyperion data

            By defualt loads Hyperion pass EO1H0410362008289110KF over sunshine canyon
            landfill

            Reference ==========================================================
                N/A

            Inputs =============================================================
                band_req - band wavelength to load
                adjust_for_gain - N/A

            Returns ============================================================
                2D np array of radiance data for band wavelength called

                - To load a row

                    band_array[row_number, :]

                - To load a column

                    band_array[:, col_number]

                - To load a pixel

                    band_array[row_number, col_number]

        '''

        # Create band filename
        if str(band_req) not in self.approx_band_centers:
            band_to_load = select_closest_band(int(band_req), list(self.approx_band_centers.keys()))
            logging.warning('- WARNING: requested band {} was not found, used {} instead.'.format(band_req, band_to_load))
        else:
            band_to_load = band_req

        band_name = self.approx_band_centers[str(band_to_load)].zfill(3)
        fn = self.hyperion_pass + '_B' + band_name + '_L1GST.TIF'
        if os.path.exists(os.path.join(self.hyperion_folder_filepath, fn)):
            path = os.path.join(self.hyperion_folder_filepath, fn)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.hyperion_folder_filepath, fn))

        with rasterio.open(path) as src:
            band_array = src.read(1)
            if self.scale_factor != 1:
                band_array = band_array / float(self.scale_factor)
            return band_array

    def load_pixel(self, row, col, adjust_for_gain=False):

        '''
            Function for reading all bands of an individual pixel from AVIRIS
            flight data

            Reference ==========================================================
                N/A

            Inputs =============================================================
                row - int of row number of requested pixel
                col - int of column number of requested pixel
                adjust_for_gain - N/A

            Returns ============================================================
                Ordered dict of wavelengths vs irradiance for requested pixel

        '''

        result_dict = {}

        for i, band in enumerate(self.approx_band_centers):
            band_name = self.approx_band_centers[str(band)].zfill(3)
            fn = self.hyperion_pass + '_B' + band_name + '_L1GST.TIF'
            with rasterio.open(os.path.join(self.hyperion_folder_filepath, fn)) as src:
                value = src.read(1)[row, col]

            if adjust_for_gain:
                value = value / float(self.info['gain_values'][band_index][0])
            elif self.scale_factor != 1:
                value = value / float(self.scale_factor)
            else:
                pass
            result_dict[band] = value

        return result_dict




class aviris_band_reader(object):
    '''
        Class for reading AVIRIS flight data from uncompressed AVIRIS flight
        folder. No files need to be modified after downloading from AVIRIS data
        portal. Just uncompress in the aviris_flight_folder and go.

        By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon
        landfill

        Reference ==============================================================
            N/A

        Inputs =================================================================
            Optional:
                aviris_flight_number - AVIRIS flight number to load
                aviris_filename - filename to load in AVIRIS flight number folder
                samples - from *hdr file in AVERIS flight folder (Defualt 780)
                lines - from *hdr file in AVERIS flight folder (Defualt 8355)
                bands - from *hdr file in AVERIS flight folder (Defualt 224)
                aviris_calibration_filename - name of AVIRIS file for reflectance calibration
                aviris_gain_filename - name of AVIRIS gain file for reflectance calibration

        Returns ================================================================
            class to load radiance bands as np arrays

        class Attributes =======================================================
            band_reader.aviris_flight -  AVIRIS flight loaded
            band_reader.n_cols - number of columns in AVIRIS band file (equals input samples)
            band_reader.n_rows - number of rows in AVIRIS band file (equals input lines)
            band_reader.n_bands - number of bands in AVIRIS band file (equals input bands)
            band_reader.scale_factor - multiplier of bands (equals input scale_factor)
            band_reader.aviris_flight_folder_filepath - full filepath for AVIRIS flight folder
            band_reader.bands_filepath - full filepath for AVIRIS band file

            band_reader.info - dict with useful info from AVIRIS flight
                Contains:
                    # General info
                    ['info']['n_rows'] = number of rows in .npy files
                    ['info']['n_cols'] = number of columns in .npy files
                    ['info']['n_bands'] = number of bands from AVIRIS flight
                    ['info']['AVIRIS_flight'] = aviris_flight

                    # Band info
                    ['band_calibration']['band_quantity'] = 'Wavelength'
                    ['band_calibration']['band_unit'] = 'nm'
                    ['band_calibration']['centers'] = mathmatical center of wavelength
                    ['band_calibration']['bandwidths'] = bandwidths of wavelengths
                    ['band_calibration']['bands'] = wavelengths callable

                    # Gain values
                    ['gain_values'] = np array of gain values for each band

                Call any of above w/ band_reader.info['INSERT_AS_SHOWN_ABOVE']
    '''
    def __init__(self,
                 aviris_flight = 'f111115t01p00r08',
                 aviris_flight_folder = 'f111115t01p00r08rdn_c',
                 aviris_bands_filename = 'f111115t01p00r08rdn_c_sc01_ort_img',
                 samples = 780,
                 lines = 8355,
                 bands = 224,
                 aviris_calibration_filename = 'f111115t01p00r08rdn_c.spc',
                 aviris_gain_filename = 'f111115t01p00r08rdn_c.gain',
                 scale_factor = 10000.0
        ):

        super(aviris_band_reader, self).__init__()

        self.aviris_flight = aviris_flight
        self.n_cols = samples
        self.n_rows = lines
        self.n_bands = bands
        self.scale_factor = scale_factor
        self.mode = 'aviris'

        # Check if aviris flight dir exists
        if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder)):
            self.aviris_flight_folder_filepath = os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder))

        # Check if aviris bands file exists
        if os.path.exists(os.path.join(self.aviris_flight_folder_filepath, aviris_bands_filename)):
            self.bands_filepath = os.path.join(self.aviris_flight_folder_filepath, aviris_bands_filename)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.aviris_flight_folder_filepath, aviris_bands_filename))

        # Check if aviris flight has been parsed before by the program and if not then do so
        info_file_name = aviris_flight + '_info.pickle'
        if not os.path.exists(os.path.join(self.aviris_flight_folder_filepath, info_file_name)):
            self.info = self.parse_aviris_flight(info_file_name, aviris_calibration_filename, aviris_gain_filename)
        else:
            with open(os.path.join(self.aviris_flight_folder_filepath, info_file_name), "rb") as f:
                 self.info = pickle.load(f)

        self.memmap = self.get_memmap()


    def parse_aviris_flight(self, info_file_name, aviris_calibration_filename, aviris_gain_filename):

        '''
            Function for loading AVIRIS flight files of the first time

            By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon landfill

            Inputs =================================================================
                info_file_name - name for info file to be written by parser
                aviris_calibration_filename - name of AVIRIS file for reflectance calibration
                aviris_gain_filename - name of AVIRIS gain file for reflectance calibration

            Returns ================================================================
                flight_dict - dict with useful info from AVIRIS flight
                    Contains:
                        # General info
                        ['info']['n_rows'] = number of rows in .npy files
                        ['info']['n_cols'] = number of columns in .npy files
                        ['info']['n_bands'] = number of bands from AVIRIS flight
                        ['info']['AVIRIS_flight'] = aviris_flight

                        # Band info
                        ['band_calibration']['band_quantity'] = 'Wavelength'
                        ['band_calibration']['band_unit'] = 'nm'
                        ['band_calibration']['centers'] = mathmatical center of wavelength
                        ['band_calibration']['bandwidths'] = bandwidths of wavelengths
                        ['band_calibration']['bands'] = wavelengths callable

                        # Gain values
                        ['gain_values'] = np array of gain values for each band

        '''

        if not aviris_calibration_filename: aviris_calibration_filename = glob.glob(self.aviris_flight_folder_filepath + '/*.spc')[0]
        if not aviris_gain_filename: aviris_gain_filename = glob.glob(self.aviris_flight_folder_filepath + '/*.gain')

        # Check if aviris flight calibration file exists
        if os.path.exists(os.path.join(self.aviris_flight_folder_filepath, aviris_calibration_filename)):
            self.calibration_filepath = os.path.join(self.aviris_flight_folder_filepath, aviris_calibration_filename)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.aviris_flight_folder_filepath, aviris_calibration_filename))

        # Check if aviris flight gain file exists
        if os.path.exists(os.path.join(self.aviris_flight_folder_filepath, aviris_gain_filename)):
            self.gain_filepath = os.path.join(self.aviris_flight_folder_filepath, aviris_gain_filename)
            gain_values = np.genfromtxt(self.gain_filepath)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.aviris_flight_folder_filepath, aviris_gain_filename))

        logging.info('Parsing AVIRIS flight number: {}'.format(self.aviris_flight))

        # Band calibration info from AVIRIS flight calibration file
        band_calibration = {}
        band_calibration['band_quantity'] = 'Wavelength'
        band_calibration['band_unit'] = 'nm'

        try:
            fin = open(self.calibration_filepath)
        except Exception:
            raise

        rows = [line.split() for line in fin]
        rows = [[float(x) for x in row] for row in rows]
        columns = list(zip(*rows))

        band_calibration['centers'] = columns[0]
        band_calibration['bandwidths'] = columns[1]
        band_calibration['bands'] = ["%.0f" % number for number in columns[0]]

        # General info
        info_dict = {}
        info_dict['n_rows'] = self.n_rows
        info_dict['n_cols'] = self.n_cols
        info_dict['n_bands'] = self.n_bands
        info_dict['AVIRIS_flight'] = self.aviris_flight

        # AVIRIS flight dict with band, flight info, and other useful things
        flight_dict = {}
        flight_dict['info'] = info_dict
        flight_dict['gain_values'] = gain_values
        flight_dict['band_calibration'] = band_calibration

        # Write AVIRIS flight info
        # if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight)):
        logging.info('-> Completed')
        logging.info('Writing AVIRIS flight info')
        try:
            with open(os.path.join(self.aviris_flight_folder_filepath, info_file_name), "wb") as f:
                 pickle.dump(flight_dict, f)
        except Exception:
            raise
        logging.info('-> Completed')
        logging.info('Success: AVIRIS Flight has been parsed')

        return flight_dict

    def get_memmap(self):
        '''
            Function for loading memmap of AVIRIS band file

            Inputs =================================================================
                N/A

            Returns ================================================================
                np.memmap of AVIRIS band file

        '''
        if sys.byteorder == 'little':
            byte_order = 0   # little endian
        else:
            byte_order = 1   # big endian
        dtype = np.dtype('i2').str
        if byte_order != 1:
            dtype = np.dtype(dtype).newbyteorder().str

        if (os.path.getsize(self.bands_filepath) < sys.maxsize):
            try:
                return np.memmap(
                    self.bands_filepath,
                    dtype = dtype,
                    mode = 'r',
                    offset = 0,
                    shape = (self.n_rows, self.n_cols, self.n_bands)
                )
            except Exception:
                raise

        else:
            raise ValueError('AVIRIS bands file is too large for system to load')

    def load_band(self, band_req, adjust_for_gain=False):
        '''
            Function for reading AVIRIS flight data from .npy files pickled by
            create_pickled_aviris_flight()

            By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon
            landfill

            Reference ==========================================================
                N/A

            Inputs =============================================================
                band_req - band wavelength to load
                adjust_for_gain - If want to divide band array by gain value in .gain file (Default: False)

            Returns ============================================================
                2D np array of radiance data for band wavelength called

                - To load a row

                    band_array[row_number, :]

                - To load a column

                    band_array[:, col_number]

                - To load a pixel

                    band_array[row_number, col_number]

        '''

        # Create band filename
        if str(band_req) not in self.info['band_calibration']['bands']:
            band_to_load = select_closest_band(int(band_req), self.info['band_calibration']['bands'])
            logging.warning('- WARNING: requested band {} was not found, used {} instead.'.format(band_req, band_to_load))
        else:
            band_to_load = band_req

        try:
            band_index = self.info['band_calibration']['bands'].index(str(band_to_load))
        except ValueError:
            raise ValueError('Band called not found in AVIRIS band file.\nPlease check the available bands in band_reader.info[\'band_calibration\'][\'bands\']')

        if self.memmap is not None:
            band_array = np.array(self.memmap[:, :, int(band_index)])
            if adjust_for_gain:
                band_array = band_array / float(self.info['gain_values'][band_index][0])
            elif self.scale_factor != 1:
                band_array = band_array / float(self.scale_factor)
            else:
                pass

            return band_array
        else:
            raise ValueError('No memmap found')


    def load_pixel(self, row, col, adjust_for_gain=False):

        '''
            Function for reading all bands of an individual pixel from AVIRIS
            flight data

            Reference ==========================================================
                N/A

            Inputs =============================================================
                row - int of row number of requested pixel
                col - int of column number of requested pixel
                adjust_for_gain - N/A

            Returns ============================================================
                Ordered dict of wavelengths vs irradience for requested pixel

        '''

        result_dict = {}

        if self.memmap is not None:
            for i, band in enumerate(self.info['band_calibration']['bands']):
                value = self.memmap[row, col, i]
                if adjust_for_gain:
                    value = value / float(self.info['gain_values'][band_index][0])
                elif self.scale_factor != 1:
                    value = value / float(self.scale_factor)
                else:
                    pass
                result_dict[band] = value

            return result_dict
        else:
            raise ValueError('No memmap found')



class pickled_aviris_band_reader(object):
    '''
        Class for reading AVIRIS flight data from .npy files pickled by
        create_pickled_aviris_flight()

        By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon
        landfill

        Reference ==============================================================
            N/A

        Inputs =================================================================
            Optional:
                aviris_flight - AVIRIS flight to load

        Returns ================================================================
            class to load radiance bands as np arrays

        class Attributes =======================================================
            band_reader.aviris_flight -  AVIRIS flight loaded
            band_reader.np_path - path will load .npy files from

            band_reader.info - dict with useful info from AVIRIS flight
                Contains:
                    # General info
                    ['info']['n_rows'] = number of rows in .npy files
                    ['info']['n_cols'] = number of columns in .npy files
                    ['info']['n_bands'] = number of bands from AVIRIS flight
                    ['info']['AVIRIS_flight'] = aviris_flight

                    # Band info
                    ['band_calibration']['band_quantity'] = 'Wavelength'
                    ['band_calibration']['band_unit'] = 'nm'
                    ['band_calibration']['centers'] = mathmatical center of wavelength
                    ['band_calibration']['bandwidths'] = bandwidths of wavelengths
                    ['band_calibration']['bands'] = wavelengths callable

                    # Gain values
                    ['gain_values'] = np array of gain values for each band

                Call any of above w/ band_reader.info['INSERT_AS_SHOWN_ABOVE']
    '''
    def __init__(self, aviris_flight = 'f111115t01p00r08'):
        super(pickled_aviris_band_reader, self).__init__()
        self.aviris_flight = aviris_flight
        self.mode = 'pickled_aviris'

        # Check if aviris flight data info exists and if so load
        fn = aviris_flight + '_info.pickle'
        with open(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight, fn), "rb") as f:
             self.info = pickle.load(f)

        # Check if pickled aviris flight dir exists with .npy files
        if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight, 'np_bands')):
            self.np_path = os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight, 'np_bands')
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight, 'np_bands'))

    def load_band(self, band_req, adjust_for_gain=False):

        '''
            Function for reading AVIRIS flight data from .npy files pickled by
            create_pickled_aviris_flight()

            Reference ==========================================================
                N/A

            Inputs =============================================================
                band_req - band wavelength to load

            Returns ============================================================
                2D np array of radiance data for band wavelength called

                - To load a row

                    band_array[row_number, :]

                - To load a column

                    band_array[:, col_number]

                - To load a pixel

                    band_array[row_number, col_number]

        '''

        # Create band filename
        if str(band_req) not in self.info['band_calibration']['bands']:
            band_to_load = select_closest_band(int(band_req), self.info['band_calibration']['bands'])
            logging.warning('- WARNING: requested band {} was not found, used {} instead.'.format(band_req, band_to_load))
        else:
            band_to_load = band_req

        band_to_load = str(band_to_load)
        band_to_load += '.npy'

        # Check if the file exists and if so load it as np array
        if os.path.exists(os.path.join(self.np_path, band_to_load)):
            band_array = np.load(os.path.join(self.np_path, band_to_load))
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.np_path, band_to_load))

        return band_array

    def load_pixel(self, row, col, adjust_for_gain=False):

        '''
            Function for reading all bands of an individual pixel from AVIRIS
            flight data from .npy files pickled by create_pickled_aviris_flight()

            Reference ==========================================================
                N/A

            Inputs =============================================================
                row - int of row number of requested pixel
                col - int of column number of requested pixel
                adjust_for_gain - N/A

            Returns ============================================================
                Ordered dict of wavelengths vs irradience for requested pixel

        '''

        result_dict = {}

        for i, band in enumerate(self.info['band_calibration']['bands']):
            band_to_load = str(band)
            band_to_load += '.npy'
            if os.path.exists(os.path.join(self.np_path, band_to_load)):
                band_array = np.load(os.path.join(self.np_path, band_to_load), mmap_mode='r')
                result_dict[band] = band_array[row, col]
            else:
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.np_path, band_to_load))
        return result_dict



################################################################################
###                                 METHODS                                  ###
################################################################################

def select_closest_band(band_req, band_list):
    '''
        Returns closest band available to band_req.

        Inputs =============================================================
            band_req - band wavelength to match
            band_req - list of band wavelengths available

        Returns ============================================================
            band available, if two numbers are equally close, returns the
            smallest number.
    '''

    bands = list(map(int, band_list))
    bands.sort()
    pos = bisect_left(bands, band_req)
    if pos == 0:
        return bands[0]
    if pos == len(bands):
        return bands[-1]
    before = bands[pos - 1]
    after = bands[pos]
    if after - band_req < band_req - before:
       return after
    else:
       return before


def create_pickled_aviris_flight(
    aviris_flight = 'f111115t01p00r08',
    aviris_flight_folder = 'f111115t01p00r08rdn_c',
    aviris_bands_filename = 'f111115t01p00r08rdn_c_sc01_ort_img',
    samples = 780,
    lines = 8355,
    bands = 224,
    aviris_calibration_filename = 'f111115t01p00r08rdn_c.spc',
    aviris_gain_filename = 'f111115t01p00r08rdn_c.gain',
    adjust_for_gain = False,
    scale_factor = 10000.0
    ):

    '''
        Function for creating pickled AVIRIS flight data using spectral python library

        By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon landfill

        Reference ==============================================================
            N/A

        Inputs =================================================================
            Optional:
                aviris_flight - AVIRIS flight number
                aviris_flight_folder - AVIRIS flight folder to load
                aviris_bands_filename - filename to load in AVIRIS flight number folder
                samples - from *hdr file in AVERIS flight folder (Defualt 780)
                lines - from *hdr file in AVERIS flight folder (Defualt 8355)
                bands - from *hdr file in AVERIS flight folder (Defualt 224)
                aviris_calibration_filename - name of AVIRIS file for reflectance calibration
                aviris_gain_filename - name of AVIRIS gain file for reflectance calibration
                adjust_for_gain - if should devide bands by associated gain value to true values (Default False)
                scale_factor - if want to dived all values by some value (Default 10000.0)

        Returns ================================================================
            N/A

    '''

    # Check if aviris flight dir exists
    if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_bands_filename)):
        filepath = os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_bands_filename)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_bands_filename))

    # Check if aviris flight calibration file exists
    if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_calibration_filename)):
        calibration_filepath = os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_calibration_filename)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_calibration_filename))

    # if not aviris_calibration_filename: aviris_calibration_filename = glob.glob(self.aviris_flight_folder_filepath + '/*.spc')[0]
    # if not aviris_gain_filename: aviris_gain_filename = glob.glob(self.aviris_flight_folder_filepath + '/*.gain')

    # Check if aviris flight gain file exists
    if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_gain_filename)):
        gain_filepath = os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_gain_filename)
        gain_values = np.genfromtxt(gain_filepath)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_gain_filename))

    # Check if dir for pickled flight data exists and if not make it
    if not os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight)):
        os.makedirs(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight, 'np_bands'))
    np_path = os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight, 'np_bands')

    logging.info('Pickling AVIRIS flight number: {}'.format(aviris_flight))

    # load memmap of AVIRIS band file
    if sys.byteorder == 'little':
        byte_order = 0   # little endian
    else:
        byte_order = 1   # big endian
    dtype = np.dtype('i2').str
    if byte_order != 1:
        dtype = np.dtype(dtype).newbyteorder().str

    if (os.path.getsize(filepath) < sys.maxsize):
        try:
            memmap = np.memmap(
                filepath,
                dtype = dtype,
                mode = 'r',
                offset = 0,
                shape = (lines, samples, bands)
            )
        except Exception:
            raise

    else:
        raise ValueError('AVIRIS bands file is too large for system to load')

    # Band calibration info from AVIRIS flight calibration file
    band_calibration = {}
    band_calibration['band_quantity'] = 'Wavelength'
    band_calibration['band_unit'] = 'nm'

    fin = builtins.open(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', aviris_flight_folder, aviris_calibration_filename))
    rows = [line.split() for line in fin]
    rows = [[float(x) for x in row] for row in rows]
    columns = list(zip(*rows))

    band_calibration['centers'] = columns[0]
    band_calibration['bandwidths'] = columns[1]
    band_calibration['bands'] = ["%.0f" % number for number in columns[0]]

    # General info
    info_dict = {}
    info_dict['n_rows'] = lines
    info_dict['n_cols'] = samples
    info_dict['n_bands'] = bands
    info_dict['AVIRIS_flight'] = aviris_flight

    # AVIRIS flight dict with band, flight info, and other useful things
    flight_dict = {}
    flight_dict['info'] = info_dict
    flight_dict['gain_values'] = gain_values
    flight_dict['band_calibration'] = band_calibration

    # Write AVIRIS flight info
    if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight)):
        fn = aviris_flight + '_info.pickle'
        logging.info('Writing AVIRIS flight info...')
        try:
            with open(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight, fn), "wb") as f:
                 pickle.dump(flight_dict, f)
        except Exception as e:
            logging.warning(e)
            return
        logging.info('-> Completed')
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights', aviris_flight))

    # Write each AVIRIS band as separate .npy file
    if os.path.exists(np_path):
        for i, band in enumerate(band_calibration['bands']):
            band_array = np.array(memmap[:, :, i])
            if adjust_for_gain:
                band_array = band_array / float(gain_values[i][0])
            elif scale_factor != 1:
                band_array = band_array / float(scale_factor)
            else:
                pass

            np.save(os.path.join(np_path, band), band_array)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), np_path)

    logging.info('Success: AVIRIS Flight has been pickled')


def get_available_aviris_flights():
    '''
        Function listing all AVIRIS flights available

        Inputs =================================================================
            N/A

        Returns ================================================================
            List of AVIRIS flights available

    '''
    if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data')):
        available_flights = os.listdir(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data'))
        if '.DS_Store' in available_flights: available_flights.remove('.DS_Store')
        if 'pickled_AVIRIS_flights' in available_flights: available_flights.remove('pickled_AVIRIS_flights')
        return available_flights
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data'))


def get_available_pickled_aviris_flights():
    '''
        Function listing all pickled AVIRIS flights available

        Inputs =================================================================
            N/A

        Returns ================================================================
            List of pickled AVIRIS flights available

    '''
    if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights')):
        available_flights = os.listdir(os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights'))
        if '.DS_Store' in available_flights: available_flights.remove('.DS_Store')
        return available_flights
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'AVIRIS_flight_data', 'pickled_AVIRIS_flights'))


def get_available_hyperion_passes():
    '''
        Function listing all Hyperion passes available

        Inputs =================================================================
            N/A

        Returns ================================================================
            List of Hyperion passes available

    '''
    if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'HYPERION_data')):
        available_passes = os.listdir(os.path.join(os.path.dirname(os.getcwd()), 'HYPERION_data'))
        if '.DS_Store' in available_passes: available_passes.remove('.DS_Store')
        return available_passes
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(os.path.dirname(os.getcwd()), 'HYPERION_data'))
