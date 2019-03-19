from setuptools import setup, find_packages

setup(
    name='deepcheck',
    packages=find_packages(),
    description='Build and release task for determining neural network susceptibility to adversarial machine learning',
    long_description=open('README.md').read().strip(),
    version='0.12',
    url='',
    license='GPL',
    author='TeamDeepCheck',
    install_requires=['numpy', 'scipy', 'six', 'scikit-learn', 'Adversarial-Robustness-Toolbox==0.5.0', 'keras', 'tensorflow', 'Pillow', 'BeautifulTable'],
    author_email='',
    keywords=['pip','adversarial machine learning','deep learning']
    )