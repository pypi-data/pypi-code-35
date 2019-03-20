from distutils.core import setup

setup(
    name='ybc_history',
    version='1.0.6',
    description='Get history of today',
    long_description='Get today historical events',
    author='mengxf',
    author_email='mengxf01@fenbi.com',
    keywords=['pip3', 'history', 'python3', 'python'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_history'],
    package_data={'ybc_history': ['*.py']},
    license='MIT',
    install_requires=[
        'ybc_config',
        'ybc_exception',
        'requests'
    ],
)
