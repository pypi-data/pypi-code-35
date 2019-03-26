from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior
from autolens.data.array import mask as msk
from autolens.model.galaxy import galaxy_model as gm
from autolens.pipeline import phase as ph
from autolens.pipeline import pipeline
from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp
from autolens.model.inversion import pixelizations as pix
from autolens.model.inversion import regularization as reg

# This pipelines assumes a continuation from the 'pipelines/initializer/lens_light_sersic_mass_sie_source_sersic'
# pipeline, as follows:

# - The Sersic light profile initializes the Sersic (bulge) + Exponential (envelope) parameters fitted in this pipeline.
# - The SIE mass profile initializes the SIE and power-law mass profiles fitted in this phase.
# - The Sersic source light profile initializes the Sersic source light profile fitted in this phase.

# In this pipeline, we'll perform a basic analysis which initializes a lens model (the lens's light, mass and source's \
# light) and then fits the source galaxy using an inversion. This pipeline uses four phases:

# Phase 1) Fit the lens galaxy's light using an elliptical Sersic light profile.

# Phase 2) Use this lens subtracted image to fit the lens galaxy's mass (SIE+Shear) and source galaxy's light (Sersic).

# Phase 4) Initialize the resolution and regularization coefficient of the inversion using the best-fit lens model from
#          phases 1 and 2.

# Phase 5) Refit the lens galaxy's light and mass models using an inversion, with lens galaxy priors initialized from
#          phases 1 and 2 and source-pixelization parameters from phase 3.

# The first 3 phases of this pipeline are identical to the 'lens_light_and_x1_source_parametric.py' pipeline.

def make_pipeline(phase_folders=None):

    pipeline_name = 'pipeline_lens_light_bulge_and_envelope_mass_power_law_source_sersic'

    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit only the lens galaxy's light, where we:

    # 1) Set our priors on the lens galaxy (y,x) centre such that we assume the image is centred around the lens galaxy.
    # 2) Use a circular mask which includes the lens and source galaxy light.

    class LensPhase(ph.LensPlanePhase):

        def pass_priors(self, results):

            self.lens_galaxies.lens.light.centre_0 = prior.GaussianPrior(mean=0.0, sigma=0.1)
            self.lens_galaxies.lens.light.centre_1 = prior.GaussianPrior(mean=0.0, sigma=0.1)

    phase1 = LensPhase(phase_name='phase_1_lens_light_only', phase_folders=phase_folders,
                       lens_galaxies=dict(lens=gm.GalaxyModel(light=lp.EllipticalSersic)),
                       optimizer_class=nl.MultiNest, mask_function=mask_function_circular)

    # You'll see these lines throughout all of the example pipelines. They are used to make MultiNest sample the \
    # non-linear parameter space faster (if you haven't already, checkout the tutorial '' in howtolens/chapter_2).

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 30
    phase1.optimizer.sampling_efficiency = 0.3

    return pipeline.PipelineImaging(pipeline_name, phase1, phase2, phase3)