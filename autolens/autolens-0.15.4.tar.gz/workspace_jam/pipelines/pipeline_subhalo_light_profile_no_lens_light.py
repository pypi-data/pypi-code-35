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

    pipeline_name = 'pipeline_subhalo_light_profile_no_lens_light'

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

    phase1 = LensSourcePhase(phase_name='phase_1_source', phase_folders=phase_folders,
                             lens_galaxies=dict(lens=gm.GalaxyModel(mass=mp.EllipticalIsothermal,
                                                                    shear=mp.ExternalShear)),
                             source_galaxies=dict(source=gm.GalaxyModel(light=lp.EllipticalSersic)),
                             bin_up_factor=3,
                             optimizer_class=nl.MultiNest)

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 80
    phase1.optimizer.sampling_efficiency = 0.2

    ### Phase 2 ###

    # In phase 2, we perform the sensitivity analysis of our lens, using a grid search of subhalo (y,x) coordinates and
    # mass, where:

    # 1) The lens model and source-pixelization parameters are held fixed to the best-fit values from phase 2.

    class GridPhase(ph.LensSourcePlanePhase):

        def pass_priors(self, results):

            self.lens_galaxies.lens.mass = results.from_phase('phase_1_source').constant.lens.mass
            self.source_galaxies.source = results.from_phase('phase_1_source').constant.source

            self.lens_galaxies.subhalo.mass.centre_0 = prior.UniformPrior(lower_limit=-2.0, upper_limit=2.0)
            self.lens_galaxies.subhalo.mass.centre_1 = prior.UniformPrior(lower_limit=-2.0, upper_limit=2.0)
            self.lens_galaxies.subhalo.mass.kappa_s = prior.UniformPrior(lower_limit=0.00001, upper_limit=0.002)
            self.lens_galaxies.subhalo.mass.scale_radius = 5.0

    phase2 = GridPhase(phase_name='phase_2_sensitivity', phase_folders=phase_folders,
                       lens_galaxies=dict(lens=gm.GalaxyModel(mass=mp.EllipticalIsothermal,
                                                              shear=mp.ExternalShear),
                                          subhalo=gm.GalaxyModel(mass=mp.SphericalNFW)),
                       source_galaxies=dict(source=gm.GalaxyModel(light=lp.EllipticalSersic)),
                       optimizer_class=nl.GridSearch)

    ### Phase 3 ###

    # In phase 3, we attempt to detect subhalos, by performing a NxN grid search of MultiNest searches, where:

    # 1) The lens model and source-pixelization parameters are held fixed to the best-fit values from phase 1.
    # 2) Each grid search varies the subhalo (y,x) coordinates and mass as free parameters.
    # 3) The priors on these (y,x) coordinates are UniformPriors, with limits corresponding to the grid-cells.

    class GridPhase(autofit_ph.as_grid_search(ph.LensSourcePlanePhase)):

        @property
        def grid_priors(self):
            return [self.variable.subhalo.mass.centre_0, self.variable.subhalo.mass.centre_1]

        def pass_priors(self, results):

            self.lens_galaxies.subhalo.mass.centre_0 = prior.UniformPrior(lower_limit=-2.0, upper_limit=2.0)
            self.lens_galaxies.subhalo.mass.centre_1 = prior.UniformPrior(lower_limit=-2.0, upper_limit=2.0)
            self.lens_galaxies.subhalo.mass.kappa_s = prior.UniformPrior(lower_limit=0.0001, upper_limit=0.1)
            self.lens_galaxies.subhalo.mass.scale_radius = prior.UniformPrior(lower_limit=0.0, upper_limit=5.0)

            self.lens_galaxies.lens.mass.centre = results.from_phase('phase_1_source').constant.lens.mass.centre
            self.lens_galaxies.lens.mass.axis_ratio = results.from_phase('phase_1_source').constant.lens.mass.axis_ratio
            self.lens_galaxies.lens.mass.phi = results.from_phase('phase_1_source').constant.lens.mass.phi

            self.lens_galaxies.lens.mass.einstein_radius = \
                results.from_phase('phase_1_source').variable.lens.mass.einstein_radius

            self.lens_galaxies.lens.shear = results.from_phase('phase_1_source').constant.lens.shear
            self.source_galaxies.source = results.from_phase('phase_1_source').variable.source

    phase3 = GridPhase(phase_name='phase_3_subhalo_search', phase_folders=phase_folders,
                       lens_galaxies=dict(lens=gm.GalaxyModel(mass=mp.EllipticalIsothermal,
                                                              shear=mp.ExternalShear),
                                          subhalo=gm.GalaxyModel(mass=mp.SphericalTruncatedNFWChallenge)),
                       source_galaxies=dict(source=gm.GalaxyModel(light=lp.EllipticalSersic)),
                       number_of_steps=4, optimizer_class=nl.MultiNest)

    phase3.optimizer.const_efficiency_mode = True
    phase3.optimizer.n_live_points = 50
    phase3.optimizer.sampling_efficiency = 0.3

    class SubhaloPhase(ph.LensSourcePlanePhase):

        def pass_priors(self, results):

            self.lens_galaxies.lens.mass = results.from_phase('phase_1_source').variable.lens.mass
            self.lens_galaxies.lens.shear = results.from_phase('phase_1_source').variable.lens.shear
            self.lens_galaxies.lens.subhalo = results.from_phase('phase_3_subhalo_search').best_result.variable.lens.subhalo
            self.source_galaxies.source = results.from_phase('phase_3_subhalo_search').best_result.variable.source

    phase4 = SubhaloPhase(phase_name='phase_4_subhalo', phase_folders=phase_folders,
                          lens_galaxies=dict(lens=gm.GalaxyModel(mass=mp.EllipticalIsothermal,
                                                                 shear=mp.ExternalShear),
                                             subhalo=gm.GalaxyModel(mass=mp.SphericalTruncatedNFWChallenge)),
                          source_galaxies=dict(source=gm.GalaxyModel(light=lp.EllipticalSersic)),
                          optimizer_class=nl.MultiNest)

    phase4.optimizer.const_efficiency_mode = True
    phase4.optimizer.n_live_points = 80
    phase4.optimizer.sampling_efficiency = 0.3

    return pipeline.PipelineImaging(pipeline_name, phase1, phase3, phase4)