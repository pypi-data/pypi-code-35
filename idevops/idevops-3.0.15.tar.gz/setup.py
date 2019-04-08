"""
Build iost net within one key.
"""
from setuptools import find_packages, setup
from idevops import VERSION

dependencies = [
    'ansible',
    'boto3',
    'click',
    'ptable',
]

from os import path
from io import open
this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='idevops',
    version=VERSION,
    url='https://github.com/iost-official/idevops',
    license='LGPLv3+',
    author='Yuanyi',
    author_email='yuanyi@iost.io',
    description='Build iost net within one button.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'idevops = idevops.cli:main',
            'ido = idevops.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
