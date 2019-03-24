import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discord-rpc.py",
    url='https://gitlab.com/somberdemise/discord-rpc.py',
    version="1.0.1",
    author="Gustavo (somberdemise)",
    author_email="gustavo@gustavo.dev",
    description="A Discord Rich Presence library for Python 2 & 3",
    license='Mozilla Public License 2.0 (MPL 2.0)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'discord_rpc',
        'discord_rpc.codes',
        'discord_rpc.connection',
        'discord_rpc.util'
    ],
    platforms=[
        'Windows',
        'Linux',
        'OSX'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",

        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
)
