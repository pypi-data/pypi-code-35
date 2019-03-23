import click
import json
import os
from pathlib import Path

from cookiecutter_project_upgrader.logic import update_project_template_branch


@click.command()
@click.option('--context-file', '-c', type=click.Path(file_okay=True, readable=True, allow_dash=True),
              default="docs/cookiecutter_input.json", help="Default: docs/cookiecutter_input.json")
@click.option('--branch', '-b', default="cookiecutter-template", help="Default: cookiecutter-template")
@click.option('--merge-now', '-m', is_flag=True, default=False, help="Execute a git merge after a successful update")
def main(context_file: str, branch: str, merge_now: bool):
    """Upgrade projects created from a Cookiecutter template"""
    context = _load_context(context_file)
    project_directory = os.getcwd()
    update_project_template_branch(context, project_directory, branch, merge_now)


def _load_context(context_file: str):
    context_str = Path(context_file).read_text(encoding="utf-8")
    context = json.loads(context_str)
    return context
