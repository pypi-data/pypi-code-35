from setuptools import setup

setup(
    name='dipr',
    version='1.0dev',
    packages=['Repos', 'Errors', 'Commands', 'Settings', 'Arguments', 'Protocols', 'Protocols.Hg', 'Protocols.Hg.hglib',
              'Protocols.Git', 'Utilities'],
    package_dir={'': 'dipr'},
    url='http://www.dipr.dev',
    license='MIT',
    author='ZaXa Software, LLC',
    author_email='info@zaxasoft.com',
    description='A revision control independent dependency and sub-repository management package.',
    package_data={
        'Templates': ['dipr/Templates/*.yaml']
    },
    include_package_data=True,
    install_requires=[
        'ruamel-yaml',
        'gitpython'
    ]
)