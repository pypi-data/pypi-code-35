from setuptools import setup

setup(
    name='lever-jwt',
    version='0.1.4',
    description='lever jwt implementation',
    license='MIT',
    packages=['lever_jwt'],
    author='Fashola Ayodeji',
    author_email='fashtop3@gmail.com',
    keywords=['lever-auth'],
    url='https://github.com/fashtop3/lever-jwt.git',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyjwt==1.5.3',
        'flask',
    ]
)
