from azureml.core import Experiment
from datetime import datetime
from .mock_objects import MockPipelineRun


def print_graph(graph):
    print("GRAPH [%s]" % str(graph))
    for node in graph.nodes:
        print("node: %s" % node.name)
        for i in node.inputs:
            if i.incoming_edge is not None:
                input_name = i.name
                output_name = i.incoming_edge.source_port.name
                print("%s <- %s" % (input_name, output_name))


start_checkpoint = None


def print_elapsed():
    global start_checkpoint
    if start_checkpoint is None:
        start_checkpoint = datetime.now()
    elapsed = datetime.now() - start_checkpoint
    print(elapsed.seconds, "secs ")


def print_run_logs(pipeline_run):
    step_runs = pipeline_run.get_children()
    for step_run in step_runs:
        status = step_run.get_status()
        print('node', step_run._node_id, 'status:', status)
        if status == "Failed" or status == "Finished":
            joblog = step_run.get_job_log()
            print('job log:', joblog)
            stdout_log = step_run.get_stdout_log()
            print('stdout log:', stdout_log)
            stderr_log = step_run.get_stderr_log()
            print('stderr log:', stderr_log)


def download_pipeline_run_outputs(pipeline_run, file_path):
    step_runs = pipeline_run.get_children()
    for step_run in step_runs:
        status = step_run.get_status()
        print('node', step_run._node_id, 'downloading outputs')

        if status == "Finished":
            output_port_runs = step_run.get_outputs().values()

            for output_port_run in output_port_runs:
                path = file_path + "\\" + step_run._node_id + "_" + output_port_run.name
                port_data = output_port_run.get_port_data_reference()
                port_data.download(path)

            print('got outputs')


def submit_pipeline(pipeline, dry_run=False, pipeline_parameters=None):
    print_graph(pipeline.graph)

    print_elapsed()
    print("RUN [%s]" % str(pipeline._name))
    if not dry_run:
        experiment = Experiment(pipeline._graph_context._workspace, 'helloworld')
        pipeline_run = experiment.submit(pipeline, regenerate_outputs=True)
    else:
        if not pipeline.graph._finalized:
            pipeline.graph.finalize()
        pipeline_run_id = pipeline.graph._graph_provider.submit(
            pipeline.graph,
            continue_on_step_failure=False,
            experiment_name=pipeline._graph_context._experiment_name,
            pipeline_parameters=pipeline_parameters)
        pipeline_run = MockPipelineRun(context=pipeline._graph_context, run_id=pipeline_run_id)
    return pipeline_run


def run_pipeline(pipeline, verbose=False, download_outputs=False, file_path=None, dry_run=False,
                 pipeline_parameters=None):
    pipeline_run = submit_pipeline(pipeline, dry_run, pipeline_parameters)
    pipeline_run.wait_for_completion()
    status = pipeline_run.get_status()

    if status == "Failed" or verbose:
        print_run_logs(pipeline_run)

    if status == "Finished" and download_outputs:
        download_pipeline_run_outputs(pipeline_run, file_path)

    return status


def validate_and_run_pipeline(pipeline, dry_run=True, pipeline_parameters=None):
    errors = pipeline.validate()
    assert (len(errors) == 0)

    run_pipeline(pipeline, dry_run=dry_run, pipeline_parameters=pipeline_parameters)
