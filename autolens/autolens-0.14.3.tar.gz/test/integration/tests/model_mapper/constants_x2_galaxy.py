import os

from autofit import conf
from autofit.optimize import non_linear as nl
from autolens.model.galaxy import galaxy_model as gm
from autolens.pipeline import phase as ph
from autolens.pipeline import pipeline as pl
from autolens.model.profiles import light_profiles as lp
from test.integration import integration_util
from test.simulation import simulation_util

test_type = 'model_mapper'
test_name = "constants_x2_galaxy"

test_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))
output_path = test_path + 'output/'
config_path = test_path + 'config'
conf.instance = conf.Config(config_path=config_path, output_path=output_path)

def pipeline():

    integration_util.reset_paths(test_name=test_name, output_path=output_path)
    ccd_data = simulation_util.load_test_ccd_data(data_type='lens_only_dev_vaucouleurs', data_resolution='LSST')
    pipeline = make_pipeline(test_name=test_name)
    pipeline.run(data=ccd_data)


def make_pipeline(test_name):

    class MMPhase(ph.LensPlanePhase):

        def pass_priors(self, results):
            self.lens_galaxies.lens_0.light.axis_ratio = 0.2
            self.lens_galaxies.lens_0.light.phi = 90.0
            self.lens_galaxies.lens_0.light.centre_0 = 1.0
            self.lens_galaxies.lens_0.light.centre_1 = 2.0
            self.lens_galaxies.lens_1.light.axis_ratio = 0.2
            self.lens_galaxies.lens_1.light.phi = 90.0
            self.lens_galaxies.lens_1.light.centre_0 = 1.0
            self.lens_galaxies.lens_1.light.centre_1 = 2.0

    phase1 = MMPhase(phase_name='phase_1', phase_folders=[test_type, test_name],
                     lens_galaxies=dict(lens_0=gm.GalaxyModel(light=lp.EllipticalSersic),
                                        lens_1=gm.GalaxyModel(light=lp.EllipticalSersic)),
                     optimizer_class=nl.MultiNest)

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 20
    phase1.optimizer.sampling_efficiency = 0.8

    return pl.PipelineImaging(test_name, phase1)


if __name__ == "__main__":
    pipeline()
