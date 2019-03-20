import toml


def get_entrypoint(taskdef):
    return toml.load(taskdef)["task"]["entrypoint"]


def get_workdir(taskdef):
    return toml.load(taskdef)["task"]["workdir"]


def returns_files(taskdef):
    return "data_dir" in toml.load(taskdef)["task"]["requires"]