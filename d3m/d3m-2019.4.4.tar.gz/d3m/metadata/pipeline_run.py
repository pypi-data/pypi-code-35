import copy
import datetime
import enum
import json
import logging
import os.path
import re
import typing
import uuid
import yaml

import git  # type: ignore
import GPUtil  # type: ignore

import d3m
from d3m import container, environment_variables, exceptions, utils, types
from d3m.metadata import base as metadata_base, hyperparams as hyperparams_module, pipeline as pipeline_module, problem
from d3m.primitive_interfaces import base

__all__ = ('PipelineRun', 'User', 'RuntimeEnvironment')

logger = logging.getLogger(__name__)

DOCKER_MAC_ADDRESS_MASK = 0x0242ac110000
PROC_INFO_RE = re.compile(r'^([^:]+?)\s*:\s*(.*)$')
PROC_MEMORY_PATH = '/proc/meminfo'
PROC_TOTAL_MEMORY_KEY = 'MemTotal'
CGROUP_MEMORY_LIMIT_PATH = '/sys/fs/cgroup/memory/memory.limit_in_bytes'
CGROUP_CPU_SHARES_PATH = '/sys/fs/cgroup/cpu/cpu.shares'

# Comma because we unpack the list of validators returned from "load_schema_validators".
PIPELINE_RUN_SCHEMA_VALIDATOR, = utils.load_schema_validators(metadata_base.SCHEMAS, ('pipeline_run.json',))

PIPELINE_RUN_SCHEMA_VERSION = 'https://metadata.datadrivendiscovery.org/schemas/v0/pipeline_run.json'


class User(dict):
    def __init__(self, id_: str, chosen: bool = False, rationale: str = None) -> None:
        super().__init__()

        self['id'] = id_
        self['chosen'] = chosen

        if rationale is not None:
            self['rationale'] = rationale

    @classmethod
    def _yaml_representer(cls, dumper: yaml.Dumper, data: typing.Any) -> typing.Any:
        return dumper.represent_dict(data)


yaml.Dumper.add_representer(User, User._yaml_representer)
yaml.SafeDumper.add_representer(User, User._yaml_representer)


class PipelineRunStep:
    def __init__(
        self, step_type: metadata_base.PipelineStepType, start: str, environment: typing.Dict[str, typing.Any] = None
    ) -> None:
        self.type = step_type
        self.status: typing.Dict[str, typing.Any] = {}
        self.start: str = start
        self.end: str = None
        self.environment = environment

    def to_json_structure(self) -> typing.Dict:
        if self.start is None:
            raise exceptions.InvalidStateError("Start timestamp not set.")

        if self.end is None:
            raise exceptions.InvalidStateError("End timestamp not set.")

        if 'state' not in self.status:
            raise exceptions.InvalidStateError("Status not set.")

        json_structure = {
            'type': self.type.name,
            'status': self.status,
            'start': self.start,
            'end': self.end
        }

        if self.environment is not None:
            json_structure['environment'] = self.environment

        return json_structure

    def set_successful(self, message: str = None) -> None:
        self.status['state'] = metadata_base.PipelineRunStatusState.SUCCESS.name
        if message is not None and message:
            self.status['message'] = message

    def set_failed(self, message: str = None) -> None:
        self.status['state'] = metadata_base.PipelineRunStatusState.FAILURE.name
        if message is not None and message:
            self.status['message'] = message

    def set_end_timestamp(self) -> None:
        self.end = utils.datetime_for_json(datetime.datetime.now(datetime.timezone.utc))


class PipelineRunPrimitiveStep(PipelineRunStep):
    def __init__(
        self, step: pipeline_module.PrimitiveStep, start: str, environment: typing.Dict[str, typing.Any] = None,
    ) -> None:
        super().__init__(
            step_type=metadata_base.PipelineStepType.PRIMITIVE,
            start=start,
            environment=environment
        )

        self.hyperparams: hyperparams_module.Hyperparams = None
        self.pipeline_hyperparams: typing.Set[str] = None
        self.random_seed: typing.Optional[int] = None
        self.method_calls: typing.List[typing.Dict[str, typing.Any]] = []
        self.arguments = step.arguments

    def to_json_structure(self) -> typing.Dict:
        json_structure = super().to_json_structure()

        # Validate that the Method calls are finished, and they have status.
        for method_call in self.method_calls:
            if 'end' not in method_call:
                raise exceptions.InvalidStateError("End timestamp not set.")
            if 'status' not in method_call:
                raise exceptions.InvalidStateError("Status not set.")

        if self.method_calls:
            json_structure['method_calls'] = self.method_calls

        if self.random_seed is not None:
            json_structure['random_seed'] = self.random_seed

        hyperparams_json_structure = self._hyperparams_to_json_structure()
        if hyperparams_json_structure is not None:
            json_structure['hyperparams'] = hyperparams_json_structure

        return json_structure

    def _hyperparams_to_json_structure(self) -> typing.Optional[typing.Dict]:
        if self.hyperparams is None:
            return None

        hyperparams_json = {}

        for hyperparameter_name, value in self.hyperparams.items():
            if hyperparameter_name in self.pipeline_hyperparams:
                continue

            hyperparams_json[hyperparameter_name] = {
                'type': metadata_base.ArgumentType.VALUE.name,
                'data': self.hyperparams.configuration[hyperparameter_name].value_to_json_structure(value),
            }

        if hyperparams_json:
            return hyperparams_json
        else:
            return None

    def add_method_call(
        self, method_name: str, *, runtime_arguments: typing.Dict = None,
        environment: typing.Dict[str, typing.Any] = None
    ) -> int:
        """
        Returns
        -------
        int
            The id of the method call.
        """

        if runtime_arguments is None:
            runtime_arguments = {}
        else:
            # We convert everything directly to json structure.
            def recurse(item: typing.Any) -> typing.Any:
                if isinstance(item, enum.Enum):
                    return item.name
                elif not isinstance(item, typing.Dict):
                    return item
                else:
                    _json_structure = {}
                    for key, value in item.items():
                        _json_structure[key] = recurse(value)
                    return _json_structure

            runtime_arguments = recurse(runtime_arguments)

        if method_name == '__init__' and runtime_arguments:
            raise exceptions.InvalidArgumentValueError(
                f'MethodCall with method `__init__` cannot have arguments. '
                f'Hyper-parameters are the arguments to `__init__`.'
            )

        method_call: typing.Dict[str, typing.Any] = {
            'name': method_name,
        }

        if runtime_arguments:
            method_call['arguments'] = runtime_arguments

        # we store everything as json structure.
        if environment is not None:
            method_call['environment'] = environment

        self.method_calls.append(method_call)
        return len(self.method_calls) - 1

    def set_method_call_start_timestamp(self, method_call_id: int) -> None:
        self.method_calls[method_call_id]['start'] = utils.datetime_for_json(datetime.datetime.now())

    def set_method_call_end_timestamp(self, method_call_id: int) -> None:
        if 'start' not in self.method_calls[method_call_id]:
            raise exceptions.InvalidStateError("Start timestamp not set.")
        self.method_calls[method_call_id]['end'] = utils.datetime_for_json(datetime.datetime.now())

    def set_method_call_result_metadata(self, method_call_id: int, result: typing.Union[base.CallResult, base.MultiCallResult]) -> None:
        metadata = None
        if isinstance(result, base.CallResult):
            if result.value is not None and isinstance(result.value, types.Container):
                metadata = {
                    'value': result.value.metadata.to_json_structure()
                }
        elif isinstance(result, base.MultiCallResult):
            metadata = {
                produce_method_name: value.metadata.to_json_structure()
                for produce_method_name, value in result.values.items()
                if value is not None and isinstance(value, types.Container)
            }

        # check if metadata is empty
        if metadata is not None:
            for key, value in metadata.items():
                if value is not None:
                    self.method_calls[method_call_id]['metadata'] = metadata
                    break

    def set_method_call_successful(self, method_call_id: int, message: str = None) -> None:
        self.method_calls[method_call_id]['status'] = {
            'state': metadata_base.PipelineRunStatusState.SUCCESS.name,
        }
        if message is not None and message:
            self.method_calls[method_call_id]['status']['message'] = message

    def set_method_call_failed(self, method_call_id: int, message: str = None) -> None:
        self.method_calls[method_call_id]['status'] = {
            'state': metadata_base.PipelineRunStatusState.FAILURE.name,
        }
        if message is not None and message:
            self.method_calls[method_call_id]['status']['message'] = message

    def get_method_call_logging_callback(self, method_call_id: int) -> typing.Callable:
        if 'logging' not in self.method_calls[method_call_id]:
            self.method_calls[method_call_id]['logging'] = []
        return self.method_calls[method_call_id]['logging'].append


class PipelineRunSubpipelineStep(PipelineRunStep):
    def __init__(self, start: str, random_seed: int, environment: typing.Dict[str, typing.Any] = None) -> None:
        super().__init__(
            step_type=metadata_base.PipelineStepType.SUBPIPELINE,
            start=start,
            environment=environment,
        )

        self.random_seed = random_seed
        self.steps: typing.List[typing.Dict] = []

    def to_json_structure(self) -> typing.Dict:
        json_structure = super().to_json_structure()
        json_structure['random_seed'] = self.random_seed
        if self.steps:
            json_structure['steps'] = self.steps
        return json_structure

    def add_step(self, step: typing.Dict) -> None:
        self.steps.append(step)


class PipelineRun:
    STEPS = 'steps'
    METHOD_CALLS = 'method_calls'

    def __init__(
        self, pipeline: pipeline_module.Pipeline, problem_description: problem.Problem = None, *,
        phase: metadata_base.PipelineRunPhase, context: metadata_base.Context,
        environment: typing.Dict[str, typing.Any], random_seed: int, previous_pipeline_run_id: str = None,
        users: typing.Sequence[User] = None,
    ) -> None:
        self.schema = PIPELINE_RUN_SCHEMA_VERSION

        self.pipeline = {
            'id': pipeline.id,
            'digest': pipeline.get_digest(),
        }

        self.datasets: typing.List[typing.Dict[str, typing.Any]] = []

        self.problem: typing.Dict[str, typing.Any] = None
        if problem_description is not None:
            self._set_problem(problem_description)

        self.steps: typing.List[PipelineRunStep] = []
        self.status: typing.Dict[str, typing.Any] = {}
        self.start: str = None
        self.end: str = None

        self.run: typing.Dict[str, typing.Any] = {
            'phase': phase.name,
        }
        self.context = context
        self.previous_pipeline_run_id = previous_pipeline_run_id

        if users is None:
            self.users: typing.List[User] = []
        else:
            self.users = list(users)

        self.environment = environment
        self.random_seed = random_seed

        self._components: typing.Dict[str, typing.Any] = {}
        self._step_start_timestamps: typing.Dict[int, str] = {}

    def _to_json_structure(self) -> typing.Dict:
        if self.start is None:
            raise exceptions.InvalidStateError("Start timestamp not set.")

        if self.end is None:
            raise exceptions.InvalidStateError("End timestamp not set.")

        if 'state' not in self.status:
            raise exceptions.InvalidStateError('status not set')

        json_structure = {
            'schema': self.schema,
            'pipeline': self.pipeline,
            'datasets': self.datasets,
            'status': self.status,
            'start': self.start,
            'end': self.end,
            'run': self.run,
            'environment': self.environment,
            'random_seed': self.random_seed,
        }

        if self.steps:
            json_structure['steps'] = [step.to_json_structure() for step in self.steps]

        if self.previous_pipeline_run_id is not None:
            json_structure['previous_pipeline_run'] = {
                'id': self.previous_pipeline_run_id
            }

        if self.context is not None:
            json_structure['context'] = self.context.name

        if self.problem is not None:
            json_structure['problem'] = self.problem

        if self.users:
            json_structure['users'] = self.users

        json_structure['id'] = utils.compute_hash_id(json_structure)

        return json_structure

    def to_json_structure(self) -> typing.Dict:
        json_structure = self._to_json_structure()

        PIPELINE_RUN_SCHEMA_VALIDATOR.validate(json_structure)

        return json_structure

    def to_yaml(self, file: typing.TextIO, *, appending: bool = False, **kwargs: typing.Any) -> typing.Optional[str]:
        obj = self.to_json_structure()

        if 'default_flow_style' not in kwargs:
            kwargs['default_flow_style'] = False
        if appending and 'explicit_start' not in kwargs:
            kwargs['explicit_start'] = True

        return yaml.safe_dump(obj, stream=file, **kwargs)

    def add_input_dataset(self, dataset: container.Dataset) -> None:
        metadata = dataset.metadata.query(())
        self.datasets.append({
            'id': metadata['id'],
            'digest': metadata['digest']
        })

    def add_primitive_step(self, step: pipeline_module.PrimitiveStep) -> int:
        if not isinstance(step, pipeline_module.PrimitiveStep):
            raise exceptions.InvalidArgumentTypeError('step must be of type PrimitiveStep, not {}'.format(type(step)))
        self.steps.append(
            PipelineRunPrimitiveStep(step, self._step_start_timestamps[len(self.steps)])
        )
        return len(self.steps) - 1

    def _get_primitive_step(self, primitive_step_id: int) -> PipelineRunPrimitiveStep:
        if primitive_step_id >= len(self.steps):
            raise exceptions.InvalidArgumentValueError('There does not exist a step with id {}'.format(primitive_step_id))

        primitive_step = self.steps[primitive_step_id]
        if not isinstance(primitive_step, PipelineRunPrimitiveStep):
            raise exceptions.InvalidArgumentValueError('Step id {} does not refer to a PipelineRunPrimitiveStep'.format(primitive_step_id))

        return primitive_step

    def set_primitive_step_hyperparams(
        self, primitive_step_id: int,
        hyperparams: hyperparams_module.Hyperparams,
        pipeline_hyperparams: typing.Dict[str, typing.Dict],
    ) -> None:
        primitive_step = self._get_primitive_step(primitive_step_id)
        primitive_step.hyperparams = hyperparams
        primitive_step.pipeline_hyperparams = set(pipeline_hyperparams.keys())

    def set_primitive_step_random_seed(self, primitive_step_id: int, random_seed: int) -> None:
        primitive_step = self._get_primitive_step(primitive_step_id)
        primitive_step.random_seed = random_seed

    def add_subpipeline_step(self, subpipeline_run: 'PipelineRun') -> int:
        pipeline_run_subpipeline_step = PipelineRunSubpipelineStep(
            self._step_start_timestamps[len(self.steps)], subpipeline_run.random_seed
        )

        for step_id, step in enumerate(subpipeline_run.steps):
            step_json = step.to_json_structure()
            pipeline_run_subpipeline_step.add_step(step_json)
            state = step_json['status']['state']
            message = step_json['status'].get('message', None)
            if state == metadata_base.PipelineRunStatusState.SUCCESS.name:
                pipeline_run_subpipeline_step.set_successful(message)
            elif state == metadata_base.PipelineRunStatusState.FAILURE.name:
                message = 'Failed on subpipeline step {}:\n{}'.format(step_id, message)
                pipeline_run_subpipeline_step.set_failed(message)
                if message is not None and message:
                    self.status['message'] = message
            else:
                raise exceptions.UnexpectedValueError('unknown subpipeline status state: {}'.format(state))

        self.steps.append(pipeline_run_subpipeline_step)

        return len(self.steps) - 1

    def add_method_call_to_primitive_step(
        self, primitive_step_id: int, method_name: str, *,
        runtime_arguments: typing.Dict = None, environment: typing.Dict[str, typing.Any] = None
    ) -> typing.Tuple[int, int]:
        if runtime_arguments is None:
            runtime_arguments = {}

        # TODO allow runtime arguments not specified in pipeline?
        primitive_step = self._get_primitive_step(primitive_step_id)
        method_call_id = primitive_step.add_method_call(
            method_name, runtime_arguments=runtime_arguments, environment=environment
        )
        return (primitive_step_id, method_call_id)

    def get_method_call_logging_callback(
        self, step_and_method_call_id: typing.Tuple[int, int]
    ) -> typing.Callable:
        step_id, method_call_id = step_and_method_call_id
        primitive_step = self._get_primitive_step(step_id)
        return primitive_step.get_method_call_logging_callback(method_call_id)

    def run_started(self) -> None:
        self.start = utils.datetime_for_json(datetime.datetime.now(datetime.timezone.utc))

    def _set_end_timestamp(self) -> None:
        self.end = utils.datetime_for_json(datetime.datetime.now(datetime.timezone.utc))

    def step_started(self, step_id: int) -> None:
        self._step_start_timestamps[step_id] = utils.datetime_for_json(datetime.datetime.now(datetime.timezone.utc))

    def method_call_started(self, step_and_method_call_id: typing.Tuple[int, int]) -> None:
        step_id, method_call_id = step_and_method_call_id
        primitive_step = self._get_primitive_step(step_id)
        primitive_step.set_method_call_start_timestamp(method_call_id)

    def set_method_call_result_metadata(
        self, step_and_method_call_id: typing.Tuple[int, int],
        result: typing.Union[base.CallResult, base.MultiCallResult]
    ) -> None:
        step_id, method_call_id = step_and_method_call_id
        primitive_step = self._get_primitive_step(step_id)
        primitive_step.set_method_call_result_metadata(method_call_id, result)

    def run_successful(self, message: str = None) -> None:
        self._set_end_timestamp()
        self.status['state'] = metadata_base.PipelineRunStatusState.SUCCESS.name
        if message is not None and message:
            self.status['message'] = message

    def step_successful(self, step_id: int, message: str = None) -> None:
        if step_id >= len(self.steps):
            raise exceptions.InvalidArgumentValueError('There does not exist a step with id {}'.format(step_id))
        self.steps[step_id].set_end_timestamp()
        self.steps[step_id].set_successful(message)

    def method_call_successful(self, step_and_method_call_id: typing.Tuple[int, int], message: str = None) -> None:
        step_id, method_call_id = step_and_method_call_id
        primitive_step = self._get_primitive_step(step_id)
        primitive_step.set_method_call_end_timestamp(method_call_id)
        primitive_step.set_method_call_successful(method_call_id, message)

    def run_failed(self, message: str = None) -> None:
        self._set_end_timestamp()
        self.status['state'] = metadata_base.PipelineRunStatusState.FAILURE.name
        if message is not None and message:
            self.status['message'] = message

    def step_failed(self, step_id: int, message: str = None) -> None:
        if step_id >= len(self.steps):
            return
        self.steps[step_id].set_end_timestamp()
        self.steps[step_id].set_failed(message)

    def method_call_failed(self, step_and_method_call_id: typing.Tuple[int, int], message: str = None) -> None:
        step_id, method_call_id = step_and_method_call_id
        if step_id >= len(self.steps):
            return
        primitive_step = self._get_primitive_step(step_id)
        primitive_step.set_method_call_end_timestamp(method_call_id)
        primitive_step.set_method_call_failed(method_call_id, message)

    def is_failed(self) -> bool:
        return self.status['state'] == metadata_base.PipelineRunStatusState.FAILURE.name

    def _set_problem(self, problem_description: problem.Problem) -> None:
        self.problem = {
            'id': problem_description['id'],
            'digest': problem_description['digest'],
        }

    def set_fold_group(self, fold_group_id: uuid.UUID, fold: int) -> None:
        self.run['fold_group'] = {
            'id': str(fold_group_id),
            'fold': fold,
        }

    def set_data_preparation_pipeline_run(
        self, data_preparation_pipeline_run: 'PipelineRun'
    ) -> None:
        if data_preparation_pipeline_run.start is None:
            raise exceptions.InvalidArgumentValueError("Data preparation pipeline start timestamp argument not provided.")

        if data_preparation_pipeline_run.end is None:
            raise exceptions.InvalidArgumentValueError("Data preparation pipeline end timestamp argument not provided.")

        self.run['data_preparation'] = {
            'pipeline': data_preparation_pipeline_run.pipeline,
            'steps': [step.to_json_structure() for step in data_preparation_pipeline_run.steps],
            'status': data_preparation_pipeline_run.status,
            'start': data_preparation_pipeline_run.start,
            'end': data_preparation_pipeline_run.end,
            'random_seed': data_preparation_pipeline_run.random_seed,
        }

        if data_preparation_pipeline_run.is_failed():
            message = 'Data preparation pipeline failed:\n{}'.format(
                data_preparation_pipeline_run.status['message']
            )
            self.status['state'] = metadata_base.PipelineRunStatusState.FAILURE.name
            if message is not None and message:
                self.status['message'] = message

    def set_scoring_pipeline_run(self, scoring_pipeline_run: 'PipelineRun') -> None:
        if scoring_pipeline_run.start is None:
            raise exceptions.InvalidArgumentValueError("Scoring pipeline start timestamp argument not provided.")

        if scoring_pipeline_run.end is None:
            raise exceptions.InvalidArgumentValueError("Scoring pipeline end timestamp argument not provided.")

        self.run['scoring'] = {
                'pipeline': scoring_pipeline_run.pipeline,
                'steps': [step.to_json_structure() for step in scoring_pipeline_run.steps],
                'status': scoring_pipeline_run.status,
                'start': scoring_pipeline_run.start,
                'end': scoring_pipeline_run.end,
                'random_seed': scoring_pipeline_run.random_seed,
            }

        if scoring_pipeline_run.is_failed():
            message = 'Scoring pipeline failed:\n{}'.format(
                scoring_pipeline_run.status['message']
            )
            self.status['state'] = metadata_base.PipelineRunStatusState.FAILURE.name
            if message is not None and message:
                self.status['message'] = message

    def set_scores(
        self, scores: container.DataFrame, metrics: typing.Sequence[typing.Dict], problem_description: problem.Problem,
    ) -> None:
        if 'results' not in self.run:
            self.run['results'] = {}

        if 'scores' not in self.run['results']:
            self.run['results']['scores'] = []

        for columns in scores.itertuples(index=False, name=None):
            metric, value = columns[0:2]

            self.run['results']['scores'].append(
                {
                    'metric': copy.deepcopy(self._get_metric(metric, metrics)),
                    'value': float(value),
                }
            )

    def _get_metric(self, metric: problem.PerformanceMetric, performance_metrics: typing.Sequence[typing.Dict]) -> typing.Dict:
        """
        Returns a metric description from a list of them, given metric.

        Parameters
        ----------
        metric : PerformanceMetric
            A metric name.
        performance_metrics : Sequence[Dict]
            A list of performance metric descriptions used.

        Returns
        -------
        Dict
            A metric description.
        """

        for performance_metric in performance_metrics:
            if performance_metric['metric'] == metric:
                metric_description = {
                    'metric': performance_metric['metric'].name,
                }

                if performance_metric.get('params', {}):
                    metric_description['params'] = performance_metric['params']

                return metric_description

        raise KeyError("Cannot find metric '{metric}' among those defined in the problem description.".format(metric=metric))

    def set_predictions(self, predictions: container.DataFrame) -> None:
        if not isinstance(predictions, container.DataFrame):
            return

        if 'results' not in self.run:
            self.run['results'] = {}

        if 'predictions' not in self.run['results']:
            self.run['results']['predictions'] = {}

        if not self.run['results']['predictions']:
            self.run['results']['predictions'] = {
                'header': [],
                'values': [],
            }

        column_names = []
        for column_index in range(len(predictions.columns)):
            # We use column name from the DataFrame is metadata does not have it. This allows a bit more compatibility.
            column_names.append(predictions.metadata.query_column(column_index).get('name', predictions.columns[column_index]))

            # "tolist" converts values to Python values and does not keep them as numpy.float64 or other special types.
            self.run['results']['predictions']['values'].append(predictions.iloc[:, column_index].tolist())

        self.run['results']['predictions']['header'] += column_names

    def get_id(self) -> str:
        return self._to_json_structure()['id']


class RuntimeEnvironment(dict):
    def __init__(
        self, *,
        worker_id: str = None,
        cpu_resources: typing.Dict[str, typing.Any] = None,
        memory_resources: typing.Dict[str, typing.Any] = None,
        gpu_resources: typing.Dict[str, typing.Any] = None,
        reference_benchmarks: typing.Sequence[str] = None,
        reference_engine_version: str = None,
        engine_version: str = None,
        base_docker_image: typing.Dict[str, str] = None,
        docker_image: typing.Dict[str, str] = None,
    ) -> None:
        """
        Create an instance of the runtime environment description in which a pipeline is run.

        Parameters
        ----------
        worker_id: str
            A globally unique identifier for the machine on which the runtime is running.
            The idea is that multiple runs on the same system can be grouped together.
            If not provided, `uuid.getnode()` is used to obtain an identifier.
        cpu_resources : typing.Dict[str, typing.Any]
            A description of the CPU resources available in this environment.
        memory_resources : typing.Dict[str, typing.Any]
            A description of the memory resources available in this environment.
        gpu_resources : typing.Dict[str, typing.Any]
            A description of the GPU resources available in this environment.
        reference_benchmarks : typing.Sequence[str]
            A list of ids of standard and optional additional benchmarks which were run in the same or
            equivalent RuntimeEnvironment. The timing characteristics of these benchmarks can be
            expected to be the same as anything timed in this RuntimeEnvironment.
        reference_engine_version : str
            A git commit hash or version number for the reference engine used. If subclassing the
            reference engine, list it here.
        engine_version : str
            A git commit hash or version number for the engine used. This is primarily useful for the
            author. If using the reference engine directly, list its git commit hash or version number
            here as well as in the reference_engine_version.
        base_docker_image : typing.Dict[str, str]
            If the engine was run in a public or known docker container, specify the base docker image
            description here.
        docker_image : typing.Dict[str, str]
            If the engine was run in a public or known docker container, specify the actual docker
            image description here. This is primarily useful for the author.
        """

        super().__init__()

        if worker_id is None:
            worker_id = self._get_worker_id()
        self['worker_id'] = worker_id

        resources = {}
        if cpu_resources is None:
            cpu_resources = self._get_cpu_resources()
        if cpu_resources is not None:
            resources['cpu'] = cpu_resources
        if memory_resources is None:
            memory_resources = self._get_memory_resources()
        if memory_resources is not None:
            resources['memory'] = memory_resources
        if gpu_resources is None:
            gpu_resources = self._get_gpu_resources()
        if gpu_resources is not None:
            resources['gpu'] = gpu_resources

        if resources:
            self['resources'] = resources

        if reference_benchmarks is not None:
            self['reference_benchmarks'] = reference_benchmarks

        if reference_engine_version is None:
            reference_engine_version = self._get_reference_engine_version()
        self['reference_engine_version'] = reference_engine_version

        if engine_version is None:
            engine_version = self['reference_engine_version']
        self['engine_version'] = engine_version

        if base_docker_image is None:
            base_docker_image = self._get_docker_image(
                environment_variables.D3M_BASE_IMAGE_NAME,
                environment_variables.D3M_BASE_IMAGE_DIGEST,
            )
        if base_docker_image is not None:
            self['base_docker_image'] = base_docker_image

        if docker_image is None:
            docker_image = self._get_docker_image(
                environment_variables.D3M_IMAGE_NAME,
                environment_variables.D3M_IMAGE_DIGEST,
            )
        if docker_image is not None:
            self['docker_image'] = docker_image

        self['id'] = utils.compute_hash_id(self)

    @classmethod
    def _get_reference_engine_version(cls) -> str:
        try:
            # Get the git commit hash of the d3m repository.
            path = os.path.abspath(d3m.__file__).rsplit('d3m', 1)[0]
            return utils.current_git_commit(
                path=path, search_parent_directories=False,
            )
        except git.exc.InvalidGitRepositoryError:
            return d3m.__version__

    @classmethod
    def _get_worker_id(cls) -> str:
        """
        Compute the worker id.
        """

        mac_address = uuid.getnode()

        if mac_address >> 16 == DOCKER_MAC_ADDRESS_MASK >> 16:
            # Docker generates MAC addresses in the range 02:42:ac:11:00:00 to 02:42:ac:11:ff:ff
            # if one is not provided in the configuration
            logger.warning(
                "'worker_id' was generated using the MAC address inside Docker "
                "container and is not a reliable compute resource identifier."
            )
        elif (mac_address >> 40) % 2 == 1:
            # uuid.getnode docs state:
            # If all attempts to obtain the hardware address fail, we choose a
            # random 48-bit number with its eighth bit set to 1 as recommended
            # in RFC 4122.
            logger.warning(
                "'worker_id' was generated using a random number because the "
                "MAC address could not be determined."
            )

        return str(uuid.uuid5(utils.HASH_ID_NAMESPACE, json.dumps(mac_address, sort_keys=True)))

    @classmethod
    def _get_docker_image(cls, image_name_env_var: str, image_digest_env_var: str) -> typing.Optional[typing.Dict]:
        """
        Returns the docker image description.
        """

        docker_image = {}

        if image_name_env_var not in os.environ:
            logger.warning('Docker image environment variable not set: %(variable_name)s', {
                'variable_name': image_name_env_var,
            })
        elif os.environ[image_name_env_var]:
            docker_image['image_name'] = os.environ[image_name_env_var]

        if image_digest_env_var not in os.environ:
            logger.warning('Docker image environment variable not set: %(variable_name)s', {
                'variable_name': image_digest_env_var,
            })
        elif os.environ[image_digest_env_var]:
            docker_image['image_digest'] = os.environ[image_digest_env_var]

        if docker_image:
            return docker_image
        else:
            return None

    @classmethod
    def _get_configured_available(cls, environment_variable: str) -> typing.Optional[str]:
        return os.environ.get(environment_variable, None)

    # TODO: Split into more methods.
    @classmethod
    def _get_cpu_resources(
        cls, *,
        devices: typing.Optional[typing.Sequence[str]] = None,
        physical_present: int = None, logical_present: int = None, configured_available: str = None,
        constraints: typing.Dict = None
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        cpu_resource: typing.Dict[str, typing.Any] = {}

        # Get cpus.
        cpus: typing.List[typing.Dict] = []
        cores = os.sched_getaffinity(0)
        with open('/proc/cpuinfo', 'r', encoding='ascii') as fp:
            cpu: typing.Dict = {}
            for line in fp:
                line = line.strip()
                if not line:
                    if cpu and int(cpu['processor']) in cores:
                        cpus.append(cpu)
                        cpu = {}
                else:
                    match = PROC_INFO_RE.match(line)
                    if match is None:
                        raise ValueError("Error parsing /proc/cpuinfo")
                    cpu[match.group(1)] = match.group(2)

        # devices
        if devices is None:
            try:
                # TODO is it possible to have multiple with the same model name?
                devices = list(set([cpu['model name'] for cpu in cpus]))
            except Exception as error:
                logger.warning('Failed to get CPU information.', exc_info=error)
        if devices is not None:
            cpu_resource['devices'] = [{'name': name} for name in devices]

        # physical_present
        if physical_present is None:
            try:
                physical_ids: typing.List = []
                physical_present = 0
                for cpu in cpus:
                    physical_id = cpu['physical id']
                    if physical_id in physical_ids:
                        continue
                    physical_ids.append(physical_id)
                    physical_present += int(cpu['cpu cores'])
            except Exception as error:
                logger.warning('Failed to get CPU information.', exc_info=error)
        if physical_present is not None:
            cpu_resource['physical_present'] = physical_present

        # logical_present
        if logical_present is None:
            try:
                logical_present = len(cpus)
            except Exception as error:
                logger.warning('Failed to get CPU information.', exc_info=error)
        if logical_present is not None:
            cpu_resource['logical_present'] = logical_present

        # configured_available
        if configured_available is None:
            configured_available = cls._get_configured_available(
                environment_variables.D3M_CPU,
            )
        if configured_available is not None:
            cpu_resource['configured_available'] = configured_available

        # constraints
        if constraints is None:
            try:
                cpu_shares = None
                with open(CGROUP_CPU_SHARES_PATH, 'r', encoding='ascii') as fp:
                    for line in fp:
                        line = line.strip()
                        cpu_shares = int(line)
                        is_limited_memory = cpu_shares < 1e5
                        if is_limited_memory:
                            cpu_shares = cpu_shares
                            break
                if cpu_shares is not None:
                    constraints = {
                        'cpu_shares': cpu_shares
                    }
            except Exception as error:
                logger.warning('Failed to get CPU information.', exc_info=error)
        if constraints is not None:
            cpu_resource['constraints'] = constraints

        if cpu_resource:
            return cpu_resource
        else:
            return None

    # TODO: Split into more methods.
    @classmethod
    def _get_memory_resources(
        cls, *,
        devices: typing.Sequence[typing.Dict[str, str]] = None, total_memory: int = None,
        configured_memory: str = None, constraints: typing.Dict = None
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        memory_resource: typing.Dict[str, typing.Any] = {}

        # devices
        # TODO get devices when None. Consider lshw.
        # if devices is None:
        #   get_devices()
        if devices is not None:
            memory_resource['devices'] = [{'name': name} for name in devices]

        # total_memory (bytes)
        if total_memory is None:
            try:
                with open(PROC_MEMORY_PATH, 'r', encoding='ascii') as fp:
                    for line in fp:
                        line = line.strip()
                        match = PROC_INFO_RE.match(line)
                        if match is None:
                            raise ValueError("Error parsing /proc/meminfo")
                        key, value = match.groups()
                        if key == PROC_TOTAL_MEMORY_KEY:
                            total_memory_kb = int(value.split()[0])
                            total_memory = total_memory_kb * 1024
            except Exception as error:
                logger.warning('Failed to get memory information.', exc_info=error)
        if total_memory is not None:
            memory_resource['total_memory'] = total_memory

        # configured_memory
        if configured_memory is None:
            configured_memory = cls._get_configured_available(
                environment_variables.D3M_RAM,
            )
        if configured_memory is not None:
            memory_resource['configured_memory'] = configured_memory

        # constraints
        if constraints is None:
            try:
                memory_limit = None
                with open(CGROUP_MEMORY_LIMIT_PATH, 'r', encoding='ascii') as fp:
                    for line in fp:
                        line = line.strip()
                        mem_bytes = int(line)
                        # TODO: Use highest positive signed 64-bit integer rounded down to
                        # multiples of the page size on the system instead of 9e15.
                        is_limited_memory = mem_bytes < 9e15
                        if is_limited_memory:
                            memory_limit = mem_bytes
                        break

                if memory_limit is not None:
                    constraints = {
                        'memory_limit': memory_limit
                    }
            except FileNotFoundError as error:
                logger.warning('Failed to get memory information.', exc_info=error)
        if constraints is not None:
            memory_resource['constraints'] = constraints

        if memory_resource:
            return memory_resource
        else:
            return None

    # TODO: Split into more methods.
    @classmethod
    def _get_gpu_resources(
        cls, *,
        devices: typing.Sequence = None, total_memory: int = None,
        configured_memory: str = None, constraints: typing.Dict = None
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        gpu_resource: typing.Dict[str, typing.Any] = {}

        # devices
        # TODO get devices when None. Consider lshw.
        # if devices is None:
        #   get_devices()
        if devices is None:
            return None
        else:
            gpu_resource['devices'] = [{'name': name} for name in devices]

        gpus: typing.List[GPUtil.GPU] = None
        try:
            gpus = GPUtil.getGPUs()
        except FileNotFoundError as error:
            logger.warning('Failed to get GPU information.', exc_info=error)
            return None

        # total_memory (bytes)
        if total_memory is None:
            try:
                total_memory_mib = sum(gpu.memoryTotal for gpu in gpus)
                total_memory = int(total_memory_mib) * 2**20
            except FileNotFoundError as error:
                logger.warning('Failed to get GPU information.', exc_info=error)
        if total_memory is not None:
            gpu_resource['total_memory'] = total_memory

        # configured_memory
        # There is currently no limit on GPU memory through configuration.
        if configured_memory is None:
            if 'total_memory' in gpu_resource:
                configured_memory = str(gpu_resource['total_memory'])
        if configured_memory is not None:
            gpu_resource['configured_memory'] = configured_memory

        # constraints
        # TODO get devices when None.
        # if constraints is None:
        #   get_constraints()
        if constraints is not None:
            gpu_resource['constraints'] = constraints

        if gpu_resource:
            return gpu_resource
        else:
            return None

    @classmethod
    def _yaml_representer(cls, dumper: yaml.Dumper, data: typing.Any) -> typing.Any:
        return dumper.represent_dict(data)


yaml.Dumper.add_representer(RuntimeEnvironment, RuntimeEnvironment._yaml_representer)
yaml.SafeDumper.add_representer(RuntimeEnvironment, RuntimeEnvironment._yaml_representer)
