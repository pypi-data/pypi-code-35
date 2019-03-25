from setuptools import setup


setup(
    name = 'devtracker',
    version = '0.1.0',
    author="ConSou",
    author_email="conorsouhrada@gmail.com",
    description="A simple way to track time spent working on projects.",
    url="https://github.com/ConSou/devtracker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = ['devtracker'],
    entry_points = {
        'console_scripts': [
            'devtracker = devtracker.__main__:main',
            'dt = devtracker.__main__:main'
        ]
    })
