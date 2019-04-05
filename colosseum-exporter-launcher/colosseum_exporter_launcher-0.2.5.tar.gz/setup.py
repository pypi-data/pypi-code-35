from setuptools import setup, find_packages

setup(
    name='colosseum_exporter_launcher',
    version='0.2.5',
    description='launches exporters for colosseum via docker container',
    author='Marc',
    author_email='marc@42maru.com',
    url='https://github.com/42maru/colosseum_exporter_launcher',
    download_url='https://github.com/42maru/colosseum_exporter_launcher/archive/master.zip',
    packages=find_packages('colosseum_exporter_launcher'),
    keywords=['colosseum', 'prometheus', 'exporter'],
    python_requires='>=3.5',
    license='MIT',
    install_requires=[
        'requests==2.21.0',
        'click==7.0'
    ],
    long_description=open('README.md').read(),
    scripts=['./colosseum_exporter_launcher/launcher.py']
)
