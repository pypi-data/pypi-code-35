from autofit import conf
from autofit import aggregator
import os

# Setup the path to the workspace, using a relative directory name.
workspace_path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path and output path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output')

agg = aggregator.Aggregator(directory=workspace_path + 'output')

pipeline = 'pipeline_parallel_x2_species'
phase = 'phase_4_final'

# print(agg.phases_with(pipeline=pipeline, phase=phase))
print(agg.model_results(pipeline=pipeline, phase=phase))