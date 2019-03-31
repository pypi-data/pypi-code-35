from .cli import CLI
from .commands import CreateProject

cli = CLI()

cli.add_command(CreateProject, 'create')
