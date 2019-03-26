import os, json


def run_file(directory:str)->str:
    return os.path.join(directory, 'run.json')

def config_file(directory:str)->str:
    return os.path.join(directory, 'config.json')

def has_config_file(directory:str)->bool:
    return os.path.isfile(config_file(directory))

def has_run_file(directory:str)->bool:
    return os.path.isfile(run_file(directory))

def get_json(directory:str, which:str='config')->dict:
    file_fn = run_file if which == 'config' else config_file
    with open(file_fn(directory), 'r') as f:
        return json.read(f)

def run_status(directory:str)->bool:
    if not has_run_file(directory): return
    return get_json(directory, 'run')['status']


def is_run_completed(directory:str) -> bool:
    return run_status(directory) == 'COMPLETED'

def is_run_running(run_file:str) -> bool:
    return run_status(directory) == 'RUNNING'

def is_sacred_expirment(directory:str)->bool:
    return (
        os.path.isdir(directory)
        and has_run_file(directory)
        and has_config_file(directory)
    )

def gather_experiments(experiments_dir:str)->list:
    return [
        _dir
        for _dir in os.path.listdir(experiments_dir)
        if is_sacred_expirment(os.path.join(experiments_dir, _dir))
    ]

def is_rerun(config:dict, experiment_dir) -> bool:
    if is_sacred_expirment(experiment_dir):
        other_config = get_json(experiment_dir, 'config')
        if other_config != config: return False
        if is_run_running(run_file) or is_run_completed(run_file): return True
    return False
