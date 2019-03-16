"""Setup file
"""


import setuptools
import pyperbolic


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='pyperbolic',
                 version=pyperbolic.__version__,
                 description='Hyperbolic geometry in Python',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=pyperbolic.__github_url__,
                 author='James W. Kennington',
                 author_email='jameswkennington@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)
