from autofit.tools import path_util
from autocti.data import util
from autocti.charge_injection import ci_frame
from autocti.charge_injection import ci_data
from autocti.charge_injection import ci_pattern

from autocti.model import arctic_settings
from autocti.model import arctic_params

import os

# This tool allows one to make simulated charge injection imaging data-sets for calibrating parallel charge transfer
# inefficiency, which can be used to test example pipelines and investigate CTI modeling on data-sets where the
# 'true' answer is known.

# The 'ci_data_type', 'ci_data_model' and 'ci_data_resolution' determine the directory the output data folder, e.g:

# The image will be output as '/workspace/data/ci_data_type/ci_data_model/ci_data_resolution/ci_image.fits'.
# The noise-map will be output as '/workspace/data/ci_data_type/ci_data_model/ci_data_resolution/ci_noise_map.fits'.
# The pre cti ci image will be output as '/workspace/data/ci_data_type/ci_data_model/ci_data_resolution/ci_pre_cti.fits'.

# Lets setup the relative path to the workspace, so we can output the data in the 'data' folder..
workspace_path = '{}/../../../../'.format(os.path.dirname(os.path.realpath(__file__)))

ci_data_type = 'ci_images_uniform'
ci_data_model = 'parallel_x2_species'
ci_data_resolution = 'low_res'

# Create the path where the data will be output, which in this case is
# '/workspace/data/ci_images_uniform/parallel_x2_species/high_res/'
ci_data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=['data', ci_data_type, ci_data_model, ci_data_resolution])

if ci_data_resolution is 'high_res':
    shape = (2316, 2119)
    frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                            parallel_overscan=ci_frame.Region((2296, 2316, 51, 2099)),
                                            serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                            serial_overscan=ci_frame.Region((0, 2296, 2099, 2119)))
elif ci_data_resolution is 'mid_res':
    shape = (2316, 1034)
    frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                            parallel_overscan=ci_frame.Region((2296, 2316, 51, 1014)),
                                            serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                            serial_overscan=ci_frame.Region((0, 2296, 1014, 1034)))
elif ci_data_resolution is 'low_res':
    shape = (2316, 3)
    frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                            parallel_overscan=ci_frame.Region((2296, 2316, 0, 2)),
                                            serial_prescan=ci_frame.Region((0, 2316, 0, 1)),
                                            serial_overscan=ci_frame.Region((0, 2296, 2, 3)))

# Specify the charge injection regions on the CCD, which in this case is 7 equally spaced rectangular blocks.
ci_regions = [(330, 360, 1, 2)]

# The normalization of every ci image - this size of this list thus determines how many images are simulated.
normalizations=[100.0, 500.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0, 84700.0]

# The CTI settings of arCTIc, which models the CCD read-out including CTI. For parallel ci data, we include 'charge
# injection mode' which accounts for the fact that every pixel is transferred over the full CCD.
parallel_cti_settings = arctic_settings.Settings(well_depth=84700, niter=1, express=2, n_levels=2000,
                                        charge_injection_mode=True, readout_offset=0)
cti_settings = arctic_settings.ArcticSettings(parallel=parallel_cti_settings)

# The CTI model parameters of arCTIc, which includes each trap species density / lifetime and the CCD properties for
# parallel charge transfer.
parallel_species_0 = arctic_params.Species(trap_density=1.0, trap_lifetime=1.0)

### Holger Israel serial CTI model ###

# parallel_species_0 = arctic_params.Species(trap_density=0.01, trap_lifetime=0.8)
# parallel_species_1 = arctic_params.Species(trap_density=0.03, trap_lifetime=4.0)
# parallel_species_2 = arctic_params.Species(trap_density=0.9, trap_lifetime=20.0)

parallel_ccd = arctic_params.CCD(well_notch_depth=1.0e-4, well_fill_beta=0.58, well_fill_alpha=1.0, well_fill_gamma=0.0)

cti_params = arctic_params.ArcticParams(parallel_species=[parallel_species_0],
                                        parallel_ccd=parallel_ccd)

# Use the ci normalizations and regions to create the ci pattern of every image that is to be simulated.
ci_patterns = ci_pattern.uniform_from_lists(normalizations=normalizations, regions=ci_regions)

# Use the simulate ci patterns to generate the pre-cti charge injection images.
ci_pre_ctis = list(map(lambda ci_pattern :
                       ci_pattern.simulate_ci_pre_cti(shape=shape),
                       ci_patterns))

# Use every ci pattern to simulate a ci image.
datas = list(map(lambda ci_pre_cti, ci_pattern:
                    ci_data.simulate(ci_pre_cti=ci_pre_cti, frame_geometry=frame_geometry,
                                     ci_pattern=ci_pattern, cti_settings=cti_settings, cti_params=cti_params,
                                     read_noise=None),
                 ci_pre_ctis, ci_patterns))

# [[[84.48938586]
#   [91.9440306 ]
#   [94.62585263]]]

ci_frame = datas[0].ci_frame
print(ci_frame.parallel_front_edge_arrays_from_frame(array=datas[0].image, rows=(0,20)))

import sys
sys.exit()

# Now, output every image to the data folder as the filename 'ci_data_normalization.fits'
list(map(lambda ci_data, normalization :
         util.numpy_array_2d_to_fits(array_2d=ci_data.image,
                                     file_path=ci_data_path + 'image_' + str(int(normalization)) + '.fits',
                                     overwrite=True),
         datas, normalizations))

# Output every pre-cti image to the data folder as the filename 'ci_pre_cti_normalization.fits'. This allows the
# calibration pipeline to load these images as the model pre-cti images, which is necessary for non-uniform ci patterns.
list(map(lambda ci_data, normalization :
         util.numpy_array_2d_to_fits(array_2d=ci_data.ci_pre_cti,
                                     file_path=ci_data_path + 'ci_pre_cti_' + str(int(normalization)) + '.fits',
                                     overwrite=True),
         datas, normalizations))