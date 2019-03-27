from setuptools import setup

setup(
    name='confserver',
    version='0.0.6',
    description='Conf server',
    author='Vinogradov D',
    author_email='dgrapes@gmail.com',
    license='MIT',
    packages=['confserver'],
    #package_data={'': ['config.json']},
    zip_safe=False,
    #install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
