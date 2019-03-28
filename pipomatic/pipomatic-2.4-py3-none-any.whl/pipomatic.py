import os
import re
import subprocess
from pathlib import Path
from sys import argv

import click
import nbformat
from nbconvert import PythonExporter
from traitlets.config import Config

def update_setup(stem, username, setup_base):
    # Update the setup file by amending the filename, author and py_modules
    setup_file = Path.cwd() / 'setup.py'

    if not setup_file.exists():
        setup_file.write_text(setup_base)

    setup_text = setup_file.read_text()

    # Set the name of the file to the name of the notebook
    name = re.search(r'name=\"(.*)\",', setup_text).group(1)
    setup_text = setup_text.replace(f'name="{name}"', f'name="{stem}"')

    # Set author to the PyPI username it will be published to
    author = re.search(r'author=\"(.*)\",', setup_text).group(1)
    setup_text = setup_text.replace(f'author="{author}"', f'author="{username}"')

    # Set py_modules is set to the name of the notebook file
    pymod = re.search(r'py_modules=\[\"(.*)\"\],', setup_text).group(1)
    setup_text = setup_text.replace(f'py_modules=["{pymod}"', f'py_modules=["{stem}"')

    # Increment the version number by 0.1
    version = float(re.search(r'version=\"(.*)\",', setup_text).group(1))
    new_version = version + .1
    new_version = f'{new_version:0.1f}'
    setup_text = setup_text.replace(f'version="{version}"', f'version="{new_version}"')
    
    # Save the setup file
    setup_file.write_text(setup_text)
    return new_version, setup_text


def run_process(cmd):
    # Run the CLI processes that black the code and push it to PyPI
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
    process.wait()
    return 'Success'


def build_config():
    # Modify the notebook by removing all cells not marked with build or test and remove output
    c = Config()
    c.PythonExporter.preprocessors = ['nbconvert.preprocessors.TagRemovePreprocessor']
    c.TemplateExporter.exclude_output=True
    c.TagRemovePreprocessor.remove_cell_tags=['build', 'test']
    return c

# The base configuration for the setup module
setup_base = """
import setuptools

setuptools.setup(
    name="",
    version="0.0",
    author="",
    author_email="",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    py_modules=[""],
    install_requires=[
        ""
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
"""


@click.command()
@click.argument('filename')
@click.option('--pypi_username', prompt='Enter your PyPI username')
@click.option('--password', 
              prompt='Enter your PyPI password', 
              hide_input=True,
              confirmation_prompt=False)
def main(filename, pypi_username, password):
    
    # Setup folders and files
    folder = Path.cwd()
    notebook_file = (folder / filename).with_suffix('.ipynb')
    print(notebook_file)
    python_file = notebook_file.with_suffix('.py')
    stem = notebook_file.stem
    if not (folder / 'setup.py').exists():
        (folder / 'setup.py').write_text(setup_base)

    # Read notebook content into nb variable
    notebook_json = notebook_file.read_text()
    nb = nbformat.reads(notebook_json, as_version=4)

    # Export notebook cells that are not tagged as test or build
    c = build_config()
    exporter = PythonExporter(config=c)
    code = exporter.from_notebook_node(nb)[0]

    # Write the exported cells to a Python file
    (folder / python_file).write_text(code)
    version, updated_setup_text = update_setup(stem, pypi_username, setup_base)

    # Black the code so it's in a consistent format
    cmd_black = f"black {python_file}"
    cmd_black_setup = f"black setup.py"

    # Build wheel and upload to PyPI
    cmd_setup = f"python setup.py sdist bdist_wheel"
    cmd_twine = f'twine upload dist/*{version}* -u "{pypi_username}" -p "{password}"'

    # Run all processes
    run_process(cmd_black_setup)
    run_process(cmd_black)
    run_process(cmd_setup)
    run_process(cmd_twine)

    print(f"Updated to version {version}")


if __name__ == "__main__":
    main()
