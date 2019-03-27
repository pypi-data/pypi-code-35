from pathlib import Path

from invoke import task

PROJECT_ROOT_PATH = Path(__file__).parents[2]
PROJECT_DIST_PATH = Path(PROJECT_ROOT_PATH, "dist", "*")
PYPI_URL_PROD = "https://upload.pypi.org/legacy/"
PYPI_URL_TEST = "https://test.pypi.org/legacy/"


@task
def compile(ctx):
    """Compile the current library for distribution."""
    with ctx.cd(str(BASE_PATH)): 
        ctx.run("python3 setup.py sdist bdist_wheel")


@task
def publish(ctx, prod=False):
    """Publish the current library to PyPI."""
    url = PYPI_URL_PROD if prod else PYPI_URL_TEST
    with ctx.cd(str(BASE_PATH)): 
        cmd = f"twine upload --repository-url {url} {str(PROJECT_DIST_PATH)}"
        ctx.run(cmd)

