from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior
from autofit.mapper import prior_model
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform an analysis which fits two parallel trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses four phases:

# Phase 1) Fit a small section (60 columns of every charge injection) using a parallel CTI model
#          with 1 trap species and a model for the parallel CCD volume filling parameters.

# Phase 2) Fit a small section (again, 60 columns) using a parallel CTI model with 2 trap species and a model for the
#          parallel CCD volume filling parameters. The priors on trap densities and volume filling parameters are
#          initialized from the results of phase 1.

# Phase 3) Use the best-fit model from phase 2 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 4) Refit the phase 2 model, using priors initialized from the results of phase 2 and the scaled noise-map
#          computed in phase 3.

def make_pipeline(phase_folders=None, tag_phases=True, columns=None, rows=None, mask_function=msk.Mask.empty_for_shape,
                  cosmic_ray_parallel_buffer=None, cosmic_ray_serial_buffer=None, cosmic_ray_diagonal_buffer=None):

    pipeline_name = 'pipeline_parallel_x2_serial_x3_species'

    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the data with a one species parallel CTI model and parallel CCD filling model. In this
    # phase we will:

    # 1) Extract and fit the 10 columns of each charge injection region which is furthest from the clocking direction
    # (and therefore least affected by parallel CTI).

    class ParallelPhase(ph.ParallelPhase):

        def pass_priors(self, results):
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0

    phase1 = ParallelPhase(phase_name='phase_1_parallel_x1_species_initialize', phase_folders=phase_folders,
                           tag_phases=tag_phases,
                           optimizer_class=nl.MultiNest,
                           parallel_species=[prior_model.PriorModel(arctic_params.Species)],
                           parallel_ccd=arctic_params.CCD, mask_function=mask_function,
                           columns=columns,
                           cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                           cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                           cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    # You'll see these lines throughout all of the example pipelines. They are used to make MultiNest sample the \
    # non-linear parameter space faster.

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 30
    phase1.optimizer.sampling_efficiency = 0.2

    ### PHASE 2 ###

    # In phase 2, we will fit the data with a two species parallel CTI model and parallel CCD filling model. In this
    # phase we will:

    # 1) As in phase 1, extract and fit the 10 columns of charge injection imaging data closest to the read-out
    # register.
    # 2) Use priors on the trap density and ccd volume filling parameters based on the results of phase 1.

    class ParallelPhase(ph.ParallelPhase):

        def pass_priors(self, results):

            previous_total_density = results[-1].constant.parallel_species[0].trap_density

            self.parallel_species[0].trap_density = prior.UniformPrior(lower_limit=0.0,
                                                                       upper_limit=previous_total_density)
            self.parallel_species[1].trap_density = prior.UniformPrior(lower_limit=0.0,
                                                                       upper_limit=previous_total_density)
            self.parallel_species[0].trap_lifetime = prior.UniformPrior(lower_limit=0.0, upper_limit=30.0)
            self.parallel_species[1].trap_lifetime = prior.UniformPrior(lower_limit=0.0, upper_limit=30.0)

            self.parallel_ccd.well_notch_depth = \
                results.from_phase('phase_1_parallel_x1_species_initialize').variable.parallel_ccd.well_notch_depth
            self.parallel_ccd.well_fill_beta = \
                results.from_phase('phase_1_parallel_x1_species_initialize').variable.parallel_ccd.well_fill_beta
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0

    phase2 = ParallelPhase(phase_name='phase_2_parallel_x2_species_initialize', phase_folders=phase_folders,
                           tag_phases=tag_phases,
                           parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                             prior_model.PriorModel(arctic_params.Species)],
                           parallel_ccd=arctic_params.CCD,
                           optimizer_class=nl.MultiNest, mask_function=mask_function,
                           columns=columns,
                           cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                           cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                           cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase2.optimizer.const_efficiency_mode = True
    phase2.optimizer.n_live_points = 50
    phase2.optimizer.sampling_efficiency = 0.2

    ### PHASE 3 ###

    # In phase 3, we will fit the data with a one species serial CTI model and serial CCD filling model. In this
    # phase we will:

    # 1) Extract and fit the 10 rows of each charge injection region which is furthest from the clocking direction (and
    # therefore least affected by parallel CTI).
    # 2) Use the best fit parallel CTI model of the previous phase to add parallel CTI, but fix its model parameters.

    class ParallelSerialPhase(ph.ParallelSerialPhase):

        def pass_priors(self, results):
            
            self.parallel_ccd = results.from_phase('phase_2_parallel_x2_species_initialize').constant.parallel_ccd
            self.parallel_species = results.from_phase('phase_2_parallel_x2_species_initialize').constant.parallel_species
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0
            
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase3 = ParallelSerialPhase(phase_name='phase_3_serial_x1_species_initialize', phase_folders=phase_folders,
                                 tag_phases=tag_phases,
                                 parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                   prior_model.PriorModel(arctic_params.Species)],
                                 parallel_ccd=arctic_params.CCD,
                                 serial_species=[prior_model.PriorModel(arctic_params.Species)],
                                 serial_ccd=arctic_params.CCD,
                                 optimizer_class=nl.MultiNest, mask_function=mask_function,
                                 cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                 cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                 cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    # You'll see these lines throughout all of the example pipelines. They are used to make MultiNest sample the \
    # non-linear parameter space faster.

    phase3.optimizer.const_efficiency_mode = True
    phase3.optimizer.n_live_points = 30
    phase3.optimizer.sampling_efficiency = 0.2

    ### PHASE 4 ###

    # In phase 4, we will fit the data with a three species serial CTI model and serial CCD filling model. In this
    # phase we will:

    # 1) As in phase 1, extract and fit the 10 rows of charge injection imaging data closest to the read-out
    # register.
    # 2) Use priors on the trap density and ccd volume filling parameters based on the results of phase 1.
    # 2) Use the best fit parallel CTI model of phase 2 to add parallel CTI, but fix its model parameters.

    class ParallelSerialPhase(ph.ParallelSerialPhase):

        def pass_priors(self, results):
            
            self.parallel_ccd = results.from_phase('phase_2_parallel_x2_species_initialize').constant.parallel_ccd
            self.parallel_species = results.from_phase('phase_2_parallel_x2_species_initialize').constant.parallel_species
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0

            previous_total_density = results[-1].constant.serial_species[0].trap_density

            self.serial_species[0].trap_density = prior.UniformPrior(lower_limit=0.0, upper_limit=previous_total_density)
            self.serial_species[1].trap_density = prior.UniformPrior(lower_limit=0.0, upper_limit=previous_total_density)
            self.serial_species[2].trap_density = prior.UniformPrior(lower_limit=0.0, upper_limit=previous_total_density)
            self.serial_species[0].trap_lifetime = prior.UniformPrior(lower_limit=0.0, upper_limit=30.0)
            self.serial_species[1].trap_lifetime = prior.UniformPrior(lower_limit=0.0, upper_limit=30.0)
            self.serial_species[2].trap_lifetime = prior.UniformPrior(lower_limit=0.0, upper_limit=30.0)

            self.serial_ccd.well_notch_depth = \
                results.from_phase('phase_3_serial_x1_species_initialize').variable.serial_ccd.well_notch_depth
            self.serial_ccd.well_fill_beta = \
                results.from_phase('phase_3_serial_x1_species_initialize').variable.serial_ccd.well_fill_beta
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase4 = ParallelSerialPhase(phase_name='phase_4_serial_x3_species_initialize', phase_folders=phase_folders,
                                 tag_phases=tag_phases,
                                 parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                   prior_model.PriorModel(arctic_params.Species)],
                                 parallel_ccd=arctic_params.CCD,
                                 serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                 prior_model.PriorModel(arctic_params.Species),
                                                 prior_model.PriorModel(arctic_params.Species)],
                                 serial_ccd=arctic_params.CCD,
                                 optimizer_class=nl.MultiNest, mask_function=mask_function,
                                 cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                 cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                 cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase4.optimizer.const_efficiency_mode = True
    phase4.optimizer.n_live_points = 60
    phase4.optimizer.sampling_efficiency = 0.2

    ### PHASE 5 ###

    # In phase 5, we will fit the data with a two species parallel and three species serial CTI model. In this
    # phase we will:

    # 1) Initialize the priors on this model from phases 2 and 4 of the pipeline.

    class ParallelSerialPhase(ph.ParallelSerialPhase):

        def pass_priors(self, results):
            
            self.parallel_ccd = results.from_phase('phase_2_parallel_x2_species_initialize').variable.parallel_ccd
            self.parallel_species = results.from_phase('phase_2_parallel_x2_species_initialize').variable.parallel_species
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0
            self.serial_ccd = results.from_phase('phase_4_serial_x3_species_initialize').variable.serial_ccd
            self.serial_species = results.from_phase('phase_4_serial_x3_species_initialize').variable.serial_species
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase5 = ParallelSerialPhase(phase_name='phase_5_parallel_x2_serial_x3_species_initialize', 
                                 phase_folders=phase_folders,
                                 tag_phases=tag_phases,
                                 parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                   prior_model.PriorModel(arctic_params.Species)],
                                 parallel_ccd=arctic_params.CCD,
                                 serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                 prior_model.PriorModel(arctic_params.Species),
                                                 prior_model.PriorModel(arctic_params.Species)],
                                 serial_ccd=arctic_params.CCD,
                                 optimizer_class=nl.MultiNest, mask_function=mask_function,
                                 cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                 cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                 cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase5.optimizer.const_efficiency_mode = True
    phase5.optimizer.n_live_points = 80
    phase5.optimizer.sampling_efficiency = 0.2

    ### PHASE 6 ###

    # The best fit model of phase 5 is used to create a 'noise-scaling' map for every charge injection image. These
    # noise-scaling maps are used in conjunction with 'hyper-noise' models to scale the noise-maps in a way that
    # equally weights the fit across all charge injection images.

    class ParallelSerialHyperModelFixedPhase(ph.ParallelSerialHyperPhase):

        def pass_priors(self, results):

            self.parallel_species = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').constant.parallel_species
            self.parallel_ccd = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').constant.parallel_ccd
            self.serial_species = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').constant.serial_species
            self.serial_ccd = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').constant.serial_ccd

    phase6 = ParallelSerialHyperModelFixedPhase(phase_name='phase_6_noise_scaling', phase_folders=phase_folders,
                                                tag_phases=tag_phases,
                                                parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                                  prior_model.PriorModel(arctic_params.Species)],
                                                parallel_ccd=arctic_params.CCD,
                                                serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                                prior_model.PriorModel(arctic_params.Species),
                                                                prior_model.PriorModel(arctic_params.Species)],
                                                serial_ccd=arctic_params.CCD,
                                                optimizer_class=nl.MultiNest, mask_function=mask_function,
                                                cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                                cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                                cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase6.optimizer.const_efficiency_mode = True
    phase6.optimizer.n_live_points = 30
    phase6.optimizer.sampling_efficiency = 0.2

    ### PHASE 7 ###

    # In phase 7, we will fit the data with a 2 species parallel and 3 species serial CTI model. In this
    # phase we will:

    # 1) Use the scaled noise-map computed in phase 6.
    # 2) Initialize the priors on the parallel and serial CTI models from the results of phase 5.

    class ParallelSerialHyperFixedPhase(ph.ParallelSerialHyperPhase):

        def pass_priors(self, results):

            self.hyper_noise_scalars = results.from_phase('phase_6_noise_scaling').constant.hyper_noise_scalars

            self.parallel_species = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').variable.parallel_species
            self.parallel_ccd = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').variable.parallel_ccd
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0

            self.serial_species = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').variable.serial_species
            self.serial_ccd = \
                results.from_phase('phase_5_parallel_x2_serial_x3_species_initialize').variable.serial_ccd
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase7 = ParallelSerialHyperFixedPhase(phase_name='phase_7_parallel_x2_serial_x3_species', phase_folders=phase_folders,
                                           tag_phases=tag_phases,
                                           parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                             prior_model.PriorModel(arctic_params.Species)],
                                           parallel_ccd=arctic_params.CCD,
                                           serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                           prior_model.PriorModel(arctic_params.Species),
                                                           prior_model.PriorModel(arctic_params.Species)],
                                           serial_ccd=arctic_params.CCD,
                                           optimizer_class=nl.MultiNest, mask_function=mask_function,
                                           cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                           cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                           cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    # For the final CTI model, constant efficiency mode has a tendency to sample parameter space too fast and infer an
    # inaccurate model. Thus, we turn it off for phase 2.

    phase7.optimizer.const_efficiency_mode = False
    phase7.optimizer.n_live_points = 50
    phase7.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1, phase2, phase3, phase4, phase5, phase6, phase7)