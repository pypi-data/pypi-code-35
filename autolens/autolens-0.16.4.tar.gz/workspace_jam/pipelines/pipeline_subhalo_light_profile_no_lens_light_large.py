from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior
from autofit.tools import phase as autofit_ph
from autolens.data.array import mask as msk
from autolens.model.galaxy import galaxy_model as gm
from autolens.pipeline import phase as ph
from autolens.pipeline import pipeline
from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp
from autolens.model.inversion import pixelizations as pix
from autolens.model.inversion import regularization as reg

import os

# In this pipeline, we'll perform a subhalo analysis which fits a source galaxy using a light profile
# followed by an inversion, where the lens galaxy's light is not present in the image. Two grid-searches will then be
# performed, to assess our sensitivity to subhalos and to attempt to detect subhalos in the observed image. The
# pipeline comprises four phases:

# Phase 1) Fit the lens galaxy's mass (SIE) and source galaxy's light using a single Sersic light profile.

# Phase 2) Fit the lens galaxy's mass (SIE) and source galaxy's light using an inversion, initializing the priors
#          of the lens the results of Phase 1.

# Phase 3) Perform the sensitivity analysis, using an ordinary grid search over subhalo (y,x) coordinates and mass.

# Phase 4) Perform the subhalo detection analysis, using a Multinest grid search oer subhalo (y,x) coordinate cells,
#          where each phase optimizes the subhalo position in these cells as well as its mass and concentration.

def make_pipeline(phase_folders=None):

    pipeline_name = 'pipeline_subhalo_light_profile_no_lens_light_large'

    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the lens galaxy's mass and one source galaxy, where we:

    # 1) Set our priors on the lens galaxy (y,x) centre such that we assume the image is centred around the lens galaxy.

    class LensSourcePhase(ph.LensSourcePlanePhase):

        def pass_priors(self, results):

            self.lens_galaxies.lens.mass.centre_0 = prior.GaussianPrior(mean=0.0, sigma=0.1)
            self.lens_galaxies.lens.mass.centre_1 = prior.GaussianPrior(mean=0.0, sigma=0.1)

            self.lens_galaxies.subhalo.mass.kappa_s = prior.UniformPrior(lower_limit=0.0001, upper_limit=0.1)
            self.lens_galaxies.subhalo.mass.scale_radius = prior.UniformPrior(lower_limit=0.0, upper_limit=5.0)
            self.lens_galaxies.subhalo.mass.centre_0 = 0.898
            self.lens_galaxies.subhalo.mass.centre_1 = 1.66

    phase1 = LensSourcePhase(phase_name='phase_1_source', phase_folders=phase_folders,
                             lens_galaxies=dict(lens=gm.GalaxyModel(mass=mp.EllipticalIsothermal,
                                                                    shear=mp.ExternalShear),
                                                subhalo=gm.GalaxyModel(mass=mp.SphericalTruncatedNFWChallenge)),
                             source_galaxies=dict(source=gm.GalaxyModel(light=lp.EllipticalSersic)),
                             optimizer_class=nl.MultiNest)

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 80
    phase1.optimizer.sampling_efficiency = 0.2

    return pipeline.PipelineImaging(pipeline_name, phase1)