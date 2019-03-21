from autofit.tools import path_util
from autofit import conf

from autolens.data import ccd

import os

workspace_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output')

data_type = 'slacs'

data_name = 'slacs0252+0039'
data_name = 'slacs0737+3216'
data_name = 'slacs1430+4105'
data_name = 'slacs2238-0754'

pixel_scale = 0.03

data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=[data_type, data_type])

ccd_data = ccd.load_ccd_data_from_fits(image_path=data_path + 'F814W_image.fits',
                                       psf_path=data_path + 'F814W_psf.fits',
                                       noise_map_path=data_path + 'F814W_noise_map.fits', pixel_scale=pixel_scale)

from workspace_jam.pipelines import pipeline_subhalo_inversion_lens_light

pipeline = \
    pipeline_subhalo_inversion_lens_light.make_pipeline(phase_folders=[data_type, data_name])

pipeline.run(data=ccd_data)