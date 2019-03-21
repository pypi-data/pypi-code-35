from distutils.core import setup

setup(
    name='dataFrameWrapper',  # How you named your package folder (MyLib)
    packages=['dataFrameWrapper'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Package wrapper of dataframes',  # Give a short description about your library
    author='ali rahmani',  # Type in your name
    author_email='institut.ali53@gmail.com',  # Type in your E-Mail
    url='https://github.com/rahmaniali/dataFrameWrapper.git',  # Provide either the link to your github or to your website
    download_url='https://github.com/rahmaniali/dataFrameWrapper/archive/v0.1.tar.gz',  # I explain this later on
    keywords=['dataframes', 'pandas', 'wrapper'],  # Keywords that define your package best
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
