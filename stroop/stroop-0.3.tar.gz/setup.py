from setuptools import setup, find_packages

setup(
    name='stroop',
    version='0.3',
    description='a package for stroop stimuli',
    keywords='cognitive science',
    url='https://github.com/qihongl/stroop-stimuli',
    author='Qihong Lu',
    author_email='qlu@princeton.edu',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    zip_safe=False
)
