__author__ = 'degibenz'

from setuptools import setup, find_packages

setup(
    name="aio_swagger",
    version="0.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pyyaml', 'jinja2', 'aiohttp'],
    author="Alexey Shkil",
    author_email="aleksey.shkil@homecredit.ru",
    url="https://gitlab.homecred.it/internal/aio-swagger"
)
