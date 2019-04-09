VERSION = '0.0.2'

try:
    from setuptools import setup,  find_packages
except ImportError:
    from distutils.core import setup, find_packages

import os
import re

with open('README.md', 'r') as f:
    readme = f.read()

def order_versions(versions):
    '''
    Order a list of x.y.z version strings from lowest to highest
    '''
    return [".".join(v) for v in sorted(
        [v.split('.') for v in versions],
        key=lambda x:(int(x[0]), int(x[1]), int(x[2]))
    )]

def get_version():
    '''
    Retrieve the current version number from the most recent entry in CHANGELOG
    or fallback to the global VERSION variable.
    '''
    backup_version = VERSION
    all_versions = []
    if os.path.exists('CHANGELOG.md'):
        with open("CHANGELOG.md", "r") as cl:
            for line in cl.readlines():
                pattern = re.compile(r'\[\d+\.\d+\.\d+\]')
                match = pattern.search(line)
                if match:
                    all_versions.append(
                        match.string[match.start()+1:match.end()-1]
                    )
    if len(all_versions) > 0:
        if backup_version not in all_versions:
            all_versions.append(backup_version)
        return order_versions(all_versions)[-1]
    else:
        return backup_version

setup(
    name='gynx',
    version=get_version(),
    description='Google Drive sync client for Linux',
    license='GPL',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Matthew Levy',
    author_email='matt@webkolektiv.com',
    url='https://gitlab.com/ml394/gynx.git',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'dictdiffer==0.7.1',
        'google-api-python-client==1.7.4',
        'google-auth==1.6.1',
        'google-auth-httplib2==0.0.3',
        'httplib2==0.12.0',
        'oauth2client==4.1.3',
        'pyasn1==0.4.4',
        'pytz==2018.7',
    ],
    scripts=['bin/gynx', 'bin/gynx_run.py'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Filesystems'
    ]
)
