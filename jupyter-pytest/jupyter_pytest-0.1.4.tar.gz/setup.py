from setuptools import setup

setup(
    version='0.1.4',
    name='jupyter_pytest',
    author='Olav Vahtras',
    author_email='olav.vahtras@gmail.com',
    url='https://github.com/vahtras/jupyter-pytest',
    py_modules=['jupytest'],
    install_requires=['jupyter', 'pytest'],
)
