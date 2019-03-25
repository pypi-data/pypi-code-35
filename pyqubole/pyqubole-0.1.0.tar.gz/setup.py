from distutils.core import setup

setup(
        name='pyqubole',
        version='0.1.0',
        author='Wesley Goi',
        author_email='picy2k@gmail.co',
        packages=['qubole'],
        scripts=['bin/qubole'],
        description='Managing qubole clusters',
        long_description=open('README.md').read(),
)
