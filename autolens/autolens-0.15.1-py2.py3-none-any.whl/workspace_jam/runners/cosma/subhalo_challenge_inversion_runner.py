from autofit.tools import path_util
from autofit import conf
import sys
from autolens.data import ccd
from autolens.data.array import mask as msk

import os

# Given your username is where your data is stored, you'll need to put your cosma username here.
cosma_username = 'pdtw24'
cosma_path = '/cosma5/data/autolens/'

workspace_path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path, and override the output path with the Cosma path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=cosma_path + 'output_' + cosma_username)

# The fifth line of this batch script - '#SBATCH --array=1-17' is what species this. Its telling Cosma we're going to
# run 17 jobs, and the id's of those jobs will be numbered from 1 to 17. Infact, these ids are passed to this runner,
# and we'll use them to ensure that each jobs loads a different image. Lets get the cosma array id for our job.
cosma_array_id = int(sys.argv[1])

### Subhalo challenge data strings ###

data_type = 'subhalo_challenge_inv_4'

if cosma_array_id == 1 or cosma_array_id  == 2:
    data_level = 'level_0'
else:
    data_level = 'level_1'

pixel_scale = 0.00976562

data_name = []
data_name.append('') # Task number beings at 1, so keep index 0 blank
data_name.append('large_hi_sn_system_1') # Index 1
data_name.append('small_hi_sn_system_1') # Index 2

data_name.append('large_hi_sn_system_1') # Index 3
data_name.append('large_hi_sn_system_2') # Index 4
data_name.append('large_md_sn_system_1') # Index 5
data_name.append('large_md_sn_system_2') # Index 6
data_name.append('large_lo_sn_system_1') # Index 7
data_name.append('large_lo_sn_system_2') # Index 8
data_name.append('small_hi_sn_system_1') # Index 9
data_name.append('small_hi_sn_system_2') # Index 10
data_name.append('small_md_sn_system_1') # Index 11
data_name.append('small_md_sn_system_2') # Index 12
data_name.append('small_lo_sn_system_1') # Index 13
data_name.append('small_lo_sn_system_2') # Index 14

data_name = data_name[cosma_array_id]

data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=cosma_path, folder_names=['data_share', data_type, data_level, data_name])

resized_shape = (700, 700)

ccd_data = ccd.load_ccd_data_from_fits(image_path=data_path + 'image.fits',
                                       psf_path=data_path + 'psf.fits',
                                       noise_map_path=data_path + 'noise_map.fits',
                                       pixel_scale=pixel_scale, resized_ccd_shape=resized_shape)

mask = msk.load_mask_from_fits(mask_path=data_path + 'mask_irregular.fits', pixel_scale=pixel_scale)
mask = mask.resized_scaled_array_from_array(new_shape=resized_shape)

# mask = msk.Mask.circular(shape=ccd_data.shape, pixel_scale=ccd_data.pixel_scale, radius_arcsec=3.2)
# ccd_plotters.plot_ccd_subplot(ccd_data=ccd_data, mask=mask)

from workspace_jam.pipelines import pipeline_subhalo_inversion_no_lens_light

pipeline = pipeline_subhalo_inversion_no_lens_light.make_pipeline(phase_folders=[data_type, data_level, data_name])

pipeline.run(data=ccd_data, mask=mask)
