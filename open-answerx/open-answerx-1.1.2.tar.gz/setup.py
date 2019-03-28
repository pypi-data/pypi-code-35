from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='open-answerx',
    version='1.1.2',
    description='{OPEN} client for AnswerX Cloud and Managed',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Diego Xirinachs',
    author_email='dxirinac@akamai.com',
    scripts=['open-answerx.py'],
    url='https://developer.akamai.com/api/network_operator/answerx/v1.html',
    namespace_packages=['akamai'],
    packages=find_packages(),
    python_requires=">=2.7.10",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'edgegrid-python'
    ],
    license='LICENSE.txt'

)
