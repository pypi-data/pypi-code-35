import setuptools

setuptools.setup(
    name='susy-tester',
    version='0.0.1',
    license='MIT',
    description='Testador de soluções para o SuSy da UNICAMP',
    author='Lucas Valente',
    author_email='lucasvvop@hotmail.com',
    url='https://www.github.com/serramatutu/susy-tester',
    packages=['susytester'],
    install_requires=['termcolor', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)