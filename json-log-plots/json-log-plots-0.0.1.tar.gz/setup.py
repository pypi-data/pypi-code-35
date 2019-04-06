from setuptools import setup


setup(
    name='json-log-plots',
    version='0.0.1',
    packages=['json_log_plots'],
    install_requires=[
        'json_lines',
        'filelock',
        'matplotlib',
    ],
    author='Konstantin Lopuhin',
    author_email='kostia.lopuhin@gmail.com',
    url='https://github.com/lopuhin/json-log-plots',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
