from setuptools import setup

setup(
    name='merakiv2',
    version='v2.0',
    packages=['merakiv2'],
    url='https://github.com/nielsvanhooy/dashboard-api-python',
    download_url = 'https://github.com/nielsvanhooy/dashboard-api-python/archive/v2.0.tar.gz',
    keywords = ['Meraki', 'SD-WAN', 'Meraki API'],
    license='MIT',
    author='hooij804',
    author_email='nielsvanhooy@gmail.com',
    description='updated python library for use with dashboard. original python api made by Shiyue Cheng',
    install_requires=[
        'requests',
    ],
)
