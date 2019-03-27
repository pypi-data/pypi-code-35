from setuptools import setup, find_packages

setup(
    name="statsd_mangler",
    version="0.1.3",
    packages=find_packages(),
    install_requires=['toml>=0.10.0'],
    entry_points = {
        'console_scripts': ['statsd_mangler=statsd_mangler.__main__:main']
    },
    author="Carl Flippin",
    author_email="cflippin@opentable.com",
    description="Namespace mangler for statsd metrics",
    license="MIT",
    url="https://github.com/opentable/statsd_mangler"
)
