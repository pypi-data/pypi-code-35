from setuptools import setup

setup(
    name='micropython-mlx90615',
    version='1.2',
    packages=['mlx90615', 'mlx90615.examples'],
    #package_dir = {'djangoforandroid': 'djangoforandroid'},

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/espressoide/micropython-mlx90615/downloads/',

    install_requires=[],

    license='GNU GPL',
    description="Micropython scripts for use MLX90615 temperatures sensors.",
    #    long_description = README,

    classifiers=[
        # 'Environment :: Web Environment',
        # 'Framework :: Django',
    ],

)
