import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from invoke import task

from .utils.pipenv import Pipenv
from .utils.print import print_action

ALEMBIC_CONFIG = "alembic.ini"
ALEMBIC_TABLE_PREFIX = "alembic_version_cs_"
PROJECT_LIBS_PATH = Path(os.environ["CS_PROJECT_LIBS_PATH"])


def _init(lib_name, alembic_config_path):
    """Runs alembic revisions from the specified library."""
    alembic_table = ALEMBIC_TABLE_PREFIX + lib_name.split("-")[1]
    os.environ["CS_DB_ALEMBIC_TABLE"] = alembic_table
    alembic_config = Config(alembic_config_path)

    script_location = Path(alembic_config.get_main_option("script_location"))
    if not script_location.is_absolute():
        script_location = Path(alembic_config_path.parent, script_location)
        alembic_config.set_main_option("script_location", str(script_location))

    from civilservant.util import init_db_engine
    with init_db_engine().begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")
    

@task
def init(c, lib=[]):
    """Runs alembic revisions from CivilServant libraries if present."""
    pipenv = Pipenv(c, exit_on_error=True)
    pipenv.ensure_active()

    libs_path = Path(pipenv.root_path, PROJECT_LIBS_PATH)
    if not lib:
        lib = [path.name for path in libs_path.iterdir()]
    for arg in lib:
        alembic_config_path = Path(libs_path, arg, ALEMBIC_CONFIG)
        if alembic_config_path.exists():
            print_action(f"Running revisions for {arg}")
            _init(arg, alembic_config_path)

