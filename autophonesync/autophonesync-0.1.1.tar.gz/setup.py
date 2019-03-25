# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name='autophonesync',
    version='0.1.1',
    description='Automatically backup phone on plug in',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/astronouth7303/phonesync',
    author='Jamie Bliss',
    author_email='jamie@ivyleav.es',
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='android backup udev systemd',  # Optional
    packages=['autophonesync'],  # Required
    python_requires='>=3.5',
    install_requires=[
        'click',
    ],
    extras_require={  # Optional
    },
    entry_points={  # Optional
        'console_scripts': [
            'autophonesync=autophonesync.cli:phonesync',
            'autophonesync-udev-handler=autophonesync.udev_handler:main',
        ],
    },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Bug Reports': 'https://gitlab.com/astronouth7303/phonesync/issues',
        'Tips': 'https://ko-fi.com/astraluma',
    },
)
