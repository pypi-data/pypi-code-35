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

Deep-Data package main script

Includes:
    1. loading data
    2. calculating band ratios
    3. creating heatmaps
    4. mixed band ratio testing

'''

import deep_data_package

aviris_flight = 'f111115t01p00r08'
hyperion_pass = 'EO1H0410362008289110KF'

# Available Modes: 'aviris', 'pickled_aviris', 'hyperion'
mode = 'pickled_aviris'

# deep_data_package.file_reader.create_pickled_aviris_flight()
# exit()

################################################################################
###                                Load Data                                 ###
################################################################################

# Create deep_data_package.file_reader instance ================================
print('Selected band_reader mode: {}'.format(mode))
if mode == 'aviris':
    # Non-pickled file verion
    band_reader = deep_data_package.file_reader.aviris_band_reader(aviris_flight)
elif mode == 'pickled_aviris':
    # pickled file band reader (if want speed and dont care about excessive memory usage)
    band_reader = deep_data_package.file_reader.pickled_aviris_band_reader(aviris_flight)
elif mode == 'hyperion':
    band_reader = deep_data_package.file_reader.hyperion_band_reader(hyperion_pass)
else:
    print('FATAL ERROR: band_reader mode: {} not recignized'.format(mode))
    print('-> ABORTING PROCESS')
    exit()

# res = band_reader.load_band('1702', False)
# print(res.shape)
# exit()

# Print all available wavelengths in AVIRIS flight =============================
# print('Available wavelengths:')
# print(band_reader.info['band_calibration']['bands'])
# print(band_reader.info['band_calibration']['bandwidths'])



################################################################################
###                          Calculate band ratios                           ###
################################################################################

# If want remove sensor gain set by AVIRIS flight tech for each band
adjust_for_calibration_gain = False

# 1215 Hydrocarbon Index Map
print('Loading HI_1215...')
result_HI_1215 = deep_data_package.functions.load_HI_1215(
    band_reader,
    adjust_for_calibration_gain = adjust_for_calibration_gain
)
print('-> Done')

# 1732 Hydrocarbon Index Map
# NOTE: wavelengths called for in function do not exactly match with
#       wavelengths measured in sunshine AVIRIS flight
print('Loading HI_1732...')
result_HI_1732 = deep_data_package.functions.load_HI_1732(
    band_reader,
    band_1 = '1702',
    band_2 = '1722',
    band_3 = '1742',
    adjust_for_calibration_gain = adjust_for_calibration_gain
)
print('-> Done')

# print('Loading HI_1452...')
# result_HI_1452 = deep_data_package.functions.load_HI_1453(band_reader)
# print('-> Done')

# Goddijn-Murphy Map
# From: "Proof of concept for a model of light reflectance of plastics
# floating on natural waters"
# print('Loading GM...')
# result_GM = deep_data_package.functions.load_GM(
#     band_reader,
#     adjust_for_calibration_gain = adjust_for_calibration_gain
# )
# print('-> Done')

# NDVI Map
# print('Loading NDVI...')
# result_NDVI = deep_data_package.functions.load_NDVI(
#     band_reader,
#     adjust_for_calibration_gain = adjust_for_calibration_gain
# )
# print('-> Done')

# NDPI
# print('Loading NDVI...')
# result_NDPI = deep_data_package.functions.load_NDPI(
#     band_reader,
#     adjust_for_calibration_gain = adjust_for_calibration_gain
# )
# print('-> Done')


# Print example results ========================================================
# print('Result HI_1215: {}'.format(result_HI_1215[100,100]))
# print('Result HI_1732: {}'.format(result_HI_1732[100,100]))
# print('Result GM: {}'.format(result_GM[100,100]))



################################################################################
###                             Heatmap Examples                             ###
################################################################################

# NOTE: MUST DOWNLOAD AVIRIS FLIGHT img FROM DRIVE TO WORK

# AVIRIS PAPAER RECREATION =====================================================

# deep_data_package.mapper.create_heatmap(
#     bandratio_array = result_HI_1215,
#     bandratio_array_name = 'HI_1215',
#     alpha = 0.6,
#     gamma_1 = 0.5836966,
#     gamma_2 = 0.5839571,
#     gamma_3 = 0.6,
#     clipped = False
# )



# Interactive Heatmap ==========================================================

# deep_data_package.mapper.create_heatmap_interactive(
#     bandratio_array = result_GM,
#     bandratio_array_name = 'result_GM',
#     flight_name = aviris_flight,
#     gamma_1 = 0.583,
#     std_multiplier = 3,
#     alpha = 1,
#     clipped = False
# )




################################################################################
###                        MIXING BAND RATIOS TESTING                        ###
################################################################################

# result_mixed = result_HI_1452
result_mixed = result_HI_1215 - result_HI_1732
# result_mixed = result_HI_1215 - result_GM
# result_mixed = result_HI_1215 - result_NDVI
# result_mixed = result_HI_1215 - result_NDPI


deep_data_package.mapper.create_heatmap_interactive(
    band_reader = band_reader,
    bandratio_array = result_mixed,
    bandratio_array_name = 'result_mixed',
    flight_name = aviris_flight,
    # gamma_1 = 0.583,
    std_multiplier = 3,
    alpha = 1,
    clipped = False
)
