"""
Project setup
"""
from distutils.core import setup

setup(
    name='ypersms_client',
    packages=['ypersms_client'],
    version='0.1',
    license='MIT',
    description='Public client for YperSMS api, written in python',
    author='Yper',
    author_email='dev@yper.fr',
    url='https://github.com/yperteam/ypersms_client-python',
    download_url='https://github.com/yperteam/ypersms_client-python/archive/0.1.tar.gz',
    keywords=['api-client', 'ypersms', 'yper', 'sms'],
    install_requires=[
        'requests',
        'nose',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
