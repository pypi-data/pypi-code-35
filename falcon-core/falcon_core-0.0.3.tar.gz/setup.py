from setuptools import setup, find_packages

setup(
    name='falcon_core',
    version='0.0.3',
    description='Falcon Core Inspired by Django for Falcon API Framework.',
    author='Maksym Sichkaruk',
    author_email='maxim.18.08.1997@gmail.com',
    url='https://github.com/Maksych/falcon_core',
    packages=find_packages(
        include=['falcon_core.*', 'falcon_core'],
        exclude=['tests.*', 'tests'],
    ),
    include_package_data=True,
    scripts=['falcon_core/bin/falcon-core.py'],
    entry_points={'console_scripts': [
        'falcon-core = falcon_core.management:execute_from_command_line',
    ]},
    zip_safe=False,
    install_requires=['falcon', 'mongoengine', 'waitress', 'gunicorn'],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
