from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='redis-tracker',
    version='1.0',
    py_modules=['tracker'],
    url='https://gitlab.com/granitosaurus/redis-tracker',
    license='GPLv3',
    author='granitosaurus',
    author_email='bernardas.alisauskas@gmail.com',
    description='simple redis key tracker for stdout and prometheus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'click',
        'redis',
    ],
    entry_points="""
        [console_scripts]
        redis-tracker=tracker:main
    """,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
