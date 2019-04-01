import subprocess

import click

from r2c.cli.commands.cli import cli
from r2c.cli.create_template import create_template_analyzer
from r2c.cli.logger import get_logger, print_success
from r2c.cli.util import get_default_org


def _get_git_author():
    try:
        git_name = (
            subprocess.check_output(["git", "config", "--get", "user.name"])
            .decode("utf-8")
            .strip()
        )
        git_email = (
            subprocess.check_output(["git", "config", "--get", "user.email"])
            .decode("utf-8")
            .strip()
        )
        return (git_name, git_email)
    except Exception as e:
        get_logger().info(e)
        return (None, None)


@cli.command()
@click.option("--analyzer-name")
@click.option("--author-name")
@click.option("--author-email")
@click.option("--run-on")
@click.option("--output-type")
@click.pass_context
def init(ctx, analyzer_name, author_name, author_email, run_on, output_type):
    """
    Creates an example analyzer for analyzing JavaScript/TypeScript.

    You may use any language to write your analysis and run it from `src/analyze.sh`.

    Once you create your analyzer, you can navigate to your analyzer directory
    and run 'r2c' commands inside that directory.

    Type `r2c -—help` to see all of the commands available.
    """
    default_name, default_email = _get_git_author()
    if not analyzer_name:
        analyzer_name = click.prompt("Analyzer name", default="example")
    if not author_name:
        author_name = click.prompt("Author name", default=default_name)
    if not author_email:
        author_email = click.prompt("Author email", default=default_email)
    if not run_on:
        run_on = click.prompt(
            "Will your analyzer produce: \n"
            + "- output for a particular `git` repository\n"
            + "- output for a particular git `commit` in a repo\n"
            + "- the same `constant` output regardless of commit or repo?",
            default="commit",
            type=click.Choice(["git", "commit", "constant"]),
        )
    if not output_type:
        output_type = click.prompt(
            "Does your analyzer output \n"
            + "- a single schema-compliant JSON file \n"
            + "- a full filesystem output?",
            default="json",
            type=click.Choice(["json", "filesystem"]),
        )
    create_template_analyzer(
        get_default_org(), analyzer_name, author_name, author_email, run_on, output_type
    )
    print_success(f"Done! Your analyzer can be found in the {analyzer_name} directory")
