import os
import re
import subprocess
from pathlib import Path
from sys import argv

import click
import nbformat
from nbconvert import PythonExporter
from shlex import quote
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
    if os.name == 'nt':
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
    else:
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
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
    setup_file = Path.cwd() / 'setup.py'
    notebook_file = (folder / filename).with_suffix('.ipynb')
    print(notebook_file)
    python_file = notebook_file.with_suffix('.py')
    stem = notebook_file.stem
    if not setup_file.exists():
        setup_file.write_text(setup_base)

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

    version_path = folder / f'dist/*{version}*'

    # Black the code so it's in a consistent format
    # cmd_black_setup = ['black', '\"{str(setup_file)}\"']
    # cmd_black = f'black \"{str(python_file)}\"'

    # Build wheel and upload to PyPI
    # cmd_setup = f"python \"{str(setup_file)}\" sdist bdist_wheel"
    # cmd_twine = f'twine upload \"{folder} / dist/*{version}*\" -u "{pypi_username}" -p "{password}"'

    # Run all processes
    if os.name == 'nt':
        subprocess.run(['black', str(setup_file)], stdout=subprocess.PIPE)
        subprocess.run(['black', str(python_file)], stdout=subprocess.PIPE)
        subprocess.run(['python', f'{str(setup_file)}', 'sdist', 'bdist_wheel'], stdout=subprocess.PIPE)
        subprocess.run(['twine', 'upload', str(version_path), '-u', pypi_username, '-p', password], stdout=subprocess.PIPE)
    else:
        subprocess.run(['black', quote(str(setup_file))], stdout=subprocess.PIPE)
        subprocess.run(['black', quote(str(python_file))], stdout=subprocess.PIPE)
        subprocess.run(['python', quote(str(setup_file)), 'sdist', 'bdist_wheel'], stdout=subprocess.PIPE)
        subprocess.run(['twine', 'upload', quote(str(version_path)), '-u', f'"{pypi_username}"', '-p', f'"{password}"'], stdout=subprocess.PIPE)

    # (cmd_black_setup)
    # run_process(cmd_black)
    # run_process(cmd_setup)
    # run_process(cmd_twine)

    print(f"Updated to version {version}")


if __name__ == "__main__":
    main()
