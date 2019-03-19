from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='BioMatcher',
    version='1.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/cmencar/bio-01",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Antonio Donvito",
    author_email="a.donvito20@studenti.uniba.it",
    description="BioMatcher helps you find microRNAs with the same seed",
)

# setup(
#     name='Matcher',
#     version='1.0',
#     py_modules=['matcher', 'filter', 'cleaner'],
#     install_requires=[
#         'Click',
#         'biopython',
#         'tqdm',
#         'pandas',
#     ],
#     entry_points='''
#         [console_scripts]
#         matcher=UserInterface:userinterface
#         filter=Filter:filtering
#         cleaner=Cleaner:cleaning
#     ''',
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     url="https://github.com/cmencar/bio-01",
#     packages=find_packages(),
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     author="Antonio Donvito",
# )

