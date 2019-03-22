from setuptools import setup

setup(
    version='0.1.1',
    name='jupyter_pytest',
    author='Olav Vahtras',
    author_email='olav.vahtras@gmail.com',
    url='https://github.com/vahtras/jupyter-pytest',
    modules='jupytest',
    requires=['jupyter', 'pytest'],
)
