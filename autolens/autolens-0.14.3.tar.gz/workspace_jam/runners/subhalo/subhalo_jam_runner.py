from autofit.tools import path_util
from autofit import conf
import os

from autolens.data import ccd
from autolens.data.array import mask as msk
from autolens.data.plotters import ccd_plotters

import os

workspace_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output')

data_type = 'subhalo_jam'
data_name = 'lens_with_05_subhalo_cuspy_source'
pixel_scale = 0.05

data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=[data_type, data_name])

ccd_data = ccd.load_ccd_data_from_fits(image_path=data_path + '/image.fits',
                                       psf_path=data_path + '/psf.fits',
                                       noise_map_path=data_path + '/noise_map.fits', pixel_scale=pixel_scale)

from workspace_jam.pipelines import pipeline_subhalo_inversion_no_lens_light

pipeline = \
    pipeline_subhalo_inversion_no_lens_light.make_pipeline(phase_folders=[data_type, data_name])

pipeline.run(data=ccd_data)